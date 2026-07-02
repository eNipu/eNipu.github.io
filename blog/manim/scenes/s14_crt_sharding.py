"""S14 - The Chinese Remainder Theorem as sharding.

11 mod 15 splits into shards (2 mod 3, 1 mod 5). Adding 7 updates each shard
independently; the shards still reconstruct the right answer. Arithmetic mod 15
is two smaller machines running in parallel.
"""

from manim import *

from theme import MSG, MASK, SCALE


def value_box(tex, color=WHITE, width=3.1):
    content = MathTex(tex, font_size=36, color=color)
    rect = RoundedRectangle(corner_radius=0.12, width=width, height=1.05, color=GREY_B)
    content.move_to(rect)
    return VGroup(rect, content)


class CRTSharding(Scene):
    def construct(self):
        title = Text("CRT: sharding for numbers", font_size=38).to_edge(UP)
        self.play(Write(title))

        big = value_box(r"11 \pmod{15}").move_to(1.55 * UP)
        s3 = value_box(r"2 \pmod{3}", MASK, 2.6).move_to(2.9 * LEFT + 0.5 * DOWN)
        s5 = value_box(r"1 \pmod{5}", MSG, 2.6).move_to(2.9 * RIGHT + 0.5 * DOWN)

        a3 = Arrow(big[0].get_bottom(), s3[0].get_top(), buff=0.1, color=MASK, stroke_width=4)
        a5 = Arrow(big[0].get_bottom(), s5[0].get_top(), buff=0.1, color=MSG, stroke_width=4)
        l3 = MathTex(r"\%\,3", font_size=30, color=MASK).next_to(a3.get_center(), LEFT, buff=0.25)
        l5 = MathTex(r"\%\,5", font_size=30, color=MSG).next_to(a5.get_center(), RIGHT, buff=0.25)

        self.play(FadeIn(big))
        self.play(GrowArrow(a3), GrowArrow(a5), Write(l3), Write(l5))
        self.play(FadeIn(s3), FadeIn(s5))
        self.wait(0.4)

        op = MathTex(r"+\,7", font_size=44, color=SCALE).next_to(big, LEFT, buff=0.9)
        op3 = MathTex(r"+7 \equiv +1", font_size=26, color=MASK).next_to(s3, DOWN, buff=0.25)
        op5 = MathTex(r"+7 \equiv +2", font_size=26, color=MSG).next_to(s5, DOWN, buff=0.25)
        self.play(Write(op))
        self.play(Write(op3), Write(op5))
        self.wait(0.3)

        new_big = MathTex(r"18 \equiv 3 \pmod{15}", font_size=36).move_to(big[1])
        new_s3 = MathTex(r"0 \pmod{3}", font_size=36, color=MASK).move_to(s3[1])
        new_s5 = MathTex(r"3 \pmod{5}", font_size=36, color=MSG).move_to(s5[1])
        self.play(Transform(big[1], new_big),
                  Transform(s3[1], new_s3),
                  Transform(s5[1], new_s5))
        self.wait(0.4)

        check = MathTex(r"3 \bmod 3 = 0\ \checkmark \qquad 3 \bmod 5 = 3\ \checkmark",
                        font_size=32, color=MSG).to_edge(DOWN, buff=1.15)
        self.play(Write(check))
        self.wait(0.4)

        note = Text("the shards never talk to each other - compute in parallel",
                    font_size=26, color=SCALE).to_edge(DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(1.8)
