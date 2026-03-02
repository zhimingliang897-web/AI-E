from manim import *

class AutoScene24(Scene):
    def construct(self):
        # Background remains black (default)

        # Pyramid base: a centered isosceles triangle (2D projection of pyramid base)
        base_triangle = Polygon(
            [-3, -2, 0], [3, -2, 0], [0, 1, 0],
            color=GREY_C, fill_opacity=0.1, stroke_width=2
        )
        base_label = Text("Transformer", font_size=24, weight=BOLD).move_to([0, -0.5, 0])

        # Icons — using simple geometric shapes to represent text, image, audio
        # Text icon: 'T' inside a circle
        text_circle = Circle(radius=0.6, color=BLUE, fill_opacity=0.15).shift([-4, 1.5, 0])
        text_letter = Text("T", font_size=28, color=BLUE, weight=BOLD).move_to(text_circle.get_center())
        text_icon = VGroup(text_circle, text_letter)

        # Image icon: rectangle with diagonal cross (simplified camera/image symbol)
        image_rect = Rectangle(width=1.2, height=0.8, color=GREEN, fill_opacity=0.15).shift([0, 2.5, 0])
        diag1 = Line([-0.5, 0.3, 0], [0.5, -0.3, 0], color=GREEN, stroke_width=2).move_to(image_rect.get_center())
        diag2 = Line([-0.5, -0.3, 0], [0.5, 0.3, 0], color=GREEN, stroke_width=2).move_to(image_rect.get_center())
        image_icon = VGroup(image_rect, diag1, diag2)

        # Audio icon: speaker-like shape — two concentric arcs + center dot
        audio_arc1 = Arc(start_angle=PI/4, angle=PI/2, radius=0.5, color=PURPLE, stroke_width=2).shift([4, 1.5, 0])
        audio_arc2 = Arc(start_angle=PI/4, angle=PI/2, radius=0.7, color=PURPLE, stroke_width=2).shift([4, 1.5, 0])
        audio_dot = Dot(point=[4, 1.5, 0], color=PURPLE, radius=0.1)
        audio_icon = VGroup(audio_arc1, audio_arc2, audio_dot)

        # Position icons around the base triangle (top-left, top, top-right)
        text_icon.move_to([-4, 1.5, 0])
        image_icon.move_to([0, 2.5, 0])
        audio_icon.move_to([4, 1.5, 0])

        # Glowing links: curved arrows from each icon to base triangle's top vertex
        top_vertex = [0, 1, 0]
        link1 = CurvedArrow(text_icon.get_bottom(), top_vertex, angle=-PI/4, color=TEAL_A, stroke_width=3, tip_length=0.15)
        link2 = CurvedArrow(image_icon.get_bottom(), top_vertex, angle=0, color=TEAL_A, stroke_width=3, tip_length=0.15)
        link3 = CurvedArrow(audio_icon.get_bottom(), top_vertex, angle=PI/4, color=TEAL_A, stroke_width=3, tip_length=0.15)

        # Add glow effect via multiple copies with fading opacity and blur (simulated with extra strokes)
        glow_links = VGroup()
        for alpha in [0.3, 0.15, 0.05]:
            l1_glow = link1.copy().set_opacity(alpha).set_stroke(width=link1.stroke_width * 0.7)
            l2_glow = link2.copy().set_opacity(alpha).set_stroke(width=link2.stroke_width * 0.7)
            l3_glow = link3.copy().set_opacity(alpha).set_stroke(width=link3.stroke_width * 0.7)
            glow_links.add(l1_glow, l2_glow, l3_glow)

        # Assemble scene
        self.play(Create(base_triangle), Write(base_label))
        self.wait(0.5)
        self.play(FadeIn(text_icon), FadeIn(image_icon), FadeIn(audio_icon))
        self.wait(0.5)
        self.play(
            Create(glow_links),
            Create(link1), Create(link2), Create(link3),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)

        # Subtle pulse on links
        self.play(
            link1.animate.set_stroke(width=5).set_color(TEAL_E),
            link2.animate.set_stroke(width=5).set_color(TEAL_E),
            link3.animate.set_stroke(width=5).set_color(TEAL_E),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.play(
            link1.animate.set_stroke(width=3).set_color(TEAL_A),
            link2.animate.set_stroke(width=3).set_color(TEAL_A),
            link3.animate.set_stroke(width=3).set_color(TEAL_A),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(1)
