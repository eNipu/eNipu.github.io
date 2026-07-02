"""S05 - Multiplication as 'rotate and reflect' on the ring of powers.

Multiplying 2 x^14 by x^4 rotates the term forward 4 powers to x^18, which folds
to x^2 with a sign flip: the result is -2 x^2.
"""

from manim import *

from theme import MSG, NOISE, MASK


class PolyMultRotateReflect(Scene):
    def construct(self):
        title = Text("Multiplication = rotate + reflect", font_size=40).to_edge(UP)
        self.play(Write(title))

        d = 16
        radius = 1.95
        center = 0.25 * UP
        circle = Circle(radius=radius, color=GREY_B).move_to(center)
        self.play(Create(circle))

        def pos(k):
            ang = PI / 2 - TAU * (k % d) / d
            return center + radius * np.array([np.cos(ang), np.sin(ang), 0])

        ticks = VGroup(*[Dot(pos(k), radius=0.04, color=GREY_B) for k in range(d)])
        labels = VGroup()
        for k in range(0, d, 4):
            lbl = MathTex(f"x^{{{k}}}", font_size=26)
            lbl.move_to(center + (radius + 0.5) * (pos(k) - center) / radius)
            labels.add(lbl)
        self.play(FadeIn(ticks), Write(labels))

        # Start term 2 x^14
        start = Dot(pos(14), radius=0.11, color=MASK)
        start_lbl = MathTex(r"2x^{14}", font_size=34, color=MASK).next_to(pos(14), LEFT)
        self.play(FadeIn(start), Write(start_lbl))
        op = MathTex(r"\times\, x^4", font_size=40).to_corner(UL).shift(DOWN * 1.2 + RIGHT * 0.5)
        self.play(Write(op))
        self.wait(0.4)

        # Rotate forward 4 powers: x^14 -> x^18, which folds to x^2 past x^15.
        arc = Arc(arc_center=center, radius=radius,
                  start_angle=PI / 2 - TAU * 14 / d, angle=-TAU * 4 / d, color=MSG)
        moving = Dot(pos(14), radius=0.11, color=MASK)
        self.play(FadeOut(start), FadeOut(start_lbl))
        self.play(Create(arc), MoveAlongPath(moving, arc), run_time=2)
        wrap_lbl = MathTex(r"x^{18}\to x^{2}", font_size=30, color=MSG).next_to(pos(2), RIGHT)
        self.play(Write(wrap_lbl))
        self.wait(0.5)

        # Reflect sign: flash to NOISE colour to indicate sign flip
        self.play(moving.animate.set_color(NOISE), Flash(moving, color=NOISE))
        result = MathTex(r"2x^{14}\cdot x^4 \equiv -\,2x^{2}\pmod{x^{16}+1}",
                         font_size=40).to_edge(DOWN, buff=0.7)
        result[0][-4:].set_color(NOISE)
        self.play(Write(result))
        self.wait(1.6)
