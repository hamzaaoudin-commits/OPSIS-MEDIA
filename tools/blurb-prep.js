// Prépare les lots de quatrièmes de couverture : data/blurb_todo/batchNN.txt
const fs=require('fs');const c=require('../data/content.json');
const src=fs.readFileSync(__dirname+'/../src/shell.html','utf8');
const GONE=eval('('+src.match(/var GONE=(\{[^}]*\})/)[1]+')');
const items=[];
for(const k of Object.keys(c.D)){for(const s of c.D[k]){if(GONE[s.id]||!s.body||!s.body.length)continue;items.push({id:s.id,name:s.name,sub:s.sub,meta:[s.dates,s.country,s.job].filter(Boolean).join(' · '),body:s.body});}}
if(c.BOOK&&c.BOOK.portraits)for(const p of c.BOOK.portraits)items.push({id:p.id,name:p.name,sub:p.sub,meta:[p.dates,p.country,p.job].filter(Boolean).join(' · '),body:p.body});
function text(b){return b.filter(t=>!/^[#@!*]/.test(t)).join(' ').replace(/\s+/g,' ');}
function brief(it){const w=text(it.body).split(' ');const head=w.slice(0,420).join(' ');const tail=w.length>520?'[…] '+w.slice(-110).join(' '):'';
 return `=== ${it.id} ===\nTITRE : ${it.name}\nCOURTE LIGNE ACTUELLE : ${it.sub}\nREPÈRES : ${it.meta}\nTEXTE (début) : ${head}\n${tail?'TEXTE (fin) : '+tail+'\n':''}`;}
const N=+process.argv[2]||38;let n=0;
for(let i=0;i<items.length;i+=N){n++;const f=`data/blurb_todo/batch${String(n).padStart(2,'0')}.txt`;fs.writeFileSync(f,items.slice(i,i+N).map(brief).join('\n'));}
console.log(items.length,'histoires,',n,'lots');
