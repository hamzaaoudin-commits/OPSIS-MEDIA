# Publier une histoire du jour (sans mise à jour de l'app)

1. Écrire l'histoire (voir `docs/STYLE_OPSIS_V4.md`) dans un fichier JSON :
   `{ "id":"dj001", "name":"Titre", "sub":"Accroche", "dates":"1925", "country":"Paris", "terr":"Destins", "c":"#E8B04A", "published_at":"2027-01-04T05:00:00Z", "src":"sources", "body":["@Lieu, date","paragraphe","!retournement","#intertitre"] }`
   (ids `dj001`, `dj002`… ; `terr` = un des thèmes existants ; 600 mots minimum.)
2. `node tools/publish.js histoire.json` — contrôle le format puis ajoute l'histoire à `data/feed.json` (`--replace` pour corriger une histoire déjà publiée).
3. `node tools/build.js`, puis déployer `app/` (copie dans `opsis-app`, push → Vercel). Une minute plus tard, `…/data/feed.json` contient l'histoire.
4. L'app (web et stores) la lit au prochain lancement et l'affiche **à partir de `published_at`** : à cette heure elle devient la une de l'accueil. Une histoire datée dans le futur reste invisible dans l'app, mais le fichier est public : ne l'ajoute que le jour même ou la veille si le secret compte.

Corriger une histoire existante : même flux, avec `series` et `id` d'origine (voir `docs/BACKEND.md` pour les lignes complètes). Retirer : `"status":"archived"`.
