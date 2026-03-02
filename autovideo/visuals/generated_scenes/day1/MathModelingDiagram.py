from manim import *

class MathModelingDiagram(Scene):
    def construct(self):
        # Background remains black (default)

        # Left side: speech bubbles with Chinese words
        bubble1 = RoundedRectangle(corner_radius=0.3, width=4, height=2, color=BLUE, fill_opacity=0.1)
        bubble1.shift(LEFT * 4 + UP * 1.5)
        text1 = Text("语音信号", font="Microsoft YaHei", color=BLUE).scale(0.6)
        text1.move_to(bubble1.get_center())

        bubble2 = RoundedRectangle(corner_radius=0.3, width=4, height=2, color=TEAL, fill_opacity=0.1)
        bubble2.shift(LEFT * 4 + DOWN * 0.5)
        text2 = Text("环境噪声", font="Microsoft YaHei", color=TEAL).scale(0.6)
        text2.move_to(bubble2.get_center())

        # Speech bubble tails
        tail1 = Polygon(
            bubble1.get_bottom() + DOWN * 0.2,
            bubble1.get_bottom() + DOWN * 0.6 + LEFT * 0.3,
            bubble1.get_bottom() + DOWN * 0.6 + RIGHT * 0.3,
            color=BLUE, fill_opacity=0.1
        )
        tail1.set_stroke(width=0)
        tail2 = Polygon(
            bubble2.get_bottom() + DOWN * 0.2,
            bubble2.get_bottom() + DOWN * 0.6 + LEFT * 0.3,
            bubble2.get_bottom() + DOWN * 0.6 + RIGHT * 0.3,
            color=TEAL, fill_opacity=0.1
        )
        tail2.set_stroke(width=0)

        left_group = VGroup(bubble1, bubble2, tail1, tail2, text1, text2)

        # Right side: abstract probability curves and P_w
        # Axes for curve sketch
        axes = NumberPlane(
            x_range=[-2, 2, 1],
            y_range=[-0.5, 1.5, 0.5],
            background_line_style={"stroke_opacity": 0.2},
            axis_config={"include_ticks": False, "stroke_width": 1}
        ).scale(0.7).shift(RIGHT * 3.5)

        # Two smooth probability-like curves
        curve1 = FunctionGraph(
            lambda x: 0.8 * (1 - (x/1.5)**2) if abs(x) < 1.5 else 0,
            x_range=[-1.5, 1.5],
            color=YELLOW,
            stroke_width=3
        ).move_to(axes.c2p(0, 0)).shift(UP * 0.2)

        curve2 = FunctionGraph(
            lambda x: 0.5 * (1 - (x/2)**4),
            x_range=[-2, 2],
            color=PURPLE,
            stroke_width=3
        ).move_to(axes.c2p(0, 0)).shift(DOWN * 0.1)

        # Greek letter P_w
        p_w = MathText(r"P_w", color=RED).scale(1.4).next_to(axes, UP, buff=0.5)

        right_group = VGroup(axes, curve1, curve2, p_w)

        # Arrow connecting left to right
        arrow = Arrow(
            left_group.get_right(),
            right_group.get_left(),
            buff=0.3,
            color=GREY_C,
            stroke_width=3,
            tip_length=0.25
        )
        arrow_label = Text("数学建模", font="Microsoft YaHei", color=GREY_C).scale(0.6).next_to(arrow, UP, buff=0.2)

        # Assemble full diagram
        diagram = VGroup(left_group, arrow, arrow_label, right_group)

        # Animation
        self.play(
            Create(bubble1), Write(text1), FadeIn(tail1),
            Create(bubble2), Write(text2), FadeIn(tail2),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            Create(axes),
            Create(curve1),
            Create(curve2),
            Write(p_w),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            GrowArrow(arrow),
            Write(arrow_label),
            run_time=1.5
        )
        self.wait(1)

        # Optional subtle emphasis
        self.play(
            bubble1.animate.set_fill(BLUE, opacity=0.2),
            bubble2.animate.set_fill(TEAL, opacity=0.2),
            curve1.animate.set_color(YELLOW_E),
            curve2.animate.set_color(PURPLE_A),
            p_w.animate.set_color(RED_E),
            run_time=1
        )
        self.wait(1)
