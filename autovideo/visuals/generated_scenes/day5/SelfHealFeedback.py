from manim import *

class SelfHealFeedback(Scene):
    def construct(self):
        # Background elements (subtle)
        bg_circle = Circle(radius=6, color=GREY_C, stroke_width=0.5).set_opacity(0.1)
        self.add(bg_circle)

        # LLM node (central brain-like shape)
        llm_body = Circle(radius=1.2, color=BLUE, fill_opacity=0.15)
        llm_core = Circle(radius=0.3, color=BLUE, fill_opacity=1)
        llm_spokes = VGroup(*[
            Line(llm_core.get_center(), llm_body.point_at_angle(angle))
            for angle in [0, PI/3, 2*PI/3, PI, -2*PI/3, -PI/3]
        ]).set_stroke(BLUE, width=1, opacity=0.4)
        llm = VGroup(llm_body, llm_core, llm_spokes).shift(UP * 0.5)

        # Input text (user query)
        user_query = Text("Get weather forecast", font_size=24, color=WHITE)
        user_query_arrow = Arrow(
            start=user_query.get_bottom() + DOWN * 0.3,
            end=llm.get_top() + DOWN * 0.2,
            buff=0,
            stroke_width=2).set_color(YELLOW)

        # Error bubble (red, with exclamation)
        error_bubble = RoundedRectangle(
            corner_radius=0.2,
            width=5.2,
            height=1.4,
            fill_color=RED,
            fill_opacity=0.9,
            stroke_color=RED_E,
            stroke_width=1.5
        )
        exclamation = Text("!", font_size=36, color=WHITE, weight=BOLD)
        exclamation.move_to(error_bubble.get_center() + LEFT * 1.8)
        error_text = Text(
            "Missing required parameter: city",
            font_size=22,
            color=WHITE,
            line_spacing=1.3
        )
        error_text.move_to(error_bubble.get_center() + RIGHT * 0.2)

        error_group = VGroup(error_bubble, exclamation, error_text)

        # Position error below LLM
        error_group.next_to(llm, DOWN, buff=1.0)

        # Feedback arrow (curved back to LLM)
        feedback_arrow = CurvedArrow(error_group.get_top(), llm.get_bottom() + UP * 0.1,
            angle=-PI/3,
            stroke_width=2,
            tip_length=0.15
        ).set_color(PURPLE)

        # "Self-heal" label near arrow
        heal_label = Text("Self-heal feedback", font_size=20, color=PURPLE).next_to(feedback_arrow, RIGHT, buff=0.2)

        # Animate sequence
        self.play(Write(user_query), run_time=1)
        self.wait(0.5)
        self.play(GrowArrow(user_query_arrow), run_time=1)
        self.wait(0.5)
        self.play(Create(llm), run_time=1.2)
        self.wait(0.5)
        self.play(FadeIn(error_group, shift=UP * 0.3), run_time=1.2)
        self.wait(1)
        self.play(Create(feedback_arrow), Write(heal_label), run_time=1.5)
        self.wait(1.5)

        # Subtle pulse on LLM to indicate processing
        self.play(
            llm_body.animate.set_fill(opacity=0.25),
            llm_core.animate.scale(1.15),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(1)
