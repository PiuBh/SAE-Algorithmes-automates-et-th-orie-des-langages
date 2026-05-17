# SAE 2-02 — Exploration algorithmique : Théorie des automates

**BUT1 Informatique** — Université Gustave Eiffel  
**Langage** : Python 3  
**Binôme** : Piyush & Ali

---

## Description

Implémentation complète des algorithmes de la théorie des automates finis en Python, dans le cadre de la SAE 2-02.

---

## Fonctionnalités implémentées

- **Mots** : préfixes, suffixes, facteurs, miroir
- **Langages** : concaténation, puissance, enumération
- **Automates** : saisie, lecture de lettre/mot, acceptation, langage accepté
- **Déterminisation** : algorithme des sous-ensembles + renommage
- **Complémentation** : complétion par état puits + inversion des états finaux
- **Automate produit** : intersection et différence de langages
- **Propriétés de fermeture** : préfixe, suffixe, facteur, miroir
- **Minimisation** : algorithme de Moore

---

## Structure du projet
SAE_2_02/
├── mots.py        # Partie 1.1 — opérations sur les mots
├── langages.py    # Partie 1.2 — opérations sur les langages
├── automates.py   # Parties 1.3 à 6 — algorithmes sur les automates
└── main.py        # Programme principal — démonstration

---

## Lancement

```bash
python main.py
```

---

## Structure d'un automate

Un automate est représenté par un dictionnaire Python :

```python
auto = {
    "alphabet"    : ['a', 'b'],        # lettres
    "etats"       : [0, 1, 2],         # liste des états
    "transitions" : [[0,'a',1], ...],  # [départ, lettre, arrivée]
    "I"           : [0],               # états initiaux
    "F"           : [2]                # états finaux
}
```
