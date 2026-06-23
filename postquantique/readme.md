# ML-KEM-512 -- Implementation pedagogique

Ce projet est une implementation pedagogique de ML-KEM-512 (Kyber),
un algorithme d'encapsulation de cle post-quantique standardise par le NIST.

Source principale : "Cryptographie post-quantique"
Pierre-Alain Fouque, Pascal Lafourcade, Ludovic Perret

## Structure du projet

- MLKEYBER.py   : arithmetique polynomiale dans Z_q[X]/(X^256+1), NTT
- keygen.py     : generation de cles (A, s, e, t)
- encaps.py     : encapsulation, construction de (u, v)
- decaps.py     : decapsulation, reconstruction du secret partage

## Parametres

q = 3329, n = 256, k = 2, eta = 3

## Principe

La securite repose sur le probleme Module-LWE. Une paire de cles
est generee (cle publique (A, t), cle privee s). L emetteur construit
un chiffre (u, v) a partir de la cle publique et d un secret aleatoire.
Le destinataire retrouve ce secret en utilisant sa cle privee.

