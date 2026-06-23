from MLKEYBER import n, poly_sub
from encrypt import decode_message, vec_dot


def decaps(sk, ciphertext):
    s = sk
    u, v = ciphertext
    # s^T.u = s0*u0 + s1*u1
    su = vec_dot(s, u)
    # v - s^T.u = m + bruit petit
    noisy_m = poly_sub(v, su)
    return decode_message(noisy_m)
