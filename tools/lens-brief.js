/* node tools/lens-brief.js <id> : affiche la fiche d'une histoire (métadonnées, sources, texte actuel). */
var C=require('../data/content.json'),id=process.argv[2];
Object.keys(C.D).forEach(function(k){C.D[k].forEach(function(s){if(s.id===id){
  console.log(JSON.stringify({id:s.id,titre:s.name,sous_titre:s.sub,dates:s.dates,pays:s.country,metier:s.job,sources:s.src},null,1));
  console.log('\nTEXTE ACTUEL ('+s.body.filter(function(x){return !/^[#@*]/.test(x)}).join(' ').split(/\s+/).length+' mots) :\n'+s.body.join('\n'));}});});
