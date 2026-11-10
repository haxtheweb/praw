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

Read `hax-site-building`, and from [PRAW](https://github.com/haxtheweb/praw/tree/main/skills)
`hax-site-structure`, `hax-managed-files` and `hax-content-authoring`. `hax list --format json` and
`hax site --help` describe every action and option.

## Create the site and initialize verify

```bash
meta=parity-results/A/meta.json
site_name="$(node -p "require('./$meta').siteName")"
site_description="$(node -p "require('./$meta').siteDescription")"
state_dir=parity-agent-state      # outside parity-results/
mkdir -p agent-sites && cd agent-sites
hax site "$site_name" --description="$site_description" --y --no-i --agent
cd ..
node create/test/parity/verify.cjs --results parity-results/A \
  --site "agent-sites/$site_name" --state "$state_dir" --op 0
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

## Reading one op safely

```bash
n=7
node -e '
  const fs = require("fs");
  const op = fs.readFileSync(process.argv[1], "utf8").split("\n").filter(Boolean)
    .map((l) => JSON.parse(l)).find((o) => o.i === Number(process.argv[2]));
  fs.writeFileSync("op.json", JSON.stringify(op, null, 2));
' parity-results/A/ops.jsonl "$n"
title="$(node -p "require('./op.json').title")"
```

Read each field into a shell variable like this and pass `"$title"` quoted, so quotes, `&`, `<b>` and
leading spaces reach the CLI unchanged. Look page ids up the same way from `$state_dir/state.json`.
