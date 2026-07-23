#!/usr/bin/env node
/**
 * docx-to-content.cjs
 *
 * Convert a local .docx transcript into a HAXcms tutorial page AND finalize the
 * site metadata in one pass:
 *  - extracts screenshots into <site-dir>/files/images/ and rewrites <img src>
 *    to site-relative files/images/<n>.<ext> (media lives with the site)
 *  - wraps timestamp tokens (e.g. 0:45, 1:30, 1:02:30) in
 *    <page-anchor target="#<uuid>" value="<seconds>"> for in-page video seeking
 *  - prepends a <video-player id="<uuid>" source="<watch-url>"> at the top
 *  - writes the combined HTML to the skeleton's root page (location resolved
 *    from site.json's first root item — the placeholder folder is UUID-based)
 *  - injects the author profile into site.json metadata.author (and sets the
 *    top-level author string to the author name for fallback compatibility)
 *  - sets site.json title (video title) and description
 *  - appends a <h2>Details</h2> provenance block: links to the YouTube video,
 *    every screenshot in the page, the source DOCX (copied into files/), a
 *    "Last updated" date, and the HAXcms version used in generation
 *  - when --puppeteer-json <path> is supplied, copies that JSON into files/
 *    and appends an "Automation recording" sub-section at the bottom of the
 *    Details block linking the copied file
 *
 * Usage:
 *   NODE_PATH=<create node_modules> node docx-to-content.cjs \
 *     <docx-path> <site-dir> <video-player-uuid> <youtube-watch-url> "<video-title>" \
 *     [--author-profile <path>] [--description "<text>"] [--puppeteer-json "<path>"]
 *
 * --author-profile defaults to ../references/author-profile.json (next to this
 * script). --description defaults to a generic SEO summary built from the title.
 * --puppeteer-json is optional; when omitted no automation sub-section is emitted.
 *
 * mammoth is resolved via require('mammoth') (honors NODE_PATH) with fallbacks
 * to the create and haxcms-nodejs node_modules, so it runs on this machine
 * even without NODE_PATH set.
 */
const fs = require("fs");
const path = require("path");
const os = require("os");

function resolveMammoth() {
  const candidates = [
    () => require("mammoth"),
    () =>
      require(
        path.join(
          os.homedir(),
          "Documents/git/haxtheweb/create/node_modules/mammoth",
        ),
      ),
    () =>
      require(
        path.join(
          os.homedir(),
          "Documents/git/haxtheweb/haxcms-nodejs/node_modules/mammoth",
        ),
      ),
  ];
  for (const load of candidates) {
    try {
      return load();
    } catch (e) {
      // try next candidate
    }
  }
  throw new Error(
    "Could not resolve mammoth. Run with NODE_PATH pointing at create/node_modules.",
  );
}

// "1:30" -> 90 ; "1:02:30" -> 3750 ; invalid -> null
function tsToSeconds(ts) {
  const parts = ts.split(":").map(Number);
  if (parts.some((n) => Number.isNaN(n))) {
    return null;
  }
  if (parts.length === 2) {
    return parts[0] * 60 + parts[1];
  }
  if (parts.length === 3) {
    return parts[0] * 3600 + parts[1] * 60 + parts[2];
  }
  return null;
}

// Match standalone timestamps not glued to other word chars or colons.
const TS_RE = /(?<![\w:])(\d{1,2}:\d{2}(?::\d{2})?)(?![\w:])/g;

function wrapTimestampsInText(text, uuid) {
  return text.replace(TS_RE, (m, ts) => {
    const sec = tsToSeconds(ts);
    if (sec === null) {
      return m;
    }
    return `<page-anchor target="#${uuid}" value="${sec}">${ts}</page-anchor>`;
  });
}

// Only wrap timestamps in text segments, never inside HTML tags/attributes.
function wrapTimestamps(html, uuid) {
  return html
    .split(/(<[^>]+>)/)
    .map((seg, i) => (i % 2 === 1 ? seg : wrapTimestampsInText(seg, uuid)))
    .join("");
}

// --- optional CLI flag parsing ---------------------------------------------
function parseFlags(argv) {
  const flags = {
    authorProfile: null,
    description: null,
    puppeteerJson: null,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--author-profile") {
      flags.authorProfile = argv[++i];
    } else if (a === "--description") {
      flags.description = argv[++i];
    } else if (a === "--puppeteer-json") {
      flags.puppeteerJson = argv[++i];
    }
  }
  return flags;
}

function defaultDescription(title) {
  // Generic, SEO-friendly fallback when no description is supplied.
  const clean = title.replace(/\s*\-\s*Conversation with HAX$/i, "").trim();
  return `A HAX tutorial conversation: ${clean}. Written walkthrough with screenshots and an embedded video.`;
}

// --- Details / provenance block --------------------------------------------
// Resolve the HAXcms version baked into the scaffolded site (package.json),
// falling back to the create CLI version, then the literal "unknown".
function resolveHaxcmsVersion(siteDir) {
  const candidates = [
    path.join(siteDir, "package.json"),
    path.join(os.homedir(), "Documents/git/haxtheweb/create/package.json"),
  ];
  for (let i = 0; i < candidates.length; i++) {
    try {
      const p = candidates[i];
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

// Build the bottom-of-page Details/provenance section. screenshotFilenames are
// the bare filenames written to files/images/. docxSiteRelPath and
// puppeteerSiteRelPath are site-relative paths (e.g. "files/foo.docx").
// puppeteerSiteRelPath may be null to omit the automation sub-section.
function buildDetailsSection(
  watchUrl,
  screenshotFilenames,
  docxSiteRelPath,
  lastUpdated,
  haxVersion,
  puppeteerSiteRelPath,
) {
  let imageLinks = "";
  if (screenshotFilenames.length > 0) {
    const items = screenshotFilenames
      .map((f) => `      <li><a href="files/images/${f}">${f}</a></li>`)
      .join("\n");
    imageLinks = `    <li>Images in this page
      <ul>
${items}
      </ul>
    </li>`;
  } else {
    imageLinks = "    <li>Images in this page: none</li>";
  }

  let html = `<h2>Details</h2>
<ul>
    <li><a href="${watchUrl}">YouTube video</a></li>
${imageLinks}
    <li><a href="${docxSiteRelPath}">Source transcript (DOCX)</a></li>
    <li>Last updated: ${lastUpdated}</li>
    <li>HAXcms version: ${haxVersion}</li>
</ul>`;

  if (puppeteerSiteRelPath) {
    html += `\n<h3>Automation recording</h3>\n<p><a href="${puppeteerSiteRelPath}">Puppeteer recording (JSON)</a></p>`;
  }

  return html + "\n";
}

// --- site.json metadata finalization ---------------------------------------
function finalizeSiteMetadata(siteDir, videoTitle, description, authorProfilePath) {
  const siteJsonPath = path.join(siteDir, "site.json");
  const manifest = JSON.parse(fs.readFileSync(siteJsonPath, "utf8"));

  // title + description
  manifest.title = videoTitle;
  manifest.description = description || defaultDescription(videoTitle);

  // author profile -> metadata.author (and top-level author string fallback)
  if (authorProfilePath && fs.existsSync(authorProfilePath)) {
    const profile = JSON.parse(fs.readFileSync(authorProfilePath, "utf8"));
    const author = profile && profile.author ? profile.author : null;
    if (author && typeof author === "object") {
      // resume-theme reads: name, image, email, phone, location, website,
      // website2, socialLink, socialLink2 from manifest.metadata.author.
      manifest.metadata = manifest.metadata || {};
      manifest.metadata.author = author;
      // top-level author: string for legacy fallback paths in HAXCMS.js
      manifest.author = author.name || "";
    }
  }

  // NEVER change metadata.site.name (must equal the folder name) — leave it.
  fs.writeFileSync(siteJsonPath, JSON.stringify(manifest, null, 2) + "\n");
  return {
    siteJsonPath,
    authorInjected: !!(
      manifest.metadata &&
      manifest.metadata.author &&
      manifest.metadata.author.name
    ),
  };
}

async function main() {
  const rawArgv = process.argv.slice(2);
  const flags = parseFlags(rawArgv);
  // positional args = everything that isn't a --flag or its value
  const skipNext = new Set();
  for (let i = 0; i < rawArgv.length; i++) {
    if (
      rawArgv[i] === "--author-profile" ||
      rawArgv[i] === "--description" ||
      rawArgv[i] === "--puppeteer-json"
    ) {
      skipNext.add(i);
      skipNext.add(i + 1);
    }
  }
  const positional = rawArgv.filter((_, i) => !skipNext.has(i));

  const [docxPath, siteDir, uuid, watchUrl, videoTitle] = positional;

  if (!docxPath || !siteDir || !uuid || !watchUrl || !videoTitle) {
    console.error(
      "Usage: node docx-to-content.cjs <docx> <site-dir> <video-player-uuid> <youtube-watch-url> <video-title> [--author-profile <path>] [--description <text>] [--puppeteer-json <path>]",
    );
    process.exit(1);
  }
  if (!fs.existsSync(docxPath)) {
    console.error(`DOCX not found: ${docxPath}`);
    process.exit(1);
  }
  if (!fs.existsSync(siteDir)) {
    console.error(`Site dir not found: ${siteDir}`);
    process.exit(1);
  }

  // default author profile lives next to this script in references/
  const authorProfilePath =
    flags.authorProfile ||
    path.join(__dirname, "..", "references", "author-profile.json");

  const mammoth = resolveMammoth();

  const imagesDir = path.join(siteDir, "files", "images");
  fs.mkdirSync(imagesDir, { recursive: true });
  let imgCount = 0;
  const screenshotFilenames = [];

  // mammoth image converter: write each screenshot to files/images/ and
  // rewrite the <img src> to a site-relative path so media lives with the site.
  const imageConverter = mammoth.images.imgElement(async (image) => {
    imgCount++;
    const buf = await image.read();
    const ct = (image.contentType || "image/png").toLowerCase();
    let ext = (ct.split("/")[1] || "png").replace("jpeg", "jpg");
    const filename = `screenshot-${imgCount}.${ext}`;
    fs.writeFileSync(path.join(imagesDir, filename), buf);
    screenshotFilenames.push(filename);
    return { src: `files/images/${filename}` };
  });

  // mirror the mammoth options used by the official importDocx route
  const mammothOptions = {
    convertImage: imageConverter,
    styleMap: ["u => em", "strike => del"],
  };

  const buffer = fs.readFileSync(docxPath);
  const result = await mammoth.convertToHtml({ buffer }, mammothOptions);
  let contentHtml = result.value || "";

  // wrap timestamp tokens -> <page-anchor> (in-page seeking)
  contentHtml = wrapTimestamps(contentHtml, uuid);

  // prepend the video player carrying the matching UUID
  const escapedTitle = videoTitle.replace(/"/g, "&quot;");
  const videoPlayer = `<video-player id="${uuid}" source="${watchUrl}" media-title="${escapedTitle}" data-width="100" data-margin="center"></video-player>`;

  // --- Details / provenance section ----------------------------------------
  // Copy the source DOCX into files/ so the page can link the artifact that
  // produced the content. files/ already exists (images dir was created), but
  // ensure it for the no-screenshot case.
  const filesDir = path.join(siteDir, "files");
  fs.mkdirSync(filesDir, { recursive: true });
  const docxBasename = path.basename(docxPath);
  const docxDestPath = path.join(filesDir, docxBasename);
  fs.copyFileSync(docxPath, docxDestPath);
  const docxSiteRelPath = `files/${docxBasename}`;

  // Optional puppeteer JSON: copy into files/ and link it at the bottom of the
  // Details section.
  let puppeteerSiteRelPath = null;
  if (flags.puppeteerJson) {
    if (!fs.existsSync(flags.puppeteerJson)) {
      console.error(`Puppeteer JSON not found: ${flags.puppeteerJson}`);
      process.exit(1);
    }
    const puppeteerBasename = path.basename(flags.puppeteerJson);
    fs.copyFileSync(flags.puppeteerJson, path.join(filesDir, puppeteerBasename));
    puppeteerSiteRelPath = `files/${puppeteerBasename}`;
  }

  const haxVersion = resolveHaxcmsVersion(siteDir);
  const lastUpdated = formatLastUpdated();
  const detailsHtml = buildDetailsSection(
    watchUrl,
    screenshotFilenames,
    docxSiteRelPath,
    lastUpdated,
    haxVersion,
    puppeteerSiteRelPath,
  );

  const pageHtml = `${videoPlayer}\n${contentHtml}\n${detailsHtml}`;

  // Resolve the root page's location from site.json so we overwrite the
  // skeleton's actual placeholder page (its folder is UUID-based, not
  // pages/tutorial). Falls back to pages/tutorial/index.html if site.json
  // is missing or has no root item.
  let pageFile = path.join(siteDir, "pages", "tutorial", "index.html");
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
    // fall back to pages/tutorial/index.html
  }
  fs.mkdirSync(path.dirname(pageFile), { recursive: true });
  fs.writeFileSync(pageFile, pageHtml);

  // finalize site.json: title, description, and author profile injection
  const meta = finalizeSiteMetadata(
    siteDir,
    videoTitle,
    flags.description,
    authorProfilePath,
  );

  console.log(
    JSON.stringify(
      {
        pageFile,
        imagesWritten: imgCount,
        videoPlayerId: uuid,
        contentLength: pageHtml.length,
        siteJson: meta.siteJsonPath,
        authorInjected: meta.authorInjected,
        authorProfileUsed: fs.existsSync(authorProfilePath)
          ? authorProfilePath
          : null,
        detailsSection: true,
        haxVersion,
        lastUpdated,
        docxCopied: docxSiteRelPath,
        puppeteerJsonCopied: puppeteerSiteRelPath,
      },
      null,
      2,
    ),
  );
}

main().catch((e) => {
  console.error(e && e.message ? e.message : String(e));
  process.exit(1);
});
