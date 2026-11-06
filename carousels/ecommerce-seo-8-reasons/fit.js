// Full-width headings at an even size: each .fit line is scaled to the content
// width, capped at MAX so short headings don't balloon; any remaining space is
// closed with letter-spacing. Other lines in the same heading take the same size.
const MAX=110;
document.fonts.ready.then(()=>{
 document.querySelectorAll('.h').forEach(h=>{
  const el=h.querySelector('.fit');if(!el)return;
  const W=h.clientWidth;
  h.style.fontSize='100px';el.style.letterSpacing='0px';
  const size=Math.min(100*W/el.getBoundingClientRect().width,MAX);
  h.style.fontSize=size+'px';
  const n=[...el.textContent].length;
  const gap=W-el.getBoundingClientRect().width;
  if(gap>1)el.style.letterSpacing=(gap/(n-1))+'px';
 });
});
