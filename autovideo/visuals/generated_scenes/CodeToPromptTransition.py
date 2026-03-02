from manim import *

class CodeToPromptTransition(Scene):
    def construct(self):
        # Background split
        left_rect = Rectangle(height=7, width=6, color=GREY_C, fill_opacity=0.1, stroke_width=0)
        right_rect = Rectangle(height=7, width=6, color=GREY_C, fill_opacity=0.1, stroke_width=0)
        left_rect.to_edge(LEFT, buff=0.5)
        right_rect.to_edge(RIGHT, buff=0.5)

        # Left: Code editor (Python-like)
        code_lines = [
            Text("def compute_sum(a, b):", font="Fira Code", font_size=24),
            Text("    # Compute sum of two numbers", font="Fira Code", font_size=24),
            Text("    result = a + b", font="Fira Code", font_size=24),
            Text("    return result", font="Fira Code", font_size=24),
            Text("print(compute_sum(3, 5))", font="Fira Code", font_size=24),
        ]
        code_vgroup = VGroup(*code_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        code_vgroup.move_to(left_rect.get_center())
        
        # Add line numbers and gutter
        gutter = VGroup()
        for i in range(1, 6):
            num = Text(str(i), font="Fira Code", font_size=22, color=GREY_C)
            num.next_to(code_lines[i-1], LEFT, buff=0.3)
            gutter.add(num)
        
        # Syntax coloring
        code_lines[0].set_color(BLUE)
        code_lines[2].set_color(GREEN)
        code_lines[3].set_color(GREEN)
        code_lines[4].set_color(YELLOW)
        
        # Right: Chat interface
        chat_bubble = RoundedRectangle(corner_radius=0.2, height=5.5, width=5.5, fill_color=WHITE, fill_opacity=1, stroke_width=1)
        chat_bubble.move_to(right_rect.get_center())
        
        user_prompt = Text("Hey, can you write a Python function", font="Fira Code", font_size=22)
        user_prompt2 = Text("that adds two numbers and prints the result?", font="Fira Code", font_size=22)
        user_prompt_group = VGroup(user_prompt, user_prompt2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        user_prompt_group.move_to(chat_bubble.get_top() + DOWN * 0.8)
        user_prompt_group.shift(LEFT * 0.2)
        
        # User avatar (simple circle)
        user_avatar = Circle(radius=0.3, color=TEAL_A, fill_opacity=1)
        user_avatar.next_to(user_prompt_group, LEFT, buff=0.3)
        
        # Assistant response placeholder (simplified)
        assistant_label = Text("Assistant", font="Fira Code", font_size=18, color=GREY_C)
        assistant_label.next_to(chat_bubble.get_top(), UP, buff=0.2)
        assistant_label.align_to(chat_bubble, RIGHT)
        assistant_label.shift(LEFT * 0.5)
        
        # Arrow from code to chat
        arrow_start = right_rect.get_left() + LEFT * 0.3
        arrow_end = right_rect.get_left() + RIGHT * 0.3
        transition_arrow = Arrow(
            start=arrow_start,
            end=arrow_end,
            buff=0,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.15,
            color=YELLOW
        )
        arrow_label = Text("→ Prompt Engineering", font="Fira Code", font_size=20, color=YELLOW)
        arrow_label.next_to(transition_arrow, UP, buff=0.3)

        # Assemble left side
        code_scene = VGroup(left_rect, gutter, code_vgroup)
        # Assemble right side
        chat_scene = VGroup(right_rect, chat_bubble, user_avatar, user_prompt_group, assistant_label)

        # Animation sequence
        self.play(
            DrawBorderThenFill(left_rect),
            DrawBorderThenFill(right_rect),
            run_time=1.2
        )
        self.wait(0.5)
        
        self.play(
            Write(gutter),
            Write(code_vgroup),
            run_time=2.5
        )
        self.wait(0.5)
        
        self.play(
            FadeIn(chat_bubble),
            FadeIn(user_avatar),
            Write(user_prompt_group),
            Write(assistant_label),
            run_time=2
        )
        self.wait(0.5)
        
        self.play(
            GrowArrow(transition_arrow),
            Write(arrow_label),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(1.5)
