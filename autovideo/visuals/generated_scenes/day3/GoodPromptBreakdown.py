from manim import *

class GoodPromptBreakdown(Scene):
    def construct(self):
        # Robot (simplified 2D icon using circles and rectangles)
        robot_head = Circle(radius=0.6, color=GREY_C, fill_opacity=1)
        robot_body = Rectangle(width=1.2, height=1.6, color=GREY_C, fill_opacity=1)
        robot_body.next_to(robot_head, DOWN, buff=0)
        robot_eye_left = Circle(radius=0.15, color=BLUE, fill_opacity=1).shift(LEFT * 0.25 + UP * 0.15)
        robot_eye_right = Circle(radius=0.15, color=BLUE, fill_opacity=1).shift(RIGHT * 0.25 + UP * 0.15)
        robot_mouth = Arc(start_angle=0, angle=PI, radius=0.25, color=TEAL_A).shift(DOWN * 0.2)
        robot = VGroup(robot_head, robot_body, robot_eye_left, robot_eye_right, robot_mouth)
        robot.shift(LEFT * 3.5)

        # Checklist items (Text)
        checklist_items = [
            "Role: Sci-Fi Writer",
            "Style: Concise",
            "Topic: Lying Robot",
            "Length: 300 words",
            "Twist Ending"
        ]
        
        # Create checklist as VGroup with spacing
        checklist = VGroup()
        for i, item in enumerate(checklist_items):
            text = Text(item, font_size=24, color=WHITE)
            checkmark = Text("✓", font_size=32, color=GREEN, weight=BOLD)
            item_group = VGroup(checkmark, text).arrange(RIGHT, buff=0.3)
            item_group.shift(DOWN * i * 0.9)
            checklist.add(item_group)
        
        checklist.move_to(RIGHT * 2.5)

        # Animate robot fade in
        self.play(FadeIn(robot), run_time=1.2)
        self.wait(0.5)

        # Animate checklist items one by one with checkmarks
        for item_group in checklist:
            self.play(FadeIn(item_group), run_time=0.8)
            self.wait(0.4)

        self.wait(2)
