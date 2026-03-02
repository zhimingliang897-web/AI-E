from manim import *

class PromptConstraint(Scene):
    def construct(self):
        # Create a stylized 2D "3D cartoon" bell curve using filled shapes
        # Since true 3D is forbidden, we simulate depth with layered curves and shading
        x_range = [-4, 4, 0.1]
        axes = Axes(
            x_range=x_range,
            y_range=[0, 2.5, 0.5],
            axis_config={"include_numbers": False, "color": GREY_C},
            y_length=4,
            x_length=8,
        ).set_z_index(-1)

        # Base bell curve (Gaussian-like)
        def gaussian(x):
            return 2 * np.exp(-0.3 * x**2)

        curve_base = axes.plot(gaussian, color=BLUE, stroke_width=3)
        curve_fill = axes.get_area(curve_base, x_range=[-4, 4], color=BLUE, opacity=0.2)

        # Add subtle "3D cartoon" effect: lighter top curve + shadow-like lower curve
        curve_top = axes.plot(lambda x: gaussian(x) + 0.1, color=BLUE_E, stroke_width=1.5)
        curve_shadow = axes.plot(lambda x: gaussian(x) - 0.08, color=GREY_C, stroke_width=1).set_z_index(-1)

        bell_group = VGroup(curve_shadow, curve_fill, curve_base, curve_top)

        # Spotlight beam: downward-converging trapezoid (narrowing from top to base)
        spotlight_top = Line(axes.c2p(-3.5, 2.2), axes.c2p(3.5, 2.2), color=YELLOW, stroke_width=2)
        spotlight_bottom = Line(axes.c2p(-0.8, 0.1), axes.c2p(0.8, 0.1), color=YELLOW, stroke_width=2)
        spotlight_left = Line(spotlight_top.get_left(), spotlight_bottom.get_left(), color=YELLOW, stroke_width=2)
        spotlight_right = Line(spotlight_top.get_right(), spotlight_bottom.get_right(), color=YELLOW, stroke_width=2)
        spotlight = VGroup(spotlight_top, spotlight_bottom, spotlight_left, spotlight_right)
        spotlight.set_stroke(opacity=0.7)

        # 'Prompt' text above the spotlight
        prompt_text = Text("Prompt", font_size=48, weight=BOLD, color=WHITE)
        prompt_text.next_to(spotlight_top, UP, buff=0.8)

        # Animate: show bell, then spotlight narrows (shrink width of bottom lines), then 'Prompt' appears
        self.play(
            Create(axes),
            FadeIn(curve_fill),
            Create(curve_base),
            Create(curve_top),
            Create(curve_shadow),
            run_time=1.5
        )
        self.wait(0.5)

        # Spotlight appears fully wide
        self.play(FadeIn(spotlight), run_time=1)
        self.wait(0.5)

        # Spotlight narrows: animate bottom endpoints moving inward
        narrow_target_left = axes.c2p(-0.3, 0.1)
        narrow_target_right = axes.c2p(0.3, 0.1)
        self.play(
            spotlight_bottom.animate.put_start_and_end_on(narrow_target_left, narrow_target_right),
            spotlight_left.animate.put_start_and_end_on(spotlight_top.get_left(), narrow_target_left),
            spotlight_right.animate.put_start_and_end_on(spotlight_top.get_right(), narrow_target_right),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=2
        )
        self.wait(0.5)

        # 'Prompt' fades in with glow effect (simulated via scaling + color shift)
        prompt_glow = prompt_text.copy().scale(1.05).set_color(PURPLE_A).set_opacity(0.6)
        self.play(
            FadeIn(prompt_glow, scale=1.2),
            FadeIn(prompt_text, scale=0.95),
            run_time=1.2
        )
        self.wait(0.5)

        # Optional: subtle gradient fill update on bell — recolor fill with blue-to-purple linear gradient
        # Since Manim CE doesn’t support per-mobject gradients directly in this context,
        # we approximate by fading to a purple-tinted version
        curve_fill_target = axes.get_area(curve_base, x_range=[-4, 4], color=PURPLE, opacity=0.3)
        self.play(
            Transform(curve_fill, curve_fill_target),
            curve_base.animate.set_color(PURPLE),
            curve_top.animate.set_color(PURPLE_E),
            run_time=1.5
        )
        self.wait(1)
