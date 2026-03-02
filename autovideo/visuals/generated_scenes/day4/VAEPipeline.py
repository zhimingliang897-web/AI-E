from manim import *

class VAEPipeline(Scene):
    def construct(self):
        # Title
        title = Text("VAE Pipeline", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Define positions
        image_pos = LEFT * 5
        encoder_pos = LEFT * 2
        latent_pos = ORIGIN
        decoder_pos = RIGHT * 2
        recon_pos = RIGHT * 5

        # Input image (simplified as a colored square with grid)
        input_image = Square(side_length=1.2, color=BLUE, fill_opacity=0.2)
        input_grid = VGroup()
        for i in range(3):
            for j in range(3):
                dot = Dot(point=input_image.get_corner(UL) + RIGHT*0.4*j + DOWN*0.4*i, radius=0.03, color=BLUE)
                input_grid.add(dot)
        input_image_group = VGroup(input_image, input_grid).move_to(image_pos)

        # Encoder block
        encoder = RoundedRectangle(height=1.0, width=1.6, corner_radius=0.2, color=TEAL_A, fill_opacity=0.3)
        encoder_text = Text("Encoder", font_size=24).move_to(encoder.get_center())
        encoder_group = VGroup(encoder, encoder_text).move_to(encoder_pos)

        # Latent space: 2D scatter plot (dots)
        latent_dots = VGroup()
        np.random.seed(42)
        for _ in range(30):
            x = np.random.normal(0, 0.8)
            y = np.random.normal(0, 0.8)
            dot = Dot(point=latent_pos + x * RIGHT + y * UP, radius=0.04, color=PURPLE_E)
            latent_dots.add(dot)
        latent_label = Text("2D Latent Space", font_size=20).next_to(latent_dots, UP, buff=0.3)
        latent_group = VGroup(latent_dots, latent_label).move_to(latent_pos)

        # Decoder block
        decoder = RoundedRectangle(height=1.0, width=1.6, corner_radius=0.2, color=GOLD, fill_opacity=0.3)
        decoder_text = Text("Decoder", font_size=24).move_to(decoder.get_center())
        decoder_group = VGroup(decoder, decoder_text).move_to(decoder_pos)

        # Reconstructed image (same style as input)
        recon_image = Square(side_length=1.2, color=GREEN, fill_opacity=0.2)
        recon_grid = VGroup()
        for i in range(3):
            for j in range(3):
                # Slightly perturbed positions to suggest reconstruction imperfection
                px = j * 0.4 + np.random.uniform(-0.05, 0.05)
                py = i * 0.4 + np.random.uniform(-0.05, 0.05)
                dot = Dot(point=recon_image.get_corner(UL) + RIGHT*px + DOWN*py, radius=0.03, color=GREEN)
                recon_grid.add(dot)
        recon_image_group = VGroup(recon_image, recon_grid).move_to(recon_pos)

        # Arrows
        arrow_encode = Arrow(start=input_image_group.get_right(), end=encoder_group.get_left(), buff=0.2, stroke_width=3, color=WHITE)
        arrow_sample = Arrow(start=encoder_group.get_right(), end=latent_group.get_left(), buff=0.2, stroke_width=3, color=WHITE)
        arrow_decode = Arrow(start=latent_group.get_right(), end=decoder_group.get_left(), buff=0.2, stroke_width=3, color=WHITE)
        arrow_recon = Arrow(start=decoder_group.get_right(), end=recon_image_group.get_left(), buff=0.2, stroke_width=3, color=WHITE)

        # Labels on arrows
        label_encode = Text("encode", font_size=20).next_to(arrow_encode, UP, buff=0.1)
        label_sample = Text("sample", font_size=20).next_to(arrow_sample, UP, buff=0.1)
        label_decode = Text("decode", font_size=20).next_to(arrow_decode, UP, buff=0.1)
        label_recon = Text("reconstruct", font_size=20).next_to(arrow_recon, UP, buff=0.1)

        # Build scene step-by-step
        self.play(FadeIn(input_image_group), run_time=1)
        self.wait(0.5)
        self.play(Create(arrow_encode), Write(label_encode), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(encoder_group), run_time=1)
        self.wait(0.5)
        self.play(Create(arrow_sample), Write(label_sample), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(latent_group), run_time=1)
        self.wait(0.5)
        self.play(Create(arrow_decode), Write(label_decode), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(decoder_group), run_time=1)
        self.wait(0.5)
        self.play(Create(arrow_recon), Write(label_recon), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(recon_image_group), run_time=1)
        self.wait(1)

        # Highlight latent sampling: animate one dot moving from encoder output to latent space
        sample_dot = Dot(point=encoder_group.get_right() + RIGHT*0.3, radius=0.06, color=YELLOW)
        self.play(FadeIn(sample_dot))
        self.play(
            sample_dot.animate.move_to(latent_group.get_center() + UP*0.5 + RIGHT*0.3),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(1)

        # Clean up
        self.play(
            FadeOut(title),
            FadeOut(input_image_group),
            FadeOut(encoder_group),
            FadeOut(latent_group),
            FadeOut(decoder_group),
            FadeOut(recon_image_group),
            FadeOut(arrow_encode), FadeOut(arrow_sample), FadeOut(arrow_decode), FadeOut(arrow_recon),
            FadeOut(label_encode), FadeOut(label_sample), FadeOut(label_decode), FadeOut(label_recon),
            FadeOut(sample_dot),
            run_time=1
        )
