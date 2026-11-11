# Format OPSIS Originals v3 (à suivre pour toute réécriture)

Lis d'abord `docs/modeles/lustig.md` et `docs/modeles/nyos.md` : ce sont les deux modèles écrits par Hamza. Tu reproduis leur STRUCTURE, leur TON et leur RYTHME. Lis aussi `docs/STYLE_OPSIS.md` (principes, vérité, interdits), que ce document complète. Aucune recherche web : n'écris que ce dont tu es sûr.

## Structure obligatoire (JSON `data/opsis_v3/<id>.json`)

- `name` : titre en casse normale (≤ 44 caractères), jamais en majuscules. Les titres-promesses fonctionnent : « L'homme qui aurait vendu la tour Eiffel », « Le lac qui a tué sans faire de bruit ».
- `sub` : une phrase de repère : « Lieu, date — ce que l'histoire promet. » (110–200 caractères).
- `body` : liste de lignes.
  - `#PROLOGUE — Lieu, date` en premier : une scène ou un fait qui accroche.
  - 4 à 8 chapitres `#01 — TITRE EN MAJUSCULES`, `#02 — …` (au moins 2 en 3 min, 4 en 7 min, 7 en 12 min). Chaque titre est une promesse ou une image, pas un libellé scolaire.
  - `#ÉPILOGUE — Titre` en dernier : conclusion développée, qui laisse quelque chose en mémoire, sans répéter le récit.
  - Entre les intertitres : des paragraphes COURTS (8 à 28 mots en moyenne, parfois une seule phrase, parfois 40 à 60 mots pour une description). Beaucoup de blancs. Pas de pavés.
  - Une ligne commençant par `!` = phrase forte mise en exergue (le modèle les met en gras : « Il doit être démonté. », « Le danger était là depuis des années. Mais personne ne pouvait le voir. »). Une ou deux par histoire, jamais répétée dans le paragraphe voisin.
- `learned` : 3 à 6 puces « Ce que vous venez de découvrir » (commencent par un groupe nominal : « Le rôle de la honte dans le silence des victimes. »).
- `retain` : « À retenir », 1 à 2 phrases.
- `note` : note éditoriale : ce qui est reconstitué, ce qui reste incertain, ce qui n'est pas une citation authentique (2 à 4 phrases, honnête).
- `blurb` : `b` (45–70 mots, donne envie sans spoiler la fin), `h` (6–14 mots).
- `fmt` : 3, 7 ou 12 minutes selon ce que l'histoire mérite. 3 min ≈ 600 mots, 7 min ≈ 1 300–1 800, 12 min ≈ 2 300–2 800. Choisis la durée qui sert l'histoire, ne brode jamais pour remplir.
- `src` : omets-le (les sources existantes sont conservées).
- `notes` : (facultatif) pour moi : tes doutes factuels.

## Le ton (ce que font les modèles)

- Phrases simples, courtes, rythmées. Beaucoup de phrases d'une ligne qui font tomber l'information : « Il doit être démonté. » « Pas de bombardement. Pas d'épidémie. »
- Accessible : aucune connaissance préalable. Les notions complexes passent par une image concrète au moment où elles servent (« Imagine une bouteille de soda fermée. »).
- Chaque chapitre finit sur une relance qui donne envie du suivant (« Mais l'histoire n'est pas terminée. Car il envisage de recommencer. »).
- Le lecteur comprend POURQUOI : mécanismes, psychologie, enjeux, pas seulement QUOI.
- Pas de dates en liste, pas de ton fiche, pas de références dans le texte (« selon… » interdit), pas de dialogues inventés présentés comme réels.
- Reconstitutions : au conditionnel ou en discours indirect ; tout ce qui pourrait passer pour un fait établi sans l'être est dit simplement dans le texte ou dans la `note`.

## Procédure

`python3 tools/v2_show.py <id>` pour lire la version actuelle (matière première, à restructurer et réécrire dans ce ton ; garde les faits solides, retire ce qui est douteux). Écris `data/opsis_v3/<id>.json`, puis `python3 tools/v3_check.py <id>` jusqu'à OK. Écris chaque fichier tout de suite.
