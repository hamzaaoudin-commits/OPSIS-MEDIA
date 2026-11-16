#!/usr/bin/env python3
"""OPSIS — « Une vie en épisodes ».
Construit data/lives.json (id du portrait -> épisodes) à partir des portraits de data/content.json
(sections réorganisées en ordre chronologique) et de passages nouveaux écrits ici.
    python3 tools/lives_build.py
Les portraits d'origine ne sont pas modifiés."""
import json, os
root = os.path.join(os.path.dirname(__file__), '..')
C = json.load(open(os.path.join(root, 'data/content.json')))
P = {p['id']: p for p in C['BOOK']['portraits']}

def sections(pid):
    out, cur = [], None
    for l in P[pid]['body']:
        if l.startswith('#'):
            cur = [l]; out.append(cur)
        else:
            cur.append(l)
    return out

def S(pid, k, a=0, b=None, head=False):
    """lignes de la section k (sans le titre sauf head=True), tranche [a:b] sur le corps"""
    sec = sections(pid)[k]
    body = sec[1:]
    body = body[a:b]
    return ([sec[0]] if head else []) + body

def ep(t, sub, *parts):
    body = []
    for x in parts:
        body += x
    return {'t': t, 'sub': sub, 'body': body}

HELP = ['*', "Si vous traversez une période difficile, en France le 3114 (numéro national de prévention du suicide) est joignable jour et nuit, gratuitement."]

L = {}

# ---------------------------------------------------------------- JUDY GARLAND (pt01)
g = 'pt01'
L[g] = {'eps': [
 ep('La petite Gumm', "Une enfant qui ne veut pas descendre de scène, et un studio qui la signe à treize ans.",
    S(g, 0, 0), ['*'], S(g, 1, 0, 6),
    ["Ils s’installent à Lancaster, aux portes du désert de Mojave, où Frank reprend un cinéma. Ethel est à la fois la mère, l’habilleuse et l’imprésario du trio : elle joue du piano, coud les costumes, négocie les cachets.",
     "Le nom de scène lui-même est une invention. Plusieurs versions circulent, mais la plus répandue raconte qu’en 1934, à Chicago, un présentateur trouva que « Gumm » faisait trop rire sur une affiche. Les Gumm Sisters devinrent les Garland Sisters."],
    S(g, 1, 6)),
 ep('L’usine', "La MGM fabrique une star : son nom, son poids, son sommeil.",
    S(g, 2, 0, 2),
    ["Pourtant, dès ses premiers mois, le studio sent qu’il tient quelque chose. Au printemps 1936, elle chante dans un court métrage, *Every Sunday*, avec une autre jeune recrue, Deanna Durbin. Début 1937, elle chante *You Made Me Love You* à Clark Gable lui-même, pour l’anniversaire de l’acteur. La chanson est reprise dans *Broadway Melody of 1938*, où elle l’adresse à son portrait. Elle a quatorze ans. Mayer comprend ce qu’il a signé.",
     "À partir de 1937, le studio l’associe à un autre enfant du plateau, Mickey Rooney. Ils tourneront ensemble une dizaine de films : des comédies et des comédies musicales de jeunes gens, tournées vite, vendues partout. À côté de leurs scènes, il y a l’école du studio, quelques heures de cours par jour sur le lot, et les cours comptent peu face au plateau.",
     "Judy a une mère qui est aussi, de fait, une collègue de la machine : Ethel suit le travail de sa fille, signe, accompagne, relaie les consignes. Plus tard, Judy dira qu’elle ne pouvait faire confiance à personne, parce que tous ceux qui la touchaient en tiraient un salaire."],
    S(g, 2, 2)),
 ep('Au-delà de l’arc-en-ciel', "Seize ans, un corset, et la chanson qu’on a failli couper.",
    S(g, 3, 0, 2),
    ["Au début, on ne cherche pas à cacher seulement son corps. On cherche à lui donner un autre visage. Le studio essaie d’abord de la transformer : perruque blonde, maquillage épais, costume de petite poupée. Le résultat est faux, et les essais le montrent. Le réalisateur George Cukor, consulté, demande qu’on enlève tout, la perruque et le fard. Il veut une fille de Kansas, naturelle."],
    S(g, 3, 2, 6),
    ["Il reçoit de très bonnes critiques, mais il coûte cher et ne rapporte pas tout de suite autant que le studio l’espérait. Le vrai triomphe du *Magicien d’Oz* viendra plus tard, à force de reprises, puis de la télévision : à partir de 1956, une chaîne américaine le diffuse chaque année, et chaque année des familles entières se rassemblent devant l’écran."],
    S(g, 3, 6)),
 ep('Le Chant du Missouri', "Les années de triomphe, deux mariages, et une fille.",
    ["Les années 1940 sont celles du triomphe. Judy Garland enchaîne les comédies musicales, d’abord aux côtés de Mickey Rooney, puis seule en tête d’affiche. Elle est l’une des stars les mieux payées d’Hollywood. Elle a une voix que personne d’autre n’a.",
     "Et chaque année, elle va un peu plus mal.",
     "En juillet 1941, à 19 ans, elle épouse un musicien, David Rose. Elle tombe enceinte. Selon ses biographes, sa mère et le studio la poussent à avorter : une grossesse ruinerait l’image de la jeune fille qu’elle incarne à l’écran. Elle avorte. Le mariage ne dure pas : ils divorcent en 1944."],
    ["*", "#Meet Me in St. Louis",
     "En 1944, la MGM lui propose un film de plus, une chronique familiale à l’époque de l’Exposition universelle de 1904, réalisée par Vincente Minnelli. Elle ne veut pas d’abord jouer une adolescente. On la convainc. *Le Chant du Missouri* sort à la fin de l’année et devient l’un des plus grands succès de la MGM. On y entend, pour la première fois, *The Trolley Song*, et une chanson de Noël qui n’a plus quitté les radios : *Have Yourself a Merry Little Christmas*, qu’elle chante à sa petite sœur de cinéma pour la consoler.",
     "Le réalisateur et la star se marient le 15 juin 1945. Le 12 mars 1946, naît leur fille, Liza. Entre-temps, Judy a tourné un film sans chansons, *L’Horloge*, une histoire d’amour sobre, où l’on découvre une actrice. Elle enchaîne avec *Les Girls Harvey*, un western musical dont une chanson, *On the Atchison, Topeka and the Santa Fe*, remportera l’Oscar.",
     "C’est le moment de sa vie où tout semble tenir : un mari, un enfant, des films qui font pleurer et rire l’Amérique.",
     "Mais le rythme du studio n’a pas changé. Les films s’enchaînent. Les pilules aussi."]),
 ep('Renvoyée', "Retards, effondrements, cliniques : à vingt-huit ans, le studio la met dehors.",
    ["#Elle ne tient plus",
     "En 1948, Gene Kelly se casse la cheville avant le tournage d’*Easter Parade*. Le studio demande à Fred Astaire de sortir de sa retraite pour jouer à côté de Judy. Le film est un triomphe. Le public ne voit pas ce qu’il y a derrière : une femme que l’on réveille avec des stimulants et que l’on endort avec des barbituriques."],
    S(g, 4, 3, 4),
    ["En 1949, la MGM la retire du tournage d’*Annie du Far West*. Elle ne tient plus debout. On l’envoie se reposer. Elle revient, et on lui donne un dernier film, *Summer Stock*, avec Gene Kelly. Pour le terminer, on lui demande de tourner après coup un numéro supplémentaire, *Get Happy*, en veste noire et chapeau penché. Elle a maigri. Elle danse, elle chante. C’est l’une de ses plus belles scènes.",
     "Au printemps 1950, le studio la renvoie d’un nouveau film, *Mariage royal*, après une nouvelle série d’absences. En juin, elle tente de mettre fin à ses jours. En septembre, la MGM rompt son contrat."],
    S(g, 4, 5), HELP),
 ep('Les come-back', "Palladium, Palace, *Une étoile est née* : la seconde vie, et la nuit des Oscars à l’hôpital.",
    ["Commence alors la seconde vie de Judy Garland. Celle que le public connaît le mieux : une suite de chutes et de retours, chaque fois plus spectaculaires.",
     "En avril 1951, elle chante au London Palladium, devant une salle qui ne la quitte pas des yeux. En octobre, elle est au Palace, à New York, où elle reste dix-neuf semaines. Les salles lui font des ovations interminables. Le music-hall, ce qu’elle faisait enfant, devient son salut. La profession lui décerne une récompense spéciale pour ce retour.",
     "Elle épouse en 1952 Sid Luft, qui devient son producteur. Une fille, Lorna, naît en novembre 1952. Luft veut lui offrir un film à la mesure de sa légende. Ce sera *Une étoile est née*, réalisé par George Cukor, un grand mélodrame sur une actrice qui monte pendant que son mari, un acteur, s’effondre. Le tournage est long et chaotique. Elle est souvent en retard, parfois absente. Mais quand la caméra tourne, on voit le film d’une vie. Il sort en septembre 1954. Les critiques sont superbes. Le studio, lui, coupe le film : plus d’une demi-heure disparaît de la version d’origine."],
    ["#La nuit des Oscars",
     "En mars 1955, Judy Garland attend un deuxième enfant. Le 29, elle accouche de Joey, par césarienne. Le lendemain soir, ce sont les Oscars. Elle est nommée pour la meilleure actrice. Les équipes de la télévision installent leurs caméras dans sa chambre d’hôpital, pour la filmer au moment où on annoncera sa victoire.",
     "L’Oscar va à Grace Kelly, pour *The Country Girl*. Les techniciens remballent leur matériel dans la chambre. Groucho Marx lui envoie un télégramme : c’est « le plus gros hold-up depuis celui de la Brink’s ». Hollywood le répétera pendant des années."]),
 ep('Carnegie Hall', "Le soir où elle est au sommet de son art, et l’émission qui ne marche pas.",
    ["Les années suivantes, Judy Garland vit surtout de la scène. En 1956, elle signe à Las Vegas l’un des plus gros contrats jamais offerts à une artiste de cabaret. Elle donne des concerts aux États-Unis, en Angleterre, en Europe. Elle tombe aussi gravement malade : en 1959, une hépatite aiguë la cloue à l’hôpital pendant de longues semaines, et on craint pour sa vie. Elle s’en sort. On lui dit qu’elle ne chantera plus. Elle chantera.",
     "En 1961, elle retourne à Hollywood pour un rôle dramatique de second plan dans *Jugement à Nuremberg*, de Stanley Kramer. Elle y joue une Allemande, Irene Hoffmann, dans une seule scène de procès. Elle obtient une nomination à l’Oscar du meilleur second rôle. Elle ne gagne pas, mais plus personne ne dit qu’elle n’est qu’une chanteuse."],
    S(g, 5, 2, 6)),
 ep('Hôtels', "Un public qui la hue, un film dont on la renvoie, et un dernier hiver à Londres.",
    ["En 1964, en Australie, elle arrive sur scène dans un état si dégradé que le public la hue et qu’elle doit quitter la scène. Le divorce d’avec Sid Luft est prononcé en 1965. Elle se remarie la même année avec un acteur, Mark Herron. Ce mariage ne dure presque pas.",
     "En 1967, le studio Fox l’engage pour *La Vallée des poupées*, l’adaptation d’un roman à scandale sur des femmes qui se détruisent avec les pilules. Le rôle d’une chanteuse vieillissante semble écrit pour elle. On la renvoie après quelques semaines de tournage. Susan Hayward la remplace.",
     "À ce moment-là, elle n’a plus vraiment de domicile. Elle passe d’hôtel en hôtel avec ses enfants, parfois chassée faute d’avoir payé la note.",
     "En 1968, un journaliste l’interroge. Elle se décrit comme la reine des come-back. Puis elle ajoute qu’elle commence à être fatiguée de revenir."],
    ['*'], S(g, 6, 0), HELP),
 ep('Les vingt mille', "Une nuit de vigile à New York, et ce que dit son histoire.",
    S(g, 7, 0), ['*'], S(g, 8, 0, head=True),
    ["Sa fille Liza Minnelli deviendra à son tour une star, de la scène et du cinéma. En 2001, une enquête menée par l’association américaine de l’industrie du disque et une fondation culturelle placera *Over the Rainbow* au premier rang des chansons du siècle."]),
]}

# ---------------------------------------------------------------- AMY WINEHOUSE (pt11)
w = 'pt11'
L[w] = {'eps': [
 ep('Southgate', "La grand-mère qui chantait du jazz, la guitare à treize ans, et un soir de juin à Belgrade.",
    S(w, 0, 0), ['*'], S(w, 1, 0, 4),
    ["Cynthia a connu de près le jazz londonien : elle a été la compagne du saxophoniste Ronnie Scott, qui a fondé l’un des clubs les plus célèbres de la ville. Amy grandit avec ces disques et ces histoires. À l’adolescence, elle chante dans l’orchestre de jazz des jeunes de Londres."]),
 ep('Frank', "Un premier disque salué par la critique, et que sa chanteuse n’aime pas.",
    ["À 16 ans, un ami fait passer sa cassette à un label. Elle est repérée, puis signée par une maison de disques en 2002. Son premier album, *Frank*, sort à l’automne 2003, quelques semaines après ses vingt ans. Elle écrit presque toutes ses chansons.",
     "C’est un disque de jazz et de soul, aux textes crus et drôles, où l’on entend déjà Billie Holiday et Dinah Washington, mais aussi le hip-hop qu’elle écoute dans sa chambre. Elle y parle de ses amours avec une franchise qui surprend, dans la bouche d’une fille de vingt ans.",
     "La critique est enthousiaste. *Frank* est cité aux récompenses britanniques, et Amy y gagne ses premiers prix d’auteure-compositrice. L’album se vend bien au Royaume-Uni.",
     "Mais Amy n’est pas contente. Elle trouve que son disque est trop poli, que la production a effacé ce qu’elle voulait faire. Elle le dira à plusieurs reprises : elle n’a pas eu le dernier mot sur sa propre musique."],
    S(w, 1, 5, 6),
    ["Elle quitte la maison de sa mère, s’installe dans le nord de Londres, à Camden, le quartier des concerts et des pubs. Elle y trouve ce qu’elle cherche : des musiciens, des nuits longues, des gens qui ne lui demandent pas d’être sage."]),
 ep('Blake', "L’homme d’un pub de Camden, et les chansons qui en sortent.",
    S(w, 2, 0, 2),
    ["Elle se fait tatouer son nom sur la poitrine. Ils sont comme deux enfants dans un jeu dont ils ne connaissent pas les règles."],
    S(w, 2, 2)),
 ep('Back to Black', "L’album de la décennie, et une silhouette que tout le monde reconnaît.",
    S(w, 3, 0, 2),
    ["Les cuivres sur l’album sont joués par un groupe de soul new-yorkais, les Dap-Kings. Elle enregistre vite, presque dans l’urgence, des chansons qu’elle a écrites dans la rage."],
    ["Au début de 2007, la chanteuse monte sur la scène des Brit Awards pour chanter *Rehab*, la chanson du refus de se soigner, et y gagne le titre de meilleure chanteuse britannique. L’album entre directement dans le top 10 américain, un exploit pour une artiste anglaise venue du jazz."],
    S(w, 3, 2)),
 ep('Camden', "Sous les flashs : une chute photographiée jour après jour.",
    S(w, 4, 0)),
 ep('La nuit des Grammy', "Cinq prix, un satellite, et une phrase murmurée à une amie.",
    S(w, 5, 0, 2),
    ["À la fin de la soirée, le compte est là : enregistrement de l’année et chanson de l’année pour *Rehab*, meilleur nouvel artiste, meilleur album pop vocal, meilleure interprétation pop féminine."],
    S(w, 5, 2)),
 ep('Les vautours', "Cures, rechutes, concerts annulés : tout le monde la voit aller mal.",
    S(w, 6, 0)),
 ep('Camden Square', "Les dernières semaines, et ce que dit son histoire.",
    S(w, 7, 0), HELP, ['*'], S(w, 8, 0, head=True)),
]}

# ---------------------------------------------------------------- DIEGO MARADONA (pt06)
m = 'pt06'
L[m] = {'eps': [
 ep('Villa Fiorito', "Un bidonville, un ballon de cuir, deux rêves : jouer une Coupe du monde, et la gagner.",
    S(m, 0, 0, 6), S(m, 0, 7, 8),
    ['*'], S(m, 1, 0)),
 ep('Le gamin qui nourrit sa famille', "Seize ans, premier match pro, et huit personnes qui dépendent de lui.",
    S(m, 2, 0, 1),
    ["Quelques mois plus tard, en février 1977, il joue pour la première fois avec l’équipe nationale argentine. Il a 16 ans."],
    S(m, 2, 1, 3),
    ["En 1979, à 18 ans, il mène les jeunes Argentins à la victoire en Coupe du monde des moins de vingt ans, au Japon. Il est élu meilleur joueur du tournoi. L’affront de 1978 est lavé. À 18 ans, on ne peut plus le retirer d’une liste."],
    S(m, 2, 3, 4),
    ["Au Mondial 1982, en Espagne, l’Argentine, tenante du titre, est éliminée. Contre le Brésil, Maradona est expulsé après un coup de pied à un adversaire. Il a 21 ans."],
    S(m, 2, 4)),
 ep('Naples', "Quatre-vingt mille personnes pour ne rien voir d’autre qu’un homme qui jongle.",
    S(m, 3, 0, 3),
    ["Dans ses premiers mots à la presse, il explique qu’il veut devenir l’idole des enfants pauvres de Naples, parce qu’ils sont comme il était, à Buenos Aires."],
    S(m, 3, 3),
    ["La ville sort alors d’années difficiles. En novembre 1980, un séisme a dévasté le sud de l’Italie, tuant des milliers de personnes. Naples, elle, a l’habitude qu’on ne l’attende nulle part.",
     "Il lui faudra pourtant trois saisons pour offrir à la ville le titre dont elle rêve : trois ans à porter une équipe qui n’a jamais rien gagné."]),
 ep('La main et le génie', "Quatre minutes pour montrer les deux visages, et une Coupe du monde à vingt-cinq ans.",
    ["Mexico, été 1986. Maradona est le capitaine d’une équipe d’Argentine que peu de monde juge capable de gagner. Avant ce quart de finale, il a déjà marqué. Mais c’est contre l’Angleterre que le monde va découvrir qui il est."],
    S(m, 4, 0, 6),
    ["En demi-finale, il marque deux fois contre la Belgique. En finale, l’Allemagne de l’Ouest revient de 2-0 à 2-2. À dix minutes de la fin, Maradona, marqué de près, trouve une passe qui coupe la défense. Burruchaga marque. 3-2.",
     "Il est élu meilleur joueur du tournoi."],
    S(m, 4, 6)),
 ep('Le dieu de Naples', "Un titre, une ville à genoux, et les amis qui l’entourent.",
    S(m, 5, 0, 1),
    ["Sur le mur d’un cimetière de la ville, quelqu’un écrit à la bombe une phrase qui deviendra célèbre : « Vous ne savez pas ce que vous avez raté », adressée aux morts qui n’ont pas vu ça."],
    S(m, 5, 1), ['*'], S(m, 6, 0, head=True)),
 ep('La chute', "Un contrôle positif, une carabine à plomb, et une infirmière en blouse blanche.",
    S(m, 7, 0), ['*'], S(m, 8, 0, head=True)),
 ep('Le corps qui lâche', "Vingt-trois ans de descente, ponctués de résurrections.",
    S(m, 9, 0, 2),
    ["Le 10 novembre 2001, 50 000 personnes viennent à la Bombonera, à Buenos Aires, pour son match d’adieu. Il prend le micro. Il y prononce une phrase qu’on n’oubliera pas."],
    S(m, 9, 2, 4),
    ["Il entraîne, en tout, des clubs au Moyen-Orient, en Biélorussie, au Mexique, puis, dans les derniers mois de sa vie, en Argentine, à Gimnasia La Plata."]),
 ep('Tigre', "Une maison louée, trois semaines après l’opération, et ce que dit son histoire.",
    S(m, 9, 4), ["*", "#Après lui"],
    ["Plus tard, la justice ouvrira une enquête. Sept professionnels de santé qui s’occupaient de lui seront renvoyés devant un tribunal, accusés de l’avoir laissé mourir. Lors d’un premier procès, en 2025, on montrera les images de son corps sur le lit, le ventre énormément gonflé par l’eau que son cœur malade n’arrivait plus à évacuer. Ses filles se cacheront le visage pour ne pas voir. Ce procès sera annulé après un scandale impliquant l’une des juges. Un second procès s’ouvre en 2026. À la mi-octobre 2026, le parquet a requis jusqu’à douze ans de prison, les avocats de la défense plaident, et le verdict est attendu avant la fin de l’année. Les accusés contestent toute responsabilité et restent présumés innocents."],
    ['*'], S(m, 10, 0, head=True)),
]}


# ---------------------------------------------------------------- les 49 autres vies : découpage automatique des sections
import re
HELPIDS = {'pt02','pt08','pt09','pt10','pt12','pt13','pt14','pt17','pt20','pt23','pt24','pt25','pt26'}
def nw(lines):
    return sum(len(x.split()) for x in lines if x[:1] not in '#@*')
def first_sentence(lines):
    for t in lines:
        if t[:1] in '#@*': continue
        m = re.match(r'(.{20,140}?[.!?»])(\s|$)', t)
        return (m.group(1) if m else t[:120]).strip()
    return ''
import glob
def add(pid, k, title, lines):
    ADDSEC.setdefault(pid, []).append((k, '#' + title, lines))
ADDSEC = {}   # pid -> [(k, '#Titre', [lignes])]  : section ajoutée après la section d'origine k
for _f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), 'lives_add_*.py'))):
    exec(open(_f, encoding='utf-8').read())
def auto(pid):
    sec = sections(pid)
    solo = set()
    for (k, t, lines) in [x[1] for x in sorted(enumerate(ADDSEC.get(pid, [])), key=lambda y: (-y[1][0], -y[0]))]:
        sec.insert(k + 1, [t] + lines)
        solo.add(t[1:])
    last = sec[-1]
    units = []                    # (titre, lignes sans titre)
    # cold open fusionné avec la section suivante
    first = sec[0]
    rest = sec[1:-1] if len(sec) > 2 else sec[1:]
    if len(sec) > 2:
        units.append((rest[0][0][1:], first[1:] + ['*'] + rest[0][1:]))
        for x in rest[1:]:
            units.append((x[0][1:], x[1:]))
        units[-1] = (units[-1][0], units[-1][1] + ['*', last[0]] + last[1:])
    else:
        for x in sec: units.append((x[0][1:], x[1:]))
    if len(sec) > 2 and rest[0][0][1:] in solo:
        units[0] = (units[0][0], units[0][1])
    # regroupement : épisodes d'au moins ~450 mots
    eps_, cur = [], None
    for t, lines in units:
        if t in solo and nw(lines) >= 170:
            if cur:
                if eps_ and nw(cur['body']) < 130: eps_[-1]['body'] += ['*', '#' + cur['t']] + cur['body']
                else: eps_.append(cur)
                cur = None
            eps_.append({'t': t, 'body': list(lines), 'best': nw(lines)})
            continue
        if cur is None:
            cur = {'t': t, 'body': list(lines), 'best': nw(lines)}
        else:
            cur['body'] += ['*', '#' + t] + lines
            if nw(lines) > cur['best']:
                cur['t'] = t; cur['best'] = nw(lines)
        if nw(cur["body"]) >= 130:
            eps_.append(cur); cur = None
    if cur:
        if eps_ and nw(cur["body"]) < 130:
            eps_[-1]['body'] += ['*', '#' + cur['t']] + cur['body']
        else:
            eps_.append(cur)
    out = []
    for e in eps_:
        out.append({'t': e['t'], 'sub': first_sentence(e['body']), 'body': e['body']})
    if pid in HELPIDS:
        out[-1]['body'] += HELP
    return {'eps': out}
for pid in P:
    if pid not in L:
        a = auto(pid)
        if len(a['eps']) >= 2:
            L[pid] = a

# ---- insertions ciblées (vérification des faits) : tools/lives_ins_*.py
INS = []
def ins(pid, epn, after, lines):
    """Insère `lines` après le paragraphe de l'épisode epn (1-based) qui contient `after`."""
    INS.append((pid, epn, after, lines))
for _f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), 'lives_ins_*.py'))):
    exec(open(_f, encoding='utf-8').read())
for (pid, epn, after, lines) in INS:
    body = L[pid]['eps'][epn - 1]['body']
    idx = [i for i, l in enumerate(body) if after in l]
    if len(idx) != 1:
        hits = [(n, j) for n, e in enumerate(L[pid]['eps']) for j, l in enumerate(e['body']) if after in l]
        assert len(hits) == 1, (pid, epn, after, len(idx), len(hits))
        print('  (ep déplacé)', pid, epn, '->', hits[0][0] + 1)
        body = L[pid]['eps'][hits[0][0]]['body']
        idx = [hits[0][1]]
    body[idx[0] + 1:idx[0] + 1] = lines

json.dump(L, open(os.path.join(root, 'data/lives.json'), 'w'), ensure_ascii=False, indent=1)
for pid, v in L.items():
    print(P[pid]['name'], len(v['eps']), 'épisodes')
    for e in v['eps']:
        w_ = sum(len(x.split()) for x in e['body'] if x[:1] not in '#@*')
        print('  %4d mots  %s' % (w_, e['t']))
