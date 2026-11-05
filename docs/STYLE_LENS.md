# Écrire les 3 versions (3 / 5 / 10 min) d'une histoire OPSIS

Sortie : `data/lens_src/<id>.json` = `{"3":[…],"5":[…],"10":[…]}`, chaque valeur est un tableau de blocs.
Blocs : `"#Titre de section"`, `"@Lieu, date."` (une seule fois, juste après le premier titre), `"!Phrase isolée forte"`, sinon un paragraphe. Pas de markdown (pas d'astérisques, pas de gras).

## Règles non négociables
1. **Aucun fait inventé.** Chaque fait (date, chiffre, nom, citation, lieu, geste) doit venir du texte actuel ou d'une source que tu as lue (WebFetch / WebSearch). Pas de détail de décor imaginé (odeur, météo, pensées) non sourcé.
2. **Recherche d'abord.** Lis les sources listées (`node tools/lens-brief.js <id>`), cherche-en d'autres si elles sont minces, note les faits utiles (dates, noms, chiffres, citations exactes), puis écris.
3. **Les incertitudes restent des incertitudes** : « selon », « on ne sait pas », « la légende veut que » comme dans le texte actuel. Ne transforme pas une légende en fait.
4. **Les trois versions diffèrent vraiment** : 3 min ≈ l'essentiel net (400–600 mots) ; 5 min ≈ plus de contexte, de personnes, de scènes (700–1000) ; 10 min ≈ immersion, scènes développées, causes et conséquences, ce qu'on sait / ne sait pas (1200–1800 mots, selon la matière réelle). Si la matière manque, écris plus court plutôt que de remplir : jamais de répétition ni de remplissage.
5. Voix : français, présent de narration, phrases courtes à moyennes, sobres, précises, sans clichés ni formules creuses (« plongez », « l'histoire retient », « tel un »), sans adresse au lecteur sauf rare « Imaginez ». Pas de moralisation. Termine sur un fait ou une incertitude, pas sur une morale.
6. Respecte le ton et la structure du texte actuel (mêmes grandes sections quand c'est pertinent), mais réécris : ne copie pas mot pour mot les 3 versions.
7. Écris les chiffres et les noms exactement comme dans les sources. Pas de mot anglais inutile.

## Référence de qualité
Voir `data/lens_src/fa16.json` (Henry) et `fa28.json` (kouros du Getty).

## Contrôle avant de rendre
`node -e "const d=require('./data/lens_src/ID.json');const w=a=>a.filter(x=>!/^[#@*]/.test(x)).join(' ').split(/\s+/).length;console.log(w(d['3']),w(d['5']),w(d['10']))"` — l'ordre 3<5<10 est obligatoire. Relis chaque phrase en te demandant : « d'où vient ce fait ? ».
Ne modifie aucun autre fichier. N'utilise pas git.
