#!/usr/bin/env bash
#
# ensure-hax.sh — SessionStart hook for the HAX onboarding Claude Code plugin.
#
# Makes sure the HAX CLI (`hax`, shipped by @haxtheweb/create) is available.
#   - If `hax` is already on PATH, reports its version and exits.
#   - If a local development copy is detected, reports and exits (no global install).
#   - If it is missing, installs @haxtheweb/create globally with npm.
#
# Opt out of auto-install:  export HAX_PLUGIN_NO_AUTOINSTALL=1
# Override the local dev path:  export HAX_DEV_PATH=/path/to/create
#
# This hook is best-effort and always exits 0. Anything it prints on stdout is surfaced
# to Claude as session context so the assistant knows whether the CLI is ready.
# Note: the host may still wait while this runs, and execution is bounded by the hook timeout.

set -uo pipefail

MANUAL_INSTALL="npm install --global @haxtheweb/create"

# Local development checkout path (overridable via HAX_DEV_PATH).
HAX_DEV_PATH="${HAX_DEV_PATH:-/home/bto108a/Documents/git/haxtheweb/create}"

# --- Already installed? Report and bail. ------------------------------------
if command -v hax >/dev/null 2>&1; then
  hax_path="$(command -v hax 2>/dev/null)"

  # Check if hax resolves to a path under the local dev checkout (npm link / local install).
  case "$hax_path" in
    "$HAX_DEV_PATH"*)
      echo "HAX CLI available via local development copy ($hax_path) — skipping global install."
      exit 0
      ;;
  esac

  # Also check if the local dev dist exists even if hax resolves elsewhere
  # (the local copy may be on PATH via a different mechanism).
  if [ -f "${HAX_DEV_PATH}/dist/create.js" ]; then
    echo "HAX CLI available via local development copy at ${HAX_DEV_PATH} — skipping global install."
    exit 0
  fi

  ver="$(hax --version 2>/dev/null | head -n1 | tr -d '\r')"
  echo "HAX CLI is available (hax ${ver:-installed}). Use \`hax help\` or the /hax-onboarding:* slash commands."
  exit 0
fi

# --- Local dev dist exists but hax not on PATH? Report so the user can fix. --
if [ -f "${HAX_DEV_PATH}/dist/create.js" ]; then
  echo "HAX CLI local development copy detected at ${HAX_DEV_PATH}/dist/create.js but \`hax\` is not on PATH. Add it to PATH or run \`npm link\` inside ${HAX_DEV_PATH} to use it. Skipping global install."
  exit 0
fi

# --- Respect opt-out. -------------------------------------------------------
if [ "${HAX_PLUGIN_NO_AUTOINSTALL:-0}" = "1" ]; then
  echo "HAX CLI not found; auto-install disabled (HAX_PLUGIN_NO_AUTOINSTALL=1). Install with: ${MANUAL_INSTALL}"
  exit 0
fi

# --- Need npm to install. ---------------------------------------------------
if ! command -v npm >/dev/null 2>&1; then
  echo "HAX CLI not found and npm is unavailable. Install Node.js (>=18.20.3), then run: ${MANUAL_INSTALL}"
  exit 0
fi

# --- Install globally (one-time). -------------------------------------------
# Human-facing progress goes to stderr; the result line goes to stdout/context.
echo "HAX CLI not found — installing @haxtheweb/create globally (one-time setup)…" 1>&2
if npm install --global @haxtheweb/create >/dev/null 2>&1; then
  ver="$(hax --version 2>/dev/null | head -n1 | tr -d '\r')"
  echo "Installed HAX CLI (hax ${ver:-latest}). Use \`hax help\` or the /hax-onboarding:* slash commands."
else
  echo "Could not auto-install the HAX CLI (global npm install failed — it may need elevated permissions). Install manually: ${MANUAL_INSTALL}"
fi

exit 0
