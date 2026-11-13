// Exports platform cover sizes:
//   linkedin-cover-1584x396.png  (from banner.html, LinkedIn's 4:1 size)
//   facebook-cover-1640x624.png  (from banner-facebook.html, Facebook's 2x cover size)
const {chromium}=require('playwright'),path=require('path'),{execFileSync}=require('child_process');
(async()=>{const b=await chromium.launch();const d=__dirname;
 let p=await b.newPage({viewport:{width:2000,height:504},deviceScaleFactor:2});
 await p.goto('file://'+path.join(d,'banner.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
 await p.screenshot({path:path.join(d,'_li.png')});
 p=await b.newPage({viewport:{width:1640,height:624},deviceScaleFactor:1});
 await p.goto('file://'+path.join(d,'banner-facebook.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
 await p.screenshot({path:path.join(d,'facebook-cover-1640x624.png')});await b.close();
 // 4000x1008 -> 1584x399, then trim to exactly 1584x396
 execFileSync('python3',['-c',`from PIL import Image
im=Image.open('${path.join(d,'_li.png')}').resize((1584,399),Image.LANCZOS)
im.crop((0,1,1584,397)).save('${path.join(d,'linkedin-cover-1584x396.png')}')`]);
 require('fs').unlinkSync(path.join(d,'_li.png'));})();
