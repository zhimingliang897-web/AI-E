from manim import *

class StrictValidation(Scene):
    def construct(self):
        # Create JSON lines using Text primitives
        line1 = Text('{', color=WHITE)
        line2 = Text('  "id": 1,', color=WHITE)
        line3 = Text('  "valid": false', color=WHITE)
        line4 = Text('}', color=WHITE)

        # Arrange lines into a block
        json_block = VGroup(line1, line2, line3, line4).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3
        )
        json_block.center()

        # Background rectangle for JSON block
        bg_rect = Rectangle(
            width=json_block.width + 0.5,
            height=json_block.height + 0.5,
            color=GREY,
            stroke_opacity=0.5,
            fill_opacity=0.1
        )
        bg_rect.move_to(json_block)
        bg_rect.set_z_index(-1)

        # Construct Magnifying Glass from primitives
        lens = Circle(radius=0.6, color=BLUE, stroke_width=4, fill_opacity=0)
        handle = Line(ORIGIN, DOWN * 1.0, color=GREY, stroke_width=8)
        handle.shift(DOWN * 0.6)
        mag_glass = VGroup(lens, handle)
        mag_glass.next_to(json_block, UP, buff=0.5)
        mag_glass.set_z_index(1)

        # Construct Red X from lines
        x1 = Line((UP + LEFT) * 0.4, (DOWN + RIGHT) * 0.4, color=RED, stroke_width=10)
        x2 = Line((UP + RIGHT) * 0.4, (DOWN + LEFT) * 0.4, color=RED, stroke_width=10)
        red_x = VGroup(x1, x2)
        red_x.scale(0)
        red_x.move_to(line3.get_center())
        red_x.set_z_index(2)

        # Animations
        self.play(Create(bg_rect), Write(json_block), run_time=2)
        self.wait(0.5)

        self.play(Create(mag_glass), run_time=1)
        self.wait(0.5)

        # Scan animation moving over lines
        self.play(mag_glass.animate.move_to(line1.get_center()), run_time=1)
        self.play(mag_glass.animate.move_to(line2.get_center()), run_time=1)
        self.play(mag_glass.animate.move_to(line3.get_center()), run_time=1)

        # Highlight invalid syntax
        self.play(line3.animate.set_color(RED), run_time=0.5)
        self.wait(0.5)

        # Stamp Red X
        self.play(red_x.animate.scale(1), run_time=0.5)
        self.wait(1)
