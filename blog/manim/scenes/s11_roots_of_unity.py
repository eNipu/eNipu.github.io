"""S11 - Roots of unity: multiplication that rotates.

Step a point around the 8th roots of unity by repeated multiplication by
omega. Halfway around (omega^4) is -1: negation IS a half turn. Then connect
to FV, where x is the same object with 32 steps.
"""

from manim import *

from theme import MSG, NOISE, SCALE


class RootsOfUnity(Scene):
    def construct(self):
        title = Text("Roots of unity: rotation as multiplication", font_size=36).to_edge(UP)
        self.play(Write(title))

        n = 8
        radius = 1.85
        center = 0.15 * UP

        def pos(k):
            ang = TAU * (k % n) / n
            return center + radius * np.array([np.cos(ang), np.sin(ang), 0])

        circle = Circle(radius=radius, color=GREY_B).move_to(center)
        dots = VGroup(*[Dot(pos(k), radius=0.05, color=GREY_B) for k in range(n)])
        one_lbl = MathTex("1", font_size=32).move_to(center + (radius + 0.35) * RIGHT)
        minus_lbl = MathTex("-1", font_size=32).move_to(center + (radius + 0.45) * LEFT)
        w_dir = (pos(1) - center) / radius
        w_lbl = MathTex(r"\omega", font_size=32, color=SCALE).move_to(center + (radius + 0.4) * w_dir)
        self.play(Create(circle), FadeIn(dots))
        self.play(Write(one_lbl), Write(minus_lbl), Write(w_lbl))

        cap = MathTex(r"\times\,\omega\ \text{ means: rotate } \tfrac{1}{8} \text{ of a turn}",
                      font_size=36, color=SCALE).to_edge(DOWN, buff=1.1)
        self.play(Write(cap))

        mover = Dot(pos(0), radius=0.11, color=MSG)
        power = MathTex(r"\omega^{0}=1", font_size=36, color=MSG).next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(mover), Write(power))

        half_note = None
        for k in range(1, n + 1):
            arc = Arc(arc_center=center, radius=radius,
                      start_angle=TAU * (k - 1) / n, angle=TAU / n, color=MSG)
            suffix = r"=-1" if k == 4 else (r"=1" if k == 8 else "")
            colour = NOISE if k == 4 else MSG
            new_power = MathTex(rf"\omega^{{{k}}}{suffix}", font_size=36, color=colour)
            new_power.next_to(title, DOWN, buff=0.3)
            self.play(MoveAlongPath(mover, arc), Transform(power, new_power), run_time=0.5)
            if k == 4:
                self.play(Flash(mover, color=NOISE))
                half_note = Text("half a turn = negation", font_size=24, color=NOISE)
                half_note.next_to(cap, DOWN, buff=0.3)
                self.play(FadeIn(half_note))
                self.wait(0.5)
        self.wait(0.5)

        finale = MathTex(r"\text{in FV, } x \text{ is this with } 32 \text{ steps:}\quad x^{16}\equiv -1",
                         font_size=36, color=SCALE).to_edge(DOWN, buff=1.1)
        self.play(FadeOut(half_note), Transform(cap, finale))
        self.wait(1.8)
