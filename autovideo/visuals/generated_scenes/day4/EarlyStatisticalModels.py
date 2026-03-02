from manim import *

class EarlyStatisticalModels(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Title
        title = Text("Early Statistical Models", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Timeline line
        timeline = Line(LEFT * 6, RIGHT * 6, stroke_width=2, color=GREY_C)
        timeline.shift(DOWN * 2)
        self.play(Create(timeline))

        # Year markers
        year_1965 = Text("1965", font_size=24).next_to(LEFT * 6, DOWN, buff=0.5)
        year_1970 = Text("1970", font_size=24).next_to(RIGHT * 6, DOWN, buff=0.5)
        self.play(FadeIn(year_1965), FadeIn(year_1970))

        # Arrow from 1965 to 1970
        timeline_arrow = Arrow(LEFT * 6, RIGHT * 6, buff=0, stroke_width=3, color=YELLOW)
        self.play(GrowArrow(timeline_arrow))

        # --- 1965: HMM Icon ---
        # Hidden states (3 circles in a row)
        h1 = Circle(radius=0.3, color=BLUE, fill_opacity=0.2).shift(LEFT * 4 + UP * 1)
        h2 = Circle(radius=0.3, color=BLUE, fill_opacity=0.2).shift(LEFT * 2 + UP * 1)
        h3 = Circle(radius=0.3, color=BLUE, fill_opacity=0.2).shift(RIGHT * 0 + UP * 1)
        hidden_states = VGroup(h1, h2, h3)
        
        # Speech waveform (simplified zigzag line)
        waveform_points = [
            [h1.get_right()[0], h1.get_top()[1] - 0.5, 0],
            [h1.get_right()[0] + 0.3, h1.get_top()[1] - 0.3, 0],
            [h1.get_right()[0] + 0.6, h1.get_top()[1] - 0.5, 0],
            [h1.get_right()[0] + 0.9, h1.get_top()[1] - 0.2, 0],
            [h2.get_right()[0] + 0.1, h2.get_top()[1] - 0.4, 0],
            [h2.get_right()[0] + 0.4, h2.get_top()[1] - 0.1, 0],
            [h2.get_right()[0] + 0.7, h2.get_top()[1] - 0.3, 0],
            [h3.get_right()[0] + 0.1, h3.get_top()[1] - 0.2, 0],
            [h3.get_right()[0] + 0.4, h3.get_top()[1] - 0.4, 0],
        ]
        waveform = Polyline(*waveform_points, stroke_width=2, color=TEAL_A)

        # Arrows from hidden states to waveform points
        arrows_hmm = VGroup()
        for h in [h1, h2, h3]:
            arrow = Arrow(
                h.get_bottom(),
                [h.get_x(), h.get_y() - 0.8, 0],
                stroke_width=1.5,
                color=TEAL_A
            )
            arrows_hmm.add(arrow)

        hmm_label = Text("HMM", font_size=20, color=BLUE).next_to(h2, UP, buff=0.3)

        # Group HMM icon
        hmm_icon = VGroup(hidden_states, waveform, arrows_hmm, hmm_label)
        hmm_icon.shift(DOWN * 0.5)

        # Animate 1965 HMM
        self.play(
            Create(hidden_states),
            Write(hmm_label),
            run_time=1.2
        )
        self.wait(0.3)
        self.play(
            Create(waveform),
            Create(arrows_hmm),
            run_time=1.5
        )
        self.wait(0.5)

        # --- 1970: GMM Icon ---
        # Three Gaussian blobs (ellipses with fading opacity)
        g1 = Ellipse(width=1.2, height=0.6, color=RED, fill_opacity=0.2).shift(LEFT * 3 + DOWN * 1.5)
        g2 = Ellipse(width=1.0, height=0.8, color=GREEN, fill_opacity=0.2).shift(UP * 0.2 + DOWN * 1.5)
        g3 = Ellipse(width=0.9, height=0.7, color=PURPLE, fill_opacity=0.2).shift(RIGHT * 3 + DOWN * 1.5)
        gmm_blobs = VGroup(g1, g2, g3)

        # Scatter points around each blob (small dots)
        np.random.seed(42)
        points = VGroup()
        for center, width, height, color in [
            (g1.get_center(), 1.2, 0.6, RED),
            (g2.get_center(), 1.0, 0.8, GREEN),
            (g3.get_center(), 0.9, 0.7, PURPLE),
        ]:
            for _ in range(12):
                dx = (np.random.random() - 0.5) * width
                dy = (np.random.random() - 0.5) * height * 0.7
                pt = Dot(center + [dx, dy, 0], radius=0.04, color=color)
                points.add(pt)

        gmm_label = Text("GMM", font_size=20, color=RED).next_to(g2, DOWN, buff=0.5)

        # Group GMM icon
        gmm_icon = VGroup(gmm_blobs, points, gmm_label)
        gmm_icon.shift(DOWN * 0.5)

        # Animate 1970 GMM
        self.play(
            Create(gmm_blobs),
            Write(gmm_label),
            run_time=1.2
        )
        self.wait(0.3)
        self.play(
            LaggedStartMap(FadeIn, points, lag_ratio=0.05),
            run_time=1.5
        )
        self.wait(0.5)

        # --- Labels: "Voice & Sequence" ---
        label_voice_seq = Text("Voice & Sequence", font_size=28, weight=BOLD)
        label_voice_seq.next_to(timeline, UP, buff=1.0)
        self.play(FadeIn(label_voice_seq))
        self.wait(0.5)

        # Highlight both icons with glow effect
        hmm_glow = hidden_states.copy().set_stroke(BLUE, width=4, opacity=0.5).set_fill(opacity=0)
        gmm_glow = gmm_blobs.copy().set_stroke(RED, width=4, opacity=0.5).set_fill(opacity=0)
        self.play(
            Create(hmm_glow),
            Create(gmm_glow),
            run_time=1.0
        )
        self.wait(0.5)
        self.play(
            FadeOut(hmm_glow),
            FadeOut(gmm_glow)
        )

        # Final pause
        self.wait(1.5)
