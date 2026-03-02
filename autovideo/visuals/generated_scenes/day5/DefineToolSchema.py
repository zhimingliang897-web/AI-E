from manim import *

class DefineToolSchema(Scene):
    def construct(self):
        # Title
        title = Text("JSON Schema Structure", weight=BOLD, font_size=36)
        title.to_edge(UP)

        # Define lines with specific highlighting for 'name', 'description', 'parameters'
        # Format: List of tuples (text_content, color)
        schema_lines_data = [
            [("{", WHITE)],
            [('  "', WHITE), ('name', GREEN), ('": "get_weather",', WHITE)],
            [('  "', WHITE), ('description', GREEN), ('": "Get current weather",', WHITE)],
            [('  "', WHITE), ('parameters', GREEN), (': {', WHITE)],
            [('    "type": "object",', WHITE)],
            [('    "properties": {', WHITE)],
            [('      "location": {"type": "string"}', WHITE)],
            [('    }', WHITE)],
            [('  }', WHITE)],
            [("}", WHITE)],
        ]

        lines_group = VGroup()
        for line_data in schema_lines_data:
            line_parts = VGroup()
            for text_content, color in line_data:
                # Use Monospace font for code-like appearance
                part = Text(text_content, font="Monospace", font_size=24, color=color)
                line_parts.add(part)
            # Arrange parts horizontally with no buffer to form a line
            line_parts.arrange(RIGHT, buff=0, aligned_edge=DOWN)
            lines_group.add(line_parts)

        # Arrange lines vertically
        lines_group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        lines_group.next_to(title, DOWN, buff=1)

        # Background Rectangle
        bg = Rectangle(
            width=lines_group.width + 1,
            height=lines_group.height + 1,
            color=GREY_E,
            fill_opacity=0.5
        )
        bg.set_z_index(-1)
        bg.move_to(lines_group)

        # Animations
        self.play(Write(title), rate_func=smooth)
        self.wait(0.5)
        
        self.play(Create(bg), rate_func=smooth)
        self.wait(0.5)

        # Type out lines one by one
        for line in lines_group:
            self.play(Write(line), rate_func=smooth)
            self.wait(0.2)

        self.wait(1)
