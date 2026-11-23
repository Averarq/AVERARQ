/* Plantas ilustrativas por tipología (referenciales, no son planos de arquitectura).
   Cada tipología usa una planta base de 2 pisos que se escala a sus m² construidos
   y se adapta a su programa (dormitorios, baños y recintos especiales).
   Unidades en metros. x hacia la derecha, y hacia abajo (fachada de acceso abajo). */
(function(){
"use strict";
const BW=6.5, BD=7.0;              // planta base (m)

/* Programa de cada tipología */
const PROG={
  A:{dorm:2,banos:1,extra:[],               visita:false},
  B:{dorm:2,banos:2,extra:["suite2"],       visita:true},
  C:{dorm:3,banos:2,extra:["terraza2"],     visita:true},
  D:{dorm:3,banos:2,extra:["quincho"],      visita:true},
  E:{dorm:3,banos:2,extra:["corredor"],     visita:true},
  F:{dorm:3,banos:3,extra:["corredor","suite"],visita:true},
  G:{dorm:4,banos:3,extra:["suite","logia"],visita:true},
  H:{dorm:4,banos:3,extra:["corredor","suite","escritorio"],visita:true}
};

function layout(code,m2){
  const P=PROG[code];
  const half=m2/2, D=Math.sqrt(half*BD/BW), W=half/D, sx=W/BW, sy=D/BD;
  const R=(t,n,x,y,w,h)=>({t,n,x:x*sx,y:y*sy,w:w*sx,h:h*sy});
  const has=k=>P.extra.includes(k);
  // ---- Primer piso
  const g=[
    R("cocina","Cocina",0,0,2.6,3.0),
    R("comedor","Comedor",2.6,0,3.9,3.0),
    R("escalera","",0,3.0,1.1,2.8),
    P.visita?R("bano","Baño visita",1.1,3.0,1.5,1.6):R("logia","Logia",1.1,3.0,1.5,1.6),
    R("bodega","Bodega",1.1,4.6,1.5,1.2),
    R("acceso","Acceso",0,5.8,2.6,1.2)
  ];
  if(has("escritorio")){ g.push(R("escritorio","Escritorio",2.6,3.0,2.2,1.9)); g.push(R("living","Living",2.6,4.9,3.9,2.1)); g.push(R("estar","Estar",4.8,3.0,1.7,1.9)); }
  else g.push(R("living","Living",2.6,3.0,3.9,4.0));
  // ---- Segundo piso
  const u=[R("escalera","",0,3.0,1.1,2.8), R("hall","Hall",1.1,3.0,1.5,2.0), R("bano","Baño",1.1,5.0,1.5,2.0), R("closet","Clóset",0,5.8,1.1,1.2)];
  // dormitorios norte
  if(P.dorm>=4){ u.push(R("dorm","Dormitorio 2",2.6,0,1.95,3.0)); u.push(R("dorm","Dormitorio 3",4.55,0,1.95,3.0)); }
  else u.push(R("dorm","Dormitorio 2",2.6,0,3.9,3.0));
  if(P.dorm>=3) u.push(R("dorm",P.dorm>=4?"Dormitorio 4":"Dormitorio 3",0,0,2.6,3.0));
  else u.push(has("suite2")?R("bano","Baño 2",0,0,2.6,3.0):R("estar","Estar",0,0,2.6,3.0));
  // principal
  if(has("suite")){ u.push(R("principal","Dormitorio principal",2.6,4.6,3.9,2.4)); u.push(R("bano","Baño suite",4.6,3.0,1.9,1.6)); u.push(has("logia")?R("logia","Logia",2.6,3.0,2.0,1.6):R("walkin","Walk-in",2.6,3.0,2.0,1.6)); }
  else u.push(R("principal","Dormitorio principal",2.6,3.0,3.9,4.0));
  // exteriores (fuera del perímetro)
  const gx=[], ux=[];
  if(has("corredor")) gx.push({t:"corredor",n:"Corredor",x:0,y:D,w:W,h:1.8});
  if(has("quincho"))  gx.push({t:"quincho",n:"Terraza y quincho",x:W*.35,y:D,w:W*.65,h:2.4});
  if(has("terraza2")) ux.push({t:"terraza",n:"Terraza",x:W*.4,y:D,w:W*.6,h:1.8});
  if(!has("corredor")&&!has("quincho")) gx.push({t:"pergola",n:"",x:W*.4,y:D,w:W*.6,h:1.2});
  // puertas: [x,y,ancho,orientación(h|v),giro]
  const d=(x,y,w,o,s)=>({x:x*sx,y:y*sy,w,o,s});
  const gd=[d(0.6,7.0,.9,"h",-1), d(1.25,4.6,.7,"h",1), d(1.25,5.8,.7,"h",-1)];
  const ud=[d(1.3,3.0,.8,"h",1), d(1.25,5.0,.7,"h",1), d(2.6,3.4,.8,"v",1), d(2.6,6.0,.8,"v",-1)];
  return {W,D,floors:[{n:"Primer piso",rooms:g,ext:gx,doors:gd},{n:"Segundo piso",rooms:u,ext:ux,doors:ud}]};
}

/* ---------- dibujo ---------- */
const C={wall:"#2b2e30",wood:"#d9c4a6",woodL:"#c9b08e",tile:"#dcdad4",tileL:"#c9c6be",deck:"#b08a5c",deckL:"#8f6c45",
  white:"#fbfaf7",bed:"#e9e6df",blanket:"#8c9aa3",blanket2:"#a9b6a0",wood2:"#8a6a4a",sofa:"#9aa5ab",rug:"#c9c3b8",green:"#6f8f5a",metal:"#9da3a6",glass:"#b9d7e6"};
const floorOf=t=>({cocina:"tile",bano:"tile",logia:"tile",bodega:"tile",acceso:"tile",escalera:"wood",corredor:"deck",quincho:"deck",terraza:"tile",pergola:"deck"}[t]||"wood");

function svgPlan(code,m2,opts={}){
  const L=layout(code,m2), S=46, pad=1.2, gap=2.2;
  const fl=opts.floor==null?L.floors:[L.floors[opts.floor]];
  const extH=Math.max(...fl.map(f=>Math.max(0,...f.ext.map(e=>e.y+e.h-L.D))));
  const fw=L.W, fh=L.D+extH, totalW=(opts.floor==null?fw*2+gap:fw)+pad*2, totalH=fh+pad*2+0.9;
  let o=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${totalW*S} ${totalH*S}" role="img" aria-label="Planta ilustrativa tipología ${code}">`;
  o+=`<defs>
   <pattern id="wd${code}" width="${S*1.2}" height="${S*.18}" patternUnits="userSpaceOnUse"><rect width="100%" height="100%" fill="${C.wood}"/><path d="M0 ${S*.18}H${S*1.2}M${S*.5} 0V${S*.18}" stroke="${C.woodL}" stroke-width="1"/></pattern>
   <pattern id="tl${code}" width="${S*.45}" height="${S*.45}" patternUnits="userSpaceOnUse"><rect width="100%" height="100%" fill="${C.tile}"/><path d="M0 0H${S*.45}V${S*.45}" fill="none" stroke="${C.tileL}" stroke-width="1"/></pattern>
   <pattern id="dk${code}" width="${S*.16}" height="${S}" patternUnits="userSpaceOnUse"><rect width="100%" height="100%" fill="${C.deck}"/><path d="M0 0V${S}" stroke="${C.deckL}" stroke-width="1.2"/></pattern>
   <filter id="sh${code}" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="1.2" dy="2" stdDeviation="1.6" flood-color="#000" flood-opacity=".28"/></filter>
  </defs>`;
  const fill=t=>({wood:`url(#wd${code})`,tile:`url(#tl${code})`,deck:`url(#dk${code})`})[floorOf(t)];
  const idx=opts.floor==null?[0,1]:[opts.floor];
  idx.forEach((fi,k)=>{
    const F=L.floors[fi], ox=(pad+k*(fw+gap))*S, oy=(pad+0.9)*S;
    const X=v=>ox+v*S, Y=v=>oy+v*S;
    o+=`<text x="${X(0)}" y="${Y(0)-S*.45}" font-family="Outfit,Segoe UI,sans-serif" font-size="${S*.42}" font-weight="600" fill="#eeeeec">${F.n}</text>`;
    // exteriores
    F.ext.forEach(e=>{o+=`<rect x="${X(e.x)}" y="${Y(e.y)}" width="${e.w*S}" height="${e.h*S}" fill="${fill(e.t)}"/>`;
      if(e.t==="corredor"||e.t==="pergola") for(let i=0;i<=Math.round(e.w/1.6);i++){const cx=X(e.x+Math.min(e.w-.15,i*e.w/Math.round(e.w/1.6)||.15)); o+=`<rect x="${cx-S*.09}" y="${Y(e.y+e.h)-S*.2}" width="${S*.18}" height="${S*.18}" fill="#f1efe9" filter="url(#sh${code})"/>`;}
      if(e.t==="quincho") o+=furn("quincho",e,X,Y,S,code);
      if(e.t==="terraza") o+=furn("terraza",e,X,Y,S,code);
      if(e.n) o+=label(e,X,Y,S,true);});
    // pisos
    F.rooms.forEach(r=>{o+=`<rect x="${X(r.x)}" y="${Y(r.y)}" width="${r.w*S}" height="${r.h*S}" fill="${fill(r.t)}"/>`;});
    // mobiliario
    F.rooms.forEach(r=>{o+=furn(r.t,r,X,Y,S,code);});
    // muros interiores
    F.rooms.forEach(r=>{o+=`<rect x="${X(r.x)}" y="${Y(r.y)}" width="${r.w*S}" height="${r.h*S}" fill="none" stroke="${C.wall}" stroke-width="${S*.12}"/>`;});
    // muro perimetral
    o+=`<rect x="${X(0)}" y="${Y(0)}" width="${L.W*S}" height="${L.D*S}" fill="none" stroke="${C.wall}" stroke-width="${S*.26}"/>`;
    // ventanas
    const win=(x1,y1,x2,y2)=>`<line x1="${X(x1)}" y1="${Y(y1)}" x2="${X(x2)}" y2="${Y(y2)}" stroke="${C.white}" stroke-width="${S*.2}"/><line x1="${X(x1)}" y1="${Y(y1)}" x2="${X(x2)}" y2="${Y(y2)}" stroke="${C.glass}" stroke-width="${S*.06}"/>`;
    F.rooms.forEach(r=>{ if(["escalera","closet","bodega","hall","walkin"].includes(r.t)) return;
      const ww=Math.min(r.w*.5,1.8);
      if(r.y<.01) o+=win(r.x+r.w/2-ww/2,0,r.x+r.w/2+ww/2,0);
      if(Math.abs(r.y+r.h-L.D)<.01 && r.t!=="acceso") o+=win(r.x+r.w/2-ww/2,L.D,r.x+r.w/2+ww/2,L.D);
      if(Math.abs(r.x+r.w-L.W)<.01){const wh=Math.min(r.h*.45,1.4); o+=win(L.W,r.y+r.h/2-wh/2,L.W,r.y+r.h/2+wh/2);} });
    // puertas
    F.doors.forEach(dd=>{const w=dd.w*S;
      if(dd.o==="h"){ o+=`<line x1="${X(dd.x)}" y1="${Y(dd.y)}" x2="${X(dd.x)+w}" y2="${Y(dd.y)}" stroke="${C.white}" stroke-width="${S*.3}"/>`;
        const sy=dd.s*w; o+=`<path d="M${X(dd.x)} ${Y(dd.y)} L${X(dd.x)} ${Y(dd.y)-sy} A${w} ${w} 0 0 ${dd.s>0?1:0} ${X(dd.x)+w} ${Y(dd.y)}" fill="none" stroke="#6c6f70" stroke-width="1.3"/>`; }
      else { o+=`<line x1="${X(dd.x)}" y1="${Y(dd.y)}" x2="${X(dd.x)}" y2="${Y(dd.y)+w}" stroke="${C.white}" stroke-width="${S*.3}"/>`;
        const sx=dd.s*w; o+=`<path d="M${X(dd.x)} ${Y(dd.y)} L${X(dd.x)+sx} ${Y(dd.y)} A${w} ${w} 0 0 ${dd.s>0?1:0} ${X(dd.x)} ${Y(dd.y)+w}" fill="none" stroke="#6c6f70" stroke-width="1.3"/>`; } });
    // rótulos
    F.rooms.forEach(r=>{ if(r.n) o+=label(r,X,Y,S,false); });
  });
  o+=`</svg>`; return {svg:o, L};
}
function label(r,X,Y,S,ext){
  const a=(r.w*r.h).toFixed(1).replace(".",",");
  const small=r.w<1.8||r.h<1.5, fs=S*(small?.2:.25);
  const cx=X(r.x+r.w/2), cy=Y(r.y+(ext?r.h/2:Math.min(r.h-.35,r.h*.82)));
  return `<g font-family="Outfit,Segoe UI,sans-serif" text-anchor="middle"><rect x="${cx-S*(small?.75:1.1)}" y="${cy-fs*1.05}" width="${S*(small?1.5:2.2)}" height="${fs*2.2}" rx="${fs*.4}" fill="rgba(26,28,27,.72)"/><text x="${cx}" y="${cy}" font-size="${fs}" font-weight="600" fill="#fff">${r.n}</text><text x="${cx}" y="${cy+fs*.95}" font-size="${fs*.8}" fill="#d6d6d2">${a} m²</text></g>`;
}
function furn(t,r,X,Y,S,code){
  const sh=`filter="url(#sh${code})"`, x=X(r.x), y=Y(r.y), w=r.w*S, h=r.h*S, m=S*.25;
  const rect=(a,b,c,d,f,rx=2,extra="")=>`<rect x="${a}" y="${b}" width="${c}" height="${d}" rx="${rx}" fill="${f}" ${extra}/>`;
  const bed=(bx,by,bw,bl,col)=>rect(bx,by,bw,bl,C.bed,4,sh)+rect(bx+bw*.08,by+bl*.06,bw*.84,bl*.16,C.white,4)+rect(bx,by+bl*.35,bw,bl*.65,col,4);
  const plant=(px,py)=>`<circle cx="${px}" cy="${py}" r="${S*.22}" fill="${C.green}" ${sh}/><circle cx="${px-S*.07}" cy="${py-S*.06}" r="${S*.1}" fill="#86a86d"/>`;
  switch(t){
    case "principal":{const bw=S*1.6,bl=S*2.0,bx=x+w/2-bw/2,by=y+m*1.2; return rect(bx-S*.35,by+S*.4,bw+S*.7,bl,C.rug,4)+bed(bx,by,bw,bl,C.blanket)+rect(bx-S*.55,by,S*.45,S*.45,C.wood2,3,sh)+rect(bx+bw+S*.1,by,S*.45,S*.45,C.wood2,3,sh)+plant(x+w-m*1.6,y+h-m*1.6);}
    case "dorm":{const bw=S*.95,bl=S*1.9; if(r.w*S>S*3.2){return bed(x+m,y+m,bw,bl,C.blanket2)+bed(x+w-m-bw,y+m,bw,bl,C.blanket2)+rect(x+w/2-S*.25,y+m,S*.5,S*.45,C.wood2,3,sh);} return bed(x+m,y+m,bw,bl,C.blanket2)+rect(x+m+bw+S*.1,y+m,S*.45,S*.45,C.wood2,3,sh)+rect(x+w-m-S*.6,y+h-m-S*1.2,S*.55,S*1.1,C.wood2,3,sh);}
    case "living":{const sw=Math.min(w-m*2,S*2.4); return rect(x+w/2-sw/2-S*.2,y+h*.28,sw+S*.4,S*1.6,C.rug,4)+rect(x+w/2-sw/2,y+h-m-S*.85,sw,S*.85,C.sofa,6,sh)+rect(x+w/2-sw/2,y+h-m-S*.85,sw,S*.25,"#86929a",6)+rect(x+w/2-S*.55,y+h*.38,S*1.1,S*.6,C.wood2,4,sh)+`<circle cx="${x+m+S*.45}" cy="${y+h*.35}" r="${S*.38}" fill="${C.sofa}" ${sh}/>`+plant(x+w-m-S*.2,y+m+S*.2);}
    case "comedor":{const tw=Math.min(w*.55,S*1.9),th=S*.95,tx=x+w/2-tw/2,ty=y+h/2-th/2;let c="";for(let i=0;i<3;i++){const cx=tx+tw*(i+.5)/3-S*.2;c+=rect(cx,ty-S*.5,S*.4,S*.4,"#6c7a74",6,sh)+rect(cx,ty+th+S*.1,S*.4,S*.4,"#6c7a74",6,sh);} return c+rect(tx,ty,tw,th,"#b39572",4,sh)+`<circle cx="${tx+tw/2}" cy="${ty+th/2}" r="${S*.15}" fill="${C.green}"/>`;}
    case "cocina":{const d=S*.62; return rect(x+m*.4,y+m*.4,w-m*.8,d,"#e8e6e1",2,sh)+rect(x+m*.4,y+m*.4,d,h*.75,"#e8e6e1",2,sh)+rect(x+w*.45,y+m*.5,S*.55,S*.42,C.metal,3)+`<g fill="#2e3133">${[0,1].map(i=>[0,1].map(j=>`<circle cx="${x+w*.75+i*S*.25}" cy="${y+m*.62+j*S*.22}" r="${S*.08}"/>`).join("")).join("")}</g>`+rect(x+w/2,y+h*.55,S*.9,S*.55,"#d8d2c6",3,sh);}
    case "bano":{const tub=r.w*r.h>3.5; return (tub?rect(x+m*.4,y+m*.4,w-m*.8,S*.75,C.white,10,sh)+rect(x+m*.6,y+m*.55,w-m*1.2,S*.48,C.glass,10):rect(x+w-m*.4-S*.9,y+m*.4,S*.9,S*.9,"#eef3f5",2,sh))+`<ellipse cx="${x+m*.4+S*.25}" cy="${y+h-m*.4-S*.45}" rx="${S*.2}" ry="${S*.27}" fill="${C.white}" ${sh}/>`+rect(x+w-m*.4-S*.55,y+h-m*.4-S*.45,S*.55,S*.42,C.white,6,sh);}
    case "logia":return rect(x+m*.4,y+m*.4,S*.6,S*.6,C.white,6,sh)+`<circle cx="${x+m*.4+S*.3}" cy="${y+m*.4+S*.3}" r="${S*.2}" fill="none" stroke="${C.metal}" stroke-width="2"/>`;
    case "escalera":{let s="";const n=10;for(let i=0;i<n;i++)s+=`<line x1="${x+3}" y1="${y+h*i/n}" x2="${x+w-3}" y2="${y+h*i/n}" stroke="#a88d6e" stroke-width="1.4"/>`;return s+`<path d="M${x+w/2} ${y+h-6}V${y+8}M${x+w/2-6} ${y+16}L${x+w/2} ${y+8}L${x+w/2+6} ${y+16}" stroke="#3a3d3c" stroke-width="1.8" fill="none"/>`;}
    case "closet":case "walkin":case "bodega":return `<path d="M${x+6} ${y+6}L${x+w-6} ${y+h-6}M${x+w-6} ${y+6}L${x+6} ${y+h-6}" stroke="#b5aa98" stroke-width="1"/>`+(t==="walkin"?rect(x+m*.3,y+m*.3,w-m*.6,S*.5,C.wood2,2,sh):"");
    case "escritorio":return rect(x+m,y+m,S*1.4,S*.6,C.wood2,3,sh)+`<circle cx="${x+m+S*.7}" cy="${y+m+S*.95}" r="${S*.22}" fill="#3a3d3c" ${sh}/>`+rect(x+w-m-S*.4,y+m,S*.4,h-m*2,"#e8e6e1",2,sh);
    case "estar":return rect(x+m,y+h/2-S*.45,w-m*2,S*.9,C.rug,4)+rect(x+m,y+h-m-S*.7,Math.min(w-m*2,S*1.5),S*.7,C.sofa,6,sh)+plant(x+w-m-S*.2,y+m+S*.2);
    case "acceso":return rect(x+w*.55,y+m*.4,S*.9,S*.35,C.wood2,3,sh)+plant(x+w-m-S*.1,y+h-m-S*.1);
    case "quincho":return rect(x+m,y+m,S*1.4,S*.6,"#6b6e70",3,sh)+`<circle cx="${x+w-m-S*.9}" cy="${y+h/2}" r="${S*.55}" fill="#b39572" ${sh}/>`;
    case "terraza":return rect(x+m,y+m,S*.6,S*.6,C.white,8,sh)+rect(x+m+S*.8,y+m,S*.6,S*.6,C.white,8,sh)+plant(x+w-m-S*.2,y+h-m-S*.2);
    default:return "";
  }
}
window.SP_PLANOS={svgPlan,layout,PROG};
})();
