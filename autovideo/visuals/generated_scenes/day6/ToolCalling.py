from manim import *

class ToolCalling(Scene):
    def construct(self):
        # Background
        self.camera.background_color = "#1a1a1a"

        # Robot body (simplified 3D cartoon style using layered shapes)
        robot_body = RoundedRectangle(height=3, width=2, corner_radius=0.3, fill_color=GREY_C, fill_opacity=1, stroke_width=0)
        robot_head = Circle(radius=0.8, color=GREY_C, fill_color=GREY_C, fill_opacity=1, stroke_width=0)
        robot_head.shift(UP * 1.5)
        robot = VGroup(robot_body, robot_head)

        # Eyes (glowing blue)
        eye_left = Circle(radius=0.15, color=BLUE, fill_color=BLUE, fill_opacity=0.9, stroke_width=0)
        eye_right = eye_left.copy()
        eye_left.shift(UP * 0.2 + LEFT * 0.3)
        eye_right.shift(UP * 0.2 + RIGHT * 0.3)
        robot.add(eye_left, eye_right)

        # Antenna (small curved line with dot)
        antenna_base = Line(ORIGIN, UP * 0.4, stroke_width=4, color=GREY_C).move_to(robot_head.get_top() + DOWN * 0.1)
        antenna_curve = ArcBetweenPoints(
            start=antenna_base.get_end(),
            end=antenna_base.get_end() + UR * 0.6,
            angle=-PI/3,
            stroke_width=2,
            color=GREY_C
        )
        antenna_tip = Dot(point=antenna_curve.get_end(), radius=0.07, color=YELLOW, fill_opacity=1)
        robot.add(antenna_base, antenna_curve, antenna_tip)

        # Button (slightly beveled look with highlight)
        button = RoundedRectangle(height=0.8, width=2.2, corner_radius=0.2, fill_color=BLUE, fill_opacity=0.95, stroke_width=0)
        button_highlight = RoundedRectangle(height=0.3, width=1.8, corner_radius=0.15, fill_color=WHITE, fill_opacity=0.3, stroke_width=0)
        button_highlight.move_to(button.get_top() + DOWN * 0.15)
        button_group = VGroup(button, button_highlight)
        button_label = Text("API CALL", font_size=24, weight=BOLD, color=WHITE)
        button_group.add(button_label)
        button_group.shift(DOWN * 1.2)

        # Robot arm (simple articulated arm ending in a finger pointing)
        arm_base = Line(
            start=robot_body.get_bottom() + LEFT * 0.4,
            end=robot_body.get_bottom() + LEFT * 0.4 + DOWN * 0.5 + LEFT * 0.3,
            stroke_width=6,
            color=GREY_C
        )
        forearm = Line(
            start=arm_base.get_end(),
            end=arm_base.get_end() + DOWN * 0.7 + RIGHT * 0.2,
            stroke_width=5,
            color=GREY_C
        )
        finger = Arrow(
            start=forearm.get_end(),
            end=forearm.get_end() + DOWN * 0.6,
            buff=0,
            stroke_width=3,
            color=GREY_C
        )
        arm = VGroup(arm_base, forearm, finger)

        # Position robot and button
        robot.shift(LEFT * 3)
        arm.next_to(robot_body, DOWN, buff=0).align_to(robot_body, LEFT).shift(RIGHT * 0.2)
        button_group.shift(RIGHT * 3)

        # Weather icon: sun + cloud (clean, minimal)
        sun = Circle(radius=0.3, color=YELLOW, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
        sun_rays = VGroup()
        for i in range(8):
            angle = i * PI / 4
            ray = Rectangle(width=0.06, height=0.3, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
            ray.rotate(angle).move_to(sun.get_center() + (ray.height / 2 + 0.3) * rotate(UP, angle))
            sun_rays.add(ray)
        weather_icon = VGroup(sun, sun_rays)

        # Cloud (simple overlapping circles)
        cloud_parts = VGroup(
            Circle(radius=0.25, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=0),
            Circle(radius=0.3, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=0).shift(UP * 0.15 + RIGHT * 0.2),
            Circle(radius=0.28, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=0).shift(DOWN * 0.1 + RIGHT * 0.25),
            Circle(radius=0.22, color=WHITE, fill_color=WHITE, fill_opacity=1, stroke_width=0).shift(UP * 0.1 + LEFT * 0.2),
        )
        cloud = VGroup(cloud_parts)
        weather_icon.add(cloud)
        weather_icon.scale(0.7).move_to(RIGHT * 1.5 + UP * 1.5)

        # Database icon: cylinder + grid lines
        db_base = RoundedRectangle(height=0.1, width=0.8, corner_radius=0.05, fill_color=TEAL_A, fill_opacity=1, stroke_width=0)
        db_cylinder = RoundedRectangle(height=0.6, width=0.6, corner_radius=0.15, fill_color=TEAL_A, fill_opacity=1, stroke_width=0)
        db_cylinder.align_to(db_base, DOWN)
        # Grid lines inside cylinder
        grid_lines = VGroup()
        for i in range(3):
            line = Line(
                start=db_cylinder.get_left() + UP * (0.2 * i - 0.2),
                end=db_cylinder.get_right() + UP * (0.2 * i - 0.2),
                stroke_width=1,
                color=TEAL_E
            )
            grid_lines.add(line)
        db_icon = VGroup(db_base, db_cylinder, grid_lines)
        db_icon.move_to(RIGHT * 1.5 + DOWN * 1.5)

        # Add all elements
        self.play(
            FadeIn(robot),
            FadeIn(arm),
            FadeIn(button_group),
            run_time=1.5
        )
        self.wait(0.5)

        # Press animation: finger moves to button
        self.play(
            forearm.animate.shift(DOWN * 0.4 + RIGHT * 0.1),
            finger.animate.shift(DOWN * 0.4 + RIGHT * 0.1),
            rate_func=smooth,
            run_time=1.2
        )
        self.wait(0.3)

        # Button press effect: slight scale + glow
        self.play(
            button.animate.scale(1.03).set_fill(opacity=1),
            button_highlight.animate.set_fill(opacity=0.5),
            run_time=0.4
        )
        self.play(
            button.animate.scale(0.97).set_fill(opacity=0.95),
            button_highlight.animate.set_fill(opacity=0.3),
            run_time=0.4
        )
        self.wait(0.5)

        # Reveal icons with gentle pop-in
        self.play(
            FadeIn(weather_icon, shift=DOWN * 0.3, scale=0.8),
            FadeIn(db_icon, shift=UP * 0.3, scale=0.8),
            run_time=1.2
        )
        self.wait(1)

        # Subtle pulse on icons
        self.play(
            weather_icon.animate.scale(1.05).set_opacity(0.9),
            db_icon.animate.scale(1.05).set_opacity(0.9),
            run_time=0.6
        )
        self.play(
            weather_icon.animate.scale(0.95).set_opacity(1),
            db_icon.animate.scale(0.95).set_opacity(1),
            run_time=0.6
        )
        self.wait(1.5)
