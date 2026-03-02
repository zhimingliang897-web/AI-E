from manim import *

class NextTokenPrediction(Scene):
    def construct(self):
        # Background elements
        title = Text("Next-Token Prediction", font_size=36, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Input box: "我爱"
        input_label = Text("Input:", font_size=24).shift(UP * 2 + LEFT * 3.5)
        input_box = RoundedRectangle(corner_radius=0.2, height=1.2, width=3.0, stroke_color=GREY_C, stroke_width=2, fill_color=BLACK, fill_opacity=0.7)
        input_text = Text("我爱", font="Microsoft YaHei", font_size=32, color=WHITE).move_to(input_box.get_center())
        input_group = VGroup(input_label, input_box, input_text)

        # Output box (initially dimmed)
        output_label = Text("Output:", font_size=24).shift(UP * 2 + RIGHT * 3.5)
        output_box = RoundedRectangle(corner_radius=0.2, height=1.2, width=3.0, stroke_color=GREY_C, stroke_width=2, fill_color=BLACK, fill_opacity=0.7)
        output_text = Text("?", font="Microsoft YaHei", font_size=32, color=GREY_C).move_to(output_box.get_center())
        output_prob = Text("??%", font_size=24, color=GREY_C).next_to(output_box, DOWN, buff=0.2)
        output_group = VGroup(output_label, output_box, output_text, output_prob)

        self.play(FadeIn(input_group), FadeIn(output_group))
        self.wait(0.5)

        # Animated gears — two interlocking cartoon-style gears
        # Gear 1 (left)
        gear1 = VGroup()
        for i in range(12):
            angle = i * TAU / 12
            tooth = Rectangle(height=0.4, width=0.12, fill_color=TEAL_A, fill_opacity=1, stroke_width=0).rotate(angle).move_to(
                Circle(radius=0.8).point_at_angle(angle)
            )
            gear1.add(tooth)
        gear1.add(Circle(radius=0.3, color=TEAL_A, fill_color=TEAL_A, fill_opacity=1, stroke_width=0))
        gear1.move_to(ORIGIN)

        # Gear 2 (right, slightly larger, offset to interlock)
        gear2 = VGroup()
        for i in range(12):
            angle = i * TAU / 12 + PI/12
            tooth = Rectangle(height=0.45, width=0.14, fill_color=PURPLE_A, fill_opacity=1, stroke_width=0).rotate(angle).move_to(
                Circle(radius=1.0).point_at_angle(angle)
            )
            gear2.add(tooth)
        gear2.add(Circle(radius=0.35, color=PURPLE_A, fill_color=PURPLE_A, fill_opacity=1, stroke_width=0))
        gear2.move_to(RIGHT * 1.8)

        # Position gears between input and output
        gear1.shift(LEFT * 0.8)
        gear2.shift(RIGHT * 0.8)
        gears = VGroup(gear1, gear2)

        self.play(FadeIn(gears), run_time=0.8)
        self.wait(0.3)

        # Spin gears clockwise (gear1) and counter-clockwise (gear2) for 2 seconds
        self.play(
            Rotate(gear1, angle=TAU * 1.5, about_point=gear1.get_center(), rate_func=linear),
            Rotate(gear2, angle=-TAU * 1.5, about_point=gear2.get_center(), rate_func=linear),
            run_time=2.0
        )

        # Highlight gears with pulse + subtle glow
        gear1_copy = gear1.copy().set_stroke(YELLOW, width=3).set_fill(opacity=0.3)
        gear2_copy = gear2.copy().set_stroke(YELLOW, width=3).set_fill(opacity=0.3)
        self.play(
            FadeIn(gear1_copy), FadeIn(gear2_copy),
            output_box.animate.set_stroke(YELLOW, width=3),
            output_text.animate.set_color(YELLOW),
            output_prob.animate.set_color(YELLOW),
            run_time=0.6
        )
        self.play(
            FadeOut(gear1_copy), FadeOut(gear2_copy),
            run_time=0.4
        )

        # Reveal final output: "你" + "99%"
        self.play(
            Transform(output_text, Text("你", font="Microsoft YaHei", font_size=32, color=WHITE).move_to(output_box.get_center())),
            Transform(output_prob, Text("99%", font_size=24, color=GREEN).next_to(output_box, DOWN, buff=0.2)),
            output_box.animate.set_stroke(GREEN, width=3),
            run_time=0.8
        )

        # Optional: subtle upward pulse on output box
        self.play(
            output_box.animate.scale(1.03).set_stroke(GREEN, width=4),
            output_text.animate.scale(1.05),
            output_prob.animate.scale(1.1),
            run_time=0.3
        )
        self.play(
            output_box.animate.scale(1/1.03).set_stroke(GREEN, width=3),
            output_text.animate.scale(1/1.05),
            output_prob.animate.scale(1/1.1),
            run_time=0.3
        )

        self.wait(1.5)
