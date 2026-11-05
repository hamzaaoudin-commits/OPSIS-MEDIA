# OPSIS — fondations techniques

Ce document décrit comment l'application est construite et ce qu'il faut faire pour la brancher sur un vrai serveur.

## Ce qui a changé

| Avant | Maintenant |
|---|---|
| Une seule page de 5,6 Mo qui contient les 582 histoires, les couvertures et le code | Un code léger (≈ 240 Ko) + des données dans `data/` : `content.json` (histoires) et `covers.json` (couvertures) |
| Ajouter une histoire = modifier le code et republier | Histoires du jour publiées depuis une base de données, visibles dans l'app sans mise à jour |
| Rien n'était mémorisé | Lectures, liste, réglages et série de jours sauvegardés sur l'appareil, et synchronisés entre appareils avec un compte |
| « Notification chaque matin » décorative | Vraie notification quotidienne programmée sur l'appareil |

```
src/shell.html       l'application (interface)
src/runtime/*.js     contenu · sauvegarde · comptes · synchro · notifications · écran Compte
data/                les histoires et les couvertures (source de vérité de l'instantané)
supabase/0001_init.sql   le schéma de la base
tools/build.js       assemble app.html (autonome) et app/ (à déployer)
tools/dev-server.js  serveur local qui simule Supabase (pour tout tester sans compte)
tools/seed.js        charge les histoires dans Supabase
tests/e2e.js         40 vérifications de bout en bout
```

`node tools/build.js` produit :
- `app.html` : version autonome (données embarquées), s'ouvre sans serveur, pour l'aperçu.
- `app/` : version à déployer (`index.html` léger, `data/`, `sw.js`, `manifest.webmanifest`, icônes).

## Comment le contenu arrive dans l'app

1. L'app démarre avec un **instantané** (fichiers `data/*.json`, mis en cache par le service worker). Elle fonctionne donc toujours, même sans réseau, même au premier lancement.
2. Si Supabase est configuré, elle demande à la base **uniquement ce qui a changé depuis l'instantané** (`sync_at > curseur`), puis garde le résultat en cache local (IndexedDB). Une journée normale = quelques Ko.
3. Une histoire datée dans le futur (`published_at`) est **invisible** : la base elle-même la refuse (règle de sécurité RLS).

### Publier une histoire du jour

Dans Supabase, table `stories`, ajouter une ligne :

| colonne | valeur |
|---|---|
| `id` | `dj001` (unique) |
| `series` | `dj` (série « histoire du jour ») |
| `pos` | 1, 2, 3… |
| `published_at` | la date et l'heure de publication, ex. `2027-01-04 05:00+00` |
| `data` | `{"id":"dj001","name":"Titre","sub":"Accroche","dates":"1925","country":"Paris","terr":"Arnaques","c":"#E8B04A","body":["Paragraphe…","!Paragraphe de retournement","*","#Intertitre"],"src":"Sources…"}` |
| `cover` | (facultatif) le SVG de la couverture. Sans couverture, l'app en génère une aux couleurs du thème (`c`). |

Dès `published_at`, l'histoire devient **la une de l'accueil** et entre dans « Cette semaine ». Pour la rédaction : préfixes de paragraphes `!` (retournement), `#` (intertitre), `@` (lieu/date), `*` (ornement).

### Corriger une histoire existante
Modifier la ligne (`data`) : la correction part chez tous les utilisateurs à leur prochaine ouverture.

### Limite à connaître
Les 19 séries existantes ont chacune **30 places** (6 groupes de 5) définies dans l'interface. On peut donc corriger leurs histoires à distance, mais pas en ajouter : les nouveautés passent par la série `dj`. Créer de nouvelles séries à distance demande de rendre l'interface des séries dynamique (chantier distinct).

## Mise en route de Supabase (≈ 30 minutes)

1. Créer un projet sur supabase.com (région **Europe**, par ex. Paris ou Francfort). Plan gratuit suffisant pour démarrer.
2. **SQL Editor** → coller `supabase/0001_init.sql` → *Run*.
3. **Authentication → Providers** :
   - *Email* : activé. **Authentication → Email Templates → Magic Link** : remplacer le contenu pour qu'il affiche le code, par ex. `Votre code OPSIS : {{ .Token }}`. (L'app demande un code à 6 chiffres.)
   - *Google* : créer des identifiants OAuth sur Google Cloud Console, coller client id / secret.
   - *Apple* : Apple Developer → Services ID + clé « Sign in with Apple », coller dans Supabase. **Obligatoire sur l'App Store dès qu'on propose Google.**
   - **URL Configuration** : *Site URL* = l'adresse de l'app ; ajouter l'adresse de l'app dans *Redirect URLs*.
4. Copier `opsis.config.example.json` en `opsis.config.json`, renseigner `supabaseUrl` et `supabaseAnonKey` (**Project Settings → API**, clé « anon / publishable »). Cette clé est publique par conception : la sécurité repose sur les règles RLS du fichier SQL.
5. Charger les histoires : `SUPABASE_URL=… SUPABASE_SERVICE_KEY=… node tools/seed.js`. La clé **service_role** reste sur votre ordinateur, jamais dans l'app.
6. `node tools/build.js` puis déployer le dossier `app/` (par ex. Vercel : *Root Directory* = `app`).

Tester en local sans Supabase : `npm run dev` ouvre l'app sur http://localhost:8787/ avec un faux Supabase intégré (code e-mail : `123456`).

## Comptes et synchronisation

- Connexion : e-mail + code à 6 chiffres, Google, Apple (web par redirection).
- **Apple et Google dans l'app native** : il faut un plugin Capacitor qui renvoie un jeton d'identité, à passer à `OPSIS.auth.signInWithIdToken('apple', token, nonce)` (déjà prévu côté app et côté serveur). À faire au moment de l'emballage natif.
- Principe de synchro : chaque information (`read.ar01`, `saved.cs03`, `set.fs`, `day.2027-01-04`…) est horodatée ; la fusion se fait **dans la base** (`merge_user_state`), la valeur la plus récente gagne. Deux téléphones ne s'écrasent jamais ; retirer un favori sur l'un le retire sur l'autre.
- **Série de jours** : un jour compte dès qu'une histoire est terminée ; la série tient jusqu'au lendemain soir ; le record est conservé.
- **Suppression du compte** dans Réglages (exigence de l'App Store) : efface le compte et les données synchronisées.
- Se déconnecter vide l'état local de l'appareil (appareil partagé) ; tout est dans le compte.

## Notifications

- **App native (Capacitor)** : à chaque ouverture, l'app programme sur l'appareil les **14 prochains jours** de notifications locales à l'heure choisie (6/7/8 h). Aucun serveur, ça marche hors ligne. L'autorisation est demandée à la **première histoire terminée** (pas au lancement), et le réglage se coupe si elle est refusée.
  Plugin requis : `@capacitor/local-notifications`.
- Texte : teaser publié à l'avance (`content_meta`, clé `SCHEDULE`, `{"2027-01-04":"…"}`), sinon le titre de l'histoire déjà publiée ce jour-là, sinon « Votre histoire du jour est arrivée. » (l'appareil ne peut pas connaître le titre de demain, qui n'est pas encore publié.)
- Avant le 4 janvier 2027 : une seule notification, le jour du lancement.
- **Pas fait** : le push à distance (serveur → téléphone) pour une notification avec le titre exact publié à la dernière minute, ou pour la version web installée (PWA). Cela demande Firebase Cloud Messaging / APNs ou Web Push + une fonction planifiée. Les notifications locales couvrent le besoin du lancement.

## Tests

`npm install` (une fois) puis `npm test` : lance l'app contre le serveur local et vérifie 40 points : démarrage, sauvegarde, série de jours, connexion, synchro entre deux appareils, résolution de conflit, suppression de compte, contenu publié à distance, mode hors ligne, notifications, service worker.
