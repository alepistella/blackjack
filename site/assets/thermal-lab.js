/* Shared responsive thermal playground. No remote assets or dependencies. */
document.querySelectorAll('[data-thermal-lab]').forEach(lab => {
  'use strict';
  const input = key => lab.querySelector(`[data-input="${key}"]`);
  const out = (key,value) => { lab.querySelector(`[data-out="${key}"]`).textContent=value; };
  const svg=lab.querySelector('svg'), ns='http://www.w3.org/2000/svg';
  let announce;
  function draw(){
    const state={ambient:+input('ambient').value,watts:+input('watts').value,fan:input('fan').checked,sun:input('sun').checked,grille:lab.querySelector('input[type="radio"]:checked').value};
    const r=BlackjackThermal.solve(state);
    out('ambient',`${state.ambient} °C`);out('watts',`${state.watts} W`);
    lab.querySelector('[data-out="temperature"]').replaceChildren(document.createTextNode(r.temperature.toFixed(1)+' '),Object.assign(document.createElement('small'),{textContent:'°C'}));
    out('rise',`+${r.rise.toFixed(1)} °C`);out('airflow',`${r.airflow.toFixed(2)} m³/h`);out('margin',`${r.margin<0?'−':'+'}${Math.abs(r.margin).toFixed(1)} °C`);
    out('condition',`${state.fan?'FAN':'PASSIVE'} + ${state.grille.toUpperCase()} / ${state.sun?'SUN':'SHADE'}`);
    lab.dataset.over=String(r.margin<0); lab.dataset.zone=r.temperature>60?'outside':r.temperature>=50?'caution':'normal';
    out('verdict',`${r.temperature>60?'Outside Arduino’s published ambient range. Operation is not qualified here; shutdown is not predicted.':r.temperature>=50?'Low thermal margin: within the ambient rating, less than 10 °C below its upper limit.':'Within the published ambient range, with more than 10 °C to its upper limit.'}${!state.fan&&state.grille==='slots'?' Exploratory passive-slots case.':''}`);
    const w=Math.max(240,svg.getBoundingClientRect().width),h=svg.getBoundingClientRect().height;
    svg.setAttribute('viewBox',`0 0 ${w} ${h}`);svg.replaceChildren();
    const left=42,right=w-15,top=24,bottom=h-38;
    const ymin=Math.floor(Math.min(-10+r.rise,0)/20)*20,ymax=Math.ceil(Math.max(70,50+r.rise)/20)*20;
    const x=a=>left+(a+10)/60*(right-left),y=t=>bottom-(t-ymin)/(ymax-ymin)*(bottom-top);
    function el(tag,attrs,text){const n=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));if(text!==undefined)n.textContent=text;svg.append(n);return n;}
    el('title',{},`Estimated bay air ${r.temperature.toFixed(1)} degrees Celsius, outside ${state.ambient}, heat ${state.watts} watts.`);
    [[-10,50,'normal'],[50,60,'caution'],[60,ymax,'outside']].forEach(([a,b,zone])=>{const upper=Math.min(b,ymax),lower=Math.max(a,ymin);if(upper>lower)el('rect',{x:left,y:y(upper),width:right-left,height:y(lower)-y(upper),class:`tl-band-${zone}`});});
    for(let i=0;i<=4;i++){const t=ymin+i*(ymax-ymin)/4;el('line',{x1:left,x2:right,y1:y(t),y2:y(t),class:'tl-grid'});el('text',{x:left-7,y:y(t)+4,'text-anchor':'end'},Math.round(t));}
    [-10,10,30,50].forEach(a=>el('text',{x:x(a),y:bottom+19,'text-anchor':'middle'},a));
    el('text',{x:left,y:12},'BAY AIR / °C');el('text',{x:right,y:h-3,'text-anchor':'end'},'OUTSIDE AIR / °C');
    el('line',{x1:left,x2:right,y1:y(50),y2:y(50),class:'tl-caution-line'});
    el('line',{x1:left,x2:right,y1:y(60),y2:y(60),class:'tl-reference'});el('text',{x:right-2,y:y(60)-6,'text-anchor':'end'},'60 °C reference');
    [[-Infinity,50,'normal'],[50,60,'caution'],[60,Infinity,'outside']].forEach(([a,b,zone])=>{const lo=Math.max(-10,a-r.rise),hi=Math.min(50,b-r.rise);if(hi>lo)el('path',{d:`M ${x(lo)} ${y(lo+r.rise)} L ${x(hi)} ${y(hi+r.rise)}`,class:`tl-curve tl-curve-${zone}`});});
    el('line',{x1:x(state.ambient),x2:x(state.ambient),y1:top,y2:bottom,class:'tl-guide'});
    el('line',{x1:left,x2:right,y1:y(r.temperature),y2:y(r.temperature),class:'tl-guide'});
    el('circle',{cx:x(state.ambient),cy:y(r.temperature),r:14,class:'tl-halo'});el('circle',{cx:x(state.ambient),cy:y(r.temperature),r:6,class:'tl-point'});
    clearTimeout(announce);announce=setTimeout(()=>{lab.querySelector('[role="status"]').textContent=`Estimated bay air ${r.temperature.toFixed(1)} degrees Celsius.`;},350);
  }
  lab.hidden=false;
  lab.addEventListener('input',draw);
  lab.querySelector('.tl-reset').addEventListener('click',()=>{input('ambient').value=25;input('watts').value=15;input('fan').checked=true;input('sun').checked=false;lab.querySelector('[value="slots"]').checked=true;draw();});
  new ResizeObserver(draw).observe(svg);draw();
});
