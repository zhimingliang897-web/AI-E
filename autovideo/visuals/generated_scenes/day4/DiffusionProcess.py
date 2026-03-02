from manim import *
import numpy as np

class DiffusionProcess(Scene):
    def construct(self):
        # Grid configuration
        rows = 10
        cols = 10
        square_size = 0.4
        gap = 0.05
        
        original_group = VGroup()
        noise_group = VGroup()
        reconstructed_group = VGroup()
        
        # Color palette for noise
        noise_colors = [WHITE, GREY, BLACK, GREY_B]
        
        # Generate pixels
        for r in range(rows):
            for c in range(cols):
                # Calculate position centered at origin
                x = (c - cols / 2 + 0.5) * (square_size + gap)
                y = (rows / 2 - 0.5 - r) * (square_size + gap)
                
                # Determine original color (Circle pattern)
                dist = np.sqrt(x**2 + y**2)
                if dist < 1.8:
                    color = BLUE
                else:
                    color = BLACK
                
                # 1. Original Pixel
                sq_orig = Square(side_length=square_size, stroke_width=0)
                sq_orig.set_fill(color, opacity=1)
                sq_orig.move_to([x, y, 0])
                original_group.add(sq_orig)
                
                # 2. Noise Pixel (Random color, jittered position)
                noise_color = np.random.choice(noise_colors)
                jitter_x = np.random.uniform(-0.15, 0.15)
                jitter_y = np.random.uniform(-0.15, 0.15)
                sq_noise = Square(side_length=square_size, stroke_width=0)
                sq_noise.set_fill(noise_color, opacity=1)
                sq_noise.move_to([x + jitter_x, y + jitter_y, 0])
                noise_group.add(sq_noise)
                
                # 3. Reconstructed Pixel (Same as original)
                sq_rec = Square(side_length=square_size, stroke_width=0)
                sq_rec.set_fill(color, opacity=1)
                sq_rec.move_to([x, y, 0])
                reconstructed_group.add(sq_rec)
        
        # Labels
        label_orig = Text("Original Data", font_size=24).next_to(original_group, DOWN, buff=0.5)
        label_noise = Text("Forward Diffusion (Noise)", font_size=24).next_to(noise_group, DOWN, buff=0.5)
        label_rec = Text("Reverse Diffusion (Reconstruction)", font_size=24).next_to(reconstructed_group, DOWN, buff=0.5)
        
        # Initial State
        self.add(original_group, label_orig)
        self.wait(1)
        
        # Forward Diffusion: Original -> Noise
        self.play(
            Transform(original_group, noise_group),
            Transform(label_orig, label_noise),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)
        
        # Reverse Diffusion: Noise -> Reconstructed
        self.play(
            Transform(original_group, reconstructed_group),
            Transform(label_orig, label_rec),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)
