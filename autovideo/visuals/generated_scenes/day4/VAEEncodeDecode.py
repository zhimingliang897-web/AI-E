from manim import *

class VAEEncodeDecode(Scene):
    def construct(self):
        # Title
        title = Text("VAE: Variational Autoencoder", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Input image (simplified as a stylized "image" icon)
        input_img = VGroup(
            Rectangle(width=2.0, height=1.5, color=BLUE, fill_opacity=0.1, stroke_width=2),
            Line([-0.8, 0.4, 0], [0.8, 0.4, 0], color=BLUE, stroke_width=1.5),
            Circle(radius=0.15, color=TEAL_A, fill_opacity=0.7).move_to([-0.5, -0.2, 0]),
            Circle(radius=0.15, color=YELLOW, fill_opacity=0.7).move_to([0.5, -0.2, 0]),
            Arc(start_angle=0, angle=PI, radius=0.3, color=RED, stroke_width=1.5).move_to([0, 0.1, 0])
        ).shift(LEFT * 4.5)

        input_label = Text("Input Image", font_size=24).next_to(input_img, DOWN, buff=0.3)

        # Encoder block
        encoder = RoundedRectangle(height=1.2, width=2.0, corner_radius=0.2, color=GREEN, fill_opacity=0.15, stroke_width=2)
        encoder_text = Text("Encoder", font_size=24, weight=BOLD).move_to(encoder.get_center())

        # Latent space (2D scatter plot region)
        latent_bg = RoundedRectangle(height=2.4, width=3.0, corner_radius=0.2, color=GREY_C, fill_opacity=0.05, stroke_width=1.5)
        latent_label = Text("Latent Space\nz ∈ ℝ²", font_size=22).move_to(latent_bg.get_center() + UP * 1.0)

        # Sample dots in latent space (Gaussian-like cloud)
        np.random.seed(42)
        dots = VGroup(*[
            Dot(point=[-1.0 + 0.6 * np.random.randn(), -0.8 + 0.5 * np.random.randn(), 0],
                radius=0.04, color=BLUE_E)
            for _ in range(40)
        ])

        # Highlight one sampled point
        sample_dot = Dot(point=[-0.2, 0.3, 0], radius=0.07, color=PURPLE, stroke_width=2, stroke_color=WHITE)
        sample_label = Text("z ~ q(z|x)", font_size=20, color=PURPLE).next_to(sample_dot, UR, buff=0.2)

        # Decoder block
        decoder = RoundedRectangle(height=1.2, width=2.0, corner_radius=0.2, color=ORANGE, fill_opacity=0.15, stroke_width=2)
        decoder_text = Text("Decoder", font_size=24, weight=BOLD).move_to(decoder.get_center())

        # Output image (reconstruction)
        output_img = VGroup(
            Rectangle(width=2.0, height=1.5, color=RED, fill_opacity=0.1, stroke_width=2),
            Line([-0.8, 0.4, 0], [0.8, 0.4, 0], color=RED, stroke_width=1.5),
            Circle(radius=0.15, color=TEAL_A, fill_opacity=0.5).move_to([-0.45, -0.2, 0]),
            Circle(radius=0.15, color=YELLOW, fill_opacity=0.5).move_to([0.45, -0.2, 0]),
            Arc(start_angle=0, angle=PI, radius=0.3, color=RED, stroke_width=1.5).move_to([0, 0.1, 0])
        ).shift(RIGHT * 4.5)

        output_label = Text("Reconstruction", font_size=24).next_to(output_img, DOWN, buff=0.3)

        # Arrows
        arrow1 = Arrow(input_img.get_right(), encoder.get_left(), buff=0.2, stroke_width=2)
        arrow2 = Arrow(encoder.get_right(), latent_bg.get_left() + RIGHT * 0.5, buff=0.2, stroke_width=2)
        arrow3 = Arrow(latent_bg.get_right() - RIGHT * 0.5, decoder.get_left(), buff=0.2, stroke_width=2)
        arrow4 = Arrow(decoder.get_right(), output_img.get_left(), buff=0.2, stroke_width=2)

        # Dotted line for reconstruction loss (curved upward from input to output)
        loss_line = DashedLine(
            start=input_img.get_bottom() + DOWN * 0.3,
            end=output_img.get_bottom() + DOWN * 0.3,
            dash_length=0.15,
            positive_space_ratio=0.5,
            color=PURPLE_E,
            stroke_width=2
        )
        loss_label = Text("ℒ_recon = ||x − x̂||²", font_size=22, color=PURPLE_E).next_to(loss_line, DOWN, buff=0.2)

        # Positioning
        input_img.shift(LEFT * 4.5)
        encoder.shift(LEFT * 1.5)
        latent_bg.shift(ORIGIN)
        decoder.shift(RIGHT * 1.5)
        output_img.shift(RIGHT * 4.5)

        # Build scene step-by-step
        self.play(FadeIn(input_img), Write(input_label))
        self.wait(0.5)
        self.play(Create(arrow1), Create(encoder), Write(encoder_text))
        self.wait(0.5)
        self.play(Create(arrow2), FadeIn(latent_bg), Write(latent_label))
        self.wait(0.5)
        self.play(LaggedStart(*[FadeIn(dot) for dot in dots], lag_ratio=0.02))
        self.wait(0.5)
        self.play(FadeIn(sample_dot), Write(sample_label))
        self.wait(0.5)
        self.play(Create(arrow3), Create(decoder), Write(decoder_text))
        self.wait(0.5)
        self.play(Create(arrow4), FadeIn(output_img), Write(output_label))
        self.wait(0.5)
        self.play(Create(loss_line), Write(loss_label))
        self.wait(1)

        # Emphasize sampling and reconstruction flow
        self.play(
            sample_dot.animate.scale(1.5).set_color(YELLOW).set_stroke(WHITE, width=3),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(0.5)

        # Animate reconstruction improvement (subtle morph of output to match input)
        self.play(
            output_img[0].animate.set_fill(BLUE, opacity=0.2),
            output_img[2].animate.set_fill(TEAL_A, opacity=0.7),
            output_img[3].animate.set_fill(YELLOW, opacity=0.7),
            output_img[4].animate.set_color(BLUE),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)

        # Final caption
        final_caption = Text("Minimize reconstruction loss + KL divergence", font_size=26, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Write(final_caption))
        self.wait(2)
