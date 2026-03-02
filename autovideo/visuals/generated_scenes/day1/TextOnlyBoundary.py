from manim import *

class TextOnlyBoundary(Scene):
    def construct(self):
        # Background frame (3D cartoon-style border)
        frame = RoundedRectangle(
            width=12, height=7, corner_radius=0.8,
            stroke_width=8, stroke_color=TEAL_A, fill_opacity=0.1, fill_color=GREY_C
        )
        frame.set_z_index(-1)

        # Camera icon (simplified 2D cartoon style using circles and rectangles)
        camera_body = Circle(radius=0.6, color=BLUE, fill_opacity=0.8)
        lens = Circle(radius=0.25, color=YELLOW, fill_opacity=0.9)
        viewfinder = Rectangle(width=0.4, height=0.2, color=WHITE, fill_opacity=0.7).shift(UP * 0.1)
        camera = VGroup(camera_body, lens, viewfinder).scale(0.8)

        # Speaker icon (cartoon-style: cone + circle)
        speaker_cone = Triangle(color=PURPLE, fill_opacity=0.7).rotate(-PI/2).scale(0.6)
        speaker_circle = Circle(radius=0.2, color=PURPLE_E, fill_opacity=0.9)
        speaker = VGroup(speaker_cone, speaker_circle).scale(0.8).shift(RIGHT * 0.2)

        # Group icons and position left/right
        icons = VGroup(camera, speaker).arrange(RIGHT, buff=3)
        icons.shift(UP * 1.2)

        # Cross-out diagonal line (red, thick, cartoonish)
        cross_line = Line(
            start=icons.get_corner(DL) + LEFT * 0.3 + DOWN * 0.3,
            end=icons.get_corner(UR) + RIGHT * 0.3 + UP * 0.3,
            stroke_width=12,
            color=RED
        )

        # Central glowing 'ABC' text stream — animated sequence
        abc_texts = VGroup()
        base_text = Text("ABC", font_size=72, weight=BOLD, color=WHITE)
        for i in range(5):
            t = base_text.copy()
            t.shift(DOWN * (i * 0.8))
            # Glow effect via multiple copies with fading opacity & blur-like offset
            glow_layers = VGroup()
            for j, alpha in enumerate([0.4, 0.25, 0.15, 0.08]):
                offset = j * 0.08
                glow = t.copy().set_color(YELLOW).set_opacity(alpha).shift(UR * offset + UL * offset)
                glow_layers.add(glow)
            abc_texts.add(VGroup(t, glow_layers))

        # Assemble scene
        self.add(frame)
        self.play(FadeIn(frame), run_time=1.2)
        self.wait(0.5)
        self.play(FadeIn(icons), run_time=1)
        self.wait(0.5)
        self.play(Create(cross_line), run_time=1.2)
        self.wait(0.8)

        # Animate ABC stream: fade in sequentially with subtle upward float & glow pulse
        for i, abc_group in enumerate(abc_texts):
            abc_main = abc_group[0]
            abc_glow = abc_group[1]
            self.play(
                FadeIn(abc_main),
                FadeIn(abc_glow),
                abc_main.animate.shift(UP * 0.05).set_sheen(0.5, direction=UL),
                rate_func=smooth,
                run_time=0.7
            )
            self.wait(0.3)

        # Gentle pulse animation on all ABC texts
        self.play(
            abc_texts.animate.set_sheen(0.7, direction=UR).scale(1.02),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=1.5
        )
        self.play(
            abc_texts.animate.set_sheen(0, direction=RIGHT).scale(0.99),
            run_time=1.5
        )
        self.wait(1)
