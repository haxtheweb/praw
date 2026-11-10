import json, glob, os, base64, io
from PIL import Image

D = "ext/el/hn/package/dist/"
themes = json.load(open(D + "coreConfig/themes.json"))
skels = {os.path.basename(f): json.load(open(f)) for f in sorted(glob.glob("haxcms-nodejs/src/coreConfig/skeletons/*.json"))}
images = {}
DIRS = set(open("ext/el/elements-dirs.txt").read().split())
WC = "https://github.com/haxtheweb/webcomponents/tree/master/elements/"
ISS = "https://github.com/haxtheweb/issues/issues/"
def L(a, b): return {"label": a, "url": b}

FAM = {  # theme -> family
 "clean-one": "course", "clean-two": "course", "learn-two-theme": "course",
 "polaris-theme": "polaris", "polaris-flex-theme": "polaris", "polaris-flex-sidebar": "polaris", "polaris-invent-theme": "polaris",
 "clean-portfolio-theme": "portfolio", "glossy-portfolio-theme": "portfolio", "resume-theme": "portfolio", "journey-theme": "portfolio",
 "haxma-theme": "docs",
 "bootstrap-theme": "site", "spacebook-theme": "site", "link-card-theme": "site", "twenty-six-theme": "site",
 "terrible-themes": "fun", "terrible-best-themes": "fun", "terrible-outlet-themes": "fun", "terrible-productionz-themes": "fun", "terrible-resume-themes": "fun",
}
FAMS = {"course": ("Course reading", "hax:lesson", "opportunityGreen"), "polaris": ("Polaris (Penn State)", "hax:site-map", "nittanyNavy"),
        "portfolio": ("Portfolio and resume", "hax:view-gallery", "wonderPurple"), "docs": ("Documentation", "hax:documents", "creekTeal"),
        "site": ("General websites", "hax:3-3-3-3", "inventOrange"), "fun": ("Terrible (for fun)", "places:casino", "discoveryCoral")}
NOTES = {
 "clean-one": "One of HAX's two major course reading themes, used about as much as Clean Two; their reading typography should stay the same.",
 "clean-two": "One of HAX's two major course reading themes, used about as much as Clean One.",
 "learn-two-theme": "A popular course-content theme.",
 "polaris-invent-theme": "haxtheweb.org uses Polaris Invent.",
 "polaris-flex-theme": "Covers many psu.edu patterns, including mega menus.",
}
visible = [t for t in themes if t in FAM]
for t in visible:
    p = D + "public/build/es6/node_modules/" + themes[t]["thumbnail"]
    im = Image.open(p).convert("RGB"); im.thumbnail((160, 160))
    w, h = im.size; s = min(w, h); im = im.crop(((w - s) // 2, 0, (w - s) // 2 + s, s)).resize((112, 112))
    b = io.BytesIO(); im.save(b, "JPEG", quality=70); images["theme-" + t] = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def tid(t): return "t_" + t.replace("-", "_")
def sid(f): return "k_" + os.path.splitext(f)[0].lower().replace("-", "_")
SKEL_USE = {"art-portfolio.json": "portfolio", "blog.json": "blog", "club-website.json": "club", "docs.json": "docs", "isc-graduate-portfolio.json": "portfolio",
            "online-course.json": "course", "portfolio.json": "portfolio", "resume-journey.json": "portfolio", "default-starter.json": None}
LOCAL_USE = {"blog": "Blog", "docs": "Documentation", "club": "Club website"}  # these live in the skeletons web
PEOPLE = [("winston", "polaris-theme", "built Polaris themes"), ("collin", "bootstrap-theme", "built"), ("nazman", "glossy-portfolio-theme", "built"),
          ("mcollins", "clean-portfolio-theme", "inspired")]

order = sorted(visible, key=lambda t: (list(FAMS).index(FAM[t]), themes[t]["name"].lower()))
lines = ["%% HAX themes sub-web: the themes offered in HAXcms, grouped by family, with the skeletons that use them.",
         "%% Portals: ids from hax-ecosystem.mmd. Screenshots come from the theme registry. Details in hax-themes.json.",
         "flowchart TB", "  %%@ layout rings=0,250,540,780 sizes=92,56,56,46",
         '  subgraph hub ["Themes"]', '    themes["themes"]', "  end", '  subgraph fams ["Theme families"]']
for f, (lab, ic, col) in FAMS.items(): lines.append(f'    fam_{f}["{lab}"]')
lines += ["  end", '  subgraph list ["Themes"]']
for t in order: lines.append(f'    {tid(t)}["{themes[t]["name"]}"]')
lines += ["  end", '  subgraph ks ["Skeletons, use cases and people"]']
for f in skels: lines.append(f'    {sid(f)}(["{skels[f]["meta"].get("useCaseTitle") or f}"])')
for p in sorted({v for v in SKEL_USE.values() if v} | {"skeletons", "ddd"}): lines.append(f'    {p}["{LOCAL_USE.get(p, p)}"]')
for p, _, _ in PEOPLE: lines.append(f'    {p}(("{p}"))')
lines += ["  end", ""]
for f in FAMS: lines.append(f"  themes -->|includes| fam_{f}")
for t in order: lines.append(f"  fam_{FAM[t]} -->|includes| {tid(t)}")
for f, d in skels.items():
    th = d.get("theme") if isinstance(d.get("theme"), str) else (d.get("build", {}) or {}).get("theme") or d["site"].get("theme")
    if isinstance(th, dict): th = th.get("element")
    if th in FAM: lines.append(f"  {sid(f)} -->|starts with| {tid(th)}")
    if SKEL_USE[f]: lines.append(f"  {sid(f)} -->|is a| {SKEL_USE[f]}")
    lines.append(f"  skeletons -->|includes| {sid(f)}")
for p, t, verb in PEOPLE: lines.append(f"  {p} ---|{verb}| {tid(t)}")
lines.append("  ddd -->|styles| fam_polaris")
lines += ["", "  %%@ group hub tier=0", "  %%@ group fams tier=1", "  %%@ group list tier=2", "  %%@ group ks tier=3", "  %%@ node themes portal"]
for f, (lab, ic, col) in FAMS.items(): lines.append(f"  %%@ node fam_{f} icon={ic} color={col} motion=pop")
for t in order: lines.append(f"  %%@ node {tid(t)} image=theme-{t} color={FAMS[FAM[t]][2]} motion=lift")
for f in skels: lines.append(f"  %%@ node {sid(f)} portal=skeletons")
for p in sorted({v for v in SKEL_USE.values() if v} | {"skeletons", "ddd"}): lines.append(f"  %%@ node {p} portal=skeletons" if p in LOCAL_USE else f"  %%@ node {p} portal")
for p, _, _ in PEOPLE: lines.append(f"  %%@ node {p} portal")
open("hax-themes.mmd", "w").write("\n".join(lines) + "\n")

nodes = {"themes": {"always": True}}
for f, (lab, ic, col) in FAMS.items():
    nodes["fam_" + f] = {"desc": f"{sum(1 for t in order if FAM[t] == f)} themes."}
for t in order:
    v = themes[t]; short = t
    d = {"desc": f"{v['name']}, a {'/'.join(v.get('category') or [])} theme" + (" made for fun." if v.get("terrible") else "."),
         "tag": t, "links": ({"repo": WC + t} if t in DIRS else {})}
    if t in NOTES: d["note"] = NOTES[t]
    nodes[tid(t)] = d
ev = {f"mcollins>{tid('clean-portfolio-theme')}": [L("Issue #392: michaelcollins.xyz clean-portfolio-theme", ISS + "392")],
      f"collin>{tid('bootstrap-theme')}": [L("Issue #212: bootstrap style boilerplate theme", ISS + "212")]}
def S(c, *i): return {"caption": c, "nodes": list(i)}
tours = [{"id": "themes", "label": "Themes and the skeletons that use them", "message": f"{len(order)} themes offered in HAXcms, grouped by family, with screenshots, and the skeletons that start from each.", "scenes": [
    S("Every HAX site picks a theme.", "themes"),
    S("Six families of themes.", *["fam_" + f for f in FAMS]),
    S("Course reading themes: Clean One, Clean Two and Learn2.", *[tid(t) for t in order if FAM[t] == "course"], "course"),
    S("Polaris themes bring Penn State patterns; haxtheweb.org runs on Polaris Invent.", *[tid(t) for t in order if FAM[t] == "polaris"], "winston", "ddd"),
    S("Portfolio and resume themes, many built by students.", *[tid(t) for t in order if FAM[t] == "portfolio"], "nazman", "mcollins", "portfolio"),
    S("Docs, general sites and the terrible ones, for fun.", *[tid(t) for t in order if FAM[t] in ("docs", "site", "fun")], "collin", "docs"),
    S("Skeletons start a site from a theme; open Skeletons for each one.", "skeletons", *[sid(f) for f in skels], "blog", "club"),
    S("Themes, skeletons and use cases together."),
]}]
meta = {"name": "HAX themes", "parent": "main", "noTimeline": True,
        "about": f"{len(order)} themes offered in HAXcms (hidden internal themes left out), with screenshots from the theme registry, grouped by family. {len(skels)} skeletons show which theme each starts from.",
        "kindLabels": {"rel": "families, skeletons (open the Skeletons web) and use cases", "contrib": "people who built or inspired a theme"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": ev, "tours": tours, "images": images}, open("hax-themes.json", "w"), indent=1, ensure_ascii=False)
print(len(order), "themes;", len(skels), "skeletons;", sum(len(v) for v in images.values()) // 1024, "KB images")
