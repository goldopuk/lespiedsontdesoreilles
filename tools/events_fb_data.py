# Événements repris de la page Facebook « Les pieds ont des oreilles » (événements passés, lus le 2026-10-14).
# E(id Facebook, titre, date ISO, lieu, index d'affiche dans tools/events_scan.json ou None, description, autres rendez-vous du même week-end, date de fin)
# Les événements annulés sont exclus ; ceux qui ont déjà un article WordPress ne sont pas repris ici.


def E(fb, title, date, place, poster, desc="", also=(), end=None, other_org=None):
    return dict(fb=fb, title=title, date=date, end=end, place=place, poster=poster, desc=desc.strip(),
                also=[dict(title=t, date=d, place=p) for (t, d, p) in also], other_org=other_org)


EVENTS = [
    # ---------------- 2026 ----------------
    E("1723349738813896", "Não para à Paris : week-end forró avec Le Petit Bal Perdu", "2026-11-13", "École de danse Kim Kan - Studio des Rigoles, 46 rue des Rigoles, Paris", None, """
Les Podos à Paris !
Et si on se lançait ensemble dans un week-end de forró inoubliable ? Du 13 au 15 novembre 2026, notre partenaire Marion Lima et son association Le Petit Bal Perdu organisent à Paris un grand week-end de forró.
""", end="2026-11-15"),
    E("1565675318382471", "Place aux associations", "2026-09-05", "Place de l'Amérique Latine, Saint-Nazaire", None, """
Cette année on se retrouve au Forum des associations !
C'est le moment idéal pour venir nous rencontrer, papoter, poser toutes vos questions sur les cours, les bals, les concerts… et pourquoi pas vous inscrire pour la rentrée.
À 16h, rendez-vous sur la scène de l'Alvéole 12 pour un mini-bal forró !
On ne sera pas seul·es sur le stand : vous pourrez aussi rencontrer Farofa, toute nouvelle association nazairienne autour de la culture brésilienne.
"""),
    E("1087016643655642", "Bal-concert forró avec Gandaia na Ponte au Five-Oh", "2026-08-25", "Five-Oh, skatepark, Saint-Nazaire", None,
      "Bal et concert forró avec Gandaia na Ponte. Participation libre au chapeau."),
    E("3568970433240711", "Bal-concert forró avec Gandaia na Ponte au Nomad Café", "2026-04-25", "Nomad Café, 13 allée des Myosotis, Saint-Nazaire", 103, """
Avec Gandaia na Ponte, ça part en vrille… mais en rythme. Du forró qui claque, des sourires en cascade.
19h : ouverture des portes
19h30 : initiation / échauffement au forró
20h : concert
"""),
    E("938695205434291", "Bal-concert forró avec Gandaia na Ponte à la Fraternité", "2026-04-03", "La Fraternité, 1 rue de l'Île de France, Saint-Nazaire", None, """
Une soirée chaleureuse et festive pour partager la danse et la musique brésilienne.
19h30 – 20h : mise en jambes en playlist
20h – 20h15 : initiation au forró
20h30 – 22h : concert live
Participation libre au chapeau, au profit de la Frat'. Bar sans alcool sur place.
"""),
    E("898898142590173", "Bal-concert forró avec Gandaia na Ponte à Pornichet", "2026-01-21", "Quai des Arts, Pornichet", 100, """
Initiation : 19h15-20h
Bal et concert : 20h-22h
"""),
    E("843710045250914", "Brunch forró de la nouvelle année", "2026-01-11", "Salle polyvalente d'Avalix, 3 rue du Dr Calmette, Saint-Nazaire", None, """
Après la boum brasilidade, avant d'attaquer les stages forró : brunch forró en mode auberge espagnole. Tu ramènes un plat, on ramène le café.
Danse sur playlist forró pour réveiller les jambes sans les brusquer.
Dimanche, 12h–14h.
"""),
    E("1236676981845321", "Stages forró roots intensifs avec Cokelicô", "2026-01-10", "Salle Avalix, 3 rue du Docteur Calmette, Saint-Nazaire", None, """
Intensif de progression sur 6 cours d'une heure : l'essence du forró roots (connexion, équilibre, musicalité) et une vraie autonomie en bal.
Samedi 10 janvier : corps roots et musicalité, connexion roots, équilibre et mouvement, pratique libre guidée.
Dimanche 11 janvier : footwork roots, routine roots et créativité, pratique libre guidée.
En participant aux stages, vous devenez adhérent·e de l'association Les Pieds Ont Des Oreilles.
""", end="2026-01-11"),
    # ---------------- 2025 ----------------
    E("713569877891132", "Forró et Gandaia na Ponte au Bar Bar", "2025-11-29", "La Bodeguita, Saint-Nazaire", 97, """
Concert et bal forró avec Gandaia na Ponte, dans le cadre du festival Culture Bar Bar.
Gandaia na Ponte, ou « le bazar sur le pont », est un groupe nazairien de forró : guitare, zabumba, cavaquinho, triangle, pandeiro, chant et chœur. Gratuit.
"""),
    E("1362852982121365", "Bal-brunch forró au Nomad Café", "2025-11-09", "Nomad Café, allée des Myosotis, Saint-Nazaire", 96, """
On prolonge la fête après Forró na Chuva ! Bal-brunch forró au Nomad'Café, dimanche 9 novembre, de 12h à 15h.
Mode auberge espagnole (chacun peut apporter à manger, le bar sert café, thé et jus), playlist forró pour danser. Entrée libre et gratuite.
"""),
    E("2788341794703703", "Bal forró avec Gandaia na Ponte à la Bodeguita", "2025-09-12", "La Bodeguita, 7 rue du Bois Savary, Saint-Nazaire", 91, """
Concert et bal forró avec Gandaia na Ponte, à la Bodeguita de 20h à 23h. Gratuit.
"""),
    E("2520232065005955", "Bal forró place du Commando", "2025-09-06", "Place du Commando, Saint-Nazaire", 90, """
Un petit forró à Saint-Nazaire sur la place du Commando, de 18h30 à 20h30. Gratuit.
"""),
    E("1917119492447103", "Bal forró avec Seba do Forró à Méan-Penhoët", "2025-08-28", "Maison de quartier de Méan-Penhoët, 1 rue Émile Combes, Saint-Nazaire", 89, """
Gandaia est malade, Seba prend le relais pour les Terrasses de Méan.
Initiation à la danse forró à 20h, puis concert en intérieur ou en extérieur selon la météo, à la maison de quartier. Gratuit.
"""),
    E("1194354998416044", "Forró na rua avec Gandaia na Ponte", "2025-04-28", "Place du Commando, Saint-Nazaire", 79, """
Le concert de Méan-Penhoët ayant été annulé à cause du mauvais temps, Gandaia na Ponte joue place du Commando, de 18h à 21h environ. Gratuit.
"""),
    E("1003852998360090", "Brunch et jam forró", "2025-04-20", "Salle de convivialité de Saint-Marc, 46 bd Jules Dumont d'Urville, Saint-Nazaire", None, """
Pour terminer le week-end après le concert de Nandinho, brunch forró et JAM FORRÓ. Apportez vos instruments. Auberge espagnole, boissons fournies par le bar.
"""),
    E("24099788829621132", "Stages de danse forró avec Marion Lima", "2025-04-19", "École Gambetta, 67bis rue de Cardurand, Saint-Nazaire", None, """
À l'occasion du concert de Nandinho Barros, des stages de niveau international avec Marion Lima (Paris).
15h30-17h : forró tous niveaux, un stage transversal.
17h30-19h : danse à trois (apprendre à danser en trio, changer de partenaire au cours d'une danse).
Les deux stages sont adaptés à tous les niveaux, la maîtrise des pas de base est requise.
"""),
    E("9323188311108572", "Stage de samba no pé avec Tatiana Barros", "2025-03-15", "Salle de danse Gambetta, 67bis rue de Cardurand, Saint-Nazaire", None, """
Stage de « samba no pé » dirigé par Tatiana Barros, de 16h30 à 18h, tous niveaux. Le soir : concert carnavalesque à l'R du Temps.
"""),
    E("4085051218381068", "Concert de Caio Sete Cordas", "2025-02-11", "Saint-Nazaire", 74, """
Caio Constantino, installé à Lisbonne, est un guitariste hors pair de Pernambuco (Brésil). Choro, samba, forró et compositions (1h), suivi d'un forrozinho (petit bal forró).
19h : ouverture des portes. 19h30 : concert. 20h30 : bal forró. 22h : fin.
Participation libre et consciente (environ 10 €). Réservation obligatoire par e-mail. Soirée en mode auberge espagnole.
"""),
    # ---------------- 2024 ----------------
    E("891908939669064", "Concert de Léo Corrêa et Gandaia na Ponte à la Grande Tablée", "2024-10-12", "Devant l'hôtel de ville, Saint-Nazaire", 68, """
La Grande Tablée est une grande journée de festivité devant l'hôtel de ville : animations des associations et banquet convivial.
Pour clôturer la journée, concert forró avec Gandaia na Ponte augmenté de Léo Corrêa. Initiation à la danse et concert de 20h15 à 22h.
"""),
    E("412472688512902", "Concert forró avec le Trio Turbilhão (São Paulo)", "2024-09-21", "L'R du Temps, Saint-Nazaire", 67, """
Un groupe de forró brésilien composé uniquement de femmes, originaire de la région de São Paulo, qui joue un forró traditionnel pé-de-serra, grands classiques et compositions.
20h30 : ouverture des portes et initiation à la danse. 21h30 – minuit : concert. Minuit – 1h : playlist.
Réservation via HelloAsso (12 €).
"""),
    E("1238515137580236", "Place aux assos", "2024-09-07", "Place de l'Amérique Latine, Saint-Nazaire", 66, """
Nous serons à Place aux assos pour présenter nos activités de la saison 24-25. Venez nous rencontrer, papoter, faire de la musique avec nous. Sans oublier le mini-bal à 17h.
"""),
    E("1138767783866474", "Concert du Coletivo da Chuva", "2024-08-25", "Five-Oh, skatepark, boulevard Albert 1er, Saint-Nazaire", 64, """
Forró after-beach avec le Coletivo da Chuva, face à la mer, sur la terrasse en bois du Five-Oh.
18h : début du bal. 18h30 : concert. 21h30 : on baisse le son.
Participation libre et consciente (autour de 10 €). En cas de mauvais temps, repli dans une salle polyvalente de la ville.
"""),
    E("1192004295300093", "Côté plage : atelier danse, musique et bal forró", "2024-07-10", "Skatepark, Saint-Nazaire", 62, """
10h - 11h30 : atelier d'initiation à la danse forró
12h - 13h : atelier de musique forró
20h - 21h : bal forró
""", also=[("Côté plage : atelier de musique forró", "2024-08-21", "Esplanade Monsieur Hulot, Saint-Nazaire"),
           ("Côté plage : atelier danse, musique et bal forró", "2024-08-28", "Place du Commando, Saint-Nazaire")]),
    E("408919005460711", "Gandaia na Ponte aux Terrasses de Méan-Penhoët", "2024-07-18", "MQMP, Méan-Penhoët, Saint-Nazaire", 63, """
Jeudi 18 juillet, notre dernier événement forró avant la pause estivale. Invités par la maison de quartier de Méan-Penhoët aux Terrasses de Méan pour un concert/bal forró avec Gandaia na Ponte et Léo Corrêa.
À partir de 19h30, bal-concert à 20h. L'initiation à la danse a lieu tout le long du bal. Gratuit.
""", also=[("Gandaia na Ponte à la Flânerie du Brivet", "2024-07-18", "Méan-Penhoët, Saint-Nazaire")]),
    E("2519674174905866", "Gandaia na Ponte au festival Tintamarre et Charivari", "2024-07-06", "Place Nadia Boulanger, Saint-Nazaire", 61, """
Invités par la maison de quartier de la Bouletterie à leur festival Tintamarre et Charivari. Le concert est suivi de l'Arbre à Danser. Initiation à la danse à 17h.
""", other_org="Événement organisé par Gandaia na Ponte"),
    E("3754622404783063", "Fête de la musique forró/samba", "2024-06-21", "Place du Commando, Saint-Nazaire", 57, """
Bal forró/samba avec Léo Corrêa, Gandaia na Ponte, Forró da Quinta, Pitchipalapala et jam session. De 19h à 23h, place du Commando.
"""),
    E("1176314056719107", "Sambada do Brasil (jam forró/samba)", "2024-06-14", "Le Kiosq, Saint-Nazaire", 56, """
Jam session et bal forró/samba ouvert aux musiciens de tout bord, dirigée par l'artiste brésilien Léo Corrêa. Les musiciens interprètent les standards de forró et de samba pendant que le public danse. Participation libre (chapeau).
"""),
    E("2848129568671267", "Concert forró aux Grandes Marées de Saint-Nazaire", "2024-06-01", "Rond-point de Sautron, Saint-Nazaire", None, """
Lenilda Verissimo (voix, triangle) et Karine Huet (accordéon, chant), accompagnées d'Edu Vieira (zabumba, chant) et Sébastien Pacreau (percussions, batterie). Gratuit.
"""),
    E("1155438565493119", "Roda de forró/samba au skate park", "2024-05-09", "Guinguette Five-Oh, skate park, Saint-Nazaire", None),
    E("272284092588592", "Gandaia na Ponte au Plan B", "2024-04-11", "Le Plan B, 12 place du Marché, La Turballe", None, """
Initiation à la danse, concert et bal forró avec Gandaia na Ponte, groupe de forró de Saint-Nazaire. Participation libre au chapeau.
"""),
    E("1538539863443331", "Stage de danse forró avec Madame Forró", "2024-11-16", "Salle des Landettes, 44 chemin d'Avalix, Saint-Nazaire", None, """
Ce stage est ouvert à tous les danseurs de forró, tous niveaux confondus. Il faut avoir déjà dansé et maîtriser les pas de base.
Le thème sera la qualité de la danse et la musicalité. De 14h30 à 16h30 environ.
"""),
    E("1160460032052992", "Stage de danse forró pour salseros avancés", "2024-04-07", "Salle Kerfaouet, 12B rue des Pinsons, Saint-Nazaire", None, """
Dans le cadre du Gros Week-end Forró, Marion Lima, référence du forró en France, donne un stage réservé aux danseurs de salsa confirmés (au moins 2 ans de pratique régulière). Prix subventionné : 5 €, réservation obligatoire. Le cours est suivi du bal-jam forró à la P'tite Scène des Halles.
"""),
    E("959090411878481", "Gandaia na Ponte à la Soupe aux Cailloux (Trignac)", "2024-03-30", "8 rue Marie Thérèse Eyquem, Trignac", None, """
L'association La Soupe aux Cailloux inaugure son nouveau local avec « La Crémaillère au Crayon », une journée de festivité. Gandaia se donne en concert pour l'occasion : initiation à la danse à 18h30, concert de 19h à 20h. Gratuit.
""", other_org="Événement organisé par Gandaia na Ponte"),
    E("421281060341343", "Déambulation carnavalesque", "2024-03-02", "Ruban Bleu, devant l'R du Temps, Saint-Nazaire", None, """
Déambulation carnavalesque avec l'association Les pieds ont des oreilles. Départ à 15h place des Droits de l'Homme, puis 17h au Ruban Bleu devant l'R du Temps. Rendez-vous nombreux et déguisés !
""", other_org="Événement du Centre commercial Ruban Bleu"),
    E("804746254667289", "Stages de danses du Nordeste brésilien avec Marion Lima", "2024-01-06", "Salle de danse Hibiscus, 10B rue des Hibiscus, Saint-Nazaire", None, """
Marion Lima, la superprof internationale parisienne, est parmi nous pendant trois jours pour nous transmettre son art, sa joie, sa bonne humeur et son énergie légendaire.
Samedi 6 janvier, de 13h30 à 17h30.
"""),
    E("921099733005817", "Stages pour enfants : cirque et musique brésilienne", "2024-02-26", "La Volière, 60 rue de la Ville Halluard, Saint-Nazaire", None, """
Stages pour enfants de 3 à 11 ans, du lundi 26 février au vendredi 1er mars 2024, encadrés par un·e intervenant·e cirque de La Volière et un intervenant musique brésilienne de l'association.
Cirque : acrobatie, équilibres, jonglerie, agrès aériens. Musique brésilienne : jeux de rythmes, instruments brésiliens (pandeiro, agogo, zabumba, ganzas), chansons, fabrication de petits instruments de carnaval.
Les participants étaient invités au carnaval de l'association le samedi 2 mars.
""", end="2024-03-01"),
    E("425461139823579", "Bal un peu foutraque : musique brésilienne mais pas que…", "2024-02-16", "L'Appart, Saint-Nazaire", 48, """
Cours de forró, bal pop, musique brésilienne avec Léo Corrêa et Gandaia na Ponte, rock, métissage en tout genre, magie, restauration sur place.
""", other_org="Événement organisé par Belleville en mer"),
    # ---------------- 2023 ----------------
    E("2196209773903001", "Bal-jam forró de Noël", "2023-12-17", "La P'tite Scène des Halles, Saint-Nazaire", 45, """
Et si on fêtait la fin d'année avec une pratique forró de toute beauté ? Initiation à la danse à 18h30, début de la jam à 19h. Ouvert à tous les instruments, tous niveaux. Participation libre au chapeau.
"""),
    E("1418267489033422", "Concert et bal forró avec Madame Forró & Balanceio", "2023-11-18", "La P'tite Scène des Halles, Saint-Nazaire", 44, """
Madame Forró, française expatriée au Brésil, danseuse, clown, chanteuse et accordéoniste, accompagnée de Julian Biblocq (zabumba) et Isadora (triangle et voix). Concert de 18h à 22h30 à la P'tite Scène des Halles, jauge limitée à 60.
L'après-midi (14h-16h), stage de danse forró niveau intermédiaire : connexion, trava (blocage) et musicalité.
""", also=[("Stage de danse forró inter/avancé avec Madame Forró", "2023-11-18", "Ferme Couronnée, Saint-Nazaire")]),
    E("1023248488720428", "Gandaia au Bal de la Yole à Mesquer", "2023-10-27", "Rue des Artisans, Mesquer", None, """
Gandaia donne un concert forró pendant cette soirée organisée par l'association Le défi du traict. Au programme : ouverture du Bar Bar et restauration dès 19h, Gandaia na Ponte à 20h, puis Marcel Dorcel et son orchestre.
""", other_org="Soirée organisée par l'association Le défi du traict"),
    E("696779451966911", "Initiation forró et mini-bal avec l'asso Odyssée pour s'Aimer", "2023-10-15", "Gymnase Pierre et Marie Curie, 2 rue George Sand, Saint-Nazaire", None, """
Dans le cadre de l'événement « Corps et Danse », au profit des personnes malades, initiation forró (1h) suivie d'un mini-bal (1h), pour participer à la lutte contre le cancer.
""", other_org="Événement de l'association Odyssée pour s'Aimer"),
    E("223379203700094", "Bal-jam forró dirigé par Aline", "2023-09-24", "La P'tite Scène des Halles, Saint-Nazaire", 42, """
Un bal/jam forró dirigé par Aline Le Masson de Forró Na Chuva ! Apportez vos instruments, vos pieds et vos oreilles. Participation libre au chapeau.
"""),
    E("334831018870809", "Gandaia à la Terrasse du Bois Joalland", "2023-09-17", "Place Fernand Guériff, Saint-Nazaire", None, """
Gandaia en concert pour un bal forró au bord du lac ! Initiation à la danse, ambiance festive et conviviale. Gratuit, au chapeau.
"""),
    E("961674065099686", "Le forró au Forum des assos et mini-bal", "2023-09-09", "Place de l'Amérique Latine, Saint-Nazaire", None, """
Nous aurons notre stand, comme chaque année. Mini-concert et mini-bal forró de 17h30 à 18h30 sur la scène de la terrasse.
"""),
    E("574558621511412", "CHAMS trio : musiques de Palestine", "2023-07-07", "La P'tite Scène des Halles, Saint-Nazaire", None, """
CHAMS est un trio franco-palestinien en tournée dans l'ouest de la France : oud, percussions et violon, chansons populaires du Moyen-Orient, morceaux instrumentaux et compositions originales. Prix libre (conseillé 10 €).
""", other_org="Événement organisé par Dona Iemanjà"),
    E("117114931408911", "Fête de fin d'année du forró des Podos", "2023-06-15", "Place du Commando, Saint-Nazaire", None, """
Pour fêter la fin de l'année scolaire : bal forró, concert de fin d'année de l'atelier de musique forró et démonstrations de danse forró par les élèves des cours.
"""),
    E("206473685543073", "Forró Swing Party", "2023-06-11", "Maison de quartier Immaculée Beauregard, Saint-Nazaire", 38, """
La rencontre de deux associations passionnées de danse : un stage de lindy hop (15h - 16h15), un stage de forró (16h30 - 17h45), puis soirée dansante de 18h à 22h avec apéro partagé et une playlist métissée entre swing et forró.
Gratuit pour les adhérent·e·s des associations, 5 € pour les autres. Partenariat entre Kick&Swing et Les Pieds Ont Des Oreilles.
"""),
    E("758038075812548", "Apéro forró et Gandaia à Saint-Marc-sur-Mer", "2023-05-14", "59 route de l'Océan, Saint-Marc, Saint-Nazaire", 37, """
Dans le cadre du festival Mai des Arts à Saint-Marc, Gandaia na Ponte en concert à 21h30 dans un jardin particulier face à la mer. Apéro dès 20h. Gratuit.
""", also=[("Stage de danse forró avec Alise Marieta", "2023-05-14", "Salle des Hibiscus, Saint-Nazaire"),
           ("Ateliers de danse brésilienne enfants 4/6 et 7/12 ans", "2023-05-14", "Salle des Hibiscus, Saint-Nazaire")]),
    E("112704564995932", "Bal-jam forró do domingo", "2023-04-16", "La P'tite Scène des Halles, Saint-Nazaire", 35, """
Une jam forró animée par l'accordéoniste Aline Le Masson, avec en première partie le groupe nazairien Gandaia na Ponte.
""", also=[("Atelier batucada forró par Julian Biblocq", "2023-04-16", "Maison de quartier d'Avalix, Saint-Nazaire"),
           ("Ateliers de musique brésilienne enfants 4/6 et 7/12 ans", "2023-04-16", "Salle Jardin des Plantes, Saint-Nazaire")]),
    E("698866391730017", "Forró Belem en concert", "2023-04-01", "L'Appart, Saint-Nazaire", 36, """
Un concert forró avec le groupe nantais Forró Belem : cinq musiciens, un forró à la fois traditionnel, moderne et original (accordéon, zabumba, marimba, basse, guitare, voix, triangle).
20h : playlist forró. 20h15 : initiation à la danse. 21h : concert. Minuit : le bal continue. Billetterie limitée à 65 entrées. Concert complet.
"""),
    E("521549716555746", "Carnaval forró avec Saíra en concert", "2023-02-25", "La P'tite Scène des Halles, Saint-Nazaire", 34, """
C'est carnaval, déguisons-nous ! Du forró au coco, de la valse à la ciranda, Saíra, quartet franco-brésilien, invite à un bal brésilien populaire et chaleureux, inspiré du répertoire forró des années 70.
19h : ouverture des portes. 19h15 : initiation. 20h30 : concert. Prix libre entre 7 et 12 €.
""", also=[("Stages de danse forró avec Tatiana Barros", "2023-02-25", "Espace civique Dubé, Saint-Nazaire")]),
    E("1540140023173407", "Percussion corporelle et chant forró avec Gabriel + bal-jam", "2023-02-05", "Espace civique Dubé, 1 rue des Ajoncs, Saint-Nazaire", 33, """
Plongez dans l'univers rythmique du bal brésilien à travers la percussion corporelle et le chant : ciranda, xote, baião, arrastapé. Ateliers dirigés par Gabriel Lesoeur, suivis d'un bal-jam forró.
1re partie : 14h30 - 16h. 2e partie : 16h15 - 17h45. 15 € un stage, 25 € les deux.
""", also=[("Musique et percussion corporelle brésilienne pour les enfants", "2023-02-05", "Salle des Hibiscus, Saint-Nazaire")]),
    E("753316162879351", "Bal-jam forró do domingo", "2023-01-22", "La P'tite Scène des Halles, Saint-Nazaire", None, """
Et si on fêtait le début d'année avec une pratique forró de toute beauté ? Initiation à la danse à 18h30. Ouvert à tous les instruments, tous niveaux. Participation libre au chapeau.
"""),
    E("1852080865142997", "Brunch forró au Garage", "2023-01-08", "Le Garage, Saint-Nazaire", 32, """
Un brunch forró au Garage pour fêter la nouvelle année : apportez de quoi boire et manger, dansez les quadrilles. Initiation à la danse à 11h30. Gratuit. Suivi de deux ateliers de musique forró animés par Gabriel Lesoeur.
""", also=[("Stage de musique forró (niveau inter) avec Gabriel Lesoeur", "2023-01-08", "Les Landettes, Saint-Nazaire"),
           ("Stage de percussion corporelle et chant forró (pour tous)", "2023-01-08", "Les Landettes, Saint-Nazaire")]),
    # ---------------- 2022 ----------------
    E("671327771099586", "Bal-jam forró de Noël", "2022-12-18", "La P'tite Scène des Halles, Saint-Nazaire", 31, """
Une pratique forró pour fêter la fin d'année : initiation à la danse à 19h, début de la jam à 19h30. Ouvert à tous les instruments, tous niveaux. Participation libre au chapeau.
"""),
    E("5350782015032057", "Jam session forró avec Aline, Alise et Gabiju", "2022-11-06", "L'Appart, Saint-Nazaire", 30, """
Jam session au bar L'Appart, avec Aline Le Masson (accordéoniste de Forró Na Chuva), Alise et Gabiju. Apportez vos instruments ou votre voix, vos pieds et vos oreilles. Ouvert à tous les instruments, tous niveaux. Participation libre au chapeau.
""", also=[("Stage de percussions corporelles et musique forró", "2022-11-06", "Maison de quartier de la Bouletterie, Saint-Nazaire"),
           ("Stage de forró avec Alise Marieta (niveau intermédiaire)", "2022-11-06", "Maison de quartier Chesnaie-Trébale, Saint-Nazaire"),
           ("Stage danses du Nordeste avec Alise et Gabiju", "2022-11-06", "Maison de quartier Chesnaie-Trébale, Saint-Nazaire")]),
    E("1230757807756957", "Gros week-end forró avec Black do Acordeon", "2022-10-08", "Le Garage, Saint-Nazaire", 29, """
Un week-end de folie avec deux mestres du forró : Black do Acordeon (musique) et Rudolfo Batista (danse). Stages de danse, atelier de musique, concert et jam au Garage.
Black, chanteur, accordéoniste et compositeur, est un phénomène au Brésil : un forró aux influences de reggae, samba, ijexá et baião.
Rudolfo Batista, danseur, pédagogue, musicien et producteur, brésilien d'Olinda, installé à Cologne, propose un forró aux influences multiples (roots, universitaire, coco).
""", also=[("Stage d'initiation à la danse forró", "2022-10-08", "Le Garage, Saint-Nazaire"),
           ("Stages de danse forró avec Rudolfo Batista", "2022-10-08", "Le Garage, Saint-Nazaire"),
           ("Stages de musique forró avec Leandro Campanha", "2022-10-09", "Les Landettes, Saint-Nazaire")], end="2022-10-09"),
    E("1103338773940803", "The Forroscopic's à la P'tite Scène des Halles", "2022-09-10", "La P'tite Scène des Halles, Saint-Nazaire", 27, """
Premier concert forró à la P'tite Scène des Halles avec The Forroscopic's : un forró traditionnel qui s'éloigne des sentiers battus, dans un univers swingué, chaleureux et joyeux.
19h30 : DJ. 20h : initiation à la danse. 20h30 : concert. DJ jusqu'à minuit. Participation à partir de 5 €.
"""),
    E("395115526065405", "Le forró au Forum des assos", "2022-09-03", "Saint-Nazaire", None, """
Venez nous retrouver sur notre stand au Forum des Assos à Saint-Nazaire. À 16h, mini-bal forró !
"""),
    E("623727156092160", "Gandaia à Piriac (forró et samba)", "2022-08-25", "Le Barbichet, Piriac-sur-Mer", None, """
Gandaia na Ponte en concert à Piriac, face mer, au Barbichet. Deux sets de 45 min, du forró et de la samba autour de la paillote. Au chapeau.
"""),
    E("1554174908330645", "Forró les pieds dans le sable", "2022-07-20", "Plage de Pen Bron, La Turballe", None, """
Un forró sauvage sur une plage qui l'est tout autant ! Sable, mer limpide, bon son et coucher de soleil. Pensez aux maillots de bain et de quoi partager l'apéro.
"""),
    E("766905574494677", "Forró plage à Pornichet", "2022-07-12", "Plage de Bonne Source, à droite du restaurant Le Récif, Pornichet", None, """
Un premier forró à la plage sur la plage de Bonne Source, à droite du restaurant Le Récif.
"""),
    E("568631354731257", "Les cours de forró partent en vacances", "2022-07-06", "Place du Commando, Saint-Nazaire", None, """
Pour se dire bonnes vacances et fêter l'année de cours de forró, venez boire un coup et faire quelques pas, ce mercredi soir, place du Commando.
"""),
    E("448118103437824", "Gandaia na Ponte au festival Tintamarre et Charivari", "2022-07-02", "Saint-Nazaire", None, """
Gandaia na Ponte en concert de 20h à 21h au festival Tintamarre et Charivari.
"""),
    E("1647782312270035", "Gandaia na Ponte à Pornichet pour la fête de la musique", "2022-06-21", "Bar Plein Sud, plage des libraires, Pornichet", 25, """
Concert de Gandaia na Ponte pour la fête de la musique, de 19h30 à 22h : un mix de musiques brésiliennes, à tester en dansant forró et samba sur le sable.
"""),
    E("391178229094137", "Trio Alvorada en concert", "2022-06-18", "Entre chèvres et choux, Saint-Nazaire", 26, """
Le groupe de forró brésilien Trio Alvorada, venu de São Paulo, un groupe phare du forró au Brésil : zabumba, accordéon, basse, voix, triangle.
"""),
    E("979225439437716", "Brunch - jam forró", "2022-06-12", "Place du Commando, Saint-Nazaire", 23, """
Apporte de quoi grignoter un brunch et viens danser ou jouer le forró ! À midi, place du Commando.
"""),
    E("681194956281897", "Gandaia na Ponte dans les jardins de Saint-Marc", "2022-05-21", "Villa Plaisance, 59 route de l'Océan, Saint-Marc, Saint-Nazaire", 21, """
Dans le cadre de la journée des Arts dans les jardins, Gandaia na Ponte alterne entre forró et samba, de 20h à 21h15. Pelouse pour danser autour de la scène.
"""),
    E("1320866718404985", "The Forroscopic's sous les palmiers", "2022-05-14", "Sous les palmiers, la plage, Saint-Nazaire", 15, """
The Forroscopic's emmène sur les traces du forró traditionnel, dans un univers swingué, chaleureux, sensible et joyeux. Initiation à la danse : 18h30. Concert : 19h.
"""),
    E("480850830187719", "24h avec Forró à Lenha", "2022-04-30", "L'Appart, Saint-Nazaire", 20, """
Le groupe de forró toulousain Forró à Lenha, avec Lucas Notaro, Isaac Paiva et Eduardo Vieira, rejoints par Céline Costa du groupe Forroscopics, pour un moyen-gros week-end forró.
Samedi 30 avril : la grosse soirée. Ouverture des portes à 20h, concert à 21h (8/10/15 €).
Dimanche 1er mai : ateliers et jam.
""", end="2022-05-01"),
    E("643598106733834", "Jam session forró", "2022-04-03", "L'Appart, Saint-Nazaire", 22, """
Venez danser, découvrir, écouter, jouer le forró et terminer joyeusement le week-end. Apportez votre instrument et joignez-vous aux autres musiciens.
"""),
    E("1323739514766333", "Gros week-end forró avec Cacau et Forró Na Chuva", "2022-03-19", "L'Appart et Saint-Nazaire", 19, """
Grâce à la venue de Cacau Moutinho et Forró Na Chuva, un gros week-end forró à Saint-Nazaire.
Samedi 19 mars : stage débutant de musique forró (11h-13h), stages de danse niveaux 1 et 2, puis le gros concert à L'Appart (initiation, concert d'arrumadinho de Cacau et Forró Na Chuva, DJ set).
Dimanche 20 mars : stage avancé de musique avec Léo Corrêa, stages de danse niveaux 1 et 2, puis bal/jam forró à L'Appart.
""", also=[("Atelier de musique forró débutant avec Cacau", "2022-03-19", "Saint-Nazaire"),
           ("Stage de musique forró avancé", "2022-03-20", "Saint-Nazaire"),
           ("Atelier de pandeiro débutant", "2022-03-30", "École Carnot, Saint-Nazaire")], end="2022-03-20"),
    E("454440509657511", "Atelier de musique forró avec Léo Corrêa", "2022-02-22", "Saint-Nazaire", 17, """
Ateliers forró de Léo, pour monter un groupe de forró éphémère et apprendre à jouer 2 ou 3 forrós avec style. Léo Corrêa, musicien brésilien de São Paulo, est chanteur, joueur de rabeca, percussionniste, compositeur et luthier (Forró Na Chuva). 10 personnes maximum, 3h d'atelier : 20 €.
"""),
    E("449129056831320", "Forró Belem en concert à Assérac", "2022-02-05", "Assérac", 16, """
Concert du groupe forró nantais Forró Belem : cinq musiciens, un forró traditionnel, moderne et original. 19h : DJ-set. 21h : concert. 10 €. Complet.
"""),
    # ---------------- 2021 ----------------
    E("236195941474881", "Atelier et stage de musique forró du 26 septembre", "2021-09-26", "Saint-Nazaire", 10, """
Venez apprendre à jouer et improviser le forró, cette musique populaire du Nordeste brésilien. Tout instrument (hors percussion), un minimum de maîtrise instrumentale est nécessaire. Le stage est suivi d'un bœuf. 12 places, 25 €.
""", also=[("Atelier de percussions forró", "2021-09-26", "Saint-Nazaire"),
           ("Jam forró", "2021-09-26", "L'Appart, Saint-Nazaire")]),
    E("229772902535232", "Concert forró : The Forroscopics à Saint-Nazaire", "2021-12-17", "Sous les palmiers, la plage, Saint-Nazaire", None, """
The Forroscopics, le célèbre groupe de forró rennais, est de retour pour nous transporter dans le nordeste brésilien, au son de leurs voix, accordéons, triangle, zabumba et autre contrebasse ! Ça va groover le Brésil !
18h30 : initiation à la danse forró. 19h : concert. Entrée libre avec chapeau. Nous sommes dans un bar : boire un coup est obligatoire.
"""),
    E("2922167214762485", "Concert de Léo Corrêa e as Trovadoras Itinerantes", "2021-10-22", "L'Appart, Saint-Nazaire", 12, """
Léo Corrêa, musicien, compositeur et luthier de São Paulo, accompagné de Barbara (Forró Bacana), Julian (Forró Na Chuva) et de deux musiciennes du Nordeste, Josy et Luciana : les « trovadoras itinerantes ». Un bal brésilien à la sauce nordestine : forró, coco, ciranda, arrasta-pé, rabeca, accordéon.
19h30 : DJ-set. 20h : initiation à la danse forró. 21h : concert. 6 € sur le site, 7 € sur place.
""", also=[("Atelier de musique forró (tout instrument)", "2021-10-23", "Saint-Nazaire")]),
    E("4175728629162816", "Concert de Conterrâneos (Rio de Janeiro)", "2021-10-02", "L'Appart, Saint-Nazaire", 14, """
Les deux Rodrigos du groupe carioca Conterrâneos, en tournée européenne, accompagnés de Barbara de Trio Bacana, pour un concert exceptionnel au bar L'Appart.
20h : ouverture des portes + DJ. 21h30 : concert. 2h : fin de soirée. Jauge limitée à 60 personnes. 8 € / 11 € / 14 €.
""", also=[("Masterclass forró avec Rodrigo et Rodrigo de Conterrâneos", "2021-10-03", "Saint-Nazaire"),
           ("Stages forró avec Yse Góes", "2021-10-03", "Rue des Hibiscus, Saint-Nazaire")], end="2021-10-03"),
    E("", "Jam session forró avec Conterrâneos", "2021-10-03", "L'Appart, Saint-Nazaire", 14, """
Le lendemain du concert, jam session forró à L'Appart avec les deux Rodrigos de Conterrâneos.
"""),
    E("6096676037070012", "Mini-forró brunch sauvage à Saint-Marc", "2021-09-19", "12 rue du Commandant Charcot, Saint-Nazaire", None, """
Mini-bal forró à Saint-Marc, devant le manège, pour faire un petit coup de pub pour le forró à Saint-Nazaire. 11h : café. 11h30 : mini-bal. 12h : apéro.
"""),
    E("430815244949481", "Les Pieds Ont Des Oreilles au Forum des Assos", "2021-09-04", "Base sous-marine, Saint-Nazaire", None, """
Pour lancer la rentrée, nous serons au forum des assos de Saint-Nazaire, avec un mini-bal (et initiation) de 16h à 16h30.
"""),
    E("1154333601729415", "Bal populaire brésilien avec Forró Na Chuva", "2021-07-14", "L'Appart, Saint-Nazaire", 8, """
Forró na Chuva, littéralement « le forró sous la pluie », l'expression de la musique populaire du Nordeste brésilien sous le ciel de Bretagne : Léo Corrêa, Marion Limosino, Aline Le Masson et Julian Biblocq.
18h : DJ Juliano. 18h30 : initiation à la danse forró. 19h30 : concert. 23h : fin des hostilités. Prix libre au chapeau.
"""),
    E("210628207675457", "Bal forró au bois Joalland", "2021-08-15", "Terrasse du Bois Joalland, Saint-Nazaire", 9, """
Apprendre à danser le forró à la Terrasse du Bois Joalland. Initiation à la danse : 18h30. Bal avec DJ Juliano. Soirée gratuite.
"""),
    E("225329746025923", "Atelier percussion et chant forró", "2021-05-23", "La Baule-Escoublac", None, """
Atelier de percussion et chant avec Léo de Forró Na Chuva.
"""),
    # ---------------- 2020 ----------------
    E("1262267384115748", "Forró Na Chuva en concert au Trou du Fût", "2020-10-09", "Le Trou du Fût, Saint-Nazaire", 6, """
Forró na Chuva, le « forró sous la pluie » : Léo Corrêa, Marion Limosino, Aline Le Masson et Julian Biblocq. Prix libre au chapeau.
"""),
    E("579888119365885", "Concert brésilien avec Forró De Um Dia", "2020-08-01", "Guinguette La Bara-K, Saint-Nazaire", 5, """
Un trio de forró festif : Céline Costa (voix et percussion), Manu Mezalma (accordéon, voix, percussion) et Tatiana Barros (percussion, voix). En extérieur, face mer. Atelier d'initiation à la danse de 18h à 18h30. Participation libre.
"""),
    E("1081864418823735", "Concert carnavalesque avec Forró De Um Dia", "2020-02-23", "L'Appart, Saint-Nazaire", 3, """
Le groupe Forró de Um Dia pour « pular o carnaval », avec Céline Costa, Manu Mezalma et Tatiana Barros. Thème : paillettes et plumes ! Atelier de danses brésiliennes gratuit de 17h à 18h, concert à 18h30. Participation libre.
""", also=[("Atelier danses brésiliennes avec Tatiana Barros", "2020-02-23", "L'Appart, Saint-Nazaire")]),
]

# Séries régulières : une page par série, avec la liste des dates.
SERIES = [
    dict(slug="forro-de-l-appart-2020", title="Forró de l'Appart et Afterbeach (2020)", date="2020-01", poster=0,
         intro="Les rendez-vous forró au bar L'Appart, à Saint-Nazaire, et les afterbeach de l'été 2020.",
         dates=[("2020-01-26", "Forró à l'Appart"), ("2020-04-26", "Forró à l'Appart"), ("2020-07-17", "Forró à l'Appart"),
                ("2020-07-24", "Forró Afterbeach de l'Appart"), ("2020-08-07", "Forró Afterbeach de l'Appart"),
                ("2020-08-21", "Forró Afterbeach de l'Appart"), ("2020-08-30", "Forró Afterbeach de l'Appart"),
                ("2020-10-04", "Forró de l'Appart"), ("2020-10-11", "Forró de l'Appart")]),
    dict(slug="ateliers-forro-2020", title="Ateliers forró (2020)", date="2020-01", poster=None,
         intro="Ateliers de forró à Pornichet et à Saint-Nazaire.",
         dates=[("2020-01-25", "Atelier forró à Pornichet (Hôtel Le Danicheff)"), ("2020-03-19", "Atelier forró le jeudi à Pornichet (Hôtel Le Danicheff)"),
                ("2020-03-21", "Atelier forró à Saint-Nazaire")]),
    dict(slug="cours-forro-2020", title="Cours de forró à Saint-Nazaire (2020)", date="2020-09", poster=None,
         intro="Reprise des cours de forró à Saint-Nazaire.",
         dates=[("2020-09-07", "Cours de forró"), ("2020-09-14", "Cours de forró"), ("2020-12-14", "Cours de forró")]),
    dict(slug="apero-forro-appart-2021", title="Apéro-forró à l'Appart (2021)", date="2021-05", poster=0,
         intro="Les apéro-forró du dimanche au bar L'Appart, à Saint-Nazaire, au printemps et à l'été 2021.",
         dates=[("2021-05-30", "Apéro-forró à l'Appart"), ("2021-06-06", "Apéro-forró à l'Appart"), ("2021-06-20", "Apéro-forró à l'Appart"),
                ("2021-06-27", "Apéro-forró à l'Appart"), ("2021-07-04", "Apéro-forró à l'Appart"), ("2021-07-18", "Apéro-forró à l'Appart"),
                ("2021-08-29", "Apéro-forró à l'Appart"), ("2021-09-05", "Apéro-forró à l'Appart"), ("2021-09-12", "Apéro-forró à l'Appart"),
                ("2021-09-19", "Apéro-forró à l'Appart")]),
    dict(slug="bals-forro-du-dimanche-appart-2022", title="Bals forró du dimanche à l'Appart (2021-2022)", date="2021-12", poster=0,
         intro="Le bal forró du dimanche au bar L'Appart, à Saint-Nazaire, de décembre 2021 à novembre 2022.",
         dates=[("2021-12-19", "Bal forró du dimanche"), ("2022-02-27", "Bal forró du dimanche"), ("2022-03-06", "Bal forró du dimanche"),
                ("2022-03-13", "Bal forró du dimanche"), ("2022-03-27", "Bal forró du dimanche"), ("2022-04-24", "Bal forró du dimanche"),
                ("2022-05-22", "Forró du dimanche"), ("2022-05-29", "Forró du dimanche"), ("2022-09-04", "Forró do domingo"),
                ("2022-09-25", "Forró do domingo"), ("2022-10-02", "Forró do domingo"), ("2022-10-16", "Forró do domingo"),
                ("2022-11-27", "Forró do domingo")]),
    dict(slug="apero-forro-commando", title="Apéro-forró place du Commando (2022-2023)", date="2022-08", poster=None,
         intro="Apéro-forró sur la place du Commando, à Saint-Nazaire.",
         dates=[("2022-08-30", "Apéro-forró à Saint-Nazaire"), ("2023-05-28", "Apéro-forró à Saint-Nazaire"), ("2023-06-04", "Apéro-forró à Saint-Nazaire")]),
    dict(slug="forro-do-domingo-dube-2023", title="Forró do domingo et pratiques à l'espace Dubé (2023-2024)", date="2023-11", poster=None,
         intro="Les forró do domingo et pratiques forró à l'espace civique Dubé, à Saint-Nazaire.",
         dates=[("2023-11-12", "Forró do domingo"), ("2023-11-26", "Forró do domingo"), ("2023-12-03", "Forró do domingo"),
                ("2023-12-10", "Forró do domingo"), ("2023-12-22", "Juste une pratique forró"), ("2024-01-21", "Juste une pratique forró")]),
    dict(slug="portes-ouvertes", title="Portes ouvertes des cours (2021-2025)", date="2021-09", poster=60,
         intro="Les portes ouvertes des cours de danse et de musique forró, à chaque rentrée.",
         dates=[("2021-09-29", "Porte ouverte cours de forró, École Carnot"), ("2022-09-06", "Porte ouverte cours de danse forró, École Carnot"),
                ("2022-09-08", "Porte ouverte cours de musique forró avec Léo Corrêa, École Carnot"),
                ("2022-09-15", "Porte ouverte cours de musique forró avec Léo Corrêa, École Carnot"),
                ("2023-09-13", "Porte ouverte ateliers de musique brésilienne enfants-parents, groupe scolaire Andrée Chedid"),
                ("2023-09-26", "Porte ouverte cours de danse forró, École Carnot"), ("2023-09-28", "Porte ouverte cours de musique forró, École Carnot"),
                ("2023-10-31", "Porte ouverte cours de batucada samba carioca, École Jean-Zay"),
                ("2024-07-04", "Les portes ouvertes des Pieds ont des oreilles, École Carnot"),
                ("2024-09-10", "Portes ouvertes danse et musique forró pour enfants et adultes"),
                ("2024-09-25", "Portes ouvertes ateliers de musique brésilienne enfants"),
                ("2025-09-12", "Portes ouvertes cours hebdo de danse forró"), ("2025-09-16", "Portes ouvertes cours hebdo de danse forró"),
                ("2025-09-19", "Portes ouvertes cours hebdo de danse forró"), ("2025-09-23", "Portes ouvertes cours hebdo de danse forró"),
                ("2025-09-25", "Portes ouvertes cours hebdo de musique du Nordeste brésilien"),
                ("2025-09-26", "Portes ouvertes cours hebdo de danse forró"), ("2025-09-30", "Portes ouvertes cours hebdo de danse forró"),
                ("2025-10-02", "Portes ouvertes cours hebdo de musique du Nordeste brésilien"),
                ("2025-10-03", "Portes ouvertes cours hebdo de danse forró"),
                ("2025-10-09", "Portes ouvertes cours hebdo de musique du Nordeste brésilien")]),
    dict(slug="ateliers-hebdo-coco-2024", title="Ateliers hebdo de coco et cours hebdo (2024)", date="2024-04", poster=52,
         intro="Ateliers hebdomadaires de coco, chant et percussions brésiliennes avec Léo Corrêa, et cours hebdo de danse forró.",
         dates=[("2024-04-10", "Ateliers hebdo de coco, chant et percussions brésiliennes avec Léo Corrêa (salle Lamartine)"),
                ("2024-04-24", "Ateliers hebdo de coco, chant et percussions brésiliennes avec Léo Corrêa (salle Lamartine)"),
                ("2024-06-26", "Ateliers hebdo de coco, chant et percussions brésiliennes avec Léo Corrêa (salle Lamartine)"),
                ("2024-09-24", "Cours hebdo de danse forró (École Carnot)"),
                ("2024-09-26", "Ateliers hebdo de musique brésilienne (forró, coco…), École Carnot"),
                ("2024-10-01", "Cours hebdo de danse forró (École Carnot)")]),
    dict(slug="pratiques-forro-2025-2026", title="Pratiques forró (2025-2026)", date="2025-04", poster=76,
         intro="Les pratiques de forró : place du Commando, au Five-Oh du skate park et à la salle Gambetta.",
         dates=[("2025-04-08", "Pratique forró, place du Commando"), ("2025-06-24", "Pratique forró, place du Commando"),
                ("2025-07-01", "Pratique forró, Five-Oh du skate park"), ("2025-10-28", "Pratique forró, salle Gambetta"),
                ("2026-02-01", "Pratique forró à Saint-Nazaire"), ("2026-03-29", "Pratique forró, salle Gambetta"),
                ("2026-05-17", "Pratique forró, salle Gambetta"), ("2026-06-09", "Pratique forró au Five-Oh"),
                ("2026-06-16", "Pratique forró au Five-Oh"), ("2026-06-23", "Pratique forró au Five-Oh"),
                ("2026-06-30", "Pratique forró au Five-Oh"), ("2026-07-21", "Pratique forró au Five-Oh"),
                ("2026-08-18", "Pratique forró au Five-Oh"), ("2026-09-01", "Pratique forró au Five-Oh")]),
]

# Affiches du disque dur déjà reprises (via FB ou séries) ou à écarter : elles ne sont pas republiées en « mois seul ».
DROP_POSTERS = [78, 28, 84, 86, 94]
