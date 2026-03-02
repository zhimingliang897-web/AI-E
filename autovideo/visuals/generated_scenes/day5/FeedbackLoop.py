from manim import *

class FeedbackLoop(Scene):
    def construct(self):
        # Define positions for three nodes on a circle
        center = ORIGIN
        radius = 3.0
        angle_offset = PI / 6  # slight rotation for visual balance

        # Positions: top, bottom-right, bottom-left (equally spaced)
        p1 = center + radius * rotate_vector(RIGHT, PI/2 + angle_offset)      # top
        p2 = center + radius * rotate_vector(RIGHT, -PI/6 + angle_offset)     # bottom-right
        p3 = center + radius * rotate_vector(RIGHT, -5*PI/6 + angle_offset)   # bottom-left

        # Create nodes as rounded rectangles
        node1 = RoundedRectangle(height=1.0, width=3.0, corner_radius=0.2, fill_color=BLUE, fill_opacity=0.2, stroke_color=BLUE)
        node2 = RoundedRectangle(height=1.0, width=3.0, corner_radius=0.2, fill_color=GREEN, fill_opacity=0.2, stroke_color=GREEN)
        node3 = RoundedRectangle(height=1.0, width=3.0, corner_radius=0.2, fill_color=PURPLE, fill_opacity=0.2, stroke_color=PURPLE)

        # Label nodes
        label1 = Text("AI thinks", font_size=24, color=BLUE).move_to(p1)
        label2 = Text("System runs", font_size=24, color=GREEN).move_to(p2)
        label3 = Text("AI summarizes", font_size=24, color=PURPLE).move_to(p3)

        # Group nodes with labels
        node1_group = VGroup(node1, label1).move_to(p1)
        node2_group = VGroup(node2, label2).move_to(p2)
        node3_group = VGroup(node3, label3).move_to(p3)

        # Arrows between nodes
        arrow1 = Arrow(p1, p2, buff=0.3, stroke_width=3, color=GREY_C)
        arrow2 = Arrow(p2, p3, buff=0.3, stroke_width=3, color=GREY_C)
        arrow3 = Arrow(p3, p1, buff=0.3, stroke_width=3, color=GREY_C)

        # Add all elements
        self.play(
            Create(node1_group),
            Create(node2_group),
            Create(node3_group),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            GrowArrow(arrow1),
            GrowArrow(arrow2),
            GrowArrow(arrow3),
            run_time=2
        )
        self.wait(1)

        # Optional: highlight flow with animated dots or pulses
        dot1 = Dot(p1, color=BLUE, radius=0.08)
        dot2 = Dot(p2, color=GREEN, radius=0.08)
        dot3 = Dot(p3, color=PURPLE, radius=0.08)

        self.play(FadeIn(dot1), FadeIn(dot2), FadeIn(dot3), run_time=0.8)
        self.wait(0.5)

        # Animate flow along arrows
        path1 = VMobject().set_points_as_corners([p1, p2])
        path2 = VMobject().set_points_as_corners([p2, p3])
        path3 = VMobject().set_points_as_corners([p3, p1])

        self.play(
            MoveAlongPath(dot1, path1, rate_func=linear, run_time=1.2),
            MoveAlongPath(dot2, path2, rate_func=linear, run_time=1.2),
            MoveAlongPath(dot3, path3, rate_func=linear, run_time=1.2),
        )
        self.wait(1)

        # Final emphasis: pulse all nodes
        self.play(
            node1_group.animate.scale(1.05).set_fill(opacity=0.4),
            node2_group.animate.scale(1.05).set_fill(opacity=0.4),
            node3_group.animate.scale(1.05).set_fill(opacity=0.4),
            run_time=0.6
        )
        self.play(
            node1_group.animate.scale(1/1.05).set_fill(opacity=0.2),
            node2_group.animate.scale(1/1.05).set_fill(opacity=0.2),
            node3_group.animate.scale(1/1.05).set_fill(opacity=0.2),
            run_time=0.6
        )
        self.wait(1)
