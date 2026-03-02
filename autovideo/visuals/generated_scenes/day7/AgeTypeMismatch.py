from manim import *

class AgeTypeMismatch(Scene):
    def construct(self):
        # Title
        title = Text("Age Type Mismatch", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Left side: incorrect JSON
        left_label = Text("Incorrect", color=RED, font_size=28)
        left_label.next_to(title, DOWN, buff=0.5).align_to(title, LEFT)

        # JSON text with 'age': '二十五岁' — highlight the string value in red
        left_json_lines = [
            Text("{", font="Consolas", font_size=24),
            Text('  "name": "张三",', font="Consolas", font_size=24),
            Text('  "age": "二十五岁",', font="Consolas", font_size=24),
            Text("}", font="Consolas", font_size=24),
        ]
        left_json = VGroup(*left_json_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        left_json.next_to(left_label, DOWN, buff=0.5)

        # Highlight the problematic line
        age_line_wrong = left_json_lines[2]
        warning_symbol = Text("⚠", color=RED, font_size=28)
        warning_symbol.next_to(age_line_wrong, RIGHT, buff=0.2)

        # Right side: correct JSON
        right_label = Text("Correct", color=GREEN, font_size=28)
        right_label.next_to(title, DOWN, buff=0.5).align_to(title, RIGHT)

        right_json_lines = [
            Text("{", font="Consolas", font_size=24),
            Text('  "name": "张三",', font="Consolas", font_size=24),
            Text('  "age": 25,', font="Consolas", font_size=24),
            Text("}", font="Consolas", font_size=24),
        ]
        right_json = VGroup(*right_json_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        right_json.next_to(right_label, DOWN, buff=0.5)

        # Green check mark next to correct age line
        age_line_correct = right_json_lines[2]
        check_symbol = Text("✓", color=GREEN, font_size=28)
        check_symbol.next_to(age_line_correct, RIGHT, buff=0.2)

        # Group elements for layout
        left_group = VGroup(left_label, left_json, warning_symbol)
        right_group = VGroup(right_label, right_json, check_symbol)
        full_group = VGroup(left_group, right_group).arrange(RIGHT, buff=2.0).move_to(ORIGIN)

        # Animate appearance
        self.play(
            FadeIn(left_group[0]),
            FadeIn(right_group[0]),
        )
        self.wait(0.5)
        self.play(
            FadeIn(left_group[1]),
            FadeIn(right_group[1]),
        )
        self.wait(0.5)
        self.play(
            FadeIn(warning_symbol),
            FadeIn(check_symbol),
        )
        self.wait(1)

        # Emphasize mismatch: draw red X over left age value, green check over right
        # Extract positions for overlays
        wrong_age_text = age_line_wrong.submobjects[3:]  # characters after 'age": '
        wrong_age_rect = SurroundingRectangle(VGroup(*wrong_age_text), color=RED, stroke_width=2, buff=0.05)
        wrong_age_rect.set_z_index(1)

        correct_age_text = age_line_correct.submobjects[-2:]  # digits '25'
        correct_age_rect = SurroundingRectangle(VGroup(*correct_age_text), color=GREEN, stroke_width=2, buff=0.05)
        correct_age_rect.set_z_index(1)

        self.play(Create(wrong_age_rect), run_time=0.8)
        self.wait(0.5)
        self.play(Create(correct_age_rect), run_time=0.8)
        self.wait(1)

        # Final note
        note = Text("Age must be a number, not a string", font_size=24, color=GREY_C)
        note.next_to(full_group, DOWN, buff=1.0)
        self.play(FadeIn(note))
        self.wait(2)
