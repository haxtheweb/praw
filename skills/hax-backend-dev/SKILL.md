---
name: hax-backend-dev
description: "Change the HAXcms backends in step: implement in haxcms-nodejs and haxcms-php, mirror site-spec and system-spec edits, use @site/ or @system/ MFR namespaces. Use for any API, route, operation, audit or security fix touching either backend."
version: 1.0.0
license: Apache-2.0
metadata:
  author: haxtheweb
  depends_on: [hax-managed-files, hax-testing]
  tags: [hax, haxcms, backend, nodejs, php, parity, openapi, mfr]
---

# HAX backend development (PHP / Node parity)

HAXcms ships two backends that expose the same v1 API: `haxcms-nodejs` and `haxcms-php`. A change
that lands in only one of them is a bug in the other. This skill is the workflow for keeping them in
step. It works the same from a local clone or a cloud agent: everything below resolves through the
public repositories.

- Node backend: https://github.com/haxtheweb/haxcms-nodejs
- PHP backend: https://github.com/haxtheweb/haxcms-php
- Rules (authoritative, by Rule ID): https://github.com/haxtheweb/praw/blob/main/RULES.md
- Scoped haxcms rules: https://github.com/haxtheweb/praw/blob/main/haxcms/WARP.md
- Work queue: https://github.com/haxtheweb/issues

## When to use

- Adding or changing an API route, operation, or response shape.
- Fixing an audit or security finding in either backend (rule `a8bf4a47`: resolve it in BOTH).
- Editing `site-spec.yaml` or `system-spec.yaml`.
- Adding or renaming a Microfrontend Registry (MFR) call.

## Where things live

| Concern | haxcms-nodejs | haxcms-php |
|---|---|---|
| Site-scoped routes | `src/siteRoutes/v1/` | `system/backend/php/lib/siteRoutes/` |
| System-scoped routes | `src/systemRoutes/v1/` | `system/backend/php/lib/systemRoutes/` |
| OpenAPI specs | `src/openapi/site-spec.yaml`, `src/openapi/system-spec.yaml` | `openapi/` folders under the two `lib/*Routes` dirs |
| Core operations | `src/lib/` | `system/backend/php/lib/Operations.php` and `lib/operations/` |
| Unit tests | `test/unit/`, `test/api-conformance/` | `system/backend/php/tests/` |

Check the tree before editing: layouts move, and the repos are the source of truth.

## Workflow

1. **Read the issue** in https://github.com/haxtheweb/issues and any linked plan comment. Note which
   backend the issue names; parity still applies to the other.
2. **Pick the scope.** Actions on one site use the `@site/` MFR namespace and `siteRoutes/v1`.
   Everything else (imports, conversions, session, settings) uses `@system/` and `systemRoutes/v1`.
   Do not add `@haxcms/` registrations; that namespace pointed at external endpoints that were phased
   out in favor of on-premises calls (rule `82dc87fd`).
3. **Implement in one backend first.** Reuse the existing data-model loading and file-path helpers
   instead of adding abstractions. Keep the diff surgical.
4. **Mirror it in the other backend.** Same route, same request and response shape, same error codes,
   same validation and security checks. If a behavior cannot be matched, say so in both PRs.
5. **Mirror spec edits.** Any change to `site-spec` or `system-spec` in one system is made in both.
   The spec is the contract; handler code follows it.
6. **Add tests in both** (see the `hax-testing` skill), then run each repo's pre-submission check.
7. **Open one PR per repo.** Link the PRs to each other and to the issue so a reviewer sees the pair.
   Do not merge; maintainers review and merge.

## Guardrails

- Never edit generated files, `build/`, or `node_modules/`. Load `hax-managed-files` first. If minified
  assets in a backend are wrong, fix the source in the `webcomponents` repo and hand off.
- Never run the ubiquity script or a top-level `webcomponents` build.
- Use the local `hax` CLI, never `npx`. Pass `--y --no-i` so nothing prompts.
- Link between repos by public URL, never by a local filesystem path.

## Checklist before opening the PRs

- [ ] Route exists in both backends under the right scope (`@site/` or `@system/`).
- [ ] Spec change made in both specs, if any.
- [ ] Tests added or updated in both repos and passing.
- [ ] Pre-submission checks pass in each repo.
- [ ] PRs cross-link and reference the issue.
