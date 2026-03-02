from manim import *

class DiTvsUNet(Scene):
    def construct(self):
        # Title
        title = Text("DiT vs U-Net", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Split screen
        hline = Line(LEFT * 7, RIGHT * 7, stroke_width=1, color=GREY_C).move_to(ORIGIN)
        hline.shift(UP * 2.8)
        vline = Line(UP * 2.5, DOWN * 2.5, stroke_width=1, color=GREY_C)
        vline.move_to(ORIGIN)

        # Labels
        unet_label = Text("U-Net", font_size=28, weight=BOLD).set_color(BLUE)
        dit_label = Text("DiT", font_size=28, weight=BOLD).set_color(PURPLE)
        unet_label.next_to(LEFT * 3.5 + UP * 2.5, UP, buff=0.3)
        dit_label.next_to(RIGHT * 3.5 + UP * 2.5, UP, buff=0.3)

        self.play(
            Create(hline),
            Create(vline),
            Write(unet_label),
            Write(dit_label)
        )
        self.wait(0.5)

        # === U-Net (Left) ===
        # Encoder blocks (downsampling)
        enc1 = Rectangle(height=0.6, width=1.4, fill_color=BLUE_A, fill_opacity=0.7, stroke_color=BLUE)
        enc2 = Rectangle(height=0.6, width=1.2, fill_color=BLUE_B, fill_opacity=0.7, stroke_color=BLUE)
        enc3 = Rectangle(height=0.6, width=1.0, fill_color=BLUE_C, fill_opacity=0.7, stroke_color=BLUE)

        enc1.move_to(LEFT * 2.5 + UP * 1.2)
        enc2.move_to(LEFT * 2.5 + UP * 0.2)
        enc3.move_to(LEFT * 2.5 + DOWN * 0.8)

        # Decoder blocks (upsampling)
        dec1 = Rectangle(height=0.6, width=1.0, fill_color=TEAL_A, fill_opacity=0.7, stroke_color=TEAL)
        dec2 = Rectangle(height=0.6, width=1.2, fill_color=TEAL_B, fill_opacity=0.7, stroke_color=TEAL)
        dec3 = Rectangle(height=0.6, width=1.4, fill_color=TEAL_C, fill_opacity=0.7, stroke_color=TEAL)

        dec1.move_to(LEFT * 2.5 + DOWN * 0.2)
        dec2.move_to(LEFT * 2.5 + UP * 0.8)
        dec3.move_to(LEFT * 2.5 + UP * 1.8)

        # Skip connections (arrows from encoder to decoder)
        skip1 = CurvedArrow(
            enc1.get_right() + RIGHT * 0.2,
            dec2.get_left() + LEFT * 0.2,
            angle=-PI/4,
            stroke_width=2,
            color=YELLOW
        )
        skip2 = CurvedArrow(
            enc2.get_right() + RIGHT * 0.2,
            dec1.get_left() + LEFT * 0.2,
            angle=-PI/4,
            stroke_width=2,
            color=YELLOW
        )
        skip3 = CurvedArrow(
            enc3.get_right() + RIGHT * 0.2,
            dec1.get_bottom() + DOWN * 0.1,
            angle=-PI/3,
            stroke_width=2,
            color=YELLOW
        )

        # U-Net "bottleneck"
        bottleneck = Rectangle(height=0.6, width=0.8, fill_color=PURPLE_A, fill_opacity=0.7, stroke_color=PURPLE)
        bottleneck.move_to(LEFT * 2.5 + DOWN * 1.5)

        # Arrows between U-Net layers
        down1 = Arrow(enc1.get_bottom(), enc2.get_top(), buff=0, stroke_width=2, color=BLUE)
        down2 = Arrow(enc2.get_bottom(), enc3.get_top(), buff=0, stroke_width=2, color=BLUE)
        down3 = Arrow(enc3.get_bottom(), bottleneck.get_top(), buff=0, stroke_width=2, color=BLUE)
        up1 = Arrow(bottleneck.get_right(), dec1.get_left(), buff=0, stroke_width=2, color=TEAL)
        up2 = Arrow(dec1.get_top(), dec2.get_bottom(), buff=0, stroke_width=2, color=TEAL)
        up3 = Arrow(dec2.get_top(), dec3.get_bottom(), buff=0, stroke_width=2, color=TEAL)

        # Add U-Net elements
        self.play(
            Create(enc1), Create(enc2), Create(enc3),
            Create(bottleneck),
            Create(dec1), Create(dec2), Create(dec3),
            Create(down1), Create(down2), Create(down3),
            Create(up1), Create(up2), Create(up3),
            Create(skip1), Create(skip2), Create(skip3)
        )
        self.wait(0.5)

        # U-Net caption
        unet_caption = Text("Skip connections\nenable multi-scale feature fusion", font_size=18).set_color(YELLOW)
        unet_caption.next_to(enc1, LEFT, buff=0.8)
        self.play(Write(unet_caption))
        self.wait(0.5)

        # === DiT (Right) ===
        # Input image placeholder
        img_rect = RoundedRectangle(corner_radius=0.1, height=0.8, width=1.6, fill_color=GREY_C, fill_opacity=0.3, stroke_color=GREY_C)
        img_rect.move_to(RIGHT * 2.5 + UP * 1.5)
        img_label = Text("Image", font_size=16).next_to(img_rect, UP, buff=0.2)

        # Patch grid (3x3)
        patches = VGroup()
        for i in range(3):
            for j in range(3):
                p = Square(side_length=0.3, fill_color=GREY_A, fill_opacity=0.5, stroke_color=GREY_C)
                p.move_to(RIGHT * 2.5 + RIGHT * (j - 1) * 0.35 + DOWN * (i - 1) * 0.35 + UP * 0.5)
                patches.add(p)
        patch_label = Text("Patches", font_size=16).next_to(patches, UP, buff=0.2)

        # Linear embedding layer
        embed = Rectangle(height=0.6, width=1.4, fill_color=PURPLE_A, fill_opacity=0.7, stroke_color=PURPLE)
        embed.move_to(RIGHT * 2.5 + UP * 0.1)
        embed_label = Text("Linear Embedding", font_size=16).next_to(embed, UP, buff=0.2)

        # Transformer blocks (3 stacked)
        trans1 = Rectangle(height=0.5, width=1.2, fill_color=PURPLE_B, fill_opacity=0.7, stroke_color=PURPLE)
        trans2 = Rectangle(height=0.5, width=1.2, fill_color=PURPLE_C, fill_opacity=0.7, stroke_color=PURPLE)
        trans3 = Rectangle(height=0.5, width=1.2, fill_color=PURPLE_D, fill_opacity=0.7, stroke_color=PURPLE)
        trans1.move_to(RIGHT * 2.5 + DOWN * 0.5)
        trans2.move_to(RIGHT * 2.5 + DOWN * 1.1)
        trans3.move_to(RIGHT * 2.5 + DOWN * 1.7)
        trans_label = Text("Transformer Blocks", font_size=16).next_to(trans1, UP, buff=0.2)

        # Patch reconstruction
        recon = RoundedRectangle(corner_radius=0.1, height=0.8, width=1.6, fill_color=GREY_C, fill_opacity=0.3, stroke_color=GREY_C)
        recon.move_to(RIGHT * 2.5 + DOWN * 2.4)
        recon_label = Text("Reconstruct Image", font_size=16).next_to(recon, DOWN, buff=0.2)

        # Arrows for DiT flow
        arrow1 = Arrow(img_rect.get_bottom(), patches.get_top(), buff=0.1, stroke_width=2, color=WHITE)
        arrow2 = Arrow(patches.get_bottom(), embed.get_top(), buff=0.1, stroke_width=2, color=WHITE)
        arrow3 = Arrow(embed.get_bottom(), trans1.get_top(), buff=0.1, stroke_width=2, color=WHITE)
        arrow4 = Arrow(trans1.get_bottom(), trans2.get_top(), buff=0.1, stroke_width=2, color=WHITE)
        arrow5 = Arrow(trans2.get_bottom(), trans3.get_top(), buff=0.1, stroke_width=2, color=WHITE)
        arrow6 = Arrow(trans3.get_bottom(), recon.get_top(), buff=0.1, stroke_width=2, color=WHITE)

        # Highlight "no convolutions, all attention"
        highlight = Text("No convolutions —\nall attention", font_size=20, weight=BOLD).set_color(YELLOW)
        highlight.move_to(RIGHT * 2.5 + DOWN * 3.2)

        self.play(
            Create(img_rect), Write(img_label),
            Create(patches), Write(patch_label),
            Create(embed), Write(embed_label),
            Create(trans1), Create(trans2), Create(trans3), Write(trans_label),
            Create(recon), Write(recon_label),
            Create(arrow1), Create(arrow2), Create(arrow3),
            Create(arrow4), Create(arrow5), Create(arrow6),
            Write(highlight)
        )
        self.wait(1)

        # Emphasize key contrast
        no_conv = Text("U-Net: Convolutional", font_size=22, color=BLUE).to_edge(DOWN, buff=0.8).shift(LEFT * 3)
        all_attn = Text("DiT: Attention-only", font_size=22, color=PURPLE).to_edge(DOWN, buff=0.8).shift(RIGHT * 3)
        self.play(Write(no_conv), Write(all_attn))
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(hline), FadeOut(vline),
            FadeOut(unet_label), FadeOut(dit_label),
            FadeOut(unet_caption),
            FadeOut(no_conv), FadeOut(all_attn),
            FadeOut(highlight),
            *[FadeOut(mob) for mob in self.mobjects if mob not in [title, hline, vline, unet_label, dit_label, unet_caption, no_conv, all_attn, highlight]]
        )
