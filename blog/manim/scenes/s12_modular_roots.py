"""S12 - Roots of unity without complex numbers: powers of 2 mod 17.

The values 1, 2, 4, 8, 16, 15, 13, 9 sit on a ring; multiplying by 2 hops one
position. Halfway around lands on 16 = -1 mod 17. Pure integers rotating.
"""

from manim import *

from theme import MSG, NOISE, SCALE


class ModularRoots(Scene):
    def construct(self):
        title = Text("Rotation inside the integers mod 17", font_size=36).to_edge(UP)
        self.play(Write(title))

        vals = [1, 2, 4, 8, 16, 15, 13, 9]  # 2^k mod 17, k = 0..7
        n = 8
        radius = 1.75
        center = 0.2 * DOWN

        def pos(k):
            ang = TAU * (k % n) / n
            return center + radius * np.array([np.cos(ang), np.sin(ang), 0])

        circle = Circle(radius=radius, color=GREY_B).move_to(center)
        dots = VGroup(*[Dot(pos(k), radius=0.05, color=GREY_B) for k in range(n)])
        labels = VGroup()
        for k, v in enumerate(vals):
            direction = (pos(k) - center) / radius
            lbl = MathTex(str(v), font_size=30,
                          color=NOISE if v == 16 else WHITE)
            lbl.move_to(center + (radius + 0.42) * direction)
            labels.add(lbl)
        self.play(Create(circle), FadeIn(dots), Write(labels))

        cap = MathTex(r"\times\,2\ \text{ means: hop one position}", font_size=36,
                      color=SCALE).to_edge(DOWN, buff=1.1)
        self.play(Write(cap))

        mover = Dot(pos(0), radius=0.11, color=MSG)
        power = MathTex(r"2^{0} \equiv 1", font_size=36, color=MSG).next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(mover), Write(power))

        half_note = None
        for k in range(1, n + 1):
            arc = Arc(arc_center=center, radius=radius,
                      start_angle=TAU * (k - 1) / n, angle=TAU / n, color=MSG)
            v = vals[k % n]
            colour = NOISE if k == 4 else MSG
            extra = r"\ (=-1)" if k == 4 else ""
            new_power = MathTex(rf"2^{{{k}}} \equiv {v}{extra}", font_size=36, color=colour)
            new_power.next_to(title, DOWN, buff=0.2)
            self.play(MoveAlongPath(mover, arc), Transform(power, new_power), run_time=0.5)
            if k == 4:
                self.play(Flash(mover, color=NOISE))
                half_note = Text("halfway around = negation, again", font_size=24, color=NOISE)
                half_note.next_to(cap, DOWN, buff=0.3)
                self.play(FadeIn(half_note))
                self.wait(0.5)
        self.wait(0.5)

        finale = Text("no complex numbers, no floats - just pow(2, k, 17)",
                      font_size=28, color=SCALE).to_edge(DOWN, buff=1.1)
        self.play(FadeOut(half_note), Transform(cap, finale))
        self.wait(1.8)
