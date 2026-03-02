from manim import *

class ProbabilityBarChart(Scene):
    def construct(self):
        # Title input text
        input_text = Text("我爱", font_size=36, color=WHITE)
        input_text.to_edge(UP, buff=0.5)

        # Bar chart setup
        bar_width = 1.2
        bar_gap = 1.8
        max_height = 5.0

        # '你' bar: 99% → height = 0.99 * max_height
        you_height = 0.99 * max_height
        you_bar = Rectangle(
            width=bar_width,
            height=you_height,
            fill_color=GREEN,
            fill_opacity=0.8,
            stroke_color=GREEN_E,
            stroke_width=2
        )
        you_bar.set_z_index(2)
        you_bar.shift(DOWN * (max_height - you_height) / 2)

        # '吃' bar: 0.1% → height = 0.001 * max_height = 0.005
        chi_height = 0.001 * max_height
        chi_bar = Rectangle(
            width=bar_width,
            height=chi_height,
            fill_color=GREY_C,
            fill_opacity=0.7,
            stroke_color=GREY,
            stroke_width=1.5
        )
        chi_bar.set_z_index(2)
        chi_bar.shift(DOWN * (max_height - chi_height) / 2)

        # Position bars side by side
        you_bar.shift(LEFT * bar_gap / 2)
        chi_bar.shift(RIGHT * bar_gap / 2)

        # Labels under bars
        you_label = Text("你", font_size=28, color=GREEN).next_to(you_bar, DOWN, buff=0.3)
        chi_label = Text("吃", font_size=28, color=GREY_C).next_to(chi_bar, DOWN, buff=0.3)

        # Percentage labels on top of bars
        you_pct = Text("99%", font_size=24, color=GREEN).next_to(you_bar, UP, buff=0.2)
        chi_pct = Text("0.1%", font_size=24, color=GREY_C).next_to(chi_bar, UP, buff=0.2)

        # Group all bar elements
        bars_group = VGroup(you_bar, chi_bar, you_label, chi_label, you_pct, chi_pct)

        # Add input text and bars
        self.play(Write(input_text), run_time=1.2)
        self.wait(0.5)
        self.play(DrawBorderThenFill(you_bar), DrawBorderThenFill(chi_bar), run_time=1.5)
        self.play(Write(you_label), Write(chi_label), Write(you_pct), Write(chi_pct), run_time=1.2)
        self.wait(0.8)

        # Spark animation: small glowing circles at bar tops
        sparks = VGroup()
        for bar in [you_bar, chi_bar]:
            for _ in range(6):
                spark = Circle(
                    radius=0.06,
                    fill_color=YELLOW,
                    fill_opacity=0.9,
                    stroke_color=ORANGE,
                    stroke_width=1.5
                )
                spark.move_to(bar.get_top() + UP * 0.1 + (np.random.random(3) - 0.5) * 0.3)
                sparks.add(spark)

        # Animate sparks with fade-in + slight scale & opacity pulse
        self.play(
            LaggedStart(
                *[FadeIn(spark, scale=0.5) for spark in sparks],
                lag_ratio=0.05
            ),
            run_time=1.2
        )
        self.play(
            sparks.animate.scale(1.3).set_opacity(0.6),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(0.5)

        # Optional subtle upward wiggle to emphasize "tall vs tiny"
        self.play(
            you_bar.animate.shift(UP * 0.05).set_height(you_height * 1.02),
            chi_bar.animate.shift(UP * 0.01).set_height(chi_height * 1.1),
            run_time=0.8,
            rate_func=smooth
        )

        self.wait(1.5)
