from manim import *

class TextToJsonToTool(Scene):
    def construct(self):
        # Input Text Box
        input_rect = RoundedRectangle(
            corner_radius=0.2, 
            height=1.5, 
            width=3, 
            color=BLUE,
            fill_opacity=0.1,
            fill_color=BLUE
        )
        input_text = Text("User Input", font_size=24, color=WHITE)
        input_group = VGroup(input_rect, input_text)
        input_group.move_to(ORIGIN)

        # JSON Box
        json_rect = RoundedRectangle(
            corner_radius=0.2, 
            height=1.5, 
            width=3, 
            color=GREEN,
            fill_opacity=0.1,
            fill_color=GREEN
        )
        json_rect.move_to(input_rect)
        json_text = Text("{ \"key\": \"value\" }", font_size=20, color=WHITE)
        json_text.move_to(input_text)
        json_group = VGroup(json_rect, json_text)

        # API Icon (Circle with Cross)
        api_circle = Circle(radius=0.3, color=ORANGE, fill_opacity=0.2, fill_color=ORANGE)
        api_cross = VGroup(
            Line(LEFT*0.2, RIGHT*0.2, color=WHITE),
            Line(UP*0.2, DOWN*0.2, color=WHITE)
        )
        api_icon = VGroup(api_circle, api_cross)

        # Script Icon (Rectangle with Lines)
        script_rect = Rectangle(
            height=0.6, 
            width=0.5, 
            color=WHITE, 
            fill_opacity=0.2, 
            fill_color=WHITE
        )
        script_lines = VGroup(*[
            Line(LEFT*0.15, RIGHT*0.15, color=BLACK).shift(DOWN*i*0.1) 
            for i in range(3)
        ])
        script_icon = VGroup(script_rect, script_lines)

        # Arrange Icons
        icons = VGroup(api_icon, script_icon).arrange(DOWN, buff=0.5)
        icons.next_to(input_group, RIGHT, buff=1.5)

        # Arrow
        arrow = Arrow(
            input_group.get_right(), 
            icons.get_left(), 
            color=YELLOW,
            buff=0.2
        )

        # Animations
        self.play(Create(input_group), rate_func=smooth)
        self.wait(1)

        self.play(
            Transform(input_rect, json_rect),
            FadeOut(input_text),
            FadeIn(json_text),
            rate_func=smooth
        )
        self.wait(1)

        self.play(
            Create(icons),
            Create(arrow),
            rate_func=smooth
        )
        self.wait(1)
