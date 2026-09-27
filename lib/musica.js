/* Música 1906 — trilha sonora Belle Époque do "14 Bis do Dumont", sintetizada no navegador (Web Audio, sem arquivos de áudio).
   Quatro peças originais no estilo francês de 1906:
     abertura — "L'Oiseau de Proie", marcha-galope de banda (novidade e aventura)
     passeio  — "Promenade sous les hortensias", valsa de café com acordeão (positiva e tranquila)
     voo      — "Barcarolle des nuages", barcarola com harpa e flauta (flutuando no céu)
     menu     — "Boîte à musique", gavota de caixinha de música com celesta (menus e configurações)
   Musica1906.render(id,{sr,yieldMs}) → Promise<{sr,len,ch:[L,R],dur,bar}>: cada seção é gravada num OfflineAudioContext
   separado (poucos nós por vez, roda fora da thread principal) e as caudas do fim caem no começo — o laço não tem emenda. */
(function(){
'use strict';
const TAIL=3.2;

/* ---------- notas e acordes ---------- */
const PC={c:0,d:2,e:4,f:5,g:7,a:9,b:11};
function midi(s){const m=/^([a-g])([#b]?)(\d)$/.exec(s);if(!m)throw Error('Musica1906: nota inválida "'+s+'"');
  return 12*(+m[3]+1)+PC[m[1]]+(m[2]==='#'?1:m[2]==='b'?-1:0);}
const hz=m=>440*Math.pow(2,(m-69)/12);
const QUAL={'':[0,4,7],m:[0,3,7],'7':[0,4,7,10],m7:[0,3,7,10],maj7:[0,4,7,11],'6':[0,4,7,9],m6:[0,3,7,9],
  dim:[0,3,6],dim7:[0,3,6,9],m7b5:[0,3,6,10],aug:[0,4,8]};
function chordOf(s){const m=/^([A-G])([#b]?)(maj7|m7b5|dim7|dim|aug|m7|m6|m|7|6)?(?:\/([A-G])([#b]?))?$/.exec(s);
  if(!m)throw Error('Musica1906: acorde inválido "'+s+'"');
  const acc=a=>a==='#'?1:a==='b'?-1:0,root=(PC[m[1].toLowerCase()]+acc(m[2])+12)%12,iv=QUAL[m[3]||''];
  return {root,pcs:iv.map(i=>(root+i)%12),fifth:(root+iv[2])%12,bass:m[4]?(PC[m[4].toLowerCase()]+acc(m[5])+12)%12:root};}
const inRange=(pc,lo)=>lo+(((pc-lo)%12)+12)%12;                   // a nota dessa classe logo acima de lo
function voicing(pcs,lo){return pcs.map(pc=>inRange(pc,lo)).sort((a,b)=>a-b);}
function scaleOf(k){const r=chordOf(k).root;return [0,2,4,5,7,9,11].map(i=>(r+i)%12);}

/* compassos separados por "|"; melodia "nota:unidades" (unidade = colcheia), "r" pausa, "~" liga à nota anterior;
   acordes "D" (o compasso todo) ou "D:3 A7:3" */
function parseCh(str,BU){const out=[];str.split('|').forEach((bar,bi)=>{const tk=bar.trim().split(/\s+/).filter(Boolean);
  let fixed=0,free=0;for(const t of tk){const p=t.split(':');if(p[1])fixed+=+p[1];else free++;}
  const each=free?(BU-fixed)/free:0;let u=0;
  for(const t of tk){const p=t.split(':'),d=p[1]?+p[1]:each;out.push(Object.assign(chordOf(p[0]),{u0:bi*BU+u,u1:bi*BU+u+d}));u+=d;}
  if(Math.abs(u-BU)>1e-6)throw Error('Musica1906: compasso '+(bi+1)+' de acordes com '+u+' unidades: '+bar);});return out;}
function parseMel(str,BU,nb,tag){const out=[],bars=str.split('|');
  if(bars.length!==nb)throw Error('Musica1906: '+tag+' tem '+bars.length+' compassos de melodia e '+nb+' de acordes');
  bars.forEach((bar,bi)=>{let s=0;for(const t of bar.trim().split(/\s+/).filter(Boolean)){const p=t.split(':'),d=+p[1];
      if(!(d>0))throw Error('Musica1906: duração inválida "'+t+'" em '+tag);
      if(p[0]==='~'){if(out.length)out[out.length-1].d+=d;}else if(p[0]!=='r')out.push({u:bi*BU+s,d,m:midi(p[0])});s+=d;}
    if(Math.abs(s-BU)>1e-6)throw Error('Musica1906: '+tag+' compasso '+(bi+1)+' soma '+s+' unidades (esperado '+BU+'): '+bar);});
  return out;}

/* ---------- as quatro peças ---------- */
const AB_A='D|G|D|A7|D|G|D:3 A7:3|D',
  AB_Am='d5:1 e5:1 f#5:1 a5:3|b5:2 a5:1 g5:2 e5:1|f#5:2 e5:1 d5:2 f#5:1|e5:3 a4:3|d5:1 e5:1 f#5:1 a5:3|b5:2 d6:1 b5:2 g5:1|a5:2 f#5:1 e5:2 c#5:1|d5:3 r:1 a4:1 a4:1';
const PA_A14='d5:4 e5:1 d5:1|b4:4 g4:2|a4:4 b4:1 a4:1|f#4:4 d4:2|c5:4 d5:1 c5:1|a4:4 f#4:2|g4:2 b4:2 d5:2|g5:4 r:2|d5:4 e5:1 d5:1|f5:4 d5:2|e5:4 f5:1 e5:1|eb5:4 c5:2|d5:2 g5:2 b5:2|b5:4 g#5:2',
  PA_C14='G|G|D7|D7|D7|D7|G|G|G|G7|C|Cm|G/D|E7';
const VO_A='F|F|Gm7|C7|F|Dm|Gm:3 C7:3|F',
  VO_A7='c5:3 d5:2 c5:1|a4:6|bb4:3 c5:2 bb4:1|g4:6|a4:3 c5:2 f5:1|f5:3 e5:2 d5:1|d5:3 c5:2 bb4:1';
const ME_A6='e5:2 g5:2 c6:2 g5:2|a5:1 g5:1 f5:1 e5:1 g5:4|f5:2 d5:2 b4:2 d5:2|e5:2 c5:2 g4:4|a4:2 c5:2 f5:2 a5:2|g5:1 a5:1 g5:1 f5:1 e5:4',
  ME_A2c='C|C|G7|C|F|C|G7|C',ME_A2m=ME_A6+'|f5:2 d5:2 b4:2 d5:2|c5:4 c6:4';
const TRACKS={
  abertura:{titulo:"L'Oiseau de Proie",nome:'Abertura',desc:'Marcha-galope de banda — novidade e aventura',u:60/(116*3),bar:6,k:'D',rms:0.15,seed:11,
    order:['intro','fan','A','A2','B','A2','trio','trio2','ponte','fin'],sec:{
    intro:{ch:'D|Bb|C|A7',dyn:0.85,cr:[0.45,1],
      mel:'f#5:1 a5:1 d6:1 f#6:3|f5:1 bb5:1 d6:1 f6:3|e5:1 g5:1 c6:1 e6:3|e5:1 g5:1 a5:1 c#6:3',
      lay:['cel mel .5','hrp arp .45 up','str pad .5','dr perc .8 intro']},
    fan:{ch:'D|A',mel:'a4:1 a4:1 a4:1 d5:3|e5:1 e5:1 e5:1 a5:3',
      lay:['cor mel 1','fl mel .4 +12','hrn harm .6','tuba bass .8 long','dr perc .8 fanf']},
    A:{ch:AB_A,mel:AB_Am,lay:['cor mel .9','cl harm .45','tuba bass .75 marcha','hrn chd .45 marcha','dr perc .6 marcha']},
    A2:{ch:AB_A,mel:AB_Am,lay:['cor mel .9','fl mel .45 +12','cel mel .18 +12','cl harm .45','tuba bass .8 marcha','hrn chd .5 marcha','dr perc .7 marcha']},
    B:{ch:'G|D|Em|A|Bm|F#7|Bm:3 E7:3|A7',dyn:0.9,
      mel:'b4:2 d5:1 g5:3|f#5:2 e5:1 d5:3|e5:2 g5:1 b5:2 a5:1|a5:3 e5:3|f#5:2 b5:1 a5:2 f#5:1|e5:2 c#5:1 a#4:3|d5:2 f#5:1 e5:2 g#5:1|a5:3 g5:2 e5:1',
      lay:['vln mel .75','cl harm .4','tuba bass .6 marcha','hrn chd .35 marcha','dr perc .5 marchaL']},
    trio:{k:'G',ch:'G|G|C|G|Am|D7|G:3 Em:3|A7:3 D7:3',dyn:0.85,
      mel:'b4:3 d5:3|g5:3 f#5:2 e5:1|e5:3 g5:3|d5:6|c5:3 e5:3|a5:3 g5:2 f#5:1|g5:3 e5:3|e5:3 c5:2 a4:1',
      lay:['vln mel .7','cl mel .4 -12','hrp arp .3 up','tuba bass .55 marcha','hrn chd .3 marcha','dr perc .45 marchaL']},
    trio2:{k:'G',ch:'G|G7|C|Cm|G/D|E7|Am:3 D7:3|G',dyn:0.95,
      mel:'b4:3 d5:3|g5:3 f5:3|e5:3 c6:3|c6:2 bb5:1 g5:2 eb5:1|d5:3 g5:3|g#5:3 b5:2 d6:1|c6:3 a5:2 f#5:1|g5:3 r:3',
      lay:['vln mel .75','fl mel .35 +12','cl mel .4 -12','hrp arp .3 up','tuba bass .6 marcha','hrn chd .35 marcha','dr perc .55 marcha']},
    ponte:{ch:'A7|A7',cr:[0.8,1.05],mel:'a4:1 c#5:1 e5:1 a5:3|g5:1 e5:1 c#5:1 e5:3',
      lay:['cor mel .9','fl mel .4 +12','hrn harm .5','tuba bass .7 marcha','dr perc .7 rufo']},
    fin:{ch:'D|G|A7|D',end:1,mel:'d5:1 e5:1 f#5:1 a5:3|b5:1 a5:1 g5:1 b5:3|a5:2 f#5:1 e5:2 c#5:1|d5:3 r:3',
      lay:['cor mel 1','fl mel .45 +12','cel mel .2 +12','cl harm .5','tuba bass .85 marcha','hrn chd .5 marcha','str pad .3','dr perc .8 marcha']}}},
  passeio:{titulo:'Promenade sous les hortensias',nome:'Passeio',desc:'Valsa de café com acordeão — positiva e tranquila',u:60/(126*2),bar:6,k:'G',rms:0.12,seed:23,
    order:['A','A2','B','A3'],sec:{
    A:{ch:PA_C14+'|A7|D7',mel:PA_A14+'|a5:2 g5:2 e5:2|f#5:2 e5:2 c5:2',
      lay:['acc mel .8','pz bass .7 valsa','gtr chd .45 valsa','dr perc .5 valsa']},
    A2:{ch:PA_C14+'|Am:4 D7:2|G',mel:PA_A14+'|a5:4 f#5:2|g5:6',
      lay:['vln mel .7','acc harm .35','pz bass .7 valsa','gtr chd .45 valsa','dr perc .5 valsa']},
    B:{k:'C',ch:'C|C|G7|G7|G7|G7|C|C|F|F|C|A7|Dm|G7|C|D7',dyn:0.85,
      mel:'g5:6|e5:4 c5:2|d5:4 f5:2|b4:6|d5:4 e5:1 d5:1|f5:4 b4:2|c5:6|e5:2 g5:2 c6:2|a5:6|c6:4 a5:2|g5:6|a5:2 g5:2 e5:2|f5:4 d5:2|b4:2 d5:2 f5:2|e5:6|c6:2 a5:2 f#5:2',
      lay:['fl mel .6','cl harm .4','pz bass .6 valsa','pno chd .35 valsa','dr perc .4 valsa']},
    A3:{ch:PA_C14+'|Am:4 D7:2|G',mel:PA_A14+'|a5:4 f#5:2|g5:6',
      lay:['acc mel .8','vln harm .4','fl mel .16 +12','pz bass .7 valsa','gtr chd .45 valsa','dr perc .5 valsa']}}},
  voo:{titulo:'Barcarolle des nuages',nome:'Voo',desc:'Barcarola com harpa e flauta — flutuando sobre as nuvens',u:60/(54*3),bar:6,k:'F',rms:0.11,seed:37,
    order:['A','B','A2','C'],sec:{
    A:{ch:VO_A,mel:VO_A7+'|a4:6',lay:['fl mel .6','hrp arp .45 barc','vc bass .45 barc','str pad .25']},
    B:{ch:'Dm|A7|Dm|Dm|Bb|F/C|Gm7:3 C7:3|C7',dyn:0.95,
      mel:'a5:3 g5:2 f5:1|e5:3 c#5:2 a4:1|d5:3 f5:2 a5:1|d6:6|d6:3 c6:2 bb5:1|a5:3 f5:2 c5:1|d5:3 e5:2 g5:1|bb5:3 g5:2 e5:1',
      lay:['vln mel .6','cl harm .35','hrp arp .45 barc','vc bass .45 barc','str pad .25']},
    A2:{ch:VO_A,mel:VO_A7+'|a4:3 c5:2 f5:1',lay:['vln mel .5','fl mel .35 +12','cl harm .3','hrp arp .45 barc','vc bass .45 barc','str pad .25']},
    C:{k:'Bb',ch:'Bb|Eb|Bb/F|F7|Gm|Cm7:3 F7:3|Bb|C7',dyn:0.9,
      mel:'f5:3 d5:2 bb4:1|g5:3 eb5:2 bb4:1|f5:3 bb5:2 d6:1|c6:3 a5:3|bb5:3 g5:2 d5:1|eb5:3 c5:2 a4:1|bb4:6|bb5:3 g5:2 e5:1',
      lay:['cel mel .45','fl mel .35','str pad .3','hrp arp .4 barc','vc bass .45 barc']}}},
  menu:{titulo:'Boîte à musique',nome:'Menus',desc:'Gavota de caixinha de música — calma e delicada',u:60/(96*2),bar:8,k:'C',rms:0.1,seed:41,
    order:['A','A2','B','A3'],sec:{
    A:{ch:'C|C|G7|C|F|C|D7|G',mel:ME_A6+'|f#5:2 a5:2 d6:2 c6:2|b5:2 a5:1 g5:1 d5:4',lay:['cel mel .55','pz bass .5 gav','hrp chd .35 gav']},
    A2:{ch:ME_A2c,mel:ME_A2m,lay:['cl mel .45','cel mel .22 +12','pz bass .5 gav','hrp chd .35 gav']},
    B:{ch:'Am|E7|Am|E|Dm|Am|Bm7b5:4 E7:4|Am:4 G7:4',dyn:0.9,
      mel:'e5:2 a5:2 c6:2 b5:2|g#5:2 b5:2 e5:4|a5:2 c6:2 e6:2 c6:2|b5:6 r:2|f5:2 a5:2 d6:2 a5:2|e5:2 a5:2 c6:4|d6:2 b5:2 g#5:2 e5:2|a5:4 g5:2 f5:2',
      lay:['fl mel .45','cl harm .3','pz bass .45 gav','hrp chd .3 gav','str pad .15']},
    A3:{ch:ME_A2c,mel:ME_A2m,lay:['cel mel .55','hrp harm .3','pz bass .5 gav','pno chd .28 gav']}}}
};

/* ---------- da partitura aos eventos ---------- */
function rng(seed){return function(){seed=seed+0x6D2B79F5|0;let t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296;};}
const PERC={bd:1,sn:1,cym:1,tri:1,tim:1};
const BASS={marcha:[[0,'R',2.2],[3,'5',2.2]],valsa:[[0,'A',2]],barc:[[0,'R',6]],gav:[[0,'R',2],[4,'5',2]],long:[[0,'R',6]]};
const CHD={marcha:[[2,1],[5,1]],valsa:[[2,1.6],[4,1.6]],gav:[[2,1.5],[6,1.5]]};
const ARP={up:[0,1,2,3,4,5],barc:[0,2,3,4,3,2]};
function percBar(p,bi,nb){const last=bi===nb-1,h=[];
  if(p==='marcha'){h.push(['bd',0,0.8],['bd',3,0.55],['sn',0,0.45],['sn',2,0.28]);if(bi===0)h.push(['cym',0,0.5]);
    if(last&&nb>2)for(let u=3;u<6;u+=0.5)h.push(['sn',u,0.22+(u-3)*0.14]);else h.push(['sn',5,0.28]);}
  else if(p==='marchaL'){h.push(['bd',0,0.6]);if(bi%2===0)h.push(['tri',0,0.35]);}
  else if(p==='fanf')h.push(['sn',0,0.55],['sn',1,0.45],['sn',2,0.5],['bd',3,0.9],['cym',3,0.6]);
  else if(p==='rufo'){for(let u=0;u<6;u+=0.5)h.push(['sn',u,0.18+((bi*6+u)/(nb*6))*0.6]);if(bi===0)h.push(['bd',0,0.6]);}
  else if(p==='intro'){if(!last)h.push(['tim',0,0.3,'R']);else for(let u=0;u<6;u+=0.5)h.push(['tim',u,0.12+u*0.11,'R']);}
  else if(p==='valsa'){if(bi%4===0)h.push(['tri',0,0.22]);}
  return h;}
function compile(id){const T=TRACKS[id],U=T.u,BU=T.bar,R=rng(T.seed),ev=[],secs=[];let t=0;
  const jit=()=>(R()-0.5)*0.008,hv=()=>0.94+R()*0.12;
  T.order.forEach((name,k)=>{const S=T.sec[name],tag=id+'.'+name,chs=parseCh(S.ch,BU),nb=Math.round(chs[chs.length-1].u1/BU);
    const mel=S.mel?parseMel(S.mel,BU,nb,tag):[],scale=scaleOf(S.k||T.k),len=nb*BU,t0=t;
    const at=u=>chs.find(c=>u>=c.u0-1e-6&&u<c.u1-1e-6)||chs[chs.length-1];
    const dyn=u=>(S.dyn||1)*(S.cr?S.cr[0]+(S.cr[1]-S.cr[0])*u/len:1);
    const push=(i,u,d,m,v,late)=>ev.push({i,k,t:t0+u*U+Math.max(0,jit()+(late||0)),d:d*U,f:m?hz(m):0,v:v*dyn(u)*hv()});
    const endBar=S.end?nb-1:-1;
    for(const L of S.lay){const tk=L.split(/\s+/),inst=tk[0],src=tk[1],v=+tk[2];let pat=null,oct=0;
      for(const x of tk.slice(3)){if(/^[+-]\d+$/.test(x))oct=+x;else pat=x;}
      if(src==='mel')for(const n of mel)push(inst,n.u,n.d,n.m+oct,v*(n.u%BU===0?1.08:1));
      else if(src==='harm')for(const n of mel){if(n.d<1)continue;const c=at(n.u);let h=null;
        for(const kk of [3,4,8,9])if(c.pcs.includes(((n.m-kk)%12+12)%12)){h=n.m-kk;break;}
        if(h===null&&c.pcs.includes(n.m%12)&&c.pcs.includes(((n.m-5)%12+12)%12))h=n.m-5;
        if(h===null)for(const kk of [3,4])if(scale.includes(((n.m-kk)%12+12)%12)){h=n.m-kk;break;}
        if(h!==null)push(inst,n.u,n.d,h+oct,v);}
      else if(src==='bass')for(let b=0;b<nb;b++){
        const hits=b===endBar?[[0,'R',4]]:BASS[pat];
        for(const [u,w,d] of hits){const c=at(b*BU+u),first=Math.abs(c.u0-(b*BU+u))<1e-6;
          let pc=c.bass;if(w==='5'&&!first)pc=c.fifth;else if(w==='A'&&!first&&(Math.floor(c.u0/BU)+b)%2===1)pc=c.fifth;
          push(inst,b*BU+u,d,inRange(pc,40)+oct,v*(u===0?1:0.85));}}
      else if(src==='chd')for(let b=0;b<nb;b++){const hits=b===endBar?[[0,4]]:CHD[pat];
        for(const [u,d] of hits){const c=at(b*BU+u);for(const m of voicing(c.pcs,55+oct))push(inst,b*BU+u,d,m,v*0.8,0.006);}}
      else if(src==='pad')for(const c of chs)for(const m of voicing(c.pcs,53+oct))push(inst,c.u0,c.u1-c.u0,m,v*0.7);
      else if(src==='arp')for(let b=0;b<nb;b++)for(let u=0;u<BU;u++){const c=at(b*BU+u),lo=pat==='barc'?48:50,r0=inRange(c.bass,lo),tones=[];
        for(let m=r0;m<r0+25;m++)if(c.pcs.includes(m%12))tones.push(m);
        const idx=ARP[pat][u%6];if(b===endBar&&u>0)break;push(inst,b*BU+u,pat==='barc'?2.5:1.5,tones[Math.min(idx,tones.length-1)]+oct,v*(u===0?1.1:0.9));}
      else if(src==='perc')for(let b=0;b<nb;b++){const hits=b===endBar?[['bd',0,1],['cym',0,0.9],['tim',0,0.8,'R']]:percBar(pat,b,nb);
        for(const [pi,u,pv,pm] of hits){const c=at(b*BU+u);push(pi,b*BU+u,1,pm?inRange(c.root,38):0,v*pv);}}}
    secs.push({t0,t1:t0+len*U});t+=len*U;});
  return {ev,secs,dur:t,bar:BU*U};}

/* ---------- instrumentos ---------- */
const INS={cor:{g:.33,p:-.18,r:.2},hrn:{g:.31,p:.28,r:.25},tuba:{g:.4,p:.05,r:.1,lp:900},fl:{g:.33,p:.22,r:.3},cl:{g:.19,p:-.32,r:.25},
  vln:{g:.235,p:-.25,r:.3},str:{g:.216,p:.12,r:.4},vc:{g:.34,p:.15,r:.25,lp:1600},acc:{g:.19,p:-.08,r:.2,lp:3400},pno:{g:.316,p:.18,r:.25},
  gtr:{g:.5,p:.3,r:.2},hrp:{g:.3,p:.32,r:.35},cel:{g:.47,p:-.22,r:.35},pz:{g:.57,p:0,r:.15,lp:1400},dr:{g:.5,p:.05,r:.15}};   // ganhos: cada um a ~-20 dB por nota
const cf=(c,f)=>Math.min(f,c.sampleRate*0.45);
function G(c,t,a,pk,hold,rel,to){const g=c.createGain(),p=g.gain,h=Math.max(a,hold);p.setValueAtTime(0,t);p.linearRampToValueAtTime(pk,t+a);
  p.setValueAtTime(pk,t+h);p.setTargetAtTime(0,t+h,rel);g.connect(to);return g;}
function D(c,t,pk,tau,to){const g=c.createGain(),p=g.gain;p.setValueAtTime(0,t);p.linearRampToValueAtTime(pk,t+0.004);p.setTargetAtTime(0,t+0.004,tau);g.connect(to);return g;}
function O(c,t,end,f,w,det){const o=c.createOscillator();if(typeof w==='string')o.type=w;else o.setPeriodicWave(w);
  o.frequency.value=f;if(det)o.detune.value=det;o.start(t);o.stop(end);return o;}
function F(c,type,f,q,to){const b=c.createBiquadFilter();b.type=type;b.frequency.value=cf(c,f);b.Q.value=q;b.connect(to);return b;}
function VIB(c,t,end,rate,cents,delay,os){if(end-t<delay+0.3)return;const l=c.createOscillator(),g=c.createGain();l.frequency.value=rate;
  g.gain.setValueAtTime(0,t+delay);g.gain.linearRampToValueAtTime(cents,t+delay+0.35);l.connect(g);for(const o of os)g.connect(o.detune);l.start(t+delay);l.stop(end);}
function NZ(c,X,t,end){const s=c.createBufferSource();s.buffer=X.noise;s.loop=true;s.start(t,X.rnd()*0.9);s.stop(end);return s;}
const V={
  cor(c,o,t,d,f,v){const e=t+d+0.35,g=G(c,t,0.022,v,d*0.9,0.05,o),b=c.createBiquadFilter(),fr=b.frequency;b.type='lowpass';b.Q.value=1.4;
    fr.setValueAtTime(cf(c,f*1.2),t);fr.linearRampToValueAtTime(cf(c,f*7),t+0.035);fr.setTargetAtTime(cf(c,f*4),t+0.04,0.15);b.connect(g);
    const s=O(c,t,e,f,'sawtooth');s.connect(b);VIB(c,t,e,5.3,8,0.28,[s]);},
  hrn(c,o,t,d,f,v){const e=t+d+0.3,g=G(c,t,0.03,v,d*0.85,0.06,o),b=c.createBiquadFilter(),fr=b.frequency;b.type='lowpass';b.Q.value=0.8;
    fr.setValueAtTime(cf(c,f),t);fr.linearRampToValueAtTime(cf(c,f*3),t+0.05);fr.setTargetAtTime(cf(c,f*2),t+0.06,0.2);b.connect(g);O(c,t,e,f,'sawtooth').connect(b);},
  tuba(c,o,t,d,f,v,X){const g=G(c,t,0.02,v,d*0.8,0.05,o);O(c,t,t+d+0.3,f,X.W.tuba).connect(F(c,'lowpass',f*5,0.8,g));},
  fl(c,o,t,d,f,v,X){const e=t+d+0.3,g=G(c,t,0.05,v,d*0.95,0.06,o),s=O(c,t,e,f,X.W.fl);s.connect(g);VIB(c,t,e,5,11,0.18,[s]);
    NZ(c,X,t,t+0.25).connect(F(c,'bandpass',f*2,1.5,G(c,t,0.015,v*0.3,0.02,0.05,o)));},
  cl(c,o,t,d,f,v){const e=t+d+0.3,g=G(c,t,0.035,v,d*0.95,0.06,o),s=O(c,t,e,f,'square');s.connect(F(c,'lowpass',Math.min(f*3.2,3500),0.7,g));VIB(c,t,e,4.6,5,0.3,[s]);},
  vln(c,o,t,d,f,v){const e=t+d+0.5,g=G(c,t,0.07,v,d,0.16,o),b=F(c,'lowpass',Math.min(f*5,6000),0.6,g),s1=O(c,t,e,f,'sawtooth',-7),s2=O(c,t,e,f,'sawtooth',7);
    s1.connect(b);s2.connect(b);VIB(c,t,e,5.6,13,0.12,[s1,s2]);},
  str(c,o,t,d,f,v){const e=t+d+1.4,g=G(c,t,0.3,v,d,0.45,o),b=F(c,'lowpass',f*3,0.5,g),s1=O(c,t,e,f,'sawtooth',-9),s2=O(c,t,e,f,'sawtooth',9);
    s1.connect(b);s2.connect(b);VIB(c,t,e,5,8,0.2,[s1,s2]);},
  vc(c,o,t,d,f,v){const e=t+d+0.8,g=G(c,t,0.1,v,d,0.25,o),s=O(c,t,e,f,'sawtooth',-5);s.connect(F(c,'lowpass',f*4,0.6,g));VIB(c,t,e,5.2,10,0.2,[s]);},
  acc(c,o,t,d,f,v,X){const e=t+d+0.3,g=G(c,t,0.03,v,d,0.06,o);for(const det of [-12,0,12])O(c,t,e,f,X.W.reed,det).connect(g);},
  pno(c,o,t,d,f,v,X){const tau=Math.max(0.25,Math.min(1.8,1.1*Math.sqrt(262/f))),e=t+Math.min(d+0.6,tau*5),g=D(c,t,v,tau,o);
    g.gain.setTargetAtTime(0,t+Math.max(d,0.05),0.08);
    const b=c.createBiquadFilter();b.type='lowpass';b.frequency.setValueAtTime(cf(c,f*10),t);b.frequency.setTargetAtTime(cf(c,f*2.5),t+0.01,tau*0.5);b.connect(g);
    O(c,t,e,f,X.W.pno).connect(b);const h=c.createGain();h.gain.value=0.5;h.connect(b);O(c,t,e,f,X.W.pno,4).connect(h);},
  gtr(c,o,t,d,f,v,X){const g=D(c,t,v,0.32,o);g.gain.setTargetAtTime(0,t+Math.max(d,0.05),0.06);
    const b=c.createBiquadFilter();b.type='lowpass';b.frequency.setValueAtTime(cf(c,f*7),t);b.frequency.setTargetAtTime(cf(c,f*2),t+0.01,0.12);b.connect(g);
    O(c,t,t+Math.min(d+0.4,1.6),f,X.W.hrp).connect(b);},
  hrp(c,o,t,d,f,v,X){const tau=Math.max(0.5,Math.min(2.4,1.5*Math.sqrt(262/f))),g=D(c,t,v,tau,o),b=c.createBiquadFilter();
    b.type='lowpass';b.frequency.setValueAtTime(cf(c,f*8),t);b.frequency.setTargetAtTime(cf(c,f*4),t+0.01,0.25);b.connect(g);O(c,t,t+tau*4,f,X.W.hrp).connect(b);},
  cel(c,o,t,d,f,v,X){const tau=Math.max(0.35,Math.min(1.5,1.1*Math.sqrt(523/f)));O(c,t,t+tau*4.5,f,X.W.cel).connect(D(c,t,v,tau,o));
    if(f*5.4<c.sampleRate*0.42)O(c,t,t+0.4,f*5.4,'sine').connect(D(c,t,v*0.25,0.05,o));},
  pz(c,o,t,d,f,v,X){const tau=Math.max(0.28,Math.min(0.6,0.35*Math.sqrt(110/f)*1.4));O(c,t,t+tau*5,f,X.W.pz).connect(F(c,'lowpass',f*6,0.7,D(c,t,v,tau,o)));},
  tim(c,o,t,d,f,v,X){v*=0.8;const g=D(c,t,v,0.8,o);O(c,t,t+3.5,f,'sine').connect(g);const h=D(c,t,v*0.35,0.5,o);O(c,t,t+2.5,f*1.5,'sine').connect(h);
    NZ(c,X,t,t+0.15).connect(F(c,'lowpass',300,0.7,D(c,t,v*0.5,0.03,o)));},
  bd(c,o,t,d,f,v,X){const s=O(c,t,t+0.8,110,'sine');s.frequency.setValueAtTime(110,t);s.frequency.exponentialRampToValueAtTime(46,t+0.1);s.connect(D(c,t,v,0.16,o));
    NZ(c,X,t,t+0.1).connect(F(c,'lowpass',300,0.7,D(c,t,v*0.4,0.02,o)));},
  sn(c,o,t,d,f,v,X){NZ(c,X,t,t+0.45).connect(F(c,'bandpass',2300,0.8,D(c,t,v*2.3,0.07,o)));O(c,t,t+0.3,190,'triangle').connect(D(c,t,v*1.1,0.05,o));},
  cym(c,o,t,d,f,v,X){NZ(c,X,t,t+2.6).connect(F(c,'highpass',6000,0.7,D(c,t,v*0.96,0.5,o)));},
  tri(c,o,t,d,f,v){const g=D(c,t,v*0.26,0.55,o);O(c,t,t+2.6,3150,'sine').connect(g);const h=D(c,t,v*0.15,0.45,o);O(c,t,t+2.2,4400,'sine').connect(h);}
};

/* ---------- material compartilhado: ondas, ruído, sala (reverberação) ---------- */
const DATA={};
function shared(sr){if(DATA[sr])return DATA[sr];const R=rng(99),n=Math.round(sr*2.3),ir=[new Float32Array(n),new Float32Array(n)];
  for(const a of ir){let lp=0;for(let i=0;i<n;i++){const t=i/sr,k=Math.min(0.9,0.2+t*0.5);lp=lp*k+(R()*2-1)*(1-k);
      a[i]=lp*Math.exp(-t*3.6)*(t<0.01?t/0.01:1)/(1-k*0.8);}
    for(const [ms,gain] of [[11,.5],[19,.35],[27,-.3],[37,.25],[53,-.18]]){const j=Math.round(ms*sr/1000)+(a===ir[1]?Math.round(sr*0.003):0);if(j<n)a[j]+=gain;}}
  const nz=new Float32Array(sr);for(let i=0;i<sr;i++)nz[i]=R()*2-1;
  return DATA[sr]={ir,nz};}
function buf(c,chans){const b=c.createBuffer(chans.length,chans[0].length,c.sampleRate);chans.forEach((a,i)=>{
  if(b.copyToChannel)b.copyToChannel(a,i);else b.getChannelData(i).set(a);});return b;}
function waves(c){const mk=a=>c.createPeriodicWave(new Float32Array(a.length),new Float32Array(a));
  return {reed:mk([0,1,.8,.6,.5,.45,.35,.3,.22,.18,.14,.1,.08]),pno:mk([0,1,.55,.28,.2,.12,.08,.05,.03]),hrp:mk([0,1,.35,.15,.07,.03]),
    fl:mk([0,1,.22,.07,.03]),pz:mk([0,1,.5,.22,.1,.05]),cel:mk([0,1,.12,.04,.22,0,.05]),tuba:mk([0,1,.7,.45,.3,.2,.12,.08])};}
function graph(c,sh){const m=c.createGain();m.connect(c.destination);const cv=c.createConvolver();cv.buffer=buf(c,sh.ir);cv.connect(m);
  const bus={};for(const k in INS){const I=INS[k],inp=c.createGain();inp.gain.value=I.g;let last=inp;
    if(I.lp){const b=c.createBiquadFilter();b.type='lowpass';b.frequency.value=cf(c,I.lp);last.connect(b);last=b;}
    if(c.createStereoPanner){const p=c.createStereoPanner();p.pan.value=I.p;last.connect(p);last=p;}
    last.connect(m);const s=c.createGain();s.gain.value=I.r;last.connect(s);s.connect(cv);bus[k]=inp;}
  return bus;}

/* ---------- gravação ---------- */
const OAC=window.OfflineAudioContext||window.webkitOfflineAudioContext;
async function render(id,opt){opt=opt||{};const sr=opt.sr||22050,C=compile(id),N=Math.round(C.dur*sr),L=new Float32Array(N),Rt=new Float32Array(N),sh=shared(sr);
  let next=0;async function chunk(k){const s=C.secs[k],evs=C.ev.filter(e=>e.k===k);if(!evs.length)return;
    const len=Math.ceil((s.t1-s.t0+TAIL)*sr),c=new OAC(2,len,sr),X={W:waves(c),noise:buf(c,[sh.nz]),rnd:rng(k+7)},bus=graph(c,sh);
    for(const e of evs)V[e.i](c,bus[PERC[e.i]?'dr':e.i],Math.max(0,e.t-s.t0),e.d,e.f,e.v,X);
    const out=await new Promise((ok,no)=>{c.oncomplete=ev=>ok(ev.renderedBuffer);const p=c.startRendering();if(p&&p.catch)p.catch(no);});
    const a=out.getChannelData(0),b=out.getChannelData(1),o=Math.round(s.t0*sr);
    for(let i=0;i<len;i++){const j=(o+i)%N;L[j]+=a[i];Rt[j]+=b[i];}
    if(opt.yieldMs)await new Promise(r=>setTimeout(r,opt.yieldMs));}
  // duas seções por vez: cada OfflineAudioContext grava na sua própria thread
  await Promise.all(Array.from({length:opt.par||2},async()=>{while(next<C.secs.length)await chunk(next++);}));
  let ss=0,pk=0;for(let i=0;i<N;i++){ss+=L[i]*L[i]+Rt[i]*Rt[i];pk=Math.max(pk,Math.abs(L[i]),Math.abs(Rt[i]));}
  const rms=Math.sqrt(ss/(2*N))||1,g=Math.min(TRACKS[id].rms/rms,0.95/(pk||1));
  for(let i=0;i<N;i++){L[i]*=g;Rt[i]*=g;}
  return {sr,len:N,ch:[L,Rt],dur:C.dur,bar:C.bar};}
function renderNote(inst,m,d,sr){sr=sr||22050;const sh=shared(sr),c=new OAC(2,Math.ceil((d+2.5)*sr),sr),X={W:waves(c),noise:buf(c,[sh.nz]),rnd:rng(1)};
  V[inst](c,graph(c,sh)[PERC[inst]?'dr':inst],0.01,d,hz(m),1,X);
  return new Promise(ok=>{c.oncomplete=e=>ok(e.renderedBuffer);c.startRendering();});}

window.Musica1906={
  faixas:Object.keys(TRACKS).map(id=>{const T=TRACKS[id];let dur=0;for(const n of T.order)dur+=T.sec[n].ch.split('|').length*T.bar*T.u;
    return {id,titulo:T.titulo,nome:T.nome,desc:T.desc,dur};}),
  render,_compile:compile,_note:renderNote,_TRACKS:TRACKS,_INS:INS
};
})();
