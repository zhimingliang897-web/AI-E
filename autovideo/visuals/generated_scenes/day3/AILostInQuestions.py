from manim import *

class AILostInQuestions(Scene):
    def construct(self):
        # Draw cartoon AI head: simple face with eyes and a subtle smile
        head = Circle(radius=1.2, color=BLUE_E, fill_opacity=0.15)
        left_eye = Circle(radius=0.15, color=GREY_C, fill_opacity=1).shift(LEFT * 0.4 + UP * 0.2)
        right_eye = Circle(radius=0.15, color=GREY_C, fill_opacity=1).shift(RIGHT * 0.4 + UP * 0.2)
        mouth = Arc(start_angle=PI, angle=PI, radius=0.3, color=GREY_C).shift(DOWN * 0.1)

        ai_head = VGroup(head, left_eye, right_eye, mouth)

        # Position AI head in center
        ai_head.move_to(ORIGIN)

        # Question marks — slightly varied sizes and positions around the head
        q1 = Text("?", font_size=48, color=YELLOW).shift(UP * 2.5)
        q2 = Text("?", font_size=48, color=TEAL_A).shift(DOWN * 2.5)
        q3 = Text("?", font_size=48, color=PURPLE_A).shift(LEFT * 3)
        q4 = Text("?", font_size=48, color=RED).shift(RIGHT * 3)

        # Labels for each question mark
        label1 = Text("Theme?", font_size=24, color=YELLOW).next_to(q1, UP, buff=0.3)
        label2 = Text("Audience?", font_size=24, color=TEAL_A).next_to(q2, DOWN, buff=0.3)
        label3 = Text("Length?", font_size=24, color=PURPLE_A).next_to(q3, LEFT, buff=0.3)
        label4 = Text("Style?", font_size=24, color=RED).next_to(q4, RIGHT, buff=0.3)

        # Group labels with their question marks
        q_group1 = VGroup(q1, label1)
        q_group2 = VGroup(q2, label2)
        q_group3 = VGroup(q3, label3)
        q_group4 = VGroup(q4, label4)

        # Animate AI head appearing
        self.play(FadeIn(ai_head), run_time=1.2)
        self.wait(0.5)

        # Pop up question marks one by one with bounce effect
        self.play(
            FadeIn(q_group1, scale=0.5),
            rate_func=smooth,
            run_time=1.0
        )
        self.wait(0.3)
        self.play(
            FadeIn(q_group2, scale=0.5),
            rate_func=smooth,
            run_time=1.0
        )
        self.wait(0.3)
        self.play(
            FadeIn(q_group3, scale=0.5),
            rate_func=smooth,
            run_time=1.0
        )
        self.wait(0.3)
        self.play(
            FadeIn(q_group4, scale=0.5),
            rate_func=smooth,
            run_time=1.0
        )
        self.wait(1.0)

        # Add subtle confused blinking: eyes shrink & grow
        blink_anim = AnimationGroup(
            left_eye.animate.scale(0.3).set_opacity(0.3),
            right_eye.animate.scale(0.3).set_opacity(0.3),
            run_time=0.2
        )
        self.play(blink_anim)
        self.play(
            left_eye.animate.scale(1/0.3).set_opacity(1),
            right_eye.animate.scale(1/0.3).set_opacity(1),
            run_time=0.2
        )

        # Slight head tilt to enhance confusion
        self.play(
            ai_head.animate.rotate(0.08, about_point=ORIGIN),
            run_time=0.5,
            rate_func=smooth
        )

        self.wait(2)
