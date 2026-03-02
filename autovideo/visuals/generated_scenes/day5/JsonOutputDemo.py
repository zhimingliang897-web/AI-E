from manim import *

class JsonOutputDemo(Scene):
    def construct(self):
        # Create a rounded rectangle as the output box
        box = RoundedRectangle(
            corner_radius=0.2,
            width=8,
            height=3,
            fill_color=GREY_C,
            fill_opacity=0.15,
            stroke_color=GREY_C,
            stroke_width=2
        )

        # Create JSON text with proper indentation and syntax coloring
        json_text = Text(
            '{\n  "name": "get_weather",\n  "arguments": {\n    "city": "Beijing"\n  }\n}',
            font="Monospace",
            font_size=24,
            color=WHITE
        )

        # Position text inside box
        json_text.move_to(box.get_center())

        # Add subtle highlight to curly braces and quotes for visual clarity
        # We'll recreate key parts with color emphasis
        lines = [
            Text("{", font="Monospace", font_size=24, color=TEAL_A),
            Text('"name": "get_weather",', font="Monospace", font_size=24, color=WHITE),
            Text('"arguments": {', font="Monospace", font_size=24, color=WHITE),
            Text('"city": "Beijing"', font="Monospace", font_size=24, color=WHITE),
            Text("}", font="Monospace", font_size=24, color=TEAL_A),
            Text("}", font="Monospace", font_size=24, color=TEAL_A),
        ]

        # Manually position each line for alignment
        lines[0].move_to(box.get_top() + DOWN * 0.5 + LEFT * 3.5)
        lines[1].next_to(lines[0], DOWN, aligned_edge=LEFT, buff=0.2)
        lines[2].next_to(lines[1], DOWN, aligned_edge=LEFT, buff=0.2)
        lines[3].next_to(lines[2], DOWN, aligned_edge=LEFT, buff=0.2).shift(RIGHT * 0.5)
        lines[4].next_to(lines[3], DOWN, aligned_edge=LEFT, buff=0.2).shift(LEFT * 0.5)
        lines[5].next_to(lines[4], DOWN, aligned_edge=LEFT, buff=0.2).shift(LEFT * 0.5)

        # Group all lines
        colored_json = VGroup(*lines)

        # Assemble scene
        self.play(Create(box), run_time=1.2)
        self.wait(0.5)
        self.play(FadeIn(colored_json), run_time=1.5)
        self.wait(2)

        # Optional: highlight the function name
        name_highlight = SurroundingRectangle(
            lines[1][9:22],  # "get_weather" substring
            color=YELLOW,
            buff=0.05,
            corner_radius=0.05,
            stroke_width=1.5
        )
        self.play(Create(name_highlight), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(name_highlight))

        # Optional: highlight city value
        city_highlight = SurroundingRectangle(
            lines[3][10:17],  # "Beijing"
            color=BLUE,
            buff=0.05,
            corner_radius=0.05,
            stroke_width=1.5
        )
        self.play(Create(city_highlight), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(city_highlight))

        self.wait(1)
