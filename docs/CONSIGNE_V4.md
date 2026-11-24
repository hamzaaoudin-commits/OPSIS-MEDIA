# Consigne de réécriture OPSIS v4 (à suivre pour chaque histoire)

Tu réécris des histoires vraies pour OPSIS Originals. Objectif : le plaisir de se faire raconter une histoire. PAS un résumé documentaire.

## Lis d'abord (dans l'ordre)
1. `docs/STYLE_OPSIS_V4.md` — la charte (Narrative Experience Standard + profondeur narrative).
2. Les modèles à égaler : `docs/modeles/franklin_v4.md`, `docs/modeles/christie_v4.md` (modèles de voix), `docs/modeles/lustig.md`, `docs/modeles/nyos.md` (les modèles de l'auteur). Observe : ouverture accessible, paragraphes de 40 à 90 mots, phrases de longueurs variées, moments clés développés, une question qui porte le récit, information donnée quand le lecteur en a besoin, fin factuelle sans morale.
3. La matière : `python3 tools/v4_show.py <id>` (ancien texte + sources). L'ancien texte sert de réservoir de FAITS, pas de modèle de style : ne le retouche pas, réécris.

## Règles
- Aucune recherche web. Faits = ceux de l'ancien texte + ce que tu sais avec certitude. Rien d'inventé : ni pensées, ni dialogues, ni scènes, ni chiffres. Un fait douteux est soit omis, soit présenté comme rapporté/selon les versions et listé dans `note`.
- Le lecteur ne sait RIEN : aucun lieu/institution/objet/personne sans contexte. Pas de détail dont l'importance est inconnue.
- Ouvre sur une situation universelle + un enjeu clair (qui a disparu ? quoi est arrivé ? pourquoi ça compte ?), pas sur un nom de lieu ni une dateline.
- Choisis le cœur dramatique, un point de vue, un personnage central, et l'ordre des révélations ; la structure est dictée par l'histoire (enquête, tragédie, arnaque à retournements, ascension…). N'utilise pas un plan identique d'une histoire à l'autre. Tu peux commencer par la fin/une découverte puis remonter, ou suivre l'ordre chronologique : décide selon l'histoire.
- Développe les 2-3 moments décisifs (séquences à part entière, dans l'ordre de découverte) ; résume le reste. Une révélation par paragraphe, jamais cinq.
- Pas de phrases courtes isolées en formule, pas de paragraphe-fiche. Pas de phrase-sentence ni de morale à chaque paragraphe. Pas de clichés cinématographiques.
- Fin : un fait, une conséquence, une image ou une question sans réponse. Jamais une leçon.
- Intertitres : parcimonieux (2 à 5 selon le format), en casse normale, sans numéros, lignes commençant par `#`. Pas de `@`, pas de `!`, pas de PROLOGUE/ÉPILOGUE, pas d'astérisques, pas de « ce que vous venez de découvrir / à retenir ».
- Format (choisi selon la richesse de l'histoire, pas par défaut) : 3 min = 520–850 mots ; 7 min = 1100–2000 ; 12 min = 2000–3200 (seulement si la matière le justifie sans remplissage). Si la matière ne suffit pas à développer honnêtement, reste à 3.
- Sources : ne cite pas de sources dans le récit.

## Sortie : `data/opsis_v4/<id>.json`
```
{"id":"<id>","fmt":3|7|12,"name":"titre ≤46 car., casse normale, accrocheur",
 "sub":"une phrase 60-220 car.: lieu/date — situation (sert dans les listes)",
 "body":["paragraphe","#Intertitre","paragraphe",…],
 "note":"note éditoriale : ce qui est établi, ce qui est rapporté/discuté, ce qui est à vérifier avant publication (détails de mémoire, chiffres, versions divergentes)",
 "blurb":{"b":"40-75 mots, accroche qui donne envie, sans spoiler total","h":"une ligne d'accroche"}}
```
(`src` : omets-le, les sources existantes sont conservées.)

Valide avec `python3 tools/v4_check.py <id>` ; corrige jusqu'à OK, puis relis ton texte en lecteur qui ne connaît rien : est-ce que j'ai envie de lire la suite ? Ne touche à aucun autre fichier. Ne fais pas de commit. À la fin, réponds par la liste des ids terminés et de ceux laissés en échec avec la raison (une ligne chacun).
