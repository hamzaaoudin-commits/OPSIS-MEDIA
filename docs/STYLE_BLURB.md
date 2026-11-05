# Quatrièmes de couverture OPSIS

Chaque histoire a une couverture qui se retourne. Au dos : un RÉSUMÉ (blurb) et une ACCROCHE (hook).
Le lecteur ne connaît RIEN de l'histoire. Il doit comprendre en 10 secondes de quoi ça parle, et avoir envie de lire.

## BLURB (45 à 65 mots, 3 ou 4 phrases, présent de narration)
1. Phrase 1 : QUI (nom + ce qu'il/elle est, en mots simples) et OÙ/QUAND (en toutes lettres, pas « Londres, 1704 : »). Ne commence jamais par un lieu suivi de deux-points.
2. Phrase 2 : CE QUI SE PASSE — l'événement ou le geste central, concret.
3. Phrase 3 : L'ENJEU ou la question qui reste ouverte (ce qu'on risque, ce qu'on ne sait pas, ce qui ne colle pas).
4. Facultatif : une dernière phrase courte.
- Zéro jargon, zéro sigle non expliqué, aucun nom propre qui ne soit pas introduit (« le physicien Klaus Fuchs », pas « Fuchs »).
- Ne révèle pas la chute, mais fais-la sentir. Pas de « une histoire incroyable », « vous ne devinerez jamais », pas de question en cascade, pas de points de suspension.
- Uniquement des faits présents dans le TEXTE fourni. Si le texte dit que c'est discuté ou inconnu, garde l'incertitude (« on ne sait pas si… »). N'invente ni chiffre, ni date, ni nom.
- Pas de formulations de méthode : jamais « selon les sources », « cette histoire », « ce récit sépare ».

## HOOK (6 à 14 mots)
Une image ou un paradoxe concret tiré du texte, qui donne envie. Pas de guillemets (sauf vraie citation présente dans le texte), pas de point de suspension, pas de question. Ne répète pas le blurb.

## Sortie
Un fichier JSON : data/blurb_src/batchNN.json
{ "id": {"blurb": "...", "hook": "..."}, ... }  — une entrée par histoire du lot, tous les ids.
Français correct, apostrophes droites ' ou typographiques ’ au choix, mais cohérent. Pas de markdown.

## Exemple (pr04, Galilée)
blurb : "En 1633, à Rome, Galilée a soixante-dix ans et comparaît devant l'Inquisition pour avoir défendu l'idée que la Terre tourne autour du Soleil. Dix cardinaux jugent son cas, mais sept seulement signent la sentence. Un document de 1616, que Galilée n'a jamais signé, pèse lourd dans l'affaire."
hook : "Sept cardinaux sur dix signent. Le document décisif n'est signé par personne."
