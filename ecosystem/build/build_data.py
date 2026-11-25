"""Publish the ecosystem webs as open datasets on hax.cloud (data/), for agents and anyone who wants to query them.

    python3 -I ecosystem/build/build_data.py <site-dir>

Run by site.sh after build_site.py, from that build's own output: ecosystem-webs.json (every web's JSON and Mermaid
source) and slugs.json (every page's path), so the data and the site can't disagree. Writes:

  data/index.json         a schema.org DataCatalog: one Dataset per web, with its page and downloads
  data/graph.json         every web in one graph: nodes keyed "<web>:<id>", edges between them
  data/webs/<web>.json    one web: its nodes (with their hax.cloud page), edges, evidence and tours
  data/webs/<web>.mmd     the web's Mermaid source, as drawn
  data/llms-section.md    the "Datasets" section site.sh appends to llms.txt

Edges come from the Mermaid source (`a -->|label| b`); style says which arrow drew them: solid (-->), dashed (-.->),
thick (==>) or line (---). Data is published under the repository's license (Apache-2.0).
"""
import json, os, re, sys

SITE = "https://hax.cloud/"
REPO = "https://github.com/haxtheweb/praw/blob/main/ecosystem/web/"
LICENSE = "https://www.apache.org/licenses/LICENSE-2.0"
ARROWS = {"-->": "solid", "-.->": "dashed", "==>": "thick", "---": "line"}
EDGE = re.compile(r"^\s*([\w-]+)\s*(-->|-\.->|==>|---)\s*(?:\|([^|]*)\|)?\s*([\w-]+)\s*$")
NODE = re.compile(r"^\s*([\w-]+)\s*(?:\(\(|\[\(|\[\[|\[|\(|\{\{|\{|>)\s*\"([^\"]*)\"")


def page(slugs, key):
    s = slugs.get(key)
    return SITE + s if s else None


def node_page(slugs, w, nid):
    """a node's page, in build_site.py's order: its tile in this web, the web it opens (a portal tile), the main
    web's tile, then the same node in any web"""
    for key in ("tile:%s:%s" % (w, nid), "web:" + nid, "tile:main:" + nid):
        if slugs.get(key):
            return SITE + slugs[key]
    for key, s in slugs.items():
        if key.startswith("tile:") and key.endswith(":" + nid):
            return SITE + s
    return None


def parse_mmd(mmd):
    """Labels, edges and the description comment of a Mermaid flowchart."""
    labels, edges, about = {}, [], ""
    for line in mmd.splitlines():
        if line.startswith("%%") and not line.startswith("%%@") and not about:
            # drop the tooling note some webs open with ("...: plain Mermaid flowchart plus %%@ annotations.")
            about = re.sub(r"[:.]?\s*plain Mermaid flowchart.*$", "", line[2:].strip())
            continue
        e = EDGE.match(line)
        if e:
            src, arrow, label, dst = e.groups()
            edge = {"from": src, "to": dst, "style": ARROWS[arrow]}
            if label and label.strip():
                edge["label"] = label.strip()
            edges.append(edge)
            continue
        n = NODE.match(line)
        if n and n.group(1) not in ("subgraph", "flowchart", "graph"):
            labels.setdefault(n.group(1), n.group(2))
    return labels, edges, about


def main(out):
    bundle = json.load(open(os.path.join(out, "ecosystem-webs.json")))
    slugs = json.load(open(os.path.join(out, "slugs.json")))
    data_dir = os.path.join(out, "data")
    os.makedirs(os.path.join(data_dir, "webs"), exist_ok=True)
    catalog = []
    graph = {"nodes": [], "edges": []}
    llms = []
    for w in bundle["order"]:
        src = bundle["webs"][w]
        d, mmd = src["json"], src["mmd"]
        meta = d.get("meta", {})
        labels, edges, about = parse_mmd(mmd)
        title = meta.get("name") or w
        web_page = page(slugs, "web:" + w)
        # every node the web draws: its JSON details where it has them; a node a sub-web borrows from the main
        # web (a person, a pillar) keeps its details there and links to that page
        details = d.get("nodes") or {}
        drawn = list(details) + [n for n in labels if n not in details]
        drawn += [n for e in edges for n in (e["from"], e["to"]) if n not in details and n not in labels]
        nodes = []
        for nid in dict.fromkeys(drawn):
            node = {"id": nid}
            if nid in labels and labels[nid] != nid:
                node["label"] = labels[nid]
            node["page"] = node_page(slugs, w, nid)
            node.update(details.get(nid, {}))
            nodes.append(node)
        file = "hax-" + ("ecosystem" if w == "main" else w)
        web = {"web": w, "title": title, "description": about, "page": web_page,
               "source": {"json": REPO + file + ".json", "mmd": REPO + file + ".mmd"},
               "license": LICENSE, "meta": meta, "nodes": nodes, "edges": edges,
               "evidence": d.get("evidence", {}), "tours": d.get("tours", [])}
        json.dump(web, open(os.path.join(data_dir, "webs", w + ".json"), "w"), indent=1, ensure_ascii=False)
        open(os.path.join(data_dir, "webs", w + ".mmd"), "w").write(mmd)
        for node in nodes:
            graph["nodes"].append({"key": "%s:%s" % (w, node["id"]), "web": w, "id": node["id"],
                                   "label": node.get("label", node["id"]), "page": node["page"],
                                   "desc": node.get("desc", "")})
        for e in edges:
            graph["edges"].append({**e, "web": w, "from": "%s:%s" % (w, e["from"]), "to": "%s:%s" % (w, e["to"])})
        url = SITE + "data/webs/" + w
        dataset = {"@type": "Dataset", "identifier": w, "name": title, "description": about or title,
                   "url": web_page or url + ".json", "license": LICENSE, "isAccessibleForFree": True,
                   "isBasedOn": web["source"]["json"],
                   "distribution": [
                       {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": url + ".json"},
                       {"@type": "DataDownload", "encodingFormat": "text/vnd.mermaid", "contentUrl": url + ".mmd"}],
                   "variableMeasured": ["%d nodes" % len(nodes), "%d edges" % len(edges)]}
        if meta.get("updated"):
            dataset["dateModified"] = meta["updated"]
        catalog.append(dataset)
        llms.append("- [%s](%s.json): %s (%d nodes, %d edges)" % (title, url, about or title, len(nodes), len(edges)))
    graph["meta"] = {"about": "Every hax.cloud web in one graph. Node keys are <web>:<id>; the same id in two webs is "
                              "the same thing drawn in two places.", "webs": len(catalog), "license": LICENSE}
    json.dump(graph, open(os.path.join(data_dir, "graph.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    index = {"@context": "https://schema.org", "@type": "DataCatalog", "@id": SITE + "data/index.json",
             "name": "hax.cloud datasets",
             "description": "The webs behind hax.cloud as open data: every part of HAX, the people and places it "
                            "connects, and the evidence for each link. Built from PRAW on every push to main.",
             "url": SITE, "license": LICENSE, "isAccessibleForFree": True,
             "publisher": {"@type": "Organization", "name": "HAXTheWeb", "url": "https://haxtheweb.org/",
                           "sameAs": ["https://github.com/haxtheweb"]},
             "isBasedOn": "https://github.com/haxtheweb/praw/tree/main/ecosystem",
             "distribution": [{"@type": "DataDownload", "name": "Whole graph", "encodingFormat": "application/json",
                               "contentUrl": SITE + "data/graph.json"}],
             "dataset": catalog}
    json.dump(index, open(os.path.join(data_dir, "index.json"), "w"), indent=1, ensure_ascii=False)
    section = ["", "## Datasets", "",
               "The webs behind hax.cloud as open JSON (Apache-2.0). Each web's nodes carry their hax.cloud page; "
               "edges come from the web's Mermaid source.", "",
               "- [Dataset catalog](%sdata/index.json): schema.org DataCatalog of every web below" % SITE,
               "- [Whole graph](%sdata/graph.json): every web's nodes and edges in one file" % SITE] + llms
    open(os.path.join(data_dir, "llms-section.md"), "w").write("\n".join(section) + "\n")
    print("data: %d webs, %d nodes, %d edges" % (len(catalog), len(graph["nodes"]), len(graph["edges"])))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
