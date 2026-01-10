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
## Fonctionnalités

### 1. Génération des clés

- `gencle_RSA()` : génère un couple de clés `(clé_publique, clé_privée)`  
- `clé_publique = (n, e)`  
- `clé_privée = (n, d)`  
- Les clés peuvent être sauvegardées dans des fichiers pour un usage ultérieur.  

### 2. Conversion texte ↔ entier

- `message_vers_entier(message)` : convertit un bloc de texte en entier  
- `entier_vers_texte(entier)` : convertit un entier en bloc de texte  

### 3. Chiffrement / déchiffrement par blocs

- `chiffrement_blocs(cle_publique, message)` : chiffre un message de longueur arbitraire en découpant en blocs compatibles avec `n`  
- `dechiffrement_blocs(cle_privee, blocs_chiffres)` : déchiffre chaque bloc et reconstitue le message complet  

### 4. Fonctions interactives

#### Envoyer un message

- `envoyer_message_depuis_fichier()` :  
  - Lit la clé publique depuis `cle_publique.txt`  
  - Demande à l’utilisateur d’entrer le message  
  - Chiffre le message par blocs  
  - Retourne la liste des blocs chiffrés  

#### Recevoir un message

- `recevoir_message(blocs_chiffres)` :  
  - Lit la clé privée depuis `cle_priv.txt`  
  - Déchiffre chaque bloc  
  - Reconstitue le message texte  
  - Affiche le message déchiffré  

---

## Étapes futures

Dans les prochaines versions, le projet prévoit :

**Signature numérique**
   - Signer un message avec la clé privée.
   - Vérifier la signature avec la clé publique.

**server chat**
   - creation d'un server chat basé avec du chiffrement RSA (en cours mais avec des erreurs, il reste beaucoup de travail)

## Notes

- Le projet est **en développement**, mais la base du chiffrement et du déchiffrement fonctionne.
- rajout de 
