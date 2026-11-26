#!/usr/bin/env node
/* OPSIS — pages de partage publiques (couverture + quatrième de couverture + invitation à lire dans l'app).
     node tools/build.js && node tools/share-pages.js
   Produit app/s/<id>/index.html et app/s/og/<id>.jpg (aperçu 1200×630 pour Instagram, WhatsApp, iMessage…).
   Aucune ligne du texte de l'histoire n'est publiée : seulement titre, couverture et quatrième de couverture. */
const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const BASE=process.env.OPSIS_BASE||'https://opsis-alpha.vercel.app';
const root=path.join(__dirname,'..'),out=path.join(root,'app/s');
const esc=t=>String(t==null?'':t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
(async()=>{
  const b=await chromium.launch(),p=await b.newPage({viewport:{width:1200,height:630}});
  await p.goto('file://'+path.join(root,'app.html'));await p.waitForTimeout(2000);
  const list=await p.evaluate(()=>{const S=OPSIS.stories(),o=[];Object.keys(S).forEach(id=>{const s=S[id];if(OPSIS.ui.vis(id))o.push({id,title:s.title,kind:s.kind||'',min:s.min,series:s.series||'',terr:s.terr||'',sub:s.sub||''});});return o;});
  const content=JSON.parse(fs.readFileSync(path.join(root,'data/content.json'),'utf8')),covers=JSON.parse(fs.readFileSync(path.join(root,'data/covers.json'),'utf8'));
  fs.rmSync(out,{recursive:true,force:true});fs.mkdirSync(path.join(out,'og'),{recursive:true});
  const css=fs.readFileSync(path.join(root,'src/fonts.css'),'utf8').replace(/url\(fonts\//g,'url(/fonts/');
  const tpl=(s,blurb,og)=>`<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>${esc(s.title)} · OPSIS</title>
<meta name="description" content="${esc(blurb.slice(0,200))}"><meta name="theme-color" content="#09090A">
<meta property="og:type" content="article"><meta property="og:site_name" content="OPSIS"><meta property="og:title" content="${esc(s.title)}"><meta property="og:description" content="${esc(blurb.slice(0,200))}"><meta property="og:image" content="${BASE}/s/og/${s.id}.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg"><style>${css}
*{box-sizing:border-box;margin:0}body{background:#09090A;color:#EDE6DA;font-family:'Hanken Grotesk',system-ui,sans-serif;min-height:100vh;-webkit-font-smoothing:antialiased;background-image:radial-gradient(100% 60% at 80% 0,#3b0a10,#09090A 70%)}
.w{max-width:520px;margin:0 auto;padding:28px 22px 44px;display:flex;flex-direction:column;gap:22px}.logo{font:800 22px 'Big Shoulders Display',Impact,sans-serif;letter-spacing:3px}
.cv{width:62%;max-width:280px;aspect-ratio:2/3;border-radius:10px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.6);align-self:center}.cv svg{width:100%;height:100%;display:block}
.k{font:700 12px/1 'Hanken Grotesk',sans-serif;letter-spacing:2.2px;color:#F04A50}h1{font:800 clamp(40px,12vw,58px)/.95 'Big Shoulders Display',Impact,sans-serif;text-transform:uppercase;margin-top:10px}
.m{color:#A39E95;font-size:14px;margin-top:10px}.b{font:400 19px/1.55 'Newsreader',Georgia,serif;color:#d8d2c7}
.cta{display:block;text-align:center;background:#D2232C;color:#fff;text-decoration:none;font-weight:700;font-size:17px;padding:17px;border-radius:14px}.n{color:#A39E95;font-size:13px;text-align:center;line-height:1.5}</style></head>
<body><div class="w"><div class="logo">OPSIS</div><div class="cv">${covers[s.id]||''}</div>
<div><p class="k">${esc((s.series||s.kind).toUpperCase())}</p><h1>${esc(s.title)}</h1><p class="m">${esc(s.kind)}${s.min?' · '+s.min+' min de lecture':''}</p></div>
<p class="b">${esc(blurb)}</p><a class="cta" id="cta" href="/#h=${encodeURIComponent(s.id)}">Lire cette histoire dans l'app</a>
<p class="n" id="nn">OPSIS · The world is made of stories.<br>L'histoire complète se lit dans l'application.</p></div>
<script>if(/[?&]cadeau=1/.test(location.search)){var c=document.getElementById('cta');c.href+='&cadeau=1';c.textContent="Lire l'histoire offerte";document.getElementById('nn').innerHTML="Cette histoire vous est offerte.<br>Elle se lit directement ici, sans compte et sans rien télécharger.";}</script></body></html>`;
  let n=0;
  for(const s of list){
    const bl=(content.BLURB&&content.BLURB[s.id]&&content.BLURB[s.id].b)||s.sub||'Une histoire vraie à lire dans OPSIS.';
    const d=path.join(out,s.id);fs.mkdirSync(d,{recursive:true});
    fs.writeFileSync(path.join(d,'index.html'),tpl(s,bl));
    /* image d'aperçu : couverture à gauche, titre à droite */
    const tmp=path.join(out,'og','_t.html');fs.writeFileSync(tmp,`<style>${css.replace(/url\(\/fonts\//g,'url(../../fonts/')}*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;background:radial-gradient(90% 100% at 85% 0,#4a0c12,#09090A 70%);color:#EDE6DA;display:flex;align-items:center;gap:56px;padding:0 90px;font-family:'Hanken Grotesk',sans-serif}.cv{flex:none;width:300px;height:450px;border-radius:12px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.6)}.cv svg{width:100%;height:100%;display:block}.k{font:700 20px 'Hanken Grotesk';letter-spacing:4px;color:#F04A50}h1{font:800 92px/.95 'Big Shoulders Display',Impact,sans-serif;text-transform:uppercase;margin-top:18px}.o{font:800 34px 'Big Shoulders Display',Impact,sans-serif;letter-spacing:5px;margin-top:34px;color:#A39E95}</style><div class="cv">${covers[s.id]||''}</div><div><p class="k">${esc((s.series||s.kind).toUpperCase())}</p><h1>${esc(s.title.length>60?s.title.slice(0,57)+'…':s.title)}</h1><p class="o">OPSIS</p></div>`);await p.goto('file://'+tmp);
    await p.evaluate(()=>document.fonts.ready);
    await p.screenshot({path:path.join(out,'og',s.id+'.jpg'),type:'jpeg',quality:82});n++;
  }

  /* parcours et collections : page de partage + aperçu */
  await p.goto('file://'+path.join(root,'app.html'));await p.waitForTimeout(2000);
  const lists=await p.evaluate(()=>OPSIS.ui.lists());
  const byId={};list.forEach(s=>byId[s.id]=s);
  const items=[].concat(lists.paths.map(x=>({...x,kind:'p'})),lists.cols.map(x=>({...x,kind:'c'})));
  const tpl2=(it)=>{const id=it.kind+'-'+it.k,lab=it.kind==='p'?'Parcours de découverte':'Collection',ids=it.ids.filter(x=>byId[x]),mos=ids.slice(0,3).map((x,i)=>`<div class="m m${i}">${covers[x]||''}</div>`).join('');
    const rows=ids.map((x,i)=>`<li><b>${i+1}</b><span>${esc(byId[x].title)}</span><i>${byId[x].min} min</i></li>`).join('');
    const desc=(it.d||'').slice(0,200)||ids.length+' histoires vraies à lire dans OPSIS.';
    return `<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>${esc(it.n)} · OPSIS</title>
<meta name="description" content="${esc(desc)}"><meta name="theme-color" content="#09090A">
<meta property="og:type" content="article"><meta property="og:site_name" content="OPSIS"><meta property="og:title" content="${esc(it.n)}"><meta property="og:description" content="${esc(desc)}"><meta property="og:image" content="${BASE}/s/og/${id}.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg"><style>${css}
*{box-sizing:border-box;margin:0}body{background:#09090A;color:#EDE6DA;font-family:'Hanken Grotesk',system-ui,sans-serif;min-height:100vh;-webkit-font-smoothing:antialiased;background-image:radial-gradient(120% 60% at 50% 0,#3a0a10,#09090A 65%)}
.w{max-width:520px;margin:0 auto;padding:28px 22px 44px;display:flex;flex-direction:column;gap:22px}.logo{font:800 22px 'Big Shoulders Display',Impact,sans-serif;letter-spacing:3px}
.fan{position:relative;height:250px}.m{position:absolute;top:0;width:36%;aspect-ratio:2/3;border-radius:9px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.6)}.m svg{width:100%;height:100%;display:block}.m0{left:9%;transform:rotate(-8deg) translateY(14px)}.m1{left:32%;z-index:2}.m2{right:9%;transform:rotate(8deg) translateY(14px)}
.k{font:700 12px/1 'Hanken Grotesk',sans-serif;letter-spacing:2.2px;color:#F04A50}h1{font:800 clamp(40px,12vw,58px)/.95 'Big Shoulders Display',Impact,sans-serif;text-transform:uppercase;margin-top:10px}
.b{font:400 18px/1.55 'Newsreader',Georgia,serif;color:#d8d2c7}ol{list-style:none;padding:0;border-top:1px solid #26242a}li{display:flex;gap:12px;align-items:baseline;padding:11px 0;border-bottom:1px solid #26242a;font-size:15px}li b{width:22px;color:#F04A50;font-weight:700}li span{flex:1}li i{font-style:normal;color:#A39E95;font-size:13px}
.cta{display:block;text-align:center;background:#D2232C;color:#fff;text-decoration:none;font-weight:700;font-size:17px;padding:17px;border-radius:14px}.n{color:#A39E95;font-size:13px;text-align:center;line-height:1.5}</style></head>
<body><div class="w"><div class="logo">OPSIS</div><div class="fan">${mos}</div>
<div><p class="k">${lab.toUpperCase()} · ${ids.length} HISTOIRES</p><h1>${esc(it.n)}</h1></div><p class="b">${esc(it.d||'')}</p><ol>${rows}</ol>
<a class="cta" href="/#${it.kind}=${encodeURIComponent(it.k)}">${it.kind==='p'?'Commencer ce parcours dans l\'app':'Découvrir cette collection dans l\'app'}</a>
<p class="n">OPSIS · The world is made of stories.<br>Les histoires se lisent dans l'application.</p></div></body></html>`;};
  for(const it of items){
    const id=it.kind+'-'+it.k,d=path.join(out,id);fs.mkdirSync(d,{recursive:true});fs.writeFileSync(path.join(d,'index.html'),tpl2(it));
    const ids=it.ids.filter(x=>byId[x]).slice(0,3),tmp=path.join(out,'og','_t.html');
    fs.writeFileSync(tmp,`<style>${css.replace(/url\(\/fonts\//g,'url(../../fonts/')}*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;background:radial-gradient(90% 100% at 85% 0,#4a0c12,#09090A 70%);color:#EDE6DA;display:flex;align-items:center;gap:40px;padding:0 80px;font-family:'Hanken Grotesk',sans-serif}.fan{position:relative;flex:none;width:430px;height:470px}.m{position:absolute;top:30px;width:210px;height:315px;border-radius:12px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.6)}.m svg{width:100%;height:100%;display:block}.m0{left:0;transform:rotate(-9deg) translateY(36px)}.m1{left:110px;z-index:2;top:10px}.m2{left:220px;transform:rotate(9deg) translateY(36px)}.k{font:700 20px 'Hanken Grotesk';letter-spacing:4px;color:#F04A50}h1{font:800 84px/.95 'Big Shoulders Display',Impact,sans-serif;text-transform:uppercase;margin-top:18px}.o{font:800 34px 'Big Shoulders Display',Impact,sans-serif;letter-spacing:5px;margin-top:30px;color:#A39E95}</style><div class="fan">${ids.map((x,i)=>`<div class="m m${i}">${covers[x]||''}</div>`).join('')}</div><div><p class="k">${it.kind==='p'?'PARCOURS':'COLLECTION'} · ${it.ids.length} HISTOIRES</p><h1>${esc(it.n.length>56?it.n.slice(0,53)+'…':it.n)}</h1><p class="o">OPSIS</p></div>`);
    await p.goto('file://'+tmp);await p.evaluate(()=>document.fonts.ready);
    await p.screenshot({path:path.join(out,'og',id+'.jpg'),type:'jpeg',quality:82});n++;
  }
  fs.rmSync(path.join(out,'og','_t.html'),{force:true});
  console.log('pages de partage :',n);await b.close();
})();
