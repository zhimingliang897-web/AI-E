from manim import *

class FSMForJson(Scene):
    def construct(self):
        # Define colors
        NODE_COLOR = BLUE
        ARROW_COLOR = GREEN
        LABEL_COLOR = WHITE
        BLOCK_COLOR = RED

        # Create states as circles with labels
        key_node = Circle(color=NODE_COLOR, radius=0.6).shift(LEFT * 3)
        key_label = Text("Key:", font_size=24, color=LABEL_COLOR).move_to(key_node.get_center())

        # Next states: three nodes arranged vertically on the right
        brace_node = Circle(color=NODE_COLOR, radius=0.6).shift(RIGHT * 2 + UP * 2)
        bracket_node = Circle(color=NODE_COLOR, radius=0.6).shift(RIGHT * 2 + DOWN * 0.5)
        quote_node = Circle(color=NODE_COLOR, radius=0.6).shift(RIGHT * 2 + DOWN * 3)

        brace_label = Text("{", font_size=24, color=LABEL_COLOR).move_to(brace_node.get_center())
        bracket_label = Text("[", font_size=24, color=LABEL_COLOR).move_to(bracket_node.get_center())
        quote_label = Text('"', font_size=24, color=LABEL_COLOR).move_to(quote_node.get_center())

        # Block state (red X) — placed below all
        block_node = Cross(stroke_color=BLOCK_COLOR, stroke_width=8, scale_factor=0.8).shift(DOWN * 5)

        # Arrows from 'Key:' to valid next states
        arrow_brace = Arrow(start=key_node.get_right(), end=brace_node.get_left(), buff=0.2, color=ARROW_COLOR, stroke_width=3)
        arrow_bracket = Arrow(start=key_node.get_right(), end=bracket_node.get_left(), buff=0.2, color=ARROW_COLOR, stroke_width=3)
        arrow_quote = Arrow(start=key_node.get_right(), end=quote_node.get_left(), buff=0.2, color=ARROW_COLOR, stroke_width=3)

        # Labels on arrows
        label_brace = Text("{", font_size=20, color=LABEL_COLOR).next_to(arrow_brace, UP, buff=0.1)
        label_bracket = Text("[", font_size=20, color=LABEL_COLOR).next_to(arrow_bracket, RIGHT, buff=0.1)
        label_quote = Text('"', font_size=20, color=LABEL_COLOR).next_to(arrow_quote, DOWN, buff=0.1)

        # "All other characters" blocked arrow: from key_node down to red X
        arrow_block = Arrow(
            start=key_node.get_bottom(),
            end=block_node.get_top(),
            buff=0.2,
            color=BLOCK_COLOR,
            stroke_width=3,
            tip_length=0.2
        )
        label_block = Text("other", font_size=20, color=BLOCK_COLOR).next_to(arrow_block, RIGHT, buff=0.1)

        # Group all elements for easier handling
        fsm_group = VGroup(
            key_node, key_label,
            brace_node, brace_label,
            bracket_node, bracket_label,
            quote_node, quote_label,
            block_node,
            arrow_brace, label_brace,
            arrow_bracket, label_bracket,
            arrow_quote, label_quote,
            arrow_block, label_block
        )

        # Animate construction
        self.play(Create(key_node), Write(key_label))
        self.wait(0.5)
        self.play(
            Create(brace_node), Write(brace_label),
            Create(bracket_node), Write(bracket_label),
            Create(quote_node), Write(quote_label),
            Create(block_node),
            Create(arrow_brace), Write(label_brace),
            Create(arrow_bracket), Write(label_bracket),
            Create(arrow_quote), Write(label_quote),
            Create(arrow_block), Write(label_block)
        )
        self.wait(2)

        # Highlight valid transitions briefly
        self.play(
            brace_node.animate.set_stroke(color=YELLOW, width=4),
            run_time=0.5
        )
        self.play(
            brace_node.animate.set_stroke(color=NODE_COLOR, width=3),
            bracket_node.animate.set_stroke(color=YELLOW, width=4),
            run_time=0.5
        )
        self.play(
            bracket_node.animate.set_stroke(color=NODE_COLOR, width=3),
            quote_node.animate.set_stroke(color=YELLOW, width=4),
            run_time=0.5
        )
        self.play(
            quote_node.animate.set_stroke(color=NODE_COLOR, width=3),
            run_time=0.5
        )
        self.wait(1)
