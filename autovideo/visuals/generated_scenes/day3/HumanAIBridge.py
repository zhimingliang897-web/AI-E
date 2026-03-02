from manim import *

class HumanAIBridge(Scene):
    def construct(self):
        # Background: soft gradient-like blur effect using large semi-transparent shapes
        bg_circle1 = Circle(radius=8, color=GREY_C, fill_opacity=0.05).set_z_index(-1)
        bg_circle2 = Circle(radius=6, color=TEAL_A, fill_opacity=0.03).move_to(UP * 1.5).set_z_index(-1)
        self.add(bg_circle1, bg_circle2)

        # --- Human figure (left) ---
        # Head
        human_head = Circle(radius=0.7, color=RED, fill_opacity=1, stroke_width=0)
        # Body (simple torso + arms)
        human_torso = Rectangle(width=0.4, height=1.2, fill_color=ORANGE, fill_opacity=1, stroke_width=0)
        human_torso.next_to(human_head, DOWN, buff=0)
        human_arms = VGroup(
            Line(ORIGIN, LEFT * 0.8, stroke_width=6, color=ORANGE),
            Line(ORIGIN, RIGHT * 0.8, stroke_width=6, color=ORANGE)
        ).rotate(PI/6).move_to(human_torso.get_top() + UP*0.1)
        human_arms[0].next_to(human_torso, LEFT, buff=0).shift(DOWN*0.2)
        human_arms[1].next_to(human_torso, RIGHT, buff=0).shift(DOWN*0.2)
        # Legs
        human_legs = VGroup(
            Rectangle(width=0.2, height=1.0, fill_color=RED, fill_opacity=1, stroke_width=0),
            Rectangle(width=0.2, height=1.0, fill_color=RED, fill_opacity=1, stroke_width=0)
        ).arrange(RIGHT, buff=0.2).next_to(human_torso, DOWN, buff=0)
        human_legs.shift(UP*0.1)
        # Speech bubble
        bubble_tail = Polygon(
            [-0.3, -0.5, 0], [0, -0.8, 0], [0.3, -0.5, 0],
            fill_color=YELLOW, fill_opacity=1, stroke_width=0
        )
        bubble_body = RoundedRectangle(corner_radius=0.2, width=2.0, height=1.0,
                                       fill_color=YELLOW, fill_opacity=1, stroke_width=0)
        bubble_body.next_to(human_torso, UP, buff=0.3).shift(LEFT*0.5)
        bubble_tail.next_to(bubble_body, DOWN, buff=0)
        speech_text = Text("Hello!", font_size=24, color=BLACK, weight=BOLD).move_to(bubble_body)
        human = VGroup(human_head, human_torso, human_arms, human_legs, bubble_body, bubble_tail, speech_text)
        human.shift(LEFT * 3.5)

        # --- AI Robot figure (right) ---
        # Head (rounded rectangle + two eye circles)
        robot_head = RoundedRectangle(corner_radius=0.3, width=1.2, height=0.9,
                                      fill_color=BLUE, fill_opacity=1, stroke_width=0)
        robot_eye_left = Circle(radius=0.12, color=WHITE, fill_opacity=1).move_to(robot_head.get_center() + LEFT*0.3 + UP*0.1)
        robot_eye_right = Circle(radius=0.12, color=WHITE, fill_opacity=1).move_to(robot_head.get_center() + RIGHT*0.3 + UP*0.1)
        robot_eye_pupil_left = Circle(radius=0.05, color=BLACK, fill_opacity=1).move_to(robot_eye_left.get_center())
        robot_eye_pupil_right = Circle(radius=0.05, color=BLACK, fill_opacity=1).move_to(robot_eye_right.get_center())
        # Torso (grid-like metallic look using lines)
        robot_torso = RoundedRectangle(corner_radius=0.2, width=0.8, height=1.3,
                                      fill_color=GREY_C, fill_opacity=1, stroke_width=0)
        grid_lines = VGroup()
        for i in range(1, 4):
            grid_lines += Line(LEFT*0.3, RIGHT*0.3, stroke_width=1, color=GREY_D).shift(UP*(0.4 - i*0.4))
            grid_lines += Line(UP*0.3, DOWN*0.3, stroke_width=1, color=GREY_D).shift(RIGHT*(0.2 - i*0.2))
        # Arms (mechanical, angled)
        robot_arm_left = Rectangle(width=0.1, height=0.9, fill_color=BLUE, fill_opacity=1, stroke_width=0).rotate(-PI/5)
        robot_arm_right = Rectangle(width=0.1, height=0.9, fill_color=BLUE, fill_opacity=1, stroke_width=0).rotate(PI/5)
        robot_arm_left.next_to(robot_torso, LEFT, buff=0).shift(UP*0.2)
        robot_arm_right.next_to(robot_torso, RIGHT, buff=0).shift(UP*0.2)
        # Legs (two vertical rectangles)
        robot_legs = VGroup(
            Rectangle(width=0.2, height=1.0, fill_color=BLUE, fill_opacity=1, stroke_width=0),
            Rectangle(width=0.2, height=1.0, fill_color=BLUE, fill_opacity=1, stroke_width=0)
        ).arrange(RIGHT, buff=0.3).next_to(robot_torso, DOWN, buff=0)
        # Input box (floating in front of robot)
        input_box = RoundedRectangle(corner_radius=0.1, width=2.2, height=0.6,
                                    fill_color=WHITE, fill_opacity=1, stroke_width=2, stroke_color=GREY_B)
        input_box.next_to(robot_torso, UP, buff=0.5).shift(RIGHT*0.2)
        cursor = Rectangle(width=0.1, height=0.4, fill_color=BLUE, fill_opacity=1).move_to(input_box.get_left() + RIGHT*0.3)
        input_text = Text("Type here...", font_size=20, color=GREY_D).move_to(input_box)
        robot = VGroup(
            robot_head, robot_eye_left, robot_eye_right, robot_eye_pupil_left, robot_eye_pupil_right,
            robot_torso, grid_lines, robot_arm_left, robot_arm_right, robot_legs,
            input_box, cursor, input_text
        )
        robot.shift(RIGHT * 3.5)

        # --- Glowing bridge of flowing words ---
        # Words to animate across the bridge
        words = ["Data", "Learn", "Reason", "Adapt", "Collaborate", "Grow"]
        word_mobjects = VGroup(*[
            Text(word, font_size=28, color=WHITE, weight=BOLD)
            .set_stroke(color=PURPLE_E, width=1, opacity=0.8)
            for word in words
        ])
        
        # Bridge path: curved upward arc between human and robot
        bridge_start = human.get_right() + RIGHT * 0.3
        bridge_end = robot.get_left() + LEFT * 0.3
        bridge_arc = ArcBetweenPoints(bridge_start, bridge_end, angle=PI/4, stroke_width=6)
        bridge_arc.set_color_by_gradient(PURPLE_A, BLUE, TEAL_A)
        bridge_arc.set_opacity(0.8)

        # Animate words flowing along the arc
        word_animations = []
        for i, word in enumerate(word_mobjects):
            # Position word at start of arc
            word.move_to(bridge_start)
            # Animate along arc path
            word_animations.append(
                word.animate.move_to(bridge_end).set_rate_func(rate_functions.ease_in_out_sine)
                .set_run_time(4 + i * 0.8)
            )

        # Add all elements
        self.play(
            FadeIn(human, shift=LEFT*2, scale=0.8),
            FadeIn(robot, shift=RIGHT*2, scale=0.8),
            Create(bridge_arc),
            run_time=2
        )
        self.wait(0.5)

        # Flow words one by one with stagger
        self.play(LaggedStart(*word_animations, lag_ratio=0.3), run_time=6)
        self.wait(1)

        # Subtle pulse on bridge
        self.play(
            bridge_arc.animate.set_stroke(opacity=1).set_color_by_gradient(PURPLE_E, BLUE, TEAL_E),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(1)
