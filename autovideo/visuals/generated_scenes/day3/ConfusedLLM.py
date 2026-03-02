from manim import *

class ConfusedLLM(Scene):
    def construct(self):
        # Background ambient dim lighting effect (subtle gradient not possible, so use low-opacity gray overlay)
        ambient = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=GREY_C,
            fill_opacity=0.15,
            stroke_width=0
        ).set_z_index(-1)

        # Cartoon AI brain: simplified 2D stylized brain using interconnected ellipses and curves
        brain_parts = VGroup()
        
        # Main left hemisphere (slightly rotated)
        left_lobe = Ellipse(width=2.0, height=2.4, color=PURPLE_E).rotate(0.2)
        # Right hemisphere
        right_lobe = Ellipse(width=2.0, height=2.4, color=PURPLE_A).rotate(-0.2)
        # Central connecting "corpus callosum"
        connector = RoundedRectangle(width=0.6, height=0.9, corner_radius=0.2, fill_color=PURPLE, fill_opacity=1, stroke_width=0)
        
        brain_parts.add(left_lobe, right_lobe, connector)
        brain = brain_parts.set_stroke(PURPLE, width=2).set_fill(opacity=0.7)

        # Add subtle "neural" dots inside brain
        neural_dots = VGroup(*[
            Dot(point, radius=0.03, color=TEAL_A).set_z_index(1)
            for point in [
                left_lobe.point_at_angle(PI/4),
                left_lobe.point_at_angle(3*PI/4),
                right_lobe.point_at_angle(-PI/4),
                right_lobe.point_at_angle(-3*PI/4),
                connector.get_center() + UP*0.2,
                connector.get_center() + DOWN*0.2,
            ]
        ])

        # Question marks swirling around brain — animated along circular paths
        qmarks = VGroup()
        q_paths = []
        for i in range(6):
            angle = TAU * i / 6
            center_offset = 2.0 * np.array([np.cos(angle), np.sin(angle), 0])
            orbit_center = brain.get_center() + center_offset
            radius = 0.8 + 0.2 * np.sin(i)
            path = Circle(radius=radius, color=YELLOW, stroke_width=1.5).move_to(orbit_center).set_z_index(-1)
            qmark = Text("?", font_size=32, color=YELLOW, weight=BOLD).move_to(orbit_center + RIGHT*radius)
            qmarks.add(qmark)
            q_paths.append(path)

        # Broken gears: two mismatched, slightly cracked gear-like shapes
        gear1 = RegularPolygon(n=12, radius=0.5, color=GREY, stroke_width=2).set_stroke(GREY, width=2)
        crack1 = Line(UP*0.3, DOWN*0.3, stroke_width=3, color=RED).rotate(PI/6)
        gear1_group = VGroup(gear1, crack1).shift(LEFT*3.5 + UP*1.2)

        gear2 = RegularPolygon(n=8, radius=0.4, color=GREY, stroke_width=2).set_stroke(GREY, width=2)
        crack2 = Line(UP*0.25, DOWN*0.25, stroke_width=3, color=RED).rotate(-PI/4)
        gear2_group = VGroup(gear2, crack2).shift(RIGHT*3.0 + DOWN*1.0)

        # Mismatched icons: eye, ear, cloud (as simple symbolic shapes)
        # Eye
        eye_outer = Circle(radius=0.35, color=BLUE, stroke_width=2)
        eye_inner = Circle(radius=0.15, color=BLUE_D).move_to(eye_outer.get_center())
        pupil = Dot(eye_outer.get_center(), radius=0.06, color=BLACK)
        eye = VGroup(eye_outer, eye_inner, pupil).shift(LEFT*2.5 + DOWN*1.5)

        # Ear
        ear_base = Ellipse(width=0.5, height=0.7, color=ORANGE, stroke_width=2)
        ear_inner = Ellipse(width=0.2, height=0.4, color=ORANGE_D).move_to(ear_base.get_center())
        ear = VGroup(ear_base, ear_inner).shift(RIGHT*2.8 + UP*1.0)

        # Cloud (symbolic "thought" or "cloud computing")
        cloud = VGroup(
            Circle(radius=0.3, color=TEAL, fill_opacity=0.8, stroke_width=0),
            Circle(radius=0.35, color=TEAL, fill_opacity=0.8, stroke_width=0).shift(LEFT*0.3),
            Circle(radius=0.25, color=TEAL, fill_opacity=0.8, stroke_width=0).shift(RIGHT*0.3),
            Circle(radius=0.3, color=TEAL, fill_opacity=0.8, stroke_width=0).shift(DOWN*0.2),
        ).shift(UP*2.2 + RIGHT*0.5)

        # Assemble all floating elements
        floaters = VGroup(gear1_group, gear2_group, eye, ear, cloud)

        # Initial positioning
        self.add(ambient)
        self.play(
            FadeIn(brain, shift=DOWN*0.5, scale=0.8),
            FadeIn(neural_dots, shift=UP*0.3),
            run_time=1.5
        )
        self.wait(0.5)

        # Animate question marks orbiting
        self.play(
            LaggedStart(*[
                MoveAlongPath(q, p, rate_func=linear, run_time=4)
                for q, p in zip(qmarks, q_paths)
            ], lag_ratio=0.15),
            FadeIn(qmarks),
            run_time=4
        )

        # Float in broken gears and icons with gentle float animation
        self.play(
            LaggedStart(
                FadeIn(gear1_group, shift=UP*0.5),
                FadeIn(gear2_group, shift=DOWN*0.5),
                FadeIn(eye, shift=LEFT*0.3),
                FadeIn(ear, shift=RIGHT*0.3),
                FadeIn(cloud, shift=UP*0.4),
                lag_ratio=0.3
            ),
            run_time=2.5
        )

        # Gentle bob & rotate floaters to enhance "confused floating" feel
        self.play(
            floaters.animate.shift(UP*0.1).rotate(0.02),
            run_time=2,
            rate_func=smooth
        )

        self.wait(1.5)
