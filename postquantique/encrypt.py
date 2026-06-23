import random
from MLKEYBER import q, n, poly_add, poly_mul_ntt
from keygen import k, sample_cbd, mat_vec_mul, vec_add


def encode_message(bits):
    """
    Encode une liste de 256 bits (0 ou 1) en polynome :
    bit 0 -> coefficient 0
    bit 1 -> coefficient q//2 (le plus loin possible de 0, pour resister au bruit)
    """
    assert len(bits) == n, f"il faut exactement {n} bits"
    half = q // 2
    return [half if b == 1 else 0 for b in bits]


def decode_message(poly):
    """
    Decode un polynome (potentiellement bruite) en 256 bits :
    pour chaque coefficient, on regarde s'il est plus proche de 0 ou de q//2.
    """
    half = q // 2
    bits = []
    for c in poly:
        # distance circulaire a 0 vs distance a half, modulo q
        dist_to_0 = min(c, q - c)
        dist_to_half = abs(c - half)
        bits.append(1 if dist_to_half < dist_to_0 else 0)
    return bits


def mat_transpose_vec_mul(A, v):
    """
    Calcule A^T . v  (transposee de A, multipliee par le vecteur v).
    A^T[i][j] = A[j][i], donc (A^T.v)[i] = somme_j A[j][i] * v[j]
    """
    k_ = len(A)
    result = []
    for i in range(k_):
        acc = [0] * n
        for j in range(k_):
            acc = poly_add(acc, poly_mul_ntt(A[j][i], v[j]))
        result.append(acc)
    return result


def vec_dot(v1, v2):
    """Produit scalaire de deux vecteurs de polynomes : somme_i v1[i] * v2[i]."""
    acc = [0] * n
    for i in range(len(v1)):
        acc = poly_add(acc, poly_mul_ntt(v1[i], v2[i]))
    return acc


def encaps(pk, message_bits=None):
    """
    Encapsulation : a partir de la cle publique pk = (A, t), produit
    un texte chiffre (u, v) et le secret partage (les bits du message).
    """
    A, t = pk

    if message_bits is None:
        message_bits = [random.randint(0, 1) for _ in range(n)]

    m_poly = encode_message(message_bits)

    r = [sample_cbd() for _ in range(k)]
    e1 = [sample_cbd() for _ in range(k)]
    e2 = sample_cbd()

    u = vec_add(mat_transpose_vec_mul(A, r), e1)
    v = poly_add(poly_add(vec_dot(t, r), e2), m_poly)

    ciphertext = (u, v)
    shared_secret = message_bits  # version simplifiee : pas de hash final
    return ciphertext, shared_secret
