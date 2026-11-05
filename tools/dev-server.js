#!/usr/bin/env node
/* OPSIS — serveur de développement.
   Sert l'application et simule la partie de Supabase dont elle se sert (contenu, comptes, synchro),
   avec les mêmes routes et les mêmes règles. Permet de tester tout le parcours sans compte Supabase.
     node tools/dev-server.js [port]         (ouvre http://localhost:8787/ )
   Code de connexion e-mail : 123456 (affiché dans la console). Dev uniquement. */
const http=require('http'),fs=require('fs'),path=require('path'),crypto=require('crypto'),url=require('url');
const root=path.join(__dirname,'..');
const PORT=+process.argv[2]||+process.env.PORT||8787;
const SERIES=['ar','cs','fa','pa','sv','cb','ev','im','es','pn','ex','ce','fi','di','pr','ld','vc','du','tm'];
const content=JSON.parse(fs.readFileSync(path.join(root,'data/content.json'),'utf8'));
const covers=JSON.parse(fs.readFileSync(path.join(root,'data/covers.json'),'utf8'));
const builtAt=content.builtAt;
const iso=t=>new Date(t).toISOString();
/* base de contenu : mêmes lignes que celles produites par tools/seed.js */
const stories=new Map();
SERIES.forEach(s=>{(content.D[s.toUpperCase()+'D']||[]).forEach((d,i)=>{stories.set(d.id,{id:d.id,series:s,pos:i,status:'live',data:d,lens:content.LENS[d.id]||null,cover:covers[d.id]||null,published_at:'2020-01-01T00:00:00Z',updated_at:builtAt,sync_at:builtAt});});});
const meta=new Map([['BOOK',{key:'BOOK',value:content.BOOK,updated_at:builtAt}],['BSRC',{key:'BSRC',value:content.BSRC,updated_at:builtAt}]]);
const users=new Map(),byEmail=new Map(),states=new Map();let code='123456';
const uid=e=>{const h=crypto.createHash('md5').update(e).digest('hex');return h.slice(0,8)+'-'+h.slice(8,12)+'-4'+h.slice(13,16)+'-a'+h.slice(17,20)+'-'+h.slice(20,32);};
const tok=(u,k)=>k+'.'+u.id+'.'+Date.now().toString(36)+Math.random().toString(36).slice(2,6);
const sessions=new Map();
function session(u){const a=tok(u,'at'),r=tok(u,'rt');sessions.set(a,u.id);sessions.set(r,u.id);return{access_token:a,refresh_token:r,expires_in:+process.env.TOKEN_TTL||3600,token_type:'bearer',user:{id:u.id,email:u.email}};}
function authUser(req){const m=(req.headers.authorization||'').match(/^Bearer (at\..+)$/);if(!m)return null;const id=sessions.get(m[1]);return id?users.get(id):null;}
const mime={'.html':'text/html; charset=utf-8','.json':'application/json','.js':'text/javascript','.png':'image/png','.svg':'image/svg+xml','.webmanifest':'application/manifest+json','.ico':'image/x-icon'};
function send(res,code_,body,type){res.writeHead(code_,{'Content-Type':type||'application/json','Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'*','Access-Control-Allow-Methods':'GET,POST,PATCH,DELETE,OPTIONS'});res.end(typeof body==='string'||Buffer.isBuffer(body)?body:JSON.stringify(body));}
const err=(res,c,m)=>send(res,c,{message:m,msg:m});
function readBody(req){return new Promise(r=>{let b='';req.on('data',d=>b+=d);req.on('end',()=>{try{r(b?JSON.parse(b):{});}catch(e){r({});}});});}
const num=s=>+String(s).replace(/[^0-9]/g,'')||0;
http.createServer(async(req,res)=>{
  const u=url.parse(req.url,true),p=u.pathname,q=u.query;
  if(req.method==='OPTIONS')return send(res,204,'');
  try{
  /* ---- AUTH ---- */
  if(p==='/auth/v1/otp'){const b=await readBody(req);if(!b.email)return err(res,422,'email requis');console.log('[dev] code pour',b.email,':',code);return send(res,200,{});}
  if(p==='/auth/v1/verify'){const b=await readBody(req);if(b.token!==code)return err(res,403,'Token has expired or is invalid');
    let usr=byEmail.get(b.email);if(!usr){usr={id:uid(b.email),email:b.email};users.set(usr.id,usr);byEmail.set(b.email,usr);}return send(res,200,session(usr));}
  if(p==='/auth/v1/token'){const b=await readBody(req);
    if(q.grant_type==='refresh_token'){const id=sessions.get(b.refresh_token);if(!id||!users.get(id))return err(res,400,'Invalid Refresh Token');return send(res,200,session(users.get(id)));}
    if(q.grant_type==='id_token'){const e=(b.provider||'x')+'@dev.local';let usr=byEmail.get(e);if(!usr){usr={id:uid(e),email:e};users.set(usr.id,usr);byEmail.set(e,usr);}return send(res,200,session(usr));}
    return err(res,400,'grant_type');}
  if(p==='/auth/v1/user'){const usr=authUser(req);return usr?send(res,200,{id:usr.id,email:usr.email}):err(res,401,'invalid JWT');}
  if(p==='/auth/v1/logout')return send(res,204,'');
  /* ---- CONTENU ---- */
  if(p==='/rest/v1/stories'){
    const gt=String(q.sync_at||'').replace(/^gt\./,'');const now=Date.now();
    let rows=[...stories.values()].filter(r=>Date.parse(r.published_at)<=now&&(!gt||r.sync_at>gt));
    rows.sort((a,b)=>a.sync_at<b.sync_at?-1:a.sync_at>b.sync_at?1:0);
    const off=+q.offset||0,lim=Math.min(+q.limit||1000,1000);return send(res,200,rows.slice(off,off+lim));}
  if(p==='/rest/v1/content_meta'){const gt=String(q.updated_at||'').replace(/^gt\./,'');return send(res,200,[...meta.values()].filter(m=>!gt||m.updated_at>gt));}
  /* ---- ÉTAT UTILISATEUR ---- */
  if(p==='/rest/v1/rpc/merge_user_state'){const usr=authUser(req);if(!usr)return err(res,401,'not authenticated');
    const b=await readBody(req),cur=states.get(usr.id)||{};
    Object.keys(b.p||{}).forEach(k=>{const v=b.p[k];if(v&&typeof v==='object'&&/^[0-9]+$/.test(String(v.t))&&(!(k in cur)||cur[k].t<v.t))cur[k]=v;});
    states.set(usr.id,cur);return send(res,200,cur);}
  if(p==='/rest/v1/rpc/delete_my_account'){const usr=authUser(req);if(!usr)return err(res,401,'not authenticated');
    states.delete(usr.id);users.delete(usr.id);byEmail.delete(usr.email);for(const[k,v]of sessions)if(v===usr.id)sessions.delete(k);return send(res,204,'');}
  /* ---- OUTILS DE TEST (dev uniquement) ---- */
  if(p==='/dev/publish'){const b=await readBody(req);const now=iso(Date.now());const r=Object.assign({status:'live',lens:null,cover:null,published_at:now,updated_at:now},b);r.sync_at=r.updated_at>r.published_at?r.updated_at:r.published_at;stories.set(r.id,r);return send(res,200,{ok:true,sync_at:r.sync_at});}
  if(p==='/dev/state'){return send(res,200,{users:[...users.values()],states:Object.fromEntries(states),stories:stories.size});}
  if(p==='/dev/code'){const b=await readBody(req);if(b.code)code=String(b.code);return send(res,200,{code});}
  /* ---- FICHIERS ---- */
  let f=p==='/'?'/index.html':p;
  let file=path.join(root,'app',f);
  if(f==='/app.html')file=path.join(root,'app.html');
  if(!file.startsWith(root)||!fs.existsSync(file)||fs.statSync(file).isDirectory()){res.writeHead(404);return res.end('404');}
  res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream','Cache-Control':'no-cache'});fs.createReadStream(file).pipe(res);
  }catch(e){console.error(e);err(res,500,String(e.message));}
}).listen(PORT,()=>console.log('OPSIS dev : http://localhost:'+PORT+'/  (code e-mail 123456)'));
