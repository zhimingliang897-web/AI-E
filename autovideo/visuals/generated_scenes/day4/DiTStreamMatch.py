from manim import *

class DiTStreamMatch(Scene):
    def construct(self):
        # Title
        title = Text("DiT Stream Matching Pipeline", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Image patches (grid of small squares)
        patch_grid = VGroup()
        for i in range(3):
            for j in range(3):
                patch = Square(side_length=0.4, color=BLUE, fill_opacity=0.3)
                patch.move_to(LEFT * 4 + RIGHT * j * 0.6 + DOWN * i * 0.6)
                patch_grid.add(patch)
        patch_label = Text("Image Patches", font_size=20).next_to(patch_grid, UP, buff=0.3)

        self.play(Create(patch_grid), Write(patch_label))
        self.wait(1)

        # Transformer blocks (stacked rectangles with "xN" label)
        transformer = RoundedRectangle(corner_radius=0.2, height=2.0, width=1.2, color=TEAL_A, fill_opacity=0.4)
        transformer.move_to(ORIGIN)
        block_label = Text("Transformer\nBlocks", font_size=20, align="center").move_to(transformer.get_center())
        n_label = Text("×N", font_size=18, color=YELLOW).next_to(transformer, RIGHT, buff=0.3)

        self.play(
            TransformFromCopy(patch_grid, transformer),
            FadeOut(patch_label),
            run_time=1.5
        )
        self.play(Write(block_label), Write(n_label))
        self.wait(1)

        # Temporal stream matching: two parallel streams with arrows and sync pulses
        stream_left = RoundedRectangle(corner_radius=0.15, height=0.8, width=2.0, color=PURPLE_A, fill_opacity=0.35)
        stream_right = RoundedRectangle(corner_radius=0.15, height=0.8, width=2.0, color=PURPLE_E, fill_opacity=0.35)
        stream_left.move_to(LEFT * 1.5 + DOWN * 2.0)
        stream_right.move_to(RIGHT * 1.5 + DOWN * 2.0)

        arrow1 = Arrow(transformer.get_bottom(), stream_left.get_top(), buff=0.2, stroke_width=3, color=GREY_C)
        arrow2 = Arrow(transformer.get_bottom(), stream_right.get_top(), buff=0.2, stroke_width=3, color=GREY_C)

        match_label = Text("Temporal Stream Matching", font_size=22).next_to(stream_left, UP, buff=0.5).shift(RIGHT * 0.5)

        self.play(
            Create(arrow1), Create(arrow2),
            FadeIn(stream_left), FadeIn(stream_right),
            Write(match_label)
        )
        self.wait(1)

        # Pulse animation on streams to indicate matching
        pulse_anim = AnimationGroup(
            stream_left.animate.set_fill(PURPLE, opacity=0.7),
            stream_right.animate.set_fill(PURPLE, opacity=0.7),
            run_time=0.4
        )
        self.play(pulse_anim)
        self.play(
            stream_left.animate.set_fill(PURPLE_A, opacity=0.35),
            stream_right.animate.set_fill(PURPLE_E, opacity=0.35)
        )
        self.wait(0.5)

        # Smooth video timeline (horizontal axis with ticks and smooth curve)
        timeline = NumberLine(
            x_range=[0, 10, 1],
            length=8,
            color=GREY_C,
            include_numbers=True,
            font_size=16,
            numbers_to_exclude=[]
        )
        timeline.next_to(stream_left, DOWN, buff=1.2).shift(RIGHT * 0.5)
        timeline_label = Text("Smooth Video Output Timeline", font_size=22).next_to(timeline, UP, buff=0.4)

        # Curve representing smooth output
        def smooth_curve(x):
            return 0.3 * np.sin(0.6 * x) + 0.1 * x - 0.5

        graph = FunctionGraph(
            smooth_curve,
            x_range=[0.5, 9.5],
            color=YELLOW,
            stroke_width=4
        )
        graph.move_to(timeline.c2p(5, 0)).shift(UP * 0.8)

        self.play(
            Create(timeline),
            Write(timeline_label),
            Create(graph)
        )
        self.wait(1)

        # Animate curve drawing
        self.play(
            Create(graph.copy().set_stroke(width=0)),
            MoveAlongPath(graph.copy().set_stroke(YELLOW, width=4), graph),
            run_time=2.5,
            rate_func=smooth
        )
        self.remove(graph)
        self.wait(0.5)

        # 'Sora' logo — stylized text with pulsing effect
        sora_logo = Text("SORA", font_size=64, weight=BOLD, font="Arial")
        sora_logo.set_color_by_gradient(BLUE, PURPLE, RED)
        sora_logo.move_to(DOWN * 1.0)

        self.play(FadeIn(sora_logo, scale=0.8))
        self.wait(0.5)

        # Pulse animation: scale + opacity
        for _ in range(3):
            self.play(
                sora_logo.animate.scale(1.15).set_opacity(0.9),
                rate_func=smooth,
                run_time=1.2
            )
            self.wait(0.3)

        self.wait(1.5)
        self.play(FadeOut(VGroup(title, patch_grid, transformer, block_label, n_label,
                                 arrow1, arrow2, stream_left, stream_right, match_label,
                                 timeline, timeline_label, sora_logo)))
        self.wait(0.5)
