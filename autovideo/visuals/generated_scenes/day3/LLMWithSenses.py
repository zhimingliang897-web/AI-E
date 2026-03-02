from manim import *

class LLMWithSenses(Scene):
    def construct(self):
        # Clean lab background: subtle grid and soft ambient light effect
        plane = NumberPlane(
            background_line_style={"stroke_color": GREY_C, "stroke_width": 1, "stroke_opacity": 0.2},
            axis_config={"stroke_opacity": 0.0},
        )
        plane.set_z_index(-1)

        # Cartoon brain (2D stylized — no 3D objects allowed)
        # Base brain shape using two mirrored lobes
        left_lobe = Ellipse(width=3.0, height=2.4, color=PURPLE_E).rotate(PI/6)
        right_lobe = Ellipse(width=3.0, height=2.4, color=PURPLE_E).rotate(-PI/6)
        brain_body = VGroup(left_lobe, right_lobe).move_to(ORIGIN)
        
        # Brain stem / base
        stem = Rectangle(width=0.8, height=1.2, fill_color=PURPLE_A, fill_opacity=1, stroke_width=0).move_to(DOWN * 1.4)
        brain = VGroup(brain_body, stem).set_stroke(PURPLE, width=3)

        # Glowing neural connections (curved lines with pulsing glow)
        connections = VGroup()
        for i in range(8):
            angle = TAU * i / 8
            start = brain.get_center() + 0.7 * np.array([np.cos(angle), np.sin(angle), 0])
            end_angle = (angle + PI/4) % TAU
            end = brain.get_center() + 1.3 * np.array([np.cos(end_angle), np.sin(end_angle), 0])
            arc = ArcBetweenPoints(start, end, angle=PI/3, color=YELLOW, stroke_width=2)
            arc.set_stroke(YELLOW, width=2.5, opacity=0.9)
            connections.add(arc)

        # Pulsing glow effect via animation (scale + opacity modulation)
        glow = Circle(radius=1.8, color=YELLOW, fill_opacity=0.15, stroke_width=0).move_to(brain.get_center())
        glow.set_z_index(-1)

        # Eyes (two symmetric eyes above brain)
        eye_left = Circle(radius=0.35, color=WHITE, stroke_width=2).move_to(UP * 1.2 + LEFT * 0.8)
        eye_right = Circle(radius=0.35, color=WHITE, stroke_width=2).move_to(UP * 1.2 + RIGHT * 0.8)
        pupil_left = Circle(radius=0.15, color=BLACK).move_to(eye_left.get_center())
        pupil_right = Circle(radius=0.15, color=BLACK).move_to(eye_right.get_center())
        eyes = VGroup(eye_left, eye_right, pupil_left, pupil_right)

        # Ears (simplified curved shapes on sides)
        ear_left = Arc(start_angle=PI/4, angle=PI*0.8, radius=0.6, color=TEAL_A, stroke_width=2).flip().rotate(PI/6).move_to(LEFT * 2.2 + UP * 0.2)
        ear_right = Arc(start_angle=PI/4, angle=PI*0.8, radius=0.6, color=TEAL_A, stroke_width=2).rotate(-PI/6).move_to(RIGHT * 2.2 + UP * 0.2)
        ears = VGroup(ear_left, ear_right)

        # Labels (subtle)
        text_llm = Text("LLM", font_size=28, weight=BOLD, color=WHITE).next_to(brain, UP, buff=0.3)
        text_senses = Text("Senses", font_size=24, color=GREY_C).next_to(text_llm, UP, buff=0.2)

        # Assemble scene
        self.add(plane)
        self.play(
            Create(brain, run_time=2),
            FadeIn(glow, scale=0.5, run_time=2),
            rate_func=smooth
        )
        self.wait(0.5)
        self.play(
            Create(connections, lag_ratio=0.2, run_time=3),
            FadeIn(eyes, shift=DOWN * 0.2, run_time=1.5),
            FadeIn(ears, shift=DOWN * 0.1, run_time=1.5),
            Write(text_llm),
            Write(text_senses),
        )
        self.wait(0.5)

        # Pulse glow and connections
        self.play(
            glow.animate.scale(1.05).set_opacity(0.25),
            connections.animate.set_opacity(1.0),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=1.2
        )
        self.play(
            glow.animate.scale(0.95).set_opacity(0.15),
            connections.animate.set_opacity(0.9),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=1.2
        )

        # Subtle zoom-in & cinematic lighting emphasis (via scaling + brightness shift)
        self.play(
            brain.animate.scale(1.03).set_stroke(width=3.5),
            glow.animate.scale(1.02),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(1.5)
