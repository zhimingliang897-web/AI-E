from manim import *

class DiscriminativeSorting(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # Formula P(Y|X)
        formula = Text("P(Y|X)", color=BLACK, font_size=60, weight=BOLD)
        formula.to_edge(UP)

        # Bins
        cat_bin = RoundedRectangle(height=2.5, width=2.5, color=BLUE, fill_opacity=0.1, stroke_width=3)
        cat_label = Text("Cat", color=BLACK, font_size=36, weight=BOLD)
        cat_label.next_to(cat_bin, DOWN)
        cat_group = VGroup(cat_bin, cat_label)
        cat_group.move_to(LEFT * 3 + DOWN * 2)

        dog_bin = RoundedRectangle(height=2.5, width=2.5, color=GREEN, fill_opacity=0.1, stroke_width=3)
        dog_label = Text("Dog", color=BLACK, font_size=36, weight=BOLD)
        dog_label.next_to(dog_bin, DOWN)
        dog_group = VGroup(dog_bin, dog_label)
        dog_group.move_to(RIGHT * 3 + DOWN * 2)

        # Input Images (Cards)
        card1 = Rectangle(height=1, width=1, color=BLACK, fill_opacity=0.05, stroke_width=2)
        text1 = Text("Img 1", color=BLACK, font_size=24)
        text1.move_to(card1.get_center())
        card1_group = VGroup(card1, text1)
        card1_group.move_to(ORIGIN)

        card2 = Rectangle(height=1, width=1, color=BLACK, fill_opacity=0.05, stroke_width=2)
        text2 = Text("Img 2", color=BLACK, font_size=24)
        text2.move_to(card2.get_center())
        card2_group = VGroup(card2, text2)
        card2_group.next_to(card1_group, DOWN, buff=0.3)

        # Robot (Simple Geometric Assembly)
        r_head = Circle(radius=0.25, color=BLACK, fill_color=GREY, fill_opacity=0.8, stroke_width=2)
        r_body = Rectangle(height=0.6, width=0.4, color=BLACK, fill_color=GREY, fill_opacity=0.8, stroke_width=2)
        r_body.next_to(r_head, DOWN, buff=0)
        r_arm = Rectangle(height=0.1, width=0.3, color=BLACK, fill_color=GREY, fill_opacity=0.8, stroke_width=2)
        r_arm.next_to(r_body, RIGHT, buff=0).shift(UP * 0.15)
        robot = VGroup(r_head, r_body, r_arm)
        robot.move_to(LEFT * 4)

        # Animations
        self.play(Write(formula), run_time=1.5)
        self.wait(0.5)

        self.play(Create(cat_bin), Write(cat_label), Create(dog_bin), Write(dog_label), run_time=1.5)
        self.wait(0.5)

        self.play(Create(card1_group), Create(card2_group), run_time=1)
        self.wait(0.5)

        self.play(Create(robot), run_time=1)
        self.wait(0.5)

        # Sort Card 1 to Cat Bin
        self.play(robot.animate.move_to(card1_group.get_center()), run_time=0.5)
        self.wait(0.2)
        # Move robot and card together to bin
        target_pos_1 = cat_bin.get_center() + UP * 0.5
        self.play(
            card1_group.animate.move_to(target_pos_1),
            robot.animate.move_to(target_pos_1 + LEFT * 0.5),
            run_time=1.5
        )
        self.wait(0.5)

        # Return Robot to Stack
        self.play(robot.animate.move_to(LEFT * 4), run_time=1)
        self.wait(0.2)

        # Sort Card 2 to Dog Bin
        self.play(robot.animate.move_to(card2_group.get_center()), run_time=0.5)
        self.wait(0.2)
        target_pos_2 = dog_bin.get_center() + UP * 0.5
        self.play(
            card2_group.animate.move_to(target_pos_2),
            robot.animate.move_to(target_pos_2 + RIGHT * 0.5),
            run_time=1.5
        )
        self.wait(0.5)

        # Highlight Formula
        self.play(formula.animate.set_color(BLUE).scale(1.1), run_time=1)
        self.wait(1)
