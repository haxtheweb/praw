const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();let bad=0;
for(const [w,scheme,rm] of [[1400,'light','no-preference'],[360,'light','reduce']]){const p=await b.newPage({viewport:{width:w,height:900},colorScheme:scheme,reducedMotion:rm});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file://'+require('path').resolve(process.argv[2]||'hax-area-icons.html'));await p.waitForTimeout(600);
 const ov=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
 const auth=await p.$('#aAuthor'),gaps=await p.$('#bGaps');
 const webs=[];for(const h of ['languages','release','community','psu','haxlab','haxschema','jos','appstore','merlin','oerschema','flows','history','importers','tutorials','openapi','mcptools','xapi','cli','quality','stack','contracts','anatomy','haxcms','skeletons','themes','skills','elements','sites','ist256','presentations']){await p.evaluate(h=>location.hash=h,h);await p.waitForTimeout(300);webs.push(h+':'+await p.$$eval('#nodes .node',x=>x.length))}
 await p.evaluate(()=>location.hash='');await p.waitForTimeout(300);
 const ov2=await p.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
 console.log(w,'overflow',ov,ov2,'author/gaps present:',!!auth,!!gaps,webs.join(' '),'errs',errs);
 // a failing exit code, so CI can block on it: the page is wider than the screen, a web drew no tiles, or the page threw
 const empty=webs.filter(x=>x.endsWith(':0'));if(ov>0||ov2>0||empty.length||errs.length){bad++;console.log('FAILED at',w+'px:',ov>0||ov2>0?'overflow':'',empty.length?'no tiles in '+empty.join(' '):'',errs.length?'page errors':'')}
 await p.close()}
await b.close();if(bad)process.exit(1)})();
