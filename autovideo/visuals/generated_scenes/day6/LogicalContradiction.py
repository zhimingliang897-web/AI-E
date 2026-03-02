from manim import *

class LogicalContradiction(Scene):
    def construct(self):
        # Background remains black (default)

        # Create two speech bubbles using ellipses and polygons for cartoon style
        # Top bubble: "A is true"
        top_bubble = VGroup()
        top_ellipse = Ellipse(width=4.0, height=1.8, color=WHITE, fill_opacity=0.05)
        top_bubble.add(top_ellipse)
        # Speech tail pointing down
        tail_points = [
            [0.5, -0.3, 0],
            [0.8, -0.8, 0],
            [0.2, -0.8, 0],
        ]
        tail = Polygon(*tail_points, color=WHITE, fill_opacity=0.05)
        top_bubble.add(tail)
        top_bubble.move_to(UP * 1.5)

        # Bottom bubble: "A is false"
        bottom_bubble = VGroup()
        bottom_ellipse = Ellipse(width=4.0, height=1.8, color=WHITE, fill_opacity=0.05)
        bottom_bubble.add(bottom_ellipse)
        # Speech tail pointing up
        tail_points2 = [
            [-0.5, 0.3, 0],
            [-0.8, 0.8, 0],
            [-0.2, 0.8, 0],
        ]
        tail2 = Polygon(*tail_points2, color=WHITE, fill_opacity=0.05)
        bottom_bubble.add(tail2)
        bottom_bubble.move_to(DOWN * 1.5)

        # Text inside bubbles
        top_text = Text("A is true", font="Comic Sans MS", color=WHITE).scale(0.7)
        top_text.move_to(top_bubble.get_center())
        bottom_text = Text("A is false", font="Comic Sans MS", color=WHITE).scale(0.7)
        bottom_text.move_to(bottom_bubble.get_center())

        # Red X connecting the two bubbles
        # Define endpoints near centers of bubbles but slightly offset for visual clarity
        x_start = top_bubble.get_bottom() + DOWN * 0.2
        x_end = bottom_bubble.get_top() + UP * 0.2
        # Draw X as two crossing lines
        line1 = Line(x_start + LEFT * 0.3, x_end + RIGHT * 0.3, color=RED, stroke_width=8)
        line2 = Line(x_start + RIGHT * 0.3, x_end + LEFT * 0.3, color=RED, stroke_width=8)

        # Assemble all elements
        self.play(
            Create(top_bubble),
            Write(top_text),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(
            Create(bottom_bubble),
            Write(bottom_text),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(
            Create(line1),
            Create(line2),
            run_time=1.0
        )
        self.wait(2)
