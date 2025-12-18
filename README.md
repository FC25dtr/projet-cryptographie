# Projet RSA – Chiffrement et Déchiffrement de messages

## Description

Ce projet implémente les **principes fondamentaux de RSA**, un algorithme de chiffrement asymétrique.  
**Important : ce projet n'utilise aucune librairie de cryptographie externe**, toutes les fonctions sont codées « maison » en Python.

Pour l’instant, le projet inclut :

1. **Génération de clés RSA** :
   - Génération de deux nombres premiers aléatoires (`p` et `q`) avec le test de primalité **Miller-Rabin**.
   - Calcul du module `n = p * q`.
   - Calcul de la fonction φ(n) pour RSA.
   - Sélection d’un exposant public `e` et calcul de l’inverse modulo pour obtenir l’exposant privé `d`.
   - Les clés sont renvoyées sous forme de tuples :
     - Clé publique : `(n, e)`
     - Clé privée : `(n, d)`

2. **Chiffrement et déchiffrement des messages** :
   - Le texte est transformé en un **grand entier** grâce à la conversion `texte → entier`.
   - Chiffrement avec la **clé publique `(n, e)`** : `c ≡ m^e mod n`.
   - Déchiffrement avec la **clé privée `(n, d)`** : `m ≡ c^d mod n`.
   - Conversion inverse `entier → texte` pour récupérer le message original.

3. **Fonction de test de primalité** :
   - Implémentation de **Miller-Rabin** pour vérifier que les nombres générés sont premiers.

---

## Fonctionnement actuel

- L’utilisateur peut **entrer un message texte**, qui est converti en entier.
- Les clés RSA peuvent être générées automatiquement.
- Le message est **chiffré avec la clé publique** et **déchiffré avec la clé privée** pour récupérer le texte original.
- Le projet gère **des messages de longueur variable** grâce à la conversion en blocs d’octets.

---

## Étapes futures

Dans les prochaines versions, le projet prévoit :

1. **Gestion des messages très longs**
   - Découpage en blocs si l’entier du message dépasse `n`.
   - Réassemblage des blocs après déchiffrement.

2. **Signature numérique**
   - Signer un message avec la clé privée.
   - Vérifier la signature avec la clé publique.

3. **Optimisations**
   - Améliorer la génération de nombres premiers pour plus de rapidité.
   - Optimiser le chiffrement/déchiffrement pour des blocs plus grands.

## Notes

- Le projet est **en développement**, mais la base du chiffrement et du déchiffrement fonctionne.
- Les améliorations futures permettront un système RSA **complet et robuste**, avec signature numérique et gestion des messages longs.
