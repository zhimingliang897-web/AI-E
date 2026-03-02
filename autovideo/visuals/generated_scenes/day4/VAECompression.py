from manim import *

class VAECompression(Scene):
    def construct(self):
        # 1. Create Input Data (Represented as a grid of squares)
        input_grid = VGroup()
        for i in range(3):
            for j in range(3):
                square = Square(side_length=0.5, color=BLUE, fill_opacity=0.8)
                square.shift(RIGHT * i * 0.5 + UP * j * 0.5)
                input_grid.add(square)
        input_grid.center()
        input_label = Text("Input Data", weight=BOLD, color=BLUE).next_to(input_grid, DOWN, buff=0.5)

        # 2. Create Latent Space (Represented as a glowing sphere/circle)
        # Using Circle instead of forbidden Sphere
        core_circle = Circle(radius=0.3, color=YELLOW, fill_opacity=1)
        glow_rings = VGroup()
        for r in [0.5, 0.7, 0.9]:
            ring = Circle(radius=r, color=YELLOW, stroke_opacity=0.3)
            glow_rings.add(ring)
        latent_space = VGroup(core_circle, glow_rings).center()
        latent_space.scale(0)  # Start hidden/small for animation
        latent_label = Text("Latent Space", weight=BOLD, color=YELLOW).next_to(latent_space, DOWN, buff=0.5)
        latent_label.set_opacity(0)

        # 3. Create Output Data (Reconstructed)
        output_grid = VGroup()
        for i in range(3):
            for j in range(3):
                square = Square(side_length=0.5, color=GREEN, fill_opacity=0.8)
                square.shift(RIGHT * i * 0.5 + UP * j * 0.5)
                output_grid.add(square)
        output_grid.center()
        output_grid.scale(0)  # Start hidden/small
        output_label = Text("Reconstruction", weight=BOLD, color=GREEN).next_to(output_grid, DOWN, buff=0.5)
        output_label.set_opacity(0)

        # --- Animation Sequence ---

        # Step 1: Show Input
        self.play(Create(input_grid), Write(input_label))
        self.wait(1)

        # Step 2: Compress (Input -> Latent)
        # Visualize compression by shrinking input and expanding latent
        self.play(
            input_grid.animate.scale(0.1).set_opacity(0),
            input_label.animate.fade(1),
            latent_space.animate.scale(1).set_opacity(1),
            latent_label.animate.fade(1),
            run_time=2,
            rate_func=smooth
        )
        self.wait(0.5)

        # Step 3: Pulse Latent Space (Glowing effect)
        self.play(
            latent_space.animate.scale(1.2).set_opacity(0.8),
            run_time=0.5,
            rate_func=smooth
        )
        self.play(
            latent_space.animate.scale(1).set_opacity(1),
            run_time=0.5,
            rate_func=smooth
        )
        self.wait(0.5)

        # Step 4: Expand (Latent -> Output)
        # Visualize expansion by shrinking latent and expanding output
        self.play(
            latent_space.animate.scale(0.1).set_opacity(0),
            latent_label.animate.fade(1),
            output_grid.animate.scale(1).set_opacity(1),
            output_label.animate.fade(1),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)

        # Final State
        self.play(
            output_grid.animate.set_color(GREEN),
            run_time=0.5
        )
        self.wait(1)
