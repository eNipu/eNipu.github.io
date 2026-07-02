"""Shared palette and helpers for the FHE/LWE animation set."""

from manim import BLUE, GREEN, RED, PURPLE, YELLOW, GREY_B, WHITE

# Consistent colour language across every scene:
MSG = GREEN       # the secret message
NOISE = RED       # the small error / noise that provides security
MASK = BLUE       # the large masking term (a*s, a*u, ...)
KEY = PURPLE      # the secret key s
SCALE = YELLOW    # the scaling factor Delta = q/t
MUTED = GREY_B
INK = WHITE

TITLE_KW = dict(color=INK)
