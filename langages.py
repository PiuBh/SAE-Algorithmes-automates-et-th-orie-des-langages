"""
Partie 1.2 : Langages
Rappel: un langage est une liste de mots (chaînes de caractères).
"""

"""
Question 1.2.1
Définir une fonction concatene qui étant donnés deux langages L1 et L2 renvoie le produit de concaténation (sans doublons) de L1 et L2.
"""
def concatene(L1, L2):
    # Le produit L1.L2 contient tous les mots u.v où u est dans L1 et v dans L2.
    resultat = []
    for mot1 in L1:                       # pour chaque mot de L1
        for mot2 in L2:                   # pour chaque mot de L2
            nouveau = mot1 + mot2         # concaténation des deux chaînes
            if nouveau not in resultat:   # pas de doublon
                resultat.append(nouveau)
    return resultat

"""
Question 1.2.2
Définir une fonction puis qui étant donnés un langage L et un entier n renvoie le langage L^n (sans doublons).
"""
def puis(L, n):
    # L^0 vaut {""} par convention : un seul mot, le mot vide.
    resultat = [""]
    # On multiplie n fois par L. À chaque tour, resultat devient resultat.L.
    for k in range(n):
        resultat = concatene(resultat, L)
    return resultat

"""
Question 1.2.3
Pourquoi ne peut-on pas faire de fonction calculant l'étoile d'un langage ?

Réponse :
L'étoile d'un langage L est définie par L*=L^0 U L^1 U L^2 U...
C'est une union infinie. Alors qu'on sait qu'une fonction Python doit se terminer en un nombrefini d'étapes, or il faudrait ici concaténer L un nombre infini de fois.
La fonction tournerait sans jamais s'arrêter, donc on ne peut pas la calculer.
"""

"""
Question 1.2.4
Définir une fonction tousmots qui étant donné un alphabet A passé en paramètre renvoie la liste de tous les mots de A* de longueur inférieure à n.
"""
def tousmots(A, n):
    resultat = []
    #On génère les mots par longueur croissante : 1, 2, ..., n.
    for k in range(1, n + 1):
        for mot in puis(A, k):           # tous les mots de longueur exactement k
            if mot not in resultat:
                resultat.append(mot)
    #on ajoute le mot vide à la fin
    #pour coller à l'exemple du sujet : ['a', 'b', ..., 'bbb', '']
    resultat.append("")
    return resultat