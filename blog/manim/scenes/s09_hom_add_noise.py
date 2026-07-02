"""S09 - Homomorphic addition: add ciphertexts, and the noise adds too.

Adding the two ciphertext components adds the messages - but the noise budgets
add as well, so only a limited number of additions are safe.
"""

from manim import *

from theme import MSG, NOISE


class HomAddNoise(Scene):
    def construct(self):
        title = Text("Homomorphic addition", font_size=40).to_edge(UP)
        self.play(Write(title))

        line = MathTex(
            r"E(m_1) + E(m_2)", r"=", r"E(m_1 + m_2)", font_size=48
        ).next_to(title, DOWN, buff=0.6)
        line[0].set_color(MSG)
        line[2].set_color(MSG)
        self.play(Write(line[0]))
        self.play(Write(line[1]), Write(line[2]))
        note = Text("add componentwise; the message just adds", font_size=25, color=MSG)
        note.next_to(line, DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(0.8)

        # Noise budget bar filling as additions accumulate
        bar_bg = RoundedRectangle(width=8.0, height=0.7, corner_radius=0.1, color=GREY_B)
        bar_bg.next_to(note, DOWN, buff=1.0)
        budget_line = DashedLine(bar_bg.get_corner(UR), bar_bg.get_corner(DR), color=WHITE)
        budget_lbl = Text("budget", font_size=22).next_to(bar_bg, RIGHT, buff=0.2)
        self.play(Create(bar_bg), Create(budget_line), FadeIn(budget_lbl))

        counter = Integer(0, font_size=40).next_to(bar_bg, UP, buff=0.35)
        counter_lbl = Text("additions", font_size=22).next_to(counter, RIGHT, buff=0.25)
        self.play(FadeIn(counter), FadeIn(counter_lbl))

        fill = Rectangle(width=0.01, height=0.7, color=NOISE, fill_opacity=0.8)
        fill.align_to(bar_bg, LEFT).set_y(bar_bg.get_y())
        self.add(fill)

        widths = [0.9, 1.7, 2.4, 3.1, 3.8, 4.6, 5.6, 6.9, 8.2]
        for i, w in enumerate(widths, start=1):
            target = Rectangle(width=min(w, 8.0), height=0.7,
                               color=NOISE if w < 8.0 else YELLOW, fill_opacity=0.8)
            target.align_to(bar_bg, LEFT).set_y(bar_bg.get_y())
            self.play(Transform(fill, target), ChangeDecimalToValue(counter, i), run_time=0.4)
            if w >= 8.0:
                break

        warn = Text("noise overflows the budget, so decryption silently fails",
                    font_size=26, color=YELLOW).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(warn))
        self.wait(1.6)
