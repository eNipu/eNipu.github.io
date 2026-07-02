"""Regenerate the noise-growth figures for the FHE/LWE blog post.

Produces two PNGs in blog/assets/:

  noise_distributions.png   - how the three noise terms in a homomorphic addition
                              spread out as you add 1, 5, and 30 ciphertexts.
  addition_noise_growth.png - box/whisker plot of the largest noise coefficient
                              versus the number of additions, against the
                              decryption budget q/(2t).

Run:
    python code/noise_plots.py
"""

from __future__ import annotations

import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from fv_toy import negacyclic_raw

# Toy parameters echoing the primer.
D = 16
T = 7
Q = 874
SIGMA = 1.5
BUDGET = Q / (2 * T)  # a coefficient above this magnitude flips decryption

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog", "assets")
os.makedirs(ASSETS, exist_ok=True)

RNG = np.random.default_rng(1234)


def error():
    return np.rint(RNG.normal(0.0, SIGMA, size=D)).astype(np.int64)


def ternary():
    return RNG.integers(-1, 2, size=D, dtype=np.int64)


def term_sum_errors(n):
    """e5 = e_1 + e_3 + ... : sum of n fresh encryption errors."""
    return sum(error() for _ in range(n))


def term_error_times_masks(n):
    """e * (u_1 + ... + u_n) : one error polynomial times a sum of ternary masks."""
    e = error()
    u = sum(ternary() for _ in range(n))
    return negacyclic_raw(e, u, D)


def term_errors_times_secret(n):
    """(e_2 + e_4 + ...) * s : sum of n errors times the ternary secret key."""
    es = sum(error() for _ in range(n))
    s = ternary()
    return negacyclic_raw(es, s, D)


def combined_noise(n):
    return term_sum_errors(n) + term_error_times_masks(n) + term_errors_times_secret(n)


def plot_distributions(trials=4000):
    terms = [
        ("e_5 = sum of errors", term_sum_errors),
        ("e * sum of masks u", term_error_times_masks),
        ("sum of errors * s", term_errors_times_secret),
    ]
    counts = [1, 5, 30]
    colors = {1: "#4C72B0", 5: "#DD8452", 30: "#C44E52"}

    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for ax, (title, fn) in zip(axes, terms):
        for n in counts:
            coeffs = np.concatenate([fn(n) for _ in range(trials // D)])
            ax.hist(coeffs, bins=60, density=True, histtype="step", linewidth=2,
                    color=colors[n], label=f"{n} added")
        ax.axvline(BUDGET, color="k", ls="--", lw=1)
        ax.axvline(-BUDGET, color="k", ls="--", lw=1)
        ax.set_title(title, fontsize=11)
        ax.set_xlabel("coefficient value")
        ax.set_xlim(-150, 150)
    axes[0].set_ylabel("density")
    axes[0].legend(title="ciphertexts", fontsize=9)
    fig.suptitle(f"Noise term distributions (d={D}, sigma={SIGMA}); dashed = +/- q/(2t) = {BUDGET:.0f}",
                 fontsize=12)
    fig.tight_layout()
    out = os.path.join(ASSETS, "noise_distributions.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print("wrote", out)


def plot_growth(trials=400, max_adds=30):
    ns = list(range(1, max_adds + 1))
    data = []
    for n in ns:
        maxes = [int(np.max(np.abs(combined_noise(n)))) for _ in range(trials)]
        data.append(maxes)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.boxplot(data, positions=ns, widths=0.6, showfliers=False,
               patch_artist=True,
               boxprops=dict(facecolor="#4C72B0", alpha=0.5),
               medianprops=dict(color="#C44E52", lw=2))
    ax.axhline(BUDGET, color="k", ls="--", lw=1.5, label=f"decryption budget q/(2t) = {BUDGET:.0f}")
    ax.set_xlabel("number of homomorphic additions")
    ax.set_ylabel("largest |noise coefficient|")
    ax.set_title(f"Noise growth under homomorphic addition (d={D}, t={T}, q={Q})")
    ticks = list(range(1, max_adds + 1, 3))
    ax.set_xticks(ticks)
    ax.set_xticklabels([str(t) for t in ticks])
    ax.set_xlim(0, max_adds + 1)
    ax.legend()
    fig.tight_layout()
    out = os.path.join(ASSETS, "addition_noise_growth.png")
    fig.savefig(out, dpi=130)
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    plot_distributions()
    plot_growth()
