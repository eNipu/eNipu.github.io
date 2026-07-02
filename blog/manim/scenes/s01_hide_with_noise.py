"""S01 - The one idea behind the whole scheme: hide a value under a noisy mask.

A clean scaled message is buried under a big random mask plus a little noise.
The mask can be cancelled if you know the secret; the noise is what makes the
scheme secure.
"""

from manim import *

from theme import MSG, NOISE, MASK, KEY


class HideWithNoise(Scene):
    def construct(self):
        title = Text("The one idea", font_size=44).to_edge(UP)
        self.play(Write(title))

        msg = MathTex(r"\Delta\, m", color=MSG, font_size=72)
        self.play(FadeIn(msg, shift=UP))
        self.wait(0.4)
        label_msg = Text("scaled message", font_size=24, color=MSG).next_to(msg, DOWN)
        self.play(FadeIn(label_msg))
        self.wait(0.6)

        # Add the big mask
        eq2 = MathTex(r"\Delta\, m", r"+", r"\text{mask}", font_size=72)
        eq2[0].set_color(MSG)
        eq2[2].set_color(MASK)
        self.play(
            ReplacementTransform(msg, eq2[0]),
            FadeOut(label_msg),
            FadeIn(eq2[1]),
            FadeIn(eq2[2], shift=RIGHT),
        )
        label_mask = Text("large, random-looking", font_size=22, color=MASK).next_to(eq2[2], DOWN)
        self.play(FadeIn(label_mask))
        self.wait(0.6)

        # Add the small noise
        eq3 = MathTex(r"\Delta\, m", r"+", r"\text{mask}", r"+", r"e", font_size=72)
        eq3[0].set_color(MSG)
        eq3[2].set_color(MASK)
        eq3[4].set_color(NOISE)
        self.play(
            ReplacementTransform(eq2, eq3[0:3]),
            FadeIn(eq3[3]),
            FadeIn(eq3[4], shift=RIGHT),
        )
        label_noise = Text("tiny noise", font_size=22, color=NOISE).next_to(eq3[4], DOWN)
        self.play(FadeOut(label_mask), FadeIn(label_noise))
        brace = Brace(eq3, DOWN, buff=0.9)
        ct = brace.get_text("ciphertext")
        self.play(GrowFromCenter(brace), FadeIn(ct))
        self.wait(0.8)

        # Decryption: knowing the key cancels the mask
        self.play(FadeOut(label_noise), FadeOut(brace), FadeOut(ct), eq3.animate.shift(UP))
        arrow = MathTex(r"\downarrow\ \text{subtract mask with key } s", color=KEY, font_size=36)
        arrow.next_to(eq3, DOWN, buff=0.6)
        self.play(Write(arrow))

        result = MathTex(r"\Delta\, m", r"+", r"e", font_size=72).next_to(arrow, DOWN, buff=0.6)
        result[0].set_color(MSG)
        result[2].set_color(NOISE)
        self.play(FadeIn(result, shift=UP))
        round_txt = Text("round away e, and recover m", font_size=26, color=MSG)
        round_txt.next_to(result, DOWN, buff=0.5)
        self.play(FadeIn(round_txt))
        self.wait(1.5)
