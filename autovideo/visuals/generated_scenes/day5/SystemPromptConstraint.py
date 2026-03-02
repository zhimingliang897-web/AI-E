from manim import *

class SystemPromptConstraint(Scene):
    def construct(self):
        # Background rectangle for system prompt
        prompt_bg = RoundedRectangle(
            corner_radius=0.2,
            width=10,
            height=4,
            fill_color=GREY_C,
            fill_opacity=0.15,
            stroke_color=GREY_C,
            stroke_width=2
        )
        
        # Title
        title = Text("System Prompt", font_size=32, weight=BOLD)
        title.move_to(prompt_bg.get_top() + UP * 0.5)
        
        # Main prompt text (split for clarity)
        prompt_text = Text(
            "You are a helpful AI assistant.\n"
            "You MUST output ONLY valid JSON\n"
            "with no extra text, explanations, or markdown.",
            font_size=24,
            line_spacing=1.4,
            t2c={
                "You MUST output ONLY valid JSON": YELLOW
            }
        )
        prompt_text.move_to(prompt_bg.get_center())
        
        # Highlight box around the constraint phrase
        constraint_text = prompt_text[0][26:52]  # approximate index range for the yellow phrase
        highlight_rect = SurroundingRectangle(
            constraint_text,
            color=YELLOW,
            buff=0.1,
            stroke_width=2,
            corner_radius=0.05
        )
        
        # Optional subtle icon: gear symbol using basic shapes
        gear_center = Dot(radius=0.03, color=YELLOW).move_to(prompt_bg.get_left() + RIGHT*0.8 + UP*0.5)
        gear_teeth = VGroup()
        for i in range(8):
            angle = i * PI / 4
            tooth = Rectangle(
                width=0.2, height=0.08,
                fill_color=YELLOW, fill_opacity=1,
                stroke_width=0
            ).rotate(angle).move_to(
                gear_center.get_center() + 0.35 * np.array([np.cos(angle), np.sin(angle), 0])
            )
            gear_teeth.add(tooth)
        gear = VGroup(gear_center, gear_teeth)
        gear.scale(0.7).next_to(title, LEFT, buff=0.3)
        
        # Assemble scene
        self.play(
            Create(prompt_bg),
            Write(title),
            FadeIn(gear),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(Write(prompt_text), run_time=2.5)
        self.wait(0.5)
        self.play(Create(highlight_rect), run_time=1.0)
        self.wait(2.0)
        
        # Subtle pulse on highlight
        self.play(
            highlight_rect.animate.scale(1.03).set_stroke(YELLOW_E, width=3),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(1.0)
