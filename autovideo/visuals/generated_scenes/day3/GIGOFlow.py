from manim import *

class GIGOFlow(Scene):
    def construct(self):
        # Background is black by default

        # Create trash can for "Garbage In"
        trash_in = VGroup()
        # Trash can body: rectangle + rounded top
        body = RoundedRectangle(
            height=2.0,
            width=1.4,
            corner_radius=0.2,
            fill_color=GREY_C,
            fill_opacity=1,
            stroke_color=GREY_C,
            stroke_width=2
        )
        # Trash can lid: horizontal rectangle on top
        lid = Rectangle(
            width=1.6,
            height=0.3,
            fill_color=GREY_C,
            fill_opacity=1,
            stroke_color=GREY_C,
            stroke_width=2
        ).next_to(body, UP, buff=0)
        # Trash can handle: small arc
        handle = Arc(
            radius=0.4,
            start_angle=PI / 2,
            angle=-PI,
            stroke_color=GREY_C,
            stroke_width=2
        ).move_to(body.get_top() + UP * 0.15)
        trash_in.add(body, lid, handle)
        trash_in_label = Text("Garbage In", font="Arial", weight=BOLD, font_size=24).next_to(trash_in, DOWN, buff=0.5)

        # Create trash can for "Garbage Out"
        trash_out = trash_in.copy()
        trash_out_label = Text("Garbage Out", font="Arial", weight=BOLD, font_size=24).next_to(trash_out, DOWN, buff=0.5)

        # LLM icon: simplified brain-like shape using circles and arcs
        llm_icon = VGroup()
        # Main oval (brain base)
        brain_base = Ellipse(
            width=2.2,
            height=1.6,
            fill_color=BLUE,
            fill_opacity=0.8,
            stroke_color=BLUE,
            stroke_width=2
        )
        # Left lobe
        left_lobe = Circle(
            radius=0.5,
            fill_color=BLUE,
            fill_opacity=0.8,
            stroke_color=BLUE,
            stroke_width=2
        ).shift(LEFT * 0.7 + UP * 0.2)
        # Right lobe
        right_lobe = Circle(
            radius=0.5,
            fill_color=BLUE,
            fill_opacity=0.8,
            stroke_color=BLUE,
            stroke_width=2
        ).shift(RIGHT * 0.7 + UP * 0.2)
        # Top bump
        top_bump = Circle(
            radius=0.3,
            fill_color=BLUE,
            fill_opacity=0.8,
            stroke_color=BLUE,
            stroke_width=2
        ).shift(UP * 0.8)
        llm_icon.add(brain_base, left_lobe, right_lobe, top_bump)
        # Add subtle internal lines to suggest neural network (lighter blue)
        line1 = Line(
            start=brain_base.get_left() + UP * 0.2,
            end=brain_base.get_right() + UP * 0.2,
            stroke_color=BLUE_E,
            stroke_width=1.5
        )
        line2 = Line(
            start=brain_base.get_left() + DOWN * 0.2,
            end=brain_base.get_right() + DOWN * 0.2,
            stroke_color=BLUE_E,
            stroke_width=1.5
        )
        line3 = Line(
            start=brain_base.get_top() + LEFT * 0.3,
            end=brain_base.get_top() + RIGHT * 0.3,
            stroke_color=BLUE_E,
            stroke_width=1.5
        )
        llm_icon.add(line1, line2, line3)
        llm_label = Text("LLM", font="Arial", weight=BOLD, font_size=28).next_to(llm_icon, DOWN, buff=0.4)

        # Position elements horizontally
        total_width = 10.0
        trash_in.move_to(LEFT * 4)
        trash_out.move_to(RIGHT * 4)
        llm_icon.move_to(ORIGIN)
        trash_in_label.next_to(trash_in, DOWN, buff=0.5)
        trash_out_label.next_to(trash_out, DOWN, buff=0.5)
        llm_label.next_to(llm_icon, DOWN, buff=0.4)

        # Arrows
        arrow1 = Arrow(
            start=trash_in.get_right(),
            end=llm_icon.get_left(),
            buff=0.2,
            stroke_width=3,
            color=WHITE
        )
        arrow2 = Arrow(
            start=llm_icon.get_right(),
            end=trash_out.get_left(),
            buff=0.2,
            stroke_width=3,
            color=WHITE
        )

        # Assemble all parts
        self.play(
            Create(trash_in),
            Write(trash_in_label),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(
            Create(arrow1),
            run_time=0.8
        )
        self.wait(0.3)
        self.play(
            Create(llm_icon),
            Write(llm_label),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(
            Create(arrow2),
            run_time=0.8
        )
        self.wait(0.3)
        self.play(
            Create(trash_out),
            Write(trash_out_label),
            run_time=1.2
        )
        self.wait(0.5)

        # Spin the LLM icon for 3 seconds
        self.play(
            Rotate(
                llm_icon,
                angle=2 * PI * 3,
                about_point=llm_icon.get_center(),
                rate_func=linear,
                run_time=3.0
            ),
            Rotate(
                llm_label,
                angle=2 * PI * 3,
                about_point=llm_label.get_center(),
                rate_func=linear,
                run_time=3.0
            )
        )
        self.wait(1)
