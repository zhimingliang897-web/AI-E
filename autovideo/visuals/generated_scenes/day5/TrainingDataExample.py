from manim import *

class TrainingDataExample(Scene):
    def construct(self):
        # Title
        title = Text("Training Data Example", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Column headers
        header1 = Text("User query", font_size=24, weight=BOLD).set_color(BLUE)
        header2 = Text("Tool name & schema", font_size=24, weight=BOLD).set_color(GREEN)
        header3 = Text("JSON output", font_size=24, weight=BOLD).set_color(PURPLE)

        headers = VGroup(header1, header2, header3).arrange(RIGHT, buff=2.0)
        headers.next_to(title, DOWN, buff=1.0)

        # Draw horizontal line under headers
        line = Line(
            headers.get_left() + DOWN * 0.3,
            headers.get_right() + DOWN * 0.3,
            stroke_width=2,
            color=GREY_C
        )

        self.play(
            Write(header1), Write(header2), Write(header3),
            Create(line)
        )
        self.wait(0.5)

        # Row 1 data
        q1 = Text(
            "What's the weather in Tokyo?",
            font_size=20,
            font="Monospace"
        ).set_color(BLUE_A)
        t1 = Text(
            "weather_api: {\"location\": str}",
            font_size=20,
            font="Monospace"
        ).set_color(GREEN_A)
        j1 = Text(
            '{"temp_c": 22.5, "condition": "Partly cloudy"}',
            font_size=20,
            font="Monospace"
        ).set_color(PURPLE_A)

        row1 = VGroup(q1, t1, j1).arrange(RIGHT, buff=2.0)
        row1.next_to(line, DOWN, buff=0.8)

        # Row 2 data
        q2 = Text(
            "Book a flight from NYC to LA",
            font_size=20,
            font="Monospace"
        ).set_color(BLUE_A)
        t2 = Text(
            "flight_booking: {\"origin\": str, \"destination\": str}",
            font_size=20,
            font="Monospace"
        ).set_color(GREEN_A)
        j2 = Text(
            '{"flight_id": "FL2024", "departure": "2024-05-10T08:00"}',
            font_size=20,
            font="Monospace"
        ).set_color(PURPLE_A)

        row2 = VGroup(q2, t2, j2).arrange(RIGHT, buff=2.0)
        row2.next_to(row1, DOWN, buff=0.8)

        # Row 3 data
        q3 = Text(
            "Send email to alex@demo.com",
            font_size=20,
            font="Monospace"
        ).set_color(BLUE_A)
        t3 = Text(
            "email_sender: {\"to\": str, \"subject\": str, \"body\": str}",
            font_size=20,
            font="Monospace"
        ).set_color(GREEN_A)
        j3 = Text(
            '{"status": "sent", "message_id": "msg_789"}',
            font_size=20,
            font="Monospace"
        ).set_color(PURPLE_A)

        row3 = VGroup(q3, t3, j3).arrange(RIGHT, buff=2.0)
        row3.next_to(row2, DOWN, buff=0.8)

        # Animate rows one by one
        self.play(FadeIn(row1), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(row2), run_time=1.2)
        self.wait(0.6)
        self.play(FadeIn(row3), run_time=1.2)
        self.wait(1.0)

        # Highlight columns with subtle background rectangles
        bg1 = Rectangle(
            width=q1.width + 0.6,
            height=q1.height + 0.4,
            fill_color=BLUE_E,
            fill_opacity=0.15,
            stroke_width=0
        ).move_to(q1)
        bg2 = Rectangle(
            width=t1.width + 0.6,
            height=t1.height + 0.4,
            fill_color=GREEN_E,
            fill_opacity=0.15,
            stroke_width=0
        ).move_to(t1)
        bg3 = Rectangle(
            width=j1.width + 0.6,
            height=j1.height + 0.4,
            fill_color=PURPLE_E,
            fill_opacity=0.15,
            stroke_width=0
        ).move_to(j1)

        self.play(
            FadeIn(bg1), FadeIn(bg2), FadeIn(bg3),
            run_time=1.0
        )
        self.wait(1.5)

        # Final note
        note = Text(
            "Each row teaches the model how to map queries → tool calls → structured outputs",
            font_size=22,
            font="Microsoft YaHei",
            color=GREY_C
        ).next_to(row3, DOWN, buff=1.2)

        self.play(FadeIn(note), run_time=1.0)
        self.wait(2.0)
