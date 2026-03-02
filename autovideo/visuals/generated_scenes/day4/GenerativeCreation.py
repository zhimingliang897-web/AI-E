from manim import *

class GenerativeCreation(Scene):
    def construct(self):
        # Bright Colorful Background
        bg = Rectangle(width=50, height=50, color=BLUE, fill_opacity=1)
        bg.set_z_index(-1)
        self.add(bg)

        # Magical Robot (Abstract representation using primitives)
        head = Circle(radius=0.5, color=GREY_A, fill_opacity=1)
        body = RoundedRectangle(height=1.2, width=0.8, corner_radius=0.2, color=GREY_A, fill_opacity=1)
        body.next_to(head, DOWN, buff=0)
        left_arm = Line(start=body.get_left() + LEFT * 0.4, end=body.get_left() + LEFT * 0.8, color=GREY_A)
        right_arm = Line(start=body.get_right() + RIGHT * 0.4, end=body.get_right() + RIGHT * 0.8, color=GREY_A)
        eye_left = Dot(color=BLUE_E, radius=0.1).move_to(head.get_center() + LEFT * 0.2)
        eye_right = Dot(color=BLUE_E, radius=0.1).move_to(head.get_center() + RIGHT * 0.2)
        
        robot = VGroup(head, body, left_arm, right_arm, eye_left, eye_right)
        robot.move_to(ORIGIN)

        # Swirling Data Particles
        particles = VGroup()
        for i in range(12):
            p = Dot(color=YELLOW, radius=0.15)
            p.shift(RIGHT * 2)
            p.rotate(i * (360 / 12) * DEGREES, about_point=ORIGIN)
            particles.add(p)

        # Formula P(X)
        formula = Text("P(X)", font_size=48, weight=BOLD, color=WHITE)
        formula.next_to(robot, UP, buff=0.5)

        # Generated Images (Abstract Shapes)
        shape1 = RegularPolygon(n=5, color=GREEN, fill_opacity=0.8)
        shape2 = RegularPolygon(n=6, color=RED, fill_opacity=0.8)
        shape3 = Circle(color=PURPLE, fill_opacity=0.8)
        generated_art = VGroup(shape1, shape2, shape3)
        generated_art.arrange(RIGHT, buff=0.5)
        generated_art.next_to(robot, DOWN, buff=0.5)
        generated_art.scale(0.5)

        # Animations
        self.play(FadeIn(robot), run_time=1.5)
        self.wait(0.5)
        
        self.play(
            Rotate(particles, angle=2 * TAU, about_point=robot.get_center()),
            FadeIn(formula),
            run_time=2,
            rate_func=smooth
        )
        self.wait(0.5)

        self.play(
            FadeOut(particles),
            FadeIn(generated_art),
            formula.animate.scale(1.2).set_color(GREEN),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)
