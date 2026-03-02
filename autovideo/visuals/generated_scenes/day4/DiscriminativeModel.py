from manim import *

class DiscriminativeModel(Scene):
    def construct(self):
        # Title
        title = Text("Discriminative Model: P(Y|X)", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Split screen
        divider = Line(UP * 3, DOWN * 3, stroke_width=2, color=GREY_C)
        divider.move_to(ORIGIN)
        left_label = Text("Input X", font_size=24).next_to(divider, LEFT, buff=1.5)
        right_label = Text("Output P(Y|X)", font_size=24).next_to(divider, RIGHT, buff=1.5)

        self.play(Create(divider), Write(left_label), Write(right_label))
        self.wait(0.5)

        # --- LEFT SIDE: Labeled Images ---
        # Image placeholders (simplified as colored rectangles with labels)
        cat_img = RoundedRectangle(height=2.0, width=2.4, corner_radius=0.2, fill_color=TEAL_A, fill_opacity=0.8, stroke_color=TEAL_E)
        cat_label = Text("cat", font_size=20, color=WHITE).move_to(cat_img.get_center())
        cat_group = VGroup(cat_img, cat_label).move_to(LEFT * 4.5 + UP * 1.2)

        dog_img = RoundedRectangle(height=2.0, width=2.4, corner_radius=0.2, fill_color=PURPLE_A, fill_opacity=0.8, stroke_color=PURPLE_E)
        dog_label = Text("dog", font_size=20, color=WHITE).move_to(dog_img.get_center())
        dog_group = VGroup(dog_img, dog_label).move_to(LEFT * 4.5 + DOWN * 0.2)

        car_img = RoundedRectangle(height=2.0, width=2.4, corner_radius=0.2, fill_color=YELLOW, fill_opacity=0.7, stroke_color=GOLD)
        car_label = Text("car", font_size=20, color=BLACK).move_to(car_img.get_center())
        car_group = VGroup(car_img, car_label).move_to(LEFT * 4.5 + DOWN * 1.6)

        # Arrows from images to labels (will point to right-side chart later)
        arrow_cat = Arrow(cat_group.get_right(), RIGHT * 2.5 + UP * 1.2, buff=0.1, stroke_width=2)
        arrow_dog = Arrow(dog_group.get_right(), RIGHT * 2.5 + DOWN * 0.2, buff=0.1, stroke_width=2)
        arrow_car = Arrow(car_group.get_right(), RIGHT * 2.5 + DOWN * 1.6, buff=0.1, stroke_width=2)

        self.play(
            FadeIn(cat_group),
            FadeIn(dog_group),
            FadeIn(car_group),
            Create(arrow_cat),
            Create(arrow_dog),
            Create(arrow_car)
        )
        self.wait(0.5)

        # --- RIGHT SIDE: Probability Bar Chart ---
        # Axes
        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[0, 1.0, 0.2],
            x_length=5,
            y_length=4,
            axis_config={"include_numbers": False, "stroke_width": 1},
            y_axis_config={"include_ticks": True}
        ).move_to(RIGHT * 3.5)

        y_labels = VGroup(
            Text("cat", font_size=16).next_to(axes.c2p(0, 0), DOWN, buff=0.25),
            Text("dog", font_size=16).next_to(axes.c2p(1, 0), DOWN, buff=0.25),
            Text("car", font_size=16).next_to(axes.c2p(2, 0), DOWN, buff=0.25),
        )

        # Initial bar heights (for 'cat' input)
        bars_init = VGroup(
            Rectangle(width=0.6, height=2.4, fill_color=TEAL_A, fill_opacity=0.9, stroke_width=0),
            Rectangle(width=0.6, height=0.4, fill_color=PURPLE_A, fill_opacity=0.7, stroke_width=0),
            Rectangle(width=0.6, height=0.2, fill_color=YELLOW, fill_opacity=0.7, stroke_width=0),
        )
        bars_init.arrange(RIGHT, buff=0.3).move_to(axes.c2p(0.5, 0))

        # Add bars to axes
        bars_group = VGroup()
        for i, bar in enumerate(bars_init):
            bar.move_to(axes.c2p(i, 0) + UP * (bar.height / 2))
            bars_group.add(bar)

        # Y-axis ticks and labels
        y_ticks = VGroup()
        for y in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
            tick = Line(LEFT * 0.1, RIGHT * 0.1, stroke_width=1).move_to(axes.c2p(0, y))
            y_ticks.add(tick)

        # Labels for y-axis
        y_num_labels = VGroup(
            Text("0.0", font_size=14).next_to(axes.c2p(-0.2, 0.0), LEFT, buff=0.1),
            Text("0.2", font_size=14).next_to(axes.c2p(-0.2, 0.2), LEFT, buff=0.1),
            Text("0.4", font_size=14).next_to(axes.c2p(-0.2, 0.4), LEFT, buff=0.1),
            Text("0.6", font_size=14).next_to(axes.c2p(-0.2, 0.6), LEFT, buff=0.1),
            Text("0.8", font_size=14).next_to(axes.c2p(-0.2, 0.8), LEFT, buff=0.1),
            Text("1.0", font_size=14).next_to(axes.c2p(-0.2, 1.0), LEFT, buff=0.1),
        )

        self.play(
            Create(axes),
            FadeIn(y_ticks),
            FadeIn(y_num_labels),
            FadeIn(y_labels),
            FadeIn(bars_group)
        )
        self.wait(0.5)

        # Animate transition: cat → dog → car
        # Define bar heights for each class (normalized to max 1.0 → height 4.0 in axes units)
        cat_probs = [0.85, 0.10, 0.05]  # P(cat|cat), P(dog|cat), P(car|cat)
        dog_probs = [0.15, 0.75, 0.10]  # P(cat|dog), P(dog|dog), P(car|dog)
        car_probs = [0.05, 0.15, 0.80]  # P(cat|car), P(dog|car), P(car|car)

        # Helper to create new bars
        def make_bars(probs, colors=[TEAL_A, PURPLE_A, YELLOW]):
            b = VGroup()
            for i, p in enumerate(probs):
                h = p * 4.0  # scale to axes y-range (0–1 → 0–4)
                bar = Rectangle(
                    width=0.6, height=h,
                    fill_color=colors[i], fill_opacity=0.9 if i == 0 else 0.7,
                    stroke_width=0
                )
                bar.move_to(axes.c2p(i, 0) + UP * (h / 2))
                b.add(bar)
            return b

        # Animate cat → dog
        bars_dog = make_bars(dog_probs)
        self.play(
            Transform(bars_group, bars_dog),
            cat_group.animate.set_opacity(0.3),
            dog_group.animate.set_opacity(1.0),
            car_group.animate.set_opacity(0.3),
            run_time=1.2,
            rate_func=smooth
        )
        self.wait(0.8)

        # Animate dog → car
        bars_car = make_bars(car_probs)
        self.play(
            Transform(bars_group, bars_car),
            cat_group.animate.set_opacity(0.3),
            dog_group.animate.set_opacity(0.3),
            car_group.animate.set_opacity(1.0),
            run_time=1.2,
            rate_func=smooth
        )
        self.wait(0.8)

        # Highlight final state: add probability text on bars
        prob_texts = VGroup()
        for i, p in enumerate(car_probs):
            txt = Text(f"{p:.2f}", font_size=16, color=BLACK if i == 2 else WHITE).move_to(bars_car[i].get_top() + UP * 0.15)
            prob_texts.add(txt)
        self.play(FadeIn(prob_texts))
        self.wait(1.5)

        # Final annotation
        note = Text("Discriminative models estimate P(Y|X) directly", font_size=24, color=GREY_C)
        note.to_edge(DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(2)
