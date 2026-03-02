from manim import *

class MultimodalFusion(Scene):
    def construct(self):
        # Background remains black (default)

        # Create text icon (left): speech bubble + "T" letter
        text_icon = VGroup()
        bubble = Circle(radius=0.8, color=BLUE, fill_opacity=0.2).set_stroke(BLUE, width=3)
        tail = Polygon(
            [-0.3, -0.5, 0], [0.0, -0.8, 0], [0.3, -0.5, 0],
            fill_opacity=0.2, stroke_color=BLUE, stroke_width=3
        )
        t_letter = Text("T", font_size=36, weight=BOLD, color=BLUE)
        text_icon.add(bubble, tail, t_letter)
        text_icon.move_to(LEFT * 4)

        # Create image icon (right): camera outline + grid
        image_icon = VGroup()
        cam_body = RoundedRectangle(width=1.4, height=0.9, corner_radius=0.2, color=GREEN, fill_opacity=0.15).set_stroke(GREEN, width=3)
        lens = Circle(radius=0.3, color=GREEN, fill_opacity=0.2).set_stroke(GREEN, width=3)
        viewfinder = Rectangle(width=0.8, height=0.5, color=GREEN, fill_opacity=0).set_stroke(GREEN, width=1.5)
        # Grid lines inside viewfinder
        grid_lines = VGroup()
        for i in range(1, 3):
            grid_lines.add(Line(
                viewfinder.get_corner(UL) + RIGHT * i * 0.4,
                viewfinder.get_corner(DL) + RIGHT * i * 0.4,
                stroke_color=GREEN, stroke_width=1
            ))
            grid_lines.add(Line(
                viewfinder.get_corner(UL) + DOWN * i * 0.25,
                viewfinder.get_corner(UR) + DOWN * i * 0.25,
                stroke_color=GREEN, stroke_width=1
            ))
        image_icon.add(cam_body, lens, viewfinder, grid_lines)
        image_icon.move_to(RIGHT * 4)

        # Center multimodal badge: rounded rectangle with "MULTIMODAL" text and glow effect
        badge_bg = RoundedRectangle(width=3.2, height=1.4, corner_radius=0.4, color=PURPLE, fill_opacity=0.25).set_stroke(PURPLE, width=4)
        badge_text = Text("MULTIMODAL", font_size=32, weight=BOLD, color=PURPLE)
        badge = VGroup(badge_bg, badge_text)
        badge.move_to(ORIGIN)

        # '+' symbol centered on badge
        plus = Text("+", font_size=48, weight=BOLD, color=YELLOW).move_to(ORIGIN)

        # Glow lines: curved arrows from icons to badge
        left_glow = CurvedArrow(
            text_icon.get_right(),
            badge.get_left(),
            angle=-PI/4,
            color=YELLOW,
            stroke_width=4,
            tip_length=0.15
        )
        right_glow = CurvedArrow(
            image_icon.get_left(),
            badge.get_right(),
            angle=PI/4,
            color=YELLOW,
            stroke_width=4,
            tip_length=0.15
        )

        # Add all elements
        self.play(
            FadeIn(text_icon),
            FadeIn(image_icon),
            FadeIn(badge_bg),
            Write(badge_text),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            Create(left_glow),
            Create(right_glow),
            Write(plus),
            run_time=1.5
        )
        self.wait(0.5)

        # Subtle pulse animation on glow lines and badge
        self.play(
            left_glow.animate.set_stroke(width=6, color=YELLOW_E),
            right_glow.animate.set_stroke(width=6, color=YELLOW_E),
            badge_bg.animate.set_fill(opacity=0.35),
            rate_func=smooth,
            run_time=2
        )
        self.wait(1)

        # Final emphasis: scale up badge slightly and highlight '+'
        self.play(
            badge.animate.scale(1.05),
            plus.animate.scale(1.15).set_color(ORANGE),
            rate_func=smooth,
            run_time=1.2
        )
        self.wait(1.5)
