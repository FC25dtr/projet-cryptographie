"""
Arithmetique polynomiale dans Z_q[X]/(X^256+1) pour ML-KEM

"""

q = 3329
n = 256


zeta = 17
assert pow(zeta, 128, q) == q - 1
assert pow(zeta, 256, q) == 1


def poly_add(p1, p2):
    return [(p1[i] + p2[i]) % q for i in range(n)]


def poly_sub(p1, p2):
    return [(p1[i] - p2[i]) % q for i in range(n)]


def poly_mul_naive(p1, p2):
    """Multiplication naive O(n^2), utilisee comme reference/test."""
    result = [0] * n
    for i in range(n):
        if p1[i] == 0:
            continue
        for j in range(n):
            if p2[j] == 0:
                continue
            deg = i + j
            val = p1[i] * p2[j]
            if deg >= n:
                deg -= n
                val = -val
            result[deg] = (result[deg] + val) % q
    return result


def _eval_mod_quadratic(p, r):
    """Calcule p(X) mod (X^2 - r), retourne (a, b) tels que p(X) = a + b*X dans ce quotient."""
    a, b = 0, 0
    r_pow = 1
    for j in range(n // 2):
        a = (a + p[2 * j] * r_pow) % q
        b = (b + p[2 * j + 1] * r_pow) % q
        r_pow = (r_pow * r) % q
    return a, b


def ntt(p):
    """
    NTT directe : renvoie une liste de 256 valeurs = 128 paires (a_i, b_i),
    ou (a_i, b_i) est le reste de p mod (X^2 - r_i), avec r_i = zeta^(2i+1).
    """
    out = []
    for i in range(128):
        r_i = pow(zeta, 2 * i + 1, q)
        a, b = _eval_mod_quadratic(p, r_i)
        out.append(a)
        out.append(b)
    return out


def _build_inverse_matrix():
    """
    Construit la matrice M telle que ntt(p) = p . M (p vu comme vecteur ligne),
    puis l'inverse mod q (Gauss-Jordan). Calculee une seule fois au chargement
    du module, puis reutilisee par ntt_inv.
    """
    M = []
    for k in range(n):
        ek = [0] * n
        ek[k] = 1
        M.append(ntt(ek))

    nrows = n
    A = [row[:] + [1 if i == j else 0 for j in range(nrows)] for i, row in enumerate(M)]
    for col in range(nrows):
        piv = None
        for r in range(col, nrows):
            if A[r][col] % q != 0:
                piv = r
                break
        if piv is None:
            raise ValueError("matrice singuliere (ne devrait jamais arriver ici)")
        A[col], A[piv] = A[piv], A[col]
        inv_piv = pow(A[col][col], q - 2, q)
        A[col] = [(x * inv_piv) % q for x in A[col]]
        for r in range(nrows):
            if r != col and A[r][col] != 0:
                factor = A[r][col]
                A[r] = [(A[r][c] - factor * A[col][c]) % q for c in range(2 * nrows)]
    return [row[nrows:] for row in A]


_M_INV = _build_inverse_matrix()


def ntt_inv(P):
    """Inverse de ntt(): reconstruit p tel que ntt(p) == P."""
    return [sum(P[k] * _M_INV[k][j] for k in range(n)) % q for j in range(n)]


def _ntt_mul_base(a0, a1, b0, b1, r_i):
    """Multiplie (a0 + a1*X) par (b0 + b1*X) dans Z_q[X]/(X^2 - r_i)."""
    return (
        (a0 * b0 + a1 * b1 * r_i) % q,
        (a0 * b1 + a1 * b0) % q,
    )


def poly_mul_ntt(p1, p2):
    """Multiplication rapide via NTT : ntt -> multiplication ponctuelle -> ntt_inv."""
    P1 = ntt(p1)
    P2 = ntt(p2)
    result = [0] * n
    for i in range(128):
        r_i = pow(zeta, 2 * i + 1, q)
        a0, a1 = P1[2 * i], P1[2 * i + 1]
        b0, b1 = P2[2 * i], P2[2 * i + 1]
        result[2 * i], result[2 * i + 1] = _ntt_mul_base(a0, a1, b0, b1, r_i)
    return ntt_inv(result)


