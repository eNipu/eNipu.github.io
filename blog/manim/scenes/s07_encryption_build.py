"""S07 - Building a ciphertext, term by term.

ct = (pk0*u + e1 + (q/t)*m ,  pk1*u + e2). Highlight where the message sits and
how it is buried under a fresh random mask each time.
"""

from manim import *

from theme import MSG, NOISE, MASK, SCALE


class EncryptionBuild(Scene):
    def construct(self):
        title = Text("Encryption", font_size=44).to_edge(UP)
        self.play(Write(title))

        msg = MathTex(r"m", font_size=44, color=MSG)
        msg_note = Text("plaintext polynomial (mod t)", font_size=24, color=MSG)
        VGroup(msg, msg_note).arrange(RIGHT, buff=0.4).next_to(title, DOWN, buff=0.5)
        self.play(Write(msg), FadeIn(msg_note))
        self.wait(0.4)
        self.play(FadeOut(msg), FadeOut(msg_note))

        # ct0
        ct0 = MathTex(r"\mathbf{ct}_0", r"=", r"\mathbf{pk}_0\, u", r"+", r"e_1", r"+",
                      r"\tfrac{q}{t}\,m", font_size=48)
        ct0[2].set_color(MASK)
        ct0[4].set_color(NOISE)
        ct0[6].set_color(MSG)
        ct0[6][0:3].set_color(SCALE)
        ct0.next_to(title, DOWN, buff=1.0)

        ct1 = MathTex(r"\mathbf{ct}_1", r"=", r"\mathbf{pk}_1\, u", r"+", r"e_2", font_size=48)
        ct1[2].set_color(MASK)
        ct1[4].set_color(NOISE)
        ct1.next_to(ct0, DOWN, buff=0.8, aligned_edge=LEFT)

        self.play(Write(ct0[0]), Write(ct0[1]))
        self.play(FadeIn(ct0[2], shift=RIGHT)); self.wait(0.2)
        self.play(FadeIn(ct0[3]), FadeIn(ct0[4], shift=RIGHT)); self.wait(0.2)
        self.play(FadeIn(ct0[5]), FadeIn(ct0[6], shift=RIGHT))
        msgbox = SurroundingRectangle(ct0[6], color=MSG, buff=0.1)
        self.play(Create(msgbox))
        self.wait(0.5)

        self.play(Write(ct1))
        self.wait(0.5)

        note = Text("u is fresh & random each time, so the same m gives a different ciphertext",
                    font_size=24, color=SCALE).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(note))
        self.wait(1.6)
