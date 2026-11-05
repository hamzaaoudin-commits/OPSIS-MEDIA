# Histoires de marques OPSIS : consignes de rédaction

Tu écris des histoires VRAIES pour OPSIS, une app française d'histoires vraies. Thème : « Marques ».
Critère de choix (déjà fait pour toi) : une histoire qu'on raconterait à une soirée. Pas l'« origine d'un objet » ennuyeuse,
mais un moment où une marque a failli mourir, a pris un pari fou, a été sauvée par un détail, ou a changé de nature.

## Méthode (OBLIGATOIRE)
1. Fais de vraies recherches web (WebSearch/WebFetch) : au moins 4 sources par histoire, dont des sources solides (livre, grand média, documentation d'entreprise, archives, Wikipédia comme point de départ seulement).
2. N'écris QUE des faits que tu as vus dans tes sources. Chaque chiffre, date, nom, citation doit être vérifié. Si une source diverge d'une autre, dis-le dans le texte (« selon X… », « les récits diffèrent »). Si tu n'es pas sûr, supprime la phrase.
3. Aucune accusation non établie contre une personne vivante ou une entreprise. Reste sur ce qui est documenté (décisions de justice, déclarations publiques, documents).
4. Pas de logo, pas de slogan reproduit comme décor. Les marques sont nommées dans le texte, c'est normal.

## Forme de l'histoire (champ "body", tableau de chaînes)
- 650 à 900 mots au total (texte hors marqueurs).
- Chaque élément du tableau est une chaîne :
  - "#Titre de section" (courte, concrète) : 5 à 7 sections ;
  - "@Lieu, date précise." : ligne de situation, juste après le premier titre de section (ex. "@Portland, Oregon, 1971.") ;
  - un paragraphe = une chaîne ;
  - "!phrase forte" : une phrase de respiration qui résume le tournant (2 ou 3 par histoire, pas plus).
- Style : français clair, phrases courtes, présent de narration pour la scène d'ouverture, passé ensuite. Ouvre par une SCÈNE précise (un lieu, un jour, un geste), pas par un résumé. Une idée par paragraphe. Les nombres en chiffres sont acceptés. Pas de « incroyable », « fascinant », pas de morale lourde.
- Termine par ce qu'on retient ou ce qui reste ouvert (une dernière section courte, par exemple « Ce qu'on ne sait pas » ou « Ce que ça a changé »). Pas de conclusion moralisante.
- Apostrophes droites ', guillemets français « ».

## Champs de sortie (JSON)
Un fichier : data/marques_src/<nom_agent>.json  = une liste d'objets :
{
 "id": "mq01",            // l'id imposé dans ta mission
 "name": "Titre explicite",   // 3 à 7 mots, dit le sujet (ex. « Nike : le logo à 35 dollars »), 40 caractères max
 "sub": "Phrase d'une ligne qui donne le sujet et le tournant (110 à 180 caractères), avec lieu et année",
 "dates": "1971" ou "8 août 1963" ou "1997–2001",
 "country": "États-Unis",
 "job": "Marque ou entreprise concernée",
 "src": "Source 1 avec URL || Source 2 avec URL || ...",   // séparées par " || ", au moins 4
 "body": [...],
 "blurb": {"b": "...", "h": "..."},   // voir docs/STYLE_BLURB.md (blurb 45 à 65 mots, hook 6 à 14 mots)
 "cover": "<svg ...>"     // voir ci-dessous
}

## Couverture (champ "cover")
Une illustration SVG simple, plate, sans texte, en viewBox="0 0 200 300", style des autres couvertures OPSIS :
- un fond dégradé vertical (un <linearGradient> avec un id unique par histoire, ex. "gmq01", de la couleur de l'histoire vers #0A0708),
- un grand disque ou une forme claire derrière (autour de cx=100 cy=112 r=64..76), puis 3 à 8 formes géométriques qui évoquent un OBJET ou une SCÈNE de l'histoire (une semelle, une bouteille, une brique, un wagon, une table...). 
- Interdit : lettres, logos réels de marques, mots, silhouettes de personnes réelles.
- 1 à 3 ko maximum.

## Vérification avant de rendre
Relis ton texte : chaque chiffre est-il dans une source ? Le texte fait-il bien 650 à 900 mots ? Le JSON est-il valide (python3 -c "import json;json.load(open('...'))") ?
