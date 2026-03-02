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
        
        # Create checklist with green checkmarks
        checklist = VGroup()
        for i, item in enumerate(checklist_items):
            checkmark = Text("✓", color=GREEN, font_size=36)
            text = Text(item, font_size=28, color=WHITE)
            item_group = VGroup(checkmark, text).arrange(RIGHT, buff=0.3)
            item_group.shift(DOWN * i * 1.1)
            checklist.add(item_group)
        
        checklist.shift(RIGHT * 2.5)

        # Title
        title = Text("Good Prompt Breakdown", font_size=36, weight=BOLD, color=YELLOW)
        title.to_edge(UP, buff=0.5)

        # Animate
        self.play(FadeIn(robot), run_time=1.5)
        self.wait(0.5)
        self.play(Write(title))
        self.wait(0.5)
        self.play(LaggedStart(*[FadeIn(item, shift=RIGHT * 0.5) for item in checklist], lag_ratio=0.3))
        self.wait(2)

        # Optional subtle pulse on checkmarks
        self.play(
            *[checkmark.animate.scale(1.2).set_color(GREEN_E) for checkmark in checklist.submobjects],
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(1)
