import random
from MLKEYBER import q, n, poly_add, poly_mul_ntt

k = 2          
eta = 3        


def sample_cbd(eta=eta):
    """
    Centered Binomial Distribution : pour chaque coefficient, on tire 2*eta bits
    aleatoires, on les separe en deux moities de eta bits, et le coefficient
    vaut (somme des bits de la 1ere moitie) - (somme des bits de la 2eme moitie).
    Resultat dans {-eta, ..., eta}, ramene mod q.
    """
    poly = []
    for _ in range(n):
        a = sum(random.randint(0, 1) for _ in range(eta))
        b = sum(random.randint(0, 1) for _ in range(eta))
        poly.append((a - b) % q)
    return poly


def sample_uniform_poly():
    """Polynome a coefficients uniformes dans Z_q (utilise pour generer A)."""
    return [random.randint(0, q - 1) for _ in range(n)]


def gen_matrix_A(k=k):
    """Matrice k x k de polynomes uniformes (publique, generee aleatoirement)."""
    return [[sample_uniform_poly() for _ in range(k)] for _ in range(k)]


def mat_vec_mul(A, v):
    """Produit matrice (k x k de polynomes) x vecteur (k polynomes) -> vecteur (k polynomes)."""
    k_ = len(A)
    result = []
    for i in range(k_):
        acc = [0] * n
        for j in range(k_):
            acc = poly_add(acc, poly_mul_ntt(A[i][j], v[j]))
        result.append(acc)
    return result


def vec_add(v1, v2):
    return [poly_add(v1[i], v2[i]) for i in range(len(v1))]


def keygen():
    """
    Genere une paire de cles ML-KEM-512.
    Retourne (pk, sk) avec :
      pk = (A, t)   -- cle publique
      sk = s        -- cle privee
    """
    A = gen_matrix_A(k)
    s = [sample_cbd() for _ in range(k)]
    e = [sample_cbd() for _ in range(k)]

    t = vec_add(mat_vec_mul(A, s), e)

    pk = (A, t)
    sk = s
    return pk, sk
