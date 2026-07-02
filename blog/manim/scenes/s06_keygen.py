"""S06 - Key generation: hiding the secret key inside the public key.

pk = (-a*s + e, a). The random a scrambles s, and the small error e makes it
impossible to solve back for s. This is exactly a Ring-LWE sample.
"""

from manim import *

from theme import MSG, NOISE, MASK, KEY


class KeyGen(Scene):
    def construct(self):
        title = Text("Keys", font_size=44).to_edge(UP)
        self.play(Write(title))

        ingredients = VGroup(
            MathTex(r"s", r":\ \text{small, coefficients in } \{-1,0,1\}", font_size=38),
            MathTex(r"a", r":\ \text{uniformly random mod } q", font_size=38),
            MathTex(r"e", r":\ \text{small error}", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(title, DOWN, buff=0.6)
        ingredients[0][0].set_color(KEY)
        ingredients[1][0].set_color(MASK)
        ingredients[2][0].set_color(NOISE)
        for row in ingredients:
            self.play(Write(row), run_time=0.7)
        self.wait(0.5)

        pk = MathTex(r"\mathbf{pk} = \big(\,", r"-a\,s", r"+", r"e", r"\,,\ ", r"a", r"\,\big)",
                     font_size=52).next_to(ingredients, DOWN, buff=0.9)
        pk[1].set_color(MASK)
        pk[3].set_color(NOISE)
        pk[5].set_color(MASK)
        self.play(Write(pk))
        self.wait(0.4)

        line0 = Text("- a s  scrambles the secret", font_size=28, color=MASK)
        line1 = Text("+ e  keeps recovering s hard", font_size=28, color=NOISE)
        captions = VGroup(line0, line1).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        captions.next_to(pk, DOWN, buff=0.7)
        self.play(FadeIn(line0, shift=UP))
        self.play(FadeIn(line1, shift=UP))
        self.wait(0.8)

        hard = MathTex(r"\text{recovering } s \text{ from } \mathbf{pk} = \text{Ring-LWE (hard)}",
                       font_size=34, color=MSG).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(hard))
        self.wait(1.5)
