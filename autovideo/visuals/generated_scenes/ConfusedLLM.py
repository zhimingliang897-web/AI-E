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
        # Central connector (brainstem-like)
        stem = Ellipse(width=0.6, height=1.2, color=PURPLE).rotate(PI/6)
        
        brain_parts.add(left_lobe, right_lobe, stem)
        brain = brain_parts.set_stroke(width=3).set_fill(opacity=0.7)

        # Add subtle "neural" arcs inside brain
        arc1 = Arc(radius=0.8, start_angle=0, angle=PI, color=TEAL_A, stroke_width=1.5).move_to(left_lobe.get_center() + LEFT*0.3 + UP*0.2)
        arc2 = Arc(radius=0.7, start_angle=PI, angle=PI, color=TEAL_A, stroke_width=1.5).move_to(right_lobe.get_center() + RIGHT*0.3 + UP*0.2)
        brain.add(arc1, arc2)

        # Question marks swirling around brain — 5 total, orbiting at different radii & speeds
        qmarks = VGroup()
        for i in range(5):
            q = Text("?", font_size=36, color=YELLOW).rotate(PI/4)
            qmarks.add(q)

        # Position question marks in a loose circular arrangement
        angles = [0, TAU/5, 2*TAU/5, 3*TAU/5, 4*TAU/5]
        radii = [1.8, 2.0, 1.6, 2.1, 1.7]
        for i, (angle, r) in enumerate(zip(angles, radii)):
            x = r * np.cos(angle)
            y = r * np.sin(angle) * 0.6  # squash vertically for orbit
            qmarks[i].move_to(brain.get_center() + [x, y, 0])

        # Broken gears: two mismatched, slightly cracked gears
        gear1 = RegularPolygon(n=12, radius=0.4, color=GREY, fill_opacity=0.8, stroke_width=2)
        crack1 = Line(UP*0.2, DOWN*0.2, stroke_width=3, color=RED).rotate(PI/6)
        gear1_group = VGroup(gear1, crack1).move_to(brain.get_center() + UL*2.2)

        gear2 = RegularPolygon(n=8, radius=0.35, color=GREY, fill_opacity=0.7, stroke_width=2)
        crack2 = Line(LEFT*0.15, RIGHT*0.15, stroke_width=3, color=RED).rotate(-PI/4)
        gear2_group = VGroup(gear2, crack2).move_to(brain.get_center() + DR*2.4)

        # Mismatched icons: eye, ear, cloud (for 'cloud AI'), lightning (for 'processing'), and a broken chain link
        eye = VGroup(
            Circle(radius=0.3, color=BLUE, fill_opacity=0.2),
            Circle(radius=0.1, color=BLUE_E, fill_opacity=1),
            ArcBetweenPoints(LEFT*0.25 + UP*0.05, RIGHT*0.25 + UP*0.05, angle=PI/3, color=BLUE, stroke_width=2)
        ).scale(0.7).move_to(brain.get_center() + UR*2.0)

        ear = VGroup(
            Circle(radius=0.35, color=ORANGE, fill_opacity=0.2),
            Circle(radius=0.12, color=ORANGE_E, fill_opacity=1),
            Arc(start_angle=PI/2, angle=-PI, radius=0.2, color=ORANGE, stroke_width=2)
        ).scale(0.7).move_to(brain.get_center() + DL*2.0)

        cloud = Circle(radius=0.4, color=GREY_B, fill_opacity=0.3, stroke_width=2)
        cloud.shift(UP*0.1)
        cloud = VGroup(cloud, Circle(radius=0.3, color=GREY_B, fill_opacity=0.3, stroke_width=2).shift(UR*0.2), 
                       Circle(radius=0.35, color=GREY_B, fill_opacity=0.3, stroke_width=2).shift(UL*0.15))
        cloud.move_to(brain.get_center() + LEFT*2.5)

        lightning = VGroup(
            Line(ORIGIN, UP*0.4, stroke_width=4, color=YELLOW_E),
            Line(UP*0.4, UP*0.4 + RIGHT*0.3, stroke_width=4, color=YELLOW_E),
            Line(UP*0.4 + RIGHT*0.3, UP*0.2, stroke_width=4, color=YELLOW_E),
            Line(UP*0.2, UP*0.2 + RIGHT*0.3, stroke_width=4, color=YELLOW_E),
            Line(UP*0.2 + RIGHT*0.3, ORIGIN, stroke_width=4, color=YELLOW_E)
        ).scale(0.6).move_to(brain.get_center() + RIGHT*2.3)

        chain_link = VGroup(
            Arc(radius=0.25, start_angle=0, angle=PI, color=GREY, stroke_width=3),
            Arc(radius=0.25, start_angle=PI, angle=PI, color=GREY, stroke_width=3),
            Line(LEFT*0.25, RIGHT*0.25, stroke_width=3, color=GREY),
            Line(UP*0.25, DOWN*0.25, stroke_width=3, color=GREY)
        ).scale(0.5).move_to(brain.get_center() + UP*2.4)

        # Group all floating elements
        floaters = VGroup(
            qmarks, gear1_group, gear2_group,
            eye, ear, cloud, lightning, chain_link
        )

        # Animate
        self.add(ambient)
        self.play(
            Create(brain, run_time=2),
            Write(Text("AI", font_size=28, color=PURPLE_E).move_to(brain.get_center())),
            run_time=2
        )
        self.wait(0.5)

        # Animate question marks swirling slowly
        self.play(
            Rotate(qmarks, angle=TAU, about_point=brain.get_center(), run_time=6, rate_func=linear),
            floaters.animate.shift(DOWN*0.05).set_opacity(0.9),
            run_time=6
        )

        # Wiggle gears and icons slightly to emphasize 'broken/confused'
        self.play(
            gear1_group.animate.scale(1.05).set_color(RED_E),
            gear2_group.animate.scale(1.05).set_color(RED_E),
            eye.animate.rotate(0.1).set_color(RED_E),
            ear.animate.rotate(-0.1).set_color(RED_E),
            run_time=1.5
        )
        self.play(
            gear1_group.animate.scale(0.95).set_color(GREY),
            gear2_group.animate.scale(0.95).set_color(GREY),
            eye.animate.rotate(-0.1).set_color(BLUE),
            ear.animate.rotate(0.1).set_color(ORANGE),
            run_time=1.5
        )

        self.wait(1)
