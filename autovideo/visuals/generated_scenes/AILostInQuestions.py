from manim import *

class AILostInQuestions(Scene):
    def construct(self):
        # Draw cartoon AI head: circle face with simple features
        face = Circle(radius=1.2, color=BLUE_E, fill_opacity=0.15)
        
        # Eyes: two white circles with black pupils
        left_eye = Circle(radius=0.2, color=WHITE, fill_opacity=1).shift(LEFT * 0.4 + UP * 0.2)
        right_eye = Circle(radius=0.2, color=WHITE, fill_opacity=1).shift(RIGHT * 0.4 + UP * 0.2)
        left_pupil = Circle(radius=0.08, color=BLACK, fill_opacity=1).move_to(left_eye.get_center())
        right_pupil = Circle(radius=0.08, color=BLACK, fill_opacity=1).move_to(right_eye.get_center())
        
        # Slightly tilted eyes to show confusion
        left_eye.rotate(0.15)
        right_eye.rotate(-0.15)
        left_pupil.rotate(0.15)
        right_pupil.rotate(-0.15)
        
        # Simple curved mouth (confused expression)
        mouth = Arc(start_angle=PI/3, angle=PI*2/3, radius=0.4, color=RED_E).shift(DOWN * 0.3)
        
        # Assemble AI head
        ai_head = VGroup(face, left_eye, right_eye, left_pupil, right_pupil, mouth)
        
        # Question marks — larger, bold, playful
        qmarks = [
            Text("?", font_size=64, weight=BOLD, color=YELLOW).shift(UP * 2.5),
            Text("?", font_size=64, weight=BOLD, color=TEAL_A).shift(RIGHT * 2.8),
            Text("?", font_size=64, weight=BOLD, color=PURPLE_A).shift(DOWN * 2.5),
            Text("?", font_size=64, weight=BOLD, color=GREEN).shift(LEFT * 2.8),
        ]
        
        # Labels near each question mark
        labels = [
            Text("Theme?", font_size=28, color=YELLOW).next_to(qmarks[0], UP, buff=0.4),
            Text("Audience?", font_size=28, color=TEAL_A).next_to(qmarks[1], RIGHT, buff=0.4),
            Text("Length?", font_size=28, color=PURPLE_A).next_to(qmarks[2], DOWN, buff=0.4),
            Text("Style?", font_size=28, color=GREEN).next_to(qmarks[3], LEFT, buff=0.4),
        ]
        
        # Add head first
        self.play(FadeIn(ai_head), run_time=1.2)
        self.wait(0.5)
        
        # Pop up question marks one by one with bounce
        for i in range(4):
            self.play(
                FadeIn(qmarks[i], scale=0.5),
                Write(labels[i]),
                rate_func=smooth,
                run_time=0.8
            )
            self.wait(0.4)
        
        # Subtle head wobble to emphasize confusion
        self.play(
            ai_head.animate.rotate(0.05).shift(UP * 0.05),
            run_time=0.4,
            rate_func=smooth
        )
        self.play(
            ai_head.animate.rotate(-0.05).shift(DOWN * 0.05),
            run_time=0.4,
            rate_func=smooth
        )
        
        # Final pause
        self.wait(1.5)
