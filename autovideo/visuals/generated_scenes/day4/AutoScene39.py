from manim import *

class AutoScene39(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Brain icon: stylized using two mirrored ellipses + central arc
        left_brain = Ellipse(width=2.0, height=2.4, color=PURPLE_E).shift(LEFT * 0.6)
        right_brain = Ellipse(width=2.0, height=2.4, color=PURPLE_E).shift(RIGHT * 0.6)
        brain_core = Arc(start_angle=PI/2, angle=-PI, radius=0.8, color=PURPLE_A).shift(UP * 0.2)
        brain = VGroup(left_brain, right_brain, brain_core).scale(0.9).shift(DOWN * 0.3)

        # Core (center point inside brain)
        core_dot = Dot(point=ORIGIN, color=YELLOW, radius=0.15).set_z_index(2)

        # Three input streams — equally spaced around brain (top, left, right)
        # 1. Text stream: speech bubble
        bubble = RoundedRectangle(corner_radius=0.2, width=2.2, height=1.0, color=BLUE, fill_opacity=0.15, stroke_width=2)
        tail = Triangle().rotate(-PI/2).scale(0.2).next_to(bubble, DOWN, buff=0).set_fill(BLUE, opacity=1).set_stroke(width=0)
        speech_bubble = VGroup(bubble, tail).shift(UP * 2.5)
        text_label = Text("Text", font_size=24, color=BLUE).move_to(speech_bubble.get_center())
        text_stream = VGroup(speech_bubble, text_label)

        # 2. Image stream: camera icon (simplified)
        cam_body = Rectangle(width=1.8, height=1.2, color=GREEN, fill_opacity=0.15, stroke_width=2)
        cam_lens = Circle(radius=0.4, color=GREEN, fill_opacity=0.25, stroke_width=2)
        cam_viewfinder = Square(side_length=0.2, color=GREEN).move_to(cam_lens.get_center())
        camera = VGroup(cam_body, cam_lens, cam_viewfinder).shift(LEFT * 2.8 + UP * 0.5)
        image_label = Text("Image", font_size=24, color=GREEN).next_to(camera, LEFT, buff=0.3)
        image_stream = VGroup(camera, image_label)

        # 3. Audio stream: waveform
        waveform_points = [
            [0, 0, 0],
            [0.3, 0.4, 0],
            [0.6, -0.3, 0],
            [0.9, 0.5, 0],
            [1.2, -0.2, 0],
            [1.5, 0.0, 0]
        ]
        waveform = VGroup(*[
            Line(waveform_points[i], waveform_points[i+1], color=RED, stroke_width=3)
            for i in range(len(waveform_points)-1)
        ]).shift(RIGHT * 2.8 + UP * 0.5)
        audio_label = Text("Audio", font_size=24, color=RED).next_to(waveform, RIGHT, buff=0.3)
        audio_stream = VGroup(waveform, audio_label)

        # Arrows from each stream to core
        arrow1 = Arrow(speech_bubble.get_bottom(), core_dot.get_top() + DOWN*0.1, buff=0.1, color=BLUE, stroke_width=3, tip_length=0.2)
        arrow2 = Arrow(camera.get_right(), core_dot.get_left() + RIGHT*0.1, buff=0.1, color=GREEN, stroke_width=3, tip_length=0.2)
        arrow3 = Arrow(waveform.get_left(), core_dot.get_right() + LEFT*0.1, buff=0.1, color=RED, stroke_width=3, tip_length=0.2)

        # Assemble all elements
        all_elements = VGroup(
            brain,
            core_dot,
            text_stream,
            image_stream,
            audio_stream,
            arrow1, arrow2, arrow3
        )

        # Animation sequence
        self.play(FadeIn(brain), run_time=1.2)
        self.wait(0.5)
        self.play(FadeIn(core_dot), run_time=0.8)
        self.wait(0.5)
        self.play(
            FadeIn(text_stream),
            FadeIn(image_stream),
            FadeIn(audio_stream),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(
            Create(arrow1),
            Create(arrow2),
            Create(arrow3),
            run_time=1.5
        )
        self.wait(1.5)

        # Optional subtle pulse on core
        self.play(
            core_dot.animate.scale(1.3).set_color(YELLOW_E),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(1)
