"""
SAE 2-02 - Programme principal
"""
from mots import pref, suf, fact, miroir
from langages import concatene, puis, tousmots
from automates import (defauto, lirelettre, liremot, accepte, langage_accept,
                       deterministe, determinise, renommage,
                       complet, complete, complement,
                       inter, difference,
                       prefixe, suffixe, facteur, miroir as miroir_auto,
                       minimise)

"""
/!/ ZONE A MODIFIER A L'ORAL /!/
"""

#AUTOMATE 1 (exemple non deterministe - parties 1.3, 2, 3, 5)
auto1 = {"alphabet": ['a', 'b'],
         "etats":    [0, 1, 2],
         "transitions": [[0, 'a', 0],
                         [0, 'b', 1],
                         [1, 'a', 1],
                         [1, 'b', 2]],
         "I": [0],
         "F": [2]}

#AUTOMATE 2 (deterministe - pour inter et difference)
auto2 = {"alphabet": ['a', 'b'],
         "etats":    [0, 1, 2],
         "transitions": [[0, 'a', 0],
                         [0, 'b', 1],
                         [1, 'a', 1],
                         [1, 'b', 2],
                         [2, 'a', 2],
                         [2, 'b', 0]],
         "I": [0],
         "F": [0, 1]}

#AUTOMATE 6 (deterministe ET complet - pour minimise)
auto6 = {"alphabet": ['a', 'b'],
         "etats":    [0, 1, 2, 3, 4, 5],
         "transitions": [[0, 'a', 4], [0, 'b', 3],
                         [1, 'a', 5], [1, 'b', 5],
                         [2, 'a', 5], [2, 'b', 2],
                         [3, 'a', 1], [3, 'b', 0],
                         [4, 'a', 1], [4, 'b', 2],
                         [5, 'a', 2], [5, 'b', 5]],
         "I": [0],
         "F": [0, 1, 2, 5]}

"""
FIN DE LA ZONE A MODIFIER
"""

#Donnees fixes pour les parties 1.1 et 1.2
mot_test = "coucou"
L1 = ['aa', 'ab', 'ba', 'bb']
L2 = ['a', 'b', '']



print("=" * 50)
print("Partie 1.1 : Mots")
print("=" * 50)

# Q1.1.1
print("pref('coucou')  :", pref(mot_test))

# Q1.1.2
print("suf('coucou')   :", suf(mot_test))

# Q1.1.3
print("fact('coucou')  :", fact(mot_test))

# Q1.1.4
print("miroir('coucou'):", miroir(mot_test))



print()
print("=" * 50)
print("Partie 1.2 : Langages")
print("=" * 50)


# Q1.2.1
print("concatene(L1, L2)      :", concatene(L1, L2))

# Q1.2.2
print("puis(L1, 2)            :", puis(L1, 2))

#Q1.2.3 : reponse en commentaire dans langages.py
#L'etoile est une union infinie, on ne peut pas la calculer en temps fini.

# Q1.2.4
print("tousmots(['a','b'], 3) :", tousmots(auto1["alphabet"], 3))


print()
print("=" * 50)
print("Partie 1.3 : Automates")
print("=" * 50)

# Q1.3.1 : defauto() est definie dans automates.py.
# Elle saisit un automate au clavier (alphabet, etats, transitions...).
# On travaille ici avec un automate pre-defini pour la demonstration.
print("(Q1.3.1) defauto() definie dans automates.py - demo avec auto1 :")
print("auto1 =", auto1)

# Q1.3.2 depuis TOUS les etats (comme dans le sujet)
print("lirelettre(etats, 'a') :", lirelettre(auto1["transitions"], auto1["etats"], 'a'))

# Q1.3.3 depuis TOUS les etats (comme dans le sujet)
print("liremot(etats, 'aba')  :", liremot(auto1["transitions"], auto1["etats"], 'aba'))

# Q1.3.4
print("accepte 'ab'           :", accepte(auto1, "ab"))
print("accepte 'b'            :", accepte(auto1, "b"))

# Q1.3.5
print("langage_accept(n=5)    :", langage_accept(auto1, 5))

# Q1.3.6 : reponse en commentaire dans automates.py
# Un automate peut accepter un langage infini, la fonction ne terminerait pas.



print()
print("=" * 50)
print("Partie 2 : Determinisation")
print("=" * 50)

# Q2.1
print("deterministe(auto1)           :", deterministe(auto1))

# Q2.2
auto1_det = determinise(auto1)
print("determinise(auto1)            :", auto1_det)

# Q2.3
auto1_ren = renommage(auto1_det)
print("renommage(determinise(auto1)) :", auto1_ren)


print()
print("=" * 50)
print("Partie 3 : Complementation")
print("=" * 50)


# Q3.1
print("complet(auto1)    :", complet(auto1))

# Q3.2
print("complete(auto1)   :", complete(renommage(determinise(auto1))))

# Q3.3
print("complement(auto1) :", complement(auto1))


print()
print("=" * 50)
print("Partie 4 : Automate produit")
print("=" * 50)

# On determinise et renomme auto1 avant de faire le produit
# (inter et difference attendent des automates deterministes)
a1 = renommage(determinise(auto1))
a2 = auto2

# Q4.1
res_inter = inter(a1, a2)
print("inter(a1, a2)        :", res_inter)
print("inter (renomme)      :", renommage(res_inter))

# Q4.2
res_diff = difference(a1, a2)
print("difference(a1, a2)   :", res_diff)
print("difference (renomme) :", renommage(res_diff))


print()
print("=" * 50)
print("Partie 5 : Proprietes de fermeture")
print("=" * 50)


# Hypothese : l'automate est emonde (tous les etats sont utiles).
# On utilise auto1 determinise + renomme pour garantir cette propriete.
auto_emonde = renommage(determinise(auto1))

# Q5.1
print("prefixe :", prefixe(auto_emonde))

# Q5.2
print("suffixe :", suffixe(auto_emonde))

# Q5.3
print("facteur :", facteur(auto_emonde))

# Q5.4
print("miroir  :", miroir_auto(auto_emonde))


print()
print("=" * 50)
print("Partie 6 : Minimisation (Moore)")
print("=" * 50)

# L'algorithme de Moore exige un automate deterministe ET complet.
# auto6 est deja deterministe et complet (verifie dans le sujet).
print("minimise(auto6)      :", minimise(auto6))
print("minimise (renomme)   :", renommage(minimise(auto6)))