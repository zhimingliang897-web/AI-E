from manim import *

class HumanAIBridge(Scene):
    def construct(self):
        # Soft focus background: subtle gradient circle
        bg = Circle(radius=10, fill_color=GREY_C, fill_opacity=0.05, stroke_width=0)
        bg.set_z_index(-1)

        # Human figure (simplified 2D cartoon style)
        human_body = Rectangle(height=2.0, width=0.6, fill_color=TEAL_A, fill_opacity=1, stroke_width=0)
        human_head = Circle(radius=0.4, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
        human_head.move_to(human_body.get_top() + UP * 0.4)
        human = VGroup(human_body, human_head)
        human.shift(LEFT * 3)

        # Speech bubble
        bubble_tail = Polygon(
            [-0.2, -0.3, 0], [0.2, -0.3, 0], [0.0, -0.6, 0],
            fill_color=WHITE, fill_opacity=1, stroke_width=1, stroke_color=GREY_C
        )
        bubble = Circle(radius=0.8, fill_color=WHITE, fill_opacity=1, stroke_width=1, stroke_color=GREY_C)
        bubble.next_to(human, RIGHT, buff=0.3)
        bubble_tail.next_to(bubble, DOWN, buff=0)
        speech_bubble = VGroup(bubble, bubble_tail)
        speech_text = Text("Hello!", font_size=24, color=BLACK).move_to(bubble.get_center())

        # AI robot figure (stylized)
        robot_body = Rectangle(height=2.2, width=0.7, fill_color=BLUE, fill_opacity=1, stroke_width=0)
        robot_head = Square(side_length=0.6, fill_color=GREY_C, fill_opacity=1, stroke_width=0)
        robot_head.move_to(robot_body.get_top() + UP * 0.3)
        # Robot eyes
        eye_left = Circle(radius=0.08, fill_color=RED, fill_opacity=1, stroke_width=0).move_to(robot_head.get_center() + LEFT * 0.15 + UP * 0.05)
        eye_right = Circle(radius=0.08, fill_color=RED, fill_opacity=1, stroke_width=0).move_to(robot_head.get_center() + RIGHT * 0.15 + UP * 0.05)
        robot = VGroup(robot_body, robot_head, eye_left, eye_right)
        robot.shift(RIGHT * 3)

        # Text input box
        input_box = RoundedRectangle(corner_radius=0.1, height=0.6, width=1.8, fill_color=GREY_C, fill_opacity=0.8, stroke_width=1, stroke_color=GREY_C)
        input_box.next_to(robot, LEFT, buff=0.3)
        cursor = Rectangle(height=0.4, width=0.1, fill_color=RED, fill_opacity=1, stroke_width=0).move_to(input_box.get_center())
        input_text = Text("type here...", font_size=20, color=GREY_E).move_to(input_box.get_center())

        # Glowing bridge: flowing words along a curved path
        bridge_arc = ArcBetweenPoints(
            speech_bubble.get_right(),
            input_box.get_left(),
            angle=-PI/4,
            stroke_width=8,
            stroke_color=PURPLE_E
        )
        bridge_arc.set_z_index(-1)

        # Flowing words — animate text moving along arc
        words = ["data", "learn", "think", "adapt", "connect", "evolve"]
        word_mobjects = []
        for i, word in enumerate(words):
            w = Text(word, font_size=22, color=WHITE, weight=BOLD)
            # Position along arc using proportional parameter
            prop = i / (len(words) - 1) if len(words) > 1 else 0.5
            point = bridge_arc.point_at_proportion(prop)
            w.move_to(point + UP * 0.3)
            w.rotate(bridge_arc.get_angle_at_proportion(prop) + PI/2, about_point=point)
            word_mobjects.append(w)

        word_group = VGroup(*word_mobjects)

        # Add all elements
        self.add(bg)
        self.play(
            Create(human),
            Create(robot),
            Create(speech_bubble),
            Write(speech_text),
            Create(input_box),
            Write(input_text),
            FadeIn(cursor),
            run_time=2
        )
        self.wait(0.5)

        # Animate glowing bridge arc
        self.play(
            Create(bridge_arc),
            run_time=2,
            rate_func=smooth
        )
        self.wait(0.5)

        # Animate words flowing along bridge
        self.play(
            word_group.animate.shift(DOWN * 0.05).set_opacity(0.9),
            run_time=0.3
        )
        self.play(
            word_group.animate.shift(DOWN * 0.05).set_opacity(0.7),
            run_time=0.3
        )
        self.play(
            word_group.animate.shift(DOWN * 0.05).set_opacity(0.5),
            run_time=0.3
        )
        self.wait(1)

        # Subtle pulse on bridge
        self.play(
            bridge_arc.animate.set_stroke(width=10, color=PURPLE_A),
            run_time=1.2,
            rate_func=smooth
        )
        self.wait(1)
