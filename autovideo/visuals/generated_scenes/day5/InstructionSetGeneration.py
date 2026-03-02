from manim import *

class InstructionSetGeneration(Scene):
    def construct(self):
        # Background elements
        bg_rect = Rectangle(width=14, height=8, fill_color=GREY_C, fill_opacity=0.1, stroke_width=0)
        bg_rect.set_z_index(-1)

        # Brain icon (simplified stylized brain using ellipses and arcs)
        left_lobe = Ellipse(width=2.0, height=1.6, color=PURPLE_E).shift(LEFT * 0.8 + UP * 0.2)
        right_lobe = Ellipse(width=2.0, height=1.6, color=PURPLE_E).shift(RIGHT * 0.8 + UP * 0.2)
        center_brain = Circle(radius=0.9, color=PURPLE_A, fill_opacity=1).set_fill(PURPLE_A)
        
        # Sulcus-like curves
        top_curve = ArcBetweenPoints(
            left_lobe.get_top() + UP * 0.1,
            right_lobe.get_top() + UP * 0.1,
            angle=-PI/3,
            color=PURPLE,
            stroke_width=2
        )
        bottom_curve = ArcBetweenPoints(
            left_lobe.get_bottom() + DOWN * 0.1,
            right_lobe.get_bottom() + DOWN * 0.1,
            angle=PI/3,
            color=PURPLE,
            stroke_width=2
        )
        
        brain = VGroup(left_lobe, right_lobe, center_brain, top_curve, bottom_curve)
        brain.scale(0.8).to_edge(LEFT, buff=1.5)

        # JSON instruction set (stylized as glowing code block)
        json_text = Text(
            '{\n  "op": "ADD",\n  "a": 5,\n  "b": 3,\n  "dst": "R0"\n}',
            font="Monospace",
            font_size=20,
            color=TEAL_A
        )
        json_bg = RoundedRectangle(corner_radius=0.2, width=5.5, height=3.0, fill_color=GREY_C, fill_opacity=0.3, stroke_color=TEAL_A, stroke_width=1)
        json_group = VGroup(json_bg, json_text).arrange(DOWN, buff=0.2).next_to(brain, RIGHT, buff=1.2)

        # Arrow from brain to JSON
        arrow1 = Arrow(
            brain.get_right(),
            json_group.get_left(),
            buff=0.2,
            color=YELLOW,
            stroke_width=3)

        # Code execution engine (circuit board style: rectangle with dots & lines)
        engine_bg = RoundedRectangle(corner_radius=0.3, width=5.0, height=3.0, fill_color=GREY_C, fill_opacity=0.4, stroke_color=BLUE, stroke_width=2)
        engine_title = Text("EXEC ENGINE", font_size=16, color=BLUE, weight=BOLD).next_to(engine_bg, UP, buff=0.2)

        # Circuit elements
        chip_dots = VGroup(*[
            Dot(point=engine_bg.get_center() + np.array([x, y, 0]), radius=0.05, color=GREEN)
            for x in [-0.8, -0.2, 0.4, 0.9]
            for y in [-0.6, 0.0, 0.5]
        ])
        chip_lines = VGroup(*[
            Line(
                chip_dots[i].get_center(),
                chip_dots[j].get_center(),
                stroke_width=1.2,
                color=BLUE_E
            )
            for i, j in [(0, 4), (4, 8), (2, 7), (1, 5), (3, 6)]
        ])

        engine = VGroup(engine_bg, engine_title, chip_dots, chip_lines).next_to(json_group, RIGHT, buff=1.5)

        # Arrow from JSON to engine
        arrow2 = Arrow(
            json_group.get_right(),
            engine.get_left(),
            buff=0.2,
            color=YELLOW,
            stroke_width=3)

        # Output result display (R0 = 8)
        result = Text("R0 ← 8", font="Monospace", font_size=24, color=GREEN_B)
        result_bg = RoundedRectangle(corner_radius=0.15, width=3.0, height=1.2, fill_color=GREY_C, fill_opacity=0.3, stroke_color=GREEN_B, stroke_width=1)
        result_group = VGroup(result_bg, result).next_to(engine, RIGHT, buff=1.0)

        # Animation sequence
        self.add(bg_rect)
        self.play(FadeIn(brain), run_time=1.2)
        self.wait(0.5)
        self.play(Create(arrow1), FadeIn(json_group), run_time=1.5)
        self.wait(0.5)
        self.play(Create(arrow2), FadeIn(engine), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(result_group), run_time=1.0)
        self.wait(0.5)

        # Highlight flow: pulse brain → pulse JSON → pulse engine → highlight result
        self.play(
            brain.animate.set_stroke(YELLOW, width=3),
            rate_func=smooth,
            run_time=1.2
        )
        self.play(
            json_group.animate.set_stroke(YELLOW, width=2),
            rate_func=smooth,
            run_time=1.2
        )
        self.play(
            engine.animate.set_stroke(YELLOW, width=2),
            rate_func=smooth,
            run_time=1.2
        )
        self.play(
            result_group.animate.set_stroke(GREEN_B, width=3),
            rate_func=smooth,
            run_time=1.2
        )
        self.wait(1)
