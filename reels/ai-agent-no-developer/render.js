// Usage: node render.js preview 1.5 6 ...   -> build/preview-<t>.png
//        node render.js video                -> build/video.mp4 (30fps, silent; mix.sh adds audio)
const {chromium}=require('playwright');const {spawn}=require('child_process');const path=require('path');
const FPS=30,DUR=33;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.resolve(__dirname,'reel.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const [mode,...ts]=process.argv.slice(2);
if(mode==='preview'){for(const t of ts){await p.evaluate(t=>render(+t),t);await p.screenshot({path:`${__dirname}/build/preview-${t}.png`})}}
else{const ff=spawn('ffmpeg',['-y','-f','image2pipe','-framerate',FPS,'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p','-r',FPS,`${__dirname}/build/video.mp4`],{stdio:['pipe','ignore','inherit']});
for(let f=0;f<FPS*DUR;f++){await p.evaluate(t=>render(t),f/FPS);const buf=await p.screenshot({type:'jpeg',quality:96});
if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(f%90===0)console.log('frame',f)}
ff.stdin.end();await new Promise(r=>ff.on('close',r))}
await b.close()})();
