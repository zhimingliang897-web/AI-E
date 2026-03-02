from manim import *

class CodeToPromptTransition(Scene):
    def construct(self):
        # Background split
        left_rect = Rectangle(height=7, width=6, fill_color=GREY_C, fill_opacity=0.1, stroke_width=0)
        right_rect = Rectangle(height=7, width=6, fill_color=GREY_C, fill_opacity=0.1, stroke_width=0)
        left_rect.to_edge(LEFT, buff=0.5)
        right_rect.to_edge(RIGHT, buff=0.5)

        # Left: Code editor (Python-like)
        code_lines = [
            Text("def calculate_sum(a, b):", font="Fira Code", font_size=24),
            Text("    # Compute sum of two numbers", font="Fira Code", font_size=24),
            Text("    result = a + b", font="Fira Code", font_size=24),
            Text("    return result", font="Fira Code", font_size=24),
        ]
        code_vgroup = VGroup(*code_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        code_vgroup.move_to(left_rect.get_center())
        # Add line numbers and gutter
        gutter = VGroup()
        for i in range(1, 5):
            num = Text(str(i), font="Fira Code", font_size=22, color=GREY_C).move_to(
                code_lines[i-1].get_left() + LEFT * 0.8
            )
            gutter.add(num)
        code_editor = VGroup(gutter, code_vgroup)
        code_title = Text("code.py", font="Fira Code", font_size=20, color=TEAL_A).next_to(left_rect.get_top(), DOWN, buff=0.2).align_to(left_rect, LEFT).shift(RIGHT*0.5)

        # Right: Chat interface
        chat_bubble = RoundedRectangle(corner_radius=0.2, height=5.5, width=5.2, fill_color=WHITE, fill_opacity=1, stroke_width=1)
        chat_bubble.move_to(right_rect.get_center())
        chat_title = Text("Chat", font="Fira Code", font_size=20, color=BLUE).next_to(right_rect.get_top(), DOWN, buff=0.2).align_to(right_rect, LEFT).shift(RIGHT*0.5)

        # Prompt message
        prompt_text = Text(
            "Explain how this function works\nand suggest improvements.",
            font="Fira Code",
            font_size=22,
            line_spacing=1.3
        ).move_to(chat_bubble.get_center() + UP * 0.5)
        prompt_bg = RoundedRectangle(
            corner_radius=0.15,
            height=prompt_text.height + 0.6,
            width=prompt_text.width + 0.8,
            fill_color=BLUE,
            fill_opacity=0.1,
            stroke_width=0.8,
            stroke_color=BLUE
        ).move_to(prompt_text.get_center())

        # User avatar placeholder (circle + initial)
        user_avatar = Circle(radius=0.3, color=BLUE, fill_opacity=0.2, stroke_width=2)
        user_initial = Text("U", font_size=20, color=BLUE, weight=BOLD).move_to(user_avatar.get_center())
        user_group = VGroup(user_avatar, user_initial).next_to(chat_bubble.get_top(), DOWN, buff=0.3).align_to(chat_bubble, RIGHT).shift(LEFT*0.5)

        # Arrow from code to chat
        arrow_start = left_rect.get_right() + LEFT * 0.2
        arrow_end = right_rect.get_left() + RIGHT * 0.2
        transition_arrow = Arrow(
            arrow_start,
            arrow_end,
            buff=0.1,
            stroke_width=4,
            color=YELLOW,
            tip_length=0.25
        )
        arrow_label = Text("→ Natural Language", font="Fira Code", font_size=18, color=YELLOW).next_to(transition_arrow, UP, buff=0.2)

        # Build scene
        self.play(
            DrawBorderThenFill(left_rect),
            DrawBorderThenFill(right_rect),
            run_time=1.2
        )
        self.wait(0.5)

        # Add code editor elements
        self.play(
            Write(code_title),
            FadeIn(gutter),
            LaggedStart(*[Write(line) for line in code_lines], lag_ratio=0.3),
            run_time=2
        )
        self.wait(0.5)

        # Add chat interface
        self.play(
            DrawBorderThenFill(chat_bubble),
            Write(chat_title),
            run_time=1
        )
        self.wait(0.3)
        self.play(
            FadeIn(prompt_bg),
            Write(prompt_text),
            run_time=1.2
        )
        self.wait(0.3)
        self.play(FadeIn(user_group), run_time=0.8)
        self.wait(0.5)

        # Animate arrow
        self.play(
            GrowArrow(transition_arrow),
            Write(arrow_label),
            run_time=1.5
        )
        self.wait(1)

        # Subtle emphasis on transformation idea
        code_glow = code_vgroup.copy().set_stroke(YELLOW, width=2, opacity=0.7).set_fill(opacity=0)
        chat_glow = VGroup(prompt_bg, prompt_text).copy().set_stroke(BLUE, width=2, opacity=0.7).set_fill(opacity=0)
        self.play(
            Create(code_glow),
            Create(chat_glow),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            FadeOut(code_glow),
            FadeOut(chat_glow),
            run_time=0.8
        )
        self.wait(1)
