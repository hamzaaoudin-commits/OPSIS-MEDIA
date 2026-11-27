/* Vérifie que tout est renseigné avant d'envoyer l'app aux boutiques. Usage : npm run check */
const fs=require('fs'),path=require('path');
const c=JSON.parse(fs.readFileSync(path.join(__dirname,'..','native.config.json'),'utf8'));
const checks=[
 ['supabaseUrl',/^https:\/\/[a-z0-9]+\.supabase\.co$/,'URL du projet Supabase (https://xxxx.supabase.co)'],
 ['supabaseAnonKey',/^eyJ|^sb_publishable_/,'clé publique « anon » de Supabase'],
 ['revenueCatIosKey',/^appl_/,'clé publique RevenueCat iOS (appl_…)'],
 ['revenueCatAndroidKey',/^goog_/,'clé publique RevenueCat Android (goog_…)'],
 ['googleWebClientId',/\.apps\.googleusercontent\.com$/,'ID client Google « Application Web »'],
 ['googleIosClientId',/\.apps\.googleusercontent\.com$/,'ID client Google « iOS »']];
let bad=0;
for(const [k,re,d] of checks){const v=(c[k]||'').trim();if(!v){console.log('✗ manquant  '+k+' — '+d);bad++;}else if(!re.test(v)){console.log('✗ invalide  '+k+' — attendu : '+d);bad++;}else console.log('✓ '+k);}
if(c.entitlementId!=='premium'){console.log('! entitlementId = '+c.entitlementId+' (doit correspondre à RevenueCat)');}
const gr=fs.readFileSync(path.join(__dirname,'..','android/app/build.gradle'),'utf8').match(/versionCode (\d+)/);console.log('versionCode Android :',gr&&gr[1],'(à augmenter à chaque envoi)');
const ks=fs.existsSync(path.join(__dirname,'..','android/keystore.properties'));console.log(ks?'✓ keystore.properties présent':'✗ android/keystore.properties absent (signature du fichier Android)');if(!ks)bad++;
console.log(bad?'\n'+bad+' point(s) à régler avant publication.':'\nPrêt pour la publication.');process.exit(bad?1:0);
