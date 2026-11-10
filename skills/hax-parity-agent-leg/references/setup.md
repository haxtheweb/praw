# Getting a parity run and setting up the agent leg

Everything below uses paths relative to a working directory you choose. Nothing depends on a
particular machine layout.

## Option A: the nightly artifact

The [create `parity-nightly` workflow](https://github.com/haxtheweb/create/actions/workflows/parity-nightly.yml)
uploads a `parity-results` artifact (30-day retention) for every run.

```bash
run_id="$(gh run list --repo haxtheweb/create --workflow parity-nightly.yml \
  --status success --limit 1 --json databaseId --jq '.[0].databaseId')"
gh run download "$run_id" --repo haxtheweb/create --name parity-results --dir parity-results
git clone https://github.com/haxtheweb/create.git   # for test/parity/verify.cjs
```

`parity-results/env.json` names the haxcms-nodejs, haxcms-php and CLI refs the run used.
`parity-results/summary.md` is the nightly report; read it first so you know which differences the
scripted CLI already has.

## Option B: run the harness yourself

Follow the setup in
[create `test/parity/README.md`](https://github.com/haxtheweb/create/blob/main/test/parity/README.md)
(three sibling checkouts, haxcms-nodejs built and linked into the CLI, haxcms-php installed), then run
sequence A only. The agent leg uses sequence A because those are the ops the CLI can express.

```bash
node create/test/parity/parity.cjs --nodejs haxcms-nodejs --php haxcms-php \
  --seq A --ops 50 --out parity-results
```

Snapshots are kept for ops 0..`--snapshots` (default 100), so that is how far you can replay.

## The CLI and skills

Use the same CLI as the run, so differences are yours and not version drift:

- Nightly artifact: the CLI ref in `env.json` is the create default branch at that time. Build it from
  your create checkout (`npm ci && npm run build`, then run it as `node <create>/dist/create.js`, or
  `npm link` it so `hax` is that build). The released `npm install --global @haxtheweb/create` is fine
  for a quick pass, but say so in the report.
- Local run: use the CLI you ran the harness with.

Then install the interface skills that ship with the CLI and load the site skills:

```bash
hax skills install --all     # hax-site-building and the other interface skills
```

`hax skills install --all` installs the **released** skills. When you are testing a create branch (a
pull request, or a nightly built from the default branch), read `src/skills/*` from that create
checkout instead (for example `src/skills/hax-site-building/SKILL.md`), since those are the docs of
the build under test; the released ones may describe older options.

Read `hax-site-building` and `hax-claudehax`, and from [PRAW](https://github.com/haxtheweb/praw/tree/main/skills)
`hax-site-structure`, `hax-managed-files` and `hax-content-authoring`. `hax list --format json` and
`hax site --help` describe every action and option.

## Create the site and initialize verify

```bash
mkdir -p agent-sites
node -e '
  const fs = require("fs");
  const { spawnSync } = require("child_process");
  const [metaPath, parent] = process.argv.slice(1);
  const meta = JSON.parse(fs.readFileSync(metaPath, "utf8"));
  // runs recorded before siteDescription was added used this description
  const description =
    meta.siteDescription !== undefined ? meta.siteDescription : "Parity test site";
  const args = ["site", meta.siteName, "--description=" + description, "--y", "--no-i", "--agent"];
  const r = spawnSync("hax", args, { cwd: parent, stdio: "inherit" });
  console.log("site directory: " + parent + "/" + meta.siteName);
  process.exit(r.status === null ? 1 : r.status);
' parity-results/A/meta.json agent-sites
```

Then, with `site_dir` set to the printed site directory (the generated name is plain ASCII, such as
`agent-sites/paritya…`) and `state_dir` set to a directory outside `parity-results/`:

```bash
node create/test/parity/verify.cjs --results parity-results/A \
  --site "$site_dir" --state "$state_dir" --op 0
```

Every leg of the run created its site with that name and description (older runs without
`siteDescription` in `meta.json` used `Parity test site`). Create the site however the skills say to
create a new site with that name and description. Op 0 should show 0 diffs vs the scripted CLI; if it
does not, the site was created differently (record it as op 0 in the write-up).

Always pass `--state <dir>` with a directory **outside** the run directory, and the same one on every
call. `verify.cjs` keeps `state.json` (logical key to page id) there and appends every result to
`verify.jsonl`; it refuses a state directory inside the run, so a downloaded run stays exactly as
recorded. Use a new state directory (and a new site) for each attempt, and `--json` for
machine-readable output.

## Passing op values safely

Op values are deliberately hostile to shells: quotes, `&`, `<b>`, leading and trailing spaces,
trailing newlines, unicode, and values that start with `-`. Two rules:

- **Never capture a value with `$(…)`.** Command substitution strips trailing newlines, and
  `node -p "…title"` prints the literal `undefined` for a field the op does not have.
- **Use only the fields the op has.** Optional fields (`parent`, `slug`, `description`, `tags` on
  `addPage`) are absent when unused; check `op.field !== undefined` before passing a flag, and never
  pass a flag for a missing field.

Pass each value as its own argv element from Node, with no shell in between. Which command and
flags an op needs comes from the skills; this only shows how to hand the values over. For example,
for an op that changes a title:

```bash
n=7
node -e '
  const fs = require("fs");
  const { spawnSync } = require("child_process");
  const [opsPath, n, statePath, siteDir] = process.argv.slice(1);
  const op = fs.readFileSync(opsPath, "utf8").split("\n").filter(Boolean)
    .map((l) => JSON.parse(l)).find((o) => o.i === Number(n));
  const ids = JSON.parse(fs.readFileSync(statePath, "utf8")).keyToId;
  const args = ["site", "node:edit", "--item-id=" + ids[op.key]];
  if (op.title !== undefined) args.push("--title=" + op.title);
  args.push("--y", "--no-i", "--agent");
  const r = spawnSync("hax", args, { cwd: siteDir, stdio: "inherit" });
  process.exit(r.status === null ? 1 : r.status);
' parity-results/A/ops.jsonl "$n" "$state_dir/state.json" "$site_dir"
```

Use the `--flag=value` form so a value that starts with `-` is not read as another flag. The
argument values `$n`, `$state_dir` and `$site_dir` are your own paths and numbers, never op values.
