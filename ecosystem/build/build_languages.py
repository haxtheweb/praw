"""Languages sub-web: which elements speak which languages, and the tooling that makes it work.
Generated from the built packages (each package's locales/ folder) and i18n-manager's languages.json and translation-manifest.json. Details in hax-languages.json."""
import json, os, re, glob, collections
GH = "https://github.com/haxtheweb"
WC = GH + "/webcomponents/tree/master/elements/"
B = "haxcms-nodejs/src/public/build/es6/node_modules/@haxtheweb"
def S(c, *i): return {"caption": c, "nodes": list(i)}
def slug(s): return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
EL_IDS = set(re.findall(r"^    (b_[a-z0-9_]+)", open("hax-elements.mmd").read(), re.M))
LJ = json.load(open(B + "/i18n-manager/lib/languages.json"))["languages"]
MAN = json.load(open(B + "/i18n-manager/lib/translation-manifest.json"))["_meta"]
pkgs = sorted(os.listdir(B))
per = {}
for p in pkgs:
    d = os.path.join(B, p, "locales")
    if os.path.isdir(d):
        ls = {m.group(1) for f in os.listdir(d) for m in [re.match(r".+?\.([a-z]{2,3}(?:-[A-Za-z]+)?)\.(?:haxProperties\.)?json$", f)] if m}
        if ls: per[p] = ls
def has_strings(p):
    t = "".join(open(f, errors="ignore").read() for f in glob.glob(os.path.join(B, p, "*.js")) + glob.glob(os.path.join(B, p, "lib", "*.js")))
    return bool(re.search(r"this\.t\s*=\s*\{", t))
ready = [p for p in pkgs if p not in per and has_strings(p) and p != "i18n-manager"]
langcount = collections.Counter(l for v in per.values() for l in v)
base = {k: v for k, v in LJ.items() if not v.get("parent")}
variants = {k: v for k, v in LJ.items() if v.get("parent")}
full = [p for p, v in per.items() if len(v) >= 100]
partial = [p for p, v in per.items() if len(v) < 100]
none = [p for p in pkgs if p not in per and p not in ready]
langs = sorted([k for k in base if langcount.get(k)], key=lambda k: base[k]["name"])
rtl = [k for k in langs if base[k].get("dir") == "rtl"]
lines = ["%% Languages sub-web: which elements speak which languages, generated from the built packages' locales folders and i18n-manager's language registry.",
         "%% Portals: ids from hax-ecosystem.mmd, hax-skills.mmd and hax-haxschema.mmd. Details in hax-languages.json.",
         "flowchart TB", "  %%@ layout rings=0,210,420,610,900 sizes=92,60,60,52,40",
         '  subgraph hub ["Languages"]', '    languages["languages"]', "  end",
         '  subgraph tools ["How it works"]', '    lg_manager["i18n-manager"]', '    lg_mixin["I18NMixin"]', '    lg_registry[("languages.json")]', '    lg_manifest[("translation-manifest.json")]',
         '    lg_files["locales folder"]', '    hslocale["hslocale"]', '    s_hax_i18n_translate["s_hax_i18n_translate"]', '    lg_picker["Language picker"]', "  end",
         '  subgraph bands ["How much is translated"]', '    lg_full["Every language"]', '    lg_partial["Some languages"]', '    lg_ready["Strings ready, not translated yet"]', '    lg_none["No strings to translate"]', "  end",
         '  subgraph dirs ["Writing direction"]', '    lg_ltr["Left to right"]', '    lg_rtl["Right to left"]', '    lg_variants["Regional variants"]', "  end"]
lines += ['  subgraph rdy ["Next to translate"]']
for p in ready: lines.append(f'    {"b_" + p.replace("-", "_")}["{p}"]')
lines += ["  end", '  subgraph langsg ["Languages"]']
for k in langs: lines.append(f'    lang_{slug(k)}["{base[k]["name"]}"]')
lines += ["  end", "",
          "  languages -->|runs on| lg_manager", "  lg_mixin -->|registers elements with| lg_manager", "  lg_manager -->|reads| lg_registry", "  lg_manager -->|loads| lg_files", "  lg_manifest -.->|indexes| lg_files",
          "  hslocale -.->|translates editor labels in| lg_files", "  s_hax_i18n_translate -->|writes| lg_files", "  lg_picker -->|sets the language for| lg_manager",
          "  lg_files -->|cover| lg_full", "  lg_files -->|cover| lg_partial", "  lg_mixin -->|is ready in| lg_ready", "  languages -->|counts| lg_none",
          "  lg_registry -->|lists| lg_ltr", "  lg_registry -->|lists| lg_rtl", "  lg_registry -->|maps| lg_variants"]
for p in ready: lines.append(f'  lg_ready -->|includes| {"b_" + p.replace("-", "_")}')
for k in langs:
    lines.append(f"  {'lg_rtl' if k in rtl else 'lg_ltr'} -->|includes| lang_{slug(k)}")
lines += ["", "  %%@ group hub tier=0", "  %%@ group tools tier=1", "  %%@ group bands tier=2", "  %%@ group dirs tier=2", "  %%@ group rdy tier=3", "  %%@ group langsg tier=4",
          "  %%@ node languages portal", "  %%@ node hslocale portal=haxschema", "  %%@ node s_hax_i18n_translate portal=skills",
          "  %%@ node lg_manager icon=icons:translate color=skyBlue motion=tilt", "  %%@ node lg_mixin icon=hax:code-json color=skyBlue motion=nudge", "  %%@ node lg_registry icon=hax:code-json color=skyBlue motion=nudge",
          "  %%@ node lg_manifest icon=hax:code-json color=skyBlue motion=nudge", "  %%@ node lg_files icon=icons:folder-open color=skyBlue motion=nudge", "  %%@ node lg_picker icon=icons:translate color=beaverBlue motion=pop",
          "  %%@ node lg_full icon=icons:check-circle color=forestGreen motion=pop", "  %%@ node lg_partial icon=icons:translate color=roarGolden motion=pop", "  %%@ node lg_ready icon=icons:build color=inventOrange motion=pop", "  %%@ node lg_none icon=icons:view-day color=limestoneGray motion=nudge",
          "  %%@ node lg_ltr mono=LTR color=creekTeal motion=nudge", "  %%@ node lg_rtl mono=RTL color=creekTeal motion=nudge", "  %%@ node lg_variants mono=VAR color=creekTeal motion=nudge"]
for p in ready:
    i = "b_" + p.replace("-", "_")
    lines.append(f"  %%@ node {i} portal=elements" if i in EL_IDS else f"  %%@ node {i} icon=hax:bricks color=inventOrange motion=nudge")
for k in langs: lines.append(f"  %%@ node lang_{slug(k)} mono={k.upper()[:4]} color={'athertonViolet' if k in rtl else 'skyBlue'} motion=nudge")
open("hax-languages.mmd", "w").write("\n".join(lines) + "\n")
I18N = WC + "i18n-manager"
nodes = {"languages": {"always": True},
         "lg_manager": {"desc": "i18n-manager: the singleton every element registers with. It knows the reader's language, loads each element's translation file on demand and tells elements when the language changes.", "links": {"code": I18N}},
         "lg_mixin": {"desc": "I18NMixin: what an element extends to get a this.t object of English strings and have it swapped for the reader's language.", "links": {"code": I18N + "/lib/I18NMixin.js"}},
         "lg_registry": {"desc": f"languages.json: the canonical registry. {len(base)} languages with English and native names and writing direction, plus {len(variants)} regional variants that resolve to their parent.", "links": {"code": I18N + "/lib/languages.json"}},
         "lg_manifest": {"desc": f"translation-manifest.json: built by scanning the elements. {MAN['elementsScanned']} elements scanned, {MAN['elementsWithTranslations']} with translations, {MAN['translationFilesFound']:,} translation files.", "links": {"code": I18N + "/lib/translation-manifest.json"}},
         "lg_files": {"desc": "Each element keeps locales/<tag>.<lang>.json for its own strings and locales/<tag>.haxProperties.<lang>.json for its editor labels."},
         "lg_picker": {"desc": "haxcms-language-picker: the site setting that chooses a site's language, which the editor and every element on the page follow."},
         "lg_full": {"desc": f"{len(full)} packages are translated into 100 or more languages.", "kind": "band"},
         "lg_partial": {"desc": f"{len(partial)} packages have some translation files: {', '.join(partial)}." if partial else "None.", "kind": "band"},
         "lg_ready": {"desc": f"{len(ready)} packages already keep their strings in this.t but have no translation files yet, so they are the next to translate.", "kind": "band"},
         "lg_none": {"desc": f"{len(none)} packages show no text of their own (behaviors, utilities, wrappers), so there is nothing to translate.", "kind": "band"},
         "lg_ltr": {"desc": f"{len(langs) - len(rtl)} languages written left to right.", "kind": "dir"},
         "lg_rtl": {"desc": f"{len(rtl)} languages written right to left: {', '.join(base[k]['name'] for k in rtl)}. Elements flip their layout for these.", "kind": "dir"},
         "lg_variants": {"desc": f"{len(variants)} regional variants, such as {', '.join(list(variants)[:6])}, resolve to their parent language's files.", "kind": "dir"}}
for p in ready:
    i = "b_" + p.replace("-", "_")
    if i not in EL_IDS: nodes[i] = {"desc": f"@haxtheweb/{p}: keeps its strings in this.t; no translation files yet.", "links": {"repo": WC + p}, "kind": "element"}
for k in langs:
    v = base[k]
    nodes[f"lang_{slug(k)}"] = {"desc": f"{v['name']} ({v['nativeName']}), locale {v['locale']}, {'right to left' if v.get('dir') == 'rtl' else 'left to right'}. {langcount[k]} packages translated.", "kind": "language"}
tours = [{"id": "languages", "label": "Every element, every language", "message": f"{len(per)} packages translated into {len(langs)} languages, and how it works.", "scenes": [
    S("Elements extend I18NMixin and register with i18n-manager.", "lg_manager", "lg_mixin"),
    S("Translations live next to each element, indexed by a manifest and a shared language registry.", "lg_files", "lg_registry", "lg_manifest", "hslocale"),
    S("The hax-i18n-translate skill writes them; the site's language picker chooses one.", "s_hax_i18n_translate", "lg_picker"),
    S("How much is translated.", "lg_full", "lg_partial", "lg_ready", "lg_none"),
    S("Next to translate.", "lg_ready", *["b_" + p.replace("-", "_") for p in ready]),
    S("Right to left languages flip the layout.", "lg_rtl", *[f"lang_{slug(k)}" for k in rtl]),
    S(f"All {len(langs)} languages.", "lg_ltr", "lg_rtl", *[f"lang_{slug(k)}" for k in langs]), ]}]
meta = {"name": "Languages", "parent": "main", "noTimeline": True, "sectionLabels": {"band": "coverage", "dir": "writing direction", "language": "languages", "element": "elements"},
        "about": f"Which elements speak which languages, generated from the built packages: {len(per)} of {len(pkgs)} packages ship translations, almost all in {len(langs)} languages, from {MAN['translationFilesFound']:,} translation files. The rest either have strings ready to translate or show no text.",
        "kindLabels": {"rel": "tooling, coverage and languages", "schema": "files and schemas"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-languages.json", "w"), indent=1, ensure_ascii=False)
json.dump({"packages": sorted(per), "ready": ready, "languages": langs}, open("ext/languages_report.json", "w"))
print(len(per), "translated;", len(ready), "ready;", len(langs), "languages;", len(rtl), "rtl")
