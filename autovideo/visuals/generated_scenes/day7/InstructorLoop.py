from manim import *

class InstructorLoop(Scene):
    def construct(self):
        # Define positions in a horizontal loop
        llm_output = Text("LLM Output", font_size=24).shift(LEFT * 4)
        pydantic_check = Text("Pydantic Check", font_size=24).shift(UP * 2)
        error_feedback = Text("Error Feedback", font_size=24).shift(RIGHT * 4)
        llm_regenerate = Text("LLM Regenerate", font_size=24).shift(DOWN * 2)

        # Success checkmark near Pydantic Check
        checkmark = Text("✅", font_size=36, color=GREEN).next_to(pydantic_check, UP, buff=0.5)

        # Arrows (green, thick)
        arrow1 = Arrow(llm_output.get_right(), pydantic_check.get_bottom(), buff=0.2, color=GREEN, stroke_width=4)
        arrow2 = Arrow(pydantic_check.get_right(), error_feedback.get_left(), buff=0.2, color=GREEN, stroke_width=4)
        arrow3 = Arrow(error_feedback.get_bottom(), llm_regenerate.get_right(), buff=0.2, color=GREEN, stroke_width=4)
        arrow4 = Arrow(llm_regenerate.get_left(), llm_output.get_bottom(), buff=0.2, color=GREEN, stroke_width=4)

        # Group all elements
        loop_group = VGroup(
            llm_output, pydantic_check, error_feedback, llm_regenerate,
            checkmark, arrow1, arrow2, arrow3, arrow4
        )

        # Animate step-by-step
        self.play(FadeIn(llm_output), run_time=0.8)
        self.wait(0.5)
        self.play(Create(arrow1), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(pydantic_check), FadeIn(checkmark), run_time=0.8)
        self.wait(0.5)
        self.play(Create(arrow2), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(error_feedback), run_time=0.8)
        self.wait(0.5)
        self.play(Create(arrow3), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(llm_regenerate), run_time=0.8)
        self.wait(0.5)
        self.play(Create(arrow4), run_time=0.8)
        self.wait(1)

        # Emphasize the loop with a gentle pulse
        self.play(
            loop_group.animate.scale(1.03).set_color(GREEN),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(1)
