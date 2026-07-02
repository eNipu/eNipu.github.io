"""S04 - From vectors to polynomials, and the modulus x^d + 1.

Show a polynomial as its coefficient vector, then the ring rule x^d = -1 that
folds high powers back down (x^18 -> -x^2 for d = 16).
"""

from manim import *

from theme import MSG, NOISE, KEY


class PolyRing(Scene):
    def construct(self):
        title = Text("Data as polynomials", font_size=42).to_edge(UP)
        self.play(Write(title))

        poly = MathTex(r"a_{d-1}x^{d-1} + \cdots + a_2 x^2 + a_1 x + a_0", font_size=44)
        poly.next_to(title, DOWN, buff=0.7)
        self.play(Write(poly))

        vec = MathTex(r"(\,a_{d-1},\ \ldots,\ a_2,\ a_1,\ a_0\,)", font_size=44)
        vec.next_to(poly, DOWN, buff=0.6)
        note = Text("just a vector of coefficients (each mod t)", font_size=26, color=MSG)
        note.next_to(vec, DOWN, buff=0.35)
        self.play(TransformFromCopy(poly, vec))
        self.play(FadeIn(note))
        self.wait(1.0)

        self.play(FadeOut(poly), FadeOut(vec), FadeOut(note))

        # The polynomial modulus
        modtxt = MathTex(r"\text{work modulo}\quad x^{d}+1,\qquad d = 2^n", font_size=44)
        modtxt.next_to(title, DOWN, buff=0.8)
        self.play(Write(modtxt))

        rule = MathTex(r"x^{d} \equiv -1", font_size=56)
        rule.next_to(modtxt, DOWN, buff=0.7)
        rule[0][0:2].set_color(KEY)
        self.play(Write(rule))
        self.wait(0.6)

        # Concrete fold for d = 16
        example = MathTex(r"x^{18}", r"=", r"x^{16}\cdot x^{2}", r"=", r"-x^{2}", font_size=52)
        example[0].set_color(NOISE)
        example[4].set_color(NOISE)
        example.next_to(rule, DOWN, buff=0.8)
        self.play(Write(example[0]), Write(example[1]), Write(example[2]))
        self.wait(0.4)
        self.play(Write(example[3]), Write(example[4]))
        caption = Text("high powers fold back down - and flip sign", font_size=26, color=MSG)
        caption.next_to(example, DOWN, buff=0.5)
        self.play(FadeIn(caption))
        self.wait(1.5)
