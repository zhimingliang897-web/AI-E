from manim import *

class ExecutionFlow(Scene):
    def construct(self):
        # Title
        title = Text("Execution Flow", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Define positions (horizontal layout)
        left_x = -6
        x_spacing = 2.8
        positions = {
            "llm": LEFT * 6,
            "json": LEFT * 3,
            "python": ORIGIN,
            "api": RIGHT * 3,
            "response": RIGHT * 6,
            "reply": RIGHT * 9,
        }

        # Icons (simplified stylized representations)
        llm_icon = Circle(radius=0.6, color=BLUE, fill_opacity=0.2).move_to(positions["llm"])
        llm_label = Text("LLM", font_size=24).move_to(positions["llm"])

        json_icon = Rectangle(width=1.2, height=0.8, color=TEAL_A, fill_opacity=0.2).move_to(positions["json"])
        json_label = Text("JSON", font_size=24).move_to(positions["json"])

        python_icon = Square(side_length=1.0, color=YELLOW, fill_opacity=0.2).move_to(positions["python"])
        python_label = Text("Python\nScript", font_size=20, line_spacing=0.8).move_to(positions["python"])

        api_icon = Ellipse(width=1.4, height=0.9, color=PURPLE_A, fill_opacity=0.2).move_to(positions["api"])
        api_label = Text("Weather\nAPI", font_size=20, line_spacing=0.8).move_to(positions["api"])

        response_icon = RoundedRectangle(corner_radius=0.2, width=1.3, height=0.8, color=GREY_C, fill_opacity=0.2).move_to(positions["response"])
        response_label = Text("Response", font_size=24).move_to(positions["response"])

        reply_icon = Circle(radius=0.6, color=GREEN, fill_opacity=0.2).move_to(positions["reply"])
        reply_label = Text("Natural\nLanguage\nReply", font_size=18, line_spacing=0.7).move_to(positions["reply"])

        # Group icons and labels
        all_icons = VGroup(
            llm_icon, json_icon, python_icon, api_icon, response_icon, reply_icon
        )
        all_labels = VGroup(
            llm_label, json_label, python_label, api_label, response_label, reply_label
        )

        # Draw all icons and labels
        self.play(
            Create(llm_icon), Write(llm_label),
            Create(json_icon), Write(json_label),
            Create(python_icon), Write(python_label),
            Create(api_icon), Write(api_label),
            Create(response_icon), Write(response_label),
            Create(reply_icon), Write(reply_label),
            run_time=2
        )
        self.wait(1)

        # Arrows: LLM → JSON → Python → API → Response → LLM → Reply
        arrow_1 = Arrow(llm_icon.get_right(), json_icon.get_left(), buff=0.1, stroke_width=3)
        arrow_2 = Arrow(json_icon.get_right(), python_icon.get_left(), buff=0.1, stroke_width=3)
        arrow_3 = Arrow(python_icon.get_right(), api_icon.get_left(), buff=0.1, stroke_width=3)
        arrow_4 = Arrow(api_icon.get_right(), response_icon.get_left(), buff=0.1, stroke_width=3)
        arrow_5 = Arrow(response_icon.get_right(), reply_icon.get_left(), buff=0.1, stroke_width=3)

        # Return arrow: Reply → LLM (curved upward to avoid overlap)
        arrow_return = CurvedArrow(
            reply_icon.get_top() + UP * 0.3,
            llm_icon.get_top() + UP * 0.3,
            angle=-PI/2,
            stroke_width=3)

        # Animate forward flow
        self.play(GrowArrow(arrow_1), run_time=1)
        self.wait(0.5)
        self.play(GrowArrow(arrow_2), run_time=1)
        self.wait(0.5)
        self.play(GrowArrow(arrow_3), run_time=1)
        self.wait(0.5)
        self.play(GrowArrow(arrow_4), run_time=1)
        self.wait(0.5)
        self.play(GrowArrow(arrow_5), run_time=1)
        self.wait(1)

        # Animate return path
        self.play(Create(arrow_return), run_time=1.5)
        self.wait(1)

        # Highlight LLM again at end
        llm_pulsate = llm_icon.copy().set_stroke(YELLOW, width=4).set_fill(opacity=0)
        self.play(
            Create(llm_pulsate),
            llm_icon.animate.set_stroke(YELLOW, width=3),
            run_time=1
        )
        self.wait(1)

        # Fade out all except title and final reply
        self.play(
            FadeOut(all_icons - reply_icon),
            FadeOut(all_labels - reply_label),
            FadeOut(arrow_1, arrow_2, arrow_3, arrow_4, arrow_5, arrow_return),
            reply_icon.animate.scale(1.3).set_color(GREEN_E),
            reply_label.animate.scale(1.2).set_color(WHITE),
            run_time=1.5
        )
        self.wait(1)

        # Final note
        note = Text("End-to-end reasoning & tool use", font_size=24, color=GREY).to_edge(DOWN, buff=0.5)
        self.play(Write(note))
        self.wait(2)
