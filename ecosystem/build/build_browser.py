"""HAXcms in the browser sub-web: what haxcms-browser (browser.hax.cloud) does, and the services it works with.

Curated from haxcms-browser's README and docs/providers.md (haxtheweb/issues#3331 runs HAXcms in a tab;
haxtheweb/issues#3341 adds sign-in, cloud storage and publishing). Each service is a tile with how it is used
and what it needs set up; parts of the main web (HAXcms Node.js, Deploy targets, the HAX CLI) are portals.

  hax-browser.mmd   the browser runtime, where sites are saved, sign-in and publishing   (main web: HAXcms in the browser)"""
import json, re
GH = "https://github.com/haxtheweb"
REPO = GH + "/haxcms-browser"
DOCS = REPO + "/blob/main/docs/providers.md"
ISS = "https://github.com/haxtheweb/issues/issues/"
def L(a, b): return {"label": a, "url": b}
def S(c, *i): return {"caption": c, "nodes": list(i)}
def anchor(h): return DOCS + "#" + re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", h.lower()).strip())
MAIN = set(re.findall(r"^\s+(\w+)[\[\(\{>]", open("hax-ecosystem.mmd").read(), re.M))

# id, label, mono, desc, docs heading (None: nothing to register), status
RUNTIME = [
    ("br_worker", "haxcms-nodejs in a Worker", None, "The whole haxcms-nodejs app, bundled with esbuild, running in a Web Worker with an in-memory file system. Every result must match haxcms-nodejs on Node: a parity scenario runs the same requests on both.", None, "deployed"),
    ("br_relay", "Service worker relay", None, "The HAXcms pages in the frame ask for URLs as usual; the service worker hands each request to the page that owns the Worker and returns its answer. Nothing HAXcms asks for reaches the web server.", None, "deployed"),
    ("br_broker", "Publish broker", None, "Small stateless Vercel functions deployed with the page: they finish sign-ins with each app's client secret and pass Surge uploads on. They keep nothing and only answer their own page.", "How it fits together", "deployed"),
]
STORAGE = [
    ("st_folder", "A folder", None, "A folder the person picks on their computer (File System Access, Chromium browsers). Each site is a normal HAXsite folder in it.", None, "deployed"),
    ("st_browser", "This browser", None, "The browser's own private file system: the default, and what Firefox and Safari use. Browsers can clear it when space runs low, so the bar suggests a folder or the cloud.", None, "deployed"),
    ("st_gdrive", "Google Drive", "GD", "A \"HAXcms sites\" folder in the person's Drive, with the drive.file scope: HAXcms only reaches files it made.", "Google (sign-in, Google Drive)", "in-progress"),
    ("st_onedrive", "OneDrive", "OD", "OneDrive's Apps/<app> folder, the only folder the app can reach (Files.ReadWrite.AppFolder).", "Microsoft (sign-in, OneDrive)", "in-progress"),
    ("st_dropbox", "Dropbox", "DB", "Dropbox's app folder, with scoped access.", "Dropbox (cloud storage)", "in-progress"),
    ("st_box", "Box", "BX", "A \"HAXcms sites\" folder in Box. Box only answers browser calls from origins listed on the app.", "Box (cloud storage)", "in-progress"),
    ("st_webdav", "Nextcloud / WebDAV", "DAV", "Any WebDAV server the person points at, with an app password that is never stored. The server has to allow the page's origin (for Nextcloud, the WebAppPassword app).", "Nextcloud and other WebDAV servers: set up on the server", "in-progress"),
]
SIGNIN = [
    ("si_google", "Google", "G", "Sign in with Google; name, email and picture become the author of new sites.", "Google (sign-in, Google Drive)", "in-progress"),
    ("si_microsoft", "Microsoft", "MS", "Sign in with a work, school or personal Microsoft account.", "Microsoft (sign-in, OneDrive)", "in-progress"),
    ("si_github", "GitHub", "GH", "Sign in with GitHub through the HAX GitHub App.", "GitHub (sign-in, GitHub Pages)", "in-progress"),
    ("si_gitlab", "GitLab", "GL", "Sign in with GitLab.com.", "GitLab (sign-in, GitLab Pages)", "in-progress"),
    ("si_apple", "Apple", "A", "Sign in with Apple; Apple posts back to the broker, which passes on only the name and email.", "Apple (sign-in)", "in-progress"),
]
PUBLISH = [
    ("pb_surge", "Surge", "SG", "Free *.surge.sh addresses with a Surge token or email and password, through the broker (up to about 4 MB per site; the dialog says so).", "Surge (publishing): no setup", "deployed"),
    ("pb_ghpages", "GitHub Pages", "GH", "A public repository named after the site, with .nojekyll, and Pages turned on.", "GitHub (sign-in, GitHub Pages)", "in-progress"),
    ("pb_glpages", "GitLab Pages", "GL", "A public project with the site in public/ and a .gitlab-ci.yml pages job.", "GitLab (sign-in, GitLab Pages)", "in-progress"),
    ("pb_cbpages", "Codeberg Pages", "CB", "A public repository with the site on its pages branch and the git-pages webhook.", "Codeberg (Codeberg Pages)", "in-progress"),
    ("pb_netlify", "Netlify", "NF", "A Netlify site, deployed by file digest so republishing sends only what changed.", "Netlify (publishing)", "in-progress"),
    ("pb_vercel", "Vercel", "VC", "A production deployment of a Vercel project, through the HAX Vercel integration.", "Vercel (publishing)", "in-progress"),
    ("pb_download", "Download site", None, "Always there: HAXcms's own zip of the site, to publish anywhere with the HAX CLI.", None, "deployed"),
]
PORTALS = ["nodejs", "deploy", "cli", "haxcms"]
missing = [p for p in PORTALS if p not in MAIN]
assert not missing, "not tiles in hax-ecosystem.mmd: " + ", ".join(missing)

GROUPS = [("rt", "How it runs", RUNTIME), ("sg", "Where sites are saved", STORAGE), ("sig", "Sign in with", SIGNIN), ("pg", "Publish to", PUBLISH)]
lines = ["%% HAXcms in the browser sub-web, generated by build_browser.py from haxcms-browser's README and docs/providers.md.",
         "%% Portals: ids from hax-ecosystem.mmd. Details in hax-browser.json.",
         "flowchart TB", "  %%@ layout rings=0,200,430,690,950 sizes=92,58,50,46,44",
         '  subgraph hub ["HAXcms in the browser"]', '    browser(("HAXcms in the browser"))', "  end"]
for gid, glabel, items in GROUPS:
    lines.append(f'  subgraph {gid} ["{glabel}"]')
    lines += [f'    {i[0]}["{i[1]}"]' for i in items]
    lines.append("  end")
lines += ['  subgraph partsg ["Parts of HAX"]'] + [f'    {p}["{p}"]' for p in PORTALS] + ["  end", ""]
lines += ["  browser -->|runs| br_worker", "  browser -->|relays through| br_relay", "  browser -->|signs in through| br_broker",
          "  br_worker -.->|bundles| nodejs", "  br_worker -->|serves| haxcms"]
lines += [f"  browser -->|saves to| {i[0]}" for i in STORAGE]
lines += [f"  browser -->|signs in with| {i[0]}" for i in SIGNIN]
lines += [f"  browser -->|publishes to| {i[0]}" for i in PUBLISH]
lines += ["  br_broker -->|passes on| pb_surge", "  pb_download -->|then| cli"]
lines += [f"  {i[0]} -->|is one of the| deploy" for i in PUBLISH if i[0] not in ("pb_download",)]
lines += ["", "  %%@ group hub tier=0", "  %%@ group rt tier=1", "  %%@ group sg tier=2", "  %%@ group sig tier=3", "  %%@ group pg tier=3", "  %%@ group partsg tier=4",
          "  %%@ node browser icon=icons:chrome-reader-mode color=skyBlue motion=pulse",
          "  %%@ node br_worker icon=hardware:memory color=limestoneGray motion=spin",
          "  %%@ node br_relay icon=hax:remote color=slateGray motion=nudge",
          "  %%@ node br_broker icon=icons:lock-open color=coalyGray motion=nudge",
          "  %%@ node st_folder icon=icons:folder-open color=creekTeal motion=lift",
          "  %%@ node st_browser icon=icons:dns color=creekTeal motion=lift",
          "  %%@ node pb_download icon=icons:cloud-upload color=pughBlue motion=lift"]
for items, color, motion in ((STORAGE, "creekTeal", "lift"), (SIGNIN, "wonderPurple", "pop"), (PUBLISH, "pughBlue", "lift")):
    for i in items:
        if i[2]:
            lines.append(f"  %%@ node {i[0]} mono={i[2]} color={color} motion={motion}")
lines += [f"  %%@ node {p} portal" for p in PORTALS]
open("hax-browser.mmd", "w").write("\n".join(lines) + "\n")

KIND = {"rt": "runtime", "sg": "storage", "sig": "signin", "pg": "publish"}
nodes = {"browser": {"always": True, "desc": "haxcms-nodejs running in a browser tab at browser.hax.cloud: make sites with no install, keep them in a folder, the browser or cloud storage, sign in with an account you have, and publish for free. Which services a deployment offers depends on the OAuth apps whoever runs it registers (docs/providers.md).",
                     "links": {"try it": "https://browser.hax.cloud", "repo": REPO, "setup": DOCS, "issue": ISS + "3341"}}}
for gid, _, items in GROUPS:
    for i, label, mono, desc, heading, status in items:
        n = {"desc": desc, "kind": KIND[gid], "status": status, "links": {}}
        if heading:
            n["links"]["setup"] = anchor(heading)
        if status == "in-progress":
            n["note"] = "Built; works once the deployment registers this service's app (haxtheweb/issues#3341)."
            n["links"]["issue"] = ISS + "3341"
        nodes[i] = n
tours = [{"id": "zero-to-published", "label": "From zero to a published site", "kind": "story",
          "message": "No install, no server: sign in, keep the site somewhere safe, publish it free.",
          "scenes": [S("Open browser.hax.cloud: HAXcms Node.js runs in the tab.", "browser", "br_worker", "nodejs"),
                     S("Sign in with an account you have; you become the author of the sites you make.", "browser", *[i[0] for i in SIGNIN], "br_broker"),
                     S("Keep the sites in a folder, the browser or cloud storage you already have.", "browser", *[i[0] for i in STORAGE]),
                     S("Publish free, straight from the browser.", "browser", *[i[0] for i in PUBLISH], "deploy"),
                     S("All of it.")]}]
meta = {"name": "HAXcms in the browser", "slug": "haxcms-browser", "parent": "main", "noTimeline": True,
        "sectionLabels": {"runtime": "how it runs", "storage": "where sites are saved", "signin": "sign in with", "publish": "publish to"},
        "about": "What haxcms-browser does and the services it works with, from its README and docs/providers.md. Services marked in progress are built and need their OAuth app registered on a deployment before they show.",
        "links": {"try it": "https://browser.hax.cloud", "repo": REPO, "setup": DOCS}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-browser.json", "w"), indent=1, ensure_ascii=False)
print(len(nodes), "nodes")
