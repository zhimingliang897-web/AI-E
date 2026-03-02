from manim import *

class GIGOFlow(Scene):
    def construct(self):
        # Background is black by default

        # Create trash can for "Garbage In"
        trash_in = VGroup()
        # Trash can body: rectangle + rounded top
        body = Rectangle(height=2.0, width=1.2, fill_color=GREY_C, fill_opacity=1, stroke_color=GREY_C)
        lid = Arc(start_angle=PI, angle=PI, radius=0.6, stroke_color=GREY_C, stroke_width=4)
        lid.move_to(body.get_top() + DOWN * 0.1)
        trash_in.add(body, lid)
        # Handle
        handle = Arc(start_angle=PI/2, angle=-PI, radius=0.3, stroke_color=GREY_C, stroke_width=4)
        handle.move_to(body.get_top() + UP * 0.3)
        trash_in.add(handle)
        trash_in.move_to(LEFT * 5)

        # Label for "Garbage In"
        label_in = Text("Garbage In", font="Arial", weight=BOLD, color=WHITE).next_to(trash_in, DOWN, buff=0.5)

        # Create trash can for "Garbage Out"
        trash_out = trash_in.copy()
        trash_out.move_to(RIGHT * 5)

        # Label for "Garbage Out"
        label_out = Text("Garbage Out", font="Arial", weight=BOLD, color=WHITE).next_to(trash_out, DOWN, buff=0.5)

        # LLM icon: stylized brain-like shape using circles and arcs
        llm_icon = VGroup()
        # Main oval (brain base)
        brain_oval = Ellipse(width=2.4, height=1.8, fill_color=BLUE, fill_opacity=0.8, stroke_color=BLUE_E, stroke_width=3)
        # Two hemispheres
        left_hemi = Circle(radius=0.7, fill_color=BLUE_A, fill_opacity=0.9, stroke_color=BLUE_E, stroke_width=2)
        right_hemi = left_hemi.copy()
        left_hemi.move_to(brain_oval.get_center() + LEFT * 0.4)
        right_hemi.move_to(brain_oval.get_center() + RIGHT * 0.4)
        # Central connector arc
        connector = ArcBetweenPoints(
            left_hemi.get_right() + LEFT * 0.1,
            right_hemi.get_left() + RIGHT * 0.1,
            angle=PI/3,
            stroke_color=BLUE_E,
            stroke_width=2
        )
        # Add synapse-like dots
        synapses = VGroup()
        for i in range(6):
            angle = TAU * i / 6
            dot = Dot(
                point=brain_oval.get_center() + 0.9 * np.array([np.cos(angle), np.sin(angle), 0]),
                color=TEAL_A,
                radius=0.07
            )
            synapses.add(dot)
        llm_icon.add(brain_oval, left_hemi, right_hemi, connector, synapses)
        llm_icon.move_to(ORIGIN)

        # Arrows
        arrow_left = Arrow(trash_in.get_right(), llm_icon.get_left() + LEFT * 0.3, buff=0.2, stroke_width=3, max_tip_length_to_length_ratio=0.1)
        arrow_right = Arrow(llm_icon.get_right() + RIGHT * 0.3, trash_out.get_left(), buff=0.2, stroke_width=3, max_tip_length_to_length_ratio=0.1)

        # Group all elements
        flow_group = VGroup(trash_in, label_in, trash_out, label_out, llm_icon, arrow_left, arrow_right)

        # Animate
        self.play(
            Create(trash_in),
            Write(label_in),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(
            Create(arrow_left),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            FadeIn(llm_icon),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(
            Create(arrow_right),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            Write(label_out),
            Create(trash_out),
            run_time=1.2
        )
        self.wait(1)

        # Spin the LLM icon for 3 seconds
        self.play(
            Rotate(llm_icon, angle=TAU * 3, about_point=llm_icon.get_center()),
            run_time=3,
            rate_func=linear
        )
        self.wait(1)
