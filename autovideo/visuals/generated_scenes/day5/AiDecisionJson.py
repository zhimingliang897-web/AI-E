from manim import *

class AiDecisionJson(Scene):
    def construct(self):
        main_body = Ellipse(width=3.5, height=2.5, color=BLUE_E, fill_opacity=0.9)
        tail_1 = Circle(radius=0.35, color=BLUE_E, fill_opacity=0.9).shift(DOWN * 0.7 + LEFT * 0.6)
        tail_2 = Circle(radius=0.25, color=BLUE_E, fill_opacity=0.9).shift(DOWN * 1.1 + LEFT * 1.1)
        tail_3 = Circle(radius=0.15, color=BLUE_E, fill_opacity=0.9).shift(DOWN * 1.4 + LEFT * 1.5)
        
        thought_bubble = VGroup(main_body, tail_1, tail_2, tail_3)
        
        json_str = "{\n  'name': 'get_weather',\n  'arguments': {\n    'city': 'Beijing'\n  }\n}"
        json_text = Text(json_str, font="Microsoft YaHei", color=GREEN, font_size=24)
        
        self.play(Create(thought_bubble), run_time=1.5)
        self.wait(1)
        self.play(ReplacementTransform(thought_bubble, json_text), run_time=2)
        self.wait(1)
