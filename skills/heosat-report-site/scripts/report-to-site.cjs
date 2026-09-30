#!/usr/bin/env node
/**
 * report-to-site.cjs
 *
 * Convert a HEOSAT assessment (scores.json produced by the `heosat` skill's
 * aggregate step) into a single-page HAXcms report site page, and finalize the
 * site metadata — in one pass:
 *
 *  - reads <scores-dir>/scores.json (all 45 scores, evidence, notes,
 *    strengths, recommendations, project context)
 *  - reads the bundled HEOSAT rubric (default: ../heosat/references/rubric.json
 *    next to this skill) for section titles, question texts, scale names,
 *    and the rubric version
 *  - computes section averages + the overall score (same math as the heosat
 *    skill's aggregate.py)
 *  - builds the page: H1, context + overall stop-note, editable-table
 *    scorecard, a11y-collapse-group with one a11y-collapse per section
 *    (heading-button so the whole heading is clickable), per-question
 *    evidence detail, strengths, recommendations as collapses, and an
 *    About/provenance block
 *  - copies report.md (if present) and scores.json into <site-dir>/files/ as
 *    heosat-report.md and heosat-scores.json and links them from the About
 *    block
 *  - writes the combined HTML to the skeleton's root page (location resolved
 *    from site.json's first root item — the placeholder folder is UUID-based)
 *  - finalizes site.json: title, description, metadata.site.description
 *    (the resume-theme sidebar subtitle), the ROOT PAGE ITEM TITLE, and
 *    metadata.author — which is the ASSESSED PROJECT's profile (never the
 *    publishing person's): resume-theme reads name, image, email, phone,
 *    location, website, website2, socialLink, socialLink2 from
 *    metadata.author, so the project profile maps project details into
 *    those slots.
 *
 * Usage:
 *   node report-to-site.cjs <scores-dir> <site-dir> \
 *     [--project-profile <path>] [--rubric <path>] [--description "<text>"]
 *
 * --project-profile defaults to <scores-dir>/project-profile.json, which the
 * calling agent writes from `gh` metadata before running this script:
 *   {
 *     "name": "BookLooky Official LRS Rater",
 *     "image": "https://avatars.githubusercontent.com/u/...",
 *     "location": "MIT License · TypeScript · Node 18+",
 *     "website": "https://github.com/TheWootini/booklooky-official-lrs-rater",
 *     "website2": "https://booklooky.com"
 *   }
 * No email/phone/socialLink fields — this is the project, not a person.
 * If no profile file exists, a minimal one is derived from scores.json
 * (name from the repo slug, website from repoUrl).
 *
 * --rubric defaults to ../heosat/references/rubric.json (the sibling `heosat`
 * skill bundled on this machine).
 *
 * NEVER touches metadata.site.name (must equal the site folder name).
 */
const fs = require("fs");
const path = require("path");
const os = require("os");

// --- escaping ---------------------------------------------------------------

function escAttr(s) {
  return String(s).replace(/"/g, "&quot;");
}

function escText(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// --- scoring math (mirrors the heosat skill's aggregate.py) -----------------

function bandLabel(scale, value) {
  const nearest = Math.max(0, Math.min(scale.length - 1, Math.round(value)));
  return scale[nearest];
}

function fmtAvg(value) {
  return (Math.round(value * 10) / 10).toFixed(1);
}

// --- CLI flags ---------------------------------------------------------------

function parseFlags(argv) {
  const keys = {
    "--project-profile": "projectProfile",
    "--rubric": "rubric",
    "--description": "description",
  };
  const flags = { projectProfile: null, rubric: null, description: null };
  const skipNext = new Set();
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (Object.prototype.hasOwnProperty.call(keys, a)) {
      flags[keys[a]] = argv[i + 1];
      skipNext.add(i);
      skipNext.add(i + 1);
      i++;
    }
  }
  return { flags, positional: argv.filter((_, i) => !skipNext.has(i)) };
}

// --- HAXcms version (mirrors the hax-tutorial-site skill) -------------------

function resolveHaxcmsVersion(siteDir) {
  const candidates = [
    path.join(siteDir, "package.json"),
    path.join(os.homedir(), "Documents/git/haxtheweb/create/package.json"),
  ];
  for (const p of candidates) {
    try {
      if (fs.existsSync(p)) {
        const pkg = JSON.parse(fs.readFileSync(p, "utf8"));
        if (pkg && typeof pkg.version === "string" && pkg.version !== "") {
          return pkg.version;
        }
      }
    } catch (e) {
      // try next candidate
    }
  }
  return "unknown";
}

function formatLastUpdated() {
  return new Date().toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

// --- page building ------------------------------------------------------------

function slugToDisplayName(slug) {
  return String(slug)
    .split(/[-_]/)
    .filter(Boolean)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

function buildScorecardTable(rubric, sectionStats, overall) {
  const scale = rubric.scale;
  const rows = sectionStats
    .map(
      (st, i) =>
        `        <tr>
          <td>${i + 1}</td>
          <td>${escText(st.title)}</td>
          <td>${fmtAvg(st.avg)}</td>
          <td>${escText(bandLabel(scale, st.avg))}</td>
        </tr>`,
    )
    .join("\n");
  return `<editable-table bordered condensed responsive striped>
  <table>
    <caption>HEOSAT ${escText(rubric.version)} — section scorecard (0 Not present – 5 Leading / exemplary)</caption>
    <thead>
      <tr>
        <th scope="col">#</th>
        <th scope="col">Section</th>
        <th scope="col">Avg (0-5)</th>
        <th scope="col">Nearest band</th>
      </tr>
    </thead>
    <tbody>
${rows}
        <tr>
          <td>—</td>
          <td><strong>Overall (${sectionStats.reduce((a, s) => a + s.scores.length, 0)} questions)</strong></td>
          <td><strong>${fmtAvg(overall.avg)}</strong></td>
          <td><strong>${escText(bandLabel(scale, overall.avg))}</strong></td>
        </tr>
    </tbody>
  </table>
</editable-table>`;
}

function buildQuestionBlock(question, scale) {
  const entry = question.entry;
  const lines = [];
  lines.push(`      <h3>${escText(question.id)} — ${entry.score} / 5 (${escText(scale[entry.score])})</h3>`);
  lines.push(`      <p><em>${escText(question.text)}</em></p>`);
  if (entry.evidence && entry.evidence.length > 0) {
    lines.push("      <ul>");
    for (const ev of entry.evidence) {
      lines.push(`        <li>Evidence: ${escText(ev)}</li>`);
    }
    lines.push("      </ul>");
  }
  if (entry.notes && entry.notes.trim() !== "") {
    lines.push(`      <p><strong>Notes:</strong> ${escText(entry.notes)}</p>`);
  }
  return lines.join("\n");
}

function buildSectionCollapses(rubric, sections, scores) {
  const scale = rubric.scale;
  return sections
    .map((s, i) => {
      const vals = s.questions.map((q) => scores[q.id].score);
      const avg = vals.reduce((a, b) => a + b, 0) / vals.length;
      const heading = `${i + 1}. ${s.title} — ${fmtAvg(avg)} / 5 (${bandLabel(scale, avg)})`;
      const questionBlocks = s.questions
        .map((q) => buildQuestionBlock({ id: q.id, text: q.text, entry: scores[q.id] }, scale))
        .join("\n");
      return `    <a11y-collapse heading="${escAttr(heading)}" heading-button icon="arrow-drop-down" label="toggle ${escAttr(s.title)} section" tooltip="toggle section detail">
      <div slot="content">
${questionBlocks}
      </div>
    </a11y-collapse>`;
    })
    .join("\n");
}

function buildRecommendationCollapses(recommendations) {
  return recommendations
    .map((rec, i) => {
      const priority = String(rec.priority || "medium").toUpperCase();
      const heading = `${i + 1}. ${priority} — ${rec.title || ""}`;
      const content = [];
      if (rec.detail) {
        content.push(`        <p>${escText(rec.detail)}</p>`);
      }
      if (rec.learn) {
        content.push(
          `        <p>Learn more: <a href="${escAttr(rec.learn)}" target="_blank">${escText(rec.learn)}</a></p>`,
        );
      }
      return `    <a11y-collapse heading="${escAttr(heading)}" heading-button icon="arrow-drop-down" label="toggle recommendation ${i + 1}" tooltip="toggle recommendation detail">
      <div slot="content">
${content.join("\n")}
      </div>
    </a11y-collapse>`;
    })
    .join("\n");
}

function buildAboutSection(rubric, doc, reportCopied, scoresCopied, lastUpdated, haxVersion) {
  const items = [];
  items.push(
    `    <li>Rubric: HEOSAT ${escText(rubric.version)} — <a href="https://locusplex.us/HEOSAT/" target="_blank">locusplex.us/HEOSAT</a> (${rubric.sections.reduce((a, s) => a + s.questions.length, 0)} questions in ${rubric.sections.length} sections, scored 0–5)</li>`,
  );
  items.push(`    <li>Assessed: ${escText(doc.assessedAt || "n/a")}</li>`);
  if (reportCopied) {
    items.push(
      `    <li><a href="files/heosat-report.md" target="_blank">Full report (Markdown)</a></li>`,
    );
  }
  if (scoresCopied) {
    items.push(
      `    <li><a href="files/heosat-scores.json" target="_blank">Machine-readable scores (JSON)</a></li>`,
    );
  }
  items.push(`    <li>Last updated: ${escText(lastUpdated)}</li>`);
  items.push(`    <li>HAXcms version: ${escText(haxVersion)}</li>`);
  items.push(
    `    <li>HEOSAT is adapted from the OSS Watch Open Source Openness Rating; guidance content CC BY-SA 4.0. This is a locally generated assessment against the published rubric — not an official certification of any kind.</li>`,
  );
  return `<h2 data-margin="s">About this assessment</h2>
<ul>
${items.join("\n")}
</ul>`;
}

// --- main ----------------------------------------------------------------------

function main() {
  const { flags, positional } = parseFlags(process.argv.slice(2));
  const [scoresDir, siteDir] = positional;

  if (!scoresDir || !siteDir) {
    console.error(
      'Usage: node report-to-site.cjs <scores-dir> <site-dir> [--project-profile <path>] [--rubric <path>] [--description "<text>"]',
    );
    process.exit(1);
  }
  if (!fs.existsSync(siteDir)) {
    console.error(`Site dir not found: ${siteDir}`);
    process.exit(1);
  }

  const scoresPath = path.join(scoresDir, "scores.json");
  if (!fs.existsSync(scoresPath)) {
    console.error(`scores.json not found in: ${scoresDir}`);
    process.exit(1);
  }
  const doc = JSON.parse(fs.readFileSync(scoresPath, "utf8"));

  // rubric: sibling heosat skill by default
  const rubricPath =
    flags.rubric ||
    path.join(__dirname, "..", "..", "heosat", "references", "rubric.json");
  if (!fs.existsSync(rubricPath)) {
    console.error(`HEOSAT rubric not found: ${rubricPath}`);
    process.exit(1);
  }
  const rubric = JSON.parse(fs.readFileSync(rubricPath, "utf8")).data;

  // project profile (the assessed project — never the publishing person)
  const projectProfilePath =
    flags.projectProfile || path.join(scoresDir, "project-profile.json");
  let profile = null;
  if (fs.existsSync(projectProfilePath)) {
    const p = JSON.parse(fs.readFileSync(projectProfilePath, "utf8"));
    profile = p.project || p.author || p;
  } else {
    profile = {
      name: slugToDisplayName(String(doc.repo || "project").split("/").pop()),
      website: doc.repoUrl || "",
    };
  }

  // --- compute ----------------------------------------------------------------
  const scale = rubric.scale;
  const scores = doc.scores || {};
  const expectedIds = rubric.sections.flatMap((s) => s.questions.map((q) => q.id));
  const missingIds = expectedIds.filter((id) => !scores[id]);
  if (missingIds.length > 0) {
    console.error(
      `scores.json is missing ${missingIds.length} rubric question(s): ${missingIds.join(", ")}` +
        " — re-run the heosat skill's aggregate.py to produce a complete scores.json",
    );
    process.exit(1);
  }
  const sectionStats = rubric.sections.map((s) => {
    const vals = s.questions.map((q) => scores[q.id].score);
    return { title: s.title, scores: vals, avg: vals.reduce((a, b) => a + b, 0) / vals.length };
  });
  const allVals = rubric.sections.flatMap((s) => s.questions.map((q) => scores[q.id].score));
  const overallAvg = allVals.reduce((a, b) => a + b, 0) / allVals.length;
  const dist = {};
  for (let i = 0; i < scale.length; i++) {
    dist[i] = allVals.filter((v) => v === i).length;
  }
  const levelDist = scale.map((name, i) => `${name}: ${dist[i]}`).join(", ");

  // --- artifacts into files/ ----------------------------------------------------
  const filesDir = path.join(siteDir, "files");
  fs.mkdirSync(filesDir, { recursive: true });
  let reportCopied = false;
  const reportSrc = path.join(scoresDir, "report.md");
  if (fs.existsSync(reportSrc)) {
    fs.copyFileSync(reportSrc, path.join(filesDir, "heosat-report.md"));
    reportCopied = true;
  }
  fs.copyFileSync(scoresPath, path.join(filesDir, "heosat-scores.json"));

  // --- page ------------------------------------------------------------------
  const haxVersion = resolveHaxcmsVersion(siteDir);
  const lastUpdated = formatLastUpdated();
  const overallBand = bandLabel(scale, overallAvg);
  const siteTitle = `HEOSAT Assessment: ${profile.name || doc.repo}`;

  const pageParts = [];
  pageParts.push(`<h1>${escText(siteTitle)}</h1>`);
  pageParts.push(
    `<stop-note title="Overall: ${escAttr(fmtAvg(overallAvg))} / 5 (${escAttr(overallBand)})"><span slot="message">45-question maturity assessment against HEOSAT ${escText(rubric.version)} · assessed ${escText(doc.assessedAt || "n/a")} · every score backed by cited evidence or an explicit "checked, not found" note.</span></stop-note>`,
  );
  if (doc.context) {
    pageParts.push(`<p data-margin="xs">${escText(doc.context)}</p>`);
  }
  pageParts.push(`<h2 data-margin="s">Scorecard</h2>`);
  pageParts.push(buildScorecardTable(rubric, sectionStats, { avg: overallAvg }));
  pageParts.push(`<p data-margin="xs">Level distribution — ${escText(levelDist)}</p>`);
  pageParts.push(`<h2 data-margin="s">Section detail</h2>`);
  pageParts.push(
    `<p data-margin="xs">Expand a section to see all 45 scored questions with the evidence behind every score.</p>`,
  );
  pageParts.push(`<a11y-collapse-group>
${buildSectionCollapses(rubric, rubric.sections, scores)}
</a11y-collapse-group>`);
  if (doc.strengths && doc.strengths.length > 0) {
    pageParts.push(`<h2 data-margin="s">Strengths</h2>`);
    pageParts.push(
      `<ul>\n${doc.strengths.map((s) => `  <li>${escText(s)}</li>`).join("\n")}\n</ul>`,
    );
  }
  if (doc.recommendations && doc.recommendations.length > 0) {
    pageParts.push(`<h2 data-margin="s">Prioritized recommendations</h2>`);
    pageParts.push(`<a11y-collapse-group>
${buildRecommendationCollapses(doc.recommendations)}
</a11y-collapse-group>`);
  }
  pageParts.push(
    buildAboutSection(rubric, doc, reportCopied, true, lastUpdated, haxVersion),
  );
  const pageHtml = pageParts.join("\n");

  // --- write the page (resolve root page location from site.json) ---------------
  let pageFile = path.join(siteDir, "pages", "report", "index.html");
  try {
    const manifest = JSON.parse(
      fs.readFileSync(path.join(siteDir, "site.json"), "utf8"),
    );
    const root =
      Array.isArray(manifest.items) &&
      manifest.items.find(
        (it) => it && it.parent === null && parseInt(it.indent, 10) === 0,
      );
    if (root && typeof root.location === "string" && root.location !== "") {
      pageFile = path.join(siteDir, root.location);
    }
  } catch (e) {
    // fall back to pages/report/index.html
  }
  fs.mkdirSync(path.dirname(pageFile), { recursive: true });
  fs.writeFileSync(pageFile, pageHtml);

  // --- finalize site.json --------------------------------------------------------
  const siteJsonPath = path.join(siteDir, "site.json");
  const manifest = JSON.parse(fs.readFileSync(siteJsonPath, "utf8"));
  const description =
    flags.description ||
    `${profile.name || doc.repo} — HEOSAT maturity assessment: ${fmtAvg(overallAvg)}/5 (${overallBand}), scored against HEOSAT ${rubric.version} on ${doc.assessedAt || "n/a"}.`;

  manifest.title = siteTitle;
  manifest.description = description;
  manifest.metadata = manifest.metadata || {};
  // resume-theme sidebar subtitle (metadata.site.description — NOT site.name,
  // which must always equal the site folder name and is never touched here)
  manifest.metadata.site = manifest.metadata.site || {};
  manifest.metadata.site.description = `HEOSAT maturity assessment — ${fmtAvg(overallAvg)}/5 (${overallBand}) · assessed ${doc.assessedAt || "n/a"}`;
  // the assessed PROJECT's profile in the resume-theme author slot
  manifest.metadata.author = profile;
  manifest.author = profile.name || "";
  // root page menu label
  if (Array.isArray(manifest.items)) {
    const root = manifest.items.find(
      (it) => it && it.parent === null && parseInt(it.indent, 10) === 0,
    );
    if (root) {
      root.title = "HEOSAT Assessment";
    }
  }
  fs.writeFileSync(siteJsonPath, JSON.stringify(manifest, null, 2) + "\n");

  console.log(
    JSON.stringify(
      {
        pageFile,
        contentLength: pageHtml.length,
        siteJson: siteJsonPath,
        siteTitle,
        description,
        authorInjected: !!(manifest.metadata.author && manifest.metadata.author.name),
        projectProfileUsed: fs.existsSync(projectProfilePath)
          ? projectProfilePath
          : "derived-from-scores.json",
        reportCopied: reportCopied ? "files/heosat-report.md" : null,
        scoresCopied: "files/heosat-scores.json",
        overall: { avg: fmtAvg(overallAvg), band: overallBand },
        sectionAverages: sectionStats.map((s) => ({
          title: s.title,
          avg: fmtAvg(s.avg),
        })),
        haxVersion,
        lastUpdated,
      },
      null,
      2,
    ),
  );
}

main();
