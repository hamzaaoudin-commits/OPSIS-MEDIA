/* Fusionne data/lens_src/<id>.json ({"3":[…],"5":[…],"10":[…]}) dans data/content.json (LENS). */
var fs=require('fs'),path=require('path');
var root=path.join(__dirname,'..'),cf=path.join(root,'data/content.json'),dir=path.join(root,'data/lens_src');
var C=JSON.parse(fs.readFileSync(cf,'utf8'));
var ids={};Object.keys(C.D).forEach(function(k){C.D[k].forEach(function(s){ids[s.id]=1;});});
var words=function(a){return a.reduce(function(n,x){return /^[#@*]/.test(x)?n:n+x.split(/\s+/).length;},0);};
var n=0,bad=0;
fs.readdirSync(dir).filter(function(f){return /\.json$/.test(f);}).forEach(function(f){
  var id=f.replace('.json',''),v=JSON.parse(fs.readFileSync(path.join(dir,f),'utf8'));
  if(!ids[id]){console.log('INCONNU',id);bad++;return;}
  var w={};
  ['3','5','10'].forEach(function(k){
    if(!Array.isArray(v[k])||v[k].some(function(x){return typeof x!=='string'||!x;})){console.log('FORMAT',id,k);bad++;return;}
    w[k]=words(v[k]);
  });
  if(!(w['3']<w['5']&&w['5']<w['10'])){console.log('ORDRE',id,JSON.stringify(w));bad++;}
  C.LENS[id]=v;n++;
  console.log(id,JSON.stringify(w));
});
if(bad){console.log('ERREURS',bad);process.exit(1);}
fs.writeFileSync(cf,JSON.stringify(C));
console.log('fusionné',n);
