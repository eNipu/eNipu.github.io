"""S08 - Decryption: cancel the mask, then rescale and round.

ct0 + ct1*s  ->  (q/t) m + noise. Divide by q/t and round to the nearest
integer, as long as the noise stays inside the budget q/(2t).
"""

from manim import *

from theme import MSG, NOISE, SCALE


class DecryptionRescaleRound(Scene):
    def construct(self):
        title = Text("Decryption", font_size=44).to_edge(UP)
        self.play(Write(title))

        step1 = MathTex(r"\mathbf{ct}_0 + \mathbf{ct}_1\, s", font_size=48)
        step1.next_to(title, DOWN, buff=0.7)
        self.play(Write(step1))
        self.wait(0.3)

        step2 = MathTex(r"=", r"\tfrac{q}{t}\, m", r"+", r"\underbrace{e_1 + e\,u + e_2 s}_{\text{noise}}",
                        font_size=48)
        step2[1].set_color(MSG)
        step2[1][0:3].set_color(SCALE)
        step2[3].set_color(NOISE)
        step2.next_to(step1, DOWN, buff=0.6)
        self.play(Write(step2))
        cancel = Text("the mask a*u is gone - the key cancelled it",
                      font_size=25, color=SCALE).next_to(step2, DOWN, buff=0.5)
        self.play(FadeIn(cancel))
        self.wait(0.8)

        # Rescale + round
        step3 = MathTex(r"m = \left\lfloor \tfrac{t}{q}\,(\mathbf{ct}_0 + \mathbf{ct}_1 s) \right\rceil",
                        font_size=48)
        step3[0][0].set_color(MSG)
        step3.next_to(cancel, DOWN, buff=0.7)
        self.play(Write(step3))
        ok = Text("works while noise stays below the budget  q/(2t)",
                  font_size=25, color=MSG).next_to(step3, DOWN, buff=0.5)
        self.play(FadeIn(ok))
        self.wait(1.6)
