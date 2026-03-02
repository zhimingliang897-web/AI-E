from manim import *

class GenerativeDistribution(Scene):
    def construct(self):
        # Title
        title = Text("Generative Distribution", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # 1. Animated cloud of data points (2D scatter-like approximation)
        np.random.seed(42)
        points = []
        for _ in range(150):
            x = np.random.normal(0, 1.2)
            y = np.random.normal(0, 0.8) + 0.3 * x**2  # slight parabolic clustering
            points.append(Dot(point=[x, y, 0], radius=0.04, color=BLUE_E).set_z_index(2))
        cloud = VGroup(*points)
        self.play(FadeIn(cloud, scale=0.8), run_time=2)
        self.wait(0.5)

        # 2. Transform into smooth density surface (approximated with colored filled area + contour)
        # Use a stylized "density hill" — a filled curved shape with gradient-like shading via layered polygons
        density_curve = FunctionGraph(
            lambda x: 1.2 * np.exp(-x**2 / 2) * (1 + 0.3 * np.cos(2*x)),
            x_range=[-3, 3],
            color=TEAL_A,
            stroke_width=0
        )
        density_fill = Polygon(
            [-3, 0, 0],
            *[[x, y, 0] for x, y in zip(density_curve.x_values, density_curve.y_values)],
            [3, 0, 0],
            fill_opacity=0.7,
            fill_color=TEAL_C,
            stroke_width=0
        )
        density_outline = density_curve.copy().set_color(TEAL_E).set_stroke(width=2)

        self.play(
            ReplacementTransform(cloud, VGroup(density_fill, density_outline)),
            run_time=2.5,
            rate_func=smooth
        )
        self.wait(0.5)

        # 3. A new point emerges from the peak
        peak_x = 0
        peak_y = density_curve.underlying_function(peak_x)
        emergence_point = Dot(point=[peak_x, peak_y, 0], radius=0.08, color=YELLOW).set_z_index(3)
        self.play(FadeIn(emergence_point, scale=1.5), run_time=1.2)
        self.wait(0.3)

        # 4. Blossom animation: three labeled artifacts appear around the point
        # Icons as simple geometric approximations:
        # — Image: small rectangle with diagonal slash (stylized)
        image_icon = VGroup(
            Rectangle(height=0.6, width=0.8, fill_opacity=0.2, fill_color=GREY_C, stroke_color=GREY_C),
            Line([-0.3, 0.2, 0], [0.3, -0.2, 0], stroke_color=RED, stroke_width=3),
            Line([-0.3, -0.2, 0], [0.3, 0.2, 0], stroke_color=RED, stroke_width=3)
        ).scale(0.5).next_to(emergence_point, UR, buff=0.8)

        # — Text snippet: "Hello world"
        text_icon = Text("Hello world", font_size=18, font="Monospace").next_to(emergence_point, RIGHT, buff=1.2)

        # — Audio waveform: simple oscillating line
        waveform_points = [
            [0, 0, 0],
            [0.1, 0.15, 0], [0.2, -0.1, 0], [0.3, 0.2, 0],
            [0.4, -0.05, 0], [0.5, 0.1, 0]
        ]
        audio_icon = VGroup(*[
            Line(waveform_points[i], waveform_points[i+1], stroke_color=PURPLE, stroke_width=2)
            for i in range(len(waveform_points)-1)
        ]).next_to(emergence_point, DR, buff=0.8)

        # Labels
        labels = VGroup(
            Text("IMAGE", font_size=16, color=GREY_C).next_to(image_icon, UP, buff=0.3),
            Text("TEXT", font_size=16, color=GREY_C).next_to(text_icon, UP, buff=0.3),
            Text("AUDIO", font_size=16, color=GREY_C).next_to(audio_icon, UP, buff=0.3),
        )

        # 'NEW' badge above center
        new_label = Text("NEW", font_size=24, weight=BOLD, color=YELLOW).next_to(emergence_point, UP, buff=0.5)
        new_label.save_state()
        new_label.scale(0.01).move_to(emergence_point.get_center())

        # Animate blossom: scale up icons + label
        self.play(
            emergence_point.animate.scale(1.8).set_color(YELLOW_E),
            FadeIn(new_label, scale=4),
            FadeIn(image_icon, shift=UP*0.3),
            FadeIn(text_icon, shift=RIGHT*0.3),
            FadeIn(audio_icon, shift=DOWN*0.3),
            FadeIn(labels),
            run_time=2.2,
            rate_func=smooth
        )
        self.wait(0.5)

        # Emphasize 'NEW' with pulse
        self.play(
            new_label.animate.scale(1.3).set_color(GOLD),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(0.5)

        # Final subtle zoom & fade
        self.play(
            VGroup(density_fill, density_outline, emergence_point, new_label, image_icon, text_icon, audio_icon, labels).animate.scale(1.05).shift(DOWN*0.1),
            run_time=1.5
        )
        self.wait(1)
