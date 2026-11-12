// Renders banner.html (2000x504) at 2x -> 4000x1008 PNGs.
// banner.png keeps the original serif headline; banner-bebas.png uses the brand Bebas Neue headline.
const {chromium}=require('playwright'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:2000,height:504},deviceScaleFactor:2});
for(const [hash,out] of [['','banner.png'],['#bebas','banner-bebas.png']]){
 await p.goto('file://'+path.join(__dirname,'banner.html')+hash);await p.reload();await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
 await p.screenshot({path:path.join(__dirname,out)});console.log(out)}
await b.close()})();
