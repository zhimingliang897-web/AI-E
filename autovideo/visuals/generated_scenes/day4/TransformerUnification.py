from manim import *

class TransformerUnification(Scene):
    def construct(self):
        # Title
        title = Text("Transformer Unification", font_size=36, weight=BOLD)
        subtitle = Text("One Architecture, Three Domains", font_size=24, color=GREY_C)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.3)
        title_group.to_edge(UP, buff=0.5)
        self.play(Write(title_group))
        self.wait(1)

        # Input tokens (left)
        input_label = Text("Input Tokens", font_size=20).to_edge(LEFT, buff=1.2)
        input_tokens = VGroup(*[
            Rectangle(width=0.6, height=0.4, fill_color=BLUE, fill_opacity=0.8, stroke_width=1)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.2).next_to(input_label, DOWN, buff=0.5)
        for i, t in enumerate(input_tokens):
            t.add(Text(str(i+1), font_size=14, color=WHITE).move_to(t.get_center()))
        self.play(FadeIn(input_label), Create(input_tokens))
        self.wait(0.5)

        # Self-attention heatmap (center-left)
        attn_label = Text("Self-Attention\nHeatmap", font_size=20).next_to(input_tokens, RIGHT, buff=1.5)
        heatmap = VGroup()
        n = 5
        for i in range(n):
            row = VGroup()
            for j in range(n):
                alpha = 0.2 + 0.8 * (i == j or abs(i - j) == 1)
                cell = Square(side_length=0.3, fill_color=TEAL_A, fill_opacity=alpha, stroke_width=0.5)
                row.add(cell)
            row.arrange(RIGHT, buff=0)
            heatmap.add(row)
        heatmap.arrange(DOWN, buff=0)
        heatmap.next_to(attn_label, DOWN, buff=0.5)
        self.play(FadeIn(attn_label), Create(heatmap))
        self.wait(0.5)

        # Feed-forward layers (center-right)
        ff_label = Text("Feed-Forward\nLayers", font_size=20).next_to(heatmap, RIGHT, buff=1.5)
        ff_layers = VGroup(
            RoundedRectangle(height=0.8, width=0.6, corner_radius=0.1, fill_color=YELLOW, fill_opacity=0.7, stroke_width=1),
            RoundedRectangle(height=0.8, width=0.6, corner_radius=0.1, fill_color=YELLOW, fill_opacity=0.7, stroke_width=1),
        ).arrange(DOWN, buff=0.3).next_to(ff_label, DOWN, buff=0.5)
        self.play(FadeIn(ff_label), Create(ff_layers))
        self.wait(0.5)

        # Output tokens (right)
        output_label = Text("Output Tokens", font_size=20).to_edge(RIGHT, buff=1.2)
        output_tokens = VGroup(*[
            Rectangle(width=0.6, height=0.4, fill_color=PURPLE, fill_opacity=0.8, stroke_width=1)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.2).next_to(output_label, DOWN, buff=0.5)
        for i, t in enumerate(output_tokens):
            t.add(Text(str(i+1), font_size=14, color=WHITE).move_to(t.get_center()))
        self.play(FadeIn(output_label), Create(output_tokens))
        self.wait(0.5)

        # Arrows between stages
        arrow1 = Arrow(input_tokens.get_right(), heatmap.get_left(), buff=0.1, stroke_width=2)
        arrow2 = Arrow(heatmap.get_right(), ff_layers.get_left(), buff=0.1, stroke_width=2)
        arrow3 = Arrow(ff_layers.get_right(), output_tokens.get_left(), buff=0.1, stroke_width=2)
        self.play(GrowArrow(arrow1), GrowArrow(arrow2), GrowArrow(arrow3))
        self.wait(1)

        # Domain branches (below main flow)
        domains = [
            ("GPT", "Text", BLUE),
            ("ViT", "Vision", GREEN),
            ("Fusion", "Multimodal", PURPLE_E)
        ]
        domain_labels = VGroup()
        domain_icons = VGroup()
        for i, (name, desc, col) in enumerate(domains):
            label = Text(f"{name}\n{desc}", font_size=18, color=col).shift(DOWN * 2.5 + LEFT * 4 + RIGHT * i * 3.5)
            domain_labels.add(label)

            # Simple icon: circle + letter
            icon = Circle(radius=0.4, fill_color=col, fill_opacity=0.2, stroke_color=col, stroke_width=2)
            letter = Text(name[0], font_size=24, color=col, weight=BOLD).move_to(icon.get_center())
            icon_group = VGroup(icon, letter).next_to(label, DOWN, buff=0.5)
            domain_icons.add(icon_group)

        self.play(FadeIn(domain_labels), FadeIn(domain_icons))
        self.wait(1)

        # Branching arrows from output tokens to domains
        branch_arrows = VGroup()
        for i, domain_icon in enumerate(domain_icons):
            start = output_tokens[-1].get_bottom()
            end = domain_icon.get_top()
            if i == 0:
                end += LEFT * 0.3
            elif i == 2:
                end += RIGHT * 0.3
            arrow = CurvedArrow(start, end, angle=-PI/3 if i==0 else PI/3 if i==2 else 0,
                                stroke_width=1.5, tip_length=0.15, stroke_color=GREY_C)
            branch_arrows.add(arrow)

        self.play(Create(branch_arrows))
        self.wait(1)

        # Highlight unified architecture
        unified_rect = RoundedRectangle(
            height=3.5, width=12, corner_radius=0.4,
            stroke_color=WHITE, stroke_width=2, fill_opacity=0,
            z_index=-1
        ).move_to(ORIGIN).shift(DOWN * 0.5)
        unified_text = Text("Unified Architecture", font_size=28, color=WHITE, weight=BOLD)
        unified_text.next_to(unified_rect, UP, buff=0.3)

        self.play(Create(unified_rect), Write(unified_text))
        self.wait(2)

        # Fade out all except unified frame and text
        everything = VGroup(
            title_group, input_label, input_tokens, attn_label, heatmap,
            ff_label, ff_layers, output_label, output_tokens,
            arrow1, arrow2, arrow3, domain_labels, domain_icons, branch_arrows
        )
        self.play(FadeOut(everything))
        self.wait(1)
