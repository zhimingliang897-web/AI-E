from manim import *

class ParametersLabel(Scene):
    def construct(self):
        # Background is black by default

        # Create gear icon using circles and arcs
        gear = VGroup()
        outer_circle = Circle(radius=0.6, color=YELLOW_E).set_stroke(width=4)
        gear.add(outer_circle)

        # Add 6 gear teeth (arcs)
        for i in range(6):
            angle = i * TAU / 6
            start_point = outer_circle.point_at_angle(angle + PI/12)
            end_point = outer_circle.point_at_angle(angle - PI/12)
            tooth_arc = ArcBetweenPoints(
                start_point,
                end_point,
                angle=PI/3,
                stroke_color=YELLOW_E,
                stroke_width=4
            )
            gear.add(tooth_arc)

        # Group gear and center dot
        center_dot = Dot(color=YELLOW_E, radius=0.15)
        gear.add(center_dot)

        # "Parameters" text
        params_text = Text("Parameters", font="Arial", weight=BOLD, font_size=48, color=WHITE)
        params_text.next_to(gear, RIGHT, buff=0.5)

        # Group label
        label_group = VGroup(gear, params_text)
        label_group.move_to(ORIGIN)

        # Scale numbers: '1B → 10B → 100B → 1T'
        scale_texts = [
            Text("1B", font_size=36, color=TEAL_A),
            Text("10B", font_size=36, color=TEAL_A),
            Text("100B", font_size=36, color=TEAL_A),
            Text("1T", font_size=36, color=TEAL_A),
        ]

        # Position horizontally
        scale_group = VGroup()
        for i, txt in enumerate(scale_texts):
            txt.move_to((i * 3.0) * RIGHT)
            scale_group.add(txt)

        # Glowing arrows between them
        arrows = VGroup()
        glow_colors = [BLUE_A, BLUE_B, BLUE_C]
        for i in range(3):
            arrow = Arrow(
                scale_texts[i].get_right(),
                scale_texts[i+1].get_left(),
                buff=0.2,
                stroke_width=6,
                color=glow_colors[i % len(glow_colors)]
            )
            # Add glow effect via multiple copies with increasing opacity & blur (simulated)
            glow_arrow = arrow.copy().set_opacity(0.3).scale(1.3)
            glow_arrow2 = arrow.copy().set_opacity(0.15).scale(1.6)
            arrows.add(VGroup(arrow, glow_arrow, glow_arrow2))

        # Assemble full scale line
        scale_full = VGroup(scale_group, arrows)
        scale_full.next_to(label_group, DOWN, buff=1.5)

        # Animate floating effect (subtle up-down + rotation)
        self.play(
            FadeIn(gear, shift=UP * 0.5, scale=0.8),
            Write(params_text, run_time=1.5),
            rate_func=smooth
        )
        self.wait(0.5)

        # Float and gently rotate gear+text
        self.play(
            label_group.animate.shift(UP * 0.1).rotate(0.02),
            rate_func=smooth,
            run_time=3
        )

        # Animate scale in with glowing arrows
        self.play(
            FadeIn(scale_group[0], shift=UP * 0.3),
            run_time=0.8
        )
        for i in range(3):
            self.play(
                FadeIn(arrows[i], shift=RIGHT * 0.2),
                FadeIn(scale_group[i+1], shift=RIGHT * 0.3),
                run_time=0.9
            )
            self.wait(0.3)

        # Final subtle pulse on arrows
        self.play(
            arrows.animate.set_opacity(0.8),
            rate_func=smooth,
            run_time=2
        )

        self.wait(1)
