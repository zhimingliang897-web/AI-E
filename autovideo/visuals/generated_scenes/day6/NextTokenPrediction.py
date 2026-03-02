from manim import *

class NextTokenPrediction(Scene):
    def construct(self):
        # Title
        title = Text("Next Token Prediction", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Define positions in a horizontal flow
        prompt_pos = LEFT * 5.5
        embed_pos = LEFT * 1.5
        dist_pos = RIGHT * 1.5
        token_pos = RIGHT * 5.5

        # Prompt box (light blue, rounded)
        prompt = RoundedRectangle(
            width=3.0, height=1.2, corner_radius=0.3, fill_color=BLUE_A, fill_opacity=0.8, stroke_color=BLUE_E
        )
        prompt.move_to(prompt_pos)
        prompt_text = Text("Prompt", font_size=24, weight=BOLD).move_to(prompt.get_center())
        prompt_group = VGroup(prompt, prompt_text)

        # Token Embedding box (teal, rounded)
        embed = RoundedRectangle(
            width=3.0, height=1.2, corner_radius=0.3, fill_color=TEAL_A, fill_opacity=0.8, stroke_color=TEAL_E
        )
        embed.move_to(embed_pos)
        embed_text = Text("Token\nEmbedding", font_size=24, weight=BOLD).move_to(embed.get_center())
        embed_group = VGroup(embed, embed_text)

        # Probability Distribution box (purple, rounded)
        dist = RoundedRectangle(
            width=3.0, height=1.2, corner_radius=0.3, fill_color=PURPLE_A, fill_opacity=0.8, stroke_color=PURPLE_E
        )
        dist.move_to(dist_pos)
        dist_text = Text("Probability\nDistribution", font_size=24, weight=BOLD).move_to(dist.get_center())
        dist_group = VGroup(dist, dist_text)

        # Top-1 Token box (yellow-orange, rounded)
        token = RoundedRectangle(
            width=3.0, height=1.2, corner_radius=0.3, fill_color=YELLOW, fill_opacity=0.8, stroke_color=GOLD_E
        )
        token.move_to(token_pos)
        token_text = Text("Top-1 Token", font_size=24, weight=BOLD).move_to(token.get_center())
        token_group = VGroup(token, token_text)

        # Arrows between stages
        arrow1 = Arrow(prompt.get_right(), embed.get_left(), buff=0.2, stroke_width=6)
        arrow2 = Arrow(embed.get_right(), dist.get_left(), buff=0.2, stroke_width=6)
        arrow3 = Arrow(dist.get_right(), token.get_left(), buff=0.2, stroke_width=6)

        # Add all elements
        self.play(
            FadeIn(prompt_group),
            FadeIn(embed_group),
            FadeIn(dist_group),
            FadeIn(token_group),
            Create(arrow1),
            Create(arrow2),
            Create(arrow3),
        )
        self.wait(1)

        # Animate embedding step: tokens pop up inside embedding box
        tokens = VGroup(
            Circle(radius=0.2, color=WHITE, fill_opacity=0.9).shift(LEFT * 0.6 + UP * 0.2),
            Circle(radius=0.2, color=WHITE, fill_opacity=0.9).shift(RIGHT * 0.0 + UP * 0.2),
            Circle(radius=0.2, color=WHITE, fill_opacity=0.9).shift(RIGHT * 0.6 + UP * 0.2),
            Circle(radius=0.2, color=WHITE, fill_opacity=0.9).shift(LEFT * 0.3 + DOWN * 0.2),
            Circle(radius=0.2, color=WHITE, fill_opacity=0.9).shift(RIGHT * 0.3 + DOWN * 0.2),
        )
        tokens.scale(0.7)
        self.play(FadeIn(tokens), run_time=1.2)
        self.wait(0.5)

        # Animate probability distribution: bars rising
        bars = VGroup()
        bar_heights = [0.2, 0.5, 0.8, 0.4, 0.6, 0.3]
        for i, h in enumerate(bar_heights):
            bar = Rectangle(
                width=0.3,
                height=h * 0.8,
                fill_color=GREY_C,
                fill_opacity=0.9,
                stroke_color=GREY_C,
            ).move_to(dist.get_center() + LEFT * 1.2 + RIGHT * i * 0.4)
            bars.add(bar)
        self.play(
            *[GrowFromBottom(bar) for bar in bars],
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(0.5)

        # Highlight top bar and animate "Top-1 Token" appearance
        top_bar = bars[2].copy().set_color(YELLOW).set_stroke(YELLOW, width=3)
        self.play(
            bars[2].animate.set_color(YELLOW).set_stroke(YELLOW, width=3),
            Flash(bars[2], color=YELLOW, flash_radius=0.5, line_stroke_width=3),
            run_time=1.2
        )
        self.wait(0.5)

        # Final token zoom-in effect
        final_token = Text("→ 'the'", font_size=32, color=YELLOW, weight=BOLD)
        final_token.next_to(token, DOWN, buff=0.5)
        self.play(Write(final_token), run_time=1.2)
        self.wait(1)

        # Subtle pulse on final token
        self.play(
            final_token.animate.scale(1.1).set_color(GOLD),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(1)

        # Fade out all except title and final token
        self.play(
            FadeOut(prompt_group),
            FadeOut(embed_group),
            FadeOut(dist_group),
            FadeOut(token_group),
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(arrow3),
            FadeOut(tokens),
            FadeOut(bars),
        )
        self.wait(0.5)

        # End screen
        conclusion = Text("Next Token Prediction", font_size=40, weight=BOLD, color=YELLOW)
        conclusion.move_to(ORIGIN)
        self.play(ReplacementTransform(title, conclusion))
        self.wait(1)
