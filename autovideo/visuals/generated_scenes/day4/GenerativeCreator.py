from manim import *

class GenerativeCreator(Scene):
    def construct(self):
        # 1. Create Data Representation (Cloud of Dots)
        data_dots = VGroup()
        for _ in range(50):
            dot = Dot(radius=0.05, color=BLUE_E)
            dot.shift(LEFT * 3 + UP * 2)
            dot.shift(RIGHT * np.random.uniform(0, 2) + DOWN * np.random.uniform(0, 2))
            data_dots.add(dot)
        data_dots.arrange_in_grid(rows=5, cols=10, buff=0.15)
        data_dots.move_to(LEFT * 3)

        # 2. Create Equation P(X) using Text (No MathTex allowed)
        equation = Text("P(X)", font="Consolas", weight=BOLD, color=YELLOW)
        equation.scale(1.5)
        equation.move_to(UP * 2)
        
        # Glow effect for equation
        glow_circle = Circle(radius=1.2, color=YELLOW, stroke_opacity=0.3)
        glow_circle.move_to(equation)
        glow_circle.set_z_index(-1)

        # 3. Create Robot (Geometric Shapes)
        robot_body = Rectangle(height=1.5, width=1, color=GREY_B, fill_opacity=0.5)
        robot_body.set_fill(GREY_B, opacity=0.5)
        robot_head = Circle(radius=0.4, color=GREY_A)
        robot_head.next_to(robot_body, UP, buff=0)
        robot_arm = Line(start=robot_body.get_right(), end=robot_body.get_right() + RIGHT * 1.5, color=GREY_C)
        robot_arm.move_arc_center_to(robot_body.get_right())
        robot = VGroup(robot_body, robot_head, robot_arm)
        robot.move_to(RIGHT * 3)

        # 4. Create Cat Art (Geometric Shapes)
        cat_head = Circle(radius=0.6, color=WHITE)
        cat_ear_l = Triangle(color=WHITE).scale(0.3).next_to(cat_head, UP, buff=0).shift(LEFT * 0.4)
        cat_ear_r = Triangle(color=WHITE).scale(0.3).next_to(cat_head, UP, buff=0).shift(RIGHT * 0.4)
        cat_body = Ellipse(width=1.2, height=1.6, color=WHITE).next_to(cat_head, DOWN, buff=0)
        cat_art = VGroup(cat_body, cat_head, cat_ear_l, cat_ear_r)
        cat_art.move_to(LEFT * 3)
        cat_art.set_opacity(0) # Initially hidden

        # --- Animation Sequence ---

        # Step 1: Show Data
        self.play(FadeIn(data_dots), run_time=1.5)
        self.wait(0.5)

        # Step 2: Show Equation Glowing
        self.play(Create(equation), Create(glow_circle), run_time=1)
        self.play(glow_circle.animate.scale(1.2).set_opacity(0.1), run_time=0.5)
        self.play(glow_circle.animate.scale(0.8).set_opacity(0.5), run_time=0.5)
        self.wait(0.5)

        # Step 3: Show Robot
        self.play(Create(robot), run_time=1)
        self.wait(0.5)

        # Step 4: Robot Paints (Arm Movement)
        self.play(robot_arm.animate.rotate(-PI / 3, about_point=robot_body.get_right()), run_time=1)
        self.play(robot_arm.animate.rotate(PI / 3, about_point=robot_body.get_right()), run_time=1)
        self.wait(0.5)

        # Step 5: Transform Data into Art
        # Fade out data, Fade in Cat Art
        self.play(
            FadeOut(data_dots),
            FadeIn(cat_art),
            equation.animate.set_color(WHITE),
            run_time=2
        )
        
        # Final Highlight
        self.play(cat_art.animate.set_color(YELLOW), run_time=0.5)
        self.play(cat_art.animate.set_color(WHITE), run_time=0.5)
        
        self.wait(1)
