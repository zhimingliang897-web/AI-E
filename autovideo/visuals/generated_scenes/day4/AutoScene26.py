from manim import *

class AutoScene26(Scene):
    def construct(self):
        # Create clean "image" as a simple geometric representation: a centered square with grid lines
        clean_image = Square(side_length=3, color=BLUE, fill_opacity=0.1)
        grid_lines = VGroup()
        for i in range(1, 3):
            # Horizontal and vertical grid lines
            h_line = Line(
                clean_image.get_corner(DL) + i * UP * 1.5,
                clean_image.get_corner(DR) + i * UP * 1.5,
                stroke_width=1,
                color=BLUE_A
            )
            v_line = Line(
                clean_image.get_corner(DL) + i * RIGHT * 1.5,
                clean_image.get_corner(UL) + i * RIGHT * 1.5,
                stroke_width=1,
                color=BLUE_A
            )
            grid_lines.add(h_line, v_line)
        clean_image_group = VGroup(clean_image, grid_lines).move_to(ORIGIN)

        # Title text
        title = Text("Denoising Process", font_size=28, weight=BOLD).to_edge(UP)

        # Step 1: Show clean image
        self.play(FadeIn(title))
        self.wait(0.5)
        self.play(Create(clean_image_group), run_time=1.5)
        self.wait(1)

        # Step 2: Progressive Gaussian noise addition (simulate with fading in noisy blobs)
        # We'll use overlapping translucent gray circles with random positions and sizes to mimic noise
        noise_blobs = VGroup()
        np.random.seed(42)  # deterministic for reproducibility
        for _ in range(40):
            radius = 0.1 + 0.2 * np.random.random()
            x = np.random.uniform(-1.2, 1.2)
            y = np.random.uniform(-1.2, 1.2)
            blob = Circle(
                radius=radius,
                color=GREY_C,
                fill_opacity=0.4,
                stroke_width=0
            ).move_to(x * RIGHT + y * UP)
            noise_blobs.add(blob)

        # Animate noise addition in 4 progressive bursts
        self.play(
            FadeIn(noise_blobs[:10], scale=0.5),
            run_time=0.8,
            rate_func=smooth
        )
        self.wait(0.3)
        self.play(
            FadeIn(noise_blobs[10:20], scale=0.5),
            run_time=0.8,
            rate_func=smooth
        )
        self.wait(0.3)
        self.play(
            FadeIn(noise_blobs[20:30], scale=0.5),
            run_time=0.8,
            rate_func=smooth
        )
        self.wait(0.3)
        self.play(
            FadeIn(noise_blobs[30:], scale=0.5),
            run_time=0.8,
            rate_func=smooth
        )
        self.wait(1)

        # Step 3: Highlight "noisy blob" — fade out grid, emphasize noise
        noisy_blob_label = Text("Noisy Blob", font_size=24, color=YELLOW).next_to(clean_image, DOWN, buff=0.5)
        self.play(
            FadeOut(grid_lines),
            Write(noisy_blob_label),
            run_time=0.7
        )
        self.wait(1)

        # Step 4: Reverse denoising — remove noise progressively
        self.play(
            FadeOut(noisy_blob_label),
            run_time=0.5
        )
        self.play(
            FadeOut(noise_blobs[30:], scale=0.5),
            run_time=0.7,
            rate_func=smooth
        )
        self.wait(0.2)
        self.play(
            FadeOut(noise_blobs[20:30], scale=0.5),
            run_time=0.7,
            rate_func=smooth
        )
        self.wait(0.2)
        self.play(
            FadeOut(noise_blobs[10:20], scale=0.5),
            run_time=0.7,
            rate_func=smooth
        )
        self.wait(0.2)
        self.play(
            FadeOut(noise_blobs[:10], scale=0.5),
            run_time=0.7,
            rate_func=smooth
        )
        self.wait(0.5)

        # Step 5: Restore clean image — redraw grid
        self.play(FadeIn(grid_lines), run_time=1.2)
        self.wait(1)

        # Final label
        restored_label = Text("Restored Image", font_size=24, color=GREEN).next_to(clean_image, DOWN, buff=0.5)
        self.play(Write(restored_label))
        self.wait(1)
        self.play(FadeOut(restored_label))

        # Fade out all
        self.play(FadeOut(clean_image_group), FadeOut(title), run_time=1)
        self.wait(0.5)
