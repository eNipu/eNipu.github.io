"""S15 - The lattice behind LWE: the closest vector problem.

A lattice is every point reachable by integer steps along basis vectors. An
LWE value b = As + e is a point sitting NEAR the lattice; the attack is to
find which grid point it snapped off of. Easy in 2D, brutal in dimension 1000.
"""

from manim import *

from theme import MASK, NOISE, KEY, SCALE


class LatticeCVP(Scene):
    def construct(self):
        title = Text("The lattice behind LWE", font_size=38).to_edge(UP)
        self.play(Write(title))

        origin = 0.7 * DOWN
        b1 = np.array([1.15, 0.25, 0.0])
        b2 = np.array([0.35, 0.85, 0.0])

        points = []
        for i in range(-9, 10):
            for j in range(-9, 10):
                p = origin + i * b1 + j * b2
                if abs(p[0]) < 6.2 and -3.1 < p[1] < 2.1:
                    points.append(p)
        dots = VGroup(*[Dot(p, radius=0.045, color=GREY_B) for p in points])
        self.play(FadeIn(dots, lag_ratio=0.01, run_time=1.5))

        v1 = Arrow(origin, origin + b1, buff=0, color=MASK, stroke_width=5)
        v2 = Arrow(origin, origin + b2, buff=0, color=MASK, stroke_width=5)
        basis_note = Text("every point = integer steps along two basis vectors",
                          font_size=24, color=MASK).next_to(title, DOWN, buff=0.25)
        self.play(GrowArrow(v1), GrowArrow(v2), FadeIn(basis_note))
        self.wait(0.6)

        target = origin + 2 * b1 + 1 * b2
        noisy = target + np.array([0.26, -0.19, 0.0])
        noisy_dot = Dot(noisy, radius=0.09, color=NOISE)
        noisy_lbl = MathTex(r"b = \vec a \cdot \vec s + e", font_size=32, color=NOISE)
        noisy_lbl.next_to(noisy_dot, UR, buff=0.15)
        self.play(FadeIn(noisy_dot, scale=2.0), Write(noisy_lbl))

        question = Text("which grid point did it snap off of?", font_size=26, color=SCALE)
        question.next_to(basis_note, DOWN, buff=0.2)
        self.play(Transform(basis_note, question))
        self.wait(0.6)

        link = DashedLine(noisy, target, color=KEY, stroke_width=4)
        ring = Circle(radius=0.22, color=KEY).move_to(target)
        self.play(Create(link), Create(ring))
        easy = Text("in 2 dimensions: easy", font_size=26, color=KEY).to_edge(DOWN, buff=1.05)
        self.play(Write(easy))
        self.wait(0.6)

        hard = Text("in dimension 1000: exponentially hard - that wall is the security",
                    font_size=26, color=NOISE).to_edge(DOWN, buff=0.45)
        self.play(Write(hard))
        self.wait(1.8)
