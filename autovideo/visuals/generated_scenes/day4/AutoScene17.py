from manim import *

class AutoScene17(Scene):
    def construct(self):
        # Title
        title = Text("VAE Pipeline", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Input images (left)
        input_label = Text("Input Images", font_size=24).next_to(title, DOWN, buff=0.8).shift(LEFT * 3.5)
        input_images = VGroup()
        for i in range(3):
            img = Rectangle(height=1.2, width=1.2, color=TEAL_A, fill_opacity=0.2, stroke_width=2)
            img.shift(DOWN * 0.5 + LEFT * 3.5 + RIGHT * i * 1.4)
            input_images.add(img)
        self.play(FadeIn(input_label), Create(input_images))
        self.wait(0.5)

        # Encoder arrow
        encoder_arrow = Arrow(
            start=input_images.get_right() + RIGHT * 0.3,
            end=RIGHT * 1.5,
            buff=0,
            stroke_width=3,
            color=YELLOW
        )
        encoder_text = Text("Encoder", font_size=24).next_to(encoder_arrow, UP, buff=0.2)
        self.play(GrowArrow(encoder_arrow), Write(encoder_text))
        self.wait(0.5)

        # Latent space: cloud of dots
        latent_label = Text("Latent Space", font_size=24).next_to(encoder_arrow, DOWN, buff=1.0)
        latent_cloud = VGroup()
        np.random.seed(42)
        for _ in range(40):
            x = np.random.normal(0, 0.8)
            y = np.random.normal(0, 0.6)
            dot = Dot(point=[x, y, 0], radius=0.04, color=PURPLE_E)
            latent_cloud.add(dot)
        latent_cloud.scale(0.8).move_to(RIGHT * 1.5 + DOWN * 0.5)
        self.play(FadeIn(latent_label), FadeIn(latent_cloud))
        self.wait(0.5)

        # Decoder arrow
        decoder_arrow = Arrow(
            start=latent_cloud.get_right() + RIGHT * 0.3,
            end=RIGHT * 4.5,
            buff=0,
            stroke_width=3,
            color=YELLOW
        )
        decoder_text = Text("Decoder", font_size=24).next_to(decoder_arrow, UP, buff=0.2)
        self.play(GrowArrow(decoder_arrow), Write(decoder_text))
        self.wait(0.5)

        # Reconstructed images (right)
        recon_label = Text("Reconstructions", font_size=24).next_to(decoder_arrow, DOWN, buff=1.0)
        recon_images = VGroup()
        for i in range(3):
            img = Rectangle(height=1.2, width=1.2, color=BLUE, fill_opacity=0.2, stroke_width=2)
            img.shift(DOWN * 0.5 + RIGHT * 4.5 + RIGHT * i * 1.4)
            recon_images.add(img)
        self.play(FadeIn(recon_label), Create(recon_images))
        self.wait(0.5)

        # Highlight diversity: animate slight random shifts and color variations
        recon_anims = []
        for i, img in enumerate(recon_images):
            shift_vec = np.array([
                np.random.uniform(-0.1, 0.1),
                np.random.uniform(-0.1, 0.1),
                0
            ])
            new_color = [RED, GREEN, YELLOW][i % 3]
            recon_anims.append(img.animate.shift(shift_vec).set_color(new_color))
        self.play(*recon_anims, run_time=2, rate_func=smooth)
        self.wait(1)

        # Add subtle "sampling" effect: highlight a few latent dots pulsing
        pulse_dots = [latent_cloud[i] for i in [5, 12, 27, 35]]
        for dot in pulse_dots:
            self.play(dot.animate.scale(1.8).set_color(RED), run_time=0.6)
            self.play(dot.animate.scale(1/1.8).set_color(PURPLE_E), run_time=0.6)
        self.wait(1)

        # Final emphasis: draw bounding ellipse around latent cloud
        cloud_center = latent_cloud.get_center()
        ellipse = Ellipse(width=3.0, height=2.0, color=RED, stroke_width=2)
        ellipse.move_to(cloud_center)
        ellipse_label = Text("Gaussian Prior", font_size=20, color=RED).next_to(ellipse, UP, buff=0.2)
        self.play(Create(ellipse), Write(ellipse_label))
        self.wait(1.5)

        # Fade out all except title and ellipse label
        self.play(
            FadeOut(input_label),
            FadeOut(input_images),
            FadeOut(encoder_arrow),
            FadeOut(encoder_text),
            FadeOut(latent_label),
            FadeOut(latent_cloud),
            FadeOut(decoder_arrow),
            FadeOut(decoder_text),
            FadeOut(recon_label),
            FadeOut(recon_images),
            FadeOut(ellipse),
        )
        self.wait(0.5)
        self.play(Transform(ellipse_label, Text("Latent Distribution ~ N(0,I)", font_size=24, color=RED).move_to(ellipse_label)))
        self.wait(1)
