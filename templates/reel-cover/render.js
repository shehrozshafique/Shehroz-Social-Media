// Renders a 9:16 Reel cover (designed at 1080x1920) to a 4K-wide PNG (2160x3840).
// Usage: node render.js reel-cover.html
const {chromium}=require('playwright'),path=require('path');
(async()=>{const f=path.resolve(__dirname,process.argv[2]||'reel-cover.html');
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:2});
await p.goto('file://'+f);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
await p.screenshot({path:f.replace(/\.html$/,'.png')});await b.close()})();
