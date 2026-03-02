from manim import *

class DDPMProcess(Scene):
    def construct(self):
        # Create clean image placeholder (a simple stylized "image" icon)
        clean_img = VGroup(
            Rectangle(width=2.0, height=1.6, color=TEAL_A, fill_opacity=0.8),
            Line(LEFT * 0.8, RIGHT * 0.8, stroke_width=2).shift(UP * 0.4),
            Circle(radius=0.15, color=YELLOW, fill_opacity=1).shift(DOWN * 0.3 + LEFT * 0.4),
            Circle(radius=0.15, color=YELLOW, fill_opacity=1).shift(DOWN * 0.3 + RIGHT * 0.4),
            Arc(start_angle=0, angle=PI, radius=0.4, stroke_width=2).shift(DOWN * 0.6)
        ).scale(0.7)

        # Create noisy frames: grayscale fade effect using increasing opacity of gray overlay
        noise_levels = [0.1, 0.3, 0.5, 0.7, 0.9]
        noisy_imgs = []
        for i, alpha in enumerate(noise_levels):
            overlay = Rectangle(
                width=2.0, height=1.6,
                color=GREY_C,
                fill_opacity=alpha,
                stroke_width=0
            ).scale(0.7)
            noisy_img = VGroup(clean_img.copy(), overlay)
            noisy_imgs.append(noisy_img)

        # Position elements horizontally
        all_imgs = [clean_img] + noisy_imgs + [clean_img.copy()]
        spacing = 2.8
        for i, img in enumerate(all_imgs):
            img.move_to(LEFT * 5 + RIGHT * i * spacing)

        # Arrows between forward steps
        forward_arrows = VGroup()
        for i in range(len(all_imgs) - 1):
            if i < 5:  # forward diffusion (clean → noisy)
                arrow = Arrow(
                    all_imgs[i].get_right(),
                    all_imgs[i + 1].get_left(),
                    buff=0.2,
                    stroke_width=3,
                    max_tip_length_to_length_ratio=0.12
                )
                forward_arrows.add(arrow)

        # Reverse arrows (noisy → clean)
        reverse_arrows = VGroup()
        for i in range(5, len(all_imgs) - 1):
            arrow = CurvedArrow(
                all_imgs[i + 1].get_left(),
                all_imgs[i].get_right(),
                angle=-PI/3,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.12
            )
            reverse_arrows.add(arrow)

        # Labels
        labels = VGroup()
        labels.add(Text("x₀", font_size=28).next_to(all_imgs[0], DOWN, buff=0.4))
        for i in range(1, 6):
            labels.add(Text(f"xₜ", font_size=28).next_to(all_imgs[i], DOWN, buff=0.4))
        labels.add(Text("x₀", font_size=28).next_to(all_imgs[-1], DOWN, buff=0.4))

        # Noise Schedule label
        noise_label = Text("Noise Schedule", font_size=36, weight=BOLD, color=PURPLE_E)
        noise_label.to_edge(UP, buff=0.5)

        # Animate
        self.play(FadeIn(clean_img), Write(labels[0]))
        self.wait(0.5)

        # Forward diffusion: add noise step-by-step
        for i in range(5):
            self.play(
                FadeIn(noisy_imgs[i]),
                Write(labels[i + 1]),
                Create(forward_arrows[i]),
                run_time=0.8
            )
            self.wait(0.3)

        # Show full noisy chain
        self.play(FadeIn(noise_label))
        self.wait(0.5)

        # Pulse noise label
        self.play(
            noise_label.animate.scale(1.1).set_color(PURPLE_A),
            rate_func=smooth,
            run_time=1.2
        )

        # Reverse process arrows
        self.play(Create(reverse_arrows), run_time=2)
        self.wait(0.5)

        # Restore final clean image (already placed; just highlight)
        self.play(
            all_imgs[-1].animate.set_stroke(YELLOW, width=3).set_z_index(1),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            all_imgs[-1].animate.set_stroke(width=0),
            run_time=0.5
        )

        self.wait(1)
