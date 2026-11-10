# Classifying divergences and writing up the agent leg

## Classify each op that adds a new pattern

Compare each op's `verify.jsonl` entry with the previous op's. Patterns already present at op N-1 are
carried forward and belong to the op that introduced them. For every op with a **new** pattern vs the
scripted CLI (or a warning such as "addPage expected 1 new page"), pick one class:

| Class | Meaning | What to write down |
| --- | --- | --- |
| `skill-missing` | No skill said how to do this op, so you guessed. | The op type, what you looked for, where you looked. |
| `skill-wrong` | A skill said to do it a way that gives a different result (wrong flag, wrong command, outdated option, wrong value format). | The skill, the section, the text, and what is actually needed. |
| `skill-ambiguous` | The skill allowed more than one reading and you picked one that differs. | Both readings and which one the CLI matches. |
| `cli-behavior` | You did what the skill said and the CLI itself did something unexpected (error, warning, extra page). | The command, its output, the exit code. |
| `agent-error` | The skills were right and you made a mistake (quoting, wrong id, skipped a field). | What went wrong. Not a skill finding. |
| `blocked` | An earlier divergence made this op impossible to replay (unbound key). | The earlier op number. |

Differences that are also in the nightly summary for the scripted CLI vs nodejs (`summary.md`) are
CLI-vs-backend findings. Mention them once, not per op.

## Write-up for the user

Give the user this, in markdown, in your reply. Keep it factual and short; name op numbers so they
can be replayed.

```markdown
## Agent leg: <site name>, ops 0-<N>

Run: <nightly run URL or "local">, haxcms-nodejs <ref>, haxcms-php <ref>, CLI <ref or "npm vX.Y.Z">.
Skills used: hax-site-building <version>, hax-site-structure <version>, ...

**<K> of <N> ops matched the scripted CLI.** <M> ops added new divergence patterns.

| Op | Type | What I ran | Skill / section | vs CLI | vs nodejs | Class |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 5 | editSlug | `hax site node:edit --item-id ... --slug ...` | hax-site-building, "Edit a page" | +1 `site.json.items.<item>.slug` | ... | skill-wrong |

### Skill docs to fix

One entry per skill and section, with every op type it affected:

- **<skill> / <section>**: <missing | wrong | ambiguous>. Ops <list>. Needed: <the instruction that
  would have produced the CLI's result>. Suggested text: "<...>".

### CLI behavior

- <command>: <what happened>, ops <list>.

### Agent errors

- <op>: <what went wrong> (not a skill gap).
```

Do not file issues or open PRs from this write-up unless the user asks. If they ask, file in the
unified queue (https://github.com/haxtheweb/issues) and link
[haxtheweb/issues#3292](https://github.com/haxtheweb/issues/issues/3292). Skill text fixes go to
[haxtheweb/praw](https://github.com/haxtheweb/praw) for PRAW skills, and to
[haxtheweb/create `src/skills`](https://github.com/haxtheweb/create/tree/main/src/skills) for the
interface skills such as `hax-site-building`.
