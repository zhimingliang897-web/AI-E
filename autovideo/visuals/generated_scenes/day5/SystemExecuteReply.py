from manim import *

class SystemExecuteReply(Scene):
    def construct(self):
        # Define positions
        client_pos = LEFT * 4
        server_pos = RIGHT * 4

        # Server Icon (Constructed from primitives)
        server_units = VGroup(*[
            Rectangle(width=3.5, height=0.8, color=BLUE_E, fill_opacity=0.6)
            for _ in range(3)
        ])
        server_units.arrange(DOWN, buff=0.15)
        # Server lights
        lights = VGroup(*[Circle(radius=0.1, color=GREEN, fill_opacity=1) for _ in range(3)])
        lights.arrange(RIGHT, buff=0.5)
        lights.move_to(server_units.get_center())
        server = VGroup(server_units, lights)
        server.move_to(server_pos)

        # JSON Packet
        json_label = Text("JSON", font_size=24, color=WHITE)
        json_box = RoundedRectangle(corner_radius=0.2, height=1.2, width=2.2, color=GREEN, fill_opacity=0.5)
        json_packet = VGroup(json_box, json_label)
        json_packet.move_to(client_pos)

        # Result Text
        result_text = Text("Beijing 25 degrees", font_size=36, color=YELLOW)
        result_text.move_to(client_pos)

        # Arrows
        req_arrow = Arrow(json_packet.get_right(), server.get_left(), color=WHITE, buff=0.2)
        res_arrow = Arrow(server.get_left(), json_packet.get_right(), color=WHITE, buff=0.2)

        # Animation Sequence
        # 1. Show Initial State
        self.play(Create(server), Create(json_packet))
        self.wait(0.5)

        # 2. Request Phase (JSON to Server)
        self.play(Create(req_arrow))
        self.play(json_packet.animate.move_to(server.get_center()), rate_func=smooth)
        self.wait(0.5)
        self.play(FadeOut(req_arrow))

        # 3. Response Phase (Data back to Client)
        self.play(Create(res_arrow))
        # Change color to signify response data and move back
        self.play(
            json_packet.animate.set_color(TEAL).move_to(client_pos),
            rate_func=smooth
        )
        self.wait(0.5)
        self.play(FadeOut(res_arrow))

        # 4. Result Phase (Show Weather Data)
        self.play(FadeOut(json_packet), FadeIn(result_text))
        self.wait(1)
