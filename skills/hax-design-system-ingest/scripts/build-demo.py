"""Write a theme's demo site (site.json items + pages/) from a spec file.

usage: python3 build-demo.py elements/<system>-theme <spec.py>

Replaces demo/site.json "items" and the whole demo/pages/ folder, so keep the spec
as the source of truth (save any page you want to keep into it first). Files in
demo/files/ are left alone.

spec.py defines:
  PREFIX       short id prefix, e.g. "5a3e1d70" (items become item-<PREFIX>-<slug>)
  TITLE        optional site title
  DESCRIPTION  optional site description
  PAGES        menu-ordered list of
               (slug, title, description, parent_slug_or_None, html[, metadata])
               metadata is an optional dict merged into the item's metadata,
               e.g. {"icon": "icons:home"} for themes that show page icons.
"""
import json
import os
import runpy
import shutil
import sys


def main(theme_dir, spec_file):
    spec = runpy.run_path(spec_file)
    demo = os.path.join(theme_dir, "demo")
    site_path = os.path.join(demo, "site.json")
    site = json.load(open(site_path))
    pages = spec["PAGES"]
    prefix = spec["PREFIX"]
    parents = {p[0]: p[3] for p in pages}
    ids, order, items = {}, {}, []
    pages_dir = os.path.join(demo, "pages")
    if os.path.isdir(pages_dir):
        shutil.rmtree(pages_dir)
    for page in pages:
        slug, title, desc, parent, body = page[:5]
        extra = page[5] if len(page) > 5 else {}
        iid = f"item-{prefix}-{slug.replace('/', '-')}"
        ids[slug] = iid
        parent_id = ids[parent] if parent else None
        key = parent_id or "__root"
        order[key] = order.get(key, -1) + 1
        indent, p = 0, parent
        while p:
            indent += 1
            p = parents.get(p)
        location = f"pages/{iid}/index.html"
        os.makedirs(os.path.join(demo, "pages", iid))
        with open(os.path.join(demo, location), "w") as fh:
            fh.write(body.strip() + "\n")
        items.append(
            {
                "id": iid,
                "indent": indent,
                "location": location,
                "slug": slug,
                "order": order[key],
                "parent": parent_id,
                "title": title,
                "description": desc,
                "metadata": {
                    "created": 1736889000,
                    "updated": 1736889000,
                    "published": True,
                    "hideInMenu": False,
                    "locked": False,
                    "readtime": 1,
                    "tags": "",
                    "status": "",
                    **extra,
                },
            }
        )
    site["items"] = items
    if "TITLE" in spec:
        site["title"] = spec["TITLE"]
    if "DESCRIPTION" in spec:
        site["description"] = spec["DESCRIPTION"]
    with open(site_path, "w") as fh:
        json.dump(site, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"{len(items)} pages written to {demo}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
