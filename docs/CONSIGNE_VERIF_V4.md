# Consigne : vérification des faits (v4) — avec recherche web

Contexte. OPSIS publie des histoires vraies sur des personnes réelles (lancement le 4 janvier 2027). Les textes `data/opsis_v4/<id>.json` ont été réécrits SANS recherche web : des détails viennent de la mémoire d'un modèle. Ta mission : vérifier chaque histoire de ton lot contre des sources réelles, corriger, et documenter. Tu disposes de WebSearch (mode "standard") et WebFetch. Tout ce qui n'est pas confirmé doit sortir du texte ou être attribué.

## Pour chaque histoire
1. `python3 tools/v4_show.py <id>` (texte actuel) ; lis aussi `note` et `src` dans `data/opsis_v4/<id>.json` (la note liste ce qui est « établi / rapporté / à vérifier »).
2. Établis la liste des affirmations vérifiables : dates, lieux, noms, titres, chiffres, durées, citations, causalités, résultats de procès, âges, ordre des événements. Commence par celles de « À vérifier ». Ne saute aucune date ni aucun chiffre.
3. Vérifie chacune avec au moins UNE source solide, DEUX pour les dates clés, chiffres, verdicts et citations. Sources par ordre de préférence : documents primaires et institutions (tribunaux, archives, FBI, NASA, Nobel, sites officiels), encyclopédies sérieuses (Britannica, Wikipédia FR/EN pour s'orienter puis recoupement), grande presse (Le Monde, NYT, Guardian, BBC, Smithsonian…), ouvrages publiés. Un blog ou un forum ne suffit pas.
4. Corrige le texte pour qu'il colle aux sources :
   - fait faux → corrige ; fait invérifiable → supprime la phrase ou attribue-la (« selon X », « d'après le récit de… ») ;
   - sources divergentes → « selon X… ; d'après Y… » ou arrondi honnête (« une cinquantaine ») ;
   - citations : garde-les seulement si une source les donne ; sinon reformule sans guillemets ;
   - personnes vivantes ou affaires criminelles : seulement ce que disent les décisions de justice et les sources fiables ; mots précis (« accusé », « condamné », « acquitté ») ; aucune insinuation, aucune pensée prêtée ;
   - jamais d'intention, d'émotion ou de pensée qui ne soit pas documentée.
   Garde la qualité narrative (docs/STYLE_OPSIS_V4.md) et les bornes de format de `tools/v4_check.py`. Si une suppression fait passer sous le plancher de mots, complète avec des faits VÉRIFIÉS (pas de remplissage). Si le plancher est impossible à tenir, change `fmt` (7 → 3) comme l'ont fait les relectures précédentes.
5. Mets à jour `src` (liste de chaînes) : 3 à 6 entrées, UNIQUEMENT des sources réellement consultées dans cette passe et qui soutiennent l'histoire. Format : `Auteur ou institution, « Titre », éditeur ou support, année. adresse-sans-https`. Remplace les anciennes sources non consultées. Ne fabrique jamais une référence ni une URL : si tu ne l'as pas ouverte, elle n'y va pas.
6. Réécris `note` (lue par le lecteur, ≤ 650 caractères, ton sobre) : « Établi : … Rapporté : … Incertain : … ». Plus aucune mention « à vérifier avant publication » : tout ce qui reste incertain est soit retiré du texte, soit annoncé dans « Incertain ».
7. Écris le journal d'audit `data/opsis_v4/_verif/<id>.txt` : une ligne par affirmation contrôlée : `VERIFIÉ | CORRIGÉ | RETIRÉ | ATTRIBUÉ | INCERTAIN — affirmation — source (URL)`.
8. Valide : `python3 tools/v4_check.py <id>` doit répondre OK.

## Règles de travail
- Modifie les JSON par un script Python (dossier à toi dans le scratchpad) qui remplace des paragraphes par texte de départ exact (arrêt si introuvable ou en double). Ne remplace jamais par index.
- Ne touche ni à git, ni à content.json, ni aux autres ids. Je fusionne et je commite.
- Si WebFetch ou WebSearch échoue sur une source, essaie une autre ; si un fait central reste invérifiable, retire-le plutôt que de le garder.
- Ne perds pas l'histoire : la vérification ne doit pas la transformer en liste de précautions. Une phrase attribuée vaut mieux qu'un paragraphe de réserves.

## Rapport final (une ligne par id)
`id : n affirmations contrôlées, n corrigées, n retirées, n incertaines — fait le plus important corrigé — doute restant`. Signale en tête toute histoire où un fait central s'est révélé FAUX.
