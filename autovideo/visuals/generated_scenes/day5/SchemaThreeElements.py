from manim import *

class SchemaThreeElements(Scene):
    def construct(self):
        # Configuration
        box_width = 4.0
        box_height = 1.0
        box_color = BLUE
        text_color = WHITE
        check_color = GREEN

        # Create Boxes
        box1 = RoundedRectangle(width=box_width, height=box_height, color=box_color, corner_radius=0.2)
        box2 = RoundedRectangle(width=box_width, height=box_height, color=box_color, corner_radius=0.2)
        box3 = RoundedRectangle(width=box_width, height=box_height, color=box_color, corner_radius=0.2)

        # Create Text Labels
        label1 = Text("Type", weight=BOLD, color=text_color)
        label2 = Text("Description", weight=BOLD, color=text_color)
        label3 = Text("Required", weight=BOLD, color=text_color)

        # Create Checkmarks using Lines (Primitive shapes)
        def create_checkmark():
            line1 = Line(LEFT * 0.2 + UP * 0.1, ORIGIN, color=check_color, stroke_width=8)
            line2 = Line(ORIGIN, RIGHT * 0.4 + UP * 0.4, color=check_color, stroke_width=8)
            return VGroup(line1, line2)

        check1 = create_checkmark()
        check2 = create_checkmark()
        check3 = create_checkmark()

        # Assemble Groups
        # Place labels inside boxes
        label1.move_to(box1.get_center())
        label2.move_to(box2.get_center())
        label3.move_to(box3.get_center())

        # Place checkmarks to the right of boxes
        check1.next_to(box1, RIGHT, buff=0.5)
        check2.next_to(box2, RIGHT, buff=0.5)
        check3.next_to(box3, RIGHT, buff=0.5)

        group1 = VGroup(box1, label1, check1)
        group2 = VGroup(box2, label2, check2)
        group3 = VGroup(box3, label3, check3)

        # Arrange vertically
        all_groups = VGroup(group1, group2, group3)
        all_groups.arrange(DOWN, buff=0.5)
        all_groups.move_to(ORIGIN)

        # Animations
        self.play(Create(box1), Write(label1), Create(check1), run_time=1.5)
        self.wait(0.5)
        self.play(Create(box2), Write(label2), Create(check2), run_time=1.5)
        self.wait(0.5)
        self.play(Create(box3), Write(label3), Create(check3), run_time=1.5)
        self.wait(1)
