const fs=require('fs');const p=__dirname+'/../data/';
const c=JSON.parse(fs.readFileSync(p+'content.json','utf8'));
const out={};const bad=[];
for(const f of fs.readdirSync(p+'blurb_src').filter(f=>f.endsWith('.json')).sort()){
  const j=JSON.parse(fs.readFileSync(p+'blurb_src/'+f,'utf8'));
  for(const [id,v] of Object.entries(j)){
    const b=(v.blurb||'').trim(),h=(v.hook||'').trim();
    const wb=b.split(/\s+/).length,wh=h.split(/\s+/).length;
    const prob=[];
    if(wb<35||wb>85)prob.push('blurb '+wb+' mots');
    if(wh<4||wh>18)prob.push('hook '+wh+' mots');
    if(/…|\.\.\./.test(b+h))prob.push('points de suspension');
    if(/selon les sources|cette histoire|ce récit|incroyable|vous ne devinerez/i.test(b+h))prob.push('formule interdite');
    if(/^[^.:]{3,40}, \d{3,4} ?:/.test(b))prob.push('commence par lieu:date');
    if(prob.length)bad.push(id+' ['+f+'] '+prob.join(', '));
    out[id]={b,h};
  }
}
c.BLURB=out;fs.writeFileSync(p+'content.json',JSON.stringify(c));
console.log(Object.keys(out).length,'quatrièmes fusionnées;',bad.length,'à revoir');bad.forEach(x=>console.log(' -',x));
