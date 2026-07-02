"""A tiny, readable Fan-Vercauteren (FV) homomorphic encryption implementation.

This accompanies the blog post "Computing on Secrets: An Illustrated Guide to
LWE and Fully Homomorphic Encryption". It is a *teaching* implementation using
deliberately insecure toy parameters so that every number stays small enough to
inspect by hand.

Everything lives in the negacyclic polynomial ring

    R_q = Z_q[x] / (x^d + 1)

Polynomials are stored as length-d integer numpy arrays, index i holding the
coefficient of x^i.

Run directly to reproduce the worked examples from the post:

    python code/fv_toy.py
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def center(poly: np.ndarray, modulus: int) -> np.ndarray:
    """Reduce coefficients into the centered range (-modulus/2, modulus/2]."""
    poly = np.asarray(poly, dtype=np.int64) % modulus
    poly[poly > modulus // 2] -= modulus
    return poly


def negacyclic_raw(a: np.ndarray, b: np.ndarray, d: int) -> np.ndarray:
    """Polynomial product folded by x^d -> -1, but WITHOUT reducing mod q.

    This is the "rotate and reflect" operation from the post: any power that
    spills past x^(d-1) wraps around AND flips sign, because x^d = -1. Keeping
    the integer coefficients (no mod q yet) is essential for the t/q rescale in
    homomorphic multiplication.
    """
    full = np.convolve(np.asarray(a, dtype=np.int64), np.asarray(b, dtype=np.int64))
    reduced = np.zeros(d, dtype=np.int64)
    for i, coeff in enumerate(full):
        if i < d:
            reduced[i] += coeff
        else:
            reduced[i - d] -= coeff  # x^i = x^(i-d) * x^d = -x^(i-d)
    return reduced


@dataclass
class FV:
    """Toy FV scheme over R_q = Z_q[x]/(x^d + 1). NOT SECURE - illustration only."""

    d: int = 16          # ring dimension, polynomial modulus is x^d + 1
    t: int = 7           # plaintext coefficient modulus
    q: int = 874         # ciphertext coefficient modulus (q >> t)
    sigma: float = 1.5   # standard deviation of the error / noise distribution
    seed: int | None = None

    def __post_init__(self):
        self.rng = np.random.default_rng(self.seed)
        self.delta = self.q // self.t  # scaling that lifts the message into the budget

    # ----- ring arithmetic in R_q ----------------------------------------- #
    def add(self, a, b):
        return center(np.asarray(a) + np.asarray(b), self.q)

    def mul(self, a, b):
        return center(negacyclic_raw(a, b, self.d), self.q)

    # ----- sampling small polynomials -------------------------------------- #
    def ternary(self):
        """Coefficients uniformly in {-1, 0, 1} (secret key and encryption mask u)."""
        return self.rng.integers(-1, 2, size=self.d, dtype=np.int64)

    def error(self):
        """A small, discrete-Gaussian-like error polynomial."""
        return np.rint(self.rng.normal(0.0, self.sigma, size=self.d)).astype(np.int64)

    def uniform_q(self):
        """Uniformly random polynomial with coefficients in Z_q (centered)."""
        return center(self.rng.integers(0, self.q, size=self.d, dtype=np.int64), self.q)

    # ----- key generation, encryption, decryption ------------------------- #
    def keygen(self):
        """Return (public_key, secret_key).

        secret key  s : small ternary polynomial
        public key pk : (pk0, pk1) = (-(a*s) + e, a)
        """
        s = self.ternary()
        a = self.uniform_q()
        e = self.error()
        pk0 = self.add(-self.mul(a, s), e)
        return (pk0, a), s

    def encrypt(self, pk, m):
        """Encrypt plaintext polynomial m (coefficients mod t) into a ciphertext.

        ct0 = pk0*u + e1 + Delta*m
        ct1 = pk1*u + e2
        """
        pk0, pk1 = pk
        u = self.ternary()
        e1, e2 = self.error(), self.error()
        ct0 = self.add(self.add(self.mul(pk0, u), e1), self.delta * center(m, self.t))
        ct1 = self.add(self.mul(pk1, u), e2)
        return [ct0, ct1]

    def phase(self, ct, s):
        """Compute sum_i c_i * s^i (mod q), centered. This is 'noisy scaled message'."""
        acc = np.array(ct[0], dtype=np.int64)
        s_power = np.zeros(self.d, dtype=np.int64)
        s_power[0] = 1  # s^0 = 1
        for i in range(1, len(ct)):
            s_power = self.mul(s_power, s)
            acc = self.add(acc, self.mul(ct[i], s_power))
        return center(acc, self.q)

    def decrypt(self, ct, s):
        """Decrypt a ciphertext of any length [c0, c1, c2, ...] as a polynomial in s."""
        scaled = self.phase(ct, s)
        return center(np.rint(scaled * self.t / self.q).astype(np.int64) % self.t, self.t)

    def noise(self, ct, s, m):
        """Max |coefficient| of (phase - Delta*m): how much of the budget is used.

        Correct decryption requires this to stay below q/(2t).
        """
        residual = center(self.phase(ct, s) - self.delta * center(m, self.t), self.q)
        return int(np.max(np.abs(residual)))

    @property
    def budget(self) -> float:
        return self.q / (2 * self.t)

    # ----- homomorphic operations ----------------------------------------- #
    def hom_add(self, ct_a, ct_b):
        return [self.add(x, y) for x, y in zip(ct_a, ct_b)]

    def hom_mul(self, ct_a, ct_b):
        """Multiply two length-2 ciphertexts, producing a length-3 ciphertext.

        Treat each ciphertext as a linear polynomial in s: c0 + c1*s. The product
        is quadratic in s, so the result has three components. The t/q rescale on
        the *un-reduced* integer product keeps the message scaling correct.
        """
        a0, a1 = ct_a
        b0, b1 = ct_b

        def rescale(raw):
            return center(np.rint(raw * self.t / self.q).astype(np.int64), self.q)

        c0 = rescale(negacyclic_raw(a0, b0, self.d))
        c1 = rescale(negacyclic_raw(a1, b0, self.d) + negacyclic_raw(a0, b1, self.d))
        c2 = rescale(negacyclic_raw(a1, b1, self.d))
        return [c0, c1, c2]


# --------------------------------------------------------------------------- #
# Display helpers
# --------------------------------------------------------------------------- #
def poly_str(poly: np.ndarray) -> str:
    terms = []
    for i in range(len(poly) - 1, -1, -1):
        c = int(poly[i])
        if c == 0:
            continue
        if i == 0:
            terms.append(f"{c:+d}")
        elif i == 1:
            terms.append(f"{c:+d}x")
        else:
            terms.append(f"{c:+d}x^{i}")
    return " ".join(terms) if terms else "0"


def poly_from_terms(d: int, **terms) -> np.ndarray:
    """Build a polynomial from {power: coeff}, e.g. poly_from_terms(16, **{'0':3,'8':4})."""
    p = np.zeros(d, dtype=np.int64)
    for power, coeff in terms.items():
        p[int(power)] = coeff
    return p


# --------------------------------------------------------------------------- #
# Worked examples
# --------------------------------------------------------------------------- #
def demo_visual() -> None:
    """Echoes the primer's small parameters: d=16, t=7, q=874."""
    fv = FV(d=16, t=7, q=874, sigma=1.5, seed=2018)
    print(f"[visual params]  d={fv.d}, t={fv.t}, q={fv.q}, Delta=q//t={fv.delta}, "
          f"budget q/(2t)={fv.budget:.1f}")
    print("=" * 70)

    pk, s = fv.keygen()
    print("secret key  s =", poly_str(s))
    print("public pk0    =", poly_str(pk[0]))
    print("public pk1(a) =", poly_str(pk[1]))
    print("-" * 70)

    # The message from the primer: m = 3 + 4 x^8  ==  3 - 3 x^8  (mod 7)
    m = center(poly_from_terms(fv.d, **{"0": 3, "8": 4}), fv.t)
    print("plaintext   m =", poly_str(m))
    ct = fv.encrypt(pk, m)
    print("ct0           =", poly_str(ct[0]))
    print("ct1           =", poly_str(ct[1]))
    print("decrypt(ct)   =", poly_str(fv.decrypt(ct, s)),
          f"   (noise {fv.noise(ct, s, m)} / budget {fv.budget:.0f})")
    assert np.array_equal(fv.decrypt(ct, s), m), "fresh decryption failed!"
    print("fresh round-trip OK")
    print("-" * 70)

    # Homomorphic addition
    m1 = center(poly_from_terms(fv.d, **{"0": 2, "3": 1}), fv.t)
    m2 = center(poly_from_terms(fv.d, **{"0": 1, "3": 2, "5": -1}), fv.t)
    ct1, ct2 = fv.encrypt(pk, m1), fv.encrypt(pk, m2)
    ct_sum = fv.hom_add(ct1, ct2)
    got, want = fv.decrypt(ct_sum, s), center(m1 + m2, fv.t)
    print("hom add: m1 =", poly_str(m1), "| m2 =", poly_str(m2))
    print("  decrypt(E(m1)+E(m2)) =", poly_str(got), "| expected", poly_str(want),
          f"   (noise {fv.noise(ct_sum, s, want)} / budget {fv.budget:.0f})")
    assert np.array_equal(got, want), "homomorphic addition failed!"
    print("  homomorphic addition OK")


def demo_multiplication() -> None:
    """Multiplication needs more headroom; use a larger q to show it round-trips."""
    fv = FV(d=16, t=7, q=65537, sigma=1.5, seed=7)
    print()
    print(f"[headroom params]  d={fv.d}, t={fv.t}, q={fv.q}, Delta=q//t={fv.delta}, "
          f"budget q/(2t)={fv.budget:.0f}")
    print("=" * 70)
    pk, s = fv.keygen()
    m1 = center(poly_from_terms(fv.d, **{"0": 2, "3": 1}), fv.t)
    m2 = center(poly_from_terms(fv.d, **{"0": 1, "3": 2, "5": -1}), fv.t)
    ct1, ct2 = fv.encrypt(pk, m1), fv.encrypt(pk, m2)

    ct_prod = fv.hom_mul(ct1, ct2)
    got, want = fv.decrypt(ct_prod, s), fv.mul(center(m1, fv.t), center(m2, fv.t))
    want = center(want, fv.t)
    print("hom mul: decrypt(E(m1)*E(m2)) =", poly_str(got))
    print("         expected  m1*m2       =", poly_str(want))
    print(f"         ciphertext grew from 2 to {len(ct_prod)} components")
    assert np.array_equal(got, want), "homomorphic multiplication failed!"
    print("  homomorphic multiplication OK")


def main() -> None:
    demo_visual()
    demo_multiplication()


if __name__ == "__main__":
    main()
