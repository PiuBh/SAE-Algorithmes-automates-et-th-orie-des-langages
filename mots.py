"""
Partie 1.1 : Mots
Un mot est représenté par une chaîne de caractères.
Un langage est représenté par une liste de mots.
"""

"""
Question 1.1.1
Définir une fonction pref qui étant donné un mot u passé en paramètre renvoie la liste des préfixes de u.
"""
def pref(u):
    resultat = []
    #on boucle de 0 à len(u) inclus
    for k in range(len(u) + 1):
        resultat.append(u[0:k])      #tranche du début jusqu'à l'indice k
    return resultat


"""
Question 1.1.2
Définir une fonction suf qui étant donné un mot u passé en paramètre renvoie la liste des suffixes de u.
"""
def suf(u):
    resultat = []
    #même principe que pour pref, mais on prend la tranche de k jusqu'à la fin du mot
    for k in range(len(u) + 1):
        resultat.append(u[k:len(u)])  #tranche de l'indice k jusqu'à la fin
    return resultat

"""
Question 1.1.3
Définir une fonction fact qui étant donné un mot u passé en paramètre renvoie la liste sans doublons des facteurs de u.
"""
def fact(u):
    #un facteur = début d'une fin, on fait pref de chaque suf
    #On combine donc suf et pref.
    resultat = []
    for suffixe in suf(u):              # pour chaque suffixe de u
        for facteur in pref(suffixe):   # on prend tous ses préfixes
            if facteur not in resultat:  #pour éviter les doublons
                resultat.append(facteur)
    return resultat

"""
Question 1.1.4
Définir une fonction miroir qui étant donné un mot u passé en paramètre renvoie le mot miroir de u.
"""
def miroir(u):
    """On construit le miroir lettre par lettre.
    À chaque tour, on place la nouvelle lettre DEVANT le résultat.
    Exemple avec "abc" :
    on lit 'a' : resultat devient "a"
    on lit 'b' : resultat devient "ba"  (b avant a)
    on lit 'c' : resultat devient "cba" (c avant ba)
    """
    resultat = ""
    for lettre in u:
        resultat = lettre + resultat
    return resultat