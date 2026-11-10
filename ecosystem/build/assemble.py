import re
import sys,json
src,out=sys.argv[1],sys.argv[2]
s=open(src).read()
webs=[("main","hax-ecosystem"),("presentations","hax-presentations"),("elements","hax-elements"),("ist256","hax-ist256"),("sites","hax-sites"),("themes","hax-themes"),("skills","hax-skills"),("haxcms","hax-haxcms"),("skeletons","hax-skeletons"),("stack","hax-stack"),("contracts","hax-contracts"),("anatomy","hax-anatomy"),("openapi","hax-openapi"),("mcptools","hax-mcptools"),("xapi","hax-xapi"),("cli","hax-cli"),("quality","hax-quality"),("importers","hax-importers"),("tutorials","hax-tutorials"),("history","hax-history"),("flows","hax-flows"),("haxschema","hax-haxschema"),("jos","hax-jos"),("appstore","hax-appstore"),("merlin","hax-merlin"),("oerschema","hax-oerschema"),("languages","hax-languages"),("release","hax-release"),("community","hax-community"),("psu","hax-psu"),("haxlab","hax-haxlab"),("heosat","hax-heosat"),("idskills","hax-idskills")]
parts=[]
ANS=json.load(open("gap-answers.json"))
for w,f in webs:
    m=open(f+".mmd").read(); D=json.load(open(f+".json"))
    drawn=set(re.findall(r"^\s+(\w+)[\[\(\{>]",m,re.M))
    for nid,v in ANS.get(w,{}).items():
        if nid not in drawn: continue  # answers for a part this web no longer draws
        D["nodes"].setdefault(nid,{}).update({k:x for k,x in v.items() if k not in ("confirmed","skip")})
    if w=="main": D.setdefault("images",{}).update(json.load(open("images-main.json")))
    j=json.dumps(D,ensure_ascii=False,separators=(",",":"))
    assert "</script" not in m.lower()
    j=j.replace("</","<\\/")
    parts.append(f'<script type="text/plain" data-web="{w}" data-part="mmd">{m}</script>\n<script type="application/json" data-web="{w}" data-part="json">{j}</script>')
s=s.replace("__WEBS__","\n".join(parts)).replace("__ICONS__",open("icons_inline.json").read()).replace("__LAYERS__",open("ext/layers.json").read()).replace("__TRAVELER__",open("traveler.uri").read().strip())
open(out,"w").write(s); print(len(s))
