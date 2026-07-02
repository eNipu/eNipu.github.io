"""S02 - Learning With Errors: the simplest version of the whole idea.

Build the LWE sample b = <a, s> + e, then show encryption (add Delta*m) and
decryption (subtract <a, s>, round away e).
"""

from manim import *

from theme import MSG, NOISE, MASK, KEY


class LWESampleAndDecrypt(Scene):
    def construct(self):
        title = Text("Learning With Errors", font_size=42).to_edge(UP)
        self.play(Write(title))

        # The public vector a and secret s
        a = MathTex(r"\vec a = (a_1, a_2, \ldots, a_n)", font_size=40)
        s = MathTex(r"\vec s = (s_1, s_2, \ldots, s_n)", font_size=40, color=KEY)
        s_note = Text("secret key", font_size=22, color=KEY)
        VGroup(a, s).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.7)
        s_note.next_to(s, RIGHT, buff=0.5)
        self.play(Write(a))
        self.play(Write(s), FadeIn(s_note))
        self.wait(0.5)

        # The LWE sample
        sample = MathTex(r"b", r"=", r"\vec a\cdot\vec s", r"+", r"e", font_size=52)
        sample[2].set_color(MASK)
        sample[4].set_color(NOISE)
        sample.next_to(VGroup(a, s), DOWN, buff=0.9)
        self.play(FadeOut(s_note), Write(sample))
        b_note = Text("looks random; recovering s is a hard problem",
                      font_size=24, color=GREY_B).next_to(sample, DOWN, buff=0.4)
        self.play(FadeIn(b_note))
        self.wait(1.0)

        self.play(FadeOut(a), FadeOut(s), FadeOut(b_note), sample.animate.to_edge(UP, buff=1.6))

        # Encryption: hide the message by adding Delta*m
        enc = MathTex(r"b", r"=", r"\vec a\cdot\vec s", r"+", r"e", r"+", r"\Delta m", font_size=52)
        enc[2].set_color(MASK)
        enc[4].set_color(NOISE)
        enc[6].set_color(MSG)
        enc.move_to(sample)
        self.play(TransformMatchingTex(sample, enc))
        enc_lbl = Text("encryption of m", font_size=24, color=MSG).next_to(enc, DOWN, buff=0.4)
        self.play(FadeIn(enc_lbl))
        self.wait(0.8)

        # Decryption: subtract a.s using the key
        dec1 = MathTex(r"b - \vec a\cdot\vec s", r"=", r"e", r"+", r"\Delta m", font_size=52)
        dec1[2].set_color(NOISE)
        dec1[4].set_color(MSG)
        dec1.next_to(enc, DOWN, buff=1.2)
        self.play(FadeOut(enc_lbl), TransformFromCopy(enc, dec1))
        self.wait(0.6)

        dec2 = MathTex(r"\text{round}\left(\tfrac{1}{\Delta}(b-\vec a\cdot\vec s)\right)", r"=", r"m",
                       font_size=48)
        dec2[2].set_color(MSG)
        dec2.next_to(dec1, DOWN, buff=0.8)
        self.play(Write(dec2))
        box = SurroundingRectangle(dec2[2], color=MSG, buff=0.15)
        self.play(Create(box))
        self.wait(1.5)
