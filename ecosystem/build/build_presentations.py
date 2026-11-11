import json

BA = "https://events.drupal.org/baltimore2017/sessions/mad-scientist-road-show"
NB = "https://events.drupal.org/nashville2018/sessions/webcomponents-polymer-and-hax-decoupling-authoring-drupal-and-beyond"
GC18 = "https://www.drupalgovcon.org/2018/program/sessions/hax-creating-best-drupal-authoring-experience-not-creating-it-drupal"
GC19 = "https://www.drupalgovcon.org/2019/program/sessions/future-proofing-design-work-web-components"
AP19 = "https://www.slideshare.net/slideshow/haxtheweb-apereo-19/148822203"
NJ23 = "https://2023.drupalcampnj.org/sessions/hax-decoupling-authoring-experience-drupal-use-anywhere"
FOSSY24 = "https://f.sfconservancy.org/Conservancy/2024.fossy.us/raw/branch/main/schedule/presentation/198/index.html"
TALKS = "https://github.com/haxtheweb/praw/blob/main/talks/README.md"
WINS = "https://github.com/haxtheweb/praw/blob/main/WINS.md"
PLAYLIST = "https://www.youtube.com/watch?v=q0IjUz2_IhA&list=PLJQupiji7J5eTqv8JFiW8SZpSeKouZACH"

def L(label, url): return {"label": label, "url": url}

ERA = lambda y: "beaverBlue" if y and y <= 2019 else "creekTeal" if y and y <= 2024 else "inventOrange" if y else "limestoneGray"

# id, title, year, kind(icon), venue, speakers, topics, links, desc, source
T = [
 ("t17balt", "Mad Scientist Road show", 2017, "image:slideshow", "drupalcon", ["bryan", "mikepotter"], ["elmsln", "editor", "wcstandard", "components"],
  {"session": BA}, "DrupalCon Baltimore. The ELMS:LN core team on web components, Polymer and \"what HAX is (and how far along we are with it).\" The first HAX talk.", L("DrupalCon Baltimore 2017 session", BA)),
 ("t18nash", "Webcomponents, Polymer and HAX", 2018, "image:slideshow", "drupalcon", ["bryan", "nikkimk"], ["editor", "components", "wcstandard"],
  {"session": NB}, "DrupalCon Nashville: decoupling authoring for Drupal and beyond. \"This isn't tied to Drupal; we've integrated it into Drupal which means it can integrate anywhere else easily.\"", L("DrupalCon Nashville 2018 session", NB)),
 ("t18gov", "HAX: the best Drupal authoring experience, by not making it for Drupal", 2018, "image:slideshow", "govcon", ["bryan"], ["editor"],
  {"session": GC18}, "Drupal GovCon 2018, in the DC area.", L("Drupal GovCon 2018 session", GC18)),
 ("t19seattle", "HAXcms announced at DrupalCon Seattle", 2019, "image:slideshow", "drupalcon", ["bryan"], ["haxcms", "components"],
  {"notes": WINS}, "Co-presented web components with Red Hat and announced HAXcms with an early prototype.", L("WINS.md: HAXcms announced at DrupalCon", WINS)),
 ("t19gov", "Future proofing design work with web components", 2019, "image:slideshow", "govcon", ["bryan"], ["components", "design"],
  {"session": GC19}, "Drupal GovCon 2019.", L("Drupal GovCon 2019 session", GC19)),
 ("t19apereo", "HAXTheWeb @ Apereo 19", 2019, "image:slideshow", "apereo", ["bryan"], ["editor", "haxcms"],
  {"slides": AP19}, "HAX and HAXcms for the Apereo higher-education open source community.", L("Slides on SlideShare", AP19)),
 ("t23njcamp", "HAX: decoupling authoring from Drupal to use anywhere", 2023, "image:slideshow", "drupalcampnj", ["bryan", "mikepotter", "zane"], ["editor"],
  {"session": NJ23}, "DrupalCamp NJ 2023.", L("DrupalCamp NJ 2023 session", NJ23)),
 ("t23ontology", "HAX Ontology", 2023, "hax:video", None, ["billrose"], ["course"],
  {"recording": "https://www.youtube.com/watch?v=iF4UZKcAWmw"}, "The course model under every instructional feature: outcomes, pedagogy, structure, instruction, content and assessment. \"It doesn't need to be ideal. It does need to be valid.\"", L("PRAW talks", TALKS)),
 ("t23horizon", "HAX Horizon Report", 2023, "hax:video", None, ["bryan"], ["haxcms", "jos", "hax11ty", "libraries", "themes"],
  {"recording": "https://www.youtube.com/watch?v=bX04I1Cw9FA"}, "Where HAX was and where it said it would go: every site is a site.json plus static HTML. \"When we blow up the notion of a database… we can build anything.\"", L("PRAW talks", TALKS)),
 ("t24hitech", "HiTech Podcast ep. 168: Reclaiming the Internet", 2024, "hax:podcast", "hitech", ["bryan"], ["elmsln", "wcstandard", "editor", "keithbailey", "mikepotter"],
  {"recording": "https://www.youtube.com/watch?v=fKeSEZm3khE"}, "The origin story in Bryan's words, with instructional designers reacting live. \"I don't want humanity to need to code in order to put themselves on the internet.\"", L("PRAW talks", TALKS)),
 ("t24fossy", "So you want a (web) revolution?", 2024, "image:slideshow", "fossy", ["bryan"], ["editor", "components", "open"],
  {"session": FOSSY24}, "A conference talk introducing HAX: \"My social cause: reduce the cost of web publishing to zero, regardless of ability.\"", L("PRAW talks", TALKS)),
 ("t25state", "2025: State of HAX Community", 2025, "hax:video", None, ["bryan"], ["haxlab", "ddd", "agents", "accessible", "efficient", "extensible", "open", "agnostic", "remixable", "sustainable"],
  {"recording": "https://www.youtube.com/watch?v=WGv94SY0cRM"}, "Year one of HAX Lab, the seven community pillars and the 2025 roadmap. \"Meet our users where they are, not where we wish them to be.\"", L("PRAW talks", TALKS)),
 ("t25fossy", "FOSSY 2025: ten years from a notepad", 2025, "image:slideshow", "fossy", ["bryan"], ["haxlab", "cli", "security"],
  {"notes": "https://btopro.com/work/fossy25"}, "HAX Lab, a student club, a security reporting pipeline, the HAX CLI and ten years of history.", L("btopro.com: FOSSY25", "https://btopro.com/work/fossy25")),
 ("t25wilson", "Next-level community building with HAX", 2025, "hax:documents", "apereo", ["bryan"], ["ist256", "haxlab", "grants", "cli", "portfolio"],
  {"article": "https://www.apereo.org/news/2025/next-level-community-building-hax"}, "An interview by Apereo Board Chair Joshua Wilson on Bryan's model for community building: a 200-level class that uses HAX, a weekly HAX Club, then paid HAX Lab internships, with college grants and the CLI letting agents build sites.", L("Apereo news, December 1, 2025", "https://www.apereo.org/news/2025/next-level-community-building-hax")),
 ("t26nothing", "Nothing is intentional, until it is", 2026, "hax:video", None, ["bryan"], ["ubiquity", "haxcms", "themes", "wins"],
  {"recording": "https://www.youtube.com/watch?v=wkdW2EjkwZ4"}, "Ten years of HAX through ubiquity, the outline designer and SIIP; why every site since 2020 still works.", L("PRAW talks", TALKS)),
 ("t26siip", "SIIP: a Conversation with HAX", 2026, "hax:video", "apereo", ["bryan", "billrose", "jfrank", "fusco", "winston", "jimmykane", "ashley", "alyssa"], ["haxlab", "cli", "skeletons", "textbook", "wins"],
  {"recording": "https://www.youtube.com/watch?v=TNF0uzYi9Kk"}, "The pipeline, told by the students and faculty in it, with live demos of skeletons, Pressbooks import and Canvas AI analysis.", L("PRAW talks", TALKS)),
 ("t26tools", "With the right tools, you can do anything", 2026, "hax:video", None, ["bryan"], ["family", "elmsln", "editor", "haxlab", "efficient", "wins"],
  {"recording": "https://www.youtube.com/watch?v=G5yEgFIxzl0"}, "The talk Bryan ends his courses with: his career as one storyline, the retirement of the EdTechJoker persona, and the family saying in its title. Automation begets automation, from a 2015 bash-script keynote to AI in 2026.", L("PRAW talks", TALKS)),
 ("tmanymes", "The Many Mes", None, "image:slideshow", None, ["bryan"], ["praw", "agents"],
  {"notes": "https://btopro.com/hax/the-many-me-s"}, "A workshop for instructional and learning design staff: build a digital \"you\" from context, skills, inputs, rules and outputs. PRAW is the worked example.", L("PRAW talks", TALKS)),
 ("tperf", "THE web components high performance video", None, "hax:video", None, ["bryan"], ["components", "efficient"],
  {"notes": "https://btopro.com/work/the-web-components-high-performance-video"}, "Offline-capable sites with high performance scores while shipping unbundled ES modules.", L("WINS.md: Fast without a build step", WINS)),
 ("tminute", "HAX in a minute", None, "hax:video", None, ["bryan"], ["editor", "haxcms"],
  {"recording": "https://haxtheweb.github.io/art/presentation-materials/hax-in-a-minute/"}, "HAX explained in under a minute, the short intro linked from the Apereo project page.", L("Apereo: HAX project page", "https://www.apereo.org/programs/software/HAX")),
 ("tgov4", "Drupal4Gov webinar: HAX", None, "image:slideshow", "drupal4gov", [], ["editor"],
  {"session": "https://groups.drupal.org/node/527046"}, "A Drupal4Gov webinar series session on HAX.", L("groups.drupal.org", "https://groups.drupal.org/node/527046")),
]

VEN = {
 "govcon": ("Drupal GovCon", "GOV", "slateGray", "A Drupal conference in the Washington, DC area.", {"site": "https://www.drupalgovcon.org/author/btopro"}),
 "drupalcampnj": ("DrupalCamp NJ", "NJ", "forestGreen", "A regional Drupal camp in New Jersey.", {"site": NJ23}),
 "fossy": ("FOSSY", "FOSSY", "landgrantBrown", "Free and Open Source Software Yearly, run by Software Freedom Conservancy.", {}),
 "hitech": ("HiTech Podcast", "HT", "original87Pink", "A podcast hosted by instructional designers Josh Schwartz and Will Illingworth.", {"site": "https://www.youtube.com/watch?v=fKeSEZm3khE"}),
 "drupal4gov": ("Drupal4Gov", "D4G", "skyBlue", "A webinar series for Drupal in government.", {"site": "https://groups.drupal.org/node/527046"}),
}
NEWPEOPLE = {
 "zane": ("Zane Sensenig", "ZS", "Co-presented at DrupalCamp NJ 2023.", None),
}

topics = sorted({t for row in T for t in row[6]} - {p for row in T for p in row[5]})  # a person a talk covers is already drawn as a person
people = sorted({p for row in T for p in row[5]} - set(NEWPEOPLE)) + list(NEWPEOPLE)
portal_venues = ["drupalcon", "apereo"]

lines = ["%% HAX presentations sub-web: plain Mermaid flowchart plus %%@ annotations.",
         "%% Nodes that share an id with the ecosystem web (hax-ecosystem.mmd) are portals: they take their icon,",
         "%% color and details from there and link back to it. Details live in hax-presentations.json.",
         "flowchart TB",
         "  %%@ layout rings=0,380,650,890 sizes=92,46,50,42",
         '  subgraph hub ["Presentations"]', '    presentations["Presentations"]', "  end",
         '  subgraph talks ["Talks"]']
for row in T:
    lines.append(f'    {row[0]}>"{row[1]}"]')
lines += ["  end", '  subgraph topics ["What they covered"]']
for t in topics: lines.append(f'    {t}["{t}"]')
lines += ["  end", '  subgraph speakers ["Speakers"]']
for p in people:
    lines.append(f'    {p}(("{NEWPEOPLE[p][0] if p in NEWPEOPLE else p}"))')
lines += ["  end", '  subgraph venues ["Venues"]']
for v in portal_venues: lines.append(f'    {v}[["{v}"]]')
for v, (name, *_r) in VEN.items(): lines.append(f'    {v}[["{name}"]]')
lines += ["  end", ""]
for row in T:
    tid, title, year, icon, venue, spk, tops = row[:7]
    lines.append(f"  presentations -->|includes| {tid}")
    for p in spk: lines.append(f"  {p} ---|presented| {tid}")
    for t in tops: lines.append(f"  {tid} -->|covers| {t}")
    if venue: lines.append(f"  {tid} --o|was given at| {venue}")
lines += ["",
          "  %%@ group hub tier=0", "  %%@ group talks tier=1", "  %%@ group topics tier=2", "  %%@ group speakers tier=3", "  %%@ group venues tier=3",
          "  %%@ node presentations portal"]
for row in T:
    lines.append(f"  %%@ node {row[0]} icon={row[3]} color={ERA(row[2])} motion=lift")
for t in topics: lines.append(f"  %%@ node {t} portal")
for p in people:
    if p in NEWPEOPLE: lines.append(f"  %%@ node {p} mono={NEWPEOPLE[p][1]} color=keystoneYellow motion=pop")
    else: lines.append(f"  %%@ node {p} portal")
for v in portal_venues: lines.append(f"  %%@ node {v} portal")
for v, (name, mono, color, *_r) in VEN.items(): lines.append(f"  %%@ node {v} mono={mono} color={color} motion=lift")
open("hax-presentations.mmd", "w").write("\n".join(lines) + "\n")

nodes = {}
for row in T:
    tid, title, year, icon, venue, spk, tops, links, desc, src = row
    d = {"desc": desc, "links": links, "source": src, "kind": "talk"}
    if year: d.update(year=year, yearNote=title)
    if not spk: d["note"] = "No speaker recorded yet."
    nodes[tid] = d
for v, (name, mono, color, desc, links) in VEN.items():
    nodes[v] = {"desc": desc, "links": links}
for p, (name, mono, desc, note) in NEWPEOPLE.items():
    nodes[p] = {"desc": desc, "role": "community", **({"note": note} if note else {})}
nodes["presentations"] = {"always": True}

dated = sorted([r for r in T if r[2]], key=lambda r: r[2])
def S(c, *ids): return {"caption": c, "nodes": list(ids)}
tours = [{"id": "story", "label": "The story in talks", "message": "Ten years of HAX told through the talks that introduced it, from the ELMS:LN core team at DrupalCon to the SIIP conversation at Apereo.", "scenes": [
  S("Every talk hangs off one hub.", "presentations"),
  S("2017: the ELMS:LN core team shows HAX for the first time at DrupalCon Baltimore.", "t17balt", "bryan", "mikepotter", "drupalcon", "elmsln", "editor", "wcstandard", "components"),
  S("2018: Nashville and Drupal GovCon take HAX beyond Drupal.", "t18nash", "nikkimk", "t18gov", "govcon"),
  S("2019: HAXcms is announced in Seattle; Apereo and GovCon follow.", "t19seattle", "haxcms", "t19gov", "design", "t19apereo", "apereo"),
  S("2023: the course ontology, the Horizon Report and DrupalCamp NJ.", "t23ontology", "billrose", "course", "t23horizon", "jos", "hax11ty", "libraries", "themes", "t23njcamp", "zane", "drupalcampnj"),
  S("2024: the origin story on a podcast, and the revolution at FOSSY.", "t24hitech", "hitech", "keithbailey", "t24fossy", "fossy", "open"),
  S("2025: the State of HAX Community names the seven pillars; FOSSY gets ten years in one talk.", "t25state", "haxlab", "ddd", "agents", "accessible", "efficient", "extensible", "agnostic", "remixable", "sustainable", "t25fossy", "cli", "security"),
  S("Late 2025: Apereo's board chair asks how the class, the club and the lab fit together.", "t25wilson", "ist256", "grants", "portfolio"),
  S("2026: Nothing is intentional, until it is; then SIIP at Apereo with the students and faculty themselves.", "t26nothing", "ubiquity", "wins", "t26siip", "jfrank", "fusco", "winston", "jimmykane", "ashley", "alyssa", "skeletons", "textbook"),
  S("And the talk that ends every course: with the right tools, you can do anything.", "t26tools", "family", "efficient"),
  S("Still to date: workshops and videos that need a year.", "tmanymes", "praw", "tperf", "tminute", "tgov4", "drupal4gov"),
  S("Every talk points back into the ecosystem web."),
]}]
meta = {"name": "HAX presentations", "parent": "main", "timelineTier": 1,
        "about": "Talks, podcasts and webinars about HAX. Portals (shared ids) link back to hax-ecosystem.json for details.",
        "links": {"playlist": PLAYLIST, "notes": TALKS}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-presentations.json", "w"), indent=1, ensure_ascii=False)
print(len(T), "talks;", len(topics), "topics;", len(people), "speakers")
