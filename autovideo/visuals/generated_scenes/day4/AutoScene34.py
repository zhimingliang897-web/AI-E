from manim import *

class AutoScene34(Scene):
    def construct(self):
        # Set up coordinate plane
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.2},
            axis_config={"color": GREY_C, "stroke_width": 1}
        )
        
        # Latent space label
        title = Text("Latent Space", font_size=28, color=WHITE).to_edge(UP)
        
        # Diffusion steps: jagged path (discrete approximations)
        jagged_points = [
            np.array([-3.0, -2.0, 0]),
            np.array([-1.8, -1.2, 0]),
            np.array([-0.5, 0.3, 0]),
            np.array([0.7, 0.9, 0]),
            np.array([2.0, 0.2, 0]),
            np.array([3.0, -1.5, 0])
        ]
        jagged_path = VGroup()
        for i in range(len(jagged_points) - 1):
            line = Line(jagged_points[i], jagged_points[i+1], color=RED, stroke_width=2)
            jagged_path.add(line)
        
        # Smooth flow path: cubic Bezier curve through same endpoints with control points
        smooth_path = CubicBezier(
            jagged_points[0],
            jagged_points[0] + np.array([1.0, 1.5, 0]),
            jagged_points[-1] + np.array([-1.0, 1.0, 0]),
            jagged_points[-1]
        )
        smooth_path.set_color(BLUE).set_stroke(width=4)
        
        # Dots at start and end
        start_dot = Dot(jagged_points[0], color=YELLOW, radius=0.12)
        end_dot = Dot(jagged_points[-1], color=GREEN, radius=0.12)
        
        # Labels for paths
        jagged_label = Text("Diffusion Steps", font_size=24, color=RED).next_to(jagged_path, DOWN, buff=0.3)
        smooth_label = Text("Flow Trajectory", font_size=24, color=BLUE).next_to(smooth_path, UP, buff=0.3)
        
        # Animate
        self.add(plane, title)
        self.wait(0.5)
        
        self.play(Create(jagged_path), Write(jagged_label), run_time=2)
        self.play(FadeIn(start_dot), FadeIn(end_dot))
        self.wait(1)
        
        self.play(
            Transform(jagged_path, smooth_path),
            Transform(jagged_label, smooth_label),
            start_dot.animate.set_color(BLUE),
            end_dot.animate.set_color(BLUE),
            run_time=3,
            rate_func=smooth
        )
        self.wait(1)
        
        # Emphasize smoothness with a moving dot along curve
        moving_dot = Dot(color=PURPLE_A, radius=0.1)
        moving_dot.move_to(smooth_path.get_start())
        
        self.play(
            MoveAlongPath(moving_dot, smooth_path, rate_func=smooth),
            run_time=4
        )
        self.wait(1)
