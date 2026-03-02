from manim import *

class VisionArchitectureEvolution(Scene):
    def construct(self):
        # Title
        title = Text("Vision Architecture Evolution", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Split screen: left (CNN), right (Transformer)
        divider = Line(UP * 3, DOWN * 3, stroke_width=2, color=GREY_C)
        divider.move_to(ORIGIN)
        self.play(Create(divider))
        self.wait(0.5)

        # Labels
        cnn_label = Text("CNN Pipeline", font_size=24, color=BLUE).to_edge(LEFT, buff=0.7).shift(UP * 2.5)
        trans_label = Text("Transformer Attention", font_size=24, color=PURPLE).to_edge(RIGHT, buff=0.7).shift(UP * 2.5)
        self.play(Write(cnn_label), Write(trans_label))
        self.wait(0.5)

        # === LEFT SIDE: CNN PIPELINE ===
        # Input image placeholder (grayscale grid)
        input_grid = VGroup()
        for i in range(5):
            for j in range(5):
                cell = Square(side_length=0.4, fill_opacity=0.7, fill_color=GREY_C if (i+j) % 2 == 0 else GREY_C)
                cell.move_to(LEFT * 4 + RIGHT * j * 0.4 + DOWN * i * 0.4)
                input_grid.add(cell)
        input_text = Text("Input", font_size=16).next_to(input_grid, UP, buff=0.3)
        self.play(FadeIn(input_grid), Write(input_text))
        self.wait(0.5)

        # Kernel sliding animation (3x3)
        kernel = Square(side_length=1.2, color=YELLOW, stroke_width=3)
        kernel.set_z_index(1)
        kernel.move_to(LEFT * 4 + RIGHT * 0.8 + DOWN * 0.8)  # top-left position over grid

        # Edge detection kernel pattern (simplified: high contrast center)
        k_cells = VGroup()
        for i in range(3):
            for j in range(3):
                k_cell = Square(side_length=0.4, fill_opacity=0.9, fill_color=RED if (i==1 and j==1) else BLUE)
                k_cell.move_to(kernel.get_center() + RIGHT*(j-1)*0.4 + DOWN*(i-1)*0.4)
                k_cells.add(k_cell)

        kernel_group = VGroup(kernel, k_cells)
        self.play(Create(kernel_group))
        self.wait(0.5)

        # Animate kernel sliding across top row
        for j in range(3):
            self.play(kernel_group.animate.shift(RIGHT * 0.4), run_time=0.4)
        self.wait(0.3)
        # Slide down to middle row
        self.play(kernel_group.animate.shift(DOWN * 0.4 + LEFT * 0.8), run_time=0.4)
        for j in range(3):
            self.play(kernel_group.animate.shift(RIGHT * 0.4), run_time=0.4)
        self.wait(0.3)
        # Slide down to bottom row
        self.play(kernel_group.animate.shift(DOWN * 0.4 + LEFT * 0.8), run_time=0.4)
        for j in range(3):
            self.play(kernel_group.animate.shift(RIGHT * 0.4), run_time=0.4)
        self.wait(0.5)

        # Fade kernel, show edge map
        edge_map = VGroup()
        for i in range(3):
            for j in range(3):
                val = 0.8 if (i==1 and j==1) else 0.3
                cell = Square(side_length=0.4, fill_opacity=val, fill_color=TEAL_A)
                cell.move_to(LEFT * 4 + RIGHT * (j+1)*0.4 + DOWN * (i+1)*0.4)
                edge_map.add(cell)
        edge_text = Text("Edges", font_size=16).next_to(edge_map, UP, buff=0.3)
        self.play(
            FadeOut(kernel_group),
            FadeIn(edge_map),
            Write(edge_text)
        )
        self.wait(0.5)

        # Shape abstraction: combine into shape blob
        shape_blob = Circle(radius=0.6, fill_opacity=0.6, fill_color=GREEN, stroke_width=0)
        shape_blob.move_to(LEFT * 4)
        shape_text = Text("Shape", font_size=16).next_to(shape_blob, UP, buff=0.3)
        self.play(
            Transform(edge_map, shape_blob),
            Transform(edge_text, shape_text)
        )
        self.wait(0.5)

        # Object recognition: cat icon (simplified: circle head + two triangles for ears)
        cat_head = Circle(radius=0.5, fill_opacity=0.7, fill_color=GREY_C)
        left_ear = Triangle().scale(0.2).rotate(-30*DEGREES).move_to(cat_head.get_center() + LEFT*0.4 + UP*0.3)
        right_ear = Triangle().scale(0.2).rotate(30*DEGREES).move_to(cat_head.get_center() + RIGHT*0.4 + UP*0.3)
        cat = VGroup(cat_head, left_ear, right_ear)
        cat.move_to(LEFT * 4)
        obj_text = Text("Object: Cat", font_size=16).next_to(cat, UP, buff=0.3)
        self.play(
            Transform(shape_blob, cat),
            Transform(shape_text, obj_text)
        )
        self.wait(0.5)

        # === RIGHT SIDE: TRANSFORMER ATTENTION ===
        # Input tokens: simplified "cat" image as 3x3 token grid
        token_grid = VGroup()
        for i in range(3):
            for j in range(3):
                t = Circle(radius=0.2, fill_opacity=0.5, fill_color=GREY_C)
                t.move_to(RIGHT * 4 + RIGHT * j * 0.6 + DOWN * i * 0.6)
                token_grid.add(t)
        token_text = Text("Tokens", font_size=16).next_to(token_grid, UP, buff=0.3)
        self.play(FadeIn(token_grid), Write(token_text))
        self.wait(0.5)

        # Attention heatmap: start with focus on top corners (ears)
        # Create heatmap overlay: circles scaled by attention weight
        heatmap_ears = VGroup()
        # Top-left and top-right tokens → ears
        ear_weights = [0.9, 0.9, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
        for idx, t in enumerate(token_grid):
            w = ear_weights[idx]
            h = Circle(radius=0.2 * w, fill_opacity=0.7 * w, fill_color=PURPLE_A)
            h.move_to(t.get_center())
            heatmap_ears.add(h)
        heatmap_ears.set_z_index(-1)
        attn_text_ears = Text("Focus: Ears", font_size=16, color=PURPLE).next_to(token_grid, DOWN, buff=0.3)
        self.play(FadeIn(heatmap_ears), Write(attn_text_ears))
        self.wait(0.5)

        # Transition to full-cat attention
        full_weights = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
        heatmap_full = VGroup()
        for idx, t in enumerate(token_grid):
            w = full_weights[idx]
            h = Circle(radius=0.2 * w, fill_opacity=0.7 * w, fill_color=PURPLE_E)
            h.move_to(t.get_center())
            heatmap_full.add(h)
        heatmap_full.set_z_index(-1)
        attn_text_full = Text("Focus: Whole Cat", font_size=16, color=PURPLE).next_to(token_grid, DOWN, buff=0.3)
        self.play(
            Transform(heatmap_ears, heatmap_full),
            Transform(attn_text_ears, attn_text_full)
        )
        self.wait(0.5)

        # Highlight final cat object on right side too (mirror left)
        cat_right = cat.copy().move_to(RIGHT * 4)
        obj_text_right = Text("Object: Cat", font_size=16).next_to(cat_right, UP, buff=0.3)
        self.play(
            FadeIn(cat_right),
            Write(obj_text_right)
        )
        self.wait(0.5)

        # Layer labels
        cnn_layers = VGroup(
            Text("Input", font_size=14).next_to(input_grid, DOWN, buff=0.2),
            Text("Edge Detection", font_size=14).next_to(edge_map, DOWN, buff=0.2),
            Text("Shape Abstraction", font_size=14).next_to(shape_blob, DOWN, buff=0.2),
            Text("Object Recognition", font_size=14).next_to(cat, DOWN, buff=0.2)
        )
        trans_layers = VGroup(
            Text("Tokens", font_size=14).next_to(token_grid, DOWN, buff=0.2),
            Text("Local Attention", font_size=14).next_to(heatmap_ears, DOWN, buff=0.2),
            Text("Global Attention", font_size=14).next_to(heatmap_full, DOWN, buff=0.2),
            Text("Object Recognition", font_size=14).next_to(cat_right, DOWN, buff=0.2)
        )

        self.play(
            Write(cnn_layers[0]), Write(trans_layers[0]),
            run_time=0.5
        )
        self.wait(0.3)
        self.play(
            Write(cnn_layers[1]), Write(trans_layers[1]),
            run_time=0.5
        )
        self.wait(0.3)
        self.play(
            Write(cnn_layers[2]), Write(trans_layers[2]),
            run_time=0.5
        )
        self.wait(0.3)
        self.play(
            Write(cnn_layers[3]), Write(trans_layers[3]),
            run_time=0.5
        )
        self.wait(1)

        # Final summary
        summary = Text("CNN: Local → Hierarchical\nTransformer: Global → Contextual", font_size=20, line_spacing=1.3)
        summary.to_edge(DOWN, buff=0.7)
        self.play(Write(summary))
        self.wait(2)
