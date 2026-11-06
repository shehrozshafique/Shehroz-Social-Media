// Renders every slide-*.html (designed at 1080x1350) to 4K PNGs (3840x4800) in out/.
const {chromium}=require('playwright'),fs=require('fs'),path=require('path');
(async()=>{const dir=__dirname;fs.mkdirSync(path.join(dir,'out'),{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:3840/1080});
for(const f of fs.readdirSync(dir).filter(f=>/^slide-\d+.*\.html$/.test(f)).sort()){
 await p.goto('file://'+path.join(dir,f));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
 await p.screenshot({path:path.join(dir,'out',f.replace('.html','.png'))});console.log(f)}
await b.close()})();
