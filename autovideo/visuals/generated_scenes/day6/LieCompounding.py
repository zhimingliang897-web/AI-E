from manim import *

class LieCompounding(Scene):
    def construct(self):
        # Use clean, bold sans-serif font; simulate "3D cartoon style" with subtle glow and depth via layering/shadow effect
        words = [
            "Lie", "Compound", "Deceive", "Fabricate", "Mislead", 
            "Distort", "Exaggerate", "Omit", "Twist", "Manipulate", "Believe"
        ]
        
        # Create word objects with consistent styling
        word_mobjects = []
        for i, word in enumerate(words):
            txt = Text(word, font="Arial", weight=BOLD, font_size=32)
            if i == 9:  # word10 → index 9 ("Manipulate")
                txt = Text(word, font="Arial", weight=BOLD, font_size=32, color=RED)
                txt.set_stroke(RED, width=2, opacity=0.7)  # glowing red effect
            elif i == 10:  # word11 → "Believe" (branching wrong)
                txt = Text(word, font="Arial", weight=BOLD, font_size=32, color=YELLOW)
                txt.set_stroke(YELLOW, width=2.5, opacity=0.8)
            else:
                txt.set_color(GREY_C)
            word_mobjects.append(txt)

        # Horizontal chain layout — spaced evenly
        chain_group = VGroup(*word_mobjects).arrange(RIGHT, buff=1.0)

        # Add subtle "3D cartoon" feel: slight offset shadows (using copies with low opacity & offset)
        shadow_group = VGroup()
        for w in word_mobjects:
            shadow = w.copy().set_opacity(0.15).set_color(BLACK).shift(DOWN * 0.08 + RIGHT * 0.08)
            shadow_group.add(shadow)
        self.add(shadow_group)

        # Initial state: only first word visible
        self.play(FadeIn(word_mobjects[0], scale=1.2))
        self.wait(0.5)

        # Animate chain one-by-one with smooth transitions
        for i in range(1, len(word_mobjects)):
            # Arrow from previous to current
            if i > 1:
                arrow = Arrow(
                    word_mobjects[i-2].get_right(),
                    word_mobjects[i-1].get_left(),
                    stroke_width=3,
                    buff=0.1,
                    color=GREY_A
                )
                self.play(GrowArrow(arrow), run_time=0.6)
                self.wait(0.2)
            
            # Fade in current word with slight scale-up
            self.play(
                FadeIn(word_mobjects[i], shift=RIGHT * 0.3, scale=1.15),
                run_time=0.7,
                rate_func=smooth
            )
            self.wait(0.4)

        # Highlight word10 ("Manipulate") with pulsing glow
        word10 = word_mobjects[9]
        self.play(
            word10.animate.set_stroke(RED, width=4, opacity=1.0),
            rate_func=smooth,
            run_time=1.8
        )

        # Branching wrong: word11 ("Believe") emerges diagonally up-right from word10
        branch_arrow = CurvedArrow(
            word10.get_top() + UP * 0.2,
            word_mobjects[10].get_center() + UR * 0.8,
            angle=-PI/4,
            stroke_width=4,
            color=YELLOW
        )
        self.play(
            Create(branch_arrow, run_time=1.2),
            FadeIn(word_mobjects[10], shift=UR * 0.5, scale=1.25),
            run_time=1.2
        )
        self.wait(0.8)

        # Final emphasis: pulse word11 and subtly wiggle word10 to imply instability/wrongness
        self.play(
            word_mobjects[10].animate.scale(1.05).set_stroke(YELLOW, width=3.5),
            word10.animate.scale(0.98).set_stroke(RED, width=4.5),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(1)
