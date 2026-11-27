/* Applique native.config.json aux fichiers natifs (Info.plist : connexion Google iOS). Lancé par `npm run sync`. */
const fs=require('fs'),path=require('path');
const cfg=JSON.parse(fs.readFileSync(path.join(__dirname,'..','native.config.json'),'utf8'));
const p=path.join(__dirname,'..','ios/App/App/Info.plist');let s=fs.readFileSync(p,'utf8');
s=s.replace(/\t?<!-- OPSIS-GOOGLE -->[\s\S]*?<!-- \/OPSIS-GOOGLE -->\n/,'');
const id=(cfg.googleIosClientId||'').trim();
if(id){
  const m=id.match(/^(\d+-[a-z0-9]+)\.apps\.googleusercontent\.com$/i);
  if(!m){console.error('googleIosClientId invalide (attendu : xxx.apps.googleusercontent.com)');process.exit(1);}
  const rev='com.googleusercontent.apps.'+m[1];
  s=s.replace('</dict>\n</plist>','\t<!-- OPSIS-GOOGLE -->\n\t<key>GIDClientID</key>\n\t<string>'+id+'</string>\n\t<key>CFBundleURLTypes</key>\n\t<array>\n\t\t<dict>\n\t\t\t<key>CFBundleURLSchemes</key>\n\t\t\t<array>\n\t\t\t\t<string>'+rev+'</string>\n\t\t\t</array>\n\t\t</dict>\n\t</array>\n\t<!-- /OPSIS-GOOGLE -->\n</dict>\n</plist>');
  console.log('Info.plist : connexion Google iOS configurée');
}else console.log('Info.plist : pas de googleIosClientId (connexion Google iOS non configurée)');
fs.writeFileSync(p,s);
