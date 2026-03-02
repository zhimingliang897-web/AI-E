from manim import *

class SelfHealingLoop(Scene):
    def construct(self):
        # AI Brain Representation
        brain_outer = Circle(color=PURPLE, radius=0.8, fill_opacity=0.5)
        brain_inner = Circle(color=WHITE, radius=0.3, fill_opacity=0.8)
        brain = VGroup(brain_outer, brain_inner)
        brain.to_edge(UP)

        # Error Message Box
        error_rect = Rectangle(color=RED, height=1, width=3)
        error_text = Text("Error: Invalid JSON", color=WHITE, font_size=24)
        error_group = VGroup(error_rect, error_text)
        error_group.next_to(brain, DOWN, buff=1.5)

        # Corrected JSON Box
        json_rect = Rectangle(color=GREEN, height=1, width=3)
        json_text = Text("{ 'status': 'ok' }", color=WHITE, font_size=24)
        json_group = VGroup(json_rect, json_text)
        json_group.move_to(error_group.get_center())

        # Green Checkmark (Constructed from Lines)
        check_l1 = Line(LEFT * 0.3 + UP * 0.3, DOWN * 0.2, color=GREEN, stroke_width=5)
        check_l2 = Line(DOWN * 0.2, RIGHT * 0.4 + UP * 0.4, color=GREEN, stroke_width=5)
        checkmark = VGroup(check_l1, check_l2)
        checkmark.move_to(json_rect.get_center() + RIGHT * 0.5)

        # Animation Sequence
        # 1. Show AI Brain
        self.play(Create(brain))
        self.wait(0.5)

        # 2. Show Error Message
        self.play(FadeIn(error_group))
        self.wait(0.5)

        # 3. Error Bounces Back to Brain
        self.play(error_group.animate.move_to(brain.get_center()), rate_func=smooth)
        self.wait(0.2)

        # 4. Brain Processes (Indicate)
        self.play(Indicate(brain, color=WHITE, scale_factor=1.2))
        self.play(FadeOut(error_group))

        # 5. Output Corrected JSON
        self.play(FadeIn(json_group))
        
        # 6. Show Green Check
        self.play(Create(checkmark))

        self.wait(1)
