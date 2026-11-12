# Relecture éditoriale OPSIS v4 — lis chaque histoire en lecteur qui ne sait rien, puis améliore-la

Pour CHAQUE id de ton lot : ouvre `data/opsis_v4/<id>.json`, lis le `body` en entier comme un lecteur curieux qui ne connaît rien au sujet. Compare mentalement avec les modèles `docs/modeles/franklin_v4.md` et `docs/modeles/christie_v4.md`, et avec `docs/STYLE_OPSIS_V4.md`. Puis corrige le fichier sur place (réécris les passages faibles, ne te contente pas de retouches cosmétiques). Si l'histoire est déjà au niveau, ne la touche pas, mais dis-le.

## Grille (réponds honnêtement à chaque point pour chaque histoire)
1. **Ouverture** : situation universelle + enjeu clair dans les 2-3 premières phrases ? Aucun nom de lieu/institution/objet inconnu sans explication ? Donne-t-elle envie de lire la suite ?
2. **Compréhension** : y a-t-il des références jamais expliquées (jargon, institution, personne, lieu, objet) ? Explique-les en une demi-phrase, naturellement.
3. **Progression** : est-ce un récit (chaque paragraphe change la compréhension) ou un résumé chronologique / une liste de faits ? Les 2-3 moments décisifs ont-ils chacun une vraie séquence ? Une révélation par paragraphe ?
4. **Style** : phrases courtes isolées en formule (« Il n'y en a plus. » / « Rien. ») → fusionne-les en phrases plus longues et fluides, garde au plus quelques courtes phrases à effet, justifiées. Paragraphes > 110 mots → scinde. Pas de paragraphe-fiche, pas d'empilement de chiffres.
5. **Personnage central** : qui, ce qu'il veut, ce qui l'en empêche, ce qu'il risque, ce qui lui arrive ? (uniquement avec des faits documentés).
6. **Rigueur** : aucune pensée, émotion ou dialogue inventé. « Il savait / il pensait / il espérait… » → supprime ou reformule en fait/témoignage rapporté (« selon… », « on rapporte »). Aucune citation non attribuée. Aucun fait douteux affirmé comme certain : adoucis ou retire, et mets-le dans `note`.
7. **Fin** : un fait, une conséquence, une image ou une question sans réponse. Jamais une morale ni une phrase-sentence (« La nature n'a pas besoin de colère… »). Réécris si besoin.
8. **Titre / blurb / sub** : cohérents avec le texte réécrit, sans spoiler total, accrocheurs, titre ≤ 46 caractères.
9. **Format** : si l'histoire est solide, tu peux l'allonger (3→7) uniquement avec des faits sûrs ; ne remplis jamais.

## Règles
- Aucune recherche web. Rien d'inventé.
- Respecte le schéma JSON existant ; garde `fmt` cohérent avec la longueur (3 = 520–850 mots, 7 = 1100–2000 mots, hors intertitres).
- Pas de PROLOGUE/ÉPILOGUE, pas de `@`, pas de `!`, pas d'astérisques, 4 intertitres max (3 min) / 6 (7 min), sans numéros.
- Après chaque correction : `python3 tools/v4_check.py <id>` doit répondre OK.
- Ne touche à aucun autre fichier. Pas de commit.
- Mets à jour `note` si tu changes des faits (ajouts de mémoire, adoucissements).

## Rapport final (court)
Pour chaque id : `id : retouchée | inchangée — principal défaut corrigé` (une ligne). Puis les ids pour lesquels tu doutes d'un fait important.
