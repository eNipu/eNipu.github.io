"""S13 - The NTT pipeline: evaluate, multiply pointwise, interpolate.

Polynomial multiplication as representation change: coefficient form to value
form (NTT), cheap pointwise multiply, back (inverse NTT). O(d^2) becomes
O(d log d), in exact integer arithmetic.
"""

from manim import *

from theme import MSG, MASK, SCALE, NOISE


def pipeline_box(tex, sub, color=WHITE):
    content = MathTex(tex, font_size=34, color=color)
    rect = RoundedRectangle(corner_radius=0.12, width=content.width + 0.7,
                            height=1.1, color=GREY_B)
    content.move_to(rect)
    caption = Text(sub, font_size=20, color=GREY_B).next_to(rect, DOWN, buff=0.18)
    return VGroup(rect, content, caption)


class NTTPipeline(Scene):
    def construct(self):
        title = Text("The NTT: an FFT for integers", font_size=38).to_edge(UP)
        self.play(Write(title))

        b1 = pipeline_box(r"a,\ b", "coefficients")
        b2 = pipeline_box(r"\hat a,\ \hat b", "values at powers of omega", MASK)
        b3 = pipeline_box(r"\hat c_i = \hat a_i \hat b_i", "pointwise, O(d)", MSG)
        b4 = pipeline_box(r"c = a \cdot b", "coefficients")
        row = VGroup(b1, b2, b3, b4).arrange(RIGHT, buff=1.05).move_to(0.6 * UP)

        arrows = VGroup()
        arrow_labels = VGroup()
        for left, right, name in ((b1, b2, "NTT"), (b2, b3, "multiply"), (b3, b4, "inverse NTT")):
            a = Arrow(left[0].get_right(), right[0].get_left(), buff=0.08, color=SCALE,
                      stroke_width=4, max_tip_length_to_length_ratio=0.35)
            arrows.add(a)
            lbl = Text(name, font_size=18, color=SCALE)
            lbl.move_to(a.get_center() + 0.85 * UP)
            arrow_labels.add(lbl)

        self.play(FadeIn(b1))
        for box, arrow, lbl in zip((b2, b3, b4), arrows, arrow_labels):
            self.play(GrowArrow(arrow), FadeIn(lbl), FadeIn(box), run_time=0.8)
        self.wait(0.4)

        naive = MathTex(r"\text{naive convolution: } O(d^2)", font_size=34, color=NOISE)
        fast = MathTex(r"\text{with the NTT: } O(d \log d)", font_size=34, color=MSG)
        costs = VGroup(naive, fast).arrange(RIGHT, buff=1.2).move_to(1.5 * DOWN)
        self.play(Write(naive))
        cross = Line(naive.get_corner(DL) + 0.1 * DOWN, naive.get_corner(UR) + 0.1 * UP,
                     color=NOISE, stroke_width=5)
        self.play(Create(cross))
        self.play(Write(fast))
        self.wait(0.4)

        note = Text("exact integer arithmetic mod q - no floats, no rounding error",
                    font_size=26, color=SCALE).to_edge(DOWN, buff=0.8)
        self.play(Write(note))
        self.wait(1.8)
