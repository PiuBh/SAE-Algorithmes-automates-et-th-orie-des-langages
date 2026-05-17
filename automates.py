"""
Partie 1.3 et suivantes : Automates
Un automate est un dictionnaire avec les cles :
   "alphabet"    : liste de lettres
   "etats"       : liste d'etats
   "transitions" : liste de transitions [depart, lettre, arrivee]
   "I"           : liste des etats initiaux
   "F"           : liste des etats finaux
"""
from langages import tousmots


"""
Fonctions auxiliaires (utilisees a plusieurs endroits)
"""
def indice(lst, x):
    #cherche la position de x dans lst, retourne -1 si pas trouvé
    #utilisé dans renommage
    for i in range(len(lst)):
        if lst[i] == x:
            return i
    return -1


def saisir_liste_entiers(message):
    #affiche un message, attend que l'utilisateur écrit des nombres séparés par des espaces  et retourne une liste d'entier sans doublons
    chaine = input(message).split()
    resultat = []
    for s in chaine:
        n = int(s)
        if n not in resultat: #évite les doublons
            resultat.append(n)
    return resultat


def existe_transition(T, etat, lettre):
    #vérifie s'il existe une transition dans T qui part de l'état avec lettre, retourne true si c'est vrai sinon false, utilisé dans complet et complete pour vérifier si une transition manque
    for t in T:
        if t[0] == etat and t[1] == lettre:
            return True
    return False

"""
Partie 1.3 : Automates (saisie et lecture)
"""

"""
Question 1.3.1
Definir une fonction defauto qui permet de faire la saisie d'un automate (sans doublon).
"""
def defauto():
    #crée un automate vide, puis remplit le champ par champ via des saisies clavier.
    auto = {}
    #lettre séparer par des espaces et split qui découpe en liste
    auto["alphabet"] = input("Alphabet (separe par des espaces) : ").split()
    #utilise saisir_liste_entiers pour récupérer des entiers sans doublons
    auto["etats"] = saisir_liste_entiers("Etats : ")
    auto["I"] = saisir_liste_entiers("Etats initiaux : ")
    auto["F"] = saisir_liste_entiers("Etats finaux : ")
    
    #demande d'abord combien il y en a, puis on les saisit une par une au format "0 a 1" et split découpe, on converti départ et arrivé en int et la lettre reste en str
    auto["transitions"] = []
    nb = int(input("Nombre de transitions : "))
    for i in range(nb):
        t = input("Transition (depart lettre arrivee) : ").split()
        transition = [int(t[0]), t[1], int(t[2])]
        # évite les doublons
        if transition not in auto["transitions"]:
            auto["transitions"].append(transition)
    return auto


"""
Question 1.3.2
Definir une fonction lirelettre qui, etant donnes une liste de transitions T, une liste d'etats E et une lettre a, renvoie la liste des etats atteignables depuis E en lisant a.
"""
#utilisé dans liremot pour lire lettre par lettre, dans determinise pour calculer où on va depuis un ensemble d'états, dans produit même raison et enfin raffiner dans la minimisation.
def lirelettre(T, E, a):
    resultat = []
    #parcourt toute les transitions T
    for transition in T:
        #vérifie si le départ de la transition est dans la liste d'états courants E et vérifie si la lettre transition[1] est bien la lettre a qu'on cherche.
        if transition[0] in E and transition[1] == a:
            if transition[2] not in resultat:
                #si tout est vraie on ajoute l'état d'arrivé qui est transition[2] au résultat, sans doublon
                resultat.append(transition[2])
    return resultat


"""
Question 1.3.3
Definir une fonction liremot qui, etant donnes T, une liste d'etats E et un mot m, renvoie les etats atteignables depuis E en lisant le mot m.
"""
#utilisé dans accepte pour vérifier si un mot est accepté
def liremot(T, E, m):
    etats_courants = E
    #lecture d'un mot entier lettre par lettre, a chaque étape elle appelle lirelettre avec la lettre courante et le résultat devient les nouveaux états courants pour la lettre suivante
    for lettre in m:
        etats_courants = lirelettre(T, etats_courants, lettre)
    return etats_courants

 
"""
Question 1.3.4
Definir une fonction accepte qui renvoie True si le mot m est accepte par l'automate.
"""
def accepte(auto, m):
    #elle prend un automate et un mot m en paramètre, utilise liremot pour calculer les états qu'on peut atteindre en lisant m depuis les états initiaux de l'automate, et vérifie si au moins un de ces états est final, si oui elle retourne true sinonn false.
    etats_arrives = liremot(auto["transitions"], auto["I"], m)
    #Accepte si au moins un etat final a ete atteint.
    for etat in etats_arrives:
        if etat in auto["F"]:
            return True
    return False


"""
Question 1.3.5
Definir une fonction langage_accept qui renvoie la liste des mots de longueur inferieure a n acceptes par l'automate.
"""
def langage_accept(auto, n):
    #elle prend un automate et un entier n en paramètre, génère tous les mots possibles jusqu'à longueur n avec tousmots 
    resultat = []
    for mot in tousmots(auto["alphabet"], n):
        #pour chaque mot elle appelle accepte pour vérifier s'il est reconnu par l'automate
        if accepte(auto, mot):
            #si oui on ajoute le mot au résultat
            resultat.append(mot)
    return resultat


"""
Question 1.3.6
Pourquoi ne peut-on pas faire une fonction qui renvoie le langage accepte par un automate ?

Reponse :
Un automate peut accepter un langage infini (par exemple une boucle sur la lettre 'a' accepte a, aa, aaa, ... sans fin). 
Mais une fonction Python doit se terminer, enumerer une infinite de mots ferait tourner la fonction indefiniment. 
C'est pour ça que langage_accept prend un entier n qui borne la longueur des mots consideres.
"""

"""
Partie 2 : Determinisation
"""

"""
Question 2.1
Definir une fonction deterministe qui renvoie True si l'automate est deterministe, False sinon.
"""
# rappel de la definition: un automate est déterministe si deux conditions sont respectés: condition 1 quand on a un seul état initial. Condition 2 pas deux transitions avec le même départ et la même lettre
def deterministe(auto):
    #Vérifie la condition 1: un seul état initial
    if len(auto["I"]) != 1:
        return False
    T = auto["transitions"]
    #Vérifie la condition 2: pas deux transitions avec le même départ et la même lettre avec deux boucles sur toutes les paires de transitions (i, j)
    for i in range(len(T)):
        for j in range(len(T)):
            if i != j and T[i][0] == T[j][0] and T[i][1] == T[j][1]:
                return False
    return True


"""
Question 2.2
Definir une fonction determinise qui determinise l'automate.
"""
def determinise(auto):
    etat_init = auto["I"] #etat initial = liste des états initiaux
    etats = [etat_init] #liste des nouveaux états, on commence avec [0]
    transitions = [] #nouvelles transitions, vide au départ
    a_traiter = [etat_init] #file d'attente des états à traiter, on commence avec [0]


    while len(a_traiter) > 0:
        courant = a_traiter[0] #on prend le premier état de la file
        a_traiter = a_traiter[1:] #on le retire de la file
        #pour chaque lettre de l'alphabet, on calcule où on peut aller depuis l'état courant avec lirelettre
        for lettre in auto["alphabet"]:
            arrivee = lirelettre(auto["transitions"], courant, lettre)
            if len(arrivee) > 0:
                if arrivee not in etats:
                    etats.append(arrivee)
                    a_traiter.append(arrivee)
                transitions.append([courant, lettre, arrivee])

    #un nouvel état est final s'il contient au moins un état final de l'ancien automate
    finals = []
    for etat in etats:
        for f in auto["F"]:
            if f in etat and etat not in finals:
                finals.append(etat)

    return {"alphabet": auto["alphabet"], "etats": etats,
            "transitions": transitions, "I": [etat_init], "F": finals}


"""
Question 2.3
Definir une fonction renommage qui renomme les etats avec les premiers entiers (0, 1, 2, ...).
"""
def renommage(auto):
    #utilisé dans main après determinise et avant complement, inter, difference et minimise, elle vise a renommer les états par son numéro de poisition dans la liste des états. Le premier état devient 0, deuxième 1, etc.
    nouveaux_etats = []
    for i in range(len(auto["etats"])):
        nouveaux_etats.append(i)
    
    #Pour chaque transition, on remplace l'état de départ et l'état d'arrivé par leur position dans la liste des états. La lettre t[1] ne change pas.
    nouvelles_transitions = []
    for t in auto["transitions"]:
        depart = indice(auto["etats"], t[0])
        arrivee = indice(auto["etats"], t[2])
        nouvelles_transitions.append([depart, t[1], arrivee])

    #Même principes que pour les états initiaux et finaux: on remplace par sa position dans la liste des états, c'est ici qu'on va utiliser indice.
    nouveaux_I = []
    for etat in auto["I"]:
        nouveaux_I.append(indice(auto["etats"], etat))

    nouveaux_F = []
    for etat in auto["F"]:
        nouveaux_F.append(indice(auto["etats"], etat))

    return {"alphabet": auto["alphabet"], "etats": nouveaux_etats,
            "transitions": nouvelles_transitions,
            "I": nouveaux_I, "F": nouveaux_F}


"""
Partie 3 : Complementation
"""

"""
Question 3.1
Definir une fonction complet qui renvoie True si l'automate est complet, False sinon.
"""
def complet(auto):
    #Rappel de la def: un automate est complet si depuis chaque état, pour chaque lettre de l'alphabet, il existe au moins une transition. Elle est utilisé dans le complement pour vérifié si on doit compléter avant d'inverser les états finaux.
    #On a une double boucle pour chaque état et pour chaque lettre, on vérifie avec existe_transition 
    for etat in auto["etats"]:
        for lettre in auto["alphabet"]:
            if not existe_transition(auto["transitions"], etat, lettre):
                return False
    return True


"""Question 3.2
Definir une fonction complete qui complete l'automate en ajoutant un etat puits.
"""
def complete(auto):
    #Role elle prend un automate incomplet et le complète en ajoutant un état puits. Utilisé dans complement et difference
    #Copies pour ne pas modifier l'automate d'origine.
    nouveaux_etats = auto["etats"][:]
    nouvelles_transitions = auto["transitions"][:]

    #Recherche manuelle du plus grand etat pour fabriquer un nouvel etat plus grand que tous les autres.
    maxi = auto["etats"][0]
    for e in auto["etats"]:
        if e > maxi:
            maxi = e
    puits = maxi + 1
    puits_utilise = False

    #Pour chaque (etat, lettre) sans transition : on en cree une vers le puits.
    for etat in auto["etats"]:
        for lettre in auto["alphabet"]:
            if not existe_transition(auto["transitions"], etat, lettre):
                nouvelles_transitions.append([etat, lettre, puits])
                puits_utilise = True

    #Le puits boucle sur lui-meme pour toutes les lettres.
    if puits_utilise:
        nouveaux_etats.append(puits)
        for lettre in auto["alphabet"]:
            nouvelles_transitions.append([puits, lettre, puits])

    return {"alphabet": auto["alphabet"], "etats": nouveaux_etats,
            "transitions": nouvelles_transitions,
            "I": auto["I"], "F": auto["F"]}


"""
Question 3.3
Definir une fonction complement qui renvoie un automate acceptant le complementaire du langage.
"""
def complement(auto):
    #Role: construit l'automate qui reconnaît l'opposé du langage. Tout mot rejeté avant est accepté, tout mot accepté avant est rejeté
    #On determinise et renomme, puis on completer et enfin on echange les etats finaux et non finaux.
    a = renommage(determinise(auto))
    a = complete(a)
    nouveaux_F = []
    for etat in a["etats"]:
        if etat not in a["F"]:
            nouveaux_F.append(etat)
    a["F"] = nouveaux_F
    return a


"""
Partie 4 : Automate produit (intersection et difference)
"""

"""
Fonction auxiliaire : construit l'automate produit de a1 et a2.
Les etats sont des paires (p, q). Cette fonction ne fixe PAS les etats finaux : inter et difference le feront, car c'est le seul point qui differe entre les deux.
"""
def produit(a1, a2):
    #Role: construit un automate dont les états sont des paires (p, q) où p vient de a1 et q vient de a2. On avance dans les deux automates en même temps
    etat_init = (a1["I"][0], a2["I"][0]) #état initial = paire des deux états initiaux
    etats = [etat_init] #liste des états du produit, on commence avec (0,0)
    transitions = [] #transitions du produit, vide au départ
    a_traiter = [etat_init] #file d'attente, même principe que determinise

    while len(a_traiter) > 0:
        courant = a_traiter[0]
        a_traiter = a_traiter[1:]
        #même principe que determinise, on traite les états un par un
        for lettre in a1["alphabet"]:
            arr1 = lirelettre(a1["transitions"], [courant[0]], lettre) #où va a1
            arr2 = lirelettre(a2["transitions"], [courant[1]], lettre) #où va a2
            #Transition seulement si les deux composantes lisent la lettre.
            if len(arr1) > 0 and len(arr2) > 0:
                nouvel_etat = (arr1[0], arr2[0]) #on forme la nouvelle paire
                if nouvel_etat not in etats: #si c'est nouveau
                    etats.append(nouvel_etat) #on l'ajoute aux états
                    a_traiter.append(nouvel_etat) #on l'ajoute à la file
                transitions.append([courant, lettre, nouvel_etat]) #on ajoute la transition

    return {"alphabet": a1["alphabet"], "etats": etats,
            "transitions": transitions, "I": [etat_init], "F": []}


"""
Question 4.1
Definir une fonction inter qui renvoie l'automate produit acceptant l'intersection L1 inter L2.
"""
def inter(a1, a2):
    #utilise produit, puis définit les états finaux
    a = produit(a1, a2)
    #(p, q) final si p final dans a1 ET q final dans a2.
    finals = []
    for etat in a["etats"]:
        if etat[0] in a1["F"] and etat[1] in a2["F"]:
            finals.append(etat)
    a["F"] = finals
    return a


"""
Question 4.2
Definir une fonction difference qui renvoie l'automate produit acceptant la difference L1 \\ L2.
La consigne precise : completer les automates avant le produit.
"""
def difference(a1, a2):
    #utilise produit (après avoir complété les deux automates), puis définit les états finaux
    a1 = complete(a1)
    a2 = complete(a2)
    a = produit(a1, a2)
    # (p, q) final si p final dans a1 ET q PAS final dans a2.
    finals = []
    for etat in a["etats"]:
        if etat[0] in a1["F"] and etat[1] not in a2["F"]:
            finals.append(etat)
    a["F"] = finals
    return a



"""
Partie 5 : Proprietes de fermeture (automate emonde attendu)
Constructions du TD4 exercice 3. Hypothese : l'automate d'entree est emonde (tous les etats sont accessibles ET co-accessibles).
"""

"""
Question 5.1
prefixe : automate acceptant les prefixes des mots de L.
"""
def prefixe(auto):
    #Renvoie un automate qui accepte tous les préfixes des mots de L.
    # Emonde => depuis tout etat on atteint encore un final, donc tous les etats deviennent finaux.
    return {"alphabet": auto["alphabet"], "etats": auto["etats"],
            "transitions": auto["transitions"],
            "I": auto["I"], "F": auto["etats"]}


"""
Question 5.2
suffixe : automate acceptant les suffixes des mots de L.
"""
def suffixe(auto):
    #Renvoie un automate qui accepte tous les suffixes des mots de L
    # Emonde => même principe que pour les préfixes, sauf que tous les états deviennent initiaux au lieu de finaux
    return {"alphabet": auto["alphabet"], "etats": auto["etats"],
            "transitions": auto["transitions"],
            "I": auto["etats"], "F": auto["F"]}


"""
Question 5.3
facteur : automate acceptant les facteurs des mots de L.
"""
def facteur(auto):
    #Renvoie un automate qui accepte tous les facteurs des mots de L
    #Combinaison de prefixe et suffixe : tous les etats deviennent a la fois initiaux et finaux.
    return {"alphabet": auto["alphabet"], "etats": auto["etats"],
            "transitions": auto["transitions"],
            "I": auto["etats"], "F": auto["etats"]}


"""
Question 5.4
miroir : automate acceptant les miroirs des mots de L.
"""
def miroir(auto):
    #renvoie un automate qui accepte les miroirs des mots de L
    #On inverse chaque transition [p, a, q] -> [q, a, p], et on echange etats initiaux et finaux.
    nouvelles_transitions = []
    for t in auto["transitions"]:
        nouvelles_transitions.append([t[2], t[1], t[0]])
    return {"alphabet": auto["alphabet"], "etats": auto["etats"],
            "transitions": nouvelles_transitions,
            "I": auto["F"], "F": auto["I"]}


"""
Partie 6 : Minimisation (algorithme de Moore)
Entree : automate deterministe et complet. On partitionne les etats en classes (finaux / non finaux au depart), puis on raffine jusqu'a stabilite (equivalence de Nerode).
"""

#Renvoie la classe (liste d'etats) qui contient etat, ou None. Utilisé dans raffiné.
def trouver_classe(etat, classes):
    #parcourt toute les classes 
    for classe in classes:
        #vérifie si l'état est dedans
        if etat in classe:
            return classe #Si oui retourne cette classe
    return None #si l'état n'est dans aucune classe, retourne None


# prend la partition actuelle et la raffine, elle sépare les états qui ne se comportent pas pareil
# Produit une partition plus fine : deux etats restent ensemble si, pour chaque lettre, ils menent dans la meme classe. Si pour une lettre ils vont dans des classes différentes on les sépare.
def raffiner(classes, auto):
    #On parcourt chaque classe de la partition actuelle, et on va la découper en sous-classes.
    nouvelles_classes = []
    for classe in classes:
        #place = est ce que cet état a trouvé une sous-classe compatible? Au départ non
        sous_classes = []
        for etat in classe:
            place = False
            #On vérifie si l'état est compatible avec une sous-classe existante:
            #Pour chaque sous-classe déjà créée, on vérifie lettre par lettre si l'état est compatible avec le représentant de cette sous-classe (sc[0] = premier état de la sous-classe)
            for sc in sous_classes:
                compatible = True
                for lettre in auto["alphabet"]:
                    #test de compatibilité
                    arr_etat = lirelettre(auto["transitions"], [etat], lettre)
                    arr_sc = lirelettre(auto["transitions"], [sc[0]], lettre)
                    #on calcul où va etat et où va sc[0] avec cette lettre.
                    #Si les deux ont une transition, on vérifie s'ils vont dans la même classe. Si classes différentes ce n'est pas compatible.
                    if len(arr_etat) > 0 and len(arr_sc) > 0:
                        if trouver_classe(arr_etat[0], classes) != \
                           trouver_classe(arr_sc[0], classes):
                            compatible = False
                    elif arr_etat != arr_sc:
                        compatible = False
                if compatible:
                    sc.append(etat) #on ajoute l'état à cette sous-classe
                    place = True
                    break #on arrête de chercher
            if not place:
                sous_classes.append([etat]) #l'état crée sa propre sous-classe
        for sc in sous_classes:
            nouvelles_classes.append(sc) #on ajoute toutes les sous-classes créées aux nouvelles classes.
    return nouvelles_classes


#Role: construit l'automate minimal en utilisant raffiner jusqu'à stabilité, puis construit le nouvel automate à partir des classes.
def minimise(auto):
    # Partition de départ: on sépare les états en deux groupes finaux et non finaux
    finaux = auto["F"][:]
    non_finaux = []
    for e in auto["etats"]:
        if e not in auto["F"]:
            non_finaux.append(e)

    classes = []
    if len(finaux) > 0:
        classes.append(finaux)
    if len(non_finaux) > 0:
        classes.append(non_finaux)

    #Rafinnement jusqu'à stabilité: on raffine jusqu'à ce que la partition ne change plus
    while True:
        nouvelles = raffiner(classes, auto)
        if nouvelles == classes:
            break
        classes = nouvelles

    #Transitions : un representant (premier etat) par classe.
    nouvelles_transitions = []
    #Construction des transitions: Pour chaque classe, on prend le représentant classe[0] et on calcule ses transitions. La classe d'arrivée devient l'état d'arrivée.
    for classe in classes:
        for lettre in auto["alphabet"]:
            arr = lirelettre(auto["transitions"], [classe[0]], lettre)
            if len(arr) > 0:
                cl_arr = trouver_classe(arr[0], classes)
                nouvelles_transitions.append([classe, lettre, cl_arr])

    nouveaux_I = []
    #Etats initiaux et finaux: Une classe est initial si elle contient un état initial de l'ancien automate. Même principe pour les finaux.
    for classe in classes:
        for i in auto["I"]:
            if i in classe and classe not in nouveaux_I:
                nouveaux_I.append(classe)

    nouveaux_F = []
    for classe in classes:
        for f in auto["F"]:
            if f in classe and classe not in nouveaux_F:
                nouveaux_F.append(classe)

    return {"alphabet": auto["alphabet"], "etats": classes,
            "transitions": nouvelles_transitions,
            "I": nouveaux_I, "F": nouveaux_F}