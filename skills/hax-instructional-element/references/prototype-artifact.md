# Prototype artifact

Every build round of an instructional element ends with a prototype artifact: the element running in the
real HAX editor, next to a feedback panel. The panel asks the round's open design questions and has a
**Copy feedback** button that produces one block the owner pastes straight back into the next prompt.
Anyone who plays with the prototype can fill it in (the owner, a product owner, instructors, students), so
feedback from people who will never open a chat with Claude still arrives in a shape Claude can act on.

## When it is required

- After the first working render of a new element, before the PR is called ready.
- Whenever a design question is open. Ask it in the artifact; the chat reply only summarizes and points
  to the artifact. Don't ask design questions only in chat.
- After feedback changes behavior: publish the next round to the **same** artifact (same file path in the
  session, or the artifact's URL from another session) so the link people already have keeps working.

Skip it only when the change is invisible to learners and authors (tests, docs, tooling).

Publish it as an artifact when the session has an artifact tool. Otherwise the page and its bundle are
plain static files: deploy the folder to any static host and share that URL. Nothing in it depends on
the host.

## What is on the page

1. **The element running in HAX.** Build the bundle with `hax-element-demo` (esbuild of `h-a-x` plus the
   element from the working branch, runtime files copied to the same `node_modules/...` paths). Sample
   content is small, real and shows every mode the questions mention (for example one activity per unit
   or mode). Load it through `importContent`, since question elements consume their answer inputs on
   upgrade. When the element is on an unmerged branch, resolve its package (and any base class it changed,
   such as multiple-choice for `QuestionElement`) from that branch's checkout, not from `node_modules`.
2. **Try this.** Three to six concrete things to do, in order, including at least one wrong answer and
   one trip into edit mode.
3. **Questions.** Grouped, numbered, one decision each. Every question has a one-line context saying
   what the element does *today*, two or three options, a **Suggested** option when Claude has a view,
   "Something else" with a text box, and an optional note.
4. **What you noticed.** Repeating tried / happened / expected entries, for bugs and surprises.
5. **You.** Name and role, so feedback from several people can be told apart.
6. **Copy feedback.** Copies the block below. If the clipboard is refused, it reveals and selects the
   text instead. A count shows how many questions are answered.

Answers are saved as a draft in that viewer's browser only (wrapped in `try/catch`); nothing is sent
anywhere. People send the copied text to the owner however they like.

## The copied block

Plain text, one block per reviewer, with the question text inline so a fresh session understands it
without the artifact:

```text
Prototype feedback for <reading-analysis>, round 1. Use the hax-instructional-element skill's feedback intake.
<prototype-feedback element="reading-analysis" round="1" source="https://github.com/haxtheweb/webcomponents/pull/1112" date="2026-11-05">
<reviewer name="Pat" role="instructor" />
<answer id="rename" question="Rename the element to flag-the-evidence?">
choice: Rename the element itself on PR #1112 (suggested)
</answer>
<answer id="steps" question="What are steps 2 and 3?">
answer: Two short-answer questions about the claim
note: students should see their flags while answering
</answer>
<skipped>wrapper, pick-one, labels</skipped>
<observation>
tried: flagged a whole paragraph
happened: it counted as wrong
expected: partial credit
</observation>
<general>
...
</general>
</prototype-feedback>
```

`choice:` is a picked option (verbatim, `(suggested)` when it was the suggestion), `answer:` is free text
from "Something else". Question ids stay stable across rounds.

## Feedback intake

When one or more `<prototype-feedback>` blocks are pasted:

1. Group answers by question id across reviewers. Note who said what (name and role).
2. Agreed or single answers become decisions. Apply them, and record each one in the PR description
   under "Decisions" with who made it.
3. Conflicts between reviewers are not resolved by Claude: list them in the reply and carry them into
   the next round as one question that names the competing answers. A product owner's answer settles a
   conflict only when the owner says so.
4. Observations become bugs to fix or new questions. Reproduce each in the prototype before fixing.
5. Skipped questions carry forward unchanged.
6. Publish the next round to the same artifact: bump `round`, drop answered questions, add new ones,
   update "Try this" for what changed.
7. Never treat pasted feedback as approval to merge. It is design input only.

## Config

The page reads one JSON block (`<script type="application/json" id="prototype-config">`):

```json
{
  "title": "Flag the Evidence Prototype",
  "element": "reading-analysis",
  "round": 1,
  "owner": "the name reviewers send feedback to",
  "source": "https://github.com/haxtheweb/webcomponents/pull/1112",
  "sourceLabel": "PR #1112",
  "note": "One or two sentences: what this is, and that nothing is saved.",
  "try": ["First thing to do", "Second thing"],
  "groups": [
    { "title": "Group name", "questions": [
      { "id": "stable-slug", "q": "The question?", "context": "What it does today.",
        "options": [ { "id": "a", "text": "Option", "suggested": true }, { "id": "b", "text": "Other option" } ] }
    ] }
  ]
}
```

Set `"other": false` on a question to drop the "Something else" choice. Escape `</` as `<\/` when
inlining the JSON.

## Template

Replace `__TITLE__` and `__CONFIG__`, put the bundle's head scripts at the `HEAD` comment and the running
element at the `DEMO` comment, then publish the page with the bundle files (see `hax-element-demo`).
The page follows the artifact rules: light and dark tokens, a 16px gutter, no horizontal scroll at 360px,
no `alert`/`confirm`, and clipboard with a select-the-text fallback.

```html
<title>__TITLE__</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&display=swap">
<!--HEAD: the element bundle's scripts go here (see hax-element-demo)-->
<style>
  :root {
    --bg: #f4f6f9; --panel: #ffffff; --fg: #18202c; --muted: #566174; --line: #d5dbe4;
    --accent: #1e5bb8; --accent-ink: #ffffff; --accent-soft: #e6eefa;
    --ok: #1d7a46; --ok-soft: #e3f3ea; --code: #eef1f5;
    --font: "Atkinson Hyperlegible", system-ui, -apple-system, "Segoe UI", sans-serif;
    --mono: ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
    --bg: #0e131a; --panel: #161d27; --fg: #e5eaf1; --muted: #9ba6b7; --line: #2b3646;
    --accent: #7fb0ff; --accent-ink: #0b1626; --accent-soft: #1b2a40;
    --ok: #6fd39b; --ok-soft: #15301f; --code: #0f1620; color-scheme: dark; } }
  :root[data-theme="dark"] {
    --bg: #0e131a; --panel: #161d27; --fg: #e5eaf1; --muted: #9ba6b7; --line: #2b3646;
    --accent: #7fb0ff; --accent-ink: #0b1626; --accent-soft: #1b2a40;
    --ok: #6fd39b; --ok-soft: #15301f; --code: #0f1620; color-scheme: dark; }
  body { background: var(--bg); color: var(--fg); font-family: var(--font); font-size: 16px; line-height: 1.5; margin: 0; }
  .top { border-bottom: 1px solid var(--line); background: var(--panel); }
  .top-in, .grid { max-width: 1320px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
  .top-in { padding-block: 64px 16px; display: flex; flex-wrap: wrap; gap: 8px 24px; align-items: baseline; justify-content: space-between; }
  .top h1 { margin: 0; font-size: 1.35rem; text-wrap: balance; }
  .meta { display: flex; flex-wrap: wrap; gap: 6px 16px; color: var(--muted); font-size: 0.875rem; }
  .meta a { color: var(--accent); }
  .tag { font-family: var(--mono); font-size: 0.8125rem; background: var(--code); padding: 1px 6px; border-radius: 4px; }
  .grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(320px, 440px); gap: 24px; padding-block: 24px 48px; align-items: start; }
  @media (max-width: 960px) { .grid { grid-template-columns: minmax(0, 1fr); } }
  .demo { min-width: 0; }
  .demo-note { margin: 0 0 12px; color: var(--muted); font-size: 0.9375rem; max-width: 70ch; }
  .panel { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; min-width: 0; display: flex; flex-direction: column; }
  @media (min-width: 961px) { .panel { position: sticky; top: calc(env(safe-area-inset-top, 0px) + 16px); max-height: calc(100dvh - 32px); } }
  .panel-body { overflow: auto; padding: 16px 18px; display: flex; flex-direction: column; gap: 20px; }
  .panel h2 { font-size: 0.8125rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin: 0 0 8px; }
  .try { margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 4px; }
  fieldset { border: 0; margin: 0; padding: 0; min-width: 0; }
  .q { border-top: 1px solid var(--line); padding-top: 14px; display: flex; flex-direction: column; gap: 8px; }
  [hidden] { display: none !important; }
  .q legend { font-weight: 700; font-size: 1rem; line-height: 1.4; padding: 0; margin-bottom: 4px; }
  .q-num { color: var(--muted); font-weight: 400; margin-right: 4px; }
  .panel .q-ctx { margin: 0; color: var(--muted); font-size: 0.9375rem; line-height: 1.45; }
  .jump { font-size: 0.875rem; color: var(--accent); }
  @media (min-width: 961px) { .jump { display: none; } }
  .opt { display: flex; gap: 8px; align-items: flex-start; padding: 6px 8px; border-radius: 6px; cursor: pointer; }
  .opt:hover { background: var(--accent-soft); }
  .opt input { margin-top: 4px; width: 18px; height: 18px; flex: none; accent-color: var(--accent); }
  .sugg { font-size: 0.75rem; letter-spacing: 0.04em; text-transform: uppercase; color: var(--ok); background: var(--ok-soft); border-radius: 999px; padding: 1px 8px; margin-left: 6px; white-space: nowrap; }
  .q.done legend::after { content: "✓ answered"; font-weight: 400; font-size: 0.8125rem; color: var(--ok); margin-left: 8px; }
  label.field { display: flex; flex-direction: column; gap: 4px; font-size: 0.9375rem; }
  input[type="text"], textarea { font: inherit; color: var(--fg); background: var(--bg); border: 1px solid var(--line); border-radius: 6px; padding: 8px 10px; width: 100%; box-sizing: border-box; }
  textarea { min-height: 64px; resize: vertical; }
  input:focus-visible, textarea:focus-visible, button:focus-visible, .opt:focus-within { outline: 2px solid var(--accent); outline-offset: 2px; }
  .two { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  @media (max-width: 420px) { .two { grid-template-columns: 1fr; } }
  .obs { display: flex; flex-direction: column; gap: 8px; border-left: 3px solid var(--line); padding-left: 10px; }
  button { font: inherit; border-radius: 6px; border: 1px solid var(--line); background: var(--panel); color: var(--fg); padding: 8px 14px; cursor: pointer; min-height: 40px; }
  button.primary { background: var(--accent); color: var(--accent-ink); border-color: var(--accent); font-weight: 700; }
  button.link { border: 0; background: none; color: var(--accent); padding: 4px 0; min-height: 0; text-decoration: underline; }
  .send { border-top: 1px solid var(--line); padding: 12px 18px 16px; display: flex; flex-direction: column; gap: 8px; }
  .send-row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  .count { color: var(--muted); font-size: 0.875rem; margin-right: auto; }
  #status { font-size: 0.875rem; color: var(--ok); min-height: 1.3em; margin: 0; }
  #output { font-family: var(--mono); font-size: 0.75rem; background: var(--code); min-height: 160px; margin-top: 6px; }
  .sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
  .confirm { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; font-size: 0.875rem; }
</style>

<header class="top">
  <div class="top-in">
    <h1 id="p-title"></h1>
    <div class="meta" id="p-meta"></div>
    <a class="jump" href="#feedback">Jump to the feedback questions</a>
  </div>
</header>

<div class="grid">
  <section class="demo" aria-labelledby="demo-h">
    <h2 id="demo-h" class="sr-only">Prototype</h2>
    <p class="demo-note" id="p-note"></p>
    <!--DEMO: the running element goes here (for example <h-a-x> with sample content)-->
  </section>

  <aside class="panel" id="feedback" aria-labelledby="fb-h">
    <div class="panel-body">
      <div>
        <h2 id="fb-h">Feedback</h2>
        <p class="q-ctx" style="margin:0">Answer what you can, skip the rest. When you're done, copy the feedback and send it to <strong id="p-owner"></strong>.</p>
      </div>
      <div id="try-wrap">
        <h2>Try this</h2>
        <ol class="try" id="try"></ol>
      </div>
      <div id="you">
        <h2>You</h2>
        <div class="two">
          <label class="field">Name<input type="text" id="r-name" autocomplete="name"></label>
          <label class="field">Role<input type="text" id="r-role" placeholder="e.g. instructor"></label>
        </div>
      </div>
      <div id="questions"></div>
      <div>
        <h2>What you noticed</h2>
        <div id="obs-list" style="display:flex;flex-direction:column;gap:14px"></div>
        <button type="button" class="link" id="obs-add">+ Add another</button>
      </div>
      <label class="field"><span><strong>Anything else</strong></span><textarea id="general"></textarea></label>
    </div>
    <div class="send">
      <div class="send-row">
        <span class="count" id="count"></span>
        <button type="button" class="primary" id="copy">Copy feedback</button>
      </div>
      <p id="status" role="status" aria-live="polite"></p>
      <button type="button" class="link" id="show-out" aria-expanded="false" aria-controls="output">See what gets copied</button>
      <textarea id="output" readonly aria-label="Feedback to send" hidden></textarea>
      <div class="confirm" id="reset-wrap">
        <button type="button" class="link" id="reset">Clear my answers</button>
      </div>
    </div>
  </aside>
</div>

<script type="application/json" id="prototype-config">__CONFIG__</script>
<script>
(() => {
  const cfg = JSON.parse(document.getElementById("prototype-config").textContent);
  const $ = (id) => document.getElementById(id);
  const key = "proto-feedback:" + cfg.element + ":" + cfg.round;
  const load = () => { try { return JSON.parse(localStorage.getItem(key) || "{}"); } catch (e) { return {}; } };
  const saved = load();
  const persist = (s) => { try { localStorage.setItem(key, JSON.stringify(s)); } catch (e) { /* drafts are a convenience */ } };

  $("p-title").textContent = cfg.title;
  $("p-owner").textContent = cfg.owner;
  $("p-note").textContent = cfg.note || "";
  const meta = $("p-meta");
  const addMeta = (html) => { const s = document.createElement("span"); s.append(...html); meta.append(s); };
  const tag = document.createElement("span"); tag.className = "tag"; tag.textContent = "<" + cfg.element + ">";
  addMeta([tag]);
  addMeta(["Round " + cfg.round]);
  if (cfg.source) { const a = document.createElement("a"); a.href = cfg.source; a.textContent = cfg.sourceLabel || cfg.source; a.target = "_blank"; a.rel = "noopener"; addMeta([a]); }

  (cfg.try || []).forEach((t) => { const li = document.createElement("li"); li.textContent = t; $("try").append(li); });
  if (!(cfg.try || []).length) { $("try-wrap").hidden = true; }

  // questions
  const qs = [];
  let n = 0;
  (cfg.groups || []).forEach((g) => {
    const wrap = document.createElement("div");
    wrap.style.cssText = "display:flex;flex-direction:column;gap:14px";
    const h = document.createElement("h2"); h.textContent = g.title; wrap.append(h);
    g.questions.forEach((q) => {
      n += 1;
      const fs = document.createElement("fieldset"); fs.className = "q"; fs.dataset.id = q.id;
      const lg = document.createElement("legend");
      const num = document.createElement("span"); num.className = "q-num"; num.textContent = n + ".";
      lg.append(num, q.q); fs.append(lg);
      if (q.context) { const c = document.createElement("p"); c.className = "q-ctx"; c.textContent = q.context; fs.append(c); }
      const opts = (q.options || []).slice();
      if (q.other !== false) { opts.push({ id: "other", text: "Something else" }); }
      opts.forEach((o) => {
        const l = document.createElement("label"); l.className = "opt";
        const r = document.createElement("input"); r.type = "radio"; r.name = "q-" + q.id; r.value = o.id;
        const s = document.createElement("span"); s.textContent = o.text;
        if (o.suggested) { const b = document.createElement("span"); b.className = "sugg"; b.textContent = "Suggested"; s.append(b); }
        l.append(r, s); fs.append(l);
      });
      const other = document.createElement("label"); other.className = "field"; other.hidden = true;
      other.append("Your answer");
      const otherIn = document.createElement("textarea"); otherIn.dataset.role = "other"; other.append(otherIn); fs.append(other);
      const nb = document.createElement("button"); nb.type = "button"; nb.className = "link"; nb.textContent = "+ Add a note";
      const nl = document.createElement("label"); nl.className = "field"; nl.hidden = true;
      nl.append("Note");
      const note = document.createElement("textarea"); note.dataset.role = "note"; note.style.minHeight = "44px"; nl.append(note);
      nb.addEventListener("click", () => { nl.hidden = false; nb.hidden = true; note.focus(); });
      fs.append(nb, nl);
      wrap.append(fs);
      qs.push({ q, n, fs, opts, other, otherIn, note, nl, nb });
    });
    $("questions").append(wrap);
  });

  // observations
  const obs = [];
  const addObs = (v) => {
    const box = document.createElement("div"); box.className = "obs";
    const mk = (label, k, ph) => { const l = document.createElement("label"); l.className = "field"; l.append(label); const t = document.createElement("textarea"); t.dataset.k = k; t.placeholder = ph; t.style.minHeight = "44px"; t.value = (v && v[k]) || ""; l.append(t); box.append(l); return t; };
    const o = { tried: mk("What I tried", "tried", "e.g. flagged a whole paragraph"), happened: mk("What happened", "happened", ""), expected: mk("What I expected", "expected", "") };
    $("obs-list").append(box); obs.push(o);
  };
  (saved.obs && saved.obs.length ? saved.obs : [null]).forEach(addObs);
  $("obs-add").addEventListener("click", () => { addObs(null); obs[obs.length - 1].tried.focus(); });

  // restore draft
  $("r-name").value = saved.name || "";
  $("r-role").value = saved.role || "";
  $("general").value = saved.general || "";
  qs.forEach((x) => {
    const a = (saved.answers || {})[x.q.id] || {};
    if (a.choice) { const r = x.fs.querySelector('input[value="' + a.choice + '"]'); if (r) { r.checked = true; } }
    x.otherIn.value = a.other || ""; x.note.value = a.note || "";
    if (x.note.value) { x.nl.hidden = false; x.nb.hidden = true; }
  });

  const attr = (s) => String(s).replace(/"/g, "'").replace(/\s+/g, " ").trim();
  const text = (s) => String(s).trim();
  const state = () => {
    const answers = {};
    qs.forEach((x) => {
      const r = x.fs.querySelector("input[type=radio]:checked");
      answers[x.q.id] = { choice: r ? r.value : "", other: x.otherIn.value, note: x.note.value };
    });
    return { name: $("r-name").value, role: $("r-role").value, general: $("general").value, answers,
      obs: obs.map((o) => ({ tried: o.tried.value, happened: o.happened.value, expected: o.expected.value })) };
  };
  const build = (s) => {
    const L = [];
    L.push("Prototype feedback for <" + cfg.element + ">, round " + cfg.round + ". Use the hax-instructional-element skill's feedback intake.");
    L.push('<prototype-feedback element="' + attr(cfg.element) + '" round="' + cfg.round + '"' + (cfg.source ? ' source="' + attr(cfg.source) + '"' : "") + ' date="' + new Date().toISOString().slice(0, 10) + '">');
    L.push('<reviewer name="' + attr(s.name || "unnamed") + '" role="' + attr(s.role || "unknown") + '" />');
    const skipped = [];
    qs.forEach((x) => {
      const a = s.answers[x.q.id];
      const hasOther = a.choice === "other" && text(a.other);
      if (!a.choice && !text(a.note)) { skipped.push(x.q.id); return; }
      L.push('<answer id="' + x.q.id + '" question="' + attr(x.q.q) + '">');
      if (a.choice && a.choice !== "other") {
        const o = x.opts.find((p) => p.id === a.choice);
        L.push("choice: " + (o ? o.text : a.choice) + (o && o.suggested ? " (suggested)" : ""));
      } else if (hasOther) {
        L.push("answer: " + text(a.other));
      } else {
        L.push("choice: none");
      }
      if (text(a.note)) { L.push("note: " + text(a.note)); }
      L.push("</answer>");
    });
    if (skipped.length) { L.push("<skipped>" + skipped.join(", ") + "</skipped>"); }
    s.obs.filter((o) => text(o.tried) || text(o.happened) || text(o.expected)).forEach((o) => {
      L.push("<observation>");
      if (text(o.tried)) { L.push("tried: " + text(o.tried)); }
      if (text(o.happened)) { L.push("happened: " + text(o.happened)); }
      if (text(o.expected)) { L.push("expected: " + text(o.expected)); }
      L.push("</observation>");
    });
    if (text(s.general)) { L.push("<general>\n" + text(s.general) + "\n</general>"); }
    L.push("</prototype-feedback>");
    return L.join("\n");
  };
  const refresh = () => {
    const s = state();
    let done = 0;
    qs.forEach((x) => {
      const a = s.answers[x.q.id];
      x.other.hidden = a.choice !== "other";
      const ok = (a.choice && a.choice !== "other") || (a.choice === "other" && text(a.other));
      x.fs.classList.toggle("done", Boolean(ok));
      if (ok) { done += 1; }
    });
    $("count").textContent = done + " of " + qs.length + " answered";
    $("output").value = build(s);
    persist(s);
  };
  document.querySelector(".panel").addEventListener("input", refresh);
  document.querySelector(".panel").addEventListener("change", refresh);
  refresh();

  $("show-out").addEventListener("click", () => {
    const o = $("output"); o.hidden = !o.hidden;
    $("show-out").setAttribute("aria-expanded", String(!o.hidden));
    $("show-out").textContent = o.hidden ? "See what gets copied" : "Hide what gets copied";
  });
  $("copy").addEventListener("click", () => {
    refresh();
    const out = $("output");
    const fallback = () => {
      out.hidden = false; $("show-out").setAttribute("aria-expanded", "true"); out.focus(); out.select();
      $("status").textContent = "Copy is blocked here. The text is selected: press Ctrl+C (⌘C on a Mac).";
    };
    try {
      navigator.clipboard.writeText(out.value).then(() => {
        $("status").textContent = "Copied. Paste it into a message to " + cfg.owner + ".";
      }, fallback);
    } catch (e) { fallback(); }
  });
  const askReset = () => {
    const w = $("reset-wrap");
    w.textContent = "";
    w.append("Clear every answer on this page?");
    const yes = document.createElement("button"); yes.type = "button"; yes.textContent = "Clear";
    const no = document.createElement("button"); no.type = "button"; no.textContent = "Keep";
    const back = () => {
      w.textContent = "";
      const b = document.createElement("button"); b.type = "button"; b.className = "link"; b.textContent = "Clear my answers";
      b.addEventListener("click", askReset); w.append(b);
    };
    yes.addEventListener("click", () => {
      document.querySelectorAll(".panel input[type=text], .panel textarea:not([readonly])").forEach((t) => { t.value = ""; });
      document.querySelectorAll(".panel input[type=radio]").forEach((r) => { r.checked = false; });
      refresh(); back(); $("status").textContent = "Cleared.";
    });
    no.addEventListener("click", back);
    w.append(yes, no); yes.focus();
  };
  $("reset").addEventListener("click", askReset);
})();
</script>
```
