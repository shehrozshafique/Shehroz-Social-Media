// Scale every .fit line so it spans the full width of its parent.
document.fonts.ready.then(()=>{
 document.querySelectorAll('.fit').forEach(el=>{
  el.style.fontSize='100px';
  const W=el.parentElement.clientWidth,w=el.getBoundingClientRect().width;
  el.style.fontSize=(100*W/w)+'px';
 });
});
