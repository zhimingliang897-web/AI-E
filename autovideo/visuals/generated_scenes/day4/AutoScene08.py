from manim import *

class AutoScene08(Scene):
    def construct(self):
        # Since true 3D surface plots and 3D particles are forbidden (no ThreeDScene, no Sphere, no ImageMobject),
        # we create a stylized 2D representation: a shaded contour-like surface using layered polygons,
        # and glowing 'X' markers animated upward from high-density regions.

        # Axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 2.5, 0.5],
            axis_config={"color": GREY_C, "stroke_width": 1},
            x_length=10,
            y_length=6,
        ).set_z_index(-1)

        # Approximate Gaussian mixture density curve P(X) — a smooth, multi-peaked function
        def p_x(x):
            return (
                0.8 * np.exp(-0.5 * (x + 1.5)**2) +
                1.2 * np.exp(-0.7 * x**2) +
                0.6 * np.exp(-0.4 * (x - 1.8)**2)
            )

        # Graph of P(X)
        graph = axes.plot(p_x, x_range=[-3, 3], color=BLUE, stroke_width=3)

        # Fill under curve with semi-transparent blue gradient effect (layered polygons)
        fill_points = [
            *[axes.c2p(x, p_x(x)) for x in np.linspace(-3, 3, 60)],
            axes.c2p(3, 0),
            axes.c2p(-3, 0)
        ]
        fill = Polygon(*fill_points, fill_color=BLUE, fill_opacity=0.2, stroke_width=0).set_z_index(-1)

        # Highlight peaks with subtle glow circles (using Annulus + Circle combo)
        peak_x_coords = [-1.5, 0.0, 1.8]
        glow_circles = VGroup()
        for px in peak_x_coords:
            glow = Annulus(inner_radius=0.05, outer_radius=0.3, fill_color=TEAL_A, fill_opacity=0.4, stroke_width=0)
            glow.move_to(axes.c2p(px, p_x(px)))
            glow.set_z_index(-2)
            glow_circles.add(glow)

        # Create 'X' markers — simple cross glyphs made from two thin rectangles
        def make_x_marker(size=0.3, color=YELLOW):
            h = Rectangle(width=size, height=size/5, fill_color=color, fill_opacity=1, stroke_width=0)
            v = Rectangle(width=size/5, height=size, fill_color=color, fill_opacity=1, stroke_width=0)
            x = VGroup(h, v).rotate(PI/4, about_point=ORIGIN)
            x.set_stroke(color, width=0)
            return x

        # Initial X particles — placed at base (y=0), below peaks
        x_particles = VGroup()
        for px in peak_x_coords:
            x_mark = make_x_marker(0.25, YELLOW_E)
            x_mark.move_to(axes.c2p(px, 0))
            x_mark.set_z_index(1)
            x_particles.add(x_mark)

        # Animate: draw axes, fill, graph, glows, then lift X particles upward along density curve
        self.play(
            Create(axes),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(
            DrawBorderThenFill(fill),
            run_time=1.5
        )
        self.play(
            Create(graph),
            run_time=1.5
        )
        self.play(
            FadeIn(glow_circles, scale=0.8),
            run_time=1.2
        )
        self.wait(0.8)

        # Animate X particles rising to peak heights with slight glow pulse
        anims = []
        for i, (px, x_mark) in enumerate(zip(peak_x_coords, x_particles)):
            target_y = p_x(px)
            anims.append(x_mark.animate.move_to(axes.c2p(px, target_y)).scale(1.3).set_color(YELLOW))
        
        self.play(
            LaggedStart(*anims, lag_ratio=0.3),
            run_time=2.5
        )

        # Add subtle pulsing glow to X's
        self.play(
            x_particles.animate.set_color(YELLOW_D).scale(0.9),
            rate_func=smooth,
            run_time=1.8
        )

        self.wait(1)
