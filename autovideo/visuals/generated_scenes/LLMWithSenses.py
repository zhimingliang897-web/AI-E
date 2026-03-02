from manim import *

class LLMWithSenses(Scene):
    def construct(self):
        # Clean lab background: subtle grid and soft ambient light effect
        plane = NumberPlane(
            background_line_style={"stroke_color": GREY_C, "stroke_width": 1, "stroke_opacity": 0.2},
            axis_config={"stroke_opacity": 0.0},
        )
        plane.set_z_index(-2)

        # Cartoon brain (2D stylized — no 3D objects allowed)
        # Base brain shape using two mirrored lobes
        left_lobe = Ellipse(width=3.0, height=2.4, color=PURPLE_E).rotate(PI/6)
        right_lobe = Ellipse(width=3.0, height=2.4, color=PURPLE_E).rotate(-PI/6)
        brain_core = VGroup(left_lobe, right_lobe).move_to(ORIGIN)
        
        # Add a smooth "cartoon brain" outline
        brain_outline = RoundedRectangle(
            width=3.8, height=2.6, corner_radius=0.8,
            stroke_color=PURPLE_A, stroke_width=6, fill_opacity=0,
        ).move_to(ORIGIN)
        
        # Glowing neural connections: curved lines with pulsing glow
        connections = VGroup()
        for i in range(8):
            angle = i * TAU / 8
            start = brain_core.get_center() + 0.7 * np.array([np.cos(angle), np.sin(angle), 0])
            end_angle = (angle + PI/4) % TAU
            end = brain_core.get_center() + 0.9 * np.array([np.cos(end_angle), np.sin(end_angle), 0])
            arc = ArcBetweenPoints(start, end, angle=PI/3, stroke_color=YELLOW, stroke_width=2)
            connections.add(arc)
        
        # Add small glowing nodes at connection endpoints
        nodes = VGroup()
        for conn in connections:
            for p in [conn.get_start(), conn.get_end()]:
                dot = Dot(p, color=YELLOW, radius=0.07)
                glow = Circle(radius=0.15, color=YELLOW, fill_opacity=0.3, stroke_width=0).move_to(p)
                nodes.add(VGroup(dot, glow))
        
        # Eyes (two symmetric eyes above brain)
        eye_left = Circle(radius=0.35, color=WHITE, stroke_color=GREY_C, stroke_width=2).shift(UP*1.4 + LEFT*1.0)
        eye_right = Circle(radius=0.35, color=WHITE, stroke_color=GREY_C, stroke_width=2).shift(UP*1.4 + RIGHT*1.0)
        pupil_left = Circle(radius=0.15, color=BLACK).move_to(eye_left.get_center())
        pupil_right = Circle(radius=0.15, color=BLACK).move_to(eye_right.get_center())
        eyes = VGroup(eye_left, eye_right, pupil_left, pupil_right)

        # Ears (two simple ear-like shapes beside brain)
        ear_left = Arc(start_angle=PI/4, angle=PI*0.8, radius=0.6, color=TEAL_A, stroke_width=3).flip().rotate(PI/6).shift(LEFT*2.2 + DOWN*0.3)
        ear_right = Arc(start_angle=PI/4, angle=PI*0.8, radius=0.6, color=TEAL_A, stroke_width=3).rotate(-PI/6).shift(RIGHT*2.2 + DOWN*0.3)
        ears = VGroup(ear_left, ear_right)

        # Label "LLM" centered above brain
        label = Text("LLM", font_size=36, weight=BOLD, color=YELLOW).next_to(brain_core, UP, buff=0.5)

        # Assemble all elements
        scene_elements = VGroup(
            plane,
            brain_core,
            brain_outline,
            connections,
            nodes,
            eyes,
            ears,
            label
        )

        # Animation sequence
        self.camera.background_color = "#0c0c14"
        self.play(FadeIn(plane), run_time=1.5)
        self.wait(0.5)

        # Build brain core
        self.play(
            Create(left_lobe, run_time=1.2),
            Create(right_lobe, run_time=1.2),
            rate_func=smooth
        )
        self.wait(0.5)
        self.play(Create(brain_outline), run_time=1.0)
        self.wait(0.5)

        # Animate neural connections with glow pulse
        self.play(
            LaggedStart(*[Create(conn) for conn in connections], lag_ratio=0.15),
            run_time=2.0
        )
        self.play(
            LaggedStart(*[FadeIn(node) for node in nodes], lag_ratio=0.1),
            run_time=1.5
        )
        self.wait(0.5)

        # Reveal eyes and ears
        self.play(FadeIn(eyes), FadeIn(ears), run_time=1.2)
        self.wait(0.5)
        self.play(FadeIn(label), run_time=0.8)
        self.wait(1.0)

        # Subtle "glow pulse" on connections and nodes
        pulse_animations = []
        for conn in connections:
            pulse_animations.append(conn.animate.set_stroke(opacity=0.3).set_stroke(YELLOW_E))
        for node in nodes:
            pulse_animations.append(node.animate.scale(1.3).set_color(YELLOW_D))
        self.play(*pulse_animations, run_time=1.0)
        self.play(*[anim.reverse() for anim in pulse_animations], run_time=1.0)

        self.wait(1.5)
