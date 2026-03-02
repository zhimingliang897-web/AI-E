from manim import *

class AutoScene31(Scene):
    def construct(self):
        # Title
        title = Text("Architecture Comparison", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Split screen: left for U-Net, right for DiT
        divider = Line(UP * 3, DOWN * 3, stroke_width=2, color=GREY_C)
        divider.move_to(ORIGIN)
        self.play(Create(divider))
        self.wait(0.5)

        # === U-Net Side (Left) ===
        unet_label = Text("U-Net", font_size=28, weight=BOLD).to_edge(UP + LEFT, buff=0.7)
        unet_label.shift(RIGHT * 2.5)
        self.play(Write(unet_label))
        self.wait(0.5)

        # U-Net schematic: encoder-decoder with skip connections
        # Encoder blocks (left column)
        enc_blocks = VGroup()
        for i in range(4):
            b = Rectangle(width=1.0, height=0.6, color=BLUE, fill_opacity=0.2, stroke_width=1.5)
            b.move_to(LEFT * 4 + UP * (1.5 - i * 1.2))
            enc_blocks.add(b)
        
        # Decoder blocks (right column)
        dec_blocks = VGroup()
        for i in range(4):
            b = Rectangle(width=1.0, height=0.6, color=TEAL_A, fill_opacity=0.2, stroke_width=1.5)
            b.move_to(RIGHT * 2 + UP * (1.5 - i * 1.2))
            dec_blocks.add(b)

        # Skip connection arcs (curved)
        skips = VGroup()
        for i in range(4):
            arc = ArcBetweenPoints(
                enc_blocks[i].get_right(),
                dec_blocks[i].get_left(),
                angle=-PI/3,
                stroke_width=1.2,
                color=PURPLE_E
            )
            skips.add(arc)

        # Add all U-Net elements
        self.play(
            Create(enc_blocks),
            Create(dec_blocks),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(Create(skips), run_time=1.5)
        self.wait(0.5)

        # Cross out "U-Net"
        cross_line = Line(
            unet_label.get_corner(DL) + DOWN * 0.1 + LEFT * 0.1,
            unet_label.get_corner(UR) + UP * 0.1 + RIGHT * 0.1,
            color=RED,
            stroke_width=6
        )
        self.play(Create(cross_line), run_time=1)
        self.wait(0.5)

        # === DiT Side (Right) ===
        dit_label = Text("DiT", font_size=28, weight=BOLD).to_edge(UP + RIGHT, buff=0.7)
        dit_label.shift(LEFT * 2.5)
        self.play(Write(dit_label))
        self.wait(0.5)

        # Grid of tokens: 4x4 grid of circles
        token_grid = VGroup()
        for i in range(4):
            for j in range(4):
                dot = Circle(radius=0.15, color=YELLOW, fill_opacity=0.7, stroke_width=1.2)
                dot.move_to(RIGHT * 5 + RIGHT * j * 0.8 + UP * (0.6 - i * 0.8))
                token_grid.add(dot)

        # Attention heads: three small overlapping circles (head icons)
        head_icon = VGroup(
            Circle(radius=0.12, color=PURPLE_A, fill_opacity=0.3, stroke_width=1),
            Circle(radius=0.12, color=PURPLE_A, fill_opacity=0.3, stroke_width=1).shift(UP * 0.15 + RIGHT * 0.15),
            Circle(radius=0.12, color=PURPLE_A, fill_opacity=0.3, stroke_width=1).shift(DOWN * 0.15 + RIGHT * 0.15),
        ).scale(0.7).next_to(token_grid, DOWN, buff=0.8)

        # Label for attention heads
        heads_label = Text("8 Heads", font_size=20, color=PURPLE_A).next_to(head_icon, DOWN, buff=0.3)

        self.play(Create(token_grid), run_time=1.5)
        self.wait(0.5)
        self.play(Create(head_icon), Write(heads_label), run_time=1)
        self.wait(1)

        # Animate attention: highlight token interactions
        highlight_tokens = [token_grid[0], token_grid[5], token_grid[10], token_grid[15]]
        highlight_arcs = VGroup()
        for t1 in highlight_tokens:
            for t2 in highlight_tokens:
                if t1 is not t2:
                    arc = CurvedArrow(
                        t1.get_center() + UP * 0.2,
                        t2.get_center() + UP * 0.2,
                        angle=PI/4,
                        stroke_width=1,
                        color=GREY_C,
                        tip_length=0.1
                    )
                    highlight_arcs.add(arc)
        highlight_arcs.set_opacity(0.4)

        self.play(
            *[t.animate.set_color(RED) for t in highlight_tokens],
            Create(highlight_arcs),
            run_time=2
        )
        self.wait(1)

        # Final emphasis
        arrow = Arrow(
            start=LEFT * 1.5 + DOWN * 2.5,
            end=RIGHT * 1.5 + DOWN * 2.5,
            stroke_width=3,
            tip_length=0.2,
            color=YELLOW
        )
        arrow_text = Text("→ Modern Standard", font_size=24, color=YELLOW).next_to(arrow, DOWN, buff=0.3)

        self.play(
            Create(arrow),
            Write(arrow_text),
            run_time=1.5
        )
        self.wait(2)
