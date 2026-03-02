from manim import *

class VaeGanBattle(Scene):
    def construct(self):
        # Title
        title = Text("VAE vs GAN Architecture", weight=BOLD, font_size=36, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Divider
        divider = Line(UP * 3.5, DOWN * 3.5, color=GRAY, stroke_width=2)
        self.add(divider)

        # --- LEFT SIDE: VAE ---
        # Input Image (Pixel grid representation)
        input_pixels = VGroup(*[Rectangle(height=0.25, width=0.25, color=WHITE, stroke_width=1) for _ in range(9)])
        input_pixels.arrange(RIGHT, buff=0.05)
        input_pixels.move_to(LEFT * 5.5)
        input_label = Text("Input", font_size=24, color=WHITE)
        input_label.next_to(input_pixels, DOWN)

        # Encoder
        encoder = Rectangle(height=1.5, width=0.8, color=BLUE, stroke_width=2)
        encoder.next_to(input_pixels, RIGHT, buff=0.5)
        enc_label = Text("Encoder", font_size=24, color=BLUE)
        enc_label.next_to(encoder, DOWN)

        # Latent Space
        latent = Circle(radius=0.4, color=GREEN, stroke_width=2)
        latent.next_to(encoder, RIGHT, buff=0.5)
        latent_label = Text("Latent Z", font_size=24, color=GREEN)
        latent_label.next_to(latent, DOWN)

        # Decoder
        decoder = Rectangle(height=1.5, width=0.8, color=BLUE, stroke_width=2)
        decoder.next_to(latent, RIGHT, buff=0.5)
        dec_label = Text("Decoder", font_size=24, color=BLUE)
        dec_label.next_to(decoder, DOWN)

        # Output Image
        output_pixels = VGroup(*[Rectangle(height=0.25, width=0.25, color=WHITE, stroke_width=1) for _ in range(9)])
        output_pixels.arrange(RIGHT, buff=0.05)
        output_pixels.next_to(decoder, RIGHT, buff=0.5)
        output_label = Text("Output", font_size=24, color=WHITE)
        output_label.next_to(output_pixels, DOWN)

        # Arrows VAE
        arrow_vae_1 = Arrow(input_pixels.get_right(), encoder.get_left(), color=WHITE, buff=0.1)
        arrow_vae_2 = Arrow(encoder.get_right(), latent.get_left(), color=WHITE, buff=0.1)
        arrow_vae_3 = Arrow(latent.get_right(), decoder.get_left(), color=WHITE, buff=0.1)
        arrow_vae_4 = Arrow(decoder.get_right(), output_pixels.get_left(), color=WHITE, buff=0.1)

        vae_group = VGroup(
            input_pixels, input_label, encoder, enc_label, 
            latent, latent_label, decoder, dec_label, 
            output_pixels, output_label, 
            arrow_vae_1, arrow_vae_2, arrow_vae_3, arrow_vae_4
        )
        vae_group.move_to(LEFT * 2.5)

        # --- RIGHT SIDE: GAN ---
        # Generator Robot (Circle body, Line arms)
        gen_body = Circle(radius=0.4, color=RED, stroke_width=2)
        gen_arm_l = Line(LEFT * 0.5, LEFT * 0.8, color=RED, stroke_width=2)
        gen_arm_r = Line(RIGHT * 0.5, RIGHT * 0.8, color=RED, stroke_width=2)
        generator = VGroup(gen_body, gen_arm_l, gen_arm_r)
        generator.move_to(RIGHT * 1.5 + UP * 1)
        gen_label = Text("Generator", font_size=24, color=RED)
        gen_label.next_to(generator, DOWN)

        # Discriminator Robot (Square body, Triangle eye)
        disc_body = Square(side_length=0.8, color=BLUE, stroke_width=2)
        disc_eye = Triangle(color=BLUE, stroke_width=2).scale(0.4)
        disc_eye.next_to(disc_body, UP, buff=0)
        discriminator = VGroup(disc_body, disc_eye)
        discriminator.move_to(RIGHT * 4.5 + UP * 1)
        disc_label = Text("Discriminator", font_size=24, color=BLUE)
        disc_label.next_to(discriminator, DOWN)

        # Noise Input
        noise = Text("Noise", font_size=20, color=GRAY)
        noise.next_to(generator, LEFT, buff=0.8)
        arrow_noise = Arrow(noise.get_right(), generator.get_left(), color=GRAY, buff=0.1)

        # Fake Image
        fake_img = Rectangle(height=0.8, width=0.8, color=GREEN, stroke_width=2)
        fake_img.next_to(generator, DOWN, buff=0.5)
        fake_label = Text("Fake", font_size=20, color=GREEN)
        fake_label.next_to(fake_img, DOWN)
        arrow_gen_fake = Arrow(generator.get_bottom(), fake_img.get_top(), color=RED, buff=0.1)

        # Real Image
        real_img = Rectangle(height=0.8, width=0.8, color=WHITE, stroke_width=2)
        real_img.next_to(discriminator, DOWN, buff=0.5)
        real_label = Text("Real", font_size=20, color=WHITE)
        real_label.next_to(real_img, DOWN)
        
        # Arrows to Discriminator
        arrow_fake_disc = Arrow(fake_img.get_right(), discriminator.get_left(), color=GREEN, buff=0.1)
        arrow_real_disc = Arrow(real_img.get_top(), discriminator.get_bottom(), color=WHITE, buff=0.1)

        gan_group = VGroup(
            generator, gen_label, discriminator, disc_label, 
            noise, arrow_noise, fake_img, fake_label, arrow_gen_fake, 
            real_img, real_label, arrow_fake_disc, arrow_real_disc
        )
        gan_group.move_to(RIGHT * 2.5)

        # --- ANIMATIONS ---
        # 1. Show VAE
        self.play(Create(input_pixels), Write(input_label))
        self.play(Create(arrow_vae_1), Create(encoder), Write(enc_label))
        self.play(Create(arrow_vae_2), Create(latent), Write(latent_label))
        self.play(Create(arrow_vae_3), Create(decoder), Write(dec_label))
        self.play(Create(arrow_vae_4), Create(output_pixels), Write(output_label))
        self.wait(1)

        # 2. Show GAN Components
        self.play(Create(noise), Create(arrow_noise), Create(generator), Write(gen_label))
        self.play(Create(discriminator), Write(disc_label))
        self.wait(0.5)

        # 3. GAN Battle Process
        # Generator creates fake
        self.play(Create(arrow_gen_fake), Create(fake_img), Write(fake_label))
        # Send to Discriminator
        self.play(Create(arrow_fake_disc))
        # Real Data enters
        self.play(Create(real_img), Write(real_label), Create(arrow_real_disc))

        # 4. Battle Effect (Flash colors & Move)
        # Discriminator Judges (Flash)
        for _ in range(3):
            self.play(
                discriminator.animate.set_color(YELLOW),
                run_time=0.15
            )
            self.play(
                discriminator.animate.set_color(BLUE),
                run_time=0.15
            )
        
        # Generator Adjusts (Move slightly)
        self.play(
            generator.animate.shift(UP * 0.2),
            run_time=0.5
        )
        self.play(
            generator.animate.shift(DOWN * 0.2),
            run_time=0.5
        )

        # 5. Final Wait
        self.wait(2)
