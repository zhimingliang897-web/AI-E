from manim import *

class CvNlpDualRole(Scene):
    def construct(self):
        # Background split
        left_rect = Rectangle(width=7, height=6, fill_opacity=0, stroke_width=0).to_edge(LEFT, buff=0.5)
        right_rect = Rectangle(width=7, height=6, fill_opacity=0, stroke_width=0).to_edge(RIGHT, buff=0.5)
        divider = Line(UP * 3, DOWN * 3, stroke_width=2, color=GREY_C)

        # --- LEFT SIDE: NLP / Speech → Brain ---
        # Speech bubbles (stacked vertically)
        bubble1 = RoundedRectangle(corner_radius=0.2, width=5, height=1.2, fill_color=BLUE, fill_opacity=0.1, stroke_color=BLUE, stroke_width=1.5)
        text1 = Text("Hello world", font_size=24, color=BLUE).move_to(bubble1.get_center())
        
        bubble2 = RoundedRectangle(corner_radius=0.2, width=5, height=1.2, fill_color=BLUE, fill_opacity=0.1, stroke_color=BLUE, stroke_width=1.5).next_to(bubble1, DOWN, buff=0.4)
        text2 = Text("Translate to French", font_size=24, color=BLUE).move_to(bubble2.get_center())

        speech_group = VGroup(bubble1, text1, bubble2, text2).move_to(left_rect.get_center() + UP * 0.8)

        # LLM "brain" icon: stylized neural network — circle with inner interconnected arcs
        brain_outer = Circle(radius=1.0, color=PURPLE, stroke_width=3)
        brain_inner = Circle(radius=0.4, color=PURPLE_A, stroke_width=2, fill_opacity=0.2)
        arc1 = ArcBetweenPoints(UP * 0.3 + LEFT * 0.2, RIGHT * 0.3 + UP * 0.1, radius=0.6, color=PURPLE_E, stroke_width=2)
        arc2 = ArcBetweenPoints(DOWN * 0.2 + LEFT * 0.25, RIGHT * 0.25 + DOWN * 0.15, radius=0.5, color=PURPLE_E, stroke_width=2)
        arc3 = ArcBetweenPoints(UP * 0.1 + RIGHT * 0.25, DOWN * 0.25 + LEFT * 0.15, radius=0.55, color=PURPLE_E, stroke_width=2)
        brain_icon = VGroup(brain_outer, brain_inner, arc1, arc2, arc3).scale(0.8).move_to(left_rect.get_center() + DOWN * 1.5)

        # Arrows from bubbles to brain
        arrow1 = Arrow(speech_group.get_bottom(), brain_icon.get_top() + UP * 0.2, buff=0.1, stroke_width=2, color=BLUE)
        arrow2 = Arrow(speech_group.get_bottom(), brain_icon.get_top() + UP * 0.2, buff=0.1, stroke_width=2, color=BLUE).shift(RIGHT * 0.3)
        arrows_in = VGroup(arrow1, arrow2)

        # --- RIGHT SIDE: CV / Camera → Eye ---
        # Camera lens: concentric circles + shutter lines
        lens_outer = Circle(radius=0.8, color=TEAL_A, stroke_width=2)
        lens_inner = Circle(radius=0.4, color=TEAL_A, stroke_width=1.5)
        shutter1 = Line(ORIGIN + UP * 0.6, ORIGIN + DOWN * 0.6, stroke_width=2, color=TEAL_A)
        shutter2 = Line(ORIGIN + LEFT * 0.6, ORIGIN + RIGHT * 0.6, stroke_width=2, color=TEAL_A)
        camera_icon = VGroup(lens_outer, lens_inner, shutter1, shutter2).scale(0.9).move_to(right_rect.get_center() + UP * 1.2)

        # Photo placeholder: rectangle with grid lines (simplified feature map)
        photo = RoundedRectangle(corner_radius=0.1, width=3.5, height=2.2, fill_color=GREY_C, fill_opacity=0.05, stroke_color=GREY_C, stroke_width=1)
        grid_lines = VGroup()
        for i in range(1, 4):
            grid_lines.add(Line(LEFT * 1.7 + UP * (0.7 - i * 0.7), RIGHT * 1.7 + UP * (0.7 - i * 0.7), stroke_width=0.5, color=GREY_C))
            grid_lines.add(Line(LEFT * 1.7 + LEFT * (i * 0.7 - 0.7), RIGHT * 1.7 + LEFT * (i * 0.7 - 0.7), stroke_width=0.5, color=GREY_C))
        photo_group = VGroup(photo, grid_lines).move_to(right_rect.get_center() + DOWN * 0.2)

        # Eye icon: simplified eye — outer ellipse + iris circle + highlight dot
        eye_ellipse = Ellipse(width=1.8, height=1.2, color=YELLOW, stroke_width=2.5)
        iris = Circle(radius=0.4, color=YELLOW_E, fill_opacity=1, stroke_width=0)
        highlight = Circle(radius=0.1, color=WHITE, fill_opacity=1, stroke_width=0)
        eye_icon = VGroup(eye_ellipse, iris, highlight).scale(0.7).move_to(right_rect.get_center() + DOWN * 1.6)

        # Arrows: camera → photo → eye
        arrow_cam_to_photo = Arrow(camera_icon.get_bottom(), photo_group.get_top(), buff=0.2, stroke_width=2, color=TEAL_A)
        arrow_photo_to_eye = Arrow(photo_group.get_bottom(), eye_icon.get_top(), buff=0.2, stroke_width=2, color=TEAL_A)

        # --- Animation sequence ---
        self.camera.background_color = BLACK

        # Title
        title = Text("CV & NLP: Dual Roles of LLMs", font_size=32, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # Draw split layout
        self.play(
            Create(left_rect),
            Create(right_rect),
            Create(divider),
            run_time=1
        )
        self.wait(0.5)

        # Left: reveal speech bubbles
        self.play(FadeIn(speech_group), run_time=1.2)
        self.wait(0.5)

        # Right: reveal camera
        self.play(FadeIn(camera_icon), run_time=1.2)
        self.wait(0.5)

        # Left: animate arrows into brain
        self.play(Create(arrows_in), run_time=1)
        self.wait(0.3)
        self.play(FadeIn(brain_icon), run_time=1.2)
        self.wait(0.5)

        # Right: camera focuses → photo appears
        self.play(
            camera_icon.animate.scale(1.1).set_color(YELLOW),
            run_time=0.8,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(0.2)
        self.play(FadeIn(photo_group), Create(arrow_cam_to_photo), run_time=1.2)
        self.wait(0.5)

        # Right: photo → eye with pulse sync
        self.play(Create(arrow_photo_to_eye), run_time=0.8)
        self.wait(0.2)
        self.play(FadeIn(eye_icon), run_time=1.2)
        self.wait(0.5)

        # Sync pulse animation on both icons
        brain_pulse = brain_icon.copy().set_stroke(width=6, color=PURPLE_E).set_opacity(0.7)
        eye_pulse = eye_icon.copy().set_stroke(width=5, color=YELLOW_E).set_opacity(0.7)

        self.play(
            FadeIn(brain_pulse),
            FadeIn(eye_pulse),
            run_time=0.6
        )
        self.play(
            FadeOut(brain_pulse),
            FadeOut(eye_pulse),
            run_time=0.6
        )
        self.wait(0.5)

        # Final sync pulse (slight scale + glow)
        self.play(
            brain_icon.animate.scale(1.08).set_color(PURPLE_E),
            eye_icon.animate.scale(1.08).set_color(YELLOW_E),
            run_time=0.5,
            rate_func=smooth
        )
        self.wait(1)
