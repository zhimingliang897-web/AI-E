from manim import *

class DiscriminativeClassifier(Scene):
    def construct(self):
        # Equation P(Y|X) using Text instead of Tex/MathTex
        equation = Text("P(Y|X)", weight=BOLD, font_size=48, color=YELLOW)
        equation.to_edge(UP)

        # Bins
        bin_cat = RoundedRectangle(corner_radius=0.2, height=1.5, width=2, color=BLUE)
        label_cat = Text("Cat", font_size=24, color=WHITE)
        label_cat.move_to(bin_cat.get_center())
        bin_cat_group = VGroup(bin_cat, label_cat)
        bin_cat_group.shift(LEFT * 3 + DOWN * 2)

        bin_dog = RoundedRectangle(corner_radius=0.2, height=1.5, width=2, color=GREEN)
        label_dog = Text("Dog", font_size=24, color=WHITE)
        label_dog.move_to(bin_dog.get_center())
        bin_dog_group = VGroup(bin_dog, label_dog)
        bin_dog_group.shift(RIGHT * 3 + DOWN * 2)

        # Robot (Simple shapes)
        robot_body = Rectangle(height=1.5, width=1, color=GREY_C)
        robot_head = Circle(radius=0.4, color=GREY_C)
        robot_head.next_to(robot_body, UP, buff=0)
        robot_arm = Line(start=robot_body.get_right(), end=robot_body.get_right() + RIGHT * 0.8, color=GREY_C)
        robot = VGroup(robot_body, robot_head, robot_arm)
        robot.move_to(DOWN * 0.5)

        # Input Image (Represented as a card)
        input_card = Rectangle(height=0.8, width=0.6, color=WHITE, fill_opacity=1)
        input_icon = Circle(radius=0.2, color=BLACK)
        input_icon.move_to(input_card.get_center())
        input_data = VGroup(input_card, input_icon)
        input_data.move_to(LEFT * 3 + DOWN * 0.5)

        # Animation Sequence
        # 1. Show Equation
        self.play(Write(equation), run_time=1)
        self.wait(0.3)

        # 2. Show Bins
        self.play(Create(bin_cat_group), Create(bin_dog_group), run_time=1)
        self.wait(0.3)

        # 3. Show Robot and Input
        self.play(Create(robot), Create(input_data), run_time=1)
        self.wait(0.3)

        # 4. Robot picks up input
        self.play(input_data.animate.move_to(robot_arm.get_end()), run_time=0.8)
        self.wait(0.2)

        # 5. Robot moves to Cat Bin
        self.play(
            robot.animate.move_to(bin_cat_group.get_center() + UP * 1),
            input_data.animate.move_to(bin_cat_group.get_center() + UP * 0.5),
            run_time=1
        )
        self.wait(0.2)

        # 6. Drop input into Cat Bin
        self.play(input_data.animate.move_to(bin_cat_group.get_center()), run_time=0.5)
        self.wait(0.3)

        # 7. Highlight Equation to show P(Y|X) logic
        self.play(equation.animate.set_color(GREEN), run_time=0.8)
        self.wait(0.5)
