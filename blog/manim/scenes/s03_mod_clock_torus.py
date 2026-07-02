"""S03 - Coefficients live on a clock (arithmetic mod t).

A 24-hour clock: adding 6 hours to 21 lands on 3. Then show the negative
representation, where the same points can be labelled -11..12.
"""

from manim import *

from theme import MSG, NOISE


class ModClockTorus(Scene):
    def construct(self):
        title = Text("Numbers on a clock  (mod t)", font_size=40).to_edge(UP)
        self.play(Write(title))

        n = 24
        radius = 2.0
        circle = Circle(radius=radius, color=GREY_B).shift(0.35 * UP)
        self.play(Create(circle))

        def point_at(k):
            ang = PI / 2 - TAU * k / n
            return circle.get_center() + radius * np.array([np.cos(ang), np.sin(ang), 0])

        dots = VGroup(*[Dot(point_at(k), radius=0.045, color=GREY_B) for k in range(n)])
        labels = VGroup()
        for k in range(0, n, 6):
            lbl = MathTex(str(k), font_size=30).move_to(point_at(k) * 1.0)
            lbl.move_to(circle.get_center() + (radius + 0.42) * (point_at(k) - circle.get_center()) / radius)
            labels.add(lbl)
        self.play(FadeIn(dots), Write(labels))
        self.wait(0.4)

        # Start at 21
        start = Dot(point_at(21), radius=0.11, color=MSG)
        start_lbl = MathTex("21", font_size=34, color=MSG).next_to(start, LEFT, buff=0.15)
        self.play(FadeIn(start), Write(start_lbl))
        eq = MathTex(r"21 + 6 \equiv 3 \pmod{24}", font_size=40).to_edge(DOWN, buff=1.1)
        self.play(Write(eq))

        # Rotate forward 6 steps, wrapping past 24 to 3
        arc = Arc(arc_center=circle.get_center(), radius=radius,
                  start_angle=PI / 2 - TAU * 21 / n, angle=-TAU * 6 / n, color=MSG)
        moving = Dot(point_at(21), radius=0.11, color=MSG)
        self.play(FadeOut(start), FadeOut(start_lbl))
        self.play(Create(arc), MoveAlongPath(moving, arc), run_time=2)
        end_lbl = MathTex("3", font_size=34, color=MSG).next_to(point_at(3), RIGHT, buff=0.15)
        self.play(Write(end_lbl))
        self.wait(1.0)

        # Negative representation
        note = Text("same points, labelled -11 .. 12  (handy for negatives)",
                    font_size=24, color=NOISE)
        note.next_to(eq, DOWN, buff=0.3)
        self.play(FadeIn(note))
        self.wait(1.4)
