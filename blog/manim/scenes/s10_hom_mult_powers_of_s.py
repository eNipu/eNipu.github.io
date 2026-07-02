"""S10 - Homomorphic multiplication: read a ciphertext as a polynomial in s.

Decryption is c0 + c1*s. Multiplying two such linear expressions gives a
quadratic in s: c0 + c1*s + c2*s^2. The ciphertext grows by one component.
"""

from manim import *

from theme import MSG, NOISE, MASK, KEY


class HomMultPowersOfS(Scene):
    def construct(self):
        title = Text("Homomorphic multiplication", font_size=40).to_edge(UP)
        self.play(Write(title))

        idea = MathTex(r"\text{read decryption as a polynomial in } s:", font_size=34)
        idea.next_to(title, DOWN, buff=0.5)
        dec = MathTex(r"\mathbf{ct}_0 + \mathbf{ct}_1\, s", font_size=46)
        dec[0][-1].set_color(KEY)
        dec.next_to(idea, DOWN, buff=0.4)
        self.play(FadeIn(idea), Write(dec))
        self.wait(0.6)
        self.play(FadeOut(idea), dec.animate.to_edge(UP, buff=1.4))

        a = MathTex(r"(\,a_0 + a_1 s\,)", font_size=46)
        b = MathTex(r"(\,b_0 + b_1 s\,)", font_size=46)
        prod = VGroup(a, b).arrange(RIGHT, buff=0.2).next_to(dec, DOWN, buff=0.9)
        for grp in (a, b):
            grp[0][-2].set_color(KEY)
        self.play(FadeOut(dec), Write(a), Write(b))
        self.wait(0.4)

        expand = MathTex(
            r"=\ ", r"a_0 b_0", r"+", r"(a_0 b_1 + a_1 b_0)", r"\,s", r"+", r"a_1 b_1", r"\,s^2",
            font_size=46,
        )
        expand.next_to(prod, DOWN, buff=0.7)
        expand[1].set_color(MASK)
        expand[3].set_color(MASK)
        expand[6].set_color(MASK)
        self.play(Write(expand))
        self.wait(0.5)

        result = MathTex(r"\mathbf{ct}' = (\,", r"c_0", r",", r"c_1", r",", r"c_2", r"\,)",
                         font_size=50).next_to(expand, DOWN, buff=0.8)
        self.play(Write(result))
        brace = Brace(result, DOWN, buff=0.2)
        grow = brace.get_text("two components become three (needs relinearisation)")
        grow.set_color(NOISE)
        self.play(GrowFromCenter(brace), FadeIn(grow))
        self.wait(1.8)
