from manim import *

class PhysicsVsLMAnalogy(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Split screen: left and right sections
        left_rect = Rectangle(height=6, width=6, color=GREY_C, stroke_width=1).to_edge(LEFT, buff=0.5)
        right_rect = Rectangle(height=6, width=6, color=GREY_C, stroke_width=1).to_edge(RIGHT, buff=0.5)

        # Labels
        title = Text("Physics vs Language Modeling", font="Microsoft YaHei", weight=BOLD, font_size=32)
        title.to_edge(UP, buff=0.5)

        # Left side: Physics — parabola trajectory
        left_title = Text("Physics", font="Microsoft YaHei", font_size=24).next_to(left_rect, UP, buff=0.2)
        physics_label = Text("y = ax² + bx + c", font_size=28).next_to(left_rect, DOWN, buff=0.3)

        # Axes for parabola
        axes_left = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-0.5, 4.5, 1],
            axis_config={"color": GREY_C, "stroke_width": 1},
            x_length=5,
            y_length=4,
        ).move_to(left_rect.get_center())

        # Parabola (e.g., y = -x² + 3)
        parabola = axes_left.plot(lambda x: -x**2 + 3, x_range=[-2, 2], color=BLUE, stroke_width=3)

        # Trajectory dots with arrow
        points = [axes_left.c2p(x, -x**2 + 3) for x in [-2, -1, 0, 1, 2]]
        traj_dots = VGroup(*[Dot(p, color=BLUE, radius=0.07) for p in points])
        traj_arrow = Arrow(points[0], points[-1], buff=0, color=BLUE, stroke_width=2, tip_length=0.15)

        # Right side: Language modeling — word sequence with probability bars
        right_title = Text("Language Modeling", font="Microsoft YaHei", font_size=24).next_to(right_rect, UP, buff=0.2)
        lm_label = Text("modeling reality", font_size=24).next_to(right_rect, DOWN, buff=0.3)

        # Word sequence: "今天 → 天气 → 很 → 好"
        words = ["今天", "天气", "很", "好"]
        word_texts = VGroup(*[
            Text(word, font="Microsoft YaHei", font_size=28, weight=BOLD) for word in words
        ]).arrange(RIGHT, buff=1.2).move_to(right_rect.get_center() + UP * 1.0)

        # Arrows between words
        arrows = VGroup(*[
            Arrow(word_texts[i].get_right(), word_texts[i+1].get_left(), buff=0.1, stroke_width=2, color=YELLOW, tip_length=0.1)
            for i in range(len(words)-1)
        ])

        # Probability bars (rising heights: 0.3 → 0.5 → 0.7 → 0.9)
        bar_heights = [0.3, 0.5, 0.7, 0.9]
        bars = VGroup()
        bar_labels = VGroup()
        for i, h in enumerate(bar_heights):
            bar = Rectangle(width=0.4, height=h*2.5, fill_color=TEAL_A, fill_opacity=0.8, stroke_width=1)
            bar.next_to(word_texts[i], DOWN, buff=0.5)
            label = Text(f"{int(h*100)}%", font_size=18).next_to(bar, DOWN, buff=0.1)
            bars.add(bar)
            bar_labels.add(label)

        # Common label "modeling reality" centered below both sides
        common_label = Text("modeling reality", font="Microsoft YaHei", font_size=28, weight=BOLD, color=PURPLE_E)
        common_label.next_to(VGroup(left_rect, right_rect), DOWN, buff=0.7)

        # Animation sequence
        self.play(
            Create(left_rect),
            Create(right_rect),
            Write(title),
            Write(left_title),
            Write(right_title),
        )
        self.wait(0.5)

        # Left: draw axes & parabola
        self.play(
            Create(axes_left),
            Create(parabola),
            run_time=2,
            rate_func=smooth
        )
        self.play(
            LaggedStart(*[FadeIn(dot) for dot in traj_dots], lag_ratio=0.3),
            Create(traj_arrow),
            Write(physics_label),
        )
        self.wait(0.5)

        # Right: reveal words and arrows
        self.play(
            LaggedStart(*[Write(w) for w in word_texts], lag_ratio=0.4),
            LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.4),
        )
        self.wait(0.5)

        # Right: grow bars with labels
        self.play(
            LaggedStart(*[GrowFromCenter(bar) for bar in bars], lag_ratio=0.4),
            LaggedStart(*[FadeIn(label) for label in bar_labels], lag_ratio=0.4),
            Write(lm_label),
        )
        self.wait(0.5)

        # Emphasize common theme
        self.play(FadeIn(common_label))
        self.wait(1.5)

        # Final zoom & hold
        self.play(
            left_rect.animate.set_stroke(BLUE, width=3),
            right_rect.animate.set_stroke(TEAL_A, width=3),
            common_label.animate.set_color(YELLOW).scale(1.1),
            run_time=1.5
        )
        self.wait(2)
