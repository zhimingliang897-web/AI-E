from manim import *

class AIBigBang2014(Scene):
    def construct(self):
        # Timeline Marker 2014
        year_text = Text("2014", weight=BOLD, color=YELLOW, font_size=72)
        year_circle = Circle(color=YELLOW, radius=1.2).set_stroke(width=3)
        marker_group = VGroup(year_circle, year_text)
        
        # VAE Icon (Compression) - Arrows converging to a center
        vae_text = Text("VAE", weight=BOLD, color=BLUE, font_size=48)
        vae_center = Dot(color=BLUE, radius=0.1)
        vae_arrow_left = Arrow(LEFT * 2, LEFT * 0.5, color=BLUE, buff=0)
        vae_arrow_right = Arrow(RIGHT * 2, RIGHT * 0.5, color=BLUE, buff=0)
        vae_content = VGroup(vae_arrow_left, vae_arrow_right, vae_center)
        vae_group = VGroup(vae_content, vae_text).arrange(DOWN, buff=0.5)
        vae_group.shift(LEFT * 3.5)
        
        # GAN Icon (Fighting) - Arrows clashing
        gan_text = Text("GAN", weight=BOLD, color=RED, font_size=48)
        gan_arrow_left = Arrow(LEFT * 1.5, RIGHT * 0.2, color=RED, buff=0)
        gan_arrow_right = Arrow(RIGHT * 1.5, LEFT * 0.2, color=RED, buff=0)
        gan_spark = Circle(color=WHITE, radius=0.2, fill_opacity=1)
        gan_content = VGroup(gan_arrow_left, gan_arrow_right, gan_spark)
        gan_group = VGroup(gan_content, gan_text).arrange(DOWN, buff=0.5)
        gan_group.shift(RIGHT * 3.5)
        
        # Initial State
        self.play(Create(year_circle), Write(year_text), run_time=2)
        self.wait(0.5)
        
        # Pulse Effect
        self.play(marker_group.animate.scale(1.2), run_time=0.5)
        self.play(marker_group.animate.scale(1/1.2), run_time=0.5)
        self.wait(0.5)
        
        # Explosion Transition
        self.play(
            FadeOut(marker_group, scale=1.5),
            FadeIn(vae_group, shift=LEFT * 3.5),
            FadeIn(gan_group, shift=RIGHT * 3.5),
            run_time=2
        )
        
        self.wait(1)
        
        # Highlight labels
        self.play(
            vae_text.animate.set_color(WHITE),
            gan_text.animate.set_color(WHITE),
            run_time=1
        )
        self.wait(1)
