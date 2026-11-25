#!/usr/bin/env node
/* Vérifie qu'un projet Supabase est prêt pour OPSIS (comptes + synchro), sans clé secrète :
   node tools/check-backend.js            (lit opsis.config.json)
   node tools/check-backend.js URL CLE    (ou en arguments)                                   */
const fs = require('fs');
let url = process.argv[2], key = process.argv[3];
if (!url) { try { const c = JSON.parse(fs.readFileSync(__dirname + '/../opsis.config.json', 'utf8')); url = c.supabaseUrl; key = c.supabaseAnonKey; } catch (e) {} }
if (!url || !key || /VOTRE-PROJET/.test(url)) { console.log('Renseignez supabaseUrl et supabaseAnonKey dans opsis.config.json (voir docs/BACKEND.md, étape 4).'); process.exit(2); }
url = url.replace(/\/$/, '');
const H = { apikey: key, Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' };
let ko = 0;
const line = (ok, msg, hint) => { if (!ok) ko++; console.log((ok ? '  ok  ' : '  KO  ') + msg + (!ok && hint ? '\n        → ' + hint : '')); };
async function get(p, o) { const r = await fetch(url + p, Object.assign({ headers: H }, o || {})); let j = null; try { j = await r.json(); } catch (e) {} return { s: r.status, j }; }
(async () => {
  console.log('Projet : ' + url);
  let st;
  try { st = await get('/auth/v1/settings'); } catch (e) { console.log('  KO  projet injoignable : ' + e.message); process.exit(1); }
  line(st.s === 200, 'API d’authentification joignable', 'vérifiez l’adresse et la clé anon');
  const ext = (st.j && st.j.external) || {};
  line(ext.email !== false && !(st.j && st.j.disable_signup), 'Inscription par e-mail (code à 6 chiffres) activée', 'Authentication → Providers → Email, et « Allow new users to sign up »');
  line(!!ext.google, 'Connexion Google activée', 'Authentication → Providers → Google (client id + secret Google Cloud)');
  line(!!ext.apple, 'Connexion Apple activée', 'Authentication → Providers → Apple (Services ID + clé Sign in with Apple). Obligatoire sur l’App Store dès que Google est proposé');
  const sr = await get('/rest/v1/stories?select=id&limit=1');
  line(sr.s === 200, 'Table stories lisible (règle RLS : seules les histoires publiées)', 'exécutez supabase/0001_init.sql dans le SQL Editor');
  const us = await get('/rest/v1/user_state?select=*&limit=1');
  line(us.s === 401 || us.s === 403 || (us.s === 200 && Array.isArray(us.j) && us.j.length === 0), 'user_state fermée aux visiteurs anonymes', 'la règle RLS state_own doit exister');
  const mu = await get('/rest/v1/rpc/merge_user_state', { method: 'POST', body: JSON.stringify({ p: {} }) });
  line(mu.s === 401 || mu.s === 403, 'merge_user_state refusée sans compte', 'revoke/grant de la fonction dans 0001_init.sql');
  const dm = await get('/rest/v1/rpc/delete_my_account', { method: 'POST', body: '{}' });
  line(dm.s === 401 || dm.s === 403, 'delete_my_account refusée sans compte', 'revoke/grant de la fonction dans 0001_init.sql');
  console.log(ko ? '\n' + ko + ' point(s) à corriger.' : '\nTout est prêt : comptes et synchronisation peuvent être activés.');
  process.exit(ko ? 1 : 0);
})();
