# Allonger une histoire OPSIS trop courte

Objectif : passer chaque histoire de ~300 mots à 650–800 mots (3 à 4 minutes de lecture), sans la trahir.

Règles
- Tu reçois un id. Lis son texte actuel dans data/content.json (cherche l'id dans D.*), y compris les champs `sub` et `src`.
- Garde le titre, le ton, la structure et TOUS les faits déjà établis. Réécris le corps en l'enrichissant : scène d'ouverture plus précise, contexte, personnages, chronologie, ce qui est discuté ou inconnu, ce qui reste ouvert à la fin.
- Recherche web obligatoire (≥ 3 sources par histoire). N'ajoute QUE des faits vérifiés par au moins une source lue. Pas de dialogues inventés, pas de pensées prêtées aux personnages, pas d'accusation non établie. Si les sources divergent, dis-le dans le texte. Si un fait n'est pas retrouvé, ne l'ajoute pas.
- Format du corps : liste de chaînes. "#Titre de section" (4 à 6 sections), "@Lieu, date." après la première section, paragraphes normaux, 2 à 3 phrases fortes préfixées de "!". Comme le texte actuel.
- Ajoute à `src` les nouvelles sources, au même format (séparées par " || " si le champ actuel les sépare ainsi, sinon à la suite).
- Écris en français soigné, phrases courtes et concrètes, sans lourdeur ni formules creuses.
- Sortie : /home/claude/opsis-media/data/allonge/out_N.json = liste d'objets {"id","body","src"} (body = liste de chaînes, src = chaîne complète mise à jour). Vérifie le JSON avec python3 et compte les mots (hors lignes # @ *) : chaque corps doit faire au moins 600 mots.
