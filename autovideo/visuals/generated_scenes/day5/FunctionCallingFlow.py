from manim import *

class FunctionCallingFlow(Scene):
    def construct(self):
        # Title
        title = Text("Function Calling Flow", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Components
        llm = Rectangle(height=1.2, width=2.0, color=BLUE, fill_color=BLUE, fill_opacity=0.2)
        llm_label = Text("LLM", font_size=24, color=BLUE).move_to(llm.get_center())

        json_box = RoundedRectangle(height=1.2, width=2.4, corner_radius=0.2, color=GREEN, fill_color=GREEN, fill_opacity=0.2)
        json_label = Text("JSON Schema", font_size=20, color=GREEN).move_to(json_box.get_center())

        api_icon = VGroup()
        # Simple API icon: cloud + gear
        cloud = Circle(radius=0.6, color=PURPLE, fill_color=PURPLE, fill_opacity=0.2)
        gear = RegularPolygon(n=6, radius=0.3, color=PURPLE, fill_color=PURPLE, fill_opacity=0.4)
        gear.rotate(PI/6)
        api_icon.add(cloud, gear)
        api_icon.scale(0.8)
        api_label = Text("External API", font_size=20, color=PURPLE).next_to(api_icon, DOWN, buff=0.3)

        # Arrows
        arrow1 = Arrow(start=llm.get_right(), end=json_box.get_left(), buff=0.2, color=GREY_C, stroke_width=3)
        arrow2 = Arrow(start=json_box.get_right(), end=api_icon.get_left(), buff=0.2, color=GREY_C, stroke_width=3)
        return_arrow = CurvedArrow(api_icon.get_top(), llm.get_top(),
            angle=-PI/2,
            color=TEAL_A,
            stroke_width=3
        )
        return_label = Text("Response", font_size=18, color=TEAL_A).next_to(return_arrow, UP, buff=0.2)

        # Positioning
        llm.shift(LEFT * 4)
        json_box.move_to(ORIGIN)
        api_icon.shift(RIGHT * 4)
        llm_label.move_to(llm.get_center())
        json_label.move_to(json_box.get_center())
        api_label.next_to(api_icon, DOWN, buff=0.3)
        return_arrow.shift(DOWN * 0.2)

        # Animate flow
        self.play(
            Create(llm),
            Write(llm_label),
            run_time=0.8
        )
        self.wait(0.3)
        self.play(
            Create(json_box),
            Write(json_label),
            run_time=0.8
        )
        self.wait(0.3)
        self.play(
            Create(api_icon),
            Write(api_label),
            run_time=0.8
        )
        self.wait(0.3)
        self.play(Create(arrow1), run_time=0.6)
        self.wait(0.2)
        self.play(Create(arrow2), run_time=0.6)
        self.wait(0.2)
        self.play(Create(return_arrow), Write(return_label), run_time=0.8)
        self.wait(1.5)

        # Fade out all except title and final flow
        self.play(
            FadeOut(llm), FadeOut(llm_label),
            FadeOut(json_box), FadeOut(json_label),
            FadeOut(api_icon), FadeOut(api_label),
            FadeOut(arrow1), FadeOut(arrow2),
            FadeOut(return_arrow), FadeOut(return_label),
            run_time=0.7
        )

        # Final clean summary
        summary = VGroup(
            Text("LLM → JSON Schema → External API → Response", font_size=28, color=WHITE),
            Text("Enables tool use via structured function calls", font_size=22, color=GREY_C)
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(summary[0]), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(summary[1]), run_time=0.8)
        self.wait(2)
