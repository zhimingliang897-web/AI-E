from manim import *

class PromptConstraint(Scene):
    def construct(self):
        # Create a stylized 2D "3D cartoon" bell curve using filled shapes
        # Since true 3D is forbidden, we simulate depth with layered curves and shading
        x_range = [-4, 4, 0.1]
        axes = Axes(
            x_range=x_range,
            y_range=[0, 2.5, 0.5],
            axis_config={"include_ticks": False, "color": GREY_C},
            tips=False
        ).set_z_index(-1)

        # Base bell curve (Gaussian-like)
        def gaussian(x):
            return 2 * np.exp(-0.3 * x**2)

        curve = axes.plot(gaussian, color=BLUE, stroke_width=3)
        curve_fill = axes.get_area(curve, x_range=[-4, 4], opacity=0.4, color=BLUE)

        # Add subtle "3D cartoon" effect: duplicate curve slightly offset + lighter fill
        curve_top = axes.plot(gaussian, color=BLUE_E, stroke_width=2).shift(UP * 0.1)
        curve_fill_top = axes.get_area(curve_top, x_range=[-4, 4], opacity=0.2, color=BLUE_A)

        # Group base distribution
        dist_group = VGroup(curve_fill, curve_fill_top, curve, curve_top)

        # Spotlight beam: narrowing cone (two converging lines + gradient fade)
        spotlight_width_start = 6.0
        spotlight_width_end = 1.2
        beam_height = 2.5

        # Left and right spotlight boundaries (as lines)
        left_line = Line(
            start=axes.c2p(-spotlight_width_start/2, 0),
            end=axes.c2p(-spotlight_width_end/2, beam_height),
            color=YELLOW,
            stroke_width=1.5,
            stroke_opacity=0.7
        )
        right_line = Line(
            start=axes.c2p(spotlight_width_start/2, 0),
            end=axes.c2p(spotlight_width_end/2, beam_height),
            color=YELLOW,
            stroke_width=1.5,
            stroke_opacity=0.7
        )

        # Gradient spotlight fill (using polygon with transparency gradient)
        spotlight_points = [
            axes.c2p(-spotlight_width_start/2, 0),
            axes.c2p(spotlight_width_start/2, 0),
            axes.c2p(spotlight_width_end/2, beam_height),
            axes.c2p(-spotlight_width_end/2, beam_height),
        ]
        spotlight_fill = Polygon(*spotlight_points, fill_opacity=0.25, fill_color=YELLOW, stroke_width=0)

        # "Prompt" text above the beam
        prompt_text = Text("Prompt", font_size=48, weight=BOLD, color=WHITE)
        prompt_text.next_to(spotlight_fill, UP, buff=0.5)

        # Animate: show distribution, then spotlight narrows, then "Prompt" appears
        self.play(
            Create(axes),
            FadeIn(curve_fill),
            Create(curve),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(
            FadeIn(curve_fill_top),
            Create(curve_top),
            run_time=1
        )
        self.wait(0.5)

        # Animate spotlight narrowing: scale width from wide to narrow over time
        self.play(
            Transform(
                VGroup(left_line, right_line, spotlight_fill),
                VGroup(
                    Line(
                        start=axes.c2p(-spotlight_width_end/2, 0),
                        end=axes.c2p(-spotlight_width_end/2, beam_height),
                        color=YELLOW,
                        stroke_width=1.5,
                        stroke_opacity=0.7
                    ),
                    Line(
                        start=axes.c2p(spotlight_width_end/2, 0),
                        end=axes.c2p(spotlight_width_end/2, beam_height),
                        color=YELLOW,
                        stroke_width=1.5,
                        stroke_opacity=0.7
                    ),
                    Polygon(
                        axes.c2p(-spotlight_width_end/2, 0),
                        axes.c2p(spotlight_width_end/2, 0),
                        axes.c2p(spotlight_width_end/2, beam_height),
                        axes.c2p(-spotlight_width_end/2, beam_height),
                        fill_opacity=0.25,
                        fill_color=YELLOW,
                        stroke_width=0
                    )
                ),
                run_time=2,
                rate_func=smooth
            )
        )
        self.wait(0.5)

        # Animate "Prompt" fading in with gentle scale-up
        self.play(
            FadeIn(prompt_text, shift=DOWN * 0.3, scale=0.8),
            run_time=1.2
        )
        self.wait(0.5)

        # Optional: subtle color shift on distribution — blue → purple gradient
        # We'll animate curve and fill colors toward purple
        self.play(
            curve.animate.set_color(PURPLE),
            curve_top.animate.set_color(PURPLE_E),
            curve_fill.animate.set_fill(color=BLUE_A, opacity=0.35),
            curve_fill_top.animate.set_fill(color=PURPLE_A, opacity=0.25),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(1)
