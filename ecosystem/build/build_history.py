"""History sub-web: how the ecosystem got here, from the Drupal years at Penn State to HAX, with a line from each early experiment to the piece of HAX it became.
Sources: Bryan Ollendyke's 2015 thesis "Information Altruism" (in PRAW; Penn State is CentralU, ELMS is YourNetwork, Bryan is Technologist Zero there), PRAW's WORLDVIEW.md, WINS.md and talks/README.md, and the years confirmed in this web.
Portals: ids from hax-ecosystem.mmd. Details in hax-history.json."""
import json
GH = "https://github.com/haxtheweb"
PRAW = GH + "/praw/blob/main/"
THESIS = PRAW + "thesis-bryan-ollendyke-information-altruism.pdf"
def L(a, b): return {"label": a, "url": b}
def S(c, *i): return {"caption": c, "nodes": list(i)}
ERAS = [("e_drupal", "The Drupal years", "2005 to 2012: a weekend Drupal course, a community of practice, and a learning platform built in the open at Penn State."),
        ("e_elmsln", "ELMS:LN", "2012 to 2016: the e-Learning Management System becomes a network of small Drupal apps; the thesis names what made it spread."),
        ("e_turn", "The turn to web components", "2015 to 2019: a note card, a friend pointing at a standard, three weeks off to rewrite a career, and a standard that settled in 2019."),
        ("e_hax", "HAX and HAXcms", "2017 on: the editor, then HAXcms on PHP, Node.js, the CLI and the MCP."),
        ("e_teach", "Teaching", "2019 on: IST 256 every semester, where class projects become HAX components.")]
# id, label, era, year, yearLabel, desc, became (portal ids), source
EVENTS = [
 ("h_hired", "Keith hires Bryan", "e_drupal", 2007, "2007", "Keith Bailey, the director who wrote pagination JavaScript himself, hires Bryan into online learning in the College of Arts and Architecture. Bryan begins contributing open source code the same year.", ["keithbailey", "aa"], PRAW + "WORLDVIEW.md"),
 ("h_elms", "ELMS is conceived", "e_drupal", 2007, "2007", "The e-Learning Management System, YourNetwork in the thesis, is conceived inside Transformational Learning Services in the College of Arts and Architecture: a learning platform built by the people who teach with it. The thesis's record of it starts July 18, 2007.", ["elmsln", "aa"], THESIS),
 ("h_weekend", "The weekend Drupal course", "e_drupal", 2008, "about 2008", "Bryan's weekend Drupal course, the start of a Drupal community at Penn State that grew to more than 50 developers and 1,000 sites by 2015.", ["psu"], PRAW + "talks/README.md"),
 ("h_altruism", "Donating effort", "e_drupal", 2009, "2007 to 2010", "Building and sharing Drupal work with other units freely, so each could grow its own capacity. Units that received it went on to hire and build; the pattern the thesis later names information altruism.", ["open", "sustainable"], THESIS),
 ("h_interviews", "The diffusion study", "e_drupal", 2010, "March to June 2010", "Interviews across the units that adopted ELMS: what made it approachable, the pull of a community, independence and empowerment, and the 'many hats' small teams wear.", ["wins"], THESIS),
 ("h_modules", "Hundreds of Drupal modules", "e_drupal", 2011, "the Drupal years", "A Drupal core maintainer with hundreds of contributed modules. The plugin lessons from those years are why HAX waited so long on a plugin architecture.", ["plugins", "extensible"], PRAW + "WORLDVIEW.md"),
 ("h_elmsln", "ELMS becomes ELMS:LN", "e_elmsln", 2012, "2012", "ELMS is rebuilt as the ELMS Learning Network: many small Drupal distributions (courses, studio, blog, interact, discussion) wired together, deployed with Drush recipes.", ["elmsln", "billrose"], GH + "/../elmsln/elmsln"),
 ("h_whitepaper", "ELMSLN white paper", "e_elmsln", 2014, "August 2014", "'ELMSLN: A Disruptive Learning Technology.' ELMS for Drupal 6 had passed 780,000 downloads on 12,000 Drupal systems; ELMS:LN is in use at Penn State and UW-Madison.", ["elmsln", "agnostic"], "https://oer.hax.psu.edu/bto108/sites/haxcellence/files/ELMSLN-whitepaper-08-28-2014.pdf"),
 ("h_thesis", "Information Altruism", "e_elmsln", 2015, "December 2015", "Bryan's M.S. thesis in IST, advised by Andrea Tapia: how donating effort, a community of practice and a technology built in the open let a grassroots system spread across a university. Written in first and third person as Technologist Zero.", ["wins", "praw", "ist"], THESIS),
 ("h_sustaining", "Sustaining innovation", "e_elmsln", 2015, "May 2015", "'ELMS Learning Network: An EdTech Platform for Sustaining Innovation,' with Michael Collins.", ["mcollins", "sustainable"], "https://oer.hax.psu.edu/bto108/sites/haxcellence/files/ELMSLN-sustaining-innovation-05-08-2015.pdf"),
 ("h_notecard", "A note card", "e_turn", 2015, "2015", "HAX starts as a note card, a napkin idea: an editor where you talk to the screen, in the Kinect era.", ["editor"], PRAW + "WINS.md"),
 ("h_standard", "Mike points at the standard", "e_turn", 2016, "2016", "Mike Potter points Bryan to the web component standard itself, not a component library. It is what made HAX possible.", ["mikepotter", "wcstandard"], PRAW + "WORLDVIEW.md"),
 ("h_rewrite", "Three weeks off", "e_turn", 2017, "2017", "Bryan takes three weeks off to rewrite his career on a standard that would not stabilize until 2019. HAX becomes a proof of concept; the first element ships; DrupalCon DC hears about it.", ["editor", "components", "drupalcon"], PRAW + "talks/README.md"),
 ("h_stable", "The standard settles", "e_turn", 2019, "2019", "Web components stabilize across browsers: 198 elements, the first site, 29 contributors, HAX Camp.", ["wcstandard", "haxcamp"], PRAW + "WINS.md"),
 ("h_haxcms", "HAXcms on PHP", "e_hax", 2018, "2018", "The smallest possible backend to make HAX work, writing sites to disk as JSON Outline Schema and HTML. DrupalCon Nashville.", ["haxcms", "php", "jos"], GH + "/haxcms-php"),
 ("h_2020", "Every site since still works", "e_hax", 2020, "2020", "hax.psu.edu opens on HAXiam; 582 elements and the first 11 sites. Because HAX saves HTML and ships the tag definitions separately, every site made since about 2020 still works.", ["haxpsu", "haxiam", "remixable"], PRAW + "WINS.md"),
 ("h_2023", "The classroom becomes the pipeline", "e_hax", 2023, "2023", "Bill Rose's course ontology gives HAX its instructional backbone, and student contributors from IST 256 and HAX Lab carry feature output to its highest levels from 2024 on.", ["billrose", "bryan", "haxlab"], PRAW + "WINS.md"),
 ("h_hax7", "HAX 7 and a new home", "e_hax", 2023, "June to September 2023", "HAX 7, the largest release yet: more than 346 features and fixes since HAX 6, Merlin for finding any function (by voice too), dark mode, better mobile authoring and new instructional blocks, put into production across hundreds of Penn State courses. A new hax.psu.edu followed in September, with Bill Rose writing in-interface tutorials (User Scaffolding).", ["merlin", "haxpsu", "billrose"], "https://www.apereo.org/news/2023/hax-7-release"),
 ("h_journey", "HAX 11 and Journey", "e_hax", 2025, "June 2025", "HAX 11 ships the Journey design; a demo site took about five minutes from concept to published with the HAX CLI, and HAX 11's developer-experience work speeds up student onboarding.", ["themes", "cli", "haxlab"], "https://www.apereo.org/news/2025/hax-project-releases-journey"),
 ("h_oars", "The OARS model course", "e_teach", 2025, "September 2025", "Bill Rose and other Penn State faculty build a course that examines the HAX community pillars through OARS: observation, analysis, reflection and synthesis.", ["billrose", "accessible", "sustainable"], "https://www.apereo.org/news/2025/hax-oars-model-course"),
 ("h_node", "Node.js, the CLI, agents", "e_hax", 2024, "2024 to 2026", "HAXcms on Node.js with the same OpenAPI contract, the CLI, PRAW and the Future Traveler, the MCP.", ["nodejs", "cli", "praw", "traveler", "mcp"], GH + "/haxcms-nodejs"),
 ("h_sixmonths", "Six months in a week", "e_elmsln", 2015, "2015", "A keynote ends with a bash script running for 25 minutes and a question: what is our job when work is automated? \"Last week I did 6 months of work.\" Automation begets automation; AI later amplifies the same process.", ["efficient", "traveler"], PRAW + "talks/README.md"),
 ("h_walkaway", "Walking away", "e_hax", 2019, "2019", "Bryan walks away from more than ten years of Drupal community to build HAX, with six events planned after HAX Camp 2019.", ["haxcamp", "editor"], PRAW + "talks/README.md"),
 ("h_crisis", "Never waste a crisis", "e_hax", 2020, "2020", "The pandemic cancels the events and delays the dream. Then \"never waste a good crisis\": the wild idea starts being adopted.", ["haxpsu", "aa"], PRAW + "talks/README.md"),
 ("h_catastrophic", "Catastrophic success", "e_hax", 2026, "2026", "Catastrophe theory's sudden shift after a long, steady build: AI does six months of work in about three days, students design accessible interfaces as web components, and people understand HAX in seconds.", ["traveler", "haxlab"], PRAW + "talks/README.md"),
 ("h_ist256", "IST 256 begins", "e_teach", 2019, "Fall 2019", "Bryan teaches IST 256 every semester from fall 2019 to spring 2026. Class projects become HAX components and students become contributors.", ["ist256", "ist", "components"], GH + "/../btopro/edtechjoker"),
]
EVENTS = [e if not e[7].startswith(GH + "/../") else (e[:7] + (e[7].replace(GH + "/../", "https://github.com/"),)) for e in EVENTS]
portals = []
for e in EVENTS:
    for p in e[6]:
        if p not in portals: portals.append(p)
lines = ["%% History sub-web: how the ecosystem got here, from the Drupal years at Penn State to HAX, with a line from each early experiment to the piece of HAX it became.",
         "%% Sources: the 2015 thesis Information Altruism (in PRAW), PRAW's WORLDVIEW.md, WINS.md and talks/README.md. Portals: ids from hax-ecosystem.mmd. Details in hax-history.json.",
         "flowchart TB", "  %%@ layout rings=0,220,470,760 sizes=92,70,60,52",
         '  subgraph hub ["Where it came from"]', '    history(("History"))', "  end", '  subgraph eras ["Eras"]']
for eid, lab, d in ERAS: lines.append(f'    {eid}["{lab}"]')
lines.append('    family["family"]')
lines += ["  end", '  subgraph events ["What happened"]']
for e in EVENTS: lines.append(f'    {e[0]}>"{e[1]}"]')
lines += ["  end", '  subgraph became ["What it became"]']
for p in portals: lines.append(f'    {p}["{p}"]')
lines += ["  end", ""]
for eid, lab, d in ERAS: lines.append(f"  history -->|has| {eid}")
for e in EVENTS:
    lines.append(f"  {e[2]} -->|includes| {e[0]}")
    for p in e[6]: lines.append(f"  {e[0]} -->|became| {p}")
lines += ["  history -->|starts with| family", "  family -->|raised| bryan", "  h_sixmonths -->|is amplified in| h_catastrophic", "  h_walkaway -->|was tested by| h_crisis",
          "  h_elms -->|grew into| h_elmsln", "  h_elmsln -->|was rebuilt as| h_haxcms", "  h_altruism -->|is the pattern in| h_thesis", "  h_notecard -->|needed| h_standard", "  h_standard -->|led to| h_rewrite", "",
          "  %%@ group hub tier=0", "  %%@ group eras tier=1", "  %%@ group events tier=2", "  %%@ group became tier=3",
          "  %%@ node history icon=icons:book color=nittanyNavy motion=pulse"]
ERACOL = {"e_drupal": "wonderPurple", "e_elmsln": "creekTeal", "e_turn": "roarGolden", "e_hax": "discoveryCoral", "e_teach": "forestGreen"}
ERAMONO = {"e_drupal": "DRPL", "e_elmsln": "ELMS", "e_turn": "WC", "e_hax": "HAX", "e_teach": "IST"}
for eid, lab, d in ERAS: lines.append(f"  %%@ node {eid} mono={ERAMONO[eid]} color={ERACOL[eid]} motion=pop")
for e in EVENTS: lines.append(f"  %%@ node {e[0]} icon=hax:documents color={ERACOL[e[2]]} motion=nudge")
for p in portals: lines.append(f"  %%@ node {p} portal")
lines.append("  %%@ node family portal")
open("hax-history.mmd", "w").write("\n".join(lines) + "\n")
nodes = {"history": {"always": True, "desc": "How the ecosystem got here. The Drupal and ELMS:LN years come from Bryan's 2015 thesis, where Penn State is CentralU, ELMS is YourNetwork and Bryan is Technologist Zero; the rest from PRAW."}}
for eid, lab, d in ERAS: nodes[eid] = {"desc": d, "kind": "era", "always": True}
for e in EVENTS: nodes[e[0]] = {"desc": e[5], "kind": "event", "year": e[3], "yearLabel": e[4], "source": L("Source", e[7]), "links": {"source": e[7]}}
for p in portals: nodes[p] = {"always": True}
nodes["family"] = {"always": True}
tours = [{"id": "history", "label": "Where it came from", "message": "From a weekend Drupal course to the Future Traveler, in five eras. Over time plays it year by year.", "scenes": [
    S("It starts with family: with the right tools you can do anything.", "family", "bryan"),
    S("Five eras.", *[e for e, *_ in ERAS]),
    S("The Drupal years: Keith hires Bryan, ELMS is conceived, a weekend course seeds a community.", "h_hired", "h_elms", "h_weekend", "keithbailey", "aa"),
    S("Donating effort builds capacity everywhere it lands; the thesis calls this information altruism.", "h_altruism", "h_interviews", "h_modules", "h_thesis"),
    S("ELMS becomes ELMS:LN, a network of small apps.", "h_elmsln", "h_whitepaper", "h_sustaining", "elmsln"),
    S("A note card, a friend pointing at a standard, three weeks off.", "h_notecard", "h_standard", "h_rewrite", "h_stable", "mikepotter", "wcstandard"),
    S("Walking away to build HAX, then a crisis that became adoption.", "h_walkaway", "h_crisis"),
    S("HAXcms, then every site since 2020 still works, then HAX 7 and the classroom as pipeline, HAX 11 and Journey, then Node.js and agents.", "h_haxcms", "h_2020", "h_hax7", "h_2023", "h_journey", "h_node"),
    S("Automation begets automation: six months in a week in 2015, catastrophic success in 2026.", "h_sixmonths", "h_catastrophic"),
    S("And the classroom becomes the pipeline, then a course about the community itself.", "h_ist256", "ist256", "h_oars"),
    S("The whole story."),
]}]
meta = {"name": "History", "parent": "main", "timelineTier": 2, "sectionLabels": {"era": "eras", "event": "events"},
        "about": "How the ecosystem got here, in five eras from 2007 to 2026. The Drupal and ELMS:LN years are drawn from Bryan Ollendyke's 2015 M.S. thesis, Information Altruism (kept in PRAW), where Penn State appears as CentralU, ELMS as YourNetwork and Bryan as Technologist Zero; the HAX years from PRAW's WORLDVIEW, WINS and talks. Each event points at the piece of HAX it became.",
        "kindLabels": {"rel": "era to event; event to what it became"}}
json.dump({"meta": meta, "nodes": nodes, "evidence": {}, "tours": tours}, open("hax-history.json", "w"), indent=1, ensure_ascii=False)
print(len(ERAS), "eras;", len(EVENTS), "events;", len(portals), "portals")
