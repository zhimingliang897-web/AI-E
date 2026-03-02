from manim import *

class TransformerFoundation(Scene):
    def construct(self):
        # Title
        title = Text("Transformer Foundation", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Input tokens (horizontal row of circles)
        input_tokens = VGroup(*[
            Circle(radius=0.3, color=BLUE, fill_opacity=0.8).shift(RIGHT * i * 1.2)
            for i in range(5)
        ])
        input_label = Text("Input Tokens", font_size=24).next_to(input_tokens, UP, buff=0.5)
        self.play(FadeIn(input_tokens), Write(input_label))
        self.wait(0.5)

        # Attention heads: arcs above tokens with glowing effect
        attention_arcs = VGroup()
        glow_arcs = VGroup()
        for i in range(3):  # 3 attention heads
            arc = ArcBetweenPoints(
                input_tokens[0].get_top() + UP * 0.5,
                input_tokens[-1].get_top() + UP * 0.5,
                angle=-PI/3 + i * PI/6,
                color=YELLOW,
                stroke_width=2
            )
            glow_arc = arc.copy().set_stroke(YELLOW_E, width=6, opacity=0.4)
            attention_arcs.add(arc)
            glow_arcs.add(glow_arc)
        
        self.play(
            FadeIn(glow_arcs),
            Create(attention_arcs, run_time=2),
            rate_func=smooth
        )
        self.wait(0.5)

        # Feed-forward layer: stacked rectangles
        ff_layer = VGroup(
            Rectangle(width=4, height=0.8, color=GREEN, fill_opacity=0.7),
            Rectangle(width=4, height=0.8, color=GREEN_A, fill_opacity=0.7).shift(DOWN * 0.9),
        ).next_to(attention_arcs, DOWN, buff=0.8)
        ff_label = Text("Feed-Forward", font_size=24).next_to(ff_layer, UP, buff=0.3)
        self.play(FadeIn(ff_layer), Write(ff_label))
        self.wait(0.5)

        # Output tokens (smaller circles below ff layer)
        output_tokens = VGroup(*[
            Circle(radius=0.25, color=PURPLE, fill_opacity=0.8).shift(RIGHT * i * 1.0 + DOWN * 2.5)
            for i in range(5)
        ])
        output_label = Text("Output Tokens", font_size=24).next_to(output_tokens, DOWN, buff=0.5)
        self.play(FadeIn(output_tokens), Write(output_label))
        self.wait(0.5)

        # 'GPT' and 'ViT' icons sprouting from base (bottom center)
        # GPT icon: stylized 'G' + 'PT' using circles and lines
        gpt_icon = VGroup(
            Circle(radius=0.4, color=TEAL_A, fill_opacity=0.9).shift(LEFT * 1.5 + DOWN * 3.5),
            Text("GPT", font_size=28, weight=BOLD, font="Arial").shift(LEFT * 1.5 + DOWN * 3.5),
        )
        # ViT icon: eye-like shape (circle + inner ellipse) + "ViT"
        vit_circle = Circle(radius=0.4, color=GOLD_A, fill_opacity=0.9).shift(RIGHT * 1.5 + DOWN * 3.5)
        vit_eye = Ellipse(width=0.3, height=0.2, color=BLACK, fill_opacity=1).move_to(vit_circle.get_center())
        vit_icon = VGroup(vit_circle, vit_eye, Text("ViT", font_size=28, weight=BOLD, font="Arial").shift(RIGHT * 1.5 + DOWN * 3.5))

        # Animate sprouting: scale up from dot
        gpt_base = Dot(point=LEFT * 1.5 + DOWN * 3.5, radius=0.05)
        vit_base = Dot(point=RIGHT * 1.5 + DOWN * 3.5, radius=0.05)
        self.play(FadeIn(gpt_base), FadeIn(vit_base))
        self.play(
            gpt_base.animate.scale(0).become(gpt_icon),
            vit_base.animate.scale(0).become(vit_icon),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(1)

        # Final emphasis: pulse attention arcs and highlight GPT/ViT
        self.play(
            attention_arcs.animate.set_stroke(YELLOW_E, width=4),
            glow_arcs.animate.set_opacity(0.7),
            gpt_icon.animate.set_stroke(TEAL_C, width=3, background=True),
            vit_icon.animate.set_stroke(GOLD_C, width=3, background=True),
            run_time=1.2
        )
        self.wait(1)

        # Fade out all except title and icons
        self.play(
            FadeOut(input_tokens), FadeOut(input_label),
            FadeOut(ff_layer), FadeOut(ff_label),
            FadeOut(output_tokens), FadeOut(output_label),
            FadeOut(attention_arcs), FadeOut(glow_arcs),
        )
        self.wait(0.5)

        # Hold final frame
        self.play(
            title.animate.scale(1.1).set_color(PURPLE_E),
            gpt_icon.animate.scale(1.05),
            vit_icon.animate.scale(1.05),
            run_time=1
        )
        self.wait(1)
