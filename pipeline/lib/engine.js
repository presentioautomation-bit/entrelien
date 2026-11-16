// Entrelien — moteur commun des films de carnets (style « carnet à l'encre », bible de production).
// Un épisode = film.html qui charge ce fichier, timing.js (window.TIMING), puis déclare ses plans avec sc().
(function(){
const LIB='file:///home/claude/prod/lib/node_modules/@fontsource/';
const css=`
@font-face{font-family:"Fraunces";src:url(${LIB}fraunces/files/fraunces-latin-400-normal.woff2) format("woff2");font-weight:400}
@font-face{font-family:"Fraunces";src:url(${LIB}fraunces/files/fraunces-latin-500-normal.woff2) format("woff2");font-weight:500}
@font-face{font-family:"Work Sans";src:url(${LIB}work-sans/files/work-sans-latin-400-normal.woff2) format("woff2");font-weight:400}
@font-face{font-family:"Work Sans";src:url(${LIB}work-sans/files/work-sans-latin-500-normal.woff2) format("woff2");font-weight:500}
@font-face{font-family:"Caveat";src:url(${LIB}caveat/files/caveat-latin-600-normal.woff2) format("woff2");font-weight:600}
html,body{margin:0;background:#000;overflow:hidden}
#stage{position:relative;width:1920px;height:1080px;overflow:hidden;
  --ground:#F3EEE4;--main:#1E2A44;--second:#4A4D55;--accent:#C9922E;--sage:#6E9583;
  --wash:color-mix(in srgb,var(--main) 10%,var(--ground));--wash2:color-mix(in srgb,var(--main) 22%,var(--ground));
  --rule:color-mix(in srgb,var(--second) 16%,var(--ground));--margin:color-mix(in srgb,var(--accent) 45%,var(--ground));
  --paper2:color-mix(in srgb,var(--second) 6%,var(--ground));--night:#1E2A44;--nightlift:color-mix(in srgb,var(--main) 82%,var(--ground));
  --shade:color-mix(in srgb,var(--main) 18%,transparent);color:var(--second);font-family:"Work Sans",system-ui,sans-serif}
.scene{position:absolute;inset:0;visibility:hidden}
.ground{position:absolute;inset:0;background:var(--ground)}
.art{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.ink{fill:none;stroke:var(--main);stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
.ink-thin{fill:none;stroke:var(--main);stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.pencil{fill:none;stroke:var(--second);stroke-width:2.5;stroke-linecap:round;opacity:.55}
.sage-ink{fill:none;stroke:var(--sage);stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.ochre-ink{fill:none;stroke:var(--accent);stroke-width:6;stroke-linecap:round;stroke-linejoin:round}
.pool{position:absolute;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.55),transparent);mix-blend-mode:soft-light}
.edge{position:absolute;inset:0;background:radial-gradient(100% 90% at 50% 45%,transparent 55%,color-mix(in srgb,var(--main) 22%,transparent))}
.night{position:absolute;inset:0;background:radial-gradient(80% 90% at 50% 40%,var(--nightlift),var(--night))}
.words{position:absolute;margin:0;display:flex;flex-direction:column;gap:22px}.words>*{margin:0}
.line{font-family:"Fraunces",Georgia,serif;font-size:80px;line-height:1.1;font-weight:400;color:var(--main)}
.sub{font-size:42px;line-height:1.35}
.hand{font-family:"Caveat",cursive;font-weight:600;font-size:56px;color:var(--main)}
.on-night,.on-night .line,.on-night .hand{color:var(--ground)}
.on-night .sub{color:color-mix(in srgb,var(--ground) 80%,var(--main))}
.mark{color:var(--accent)}.sage{color:var(--sage)}
.w{display:inline-block;white-space:pre}
.night-art .ink,.night-art .ink-thin{stroke:var(--ground)}.night-art .pencil{stroke:var(--ground);opacity:.35}
.subs{position:absolute;left:50%;bottom:34px;transform:translateX(-50%);max-width:1320px;text-align:center;font-family:"Work Sans",sans-serif;font-weight:500;font-size:34px;line-height:1.3;padding:10px 26px;border-radius:6px;color:var(--main);background:color-mix(in srgb,var(--ground) 88%,transparent);box-shadow:0 2px 14px rgba(0,0,0,.08);opacity:0}
.subs.dark{color:var(--ground);background:color-mix(in srgb,var(--night) 80%,transparent)}
.cam{position:absolute;inset:0}
.lab{position:absolute;margin:0;font-family:"Work Sans",sans-serif;font-size:26px;color:var(--second)}
.note{position:absolute;margin:0;font-family:"Caveat",cursive;font-weight:600;font-size:48px;line-height:1.1;color:var(--second)}
`;
const st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

// ---------- outils ----------
const clamp01=x=>Math.max(0,Math.min(1,x)), seg=(t,a,b)=>clamp01((t-a)/(b-a)), lerp=(a,b,p)=>a+(b-a)*p;
const eo=x=>1-Math.pow(1-x,3), eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;
Object.assign(window,{clamp01,seg,lerp,eo,eio});
window.split=function(el){const words=el.textContent.split(' ');el.textContent='';return words.map((w,i)=>{const s=document.createElement('span');s.className='w';s.textContent=w+(i<words.length-1?' ':'');el.appendChild(s);return s})};
window.wordsIn=function(spans,t,t0,st=.11){spans.forEach((s,i)=>{const p=eo(seg(t,t0+i*st,t0+i*st+.5));s.style.opacity=p;s.style.transform='translateX('+lerp(28,0,p).toFixed(1)+'px)'})};
window.fade=function(el,t,a,b=.6,dy=16){const p=eo(seg(t,a,a+b));el.style.opacity=p;el.style.transform='translateY('+lerp(dy,0,p).toFixed(1)+'px)'};
window.show=function(el,t,a,b=.6){el.style.opacity=eo(seg(t,a,a+b))};
window.pool=(x,y,w,h,c)=>'<div class="pool '+c+'" style="left:'+x+'px;top:'+y+'px;width:'+w+'px;height:'+h+'px"></div>';
window.push=(el,t,dur,a,b,ox,oy)=>{el.style.transformOrigin=ox+'px '+oy+'px';el.style.transform='scale('+lerp(a,b,eio(seg(t,0,dur)))+')'};
window.TXT=(cls,x,y,size,txt,col,anchor,font)=>'<text class="'+cls+'" x="'+x+'" y="'+y+'" text-anchor="'+(anchor||'middle')+'" style="font-family:'+(font||'Work Sans,sans-serif')+';font-weight:500;font-size:'+size+'px;fill:'+col+'">'+txt+'</text>';
window.note=(cls,x,y,txt,extra)=>'<p class="note '+cls+'" style="left:'+x+'px;top:'+y+'px;'+(extra||'')+'">'+txt+'</p>';

// ---------- dessins ----------
const PH='M-130 -250 Q-130 -270 -110 -270 H110 Q130 -270 130 -250 V250 Q130 270 110 270 H-110 Q-130 270 -130 250 Z';
window.W={
  page(id){return '<defs><pattern id="'+id+'-rule" width="1920" height="64" patternUnits="userSpaceOnUse"><rect width="1920" height="64" style="fill:var(--ground)"/><rect y="62" width="1920" height="2" style="fill:var(--rule)"/></pattern>'+
    '<pattern id="'+id+'-grain" width="9" height="11" patternUnits="userSpaceOnUse"><circle cx="2" cy="3" r=".9" style="fill:var(--rule)"/><circle cx="7" cy="8" r=".7" style="fill:var(--rule)"/></pattern></defs>'+
    '<rect x="-200" y="-200" width="2320" height="1480" fill="url(#'+id+'-rule)"/><rect x="-200" y="-200" width="2320" height="1480" fill="url(#'+id+'-grain)" opacity=".5"/><rect x="196" y="-200" width="3" height="1480" style="fill:var(--margin)"/>'},
  prep(root){return Array.from(root.querySelectorAll('[data-draw]')).map(el=>{const len=el.getTotalLength();el.style.strokeDasharray=len+' '+len;return{el,len,a:+el.dataset.draw,d:+(el.dataset.dur||.8)}})},
  draw(list,t){for(const s of list){const p=eo(clamp01((t-s.a)/s.d));s.el.style.strokeDashoffset=(s.len*(1-p)).toFixed(1);s.el.style.opacity=p>0?1:0}},
  boil(el,t,a=1.1){const k=Math.floor(t*12)%3;el.setAttribute('transform','translate('+[0,a,-a*.6][k]+' '+[0,-a*.5,a*.7][k]+')')},
  ground(y,x0,x1,d){return '<path class="ink-thin" data-draw="'+(d||0)+'" data-dur="1.2" d="M'+x0+' '+y+' Q'+((x0+x1)/2)+' '+(y-12)+' '+x1+' '+y+'"/>'},
  figure(cls,x,y,s,flip,fill){const f=flip?-1:1;fill=fill||'var(--wash2)';const b='M-34 0 L-30 -150 Q-48 -160 -56 -250 Q-58 -300 -20 -318 L20 -318 Q58 -300 56 -250 Q48 -160 30 -150 L34 0 Z';
    return '<g class="'+cls+'" transform="translate('+x+' '+y+') scale('+(s*f)+' '+s+')"><ellipse cx="0" cy="4" rx="90" ry="12" style="fill:var(--shade)"/><path d="'+b+'" style="fill:'+fill+'"/><path class="ink-thin" d="'+b+'"/><circle cy="-362" r="38" style="fill:'+fill+'"/><circle class="ink-thin" cy="-362" r="38"/><path class="pencil" d="M-24 -220 Q0 -210 24 -224 M-20 -120 L-16 -40 M18 -120 L16 -40"/></g>'},
  // silhouette de femme (robe évasée), sans visage
  woman(cls,x,y,s,flip,fill){const f=flip?-1:1;fill=fill||'var(--wash)';const b='M-70 0 L-34 -150 Q-50 -170 -52 -250 Q-54 -300 -18 -318 L18 -318 Q54 -300 52 -250 Q50 -170 34 -150 L70 0 Z';
    return '<g class="'+cls+'" transform="translate('+x+' '+y+') scale('+(s*f)+' '+s+')"><ellipse cx="0" cy="4" rx="100" ry="12" style="fill:var(--shade)"/><path d="'+b+'" style="fill:'+fill+'"/><path class="ink-thin" d="'+b+'"/><path d="M-40 -392 Q0 -420 40 -392 Q52 -350 44 -320 L-44 -320 Q-52 -350 -40 -392 Z" style="fill:'+fill+'"/><circle cy="-360" r="35" style="fill:'+fill+'"/><circle class="ink-thin" cy="-360" r="35"/><path class="ink-thin" d="M-36 -372 Q-44 -330 -40 -310 M36 -372 Q44 -330 40 -310"/><path class="pencil" d="M-22 -220 Q0 -210 22 -222 M-40 -90 Q0 -80 40 -90"/></g>'},
  tel(cls,x,y,s,night,inner){return '<g class="'+cls+'" transform="translate('+x+' '+y+') scale('+s+')"><path d="'+PH+'" style="fill:'+(night?'var(--nightlift)':'var(--paper2)')+'"/><path class="ink" d="'+PH+'"/>'+
    '<rect x="-104" y="-220" width="208" height="420" style="fill:'+(night?'#2B3754':'var(--ground)')+'"/><path class="ink-thin" d="M-26 236 H26"/>'+(inner||'')+'</g>'},
  moon(cls,x,y,r){return '<g class="'+cls+'"><path d="M'+x+' '+(y-r)+' A'+r+' '+r+' 0 1 0 '+x+' '+(y+r)+' A'+(r*.72)+' '+(r*.72)+' 0 1 1 '+x+' '+(y-r)+' Z" style="fill:var(--ground);opacity:.85"/></g>'},
  bub(cls,x,y,w,h,left,col){const tail=left?'M'+(x+40)+' '+(y+h)+' L'+(x+24)+' '+(y+h+34)+' L'+(x+80)+' '+(y+h):'M'+(x+w-80)+' '+(y+h)+' L'+(x+w-24)+' '+(y+h+34)+' L'+(x+w-40)+' '+(y+h);
    return '<g class="'+cls+'"><path d="'+tail+'" style="fill:var(--paper2)"/><rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="22" style="fill:var(--paper2)"/><rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="22" style="fill:none;stroke:'+(col||'var(--main)')+';stroke-width:3.5"/><path d="'+tail+'" style="fill:none;stroke:'+(col||'var(--main)')+';stroke-width:3.5;stroke-linejoin:round"/></g>'},
  // bulle avec texte manuscrit intégré (HTML positionné par-dessus)
  bubText(cls,x,y,w,txt,size,col){return '<p class="note '+cls+'" style="left:'+(x+24)+'px;top:'+(y+18)+'px;width:'+(w-48)+'px;font-size:'+(size||42)+'px;color:'+(col||'var(--main)')+'">'+txt+'</p>'},
  dial(cls,x,y,r){let t='';for(let i=0;i<12;i++){const a=i*Math.PI/6;t+='<path class="ink-thin" d="M'+(x+Math.sin(a)*(r-14)).toFixed(1)+' '+(y-Math.cos(a)*(r-14)).toFixed(1)+' L'+(x+Math.sin(a)*(r-28)).toFixed(1)+' '+(y-Math.cos(a)*(r-28)).toFixed(1)+'"/>'}
    return '<g class="'+cls+'"><circle cx="'+x+'" cy="'+y+'" r="'+r+'" style="fill:var(--paper2)"/><circle class="ink" cx="'+x+'" cy="'+y+'" r="'+r+'"/>'+t+'<path class="ink '+cls+'-m" d="M'+x+' '+(y+6)+' V'+(y-r+30)+'"/><path class="ink '+cls+'-h" style="stroke-width:8" d="M'+x+' '+(y+4)+' V'+(y-r*.5)+'"/><circle cx="'+x+'" cy="'+y+'" r="7" style="fill:var(--main)"/></g>'},
  hands(r,cls,x,y,hr,mn){r.querySelector('.'+cls+'-m').setAttribute('transform','rotate('+(mn*6).toFixed(1)+' '+x+' '+y+')');r.querySelector('.'+cls+'-h').setAttribute('transform','rotate('+((hr%12)*30+mn*.5).toFixed(1)+' '+x+' '+y+')')},
  heart(cls,x,y,s,col){return '<g class="'+cls+'" transform="translate('+x+' '+y+') scale('+s+')"><path d="M0 30 C-60 -10 -50 -70 -12 -60 Q0 -56 0 -40 Q0 -56 12 -60 C50 -70 60 -10 0 30 Z" style="fill:'+(col||'var(--accent)')+'"/><path class="ink-thin" d="M0 30 C-60 -10 -50 -70 -12 -60 Q0 -56 0 -40 Q0 -56 12 -60 C50 -70 60 -10 0 30 Z"/></g>'},
  // écran de visioconférence : deux vignettes
  screen(cls,x,y,w,h,night){return '<g class="'+cls+'"><rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="18" style="fill:'+(night?'var(--nightlift)':'var(--paper2)')+'"/><rect class="ink" x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="18"/><path class="ink" d="M'+(x+w/2-90)+' '+(y+h+70)+' H'+(x+w/2+90)+' M'+(x+w/2)+' '+(y+h)+' V'+(y+h+70)+'"/></g>'},
  suitcase(cls,x,y,s){return '<g class="'+cls+'" transform="translate('+x+' '+y+') scale('+s+')"><rect x="-110" y="-150" width="220" height="150" rx="14" style="fill:var(--paper2)"/><rect class="ink" x="-110" y="-150" width="220" height="150" rx="14"/><path class="ink-thin" d="M-40 -150 V-182 Q-40 -192 -30 -192 H30 Q40 -192 40 -182 V-150 M-60 -150 V0 M60 -150 V0"/></g>'},
  envelope(cls,x,y,s,col){return '<g class="'+cls+'" transform="translate('+x+' '+y+') scale('+s+')"><rect x="-110" y="-70" width="220" height="140" rx="8" style="fill:var(--paper2)"/><rect x="-110" y="-70" width="220" height="140" rx="8" style="fill:none;stroke:'+(col||'var(--main)')+';stroke-width:4"/><path d="M-110 -70 L0 10 L110 -70" style="fill:none;stroke:'+(col||'var(--main)')+';stroke-width:4;stroke-linejoin:round"/></g>'},
  calendar(cls,x,y,s,big,small,head){return '<g class="'+cls+'" transform="translate('+x+' '+y+') scale('+s+')"><rect x="-150" y="-170" width="300" height="340" rx="14" style="fill:var(--paper2)"/><rect class="ink" x="-150" y="-170" width="300" height="340" rx="14"/><rect x="-150" y="-170" width="300" height="80" rx="14" style="fill:var(--main)"/>'+
    TXT('',0,-116,34,head||'','var(--ground)')+'<text x="0" y="60" text-anchor="middle" style="font-family:Fraunces,Georgia,serif;font-weight:500;font-size:150px;fill:var(--main)">'+big+'</text>'+TXT('',0,130,32,small||'','var(--second)')+'</g>'},
  checklist(cls,x,y,items,cross){return '<g class="'+cls+'">'+items.map((it,i)=>'<g class="'+cls+'-i'+i+'"><rect class="ink-thin" x="'+x+'" y="'+(y+i*70-26)+'" width="36" height="36" rx="4"/>'+TXT('',x+56,y+i*70+4,34,it,'var(--main)','start')+(cross?'<path class="'+cls+'-x'+i+'" d="M'+(x-10)+' '+(y+i*70-6)+' H'+(x+56+it.length*17)+'" style="stroke:var(--accent);stroke-width:5;stroke-linecap:round"/>':'')+'</g>').join('')+'</g>'},
  house(cls,x,y,s){return '<g class="'+cls+'" transform="translate('+x+' '+y+') scale('+s+')"><path d="M-160 0 V-180 L0 -300 L160 -180 V0 Z" style="fill:var(--paper2)"/><path class="ink" d="M-180 -170 L0 -310 L180 -170 M-160 -185 V0 H160 V-185"/><rect class="ink-thin" x="-40" y="-110" width="80" height="110"/><rect class="ink-thin" x="-120" y="-150" width="60" height="50"/><rect class="ink-thin" x="60" y="-150" width="60" height="50"/></g>'},
  glass(cls,x,y,s){return '<g class="'+cls+'" transform="translate('+x+' '+y+') scale('+s+')"><path class="ink-thin" d="M-40 -160 Q-44 -90 0 -70 Q44 -90 40 -160 Z M0 -70 V0 M-34 0 H34" style="fill:var(--paper2)"/></g>'}
};

// ---------- montage ----------
const SCENES=[];window.SCENES=SCENES;
// sc(id, [clés de blocs], build(root), render(t, P), opts{night}) ; P(k) = début (relatif au plan) de la k-ième phrase sous-titrée du plan.
window.sc=function(id,keys,build,render,opts){SCENES.push({id,keys,build,render,night:!!(opts&&opts.night),lead:(opts&&opts.lead)||0.35})};
window.startFilm=function(){
  const T=window.TIMING,B=T.blocks,stage=document.getElementById('stage');
  SCENES.forEach((s,i)=>{s.from=i===0?0:B[s.keys[0]][0]-s.lead;});
  SCENES.forEach((s,i)=>{s.to=i<SCENES.length-1?SCENES[i+1].from:T.end;s.dur=s.to-s.from;
    const subs=T.subs.filter(x=>s.keys.includes(x[3]));s.P=k=>{const x=subs[Math.min(k,subs.length-1)];return x?x[0]-s.from:0};s.PE=k=>{const x=subs[Math.min(k,subs.length-1)];return x?x[1]-s.from:0};
    s.Bs=k=>B[k][0]-s.from;s.Be=k=>B[k][1]-s.from;});
  const subEl=document.createElement('div');subEl.className='subs';
  window.TOTAL=T.end;
  SCENES.forEach(s=>{s.root=document.createElement('div');s.root.className='scene';stage.appendChild(s.root)});stage.appendChild(subEl);
  window.SUBS=T.subs;
  window.ready=document.fonts.ready.then(()=>{SCENES.forEach(s=>{s.build.call(s,s.root)});return true});
  window.renderAt=function(t){let cur=SCENES[SCENES.length-1];for(const s of SCENES)if(t>=s.from&&t<s.to){cur=s;break}
    SCENES.forEach(s=>s.root.style.visibility=s===cur?'visible':'hidden');cur.render.call(cur,t-cur.from);
    const sub=T.subs.find(s=>t>=s[0]-.05&&t<s[1]+.25);if(sub){if(subEl.textContent!==sub[2])subEl.textContent=sub[2];subEl.style.opacity=Math.min(1,(t-sub[0]+.05)/.15,(sub[1]+.25-t)/.15)}else subEl.style.opacity=0;
    subEl.classList.toggle('dark',cur.night);return cur.id};
  window.SCENES_INFO=()=>SCENES.map(s=>[s.id,+s.from.toFixed(2),+s.to.toFixed(2)]);
};
})();
