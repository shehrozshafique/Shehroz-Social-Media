// Renders the 8 highlight covers (1080x1080) and a preview sheet (2000x520, at 2x).
const {chromium}=require('playwright'),path=require('path');
const NAMES=['start-here','results','websites','ai-systems','my-results','client-feedback','about-me','book-a-meeting'];
(async()=>{const b=await chromium.launch();const url='file://'+path.join(__dirname,'covers.html');
 let p=await b.newPage({viewport:{width:1080,height:1080}});
 for(let i=0;i<NAMES.length;i++){await p.goto(url+'#'+i);await p.reload();await p.evaluate(()=>document.fonts.ready);
  await p.screenshot({path:path.join(__dirname,`${String(i+1).padStart(2,'0')}-${NAMES[i]}.png`)});}
 p=await b.newPage({viewport:{width:2000,height:520},deviceScaleFactor:2});
 await p.goto(url+'#sheet');await p.reload();await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
 await p.screenshot({path:path.join(__dirname,'preview.png')});await b.close()})();
