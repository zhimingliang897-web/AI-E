from manim import *

class AutoScene32(Scene):
    def construct(self):
        # Title
        title = Text("Vision Transformer: Image → Tokens", font_size=30, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Original image (represented as a colored rectangle with grid)
        image = Rectangle(width=6, height=4, color=GREY_C, fill_opacity=0.1, stroke_color=GREY_C)
        image_label = Text("Input Image", font_size=24).next_to(image, DOWN, buff=0.3)
        
        # Draw 4x3 grid to simulate patches
        rows, cols = 4, 3
        patch_width = image.width / cols
        patch_height = image.height / rows
        grid_lines = VGroup()
        for i in range(1, rows):
            h_line = Line(
                start=image.get_corner(DL) + UP * i * patch_height,
                end=image.get_corner(DR) + UP * i * patch_height,
                stroke_width=1,
                color=GREY_C
            )
            grid_lines.add(h_line)
        for j in range(1, cols):
            v_line = Line(
                start=image.get_corner(DL) + RIGHT * j * patch_width,
                end=image.get_corner(UL) + RIGHT * j * patch_width,
                stroke_width=1,
                color=GREY_C
            )
            grid_lines.add(v_line)

        self.play(Create(image), Write(image_label))
        self.wait(0.5)
        self.play(Create(grid_lines))
        self.wait(0.5)

        # Animate splitting: fade out grid lines, highlight patches one by one
        self.play(FadeOut(grid_lines))
        self.wait(0.3)

        # Create patch tokens (colored squares with labels)
        patches = VGroup()
        token_labels = VGroup()
        for i in range(rows):
            for j in range(cols):
                x = image.get_left()[0] + patch_width/2 + j * patch_width
                y = image.get_bottom()[1] + patch_height/2 + i * patch_height
                patch = Square(side_length=min(patch_width, patch_height)*0.8, color=BLUE, fill_opacity=0.3, stroke_width=2)
                patch.move_to([x, y, 0])
                label = Text(f"P{i*cols+j+1}", font_size=16).move_to(patch.get_center())
                patches.add(patch)
                token_labels.add(label)

        self.play(LaggedStart(*[FadeIn(p) for p in patches], lag_ratio=0.05))
        self.play(LaggedStart(*[Write(l) for l in token_labels], lag_ratio=0.05))
        self.wait(0.5)

        # Arrow: patches → tokens
        arrow1 = Arrow(
            start=image.get_right() + RIGHT * 0.5,
            end=image.get_right() + RIGHT * 1.5,
            buff=0,
            stroke_width=3)
        tokens_label = Text("Tokens", font_size=24).next_to(arrow1, RIGHT, buff=0.5)
        self.play(GrowArrow(arrow1), Write(tokens_label))
        self.wait(0.5)

        # Arrange tokens horizontally below
        token_row = VGroup()
        for i, (p, l) in enumerate(zip(patches, token_labels)):
            token = VGroup(p.copy(), l.copy()).scale(0.7)
            token.move_to(2.5*DOWN + (i - (len(patches)-1)/2) * 1.1 * RIGHT)
            token_row.add(token)

        self.play(
            LaggedStart(
                *[TransformFromCopy(patches[i], token_row[i]) for i in range(len(patches))],
                lag_ratio=0.1
            ),
            FadeOut(image),
            FadeOut(image_label),
            FadeOut(arrow1),
            FadeOut(tokens_label),
            FadeOut(token_labels),
            run_time=2
        )
        self.wait(0.5)

        # Transformer blocks: three stacked rectangles with "Transformer Block" label
        block_width, block_height = 2.0, 1.2
        block1 = RoundedRectangle(corner_radius=0.2, width=block_width, height=block_height, fill_color=TEAL_A, fill_opacity=0.3, stroke_color=TEAL_A)
        block2 = RoundedRectangle(corner_radius=0.2, width=block_width, height=block_height, fill_color=TEAL_A, fill_opacity=0.3, stroke_color=TEAL_A)
        block3 = RoundedRectangle(corner_radius=0.2, width=block_width, height=block_height, fill_color=TEAL_A, fill_opacity=0.3, stroke_color=TEAL_A)
        blocks = VGroup(block1, block2, block3).arrange(DOWN, buff=0.4).shift(UP * 0.5)
        block_labels = VGroup(
            Text("Block 1", font_size=20).move_to(block1.get_center()),
            Text("Block 2", font_size=20).move_to(block2.get_center()),
            Text("Block 3", font_size=20).move_to(block3.get_center())
        )

        self.play(FadeIn(blocks), FadeIn(block_labels))
        self.wait(0.5)

        # Arrows from tokens to first block
        arrows_in = VGroup()
        for token in token_row:
            arrow = Arrow(
                start=token.get_top(),
                end=blocks[0].get_bottom() + LEFT * (block_width/2 - 0.2) + (token.get_center()[0] - token_row.get_center()[0]) * RIGHT * 0.8,
                stroke_width=2,
                buff=0.1
            )
            arrows_in.add(arrow)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows_in], lag_ratio=0.1))
        self.wait(0.5)

        # Highlight attention: draw connections between tokens inside block (simplified)
        attn_dots = VGroup()
        for _ in range(8):
            dot = Dot(radius=0.05, color=PURPLE_E)
            dot.move_to(blocks[0].get_center() + np.random.uniform(-0.4, 0.4, size=3))
            attn_dots.add(dot)
        self.play(FadeIn(attn_dots), run_time=1.5)
        self.wait(0.5)

        # Arrow from last block to output
        arrow_out = Arrow(
            start=blocks[2].get_top(),
            end=blocks[2].get_top() + UP * 1.2,
            stroke_width=3,
            buff=0
        )
        output_label = Text("Output Features", font_size=24).next_to(arrow_out, UP, buff=0.3)
        self.play(GrowArrow(arrow_out), Write(output_label))
        self.wait(0.5)

        # Final summary text
        summary = Text("Each patch = token → processed like text in Transformer", font_size=26, t2c={"token": YELLOW, "Transformer": BLUE})
        summary.to_edge(DOWN, buff=0.7)
        self.play(Write(summary))
        self.wait(2)
