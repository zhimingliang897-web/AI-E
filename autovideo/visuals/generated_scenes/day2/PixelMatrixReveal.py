from manim import *

class PixelMatrixReveal(Scene):
    def construct(self):
        # Background is black by default

        # Step 1: Start with a clean, stylized "photo" — represented as a vibrant 4x4 color grid (vector approximation)
        photo_grid = VGroup()
        colors = [
            [RED, BLUE, GREEN, YELLOW],
            [PURPLE, TEAL_A, GREY_C, ORANGE],
            [PINK, GOLD, MAROON, INDIGO],
            [LIME, CYAN, DARK_BLUE, WHITE]
        ]
        cell_size = 0.8
        for i in range(4):
            for j in range(4):
                square = Square(side_length=cell_size, fill_color=colors[i][j], fill_opacity=1, stroke_width=0.5, stroke_color=GREY_C)
                square.move_to((j - 1.5) * cell_size * RIGHT + (i - 1.5) * cell_size * DOWN)
                photo_grid.add(square)

        # Add subtle border to photo group
        photo_frame = SurroundingRectangle(photo_grid, buff=0.1, stroke_color=GREY_C, stroke_width=1)
        photo_group = VGroup(photo_grid, photo_frame)

        # Title label (optional subtle context)
        title = Text("Photo", font_size=24, color=GREY_C).next_to(photo_group, UP, buff=0.5)

        self.play(FadeIn(title), Create(photo_group), run_time=1.5)
        self.wait(0.5)

        # Step 2: Zoom-in animation — scale up and center
        self.play(
            photo_group.animate.scale(2.5).move_to(ORIGIN),
            title.animate.scale(0.7).next_to(photo_group, UP, buff=0.3),
            run_time=2,
            rate_func=smooth
        )
        self.wait(0.5)

        # Step 3: Dissolve into RGB number grid
        # Build RGB grid: 4x4, each cell shows e.g., "255,0,0"
        rgb_grid = VGroup()
        rgb_labels = VGroup()
        binary_pulses = VGroup()

        # Approximate RGB values from original colors (simplified for clarity & aesthetics)
        rgb_values = [
            ["255,0,0", "0,0,255", "0,255,0", "255,255,0"],
            ["128,0,128", "0,128,128", "128,128,128", "255,165,0"],
            ["255,192,203", "255,215,0", "128,0,0", "75,0,130"],
            ["0,255,0", "0,255,255", "0,0,139", "255,255,255"]
        ]

        for i in range(4):
            for j in range(4):
                # RGB text
                rgb_text = Text(rgb_values[i][j], font_size=18, color=WHITE)
                # Pixel label
                pixel_label = Text("px", font_size=12, color=GREY_C).next_to(rgb_text, UP, buff=0.15)
                # Group per cell
                cell_group = VGroup(rgb_text, pixel_label)
                cell_group.move_to(
                    (j - 1.5) * cell_size * 1.8 * RIGHT +
                    (i - 1.5) * cell_size * 1.8 * DOWN
                )
                rgb_grid.add(cell_group)

                # Binary pulse: tiny pulsing dot beside each RGB cell
                pulse_dot = Dot(radius=0.04, color=TEAL_A).next_to(rgb_text, RIGHT, buff=0.2)
                binary_pulses.add(pulse_dot)

        # Fade out photo, fade in RGB grid + pulses
        self.play(
            FadeOut(photo_group),
            FadeOut(title),
            FadeIn(rgb_grid),
            FadeIn(binary_pulses),
            run_time=2
        )
        self.wait(0.5)

        # Animate binary pulses: subtle opacity pulse (0.3 → 1 → 0.3), staggered
        for i, dot in enumerate(binary_pulses):
            self.play(
                dot.animate.set_opacity(1.0),
                rate_func=rate_functions.ease_in_out_sine,
                run_time=0.8,
                lag_ratio=0.05
            )
            self.play(
                dot.animate.set_opacity(0.3),
                rate_func=rate_functions.ease_in_out_sine,
                run_time=0.8,
                lag_ratio=0.05
            )

        # Optional: highlight top-left pixel with gentle scale + glow effect
        top_left_cell = rgb_grid[0]
        glow = Circle(
            radius=0.4,
            stroke_color=TEAL_A,
            stroke_width=2,
            fill_opacity=0,
            stroke_opacity=0.7
        ).move_to(top_left_cell.get_center())
        self.play(Create(glow), top_left_cell.animate.scale(1.15), run_time=1.2)
        self.play(FadeOut(glow), top_left_cell.animate.scale(1/1.15), run_time=0.8)

        # Final clean hold
        self.wait(1.5)
