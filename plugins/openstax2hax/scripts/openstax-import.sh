#!/usr/bin/env bash
#
# openstax-import.sh
#
# Download/mirror an OpenStax book into ./source and scaffold the project so the
# openstax2hax plugin can prepare conversion files. This script ONLY downloads
# and reports; it does not build a HAX site.
#
# Usage:
#   bash scripts/openstax-import.sh <openstax-url>
#
set -euo pipefail

# ---------------------------------------------------------------------------
# 1. Arguments
# ---------------------------------------------------------------------------
if [ "$#" -ne 1 ] || [ -z "${1:-}" ]; then
  echo "Usage: bash scripts/openstax-import.sh <openstax-url>" >&2
  echo "Example: bash scripts/openstax-import.sh https://openstax.org/details/books/principles-finance" >&2
  exit 1
fi

ORIGINAL_URL="$1"

# ---------------------------------------------------------------------------
# 2. Validate the URL is from openstax.org
# ---------------------------------------------------------------------------
# Accept https://openstax.org/... or https://www.openstax.org/... only.
if ! printf '%s' "$ORIGINAL_URL" | grep -Eq '^https?://(www\.)?openstax\.org(/|$)'; then
  echo "Refusing URL: \"$ORIGINAL_URL\"" >&2
  echo "This command only accepts OpenStax URLs from the openstax.org domain," >&2
  echo "for example: https://openstax.org/details/books/principles-finance" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# 3. Create project folders
# ---------------------------------------------------------------------------
mkdir -p source conversion hax-site

# Save the original URL for later reference.
printf '%s\n' "$ORIGINAL_URL" > conversion/source-url.txt

# ---------------------------------------------------------------------------
# 4. Resolve OpenStax "details" URLs to a readable starting page
# ---------------------------------------------------------------------------
# https://openstax.org/details/books/<slug>
#   -> https://openstax.org/books/<slug>/pages/preface
# URLs that already point at /books/<slug>/pages/... are left unchanged.
RESOLVED_URL="$ORIGINAL_URL"
if printf '%s' "$ORIGINAL_URL" | grep -Eq '/details/books/[^/]+/?$'; then
  SLUG="$(printf '%s' "$ORIGINAL_URL" | sed -E 's#.*/details/books/([^/]+)/?$#\1#')"
  RESOLVED_URL="https://openstax.org/books/${SLUG}/pages/preface"
fi

echo "Original URL : $ORIGINAL_URL"
echo "Resolved URL : $RESOLVED_URL"
echo "Source dir   : source"

# ---------------------------------------------------------------------------
# 5. Ensure wget is available
# ---------------------------------------------------------------------------
if ! command -v wget >/dev/null 2>&1; then
  echo "" >&2
  echo "Error: 'wget' is required but was not found." >&2
  echo "" >&2
  echo "Install it and try again:" >&2
  echo "  macOS:          brew install wget" >&2
  echo "  Ubuntu/Debian:  sudo apt-get install wget" >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# 6. Mirror the book with wget, logging output
# ---------------------------------------------------------------------------
DOWNLOAD_LOG="conversion/download.log"
echo "Downloading the book with wget (this can take a while)..."
echo "Log: $DOWNLOAD_LOG"

# Do not let a non-zero wget exit code abort the script; some page-requisite
# fetches may fail while the core mirror still succeeds. Capture the status.
set +e
wget \
  --mirror \
  --convert-links \
  --adjust-extension \
  --page-requisites \
  --no-parent \
  --domains openstax.org \
  --directory-prefix source \
  "$RESOLVED_URL" 2>&1 | tee "$DOWNLOAD_LOG"
WGET_STATUS="${PIPESTATUS[0]}"
set -e

if [ "$WGET_STATUS" -ne 0 ]; then
  echo "Note: wget exited with status $WGET_STATUS. Some page requisites may have"
  echo "failed; check $DOWNLOAD_LOG. Continuing if source files were downloaded."
fi

# ---------------------------------------------------------------------------
# 7. Write the import report
# ---------------------------------------------------------------------------
REPORT="conversion/import-report.md"
cat > "$REPORT" <<EOF
# OpenStax Import Report

- Original URL: $ORIGINAL_URL
- Resolved URL: $RESOLVED_URL
- Source directory: source/openstax.org
- Download log: $DOWNLOAD_LOG
- wget exit status: $WGET_STATUS

## Next command

Run the prepare command to build the conversion files:

\`\`\`text
/openstax2hax:prepare ./source/openstax.org
\`\`\`

This import step only downloaded the book. It did NOT build a HAX site. The HAX
site is built later by the claudehax plugin using
\`conversion/hax-handoff-prompt.md\`.
EOF

echo ""
echo "Import complete."
echo "  Source:        source/openstax.org"
echo "  Download log:  $DOWNLOAD_LOG"
echo "  Import report: $REPORT"
echo ""
echo "Next: /openstax2hax:prepare ./source/openstax.org"
