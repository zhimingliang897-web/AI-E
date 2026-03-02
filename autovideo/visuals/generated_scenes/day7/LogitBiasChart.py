from manim import *

class LogitBiasChart(Scene):
    def construct(self):
        # Axes
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 120, 20],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True, "color": GREY_C},
            y_axis_config={"include_ticks": True},
        )
        axes_labels = axes.get_axis_labels(
            x_label=Text("Tokens", font_size=24),
            y_label=Text("Logit Score", font_size=24)
        )

        # Token labels (x-axis positions)
        token_labels = [
            ("。", 0.5),   # illegal: Chinese period
            ("（", 1.5),   # illegal: Chinese left paren
            ("a", 2.5),    # illegal: alphabetic
            ("{", 3.5),    # legal: JSON start object
            ('"', 4.5),    # legal: JSON string quote
            ("0", 5.5),    # legal: digit
            ("9", 6.5),    # legal: digit
            ("}", 7.5),    # legal: JSON end object
        ]

        # Heights: illegal tokens at 0; legal tokens high (80–110)
        heights = [0, 0, 0, 100, 95, 85, 85, 90]

        # Bars
        bars = VGroup()
        bar_colors = []
        for i, (token, x_pos) in enumerate(token_labels):
            height = heights[i]
            color = RED if height == 0 else GREEN
            bar_colors.append(color)
            bar = Rectangle(
                width=0.6,
                height=height * 0.05,  # scale to fit axes
                fill_color=color,
                fill_opacity=0.8,
                stroke_width=0
            )
            bar.move_to(axes.c2p(x_pos, height / 2))
            bars.add(bar)

        # Token text labels below bars
        token_text = VGroup()
        for i, (token, x_pos) in enumerate(token_labels):
            txt = Text(token, font_size=28).move_to(axes.c2p(x_pos, -5))
            token_text.add(txt)

        # Title
        title = Text("Logit Bias for JSON Generation", font_size=32, weight=BOLD).to_edge(UP, buff=0.5)

        # Animate
        self.play(Create(axes), Write(axes_labels), Write(title))
        self.wait(0.5)
        self.play(Write(token_text))
        self.wait(0.5)
        self.play(LaggedStart(*[Create(bar) for bar in bars], lag_ratio=0.2))
        self.wait(1)

        # Add legend
        illegal_leg = VGroup(
            Rectangle(width=0.4, height=0.4, fill_color=RED, fill_opacity=0.8, stroke_width=0),
            Text("Illegal", font_size=20).next_to(Rectangle(width=0.4, height=0.4), RIGHT, buff=0.2)
        ).to_edge(DOWN, buff=0.5).shift(LEFT * 3)

        legal_leg = VGroup(
            Rectangle(width=0.4, height=0.4, fill_color=GREEN, fill_opacity=0.8, stroke_width=0),
            Text("Legal JSON", font_size=20).next_to(Rectangle(width=0.4, height=0.4), RIGHT, buff=0.2)
        ).next_to(illegal_leg, RIGHT, buff=1.5)

        self.play(FadeIn(illegal_leg), FadeIn(legal_leg))
        self.wait(2)
