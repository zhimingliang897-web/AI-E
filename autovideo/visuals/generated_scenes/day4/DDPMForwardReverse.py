from manim import *

class DDPMForwardReverse(Scene):
    def construct(self):
        # Set up title
        title = Text("DDPM: Forward & Reverse Process", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Create clean image placeholder (a simple stylized "image" — e.g., a centered square with grid-like pattern)
        clean_img = Square(side_length=2.0, color=TEAL_A, fill_opacity=0.8)
        grid_lines = VGroup()
        for i in range(1, 4):
            grid_lines.add(Line(clean_img.get_corner(UL) + RIGHT * i * 0.5, clean_img.get_corner(DL) + RIGHT * i * 0.5, stroke_width=1, color=TEAL_E))
            grid_lines.add(Line(clean_img.get_corner(UL) + DOWN * i * 0.5, clean_img.get_corner(UR) + DOWN * i * 0.5, stroke_width=1, color=TEAL_E))
        clean_img_group = VGroup(clean_img, grid_lines).move_to(ORIGIN)

        # Label clean image
        clean_label = Text("x₀ (clean)", font_size=24).next_to(clean_img_group, DOWN, buff=0.3)

        # Forward process: 10 noise steps → pure noise
        # Precompute sigma values decreasing from σ₀=1.0 to σ₉≈0.01 (log-linear decay)
        sigmas_forward = [round(10**(-0.1 * i), 3) for i in range(10)]  # ≈ [1.0, 0.794, ..., 0.01]
        noisy_states = [clean_img_group.copy()]
        for i in range(1, 10):
            noise_img = Square(side_length=2.0, color=GREY_C, fill_opacity=0.7 + 0.03 * i)
            # Add subtle noise texture via small random dots
            dots = VGroup(*[
                Dot(radius=0.02, color=GREY_B).move_to(
                    clean_img.get_center() + np.array([
                        (np.random.random() - 0.5) * 1.6,
                        (np.random.random() - 0.5) * 1.6,
                        0
                    ])
                ) for _ in range(30 + i * 5)
            ])
            noisy_states.append(VGroup(noise_img, dots))

        # Pure noise (step 10)
        pure_noise = Square(side_length=2.0, color=GREY_B, fill_opacity=1.0)
        pure_dots = VGroup(*[Dot(radius=0.03, color=GREY_D).move_to(
            pure_noise.get_center() + np.array([
                (np.random.random() - 0.5) * 1.8,
                (np.random.random() - 0.5) * 1.8,
                0
            ])
        ) for _ in range(120)])
        noisy_states.append(VGroup(pure_noise, pure_dots))

        # Reverse process: denoising steps (same 10 steps backward)
        denoised_states = [noisy_states[-1].copy()]  # start from pure noise
        for i in range(9, 0, -1):
            # Approximate denoised version: slightly less noisy, more structure
            denoise_img = Square(side_length=2.0, color=interpolate_color(GREY_B, TEAL_A, (10 - i) / 10), fill_opacity=0.5 + 0.04 * (10 - i))
            # Reduce dot count gradually
            n_dots = max(10, 120 - i * 10)
            dots = VGroup(*[
                Dot(radius=0.025, color=interpolate_color(GREY_D, TEAL_E, (10 - i) / 10)).move_to(
                    denoise_img.get_center() + np.array([
                        (np.random.random() - 0.5) * (1.6 - i * 0.1),
                        (np.random.random() - 0.5) * (1.6 - i * 0.1),
                        0
                    ])
                ) for _ in range(n_dots)
            ])
            denoised_states.append(VGroup(denoise_img, dots))
        denoised_states.append(clean_img_group.copy())  # final restored x₀

        # Position forward chain horizontally
        forward_chain = VGroup()
        for i, state in enumerate(noisy_states):
            state.scale(0.7)
            if i == 0:
                state.move_to(LEFT * 5.5)
            else:
                state.next_to(forward_chain[i-1], RIGHT, buff=0.8)
            forward_chain.add(state)

        # Labels for forward steps
        forward_labels = VGroup()
        for i, sigma in enumerate(sigmas_forward + [0.001]):  # add tiny sigma for last step
            label_text = f"σ={sigma}" if i < 10 else "σ≈0"
            lab = Text(label_text, font_size=18).next_to(forward_chain[i], UP, buff=0.25)
            forward_labels.add(lab)

        # Position reverse chain below forward chain
        reverse_chain = VGroup()
        for i, state in enumerate(denoised_states):
            state.scale(0.7)
            if i == 0:
                state.move_to(DOWN * 2.5 + LEFT * 5.5)
            else:
                state.next_to(reverse_chain[i-1], RIGHT, buff=0.8)
            reverse_chain.add(state)

        # Labels for reverse steps (same sigmas, but now increasing)
        reverse_labels = VGroup()
        sigmas_reverse = [0.001] + sigmas_forward[:-1]  # reverse order of sigmas (start tiny, end at 1.0)
        for i, sigma in enumerate(sigmas_reverse):
            label_text = f"σ={sigma}" if i > 0 else "σ≈0"
            lab = Text(label_text, font_size=18).next_to(reverse_chain[i], DOWN, buff=0.25)
            reverse_labels.add(lab)

        # Arrows
        forward_arrows = VGroup()
        for i in range(9):
            arrow = Arrow(
                forward_chain[i].get_right(),
                forward_chain[i+1].get_left(),
                buff=0.1,
                stroke_width=2)
            forward_arrows.add(arrow)

        reverse_arrows = VGroup()
        for i in range(9):
            arrow = Arrow(
                reverse_chain[i].get_right(),
                reverse_chain[i+1].get_left(),
                buff=0.1,
                stroke_width=2,
                color=BLUE
            )
            reverse_arrows.add(arrow)

        # Animate forward process
        self.play(FadeIn(clean_img_group), Write(clean_label))
        self.wait(0.5)

        self.play(
            FadeIn(forward_chain[0]),
            Write(forward_labels[0])
        )
        self.wait(0.3)

        for i in range(1, 10):
            self.play(
                TransformFromCopy(forward_chain[i-1], forward_chain[i]),
                Write(forward_labels[i]),
                Create(forward_arrows[i-1]),
                run_time=0.8
            )
            self.wait(0.2)

        # Animate reverse process
        self.wait(0.5)
        rev_title = Text("Reverse (Denoising)", font_size=28, color=BLUE).next_to(reverse_chain[0], UP, buff=0.8)
        self.play(Write(rev_title))
        self.wait(0.3)

        self.play(FadeIn(reverse_chain[0]), Write(reverse_labels[0]))
        self.wait(0.3)

        for i in range(1, 10):
            self.play(
                TransformFromCopy(reverse_chain[i-1], reverse_chain[i]),
                Write(reverse_labels[i]),
                Create(reverse_arrows[i-1]),
                run_time=0.8
            )
            self.wait(0.2)

        # Final highlight: clean image restored
        self.play(
            reverse_chain[-1].animate.set_stroke(TEAL_A, width=3).set_fill(opacity=0.9),
            Indicate(reverse_chain[-1], scale_factor=1.05, color=TEAL_A),
            run_time=1.2
        )
        self.wait(0.5)

        # Clean up and conclusion
        conclusion = Text("x₀ ← denoised ← ... ← x₁₀ ~ 𝒩(0,I)", font_size=26, color=YELLOW).to_edge(DOWN, buff=0.5)
        self.play(Write(conclusion))
        self.wait(2)
