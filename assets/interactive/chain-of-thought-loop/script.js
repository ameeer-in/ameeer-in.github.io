const context=document.querySelector('[data-context]');
const compute=document.querySelector('[data-compute]');
const token=document.querySelector('[data-token]');
const probability=document.querySelector('[data-probability]');
const caption=document.querySelector('[data-caption]');
const returnPath=document.querySelector('[data-return]');
const panels=[...document.querySelectorAll('[data-panel]')];
const prev=document.querySelector('[data-prev]');
const next=document.querySelector('[data-next]');
const watch=document.querySelector('[data-watch]');
const prompt='A box holds 24 pencils.\nHow many are in 17 boxes?';

const steps=[
  {panel:'context',ctx:prompt,compute:'waiting for context',token:'?',prob:'probabilities appear here',caption:'The prompt is tokenized and placed in the model\'s current context.'},
  {panel:'transformer',ctx:prompt,compute:'attention + neural layers',token:'?',prob:'computing the next-token distribution',caption:'The transformer processes relationships between 24, pencils, 17, and boxes. This computation lives in numerical activations.'},
  {panel:'prediction',ctx:prompt,compute:'first pass complete',token:'10 boxes → 240',prob:'selected from possible next tokens',caption:'Instead of jumping to the answer, the reasoning-trained model generates a useful intermediate step.'},
  {panel:'context',returning:true,ctx:prompt+'\n\n10 boxes contain 240 pencils.',compute:'context has grown',token:'240',prob:'now available to later tokens',caption:'The generated step is appended to the context. The model can now attend to 240 during the next pass.'},
  {panel:'prediction',ctx:prompt+'\n\n10 boxes contain 240 pencils.\n7 boxes contain 168 pencils.',compute:'another transformer pass',token:'7 boxes → 168',prob:'another intermediate result',caption:'The loop runs again and writes down 168. The scratchpad is carrying state across generation steps.'},
  {panel:'context',returning:true,ctx:prompt+'\n\n10 boxes contain 240 pencils.\n7 boxes contain 168 pencils.\n240 + 168 = 408.',compute:'intermediate values combined',token:'408',prob:'highest useful continuation',caption:'With both partial results in context, the model generates the final calculation.'},
  {panel:'prediction',done:true,ctx:prompt+'\n\n10 boxes contain 240 pencils.\n7 boxes contain 168 pencils.\n240 + 168 = 408.',compute:'reasoning tokens remain context',token:'408 pencils',prob:'final answer',caption:'The answer is returned. The written steps helped the computation, but they are not a complete view of everything that happened inside the transformer.'}
];

let index=0;
let playing=false;
function notifyHeight(){
  parent.postMessage({type:'interactive-resize',height:document.documentElement.scrollHeight},location.origin);
}
function render(){
  const step=steps[index];
  context.textContent=step.ctx;
  compute.textContent=step.compute;
  token.textContent=step.token;
  probability.textContent=step.prob;
  caption.textContent=step.caption;
  panels.forEach(panel=>{panel.classList.toggle('active',panel.dataset.panel===step.panel);panel.classList.toggle('done',step.done&&panel.dataset.panel==='prediction')});
  returnPath.classList.toggle('active',Boolean(step.returning));
  prev.disabled=index===0||playing;
  next.disabled=index===steps.length-1||playing;
  watch.disabled=playing;
  requestAnimationFrame(notifyHeight);
}
prev.addEventListener('click',()=>{index=Math.max(0,index-1);render()});
next.addEventListener('click',()=>{index=Math.min(steps.length-1,index+1);render()});
watch.addEventListener('click',async()=>{playing=true;index=0;render();for(let i=1;i<steps.length;i++){await new Promise(resolve=>setTimeout(resolve,1300));index=i;render()}playing=false;render()});
window.addEventListener('message',event=>{
  if(event.origin!==location.origin||event.data?.type!=='interactive-theme')return;
  document.documentElement.dataset.theme=event.data.theme;
  notifyHeight();
});
new ResizeObserver(notifyHeight).observe(document.body);
render();
