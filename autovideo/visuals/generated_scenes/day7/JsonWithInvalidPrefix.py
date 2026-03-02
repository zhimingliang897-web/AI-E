from manim import *

class JsonWithInvalidPrefix(Scene):
    def construct(self):
        # Clean JSON block (valid ASCII-only)
        json_text = Text(
            '{\n  "name": "Alice",\n  "age": 30,\n  "city": "New York"\n}',
            font="Monospace",
            font_size=24
        )
        json_text.to_edge(DOWN, buff=1.5)

        # "OK" text above JSON
        ok_text = Text("OK", color=GREEN, font_size=36, weight=BOLD)
        ok_text.next_to(json_text, UP, buff=0.8)

        self.play(Write(ok_text), Write(json_text))
        self.wait(1)

        # Introduce invalid prefix: add Chinese punctuation to the start of the JSON string
        # We'll reconstruct the text with illegal chars highlighted
        invalid_json_str = '（{\n  "name": "Alice",\n  "age": 30,\n  "city": "New York"\n}。'
        
        # Split into parts for highlighting
        parts = []
        for char in invalid_json_str:
            if char in "（。":
                t = Text(char, color=RED, font="Monospace", font_size=24)
            else:
                t = Text(char, color=WHITE, font="Monospace", font_size=24)
            parts.append(t)
        
        invalid_json = VGroup(*parts).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        invalid_json.move_to(json_text.get_center())
        invalid_json.align_to(json_text, LEFT)

        # Fade out original JSON and OK, fade in invalid version
        self.play(
            FadeOut(ok_text),
            FadeOut(json_text),
            FadeIn(invalid_json),
            run_time=1.2
        )
        self.wait(0.5)

        # Add red "X" overlay over entire JSON block
        x_width = invalid_json.width * 1.2
        x_height = invalid_json.height * 1.2
        x_rect = Rectangle(
            width=x_width,
            height=x_height,
            stroke_color=RED,
            stroke_width=8,
            fill_opacity=0,
        )
        x_rect.move_to(invalid_json.get_center())

        # Draw X: two crossing lines
        top_left = x_rect.get_corner(UL)
        bottom_right = x_rect.get_corner(DR)
        top_right = x_rect.get_corner(UR)
        bottom_left = x_rect.get_corner(DL)

        line1 = Line(top_left, bottom_right, color=RED, stroke_width=8)
        line2 = Line(top_right, bottom_left, color=RED, stroke_width=8)

        self.play(
            Create(line1),
            Create(line2),
            run_time=1.0
        )
        self.wait(1)

        # Optional: emphasize illegal chars with pulses
        illegal_chars = [p for p in parts if p.get_color() == RED]
        for char in illegal_chars:
            self.play(
                char.animate.scale(1.4).set_color(RED_E),
                rate_func=smooth,
                run_time=0.8
            )
        self.wait(1)
