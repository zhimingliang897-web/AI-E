from manim import *

class TextFormulaAnimation(Scene):
    def construct(self):
        # Create clean, bold, cartoon-style text
        text = Text("Large Language Model (LLM)", font="Comic Sans MS", weight=BOLD, font_size=36)
        text.set_color(WHITE)

        # Create glowing underline: a thick line with glow effect via multiple layers
        underline_base = Line(
            start=text.get_left() + DOWN * 0.3,
            end=text.get_right() + DOWN * 0.3,
            stroke_width=8,
            color=BLUE
        )
        # Add glow by layering slightly larger, more transparent lines
        glow_lines = VGroup()
        for i in range(3):
            offset = i * 0.05
            alpha = 0.4 - i * 0.12
            glow_line = Line(
                start=text.get_left() + DOWN * (0.3 + offset),
                end=text.get_right() + DOWN * (0.3 + offset),
                stroke_width=8 + i * 4,
                color=BLUE,
                stroke_opacity=alpha
            )
            glow_lines.add(glow_line)

        # Group text and underline for coordinated animation
        group = VGroup(text, glow_lines).move_to(ORIGIN)

        # Subtle zoom-in effect: scale from 0.9 to 1.0 with smooth easing
        self.play(
            FadeIn(text, scale=0.9),
            FadeIn(glow_lines),
            group.animate.scale(1.0).shift(UP * 0.2),  # slight upward centering during zoom
            rate_func=rate_functions.ease_in_out_sine,
            run_time=2
        )
        self.wait(0.5)

        # Gentle pulse glow effect on underline
        self.play(
            glow_lines.animate.set_stroke(opacity=0.7),
            rate_func=smooth,
            run_time=2
        )
        self.wait(1)

        # Hold final state
        self.wait(1)
