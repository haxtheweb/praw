const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();let pe=0;p.on('pageerror',e=>{pe++;console.log('PAGEERR',e.message)});
await p.goto('file://'+require('path').resolve(process.argv[2]||'hax-area-icons.html'));await p.waitForTimeout(800);
const r=await p.evaluate(()=>{const o={};Object.keys(WEBS).forEach(w=>{let m;if(w==='main'){m=modelOf(w)}else{m=parse(WEBS[w].mmd);attach(m,jsonOf(w),m.errors,BASE)}m.nodes.forEach(n=>{if(n.icon&&!ICONS[n.icon])m.errors.push(`icon "${n.icon}" on "${n.id}" is not in the inlined icon set`)});o[w]=m.errors});return o});
let n=0;for(const [w,e] of Object.entries(r)){if(e.length){n+=e.length;console.log('##',w);e.forEach(x=>console.log('  ',x))}}console.log('total errors',n,'webs',Object.keys(r).length);await b.close();
// a failing exit code, so CI can block on it: any parse, portal, tour or icon error, a page error, or no webs read
if(n||pe||!Object.keys(r).length)process.exit(1)})();
