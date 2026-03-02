"""Manim scene definitions used by AutoVideo."""

from manim import *
import numpy as np
import random


class TokenizationScene(Scene):
    """Text -> token IDs."""

    def construct(self):
        title = Text("Tokenization", font_size=48, color=BLUE).to_edge(UP)
        words = ["Apple", "is", "a", "fruit"]
        ids = ["[2034]", "[318]", "[64]", "[14314]"]

        word_group = VGroup(*[Text(w, font_size=40) for w in words]).arrange(RIGHT, buff=0.5).shift(UP * 0.8)
        id_group = VGroup(*[Text(t, font_size=34, color=GREEN) for t in ids]).arrange(RIGHT, buff=0.35).shift(DOWN * 1.0)
        arrow = Arrow(word_group.get_bottom(), id_group.get_top(), color=YELLOW, buff=0.2)

        self.play(Write(title))
        self.play(Write(word_group))
        self.play(GrowArrow(arrow))
        for w, tid in zip(word_group, id_group):
            self.play(TransformFromCopy(w, tid), run_time=0.5)
        self.wait(1.5)


class LogitsScene(Scene):
    """Probability bars for candidate tokens."""

    def construct(self):
        title = Text("Logits -> Probabilities", font_size=44, color=BLUE).to_edge(UP)
        labels = ["Apple", "Banana", "Car", "Dog", "Cat"]
        probs = [0.72, 0.15, 0.06, 0.04, 0.03]
        colors = [GREEN, YELLOW, ORANGE, RED, PURPLE]

        bars = VGroup()
        name_labels = VGroup()
        prob_labels = VGroup()

        bar_width = 0.8
        max_height = 3.8
        start_x = -3.0
        for i, (label, prob, color) in enumerate(zip(labels, probs, colors)):
            x = start_x + i * 1.5
            h = prob * max_height
            bar = Rectangle(
                width=bar_width,
                height=h,
                fill_color=color,
                fill_opacity=0.85,
                stroke_color=WHITE,
                stroke_width=1.2,
            ).move_to([x, -2.2 + h / 2, 0])
            bars.add(bar)
            name_labels.add(Text(label, font_size=20).next_to(bar, DOWN, buff=0.12))
            prob_labels.add(Text(f"{prob:.0%}", font_size=22, color=color).next_to(bar, UP, buff=0.1))

        self.play(Write(title))
        for bar, lbl, plbl in zip(bars, name_labels, prob_labels):
            self.play(GrowFromEdge(bar, DOWN), FadeIn(lbl), FadeIn(plbl), run_time=0.45)

        highlight = SurroundingRectangle(bars[0], color=YELLOW, buff=0.1)
        winner = Text("Top candidate", font_size=26, color=YELLOW).next_to(bars[0], RIGHT, buff=0.4)
        self.play(Create(highlight), Write(winner))
        self.wait(1.5)


class AttentionScene(Scene):
    """Simple self-attention sketch."""

    def construct(self):
        title = Text("Self-Attention", font_size=48, color=BLUE).to_edge(UP)
        words = ["The", "cat", "sat", "on", "the", "mat"]
        group = VGroup(*[Text(w, font_size=36) for w in words]).arrange(RIGHT, buff=0.6).shift(UP * 0.5)

        self.play(Write(title))
        self.play(Write(group))

        focus = SurroundingRectangle(group[1], color=YELLOW, buff=0.1)
        self.play(Create(focus))

        weights = [0.05, 1.0, 0.3, 0.1, 0.05, 0.5]
        lines = VGroup()
        for i, (wobj, w) in enumerate(zip(group, weights)):
            if i == 1:
                continue
            line = Line(
                group[1].get_bottom(),
                wobj.get_bottom(),
                color=interpolate_color(BLUE, RED, w),
                stroke_width=max(1, w * 6),
                stroke_opacity=min(1.0, w * 1.5),
            ).shift(DOWN * 0.3)
            lines.add(line)

        self.play(Create(lines), run_time=1.5)
        note = Text('"cat" strongly attends to "mat"', font_size=24, color=GREY_B).to_edge(DOWN)
        self.play(FadeIn(note))
        self.wait(1.5)


class MathematicalFormula(Scene):
    """Fallback formula scene without LaTeX."""

    def construct(self):
        title = Text("Language Modeling", font_size=46, color=BLUE).to_edge(UP)
        formula = Text("P(w_n | w_1 ... w_{n-1})", font_size=54, color=YELLOW)
        desc = Text("Predicting next word from context", font_size=30, color=WHITE).next_to(formula, DOWN, buff=0.9)

        self.play(Write(title))
        self.play(FadeIn(formula, shift=UP))
        self.play(Write(desc))
        self.wait(1.6)


class ProbabilityVisualization(LogitsScene):
    """Alias kept for backward compatibility."""

    pass


class TextDefinition(Scene):
    def construct(self):
        self.camera.background_color = "#1E2B33"

        full_text = Text("Large Language Model", font="Arial", font_size=44, color=WHITE)
        acronym = Text("LLM", font="Arial", font_size=88, weight=BOLD, color=YELLOW_E).move_to(full_text)

        self.play(Write(full_text), run_time=1.2)
        self.wait(0.3)
        self.play(ReplacementTransform(full_text, acronym), run_time=1.0)
        self.wait(0.3)

        for _ in range(2):
            self.play(acronym.animate.set_stroke(GOLD, width=5, opacity=0.75).scale(1.04), run_time=0.45)
            self.play(acronym.animate.set_stroke(YELLOW_D, width=3, opacity=1.0).scale(0.96), run_time=0.45)

        self.wait(0.8)


class ScaleBarAnimation(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        bar = Line(LEFT * 3, RIGHT * 3, color=WHITE, stroke_width=6)

        small_label = Text("Small", font_size=24, color=BLUE).next_to(bar.get_left(), DOWN, buff=0.5)
        medium_label = Text("Medium", font_size=24, color=GOLD).next_to(bar.get_center(), DOWN, buff=0.5)
        large_label = Text("Large", font_size=24, color=RED).next_to(bar.get_right(), DOWN, buff=0.5)

        self.play(Create(bar), run_time=1.3)
        self.play(Write(small_label), run_time=0.6)
        self.play(bar.animate.stretch_to_fit_width(6.5), Write(medium_label), run_time=1.0)
        self.play(bar.animate.stretch_to_fit_width(9), Write(large_label), run_time=1.0)
        self.wait(0.3)

        llm_label = Text("LLM", font_size=36, color=YELLOW, weight=BOLD).move_to(large_label)
        self.play(Transform(large_label, llm_label), run_time=0.8)

        theta_symbols = VGroup(
            *[
                Text("θ", font_size=18, color=TEAL_E).move_to(
                    llm_label.get_center()
                    + np.array(
                        [
                            np.cos(angle) * np.random.uniform(0.8, 2.0),
                            np.sin(angle) * np.random.uniform(0.8, 2.0),
                            0,
                        ]
                    )
                )
                for angle in np.linspace(0, TAU, 36)
            ]
        )
        self.play(LaggedStart(*[FadeIn(t, scale=0.2) for t in theta_symbols], lag_ratio=0.03), run_time=1.5)
        self.wait(0.8)


class ParameterSymbol3D(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        ring = Circle(radius=2.0, color=BLUE_E, stroke_width=3).set_opacity(0.75)
        theta = Text("θ", font_size=140, color=WHITE)
        label = Text("Parameters", font_size=36, color=BLUE).next_to(theta, DOWN, buff=1.0)
        floats = VGroup(
            Text("7B", font_size=28, color=YELLOW).shift(UP * 2 + LEFT * 2.5),
            Text("70B", font_size=28, color=GREEN).shift(DOWN * 1.8 + RIGHT * 2.2),
            Text("1T+", font_size=28, color=ORANGE).shift(UP * 0.5 + RIGHT * 3),
        )

        self.play(Create(ring), FadeIn(theta), run_time=1.2)
        self.play(Write(label), FadeIn(floats), run_time=1.0)
        self.play(Rotate(ring, angle=PI), theta.animate.scale(1.08).set_color(YELLOW_E), run_time=1.2)
        self.play(theta.animate.scale(0.93).set_color(WHITE), run_time=0.8)
        self.wait(1.0)


class MathChalkboard(Scene):
    def construct(self):
        board = Rectangle(
            height=6,
            width=10,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=GRAY,
            stroke_width=2,
        )
        self.add(board)

        eq1 = Text("Model = f(Language)", font_size=52, color=WHITE)
        eq2 = Text("P(next token | context)", font_size=54, color=YELLOW_E)
        eq1.move_to(ORIGIN)
        eq2.move_to(ORIGIN)

        self.play(Write(eq1), run_time=2)
        self.wait(0.8)
        self.play(Transform(eq1, eq2), run_time=1.8)
        self.wait(1.4)


class PhysicsVsLM(Scene):
    def construct(self):
        title = Text("Physics vs Language Models", font_size=32, color=YELLOW).to_edge(UP, buff=0.5)
        self.play(Write(title))

        hline = Line(LEFT * 7, RIGHT * 7, stroke_width=1, color=GRAY).move_to(ORIGIN)
        vline = Line(UP * 3.5, DOWN * 3.5, stroke_width=1, color=GRAY).move_to(ORIGIN)
        left_label = Text("Physics: Trajectory", font_size=24).to_corner(UL, buff=1.2)
        right_label = Text("LM: Token Probability", font_size=24).to_corner(UR, buff=1.2)
        self.play(Write(left_label), Write(right_label), Create(hline), Create(vline))

        ax_left = Axes(
            x_range=[-1, 10, 1],
            y_range=[-2, 6, 1],
            x_length=5,
            y_length=4,
            axis_config={"color": BLUE, "include_ticks": False},
        ).shift(LEFT * 3.5 + DOWN * 0.5)
        parabola = ax_left.plot(lambda x: x - 0.1 * x**2, x_range=[0, 10], color=BLUE, stroke_width=3)
        eq_physics = Text("y = x - 0.1x^2", font_size=28, color=BLUE).next_to(ax_left, DOWN, buff=0.3)

        ax_right = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1.2, 0.2],
            x_length=5,
            y_length=4,
            axis_config={"color": GREEN, "include_ticks": False},
        ).shift(RIGHT * 3.5 + DOWN * 0.5)

        def prob_curve(x):
            return np.exp(-0.5 * ((x - 5) / 1.5) ** 2)

        prob_graph = ax_right.plot(prob_curve, x_range=[0, 10], color=GREEN, stroke_width=3)
        eq_lm = Text("P(token | context)", font_size=24, color=GREEN).next_to(ax_right, DOWN, buff=0.3)

        self.play(Create(ax_left), Create(ax_right), Write(eq_physics), Write(eq_lm))
        self.play(Create(parabola, run_time=1.8), Create(prob_graph, run_time=1.8))

        context_label = Text("Context", font_size=20).next_to(ax_right, UP + LEFT, buff=0.2)
        peak = ax_right.c2p(5, prob_curve(5))
        next_token_label = Text("Next token", font_size=20, color=YELLOW).next_to(peak, UP, buff=0.2)
        arrow = Arrow(
            start=ax_right.c2p(2, 0.1),
            end=peak,
            buff=0.1,
            stroke_width=2,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.1,
        )
        self.play(Write(context_label), GrowArrow(arrow), Write(next_token_label))
        self.wait(1.2)


class NextTokenPrediction(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        input_text = Text("I love", font_size=48, color=WHITE).move_to(LEFT * 4)
        arrow = Arrow(start=input_text.get_right(), end=RIGHT * 2.5, buff=0.2, color=BLUE, stroke_width=3)

        you_text = Text("you", font_size=48, color=GREEN)
        you_prob = Text("99%", font_size=36, color=GREEN)
        you_group = VGroup(you_text, you_prob).arrange(DOWN, buff=0.2)

        eat_text = Text("eat", font_size=48, color=RED)
        eat_prob = Text("0.1%", font_size=36, color=RED)
        eat_group = VGroup(eat_text, eat_prob).arrange(DOWN, buff=0.2)

        VGroup(you_group, eat_group).arrange(RIGHT, buff=2.5).move_to(RIGHT * 3.5)
        label = Text("Next Token Prediction", font_size=32, color=YELLOW).to_edge(UP, buff=0.5)

        self.play(Write(input_text), run_time=0.9)
        self.play(GrowArrow(arrow), run_time=0.8)
        self.play(FadeIn(you_group), FadeIn(eat_group), run_time=0.9)

        you_text.save_state()
        you_prob.save_state()
        you_text.generate_target()
        you_prob.generate_target()
        you_text.target.scale(1.3).set_color(GREEN_E)
        you_prob.target.scale(1.2).set_color(GREEN_E)
        self.play(
            MoveToTarget(you_text),
            MoveToTarget(you_prob),
            you_text.animate.set_stroke(color=GREEN_A, width=2),
            you_prob.animate.set_stroke(color=GREEN_A, width=1.5),
            run_time=1.0,
        )
        self.play(Restore(you_text), Restore(you_prob), run_time=0.9)

        self.play(Write(label))
        self.wait(1.0)


class ProbabilityBarChart(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[0, 1.1, 0.2],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": False},
            y_axis_config={"include_ticks": False},
        ).to_edge(DOWN, buff=0.5)

        x_positions = [1, 2]
        labels = ["you", "eat"]
        heights = [0.99, 0.001]
        colors = [GREEN, RED]

        bars = VGroup()
        for x, h, c in zip(x_positions, heights, colors):
            bar = Rectangle(
                width=0.5,
                height=h * axes.y_length,
                fill_color=c,
                fill_opacity=0.8,
                stroke_color=c,
                stroke_width=2,
            ).move_to(axes.c2p(x, h / 2))
            bars.add(bar)

        label_texts = VGroup(
            *[
                Text(label, font="Arial", weight=BOLD, font_size=28).next_to(axes.c2p(x, 0), DOWN, buff=0.3)
                for x, label in zip(x_positions, labels)
            ]
        )
        y_label = Text("Probability (%)", font="Arial", font_size=24).rotate(90 * DEGREES).next_to(axes, LEFT, buff=0.5)

        self.play(Create(axes), Write(y_label))
        self.play(DrawBorderThenFill(bars[0]))
        self.play(DrawBorderThenFill(bars[1]))
        self.play(Write(label_texts))

        value_texts = VGroup(
            Text("99%", font="Arial", weight=BOLD, font_size=24, color=GREEN).move_to(axes.c2p(1, 1.02)),
            Text("0.1%", font="Arial", weight=BOLD, font_size=24, color=RED).move_to(axes.c2p(2, 0.04)),
        )
        self.play(Write(value_texts))
        self.wait(1.0)


class TypewriterOutput(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        content = "I love you"
        love_text = Text(content[0], font="Arial", font_size=48, color=WHITE).move_to(ORIGIN)
        self.play(Write(love_text), run_time=0.12)
        for i in range(2, len(content) + 1):
            nxt = Text(content[:i], font="Arial", font_size=48, color=WHITE).move_to(ORIGIN)
            self.play(Transform(love_text, nxt), run_time=0.09)
        self.wait(0.3)

        self.play(love_text.animate.scale(1.05).set_color("#FFD700"), rate_func=there_and_back, run_time=0.8)
        self.play(love_text.animate.set_color(WHITE), run_time=0.3)

        eat_text = Text("eat", font="Arial", font_size=36, color=GRAY).next_to(love_text, DOWN, buff=1.0)
        self.play(FadeIn(eat_text, shift=UP * 0.3, scale=0.8), run_time=0.6)
        x_icon = Cross(stroke_width=6, color=RED).scale(0.8).move_to(eat_text.get_center())
        self.play(FadeOut(eat_text, scale=0.5, shift=DOWN * 0.3, run_time=0.7), Create(x_icon, run_time=0.7))
        self.wait(0.5)


class CrossedOutModalities(Scene):
    def construct(self):
        camera = VGroup(
            Rectangle(width=1.2, height=0.8, fill_color=WHITE, fill_opacity=1, stroke_color=BLACK),
            Circle(radius=0.2, fill_color=BLACK, fill_opacity=1).shift(LEFT * 0.3 + UP * 0.1),
            Rectangle(width=0.4, height=0.15, fill_color=BLACK, fill_opacity=1).shift(DOWN * 0.25),
        ).scale(0.7)

        mic = VGroup(
            Line(UP * 0.6, DOWN * 0.4, stroke_width=4),
            Circle(radius=0.25, fill_color=WHITE, fill_opacity=1, stroke_color=BLACK).shift(UP * 0.6),
            Rectangle(width=0.5, height=0.1, fill_color=BLACK, fill_opacity=1).shift(DOWN * 0.2),
        ).scale(0.7)

        film = VGroup(
            Circle(radius=0.4, fill_color=WHITE, fill_opacity=1, stroke_color=BLACK),
            Circle(radius=0.2, fill_color=BLACK, fill_opacity=1, stroke_color=BLACK),
            Circle(radius=0.07, fill_color=BLACK, fill_opacity=1).shift(LEFT * 0.25),
            Circle(radius=0.07, fill_color=BLACK, fill_opacity=1).shift(RIGHT * 0.25),
            Rectangle(width=0.5, height=0.05, fill_color=BLACK, fill_opacity=1).rotate(PI / 2),
        ).scale(0.7)

        icons = VGroup(camera, mic, film).arrange(RIGHT, buff=1.2)

        def make_x(obj):
            return Cross(stroke_color=RED, stroke_width=12).scale(0.4).move_to(obj.get_center())

        x_camera = make_x(camera)
        x_mic = make_x(mic)
        x_film = make_x(film)
        text_only = Text("TEXT ONLY", font="Arial", weight=BOLD, font_size=36, color=WHITE)

        self.play(FadeIn(camera, mic, film), FadeIn(x_camera, x_mic, x_film), run_time=1.3)
        self.play(Write(text_only.next_to(icons, DOWN, buff=1.2)))
        self.wait(1.6)


class TextStreamFlow(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        rows = 10
        lines = []
        for i in range(rows):
            chars = "".join(random.choice("abcdefghijklmnopqrstuvwxyz ") for _ in range(48))
            txt = Text(chars, font_size=16, color=GREY_A).move_to(UP * (2.8 - i * 0.6))
            lines.append(txt)

        group = VGroup(*lines)
        self.play(FadeIn(group), run_time=0.8)
        self.play(*[line.animate.shift(RIGHT * 1.6) for line in lines], run_time=3.0, rate_func=linear)
        self.play(*[line.animate.shift(LEFT * 0.9) for line in lines], run_time=2.0, rate_func=smooth)
        self.wait(1.0)


class ModalityIconsSequence(Scene):
    def construct(self):
        self.camera.background_color = BLACK

        eye = VGroup(
            Ellipse(width=1.8, height=1.0, color=BLUE, stroke_width=4),
            Circle(radius=0.22, color=BLUE, fill_opacity=1),
        ).scale(0.8)
        vision_label = Text("Vision Model", font="Microsoft YaHei", color=WHITE).next_to(eye, DOWN, buff=0.3)

        ear = VGroup(
            Arc(radius=0.65, start_angle=-PI / 2, angle=PI * 1.45, color=GREEN, stroke_width=4),
            Arc(radius=0.33, start_angle=-PI / 2, angle=PI * 1.3, color=GREEN_A, stroke_width=3),
            Dot(radius=0.04, color=GREEN_B).shift(DOWN * 0.55),
        ).scale(0.9)
        audio_label = Text("Audio Model", font="Microsoft YaHei", color=WHITE).next_to(ear, DOWN, buff=0.3)

        brain = VGroup(
            Circle(radius=0.34, color=PURPLE_B),
            Circle(radius=0.34, color=PURPLE_B).shift(LEFT * 0.33),
            Circle(radius=0.34, color=PURPLE_B).shift(RIGHT * 0.33),
            RoundedRectangle(width=0.95, height=0.45, corner_radius=0.18, color=PURPLE_B).shift(DOWN * 0.28),
        ).set_stroke(width=3).scale(0.9)
        multimodal_label = Text("Multimodal", font="Microsoft YaHei", color=WHITE).next_to(brain, DOWN, buff=0.3)

        vision_group = VGroup(eye, vision_label).move_to(ORIGIN)
        audio_group = VGroup(ear, audio_label).move_to(ORIGIN)
        multimodal_group = VGroup(brain, multimodal_label).move_to(ORIGIN)

        self.play(FadeIn(vision_group))
        self.wait(1.2)
        self.play(Transform(vision_group, audio_group))
        self.wait(1.2)
        self.play(Transform(vision_group, multimodal_group))
        self.wait(1.6)


# ==================== Auto-Generated ====================
from manim import *

class TextDefinitionScene(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Main text with 'LLM' in gold
        full_text = Text("Large Language Model (LLM)", font="Arial", font_size=36)
        llm_part = Text("LLM", font="Arial", font_size=42, color=GOLD).move_to(
            full_text[21:24].get_center()
        )
        
        # Create base text without LLM
        base_text = Text("Large Language Model ()", font="Arial", font_size=36)
        
        # Abstract language symbols
        symbols = VGroup(
            Text("[", font_size=28, color=GREY_A),
            Text("]", font_size=28, color=GREY_A),
            Text(",", font_size=32, color=GREY_A),
            Text("∼", font_size=24, color=BLUE_B),
            Text("⋯", font_size=28, color=TEAL_A),
        )
        
        # Position symbols around the text
        symbols.arrange_in_grid(rows=1, cols=5, buff=0.8)
        symbols.move_to(ORIGIN + DOWN * 1.5)

        # Animate
        self.play(Write(base_text), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(llm_part, scale=1.2, shift=UP*0.1), run_time=1)
        self.play(
            llm_part.animate.set_stroke(GOLD_E, width=2, opacity=0.8),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(FadeIn(symbols, shift=UP*0.3, lag_ratio=0.2), run_time=2)
        self.wait(1.5)


# ==================== Auto-Generated ====================
from manim import *

class ParameterScaleScene(Scene):
    def construct(self):
        # Initial number
        num = Text("175B", font_size=80, color=WHITE)
        
        # "Parameters" label
        params_label = Text("Parameters", font_size=60, color=BLUE)
        
        # Neural network nodes (circles) arranged in a loose ring around the label
        nodes = VGroup()
        n_nodes = 8
        radius = 2.5
        for i in range(n_nodes):
            angle = i * TAU / n_nodes
            node = Circle(radius=0.2, color=YELLOW, fill_opacity=0.7)
            node.move_to(radius * np.array([np.cos(angle), np.sin(angle), 0]))
            nodes.add(node)
        
        # Position label at center
        params_label.move_to(ORIGIN)
        
        # Animate zoom-in on "175B"
        self.play(Write(num), run_time=1.5)
        self.wait(0.5)
        self.play(num.animate.scale(2.5).move_to(ORIGIN), run_time=2)
        self.wait(0.5)
        
        # Transform to "Parameters" and fade in nodes
        self.play(
            Transform(num, params_label),
            FadeIn(nodes, scale=0.5),
            run_time=2
        )
        
        # Pulsing animation for nodes
        pulse_animations = []
        for node in nodes:
            pulse_animations.append(
                node.animate.scale(1.3).set_color(ORANGE).set_run_time(1.5)
            )
            pulse_animations.append(
                node.animate.scale(1/1.3).set_color(YELLOW).set_run_time(1.5)
            )
        
        # Loop pulsing twice
        for _ in range(2):
            self.play(*pulse_animations, run_time=3)
        
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class LanguageModelingEquation(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BLACK

        # Define equation with proper spacing and fonts
        eq = MathTex(
            "P(\\text{word} \\mid \\text{context}) = \\text{softmax}(W \\cdot h + b)",
            font_size=36
        ).move_to(UP * 2)

        # Context window (sliding bar)
        context_bar = Rectangle(
            height=0.4,
            width=4.0,
            color=YELLOW,
            fill_opacity=0.2,
            stroke_width=2
        ).next_to(eq, DOWN, buff=1.5)

        # Tokens inside context window (sliding tokens)
        tokens = ["The", "cat", "sat", "on", "the", "mat"]
        token_mobs = VGroup(*[
            Text(token, font_size=24, color=WHITE).move_to(
                context_bar.get_left() + RIGHT * (0.8 * i + 0.4)
            )
            for i, token in enumerate(tokens)
        ])

        # Highlight current prediction position (rightmost slot)
        pred_arrow = Arrow(
            start=context_bar.get_right() + LEFT * 0.3 + DOWN * 0.3,
            end=context_bar.get_right() + LEFT * 0.3 + UP * 0.3,
            buff=0,
            stroke_width=2,
            color=BLUE
        )
        pred_label = Text("predict", font_size=20, color=BLUE).next_to(pred_arrow, UP, buff=0.1)

        # Animate
        self.play(Write(eq))
        self.wait(0.5)
        self.play(Create(context_bar), FadeIn(token_mobs))
        self.wait(0.5)

        # Slide context window left-to-right by shifting tokens gradually
        shift_amount = 0.8
        for _ in range(3):
            self.play(
                token_mobs.animate.shift(LEFT * shift_amount),
                run_time=1.2,
                rate_func=linear
            )
            self.wait(0.3)

        # Highlight prediction position
        self.play(GrowArrow(pred_arrow), Write(pred_label))
        self.wait(1)

        # Fade out non-equation elements to focus on equation
        self.play(
            FadeOut(context_bar),
            FadeOut(token_mobs),
            FadeOut(pred_arrow),
            FadeOut(pred_label)
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class NextTokenPredictionScene(Scene):
    def construct(self):
        # Input text
        input_text = Text("我爱", font="Microsoft YaHei", font_size=48, color=WHITE)
        
        # Output text
        output_text = Text("你", font="Microsoft YaHei", font_size=48, color=YELLOW)
        
        # Arrow
        arrow = Arrow(start=input_text.get_right(), end=output_text.get_left(), buff=0.5, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        
        # Position elements horizontally
        input_text.move_to(LEFT * 3)
        output_text.move_to(RIGHT * 3)
        arrow.next_to(input_text, RIGHT, buff=0.8)
        output_text.next_to(arrow, RIGHT, buff=0.8)
        
        # Label
        label = Text("Next Token Prediction", font="Microsoft YaHei", font_size=24, color=GRAY)
        label.next_to(arrow, DOWN, buff=1.2)
        
        # Glow effect for label
        label_glow = label.copy().set_color(YELLOW).set_opacity(0.3).scale(1.05)
        
        # Animation
        self.play(Write(input_text), run_time=0.8)
        self.wait(0.5)
        self.play(GrowArrow(arrow), run_time=0.7)
        self.wait(0.3)
        self.play(Write(output_text), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(label), run_time=0.5)
        self.play(
            label.animate.set_color(YELLOW),
            FadeIn(label_glow),
            rate_func=there_and_back,
            run_time=1.5
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class ProbabilityHeatmap(Scene):
    def construct(self):
        # Chinese text: "你好世界" — using a common font supporting CJK
        text = Text("你好世界", font="Microsoft YaHei", font_size=48)
        text.move_to(ORIGIN)

        # Split into individual characters for independent styling
        chars = VGroup(*[Text(c, font="Microsoft YaHei", font_size=48) for c in "你好世界"])
        chars.arrange(RIGHT, buff=0.5)
        chars.move_to(ORIGIN)

        # Dim all characters initially
        for char in chars:
            char.set_color(GREY_A)

        # Highlight "你" (first character) with red-hot color and add 99% label
        you_char = chars[0]
        you_char.set_color(RED_E).scale(1.2)
        
        # Create 99% label
        percent_label = Text("99%", font="Arial", font_size=36, color=RED_C)
        percent_label.next_to(you_char, UP, buff=0.3)

        # Heatmap-like background effect: subtle rectangle behind "你"
        heat_rect = Rectangle(
            width=you_char.width * 1.4,
            height=you_char.height * 1.6,
            fill_color=RED_B,
            fill_opacity=0.3,
            stroke_width=0
        )
        heat_rect.move_to(you_char.get_center())

        # Animation
        self.play(
            Write(chars),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            you_char.animate.set_color(RED_E).scale(1.2),
            FadeIn(heat_rect),
            FadeIn(percent_label),
            run_time=1.2
        )
        self.wait(1.5)
        self.play(
            FadeOut(heat_rect),
            FadeOut(percent_label),
            you_char.animate.set_color(RED_A).scale(0.9),
            run_time=0.8
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class TextStreamScene(Scene):
    def construct(self):
        # Set background to black for contrast
        self.camera.background_color = BLACK

        # Define ASCII characters to use (letters, digits, spaces, punctuation)
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .,;:!?-_=+()[]{}<>\"'`~@#$%^&*\\|/"
        
        # Create a stream of characters — multiple rows flowing at different speeds
        rows = []
        num_rows = 5
        row_heights = [i * 0.8 for i in range(num_rows)]
        
        for i in range(num_rows):
            # Each row is a long string of random ASCII chars
            line_chars = "".join(chars[int(self.renderer.time * (1 + i * 0.3) + j) % len(chars)] for j in range(80))
            text_line = Text(line_chars, font="Monospace", font_size=24, color=TEAL_A)
            text_line.move_to(UP * row_heights[i] + RIGHT * 20)  # Start far right
            rows.append(text_line)

        # Add all rows to the scene
        for row in rows:
            self.add(row)

        # Animate each row moving left continuously for ~8 seconds
        duration = 8.0
        for row in rows:
            shift_distance = 40  # Enough to scroll across screen
            self.play(
                row.animate.shift(LEFT * shift_distance),
                run_time=duration,
                rate_func=linear
            )

        # Optional: loop or fade — but per spec, just flow once
        self.wait(0.5)


# ==================== Auto-Generated ====================
from manim import *

class SplitConceptDiagram(Scene):
    def construct(self):
        # Define split screen
        left_rect = Rectangle(height=6, width=6, color=WHITE, stroke_width=2).to_edge(LEFT, buff=0.5)
        right_rect = Rectangle(height=6, width=6, color=WHITE, stroke_width=2).to_edge(RIGHT, buff=0.5)
        
        # Labels
        nlp_label = Text("NLP", font_size=36, color=BLUE).next_to(left_rect, UP, buff=0.3)
        cv_label = Text("CV", font_size=36, color=GREEN).next_to(right_rect, UP, buff=0.3)
        
        # Left side: speech bubbles and flowing text
        bubble1 = Circle(radius=0.8, color=BLUE, fill_opacity=0.1).move_to(left_rect.get_center() + LEFT * 1.2 + UP * 0.5)
        bubble2 = Circle(radius=0.6, color=BLUE, fill_opacity=0.1).move_to(left_rect.get_center() + RIGHT * 0.8 + DOWN * 0.7)
        tail = Polygon(
            bubble1.get_right(), 
            bubble1.get_right() + RIGHT * 0.4 + UP * 0.2,
            bubble1.get_right() + RIGHT * 0.4 + DOWN * 0.2,
            color=BLUE, fill_opacity=0.1, stroke_width=2
        )
        
        text1 = Text("Hello world!", font_size=20, font="Arial").move_to(bubble1.get_center())
        text2 = Text("Tokenize → Embed", font_size=20, font="Arial").move_to(bubble2.get_center())
        
        # Right side: eye icon with light rays
        eye_center = right_rect.get_center()
        eye_white = Circle(radius=0.8, color=WHITE, fill_opacity=1, stroke_width=2)
        eye_iris = Circle(radius=0.4, color=BLUE, fill_opacity=1).move_to(eye_center)
        eye_pupil = Circle(radius=0.15, color=BLACK, fill_opacity=1).move_to(eye_center)
        eye = VGroup(eye_white, eye_iris, eye_pupil).move_to(eye_center)
        
        # Light rays (4 directional)
        ray_length = 1.2
        rays = VGroup()
        for angle in [0, PI/2, PI, 3*PI/2]:
            ray = Line(
                eye_center,
                eye_center + ray_length * np.array([np.cos(angle), np.sin(angle), 0]),
                color=YELLOW,
                stroke_width=3
            )
            rays.add(ray)
        
        # Animate
        self.play(
            Create(left_rect),
            Create(right_rect),
            Write(nlp_label),
            Write(cv_label),
        )
        self.wait(0.5)
        
        self.play(
            Create(bubble1),
            Create(bubble2),
            Create(tail),
            Write(text1),
            Write(text2),
        )
        self.wait(0.5)
        
        self.play(
            Create(eye),
            Create(rays),
        )
        self.wait(1)
        
        # Subtle flow animation on left text
        self.play(
            text1.animate.shift(UP * 0.1),
            text2.animate.shift(DOWN * 0.1),
            run_time=1.5,
            rate_func=there_and_back
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class PixelToImageTranslation(Scene):
    def construct(self):
        # Left: RGB grid (simplified 3x3)
        grid_text = VGroup()
        rgb_values = [
            ["240,120,80", "235,115,75", "245,130,85"],
            ["180,90,60",  "175,85,55",  "185,95,65"],
            ["120,60,40",  "115,55,35",  "125,65,45"]
        ]
        for i, row in enumerate(rgb_values):
            for j, val in enumerate(row):
                t = Text(val, font_size=16, color=WHITE)
                t.move_to(LEFT * 4 + RIGHT * j * 1.8 + DOWN * i * 1.2)
                grid_text.add(t)
        
        grid_brace = Brace(grid_text, direction=LEFT, buff=0.2)
        grid_label = Text("Pixel Grid\n(RGB values)", font_size=20, color=GRAY).next_to(grid_brace, LEFT)

        # Right: Simple cat image (stylized with shapes)
        cat = VGroup()
        # Head
        head = Circle(radius=1.0, color="#FFD700", fill_opacity=1)
        # Ears
        ear_left = Triangle().scale(0.3).rotate(-30*DEGREES).move_to(head.get_center() + UL * 0.8).set_fill("#FFA500", 1).set_stroke(width=0)
        ear_right = Triangle().scale(0.3).rotate(30*DEGREES).move_to(head.get_center() + UR * 0.8).set_fill("#FFA500", 1).set_stroke(width=0)
        # Eyes
        eye_left = Circle(radius=0.15, color=BLACK, fill_opacity=1).move_to(head.get_center() + LEFT * 0.3 + UP * 0.2)
        eye_right = Circle(radius=0.15, color=BLACK, fill_opacity=1).move_to(head.get_center() + RIGHT * 0.3 + UP * 0.2)
        # Nose
        nose = Triangle().scale(0.1).move_to(head.get_center() + DOWN * 0.1).set_fill(BLACK, 1).set_stroke(width=0)
        # Mouth
        mouth = ArcBetweenPoints(
            head.get_center() + LEFT * 0.3 + DOWN * 0.3,
            head.get_center() + RIGHT * 0.3 + DOWN * 0.3,
            angle=-PI/2
        ).set_stroke(BLACK, width=2)
        cat.add(head, ear_left, ear_right, eye_left, eye_right, nose, mouth)
        cat.move_to(RIGHT * 4)

        cat_label = Text("Reconstructed Image\n(Cat)", font_size=20, color=GRAY).next_to(cat, UP, buff=0.5)

        # Arrow and label
        arrow = Arrow(LEFT * 1.5, RIGHT * 1.5, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.15)
        arrow_label = Text("Vision Model", font_size=24, color=YELLOW).next_to(arrow, UP, buff=0.3)

        # Assemble
        self.play(
            Write(grid_text),
            Write(grid_label),
            GrowFromCenter(grid_brace),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            Create(arrow),
            Write(arrow_label),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            FadeIn(cat),
            Write(cat_label),
            run_time=1.5
        )
        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *

class FeatureHierarchy(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Title
        title = Text("Feature Hierarchy", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Step 1: Grayscale edge map
        edge_text = Text("Edge Map", font_size=24, color=BLUE).shift(UP * 2)
        edge_rect = Rectangle(height=1.2, width=2.5, color=BLUE, stroke_width=2)
        edge_rect.next_to(edge_text, DOWN, buff=0.5)
        edge_label = Text("Grayscale Edges", font_size=18, color=BLUE).next_to(edge_rect, DOWN, buff=0.3)
        
        self.play(FadeIn(edge_text), Create(edge_rect), Write(edge_label))
        self.wait(1)

        # Step 2: Texture heatmap (slightly larger, orange)
        texture_text = Text("Texture Heatmap", font_size=24, color=ORANGE).shift(UP * 0.5)
        texture_rect = Rectangle(height=1.4, width=2.8, color=ORANGE, stroke_width=2)
        texture_rect.next_to(texture_text, DOWN, buff=0.5)
        texture_label = Text("Local Patterns", font_size=18, color=ORANGE).next_to(texture_rect, DOWN, buff=0.3)
        
        self.play(
            FadeIn(texture_text),
            Create(texture_rect),
            Write(texture_label),
            edge_text.animate.shift(LEFT * 3),
            edge_rect.animate.shift(LEFT * 3),
            edge_label.animate.shift(LEFT * 3),
        )
        self.wait(1)

        # Step 3: Object bounding box (green, larger still)
        bbox_text = Text("Object Bounding Box", font_size=24, color=GREEN).shift(DOWN * 1)
        bbox_rect = Rectangle(height=1.6, width=3.0, color=GREEN, stroke_width=2)
        bbox_rect.next_to(bbox_text, DOWN, buff=0.5)
        bbox_label = Text("Cat Region", font_size=18, color=GREEN).next_to(bbox_rect, DOWN, buff=0.3)
        
        self.play(
            FadeIn(bbox_text),
            Create(bbox_rect),
            Write(bbox_label),
            texture_text.animate.shift(LEFT * 3),
            texture_rect.animate.shift(LEFT * 3),
            texture_label.animate.shift(LEFT * 3),
            edge_text.animate.shift(LEFT * 3),
            edge_rect.animate.shift(LEFT * 3),
            edge_label.animate.shift(LEFT * 3),
        )
        self.wait(1)

        # Step 4: Final label 'cat' (bold red text with highlight)
        cat_text = Text("cat", font_size=48, color=RED, weight=BOLD)
        cat_text.shift(DOWN * 3)
        highlight = SurroundingRectangle(cat_text, color=RED, buff=0.3, stroke_width=3, fill_opacity=0.1, fill_color=RED)
        
        self.play(
            FadeIn(cat_text),
            Create(highlight),
            bbox_text.animate.shift(LEFT * 3),
            bbox_rect.animate.shift(LEFT * 3),
            bbox_label.animate.shift(LEFT * 3),
            texture_text.animate.shift(LEFT * 3),
            texture_rect.animate.shift(LEFT * 3),
            texture_label.animate.shift(LEFT * 3),
            edge_text.animate.shift(LEFT * 3),
            edge_rect.animate.shift(LEFT * 3),
            edge_label.animate.shift(LEFT * 3),
        )
        self.wait(1)

        # Arrows between layers
        arrow1 = Arrow(start=RIGHT * 1.5 + UP * 2, end=RIGHT * 1.5 + UP * 0.5, buff=0.1, stroke_width=2, color=WHITE)
        arrow2 = Arrow(start=RIGHT * 1.5 + UP * 0.5, end=RIGHT * 1.5 + DOWN * 1, buff=0.1, stroke_width=2, color=WHITE)
        arrow3 = Arrow(start=RIGHT * 1.5 + DOWN * 1, end=RIGHT * 1.5 + DOWN * 3, buff=0.1, stroke_width=2, color=WHITE)
        
        self.play(GrowArrow(arrow1), GrowArrow(arrow2), GrowArrow(arrow3))
        self.wait(1)

        # Final emphasis
        self.play(
            cat_text.animate.scale(1.2).set_color(YELLOW),
            highlight.animate.set_color(YELLOW),
            run_time=1
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class ScaleGrowthChart(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BLACK

        # Axes
        axes = Axes(
            x_range=[2015, 2025, 2],
            y_range=[0, 10, 2],
            x_length=10,
            y_length=6,
            axis_config={"color": GRAY, "include_numbers": True},
            y_axis_config={"include_ticks": True},
        ).to_edge(DOWN, buff=0.5).to_edge(RIGHT, buff=0.5)

        # Labels
        x_label = Text("Year", font_size=24, color=WHITE).next_to(axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Model Size (B parameters)", font_size=24, color=WHITE).next_to(axes.y_axis, LEFT, buff=0.3).rotate(90)

        # Data points — LLM branch (solid line)
        llm_points = [
            (2017, 0.1), (2018, 0.3), (2019, 1.5), (2020, 3.0), (2021, 6.7), (2022, 8.9), (2023, 9.8), (2024, 10.0)
        ]
        llm_dots = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE, radius=0.1).set_stroke(WHITE, width=2)
            for x, y in llm_points
        ])
        llm_line = VMobject(color=BLUE, stroke_width=3)
        llm_line.set_points_as_corners([axes.c2p(x, y) for x, y in llm_points])

        # LVM branch (dashed line, diverges after 2020)
        lvm_points = [
            (2017, 0.05), (2018, 0.15), (2019, 0.8), (2020, 2.0), (2021, 3.5), (2022, 4.8), (2023, 6.2), (2024, 7.5)
        ]
        lvm_dots = VGroup(*[
            Dot(axes.c2p(x, y), color=GREEN, radius=0.1).set_stroke(WHITE, width=2)
            for x, y in lvm_points
        ])
        lvm_line = DashedVMobject(
            VMobject(color=GREEN, stroke_width=3).set_points_as_corners([axes.c2p(x, y) for x, y in lvm_points]),
            num_dashes=16
        )

        # Glow effect on dots
        def add_glow(dot, color):
            glow = dot.copy().set_color(color).scale(2.5).set_opacity(0.3)
            return VGroup(glow, dot)

        llm_glow_dots = VGroup(*[add_glow(dot, BLUE) for dot in llm_dots])
        lvm_glow_dots = VGroup(*[add_glow(dot, GREEN) for dot in lvm_dots])

        # Labels for branches
        llm_label = Text("LLM", font_size=28, color=BLUE).next_to(llm_dots[-1], UR, buff=0.2)
        lvm_label = Text("LVM", font_size=28, color=GREEN).next_to(lvm_dots[-1], DR, buff=0.2)

        # Title
        title = Text("Model Scale Growth", font_size=36, color=WHITE).to_edge(UP, buff=0.5)

        # Animate
        self.play(Write(title), Write(axes), Write(x_label), Write(y_label))
        self.wait(0.5)

        self.play(Create(llm_line), FadeIn(llm_glow_dots, shift=UP * 0.2))
        self.wait(0.5)
        self.play(Create(lvm_line), FadeIn(lvm_glow_dots, shift=DOWN * 0.2))
        self.wait(0.5)
        self.play(FadeIn(llm_label), FadeIn(lvm_label))
        self.wait(1)

        # Highlight divergence point (2020)
        div_dot = Dot(axes.c2p(2020, 3.0), color=YELLOW, radius=0.15).set_stroke(WHITE, width=3)
        div_glow = div_dot.copy().set_color(YELLOW).scale(3).set_opacity(0.4)
        div_label = Text("Divergence", font_size=24, color=YELLOW).next_to(div_dot, UP, buff=0.3)

        self.play(FadeIn(div_glow), FadeIn(div_dot), FadeIn(div_label))
        self.wait(1.5)


# ==================== Auto-Generated ====================
from manim import *

class VLMFusionDiagram(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Eye-shaped network (vision)
        eye = SVGMobject("eye").scale(1.2).set_color(BLUE).set_stroke(width=2)
        eye_text = Text("Vision", font_size=24, color=BLUE).next_to(eye, DOWN, buff=0.3)

        # Speech-bubble-shaped network (language)
        speech = SVGMobject("speech_bubble").scale(1.2).set_color(GREEN).set_stroke(width=2)
        speech_text = Text("Language", font_size=24, color=GREEN).next_to(speech, DOWN, buff=0.3)

        # Position left and right
        eye_group = VGroup(eye, eye_text).shift(LEFT * 4)
        speech_group = VGroup(speech, speech_text).shift(RIGHT * 4)

        # Brain icon (interconnected fusion)
        brain = SVGMobject("brain").scale(1.5).set_color(PURPLE).set_stroke(width=2)
        brain_text = Text("Multimodal\nFusion", font_size=20, color=WHITE).next_to(brain, DOWN, buff=0.3)

        # Arrows: bidirectional between eye/speech → brain
        arrow_eye_to_brain = Arrow(
            start=eye.get_right(),
            end=brain.get_left(),
            buff=0.2,
            stroke_width=3,
            tip_length=0.2,
            color=YELLOW
        )
        arrow_brain_to_eye = Arrow(
            start=brain.get_left(),
            end=eye.get_right(),
            buff=0.2,
            stroke_width=3,
            tip_length=0.2,
            color=YELLOW
        )

        arrow_speech_to_brain = Arrow(
            start=speech.get_left(),
            end=brain.get_right(),
            buff=0.2,
            stroke_width=3,
            tip_length=0.2,
            color=YELLOW
        )
        arrow_brain_to_speech = Arrow(
            start=brain.get_right(),
            end=speech.get_left(),
            buff=0.2,
            stroke_width=3,
            tip_length=0.2,
            color=YELLOW
        )

        # Animate
        self.play(FadeIn(eye_group), FadeIn(speech_group))
        self.wait(1)

        self.play(
            Create(arrow_eye_to_brain),
            Create(arrow_speech_to_brain),
            Create(arrow_brain_to_eye),
            Create(arrow_brain_to_speech),
        )
        self.wait(1)

        self.play(
            Transform(eye, brain.copy().set_color(PURPLE)),
            Transform(speech, brain.copy().set_color(PURPLE)),
            FadeOut(eye_text),
            FadeOut(speech_text),
            FadeOut(arrow_eye_to_brain),
            FadeOut(arrow_speech_to_brain),
            FadeOut(arrow_brain_to_eye),
            FadeOut(arrow_brain_to_speech),
        )
        self.wait(0.5)

        self.play(FadeIn(brain), FadeIn(brain_text))
        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *

class MultimodalAgent(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Human silhouette (centered, medium size)
        silhouette = SVGMobject("https://upload.wikimedia.org/wikipedia/commons/5/5a/Person_icon.svg").scale(2.5).set_fill(GREY_A, opacity=0.8).set_stroke(WHITE, width=1)
        silhouette.shift(UP * 0.3)

        # Left half: eye + camera feed
        left_eye = Circle(radius=0.3, color=BLUE, fill_opacity=0.7).move_to(silhouette.get_center() + LEFT * 0.8 + UP * 0.4)
        camera_rect = Rectangle(width=1.2, height=0.8, color=BLUE_D, fill_opacity=0.2).next_to(left_eye, DOWN, buff=0.2)
        camera_grid = VGroup(*[
            Line(
                camera_rect.get_corner(UL) + RIGHT * i * 0.3,
                camera_rect.get_corner(DL) + RIGHT * i * 0.3,
                stroke_width=0.5, color=BLUE_B
            )
            for i in range(5)
        ] + [
            Line(
                camera_rect.get_corner(UL) + DOWN * j * 0.2,
                camera_rect.get_corner(UR) + DOWN * j * 0.2,
                stroke_width=0.5, color=BLUE_B
            )
            for j in range(5)
        ])
        camera_feed = VGroup(camera_rect, camera_grid).scale(0.9)

        # Right half: speech bubble + text stream
        bubble = SVGMobject("https://upload.wikimedia.org/wikipedia/commons/6/6c/Speech_bubble.svg").scale(0.8).set_fill(TEAL_A, opacity=0.7).set_stroke(TEAL_C, width=1)
        bubble.move_to(silhouette.get_center() + RIGHT * 0.8 + UP * 0.3)
        text_stream = Text("Hello\nVision\nText\nAI", font_size=16, font="monospace", color=WHITE).move_to(bubble.get_center()).shift(DOWN * 0.1)

        # Center pulsing 'VLM' logo
        vlm_logo = Text("VLM", font_size=40, color=YELLOW, font="Arial Black").move_to(silhouette.get_center())
        pulse_circle = Circle(radius=0.6, color=YELLOW, fill_opacity=0.15, stroke_width=2).move_to(vlm_logo.get_center())

        # Group halves
        left_half = VGroup(left_eye, camera_feed).move_to(silhouette.get_center() + LEFT * 0.5)
        right_half = VGroup(bubble, text_stream).move_to(silhouette.get_center() + RIGHT * 0.5)

        # Assemble full figure
        agent = VGroup(silhouette, left_half, right_half, pulse_circle, vlm_logo)

        # Animation
        self.play(FadeIn(silhouette), run_time=1.2)
        self.wait(0.5)
        self.play(
            FadeIn(left_eye),
            Create(camera_rect),
            FadeIn(camera_grid),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            FadeIn(bubble),
            Write(text_stream),
            run_time=1
        )
        self.wait(0.5)
        self.play(
            FadeIn(pulse_circle),
            Write(vlm_logo),
            run_time=1
        )

        # Pulse animation
        for _ in range(3):
            self.play(
                pulse_circle.animate.scale(1.2).set_opacity(0.3),
                vlm_logo.animate.set_color(GOLD),
                run_time=0.6
            )
            self.play(
                pulse_circle.animate.scale(1/1.2).set_opacity(0.15),
                vlm_logo.animate.set_color(YELLOW),
                run_time=0.6
            )

        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class WordBreakdown(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Main word "Prompt"
        prompt = Text("Prompt", font_size=72, color=WHITE)
        prompt.move_to(ORIGIN)

        # Definitions
        hint = Text("Hint", font_size=48, color=YELLOW)
        urge = Text("Urge", font_size=48, color=BLUE)
        
        # Position definitions below with spacing
        hint.next_to(prompt, DOWN, buff=1.5).shift(LEFT * 2.5)
        urge.next_to(prompt, DOWN, buff=1.5).shift(RIGHT * 2.5)

        # Spotlight effect: two circular gradients (simulated with fading rings)
        spotlight_left = Circle(radius=3.5, color=WHITE, fill_opacity=0, stroke_width=0).move_to(hint.get_center())
        spotlight_right = Circle(radius=3.5, color=WHITE, fill_opacity=0, stroke_width=0).move_to(urge.get_center())

        # Animate spotlight appearance (fading in as soft circles)
        spotlight_left.set_stroke(width=0).set_fill(WHITE, opacity=0)
        spotlight_right.set_stroke(width=0).set_fill(WHITE, opacity=0)

        # Play animation sequence
        self.play(Write(prompt), run_time=1.2)
        self.wait(0.5)

        # Split animation: prompt fades while definitions fade in
        self.play(
            FadeOut(prompt, scale=0.8),
            FadeIn(hint, shift=UP * 0.5, scale=0.8),
            FadeIn(urge, shift=UP * 0.5, scale=0.8),
            run_time=1.5
        )
        self.wait(0.5)

        # Spotlight rings pulse in
        self.play(
            Create(spotlight_left, run_time=1.5),
            Create(spotlight_right, run_time=1.5),
            spotlight_left.animate.set_stroke(YELLOW, width=2).set_fill(YELLOW, opacity=0.1),
            spotlight_right.animate.set_stroke(BLUE, width=2).set_fill(BLUE, opacity=0.1),
        )
        self.wait(0.5)

        # Subtle pulse effect (scale up/down)
        self.play(
            spotlight_left.animate.scale(1.05).set_fill(YELLOW, opacity=0.15),
            spotlight_right.animate.scale(1.05).set_fill(BLUE, opacity=0.15),
            run_time=0.8
        )
        self.play(
            spotlight_left.animate.scale(1/1.05).set_fill(YELLOW, opacity=0.1),
            spotlight_right.animate.scale(1/1.05).set_fill(BLUE, opacity=0.1),
            run_time=0.8
        )

        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class RoleComparison(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BLACK

        # Create "Prompter" side: person icon + cue card
        prompter_label = Text("Prompter", font="Arial", font_size=24, color=WHITE)
        cue_card = Rectangle(height=1.2, width=1.6, color=BLUE, fill_color=BLUE, fill_opacity=0.2)
        cue_text = Text("Prompt", font="Arial", font_size=16, color=WHITE).move_to(cue_card.get_center())
        person_icon = Text("🧑", font_size=48).next_to(cue_card, UP, buff=0.3)
        prompter_group = VGroup(cue_card, cue_text, person_icon, prompter_label).arrange(DOWN, buff=0.2)

        # Create "AI" side: AI head + question mark
        ai_label = Text("AI", font="Arial", font_size=24, color=WHITE)
        ai_head = Text("🤖", font_size=48)
        qmark = Text("?", font_size=36, color=YELLOW)
        qmark.next_to(ai_head, UP, buff=0.2)
        ai_group = VGroup(ai_head, qmark, ai_label).arrange(DOWN, buff=0.2)

        # Position groups side by side
        prompter_group.shift(LEFT * 3.5)
        ai_group.shift(RIGHT * 3.5)

        # Connecting arrow
        arrow = Arrow(
            start=prompter_group.get_right(),
            end=ai_group.get_left(),
            buff=0.2,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.08,
            color=GREEN
        )

        # Animate
        self.play(FadeIn(prompter_group), FadeIn(ai_group))
        self.wait(0.5)
        self.play(GrowArrow(arrow))
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class VisionPipelineTimeline(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Title
        title = Text("Vision Pipeline", font_size=36, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Define timeline positions (horizontal)
        width = config.frame_width - 2
        x_positions = [
            -width/2 + 0.3*width,
            -width/2 + 0.55*width,
            -width/2 + 0.8*width,
            -width/2 + 1.05*width,
        ]

        # Step 1: Pixel Grid (small grid of colored squares)
        grid_size = 4
        pixel_grid = VGroup()
        colors = [BLUE_E, GREEN_E, RED_E, YELLOW_E, PURPLE_E, TEAL_E]
        for i in range(grid_size):
            for j in range(grid_size):
                square = Square(side_length=0.3, fill_opacity=1, stroke_width=0.5)
                square.set_fill(colors[(i + j) % len(colors)])
                square.move_to([x_positions[0] + (j - (grid_size-1)/2)*0.35,
                                (i - (grid_size-1)/2)*0.35, 0])
                pixel_grid.add(square)
        label1 = Text("Pixel Grid", font_size=20, color=GRAY).next_to(pixel_grid, DOWN, buff=0.3)

        # Step 2: Edge Detection (simplified: black/white contour-like pattern)
        edge_grid = VGroup()
        for i in range(grid_size):
            for j in range(grid_size):
                # Simulate edges: white on top-left, black elsewhere — but with some variation
                fill = WHITE if (i == 0 or j == 0 or i == grid_size-1 or j == grid_size-1) else BLACK
                square = Square(side_length=0.3, fill_opacity=1, stroke_width=0.5)
                square.set_fill(fill)
                square.move_to([x_positions[1] + (j - (grid_size-1)/2)*0.35,
                                (i - (grid_size-1)/2)*0.35, 0])
                edge_grid.add(square)
        label2 = Text("Edge Detection", font_size=20, color=GRAY).next_to(edge_grid, DOWN, buff=0.3)

        # Step 3: Object Outline (clean white outline on black background — simplified shape)
        outline_shape = VGroup(
            Circle(radius=0.6, color=WHITE, stroke_width=3, fill_opacity=0),
            Line(start=[-0.4, -0.2, 0], end=[0.4, -0.2, 0], color=WHITE, stroke_width=3),
        ).move_to([x_positions[2], 0, 0])
        label3 = Text("Object Outline", font_size=20, color=GRAY).next_to(outline_shape, DOWN, buff=0.3)

        # Step 4: Labeled Photo (iconic labels only — no real image; use stylized text + icons)
        labeled_group = VGroup()
        # Cat
        cat_label = Text("🐱 cat", font_size=18, color=GREEN).shift(UP * 0.3)
        # Car
        car_label = Text("🚗 car", font_size=18, color=BLUE).shift(DOWN * 0.1)
        # Person
        person_label = Text("👤 person", font_size=18, color=YELLOW).shift(DOWN * 0.5)
        labeled_group.add(cat_label, car_label, person_label)
        labeled_group.move_to([x_positions[3], 0, 0])
        label4 = Text("Labeled Photo", font_size=20, color=GRAY).next_to(labeled_group, DOWN, buff=0.3)

        # Arrows between steps
        arrows = VGroup()
        for i in range(3):
            arrow = Arrow(
                start=x_positions[i] * RIGHT + 0.8 * DOWN,
                end=x_positions[i+1] * RIGHT + 0.8 * DOWN,
                buff=0.1,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.08
            )
            arrows.add(arrow)

        # Assemble all timeline elements
        timeline_elements = VGroup(
            pixel_grid, label1,
            edge_grid, label2,
            outline_shape, label3,
            labeled_group, label4,
            arrows
        )

        # Fade in timeline layout
        self.play(FadeIn(pixel_grid, shift=DOWN*0.5), Write(label1))
        self.wait(0.5)
        self.play(
            FadeIn(edge_grid, shift=DOWN*0.5), Write(label2),
            Create(arrows[0])
        )
        self.wait(0.5)
        self.play(
            FadeIn(outline_shape, shift=DOWN*0.5), Write(label3),
            Create(arrows[1])
        )
        self.wait(0.5)
        self.play(
            FadeIn(labeled_group, shift=DOWN*0.5), Write(label4),
            Create(arrows[2])
        )
        self.wait(1)

        # Smooth zoom-in transitions: focus on each stage sequentially
        # Zoom into pixel grid
        self.play(
            self.camera.frame.animate.move_to(pixel_grid.get_center()).set(width=2.5),
            run_time=1.2
        )
        self.wait(0.8)
        # Zoom into edge detection
        self.play(
            self.camera.frame.animate.move_to(edge_grid.get_center()).set(width=2.5),
            run_time=1.2
        )
        self.wait(0.8)
        # Zoom into outline
        self.play(
            self.camera.frame.animate.move_to(outline_shape.get_center()).set(width=2.5),
            run_time=1.2
        )
        self.wait(0.8)
        # Zoom into labeled photo
        self.play(
            self.camera.frame.animate.move_to(labeled_group.get_center()).set(width=3.0),
            run_time=1.2
        )
        self.wait(1)

        # Final zoom out to full timeline
        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=config.frame_width),
            run_time=1.5
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class PixelMatrixZoom(Scene):
    def construct(self):
        # Create 4x4 pixel grid
        pixels = VGroup()
        pixel_size = 0.6
        colors = [
            [RED, GREEN, BLUE, YELLOW],
            [MAGENTA, TEAL, GOLD, GRAY],
            [PINK, ORANGE, PURPLE, LIME],
            [INDIGO, CYAN, MAROON, OLIVE]
        ]
        
        # Generate pixel blocks with RGB labels
        rgb_values = [
            [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0]],
            [[255, 0, 255], [0, 128, 128], [255, 215, 0], [128, 128, 128]],
            [[255, 192, 203], [255, 165, 0], [128, 0, 128], [0, 255, 0]],
            [[75, 0, 130], [0, 255, 255], [128, 0, 0], [128, 128, 0]]
        ]
        
        for i in range(4):
            for j in range(4):
                square = Square(side_length=pixel_size, fill_color=colors[i][j], fill_opacity=1, stroke_width=1, stroke_color=WHITE)
                square.move_to((j - 1.5) * pixel_size, (1.5 - i) * pixel_size, 0)
                
                # RGB label
                rgb_text = Text(f"[{rgb_values[i][j][0]},{rgb_values[i][j][1]},{rgb_values[i][j][2]}]", 
                                font_size=14, color=WHITE if sum(rgb_values[i][j]) < 400 else BLACK)
                rgb_text.move_to(square.get_center())
                
                pixels.add(VGroup(square, rgb_text))
        
        # Add subtle grid lines
        grid_lines = VGroup()
        for i in range(5):
            # Horizontal lines
            h_line = Line(
                start=( -1.5 * pixel_size, (1.5 - i) * pixel_size, 0),
                end=( 1.5 * pixel_size, (1.5 - i) * pixel_size, 0),
                stroke_width=0.5,
                stroke_color=GREY_A
            )
            # Vertical lines
            v_line = Line(
                start=((i - 1.5) * pixel_size, 1.5 * pixel_size, 0),
                end=((i - 1.5) * pixel_size, -1.5 * pixel_size, 0),
                stroke_width=0.5,
                stroke_color=GREY_A
            )
            grid_lines.add(h_line, v_line)
        
        # Matrix label
        matrix_label = Text("matrix", font_size=24, color=BLUE).shift(UP * 2.5)
        
        # Initial view
        self.play(FadeIn(pixels), FadeIn(grid_lines), Write(matrix_label))
        self.wait(0.5)
        
        # Zoom in: scale up and center
        zoomed_group = VGroup(pixels, grid_lines, matrix_label)
        self.play(
            zoomed_group.animate.scale(2.5).move_to(ORIGIN),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1.5)


# ==================== Auto-Generated ====================
from manim import *

class CNNvsTransformerLayers(Scene):
    def construct(self):
        # Title
        title = Text("CNN vs Transformer Layers", font_size=32, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Split screen
        divider = Line(UP * 3, DOWN * 3, stroke_width=2, color=GRAY)
        divider.move_to(ORIGIN)
        self.play(Create(divider))

        # Left: CNN section
        cnn_label = Text("CNN Layer", font_size=24, color=BLUE).to_corner(UL, buff=0.7)
        cnn_label.shift(RIGHT * 2.5)
        self.play(Write(cnn_label))

        # Grid representing input image (8x8 pixels)
        pixel_grid = VGroup()
        for i in range(8):
            for j in range(8):
                pixel = Square(side_length=0.3, fill_opacity=0.2, fill_color=WHITE, stroke_color=GRAY, stroke_width=0.5)
                pixel.move_to(LEFT * 4.5 + RIGHT * j * 0.3 + UP * i * 0.3)
                pixel_grid.add(pixel)
        pixel_grid.move_to(LEFT * 4)

        # CNN kernel (3x3)
        kernel = Square(side_length=0.9, color=BLUE, fill_opacity=0.3, stroke_width=2)
        kernel.move_to(pixel_grid[0].get_center() + RIGHT * 0.3 + DOWN * 0.3)

        # Kernel weights (small squares inside kernel)
        kernel_weights = VGroup()
        for i in range(3):
            for j in range(3):
                w = Square(side_length=0.2, fill_color=BLUE, fill_opacity=0.7, stroke_width=0.5)
                w.move_to(kernel.get_center() + RIGHT * (j - 1) * 0.3 + DOWN * (i - 1) * 0.3)
                kernel_weights.add(w)

        self.play(FadeIn(pixel_grid), run_time=1)
        self.wait(0.5)
        self.play(FadeIn(kernel), FadeIn(kernel_weights))
        self.wait(0.5)

        # Animate kernel sliding (simplified: 3 positions horizontally, then down)
        for row in range(2):
            for col in range(2):
                target_pos = pixel_grid[(row * 8 + col) * 3 + 1].get_center() + RIGHT * 0.3 + DOWN * 0.3
                self.play(kernel.animate.move_to(target_pos),
                          kernel_weights.animate.move_to(target_pos),
                          run_time=0.4)
                self.wait(0.2)

        # Right: Transformer section
        trans_label = Text("Transformer Layer", font_size=24, color=GREEN).to_corner(UR, buff=0.7)
        trans_label.shift(LEFT * 2.5)
        self.play(Write(trans_label))

        # Patch grid (4x4 patches, each 2x2 pixels → same 8x8 image)
        patch_grid = VGroup()
        for i in range(4):
            for j in range(4):
                patch = Square(side_length=0.6, fill_opacity=0.15, fill_color=WHITE, stroke_color=GRAY, stroke_width=0.5)
                patch.move_to(RIGHT * 4.5 + RIGHT * j * 0.6 + UP * i * 0.6)
                patch_grid.add(patch)
        patch_grid.move_to(RIGHT * 4)

        # Patch labels (indices)
        patch_labels = VGroup()
        for idx, patch in enumerate(patch_grid):
            lbl = Text(str(idx), font_size=16, color=GRAY)
            lbl.move_to(patch.get_center())
            patch_labels.add(lbl)

        self.play(FadeIn(patch_grid), FadeIn(patch_labels))
        self.wait(0.5)

        # Attention heatmap: highlight some patches with increasing opacity
        attention_scores = [0.2, 0.9, 0.4, 0.7, 0.3, 0.8, 0.5, 0.6, 0.1, 0.9, 0.3, 0.4, 0.6, 0.2, 0.7, 0.5]
        heat_patches = VGroup()
        for i, patch in enumerate(patch_grid):
            heat = Square(
                side_length=0.6,
                fill_color=RED if attention_scores[i] > 0.6 else ORANGE if attention_scores[i] > 0.4 else YELLOW,
                fill_opacity=attention_scores[i] * 0.7,
                stroke_width=0
            )
            heat.move_to(patch.get_center())
            heat_patches.add(heat)

        self.play(FadeIn(heat_patches), run_time=1.5)
        self.wait(0.5)

        # Arrows and labels
        cnn_arrow = Arrow(start=LEFT * 2.5, end=LEFT * 1.5, color=BLUE, stroke_width=3, buff=0)
        trans_arrow = Arrow(start=RIGHT * 1.5, end=RIGHT * 2.5, color=GREEN, stroke_width=3, buff=0)
        self.play(GrowArrow(cnn_arrow), GrowArrow(trans_arrow))

        cnn_desc = Text("Local Receptive Field", font_size=20, color=BLUE).next_to(cnn_arrow, DOWN, buff=0.2)
        trans_desc = Text("Global Attention Weights", font_size=20, color=GREEN).next_to(trans_arrow, DOWN, buff=0.2)
        self.play(Write(cnn_desc), Write(trans_desc))

        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *

class CrossModalBridge(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Brain outline (simplified symmetrical shape)
        brain = SVGMobject("brain").scale(2).set_fill(GREY_E, opacity=0.8).set_stroke(WHITE, width=1)
        # Since we can't rely on external SVG files, replace with a stylized brain-like shape using two circles + rectangle
        left_lobe = Circle(radius=1.2, color=BLUE_A, fill_opacity=0.3).shift(LEFT * 1.5)
        right_lobe = Circle(radius=1.2, color=GREEN_A, fill_opacity=0.3).shift(RIGHT * 1.5)
        central_bridge = Rectangle(width=1.0, height=1.8, fill_color=GREY_B, fill_opacity=0.4, stroke_width=0)
        brain_group = VGroup(left_lobe, central_bridge, right_lobe).move_to(ORIGIN)

        # Eye icon (left lobe representation)
        eye_center = Dot(point=left_lobe.get_center() + UP*0.3, color=YELLOW)
        eye_white = Circle(radius=0.4, color=WHITE, fill_opacity=1).move_to(eye_center.get_center())
        eye_pupil = Circle(radius=0.15, color=BLACK).move_to(eye_center.get_center())
        eye = VGroup(eye_white, eye_pupil, eye_center)

        # Speech bubble (right lobe representation)
        bubble = VMobject()
        bubble.set_points_as_corners([
            right_lobe.get_center() + DOWN*0.5 + RIGHT*0.3,
            right_lobe.get_center() + UP*0.5 + RIGHT*0.3,
            right_lobe.get_center() + UP*0.5 + LEFT*0.3,
            right_lobe.get_center() + DOWN*0.5 + LEFT*0.3,
            right_lobe.get_center() + DOWN*0.5 + RIGHT*0.3,
        ])
        bubble.set_fill(BLUE_B, opacity=0.4).set_stroke(BLUE_C, width=1)
        # Bubble tail
        tail_points = [
            right_lobe.get_center() + DOWN*0.5 + RIGHT*0.3,
            right_lobe.get_center() + DOWN*0.8 + RIGHT*0.6,
            right_lobe.get_center() + DOWN*0.8 + RIGHT*0.3,
        ]
        tail = VMobject().set_points_as_corners(tail_points).set_stroke(BLUE_C, width=1).set_fill(BLUE_B, opacity=0.4)
        speech_bubble = VGroup(bubble, tail)

        # Golden pulsing pathway (curved line between lobes)
        pulse_path = CubicBezier(
            left_lobe.get_right(),
            left_lobe.get_right() + RIGHT*0.5 + UP*0.8,
            right_lobe.get_left() + LEFT*0.5 + UP*0.8,
            right_lobe.get_left()
        )
        pulse_path.set_stroke(GOLD, width=6).set_opacity(0.9)

        # Pulsing animation via opacity and width oscillation
        def pulsing_updater(mob, dt):
            mob.time += dt
            alpha = 0.5 + 0.5 * np.sin(mob.time * 3)
            mob.set_stroke(width=4 + 4 * alpha, opacity=0.6 + 0.4 * alpha)

        pulse_path.time = 0
        pulse_path.add_updater(pulsing_updater)

        # Label text
        label = Text("cross-modal alignment", font="Arial", weight=MEDIUM, color=GOLD).scale(0.6)
        label.next_to(pulse_path, UP, buff=0.3)

        # Assemble scene
        self.play(
            DrawBorderThenFill(brain_group),
            Create(eye),
            Create(speech_bubble),
            Create(pulse_path),
            Write(label),
            run_time=2
        )
        self.wait(1)

        # Hold with pulsing effect
        self.add(pulse_path)  # ensure updater stays active
        self.wait(4)

        # Cleanup
        pulse_path.clear_updaters()
        self.wait(0.5)


# ==================== Auto-Generated ====================
from manim import *

class WorldToTextPipeline(Scene):
    def construct(self):
        # 1. 3D Globe (simplified with rotating sphere)
        globe = Sphere(
            radius=1.0,
            resolution=(24, 48),
            fill_opacity=0.8,
            fill_color=BLUE_E,
            stroke_width=0.5,
            stroke_color=BLUE_A
        )
        # Add subtle grid lines for realism
        lon_lines = VGroup(*[
            Circle(radius=1.0, color=BLUE_D, stroke_width=0.5).rotate(PI/2, axis=RIGHT).rotate(angle, axis=OUT)
            for angle in np.linspace(0, TAU, 8, endpoint=False)
        ])
        lat_lines = VGroup(*[
            Circle(radius=1.0 * np.cos(theta), color=BLUE_D, stroke_width=0.5).shift(UP * np.sin(theta))
            for theta in np.linspace(-PI/2, PI/2, 6)
        ])
        globe_group = VGroup(globe, lon_lines, lat_lines).scale(0.7).to_edge(LEFT, buff=1.0)

        # 2. Camera feed overlay: semi-transparent rectangle with "LIVE" label
        camera_rect = Rectangle(
            width=2.2, height=1.6,
            fill_color=GREY_E, fill_opacity=0.7,
            stroke_color=TEAL_A, stroke_width=2
        ).next_to(globe_group, RIGHT, buff=0.8)
        live_label = Text("LIVE", font_size=24, color=TEAL_C).move_to(camera_rect.get_center())
        camera_feed = VGroup(camera_rect, live_label)

        # 3. Abstract logic graph (nodes & edges)
        nodes = [
            Dot(point=ORIGIN + 2*UP, color=GOLD, radius=0.12),
            Dot(point=ORIGIN + 2*DOWN + 1.5*LEFT, color=GOLD, radius=0.12),
            Dot(point=ORIGIN + 2*DOWN + 1.5*RIGHT, color=GOLD, radius=0.12),
        ]
        edges = VGroup(*[
            Line(nodes[0].get_center(), nodes[1].get_center(), color=GOLD_E, stroke_width=2),
            Line(nodes[0].get_center(), nodes[2].get_center(), color=GOLD_E, stroke_width=2),
            Line(nodes[1].get_center(), nodes[2].get_center(), color=GOLD_E, stroke_width=1.5),
        ])
        graph = VGroup(*nodes, edges).scale(0.8).next_to(camera_feed, RIGHT, buff=0.8)

        # 4. Flowing Chinese text stream (vertical, right-aligned)
        chinese_chars = ["世界", "语言", "模型", "理解", "生成", "智能", "系统", "推理"]
        text_stream = VGroup(*[
            Text(s, font="Microsoft YaHei", font_size=28, color=WHITE).shift(DOWN * i * 0.9)
            for i, s in enumerate(chinese_chars)
        ]).arrange(DOWN, aligned_edge=RIGHT, buff=0.3).to_edge(RIGHT, buff=1.0)

        # Animation sequence
        self.camera.background_color = BLACK

        # Fade in globe + rotation
        self.play(FadeIn(globe_group), run_time=1.5)
        self.play(Rotate(globe_group, angle=TAU/6, axis=UP, run_time=3, rate_func=linear))

        # Fade in camera feed
        self.play(FadeIn(camera_feed), run_time=1.2)

        # Fade in logic graph
        self.play(FadeIn(graph), run_time=1.2)

        # Animate flowing text: staggered fade-in from bottom up, then slight upward drift
        self.play(
            *[FadeIn(t, shift=DOWN * 0.5, scale=0.9) for t in text_stream],
            run_time=2.5,
            lag_ratio=0.2
        )
        self.wait(0.5)

        # Simultaneous gentle upward motion for all text (like a stream)
        self.play(
            text_stream.animate.shift(UP * 0.8),
            Rotate(globe_group, angle=TAU/12, axis=UP, run_time=2.5),
            run_time=2.5
        )

        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class AutoScene03(Scene):
    def construct(self):
        # Title
        title = Text("Text Parsing vs Pixel Recognition", font_size=36)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Left side: Text Parsing
        left_label = Text("Text Parsing", font_size=28, color=BLUE)
        left_label.shift(LEFT * 3.5 + UP * 2)
        self.play(FadeIn(left_label))

        # Right side: Pixel Recognition
        right_label = Text("Pixel Recognition", font_size=28, color=GREEN)
        right_label.shift(RIGHT * 3.5 + UP * 2)
        self.play(FadeIn(right_label))

        # Flowchart boxes for Text Parsing (left)
        box1_left = Rectangle(height=0.8, width=3, color=BLUE).shift(LEFT * 3.5 + UP * 0.5)
        text1_left = Text("Input Text", font_size=20).move_to(box1_left.get_center())
        self.play(Create(box1_left), Write(text1_left))

        box2_left = Rectangle(height=0.8, width=3, color=BLUE).shift(LEFT * 3.5 + DOWN * 0.7)
        text2_left = Text("Tokenize", font_size=20).move_to(box2_left.get_center())
        arrow1_left = Arrow(box1_left.get_bottom(), box2_left.get_top(), buff=0.1, color=BLUE)
        self.play(Create(arrow1_left), Create(box2_left), Write(text2_left))

        box3_left = Rectangle(height=0.8, width=3, color=BLUE).shift(LEFT * 3.5 + DOWN * 1.9)
        text3_left = Text("Parse Structure", font_size=20).move_to(box3_left.get_center())
        arrow2_left = Arrow(box2_left.get_bottom(), box3_left.get_top(), buff=0.1, color=BLUE)
        self.play(Create(arrow2_left), Create(box3_left), Write(text3_left))

        # Flowchart boxes for Pixel Recognition (right)
        box1_right = Rectangle(height=0.8, width=3, color=GREEN).shift(RIGHT * 3.5 + UP * 0.5)
        text1_right = Text("Input Image", font_size=20).move_to(box1_right.get_center())
        self.play(Create(box1_right), Write(text1_right))

        box2_right = Rectangle(height=0.8, width=3, color=GREEN).shift(RIGHT * 3.5 + DOWN * 0.7)
        text2_right = Text("Detect Edges", font_size=20).move_to(box2_right.get_center())
        arrow1_right = Arrow(box1_right.get_bottom(), box2_right.get_top(), buff=0.1, color=GREEN)
        self.play(Create(arrow1_right), Create(box2_right), Write(text2_right))

        box3_right = Rectangle(height=0.8, width=3, color=GREEN).shift(RIGHT * 3.5 + DOWN * 1.9)
        text3_right = Text("Recognize Patterns", font_size=20).move_to(box3_right.get_center())
        arrow2_right = Arrow(box2_right.get_bottom(), box3_right.get_top(), buff=0.1, color=GREEN)
        self.play(Create(arrow2_right), Create(box3_right), Write(text3_right))

        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *

class AutoScene05(Scene):
    def construct(self):
        # Step 1: Show matrix of numbers
        matrix_data = [
            [1, 0, 1, 0],
            [0, 1, 1, 0],
            [1, 1, 0, 1],
            [0, 0, 1, 1]
        ]
        matrix = VGroup()
        cell_size = 0.6
        for i, row in enumerate(matrix_data):
            row_group = VGroup()
            for j, val in enumerate(row):
                cell = Text(str(val), font_size=36)
                cell.move_to([j * cell_size, -i * cell_size, 0])
                row_group.add(cell)
            matrix.add(row_group)
        matrix.center().shift(UP * 0.5)
        
        self.play(Write(matrix))
        self.wait(0.5)

        # Step 2: Transform matrix into graph edges
        dots = VGroup()
        positions = [
            [-2, 1, 0],   # Node 0
            [0, 1, 0],    # Node 1
            [0, -1, 0],   # Node 2
            [-2, -1, 0]   # Node 3
        ]
        for pos in positions:
            dot = Dot(point=pos, radius=0.15, color=BLUE)
            dots.add(dot)

        edges = VGroup()
        edge_pairs = []
        for i in range(4):
            for j in range(4):
                if matrix_data[i][j] == 1:
                    edge = Line(
                        dots[i].get_center(),
                        dots[j].get_center(),
                        color=GREEN,
                        stroke_width=3
                    )
                    edges.add(edge)
                    edge_pairs.append((i, j))

        self.play(
            FadeOut(matrix),
            *[GrowFromCenter(dot) for dot in dots],
            run_time=1
        )

        for edge in edges:
            self.play(Create(edge), run_time=0.3)

        self.wait(0.5)

        # Step 3: Transform graph into simple geometric objects
        shapes = VGroup()
        shape_positions = [
            [-3, 0, 0],  # Left
            [0, 2, 0],   # Top
            [3, 0, 0],   # Right
            [0, -2, 0]   # Bottom
        ]

        shape_types = [
            Circle(radius=0.5, color=RED),
            Square(side_length=1, color=YELLOW),
            Triangle().scale(0.6).set_color(PURPLE),
            RegularPolygon(5, radius=0.5, color=ORANGE)
        ]

        for i, (shape, pos) in enumerate(zip(shape_types, shape_positions)):
            shape.move_to(pos)
            shapes.add(shape)

        self.play(
            FadeOut(dots),
            FadeOut(edges),
            *[GrowFromCenter(shape) for shape in shapes],
            run_time=1.5
        )

        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class AutoScene06(Scene):
    def construct(self):
        # Define layers with labels
        input_label = Text("Input Image", font="Arial", font_size=24)
        edge_label = Text("Edge Detection", font="Arial", font_size=24)
        shape_label = Text("Shape Assembly", font="Arial", font_size=24)
        output_label = Text("Labeled Object: Cat", font="Arial", font_size=24)

        # Position labels in a row
        labels = VGroup(input_label, edge_label, shape_label, output_label).arrange(RIGHT, buff=1.5)
        labels.to_edge(UP, buff=1.0)

        # Create placeholder rectangles for each layer
        input_rect = Rectangle(height=2, width=2, color=BLUE).next_to(input_label, DOWN, buff=0.5)
        edge_rect = Rectangle(height=2, width=2, color=GREEN).next_to(edge_label, DOWN, buff=0.5)
        shape_rect = Rectangle(height=2, width=2, color=YELLOW).next_to(shape_label, DOWN, buff=0.5)
        output_rect = Rectangle(height=2, width=2, color=RED).next_to(output_label, DOWN, buff=0.5)

        # Arrows between layers
        arrow1 = Arrow(input_rect.get_right(), edge_rect.get_left(), buff=0.2)
        arrow2 = Arrow(edge_rect.get_right(), shape_rect.get_left(), buff=0.2)
        arrow3 = Arrow(shape_rect.get_right(), output_rect.get_left(), buff=0.2)

        # Animate step by step
        self.play(Write(input_label), Create(input_rect))
        self.wait(0.5)
        self.play(Create(arrow1), Write(edge_label), Create(edge_rect))
        self.wait(0.5)
        self.play(Create(arrow2), Write(shape_label), Create(shape_rect))
        self.wait(0.5)
        self.play(Create(arrow3), Write(output_label), Create(output_rect))
        self.wait(0.5)

        # Highlight final output
        cat_text = Text("Cat", font="Arial", font_size=36, color=WHITE).move_to(output_rect)
        self.play(FadeIn(cat_text))
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class AutoScene11(Scene):
    def construct(self):
        # Since we cannot use ImageMobject or local files, simulate "mountain lake" with simple shapes
        background = Rectangle(width=14, height=8, fill_color=BLUE_E, fill_opacity=1, stroke_width=0)
        ground = Rectangle(width=14, height=2, fill_color=GREEN_E, fill_opacity=1, stroke_width=0).align_to(background, DOWN)
        mountain_left = Polygon([-5, -1, 0], [-3, 2, 0], [-1, -1, 0], color=GREY_BROWN, fill_opacity=1)
        mountain_right = Polygon([1, -1, 0], [3, 2.5, 0], [5, -1, 0], color=GREY_BROWN, fill_opacity=1)

        self.add(background, ground, mountain_left, mountain_right)
        self.wait(0.5)

        # Define poetic captions
        captions = [
            Text("湖光山色，静水流深", font="Microsoft YaHei", font_size=24, color=YELLOW),
            Text("云影徘徊，天地无言", font="Microsoft YaHei", font_size=24, color=ORANGE),
            Text("一叶扁舟，心随波远", font="Microsoft YaHei", font_size=24, color=TEAL),
        ]

        # Animate text bubbles (rounded rectangles) with captions
        for i, caption in enumerate(captions):
            bubble = RoundedRectangle(
                corner_radius=0.3,
                width=caption.width + 0.6,
                height=caption.height + 0.4,
                fill_color=WHITE,
                fill_opacity=0.9,
                stroke_color=LIGHT_GREY
            )
            caption.move_to(bubble.get_center())
            group = VGroup(bubble, caption)
            group.shift(UP * (1 - i * 1.5)).shift(RIGHT * 2)

            if i == 0:
                self.play(FadeIn(group, shift=UP * 0.5), run_time=1.2)
            else:
                self.play(FadeIn(group, shift=RIGHT * 0.3), run_time=0.8)
            self.wait(0.7)

        self.wait(1)


# Note: This scene simulates a mountain lake background using geometric shapes since real photos are not allowed.
# Animated text bubbles appear sequentially with poetic Chinese captions in an educational, serene style.


# ==================== Auto-Generated ====================
from manim import *

class AutoScene12(Scene):
    def construct(self):
        # Simulate image with red-clothed person using a simple rectangle and circle
        background = Rectangle(width=6, height=4, fill_color=GREY_E, fill_opacity=1, stroke_width=0)
        person = VGroup(
            Circle(radius=0.3, color=RED, fill_opacity=1).shift(UP * 0.2),  # head
            Rectangle(width=0.6, height=1.0, color=RED, fill_opacity=1)     # body
        ).move_to(background.get_center())
        
        self.add(background, person)
        self.wait(0.5)
        
        # Highlight the person with a glowing effect (pulsing scale)
        self.play(person.animate.scale(1.1), run_time=0.3)
        self.play(person.animate.scale(1/1.1), run_time=0.3)
        
        # Zoom in on the person
        zoom_group = VGroup(background, person)
        self.play(zoom_group.animate.scale(1.8).move_to(ORIGIN), run_time=1.5)
        
        # Display answer text
        answer_text = Text("正在拍照", font="Microsoft YaHei", font_size=36, color=YELLOW)
        answer_text.to_edge(DOWN, buff=0.5)
        self.play(Write(answer_text), run_time=1)
        
        # Add schematic UI overlay (simple frame + button icons)
        ui_frame = Rectangle(width=5, height=3, color=BLUE_E, stroke_width=2).move_to(ORIGIN)
        shutter_button = Circle(radius=0.2, color=WHITE, fill_opacity=0.3).next_to(ui_frame, DOWN, buff=0.3)
        icon_text = Text("📷", font_size=24).move_to(shutter_button)
        
        self.play(Create(ui_frame), Create(shutter_button), FadeIn(icon_text), run_time=1)
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class PixelToText(Scene):
    def construct(self):
        # Create the target text
        target_text = Text("TRANSLATE", font_size=72, color=BLUE)
        
        # Create a grid of pixels (squares)
        pixel_grid = VGroup()
        rows = 5
        cols = 10
        spacing = 0.25
        
        for i in range(cols):
            for j in range(rows):
                pixel = Square(side_length=0.2, color=GRAY, fill_opacity=1)
                # Arrange in a grid centered on screen
                x = (i - (cols - 1) / 2) * spacing
                y = (j - (rows - 1) / 2) * spacing
                pixel.move_to([x, y, 0])
                pixel_grid.add(pixel)
        
        # Animation
        self.play(Create(pixel_grid), run_time=1)
        self.wait(0.5)
        self.play(Transform(pixel_grid, target_text), run_time=2)
        self.wait(1.5)


# ==================== Auto-Generated ====================
from manim import *
import random

class ImageToMatrix(Scene):
    def construct(self):
        # Configuration for the grid
        n_rows, n_cols = 3, 3
        pixel_size = 1.2
        spacing = 0.1
        
        image_grid = VGroup()
        number_grid = VGroup()
        
        # Create the "Image" (colored squares) and the "Matrix" (numbers)
        for i in range(n_rows):
            for j in range(n_cols):
                # Random color for the pixel
                color = random.choice([RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, TEAL, MAROON])
                pixel = Square(side_length=pixel_size, color=color, fill_opacity=1, stroke_width=0)
                
                # Random number for the matrix value
                value = random.randint(10, 99)
                number = Text(str(value), font_size=36)
                
                # Calculate position
                x_pos = (j - (n_cols - 1) / 2) * (pixel_size + spacing)
                y_pos = -(i - (n_rows - 1) / 2) * (pixel_size + spacing)
                
                pixel.move_to([x_pos, y_pos, 0])
                number.move_to([x_pos, y_pos, 0])
                
                image_grid.add(pixel)
                number_grid.add(number)

        # Matrix brackets
        brackets = SurroundingRectangle(number_grid, buff=0.4, color=WHITE)

        # Animation sequence
        self.play(FadeIn(image_grid), run_time=1)
        self.wait(1)
        
        self.play(ReplacementTransform(image_grid, number_grid), run_time=1.5)
        self.play(Create(brackets), run_time=0.5)
        
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
import numpy as np

class FilteringNumbers(Scene):
    def construct(self):
        # Create a list of numbers
        numbers = [Text(str(i), font_size=48) for i in range(1, 10)]
        
        # Scatter numbers chaotically on screen
        for num in numbers:
            num.move_to(np.array([
                np.random.uniform(-5, 5),
                np.random.uniform(-3, 3),
                0
            ]))
            num.set_color(random_color())

        self.play(FadeIn(VGroup(*numbers)), run_time=0.5)
        self.wait(0.5)

        # Create a container representing the structured layer
        container = Rectangle(height=3.5, width=5.5, color=WHITE, stroke_width=2)
        self.play(Create(container), run_time=0.5)

        # Define target grid positions (3x3)
        grid_positions = []
        for i in range(9):
            row = i // 3
            col = i % 3
            # Calculate offsets relative to container center
            x = (col - 1) * 1.5
            y = (1 - row) * 1.0
            grid_positions.append(container.get_center() + np.array([x, y, 0]))

        # Animate numbers filtering into the grid
        self.play(
            *[
                numbers[i].animate.move_to(pos).set_color(BLUE) 
                for i, pos in enumerate(grid_positions)
            ],
            run_time=1.5,
            path_arc=PI/4
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class NeuralNetworkLayers(Scene):
    def construct(self):
        # Layer configurations: (x_position, number_of_nodes)
        layer_configs = [(-3, 3), (0, 4), (3, 2)]
        layers = VGroup()
        edges = VGroup()

        # Create Nodes (Neurons)
        for x, count in layer_configs:
            layer = VGroup()
            for i in range(count):
                # Distribute nodes vertically
                y = (i - (count - 1) / 2) * 1.2
                node = Circle(radius=0.25, color=BLUE, fill_opacity=0.3, stroke_width=2)
                node.move_to(x * RIGHT + y * UP)
                layer.add(node)
            layers.add(layer)

        # Create Edges (Connections)
        # Connect every node in layer i to every node in layer i+1
        for i in range(len(layers) - 1):
            for node_left in layers[i]:
                for node_right in layers[i+1]:
                    edge = Line(
                        start=node_left.get_center(),
                        end=node_right.get_center(),
                        color=GRAY,
                        stroke_width=1,
                        stroke_opacity=0.5
                    )
                    edges.add(edge)

        # Animation: Draw the network structure
        self.play(Create(edges), run_time=1)
        self.play(Create(layers), run_time=1)
        self.wait(0.5)

        # Animation: Data Processing (Simulating data flow)
        # Create two data packets starting from the input layer
        data_1 = Dot(radius=0.15, color=YELLOW).move_to(layers[0][0].get_center())
        data_2 = Dot(radius=0.15, color=ORANGE).move_to(layers[0][2].get_center())

        # Define paths through the network
        # Path 1: Input Node 0 -> Hidden Node 2 -> Output Node 0
        path_1_hidden = layers[1][2].get_center()
        path_1_output = layers[2][0].get_center()

        # Path 2: Input Node 2 -> Hidden Node 1 -> Output Node 1
        path_2_hidden = layers[1][1].get_center()
        path_2_output = layers[2][1].get_center()

        # Move data to hidden layer
        self.play(
            data_1.animate.move_to(path_1_hidden),
            data_2.animate.move_to(path_2_hidden),
            run_time=1.5,
            rate_func=linear
        )
        
        # Move data to output layer
        self.play(
            data_1.animate.move_to(path_1_output),
            data_2.animate.move_to(path_2_output),
            run_time=1.5,
            rate_func=linear
        )

        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class LinesAndEdges(Scene):
    def construct(self):
        # Create a horizontal line
        line_h = Line(LEFT * 3, RIGHT * 3, color=BLUE)
        
        # Create a vertical line
        line_v = Line(UP * 2, DOWN * 2, color=RED)
        
        # Create a square to show edges
        square = Square(color=GREEN)
        
        # Animate the lines and edges appearing
        self.play(Create(line_h))
        self.play(Create(line_v))
        self.play(Create(square))
        
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class ShapeToObject(Scene):
    def construct(self):
        # Step 1: Simple Lines
        line1 = Line(LEFT * 2, RIGHT * 2, color=YELLOW)
        line2 = Line(UP * 2, DOWN * 2, color=YELLOW)
        line3 = Line(UL * 2, DR * 2, color=YELLOW)
        lines = VGroup(line1, line2, line3)
        
        self.play(Create(lines), run_time=1)
        self.wait(0.5)

        # Step 2: Complex Shape (Star)
        star = Star(5, outer_radius=2, color=PURPLE)
        self.play(Transform(lines, star), run_time=1.5)
        self.wait(0.5)

        # Step 3: Recognizable Object (House)
        square = Square(side_length=2, color=ORANGE)
        roof = EquilateralTriangle(side_length=2.3, color=RED)
        roof.next_to(square, UP, buff=0)
        house = VGroup(square, roof)
        
        self.play(Transform(star, house), run_time=1.5)
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class VLMText(Scene):
    def construct(self):
        # Create the main text
        text = Text("VLM", font_size=96, color=WHITE)
        
        # Create a glow effect by copying the text, scaling it, 
        # and reducing opacity
        glow = text.copy()
        glow.set_color(YELLOW)
        glow.scale(1.2)
        glow.set_opacity(0.3)
        
        # Position the glow behind the text
        glow.z_index = text.z_index - 1
        
        # Add both to the scene
        self.add(glow)
        
        # Animate the glow fading in
        self.play(FadeIn(glow), run_time=1)
        
        # Animate the text being written
        self.play(Write(text), run_time=1.5)
        
        # Add a subtle pulsing effect to the glow
        self.play(
            glow.animate.set_opacity(0.5).scale(1.25),
            run_time=1,
            rate_func=there_and_back
        )
        
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class ConnectingNodes(Scene):
    def construct(self):
        # Define positions
        left_pos = LEFT * 2.5
        right_pos = RIGHT * 2.5

        # Create Nodes
        vision_circle = Circle(radius=1.0, color=BLUE, stroke_width=4)
        language_circle = Circle(radius=1.0, color=ORANGE, stroke_width=4)

        vision_circle.move_to(left_pos)
        language_circle.move_to(right_pos)

        # Create Text labels
        vision_text = Text("Vision", font_size=32).move_to(left_pos)
        language_text = Text("Language", font_size=32).move_to(right_pos)

        # Create the connecting beam
        # Connects the right edge of the left circle to the left edge of the right circle
        beam = Line(
            start=vision_circle.get_right(),
            end=language_circle.get_left(),
            color=YELLOW,
            stroke_width=8
        )

        # Animation
        self.play(Create(vision_circle), Create(language_circle))
        self.play(FadeIn(vision_text), FadeIn(language_text))
        self.wait(0.5)
        
        self.play(Create(beam), run_time=1.5)
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
import numpy as np

class IsolatedPixels(Scene):
    def construct(self):
        pixels = VGroup()
        
        # Create 30 small squares representing isolated pixels
        for _ in range(30):
            pixel = Square(
                side_length=0.25,
                color=BLUE,
                fill_opacity=0.8,
                stroke_width=0
            )
            # Position randomly within the frame
            pixel.move_to([
                np.random.uniform(-5, 5),
                np.random.uniform(-3, 3),
                0
            ])
            pixels.add(pixel)

        # Fade in the pixels
        self.play(FadeIn(pixels), run_time=1)
        
        # Animate them floating in random directions
        self.play(
            *[
                pixel.animate.shift(
                    np.random.uniform(-3, 3) * RIGHT + 
                    np.random.uniform(-2, 2) * UP
                )
                for pixel in pixels
            ],
            run_time=4,
            rate_func=linear
        )
        
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class PixelTextLogic(Scene):
    def construct(self):
        # 1. Create Pixels (Raw Data)
        pixels = VGroup()
        for x in range(-2, 3):
            for y in range(-2, 3):
                pixel = Square(side_length=0.2, color=BLUE, fill_opacity=0.7)
                pixel.shift(x * 0.3 * RIGHT + y * 0.3 * UP)
                pixels.add(pixel)
        pixels.move_to(LEFT * 3)

        # 2. Create Text Label
        raw_label = Text("RAW", font_size=36)
        raw_label.next_to(pixels, DOWN)

        # Group the raw elements
        raw_group = VGroup(pixels, raw_label)

        # 3. Create Structured Logic Diagram (Target)
        # Input Node
        input_box = Rectangle(width=2, height=1, color=BLUE, stroke_width=3)
        input_text = Text("INPUT", font_size=24)
        input_node = VGroup(input_box, input_text).arrange(DOWN)
        input_node.move_to(LEFT * 2.5)

        # Logic Node
        logic_box = Rectangle(width=2, height=1, color=GREEN, stroke_width=3)
        logic_text = Text("LOGIC", font_size=24)
        logic_node = VGroup(logic_box, logic_text).arrange(DOWN)
        logic_node.move_to(RIGHT * 2.5)

        # Connection Arrow
        arrow = Arrow(input_node.get_right(), logic_node.get_left(), buff=0.2, stroke_width=4)

        diagram = VGroup(input_node, arrow, logic_node)

        # Animation
        self.play(FadeIn(pixels), Write(raw_label), run_time=1.5)
        self.wait(0.5)
        self.play(Transform(raw_group, diagram), run_time=2)
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class WorldToLanguage(Scene):
    def construct(self):
        # 1. Create the Globe
        # A blue circle representing the ocean
        earth_base = Circle(radius=2.5, color=BLUE, fill_opacity=0.3, stroke_width=0)
        
        # Wireframe ellipses to give a 3D globe effect
        equator = Ellipse(width=5, height=1.5, color=WHITE, stroke_width=1)
        meridian_1 = Ellipse(width=5, height=1.5, color=WHITE, stroke_width=1).rotate(PI/2)
        meridian_2 = Ellipse(width=5, height=1.5, color=WHITE, stroke_width=1).rotate(PI/4)
        
        globe = VGroup(earth_base, equator, meridian_1, meridian_2)
        
        # 2. Create the "Language" (Lines of Code)
        # Using Text objects to represent code lines
        code_lines = VGroup(
            Text("const world = new Globe();", color=GREEN),
            Text("world.transform({", color=GREEN),
            Text("  into: 'language'", color=GREEN),
            Text("});", color=GREEN)
        )
        code_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        
        # 3. Animation
        self.play(FadeIn(globe), run_time=1)
        self.wait(1)
        
        # Transform the globe into the code
        self.play(ReplacementTransform(globe, code_lines, run_time=2))
        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *

class TextTransformation(Scene):
    def construct(self):
        # Initial text
        initial_text = Text("Large Language Model", font_size=48)
        
        # Final text "LLM" with simulated glow effect
        llm_text = Text("LLM", font_size=96, weight=BOLD, color=WHITE)
        
        # Create glow layers by scaling copies and reducing opacity
        glow_layer_1 = llm_text.copy().scale(1.15).set_color(YELLOW).set_opacity(0.3)
        glow_layer_2 = llm_text.copy().scale(1.3).set_color(YELLOW).set_opacity(0.15)
        
        # Group them (layers behind the main text)
        final_group = VGroup(glow_layer_2, glow_layer_1, llm_text)
        
        # Animation sequence
        self.play(FadeIn(initial_text))
        self.wait(1)
        
        # Fade out the long text and fade in the bold LLM
        self.play(
            FadeOut(initial_text),
            FadeIn(final_group),
            run_time=1.5
        )
        
        # Add a slight pulse to the glowing text
        self.play(
            final_group.animate.scale(1.05),
            rate_func=there_and_back,
            run_time=2
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class MaskReveal(Scene):
    def construct(self):
        # --- 1. Create the Brain (LLM) ---
        # Glow effect layers
        glow_outer = Circle(radius=2.8, color=YELLOW, fill_opacity=0.1, stroke_width=0)
        glow_inner = Circle(radius=2.0, color=YELLOW, fill_opacity=0.2, stroke_width=0)
        
        # Brain shape (simplified abstract representation)
        left_lobe = Ellipse(width=1.6, height=2.0, color=RED, fill_opacity=0.9)
        right_lobe = Ellipse(width=1.6, height=2.0, color=RED, fill_opacity=0.9).shift(RIGHT*0.3)
        stem = Rectangle(width=0.5, height=1.2, color=RED, fill_opacity=0.9).shift(DOWN*1.3)
        
        # Label
        label = Text("LLM", font_size=48, color=WHITE, weight=BOLD)
        
        brain_group = VGroup(glow_outer, glow_inner, left_lobe, right_lobe, stem, label)
        brain_group.center()
        brain_group.set_opacity(0) # Start invisible

        # --- 2. Create Robot Masks ---
        # Mask 1: Square with round eyes
        m1_face = Square(side_length=2.6, color=GRAY, fill_opacity=1, stroke_width=4)
        m1_eyes = VGroup(
            Circle(radius=0.3, color=BLACK),
            Circle(radius=0.3, color=BLACK)
        ).arrange(RIGHT, buff=0.7).shift(UP*0.3)
        m1_mouth = Line(LEFT*0.4, RIGHT*0.4, stroke_width=6, color=BLACK).shift(DOWN*0.6)
        mask1 = VGroup(m1_face, m1_eyes, m1_mouth)

        # Mask 2: Rectangle with visor
        m2_face = Rectangle(width=2.8, height=2.2, color=BLUE, fill_opacity=1, stroke_width=4)
        m2_eyes = Rectangle(width=1.8, height=0.25, color=BLACK).shift(UP*0.3)
        m2_mouth = Dot(color=BLACK, radius=0.15).shift(DOWN*0.6)
        mask2 = VGroup(m2_face, m2_eyes, m2_mouth)

        # Mask 3: Rounded with triangle eyes
        m3_face = RoundedRectangle(width=2.6, height=2.3, corner_radius=0.4, color=GREEN, fill_opacity=1, stroke_width=4)
        m3_eyes = VGroup(
            Triangle(color=BLACK).scale(0.25),
            Triangle(color=BLACK).scale(0.25)
        ).arrange(RIGHT, buff=0.7).shift(UP*0.3)
        m3_mouth = Rectangle(width=0.6, height=0.1, color=BLACK).shift(DOWN*0.6)
        mask3 = VGroup(m3_face, m3_eyes, m3_mouth)

        # Position masks in a triangle formation covering the center
        mask1.shift(UP * 1.5 + LEFT * 2.0)
        mask2.shift(UP * 1.5 + RIGHT * 2.0)
        mask3.shift(DOWN * 1.8)

        # Add everything to scene
        self.add(mask1, mask2, mask3, brain_group)
        
        self.wait(0.5)

        # --- 3. Animation: Masks fall away to reveal Brain ---
        self.play(
            # Masks move outward and fade
            mask1.animate.shift(LEFT*3 + DOWN*2).rotate(PI/4).set_opacity(0),
            mask2.animate.shift(RIGHT*3 + DOWN*2).rotate(-PI/4).set_opacity(0),
            mask3.animate.shift(DOWN*3).set_opacity(0),
            # Brain fades in
            brain_group.animate.set_opacity(1),
            run_time=2,
            rate_func=smooth
        )

        # --- 4. Brain Pulse ---
        self.play(
            brain_group.animate.scale(1.1),
            run_time=0.5
        )
        self.play(
            brain_group.animate.scale(0.909), # scale back to ~1.0
            run_time=0.5
        )

        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class TermDefinition(Scene):
    def construct(self):
        # 1. Display the word "Parameters"
        title = Text("Parameters", font_size=64)
        self.play(Write(title))
        self.wait(0.5)

        # 2. Display the mathematical symbol theta
        theta = Text("θ", font_size=120, color=YELLOW)
        theta.next_to(title, DOWN, buff=1)
        self.play(FadeIn(theta, scale=0.5))
        self.wait(0.5)

        # 3. Display a weights matrix visualization (3x3 grid of squares)
        matrix_group = VGroup()
        for i in range(3):
            for j in range(3):
                square = Square(side_length=0.6, color=BLUE, fill_opacity=0.6, stroke_width=2)
                # Arrange in a grid relative to each other
                square.shift(RIGHT * j * 0.7 + DOWN * i * 0.7)
                matrix_group.add(square)
        
        matrix_group.next_to(theta, DOWN, buff=1.5)
        
        self.play(Create(matrix_group, lag_ratio=0.1))
        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *

class TextToMath(Scene):
    def construct(self):
        # 1. Display text sentence
        sentence = Text("Language Rules", font_size=48)
        self.play(Write(sentence))
        self.wait(1)

        # 2. Transform text into a mathematical equation
        equation = Text("y = x²", font_size=48)
        self.play(Transform(sentence, equation))
        self.wait(1)

        # 3. Setup the coordinate system
        axes = Axes(
            x_range=[-3, 3],
            y_range=[0, 9],
            axis_config={"color": WHITE},
        )
        
        # Create the graph of the equation
        graph = axes.get_graph(lambda x: x**2, color=YELLOW)

        # 4. Transition to graph visualization
        self.play(FadeOut(sentence), Create(axes))
        self.play(Create(graph), run_time=2)
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class SplitComparison(Scene):
    def construct(self):
        # Create a divider line
        divider = Line(UP * 3.5, DOWN * 3.5, color=GRAY, stroke_width=2)
        self.play(Create(divider))

        # --- LEFT SIDE: PHYSICS ---
        # Title
        left_title = Text("Physics: Trajectory", font_size=20, color=BLUE)
        left_title.to_edge(UP, buff=0.5).align_to(divider, LEFT).shift(RIGHT * 0.5)
        
        # Axes
        axes_left = Axes(
            x_range=[-2, 2],
            y_range=[-1, 3],
            x_length=5,
            y_length=4,
            axis_config={"color": BLUE_E}
        ).shift(LEFT * 3.5 + DOWN * 0.5)
        
        # Parabola representing projectile motion
        parabola = axes_left.plot(lambda x: -0.5 * x**2 + 2.5, color=YELLOW)
        
        self.play(FadeIn(left_title))
        self.play(Create(axes_left), run_time=1)
        self.play(Create(parabola), run_time=1.5)

        # --- RIGHT SIDE: PROBABILITY ---
        # Title
        right_title = Text("Probability: Dist", font_size=20, color=GREEN)
        right_title.to_edge(UP, buff=0.5).align_to(divider, RIGHT).shift(LEFT * 0.5)
        
        # Words
        word_a = Text("Word A")
        word_b = Text("Word B")
        word_c = Text("Word C")
        words = VGroup(word_a, word_b, word_c).arrange(DOWN, buff=1.5)
        words.shift(RIGHT * 3.5 + DOWN * 1.5)
        
        # Distribution Curve (Bell Curve)
        # Positioned above the words
        dist_curve = FunctionGraph(
            lambda x: 2 * np.exp(-0.5 * (x)**2),
            x_range=[-2.5, 2.5],
            color=RED
        ).scale(1.2).shift(RIGHT * 3.5 + UP * 0.5)
        
        self.play(FadeIn(right_title))
        self.play(Write(words), run_time=1)
        self.play(Create(dist_curve), run_time=1.5)

        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
import random

class InputProcess(Scene):
    def construct(self):
        # Create a screen/terminal background
        screen = Rectangle(height=5, width=7, color=WHITE, fill_opacity=0.1)
        screen.set_stroke(width=2)
        self.play(Create(screen))
        
        # Display the Chinese input
        input_text = Text("我爱", font="Microsoft YaHei", font_size=64)
        input_text.move_to(screen)
        self.play(Write(input_text), run_time=1)
        self.wait(0.5)
        
        # Fade out input to start processing
        self.play(FadeOut(input_text))
        
        # Generate a stream of random code/numbers
        # We create a long string of hex numbers to simulate data
        code_lines = []
        for _ in range(12):
            line = "".join(random.choices("0123456789ABCDEF ", k=16))
            code_lines.append(line)
        
        code_content = "\n".join(code_lines)
        
        # Create the text object for the stream
        # Using a monospaced font for the code look
        code_stream = Text(code_content, font="Consolas", font_size=18, color=GREEN)
        code_stream.move_to(screen)
        
        # Define the scrolling animation updater
        def scroll_updater(mob, dt):
            # Move the text up
            mob.shift(UP * dt * 2.0)
            # If the top of the text goes above the screen, reset to bottom
            if mob.get_top()[1] > screen.get_top()[1]:
                mob.move_to(screen, aligned_edge=DOWN)
        
        # Add the updater and display
        code_stream.add_updater(scroll_updater)
        self.add(code_stream)
        
        # Let the scrolling animation run
        self.wait(5)
        
        # Clean up
        code_stream.remove_updater(scroll_updater)
        self.play(FadeOut(screen), FadeOut(code_stream))


# ==================== Auto-Generated ====================
from manim import *

class ProbabilityBar(Scene):
    def construct(self):
        font_name = "Microsoft YaHei"
        
        # Define bars
        # 99% -> High bar, 0.1% -> Tiny bar (exaggerated slightly for visibility)
        bar_ni = Rectangle(height=3.5, width=1.2, color=BLUE, fill_opacity=0.8)
        bar_chi = Rectangle(height=0.2, width=1.2, color=GRAY, fill_opacity=0.8)
        
        # Position bars on a baseline
        bar_ni.shift(LEFT * 2.5 + DOWN * 1.5)
        bar_chi.shift(RIGHT * 2.5 + DOWN * 1.5)
        
        # Labels below bars
        label_ni = Text("你", font=font_name, font_size=48)
        label_chi = Text("吃", font=font_name, font_size=48)
        label_ni.next_to(bar_ni, DOWN, buff=0.5)
        label_chi.next_to(bar_chi, DOWN, buff=0.5)
        
        # Percentages above bars
        text_ni = Text("99%", font=font_name, font_size=36)
        text_chi = Text("0.1%", font=font_name, font_size=36)
        text_ni.next_to(bar_ni, UP, buff=0.2)
        text_chi.next_to(bar_chi, UP, buff=0.2)
        
        # Animation 1: Grow bars from bottom
        self.play(
            GrowFromEdge(bar_ni, DOWN),
            GrowFromEdge(bar_chi, DOWN),
            run_time=1.5
        )
        
        # Animation 2: Fade in labels and percentages
        self.play(
            FadeIn(label_ni, label_chi),
            FadeIn(text_ni, text_chi),
            run_time=1
        )
        
        # Animation 3: Highlight '你' as the output
        # Change color to green and add a slight scale up
        self.play(
            bar_ni.animate.set_fill(GREEN),
            text_ni.animate.set_color(GREEN),
            run_time=1
        )
        
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class FilterModalities(Scene):
    def construct(self):
        # 1. Create the Text Icon (Document)
        paper = Rectangle(height=1.5, width=1.2, color=WHITE, stroke_width=2)
        lines = VGroup()
        for y in [0.3, 0, -0.3]:
            line = Line(paper.get_left() + 0.2*RIGHT + y*UP, paper.get_right() + 0.2*LEFT + y*UP, color=WHITE, stroke_width=2)
            lines.add(line)
        text_icon = VGroup(paper, lines)
        text_label = Text("Text", font_size=24).next_to(text_icon, DOWN)
        text_group = VGroup(text_icon, text_label)

        # 2. Create the Image Icon (Picture frame)
        frame = Square(side_length=1.5, color=BLUE, stroke_width=2)
        # Abstract mountain and sun
        sun = Circle(radius=0.25, color=YELLOW).move_to(frame.get_center() + 0.3*UP + 0.3*RIGHT)
        mountain = Polygon(
            frame.get_left() + 0.2*RIGHT + 0.4*DOWN, 
            frame.get_center() + 0.5*UP, 
            frame.get_right() + 0.2*LEFT + 0.4*DOWN, 
            color=BLUE, fill_opacity=0.5, stroke_width=0
        )
        image_icon = VGroup(frame, sun, mountain)
        image_label = Text("Image", font_size=24).next_to(image_icon, DOWN)
        image_group = VGroup(image_icon, image_label)

        # 3. Create the Video Icon (Play button)
        screen = Rectangle(height=1.5, width=1.5, color=GREEN, stroke_width=2)
        play_triangle = Polygon(ORIGIN, 0.5*UP, 0.5*DOWN, color=GREEN).move_to(screen.get_center()).shift(0.1*RIGHT)
        video_icon = VGroup(screen, play_triangle)
        video_label = Text("Video", font_size=24).next_to(video_icon, DOWN)
        video_group = VGroup(video_icon, video_label)

        # Arrange them
        all_groups = VGroup(image_group, text_group, video_group).arrange(RIGHT, buff=1.5)

        # Animation: Show all
        self.play(FadeIn(all_groups), run_time=1)
        self.wait(1)

        # Create Red X marks
        def create_cross(mob):
            return VGroup(
                Line(mob.get_corner(UL), mob.get_corner(DR), color=RED, stroke_width=5),
                Line(mob.get_corner(DL), mob.get_corner(UR), color=RED, stroke_width=5)
            )

        x_img = create_cross(image_icon)
        x_vid = create_cross(video_icon)

        # Animation: Cross out Image and Video
        self.play(Create(x_img), Create(x_vid), run_time=0.5)
        self.wait(0.5)

        # Animation: Fade out Image and Video, keep Text
        self.play(
            FadeOut(image_group), FadeOut(x_img),
            FadeOut(video_group), FadeOut(x_vid),
            run_time=1
        )

        # Animation: Highlight Text (Processing)
        self.play(text_group.animate.scale(1.2), run_time=0.5)
        self.play(text_group.animate.scale(1/1.2), run_time=0.5)
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class VennMerge(Scene):
    def construct(self):
        # Define positions for the three initial circles
        pos_left = LEFT * 3.5
        pos_right = RIGHT * 3.5
        pos_top = UP * 2.5

        # Create the three modal circles
        circle_text = Circle(radius=1.0, color=BLUE).move_to(pos_left)
        circle_image = Circle(radius=1.0, color=GREEN).move_to(pos_right)
        circle_audio = Circle(radius=1.0, color=RED).move_to(pos_top)

        # Create labels
        label_text = Text("Text", font_size=24).move_to(circle_text.get_center())
        label_image = Text("Image", font_size=24).move_to(circle_image.get_center())
        label_audio = Text("Audio", font_size=24).move_to(circle_audio.get_center())

        # Group them for easier animation
        group_text = VGroup(circle_text, label_text)
        group_image = VGroup(circle_image, label_image)
        group_audio = VGroup(circle_audio, label_audio)

        # Display initial circles
        self.play(
            Create(group_text),
            Create(group_image),
            Create(group_audio),
            run_time=1.5
        )
        self.wait(0.5)

        # Create the final Multimodal circle
        circle_multi = Circle(radius=1.8, color=GOLD)
        label_multi = Text("Multimodal", font_size=36).move_to(circle_multi.get_center())
        group_multi = VGroup(circle_multi, label_multi)

        # Animate merging: Move small circles to center and fade out
        self.play(
            group_text.animate.move_to(ORIGIN).set_opacity(0),
            group_image.animate.move_to(ORIGIN).set_opacity(0),
            group_audio.animate.move_to(ORIGIN).set_opacity(0),
            run_time=1.5
        )

        # Reveal the merged circle
        self.play(Create(group_multi), run_time=1.5)
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class NeuralNetFlow(Scene):
    def construct(self):
        # Define Neural Network Blocks
        input_box = Rectangle(height=1.2, width=2, color=GREEN, stroke_width=4)
        input_text = Text("Input", weight=BOLD, color=GREEN)
        input_group = VGroup(input_box, input_text)

        cnn_box = Rectangle(height=1.2, width=2, color=BLUE, stroke_width=4)
        cnn_text = Text("CNN", weight=BOLD, color=BLUE)
        cnn_group = VGroup(cnn_box, cnn_text)

        trans_box = Rectangle(height=1.2, width=2, color=PURPLE, stroke_width=4)
        trans_text = Text("Transformer", weight=BOLD, color=PURPLE)
        trans_group = VGroup(trans_box, trans_text)

        output_box = Rectangle(height=1.2, width=2, color=ORANGE, stroke_width=4)
        output_text = Text("Features", weight=BOLD, color=ORANGE)
        output_group = VGroup(output_box, output_text)

        # Arrange Blocks Horizontally
        blocks = VGroup(input_group, cnn_group, trans_group, output_group)
        blocks.arrange(RIGHT, buff=1.5)

        # Create Connecting Arrows
        arrow1 = Arrow(input_group.get_right(), cnn_group.get_left(), buff=0.2, color=WHITE)
        arrow2 = Arrow(cnn_group.get_right(), trans_group.get_left(), buff=0.2, color=WHITE)
        arrow3 = Arrow(trans_group.get_right(), output_group.get_left(), buff=0.2, color=WHITE)

        # Animate Structure Creation
        self.play(
            LaggedStartMap(FadeIn, blocks, lag_ratio=0.2),
            run_time=1.5
        )
        self.play(
            Create(arrow1), Create(arrow2), Create(arrow3),
            run_time=1
        )

        # Create Data Packet
        data_packet = Circle(radius=0.15, color=WHITE, fill_opacity=1)
        data_packet.move_to(input_group)

        # Animate Flow: Input -> CNN
        self.play(
            data_packet.animate.move_to(cnn_group),
            rate_func=rate_functions.smooth,
            run_time=1
        )
        
        # Animate Flow: CNN -> Transformer
        self.play(
            data_packet.animate.move_to(trans_group),
            rate_func=rate_functions.smooth,
            run_time=1
        )

        # Animate Flow: Transformer -> Output
        self.play(
            data_packet.animate.move_to(output_group),
            rate_func=rate_functions.smooth,
            run_time=1
        )

        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class BridgeConnection(Scene):
    def construct(self):
        # Define positions
        vision_pos = LEFT * 3.5
        lang_pos = RIGHT * 3.5

        # Create Vision Island
        vision_island = Ellipse(width=2.5, height=1.8, color=BLUE, fill_opacity=0.3, stroke_width=4)
        vision_text = Text("Vision", weight=BOLD, color=BLUE)
        vision_group = VGroup(vision_island, vision_text).move_to(vision_pos)

        # Create Language Island
        lang_island = Ellipse(width=2.5, height=1.8, color=ORANGE, fill_opacity=0.3, stroke_width=4)
        lang_text = Text("Language", weight=BOLD, color=ORANGE)
        lang_group = VGroup(lang_island, lang_text).move_to(lang_pos)

        # Animate Islands appearing
        self.play(FadeIn(vision_group), FadeIn(lang_group), run_time=1)
        self.wait(0.5)

        # Create the Bridge (Line connecting centers, placed behind islands)
        bridge = Line(vision_pos, lang_pos, color=YELLOW, stroke_width=10)
        bridge.set_z_index(-1)
        
        # Animate Bridge creation
        self.play(Create(bridge), rate_func=rate_functions.smooth, run_time=1)
        self.wait(0.5)

        # Create Data Particles (Dots)
        num_dots = 5
        dots = [Dot(color=WHITE, radius=0.15) for _ in range(num_dots)]

        # Animate data flowing from Vision to Language
        self.play(
            *[
                MoveAlongPath(dot, bridge, rate_func=rate_functions.linear)
                for dot in dots
            ],
            lag_ratio=0.2,
            run_time=2
        )

        # Create particles for reverse flow
        dots_rev = [Dot(color=WHITE, radius=0.15) for _ in range(num_dots)]

        # Animate data flowing from Language to Vision
        self.play(
            *[
                MoveAlongPath(dot, bridge, rate_func=rate_functions.linear, reverse=True)
                for dot in dots_rev
            ],
            lag_ratio=0.2,
            run_time=2
        )

        self.wait(0.5)


# ==================== Auto-Generated ====================
from manim import *

class ProbabilityFlow(Scene):
    def construct(self):
        # 1. Input: Clue
        clue_box = Rectangle(height=1.2, width=2.5, color=BLUE, stroke_width=3)
        clue_text = Text("Clue", color=BLUE, weight=BOLD)
        clue_group = VGroup(clue_box, clue_text).move_to(LEFT * 4)
        
        # 2. Tree Structure (Branching)
        # Start point for tree (right of Clue)
        start_point = clue_group.get_right() + RIGHT * 0.5
        
        # End points for branches (fan out)
        top_branch = start_point + RIGHT * 1.5 + UP * 1.5
        mid_branch = start_point + RIGHT * 1.5
        bot_branch = start_point + RIGHT * 1.5 + DOWN * 1.5
        
        # Lines representing probability branches
        line_top = Line(start_point, top_branch, color=GRAY, stroke_width=2)
        line_mid = Line(start_point, mid_branch, color=WHITE, stroke_width=4)
        line_bot = Line(start_point, bot_branch, color=GRAY, stroke_width=2)
        
        # Nodes at end of branches
        node_top = Circle(radius=0.15, color=GRAY).move_to(top_branch)
        node_mid = Circle(radius=0.2, color=YELLOW).move_to(mid_branch)
        node_bot = Circle(radius=0.15, color=GRAY).move_to(bot_branch)
        
        # 3. Output: Script
        script_box = Rectangle(height=1.2, width=2.5, color=GREEN, stroke_width=3)
        script_text = Text("Script", color=GREEN, weight=BOLD)
        script_group = VGroup(script_box, script_text).move_to(RIGHT * 4)
        
        # Connection from selected branch to Script
        final_line = Line(mid_branch, script_group.get_left(), color=YELLOW, stroke_width=4)

        # --- Animations ---
        
        # Show Clue
        self.play(FadeIn(clue_group))
        self.wait(0.5)
        
        # Show Tree Branching
        self.play(
            Create(line_top),
            Create(line_mid),
            Create(line_bot),
            run_time=1.5,
            rate_func=rate_functions.smooth
        )
        self.play(
            FadeIn(node_top),
            FadeIn(node_mid),
            FadeIn(node_bot)
        )
        
        # Highlight Selection (Narrowing down)
        # Dim others, Brighten middle
        self.play(
            line_top.animate.set_opacity(0.3),
            line_bot.animate.set_opacity(0.3),
            node_top.animate.set_opacity(0.3),
            node_bot.animate.set_opacity(0.3),
            line_mid.animate.set_color(YELLOW),
            node_mid.animate.scale(1.5),
            run_time=1
        )
        
        # Connect to Script
        self.play(Create(final_line), run_time=0.8)
        self.play(FadeIn(script_group))
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
import numpy as np

class ProbabilityConstraint(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 3, 1],
            axis_config={"color": WHITE}
        )
        self.add(axes)

        # Wide probability distribution (initial state)
        wide_curve = axes.plot(
            lambda x: np.exp(-0.15 * x**2),
            color=BLUE,
            stroke_width=4
        )

        # Narrow probability distribution (constrained state)
        narrow_curve = axes.plot(
            lambda x: 2.5 * np.exp(-3 * x**2),
            color=YELLOW,
            stroke_width=4
        )

        # Box representing the constraint
        box = Rectangle(
            width=2,
            height=2.5,
            color=RED,
            stroke_width=2
        )
        box.move_to(axes.c2p(0, 1.25))

        # Label
        label = Text("Prompt Constraint", color=RED)
        label.next_to(box, UP)

        # 1. Show initial wide curve
        self.play(Create(wide_curve), run_time=2)
        self.wait(1)

        # 2. Show box and transform curve to narrow peak
        self.play(
            FadeIn(box),
            Transform(wide_curve, narrow_curve, rate_func=rate_functions.ease_in_out_sine),
            run_time=3
        )

        # 3. Show label
        self.play(Write(label), run_time=1)
        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *

class CodeToChat(Scene):
    def construct(self):
        # Split screen divider
        divider = DashedLine(UP * 3.5, DOWN * 3.5, stroke_opacity=0.3)
        self.add(divider)

        # Left Side: Code (Python style)
        code_font = "Consolas"
        code_color = GREEN
        
        code_lines = VGroup(
            Text("def calculate(x):", font=code_font, color=code_color),
            Text("    result = x * 10", font=code_font, color=code_color),
            Text("    return result", font=code_font, color=code_color),
        )
        code_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        code_lines.move_to(LEFT * 3.5)
        
        # Show Code
        self.play(FadeIn(code_lines), run_time=1)
        self.wait(1)

        # Right Side: Chat Bubbles
        def create_bubble(text_content, bubble_color=BLUE):
            text_obj = Text(text_content)
            rect = RoundedRectangle(
                corner_radius=0.3,
                color=bubble_color,
                fill_color=bubble_color,
                fill_opacity=0.2,
                stroke_width=2
            )
            rect.surround(text_obj, buff=0.4)
            return VGroup(rect, text_obj)

        bubble1 = create_bubble("What does this function do?")
        bubble2 = create_bubble("It multiplies the input by 10.")
        
        chat_group = VGroup(bubble1, bubble2)
        chat_group.arrange(DOWN, aligned_edge=LEFT, buff=1)
        chat_group.move_to(RIGHT * 3.5)

        # Transition: Code fades out, Chat bubbles appear
        self.play(
            FadeOut(code_lines, rate_func=rate_functions.ease_in_sine),
            AnimationGroup(
                FadeIn(bubble1, shift=UP*0.5, rate_func=rate_functions.ease_out_back),
                FadeIn(bubble2, shift=UP*0.5, rate_func=rate_functions.ease_out_back),
                lag_ratio=0.3
            ),
            run_time=2
        )
        
        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *

class ParameterScale(Scene):
    def construct(self):
        # Title label
        title = Text("Parameters", font_size=36, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        # Numeric scale labels (left to right)
        scale_labels = [
            Text("1B", font_size=32),
            Text("10B", font_size=32),
            Text("1T", font_size=32),
            Text("10T", font_size=32),
        ]
        
        # Position horizontally centered
        scale_group = VGroup(*scale_labels).arrange(RIGHT, buff=2.0)
        scale_group.next_to(title, DOWN, buff=1.5)
        
        # Neuron cluster: small circles grouped as a cluster
        neurons = VGroup(*[Circle(radius=0.1, color=BLUE, fill_opacity=0.7) for _ in range(12)])
        neurons.arrange_in_grid(4, 3, buff=0.3)
        neurons.scale(0.8)
        neurons.next_to(scale_group, DOWN, buff=2.0)
        
        # Label for neuron cluster
        param_label = Text("参数量", font="Microsoft YaHei", font_size=28)
        param_label.next_to(neurons, DOWN, buff=0.8)
        
        # Animate
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(Write(scale_group), run_time=2)
        self.wait(0.5)
        
        # Zoom effect: scale up neurons and fade in
        self.play(
            FadeIn(neurons),
            scale_group.animate.scale(0.8).set_opacity(0.7),
            title.animate.scale(0.9).set_opacity(0.7),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(Write(param_label), run_time=1)
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class LanguageModelEquation(Scene):
    def construct(self):
        # Title
        title = Text("Language Modeling", font_size=36, weight=BOLD)
        subtitle = Text("语言规律建模", font_size=28, font="Microsoft YaHei")

        # Equation parts
        left_side = MathTex(
            r"P(\text{word}_{n+1} \mid \text{word}_1\ldots\text{word}_n)",
            font_size=32
        )
        equals = MathTex(r"=", font_size=32)
        right_side = MathTex(r"f(\ldots)", font_size=32)

        equation = VGroup(left_side, equals, right_side).arrange(RIGHT, buff=0.3)

        # Group all elements
        content = VGroup(title, subtitle, equation).arrange(DOWN, buff=0.8)
        content.move_to(ORIGIN)

        # Animate
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        self.play(Write(subtitle), run_time=1)
        self.wait(0.5)
        self.play(Write(left_side), run_time=1.2)
        self.wait(0.3)
        self.play(Write(equals), Write(right_side), run_time=1.2)
        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *
import random

class ProbabilityBars(Scene):
    def construct(self):
        # Set up axes
        axes = Axes(
            x_range=[0, 3, 1],
            y_range=[0, 1.1, 0.2],
            x_length=8,
            y_length=5,
            axis_config={"include_ticks": False},
            y_axis_config={"include_numbers": True, "font_size": 24},
        ).to_edge(DOWN, buff=0.5)

        # Bar labels and heights
        labels = ["你", "吃", "其他"]
        heights = [0.99, 0.001, 0.0001]
        colors = [BLUE, GREEN, GRAY]

        # Create bars
        bars = VGroup()
        bar_width = 0.6
        for i, (label, h, color) in enumerate(zip(labels, heights, colors)):
            bar = Rectangle(
                height=h * axes.y_length,
                width=bar_width,
                fill_color=color,
                fill_opacity=0.8,
                stroke_width=1
            )
            bar.move_to(axes.c2p(i, h/2))
            bars.add(bar)

        # Add labels under bars
        label_texts = VGroup()
        for i, label in enumerate(labels):
            text = Text(label, font="Microsoft YaHei", font_size=32).next_to(axes.c2p(i, 0), DOWN, buff=0.3)
            label_texts.add(text)

        # Add percentage texts on top of bars
        perc_texts = VGroup()
        percs = ["99%", "0.1%", "<0.01%"]
        for i, (h, perc) in enumerate(zip(heights, percs)):
            if h > 0.0005:
                txt = Text(perc, font_size=24, color=WHITE).next_to(bars[i].get_top(), UP, buff=0.1)
                perc_texts.add(txt)

        # Animate bars
        self.play(
            Create(axes),
            LaggedStart(*[GrowFromBottom(bar) for bar in bars], lag_ratio=0.3),
            run_time=2
        )
        self.wait(0.5)
        self.play(Write(label_texts), Write(perc_texts))

        # Spark animation: small circles around bars
        sparks = VGroup()
        for _ in range(30):
            i = random.randint(0, 2)
            x = axes.c2p(i, heights[i])[0] + (random.random() - 0.5) * 0.8
            y = axes.c2p(0, heights[i])[1] + (random.random() - 0.5) * 0.5
            spark = Circle(radius=0.03, color=YELLOW, fill_opacity=1).move_to([x, y, 0])
            sparks.add(spark)

        self.play(LaggedStart(
            *[Flash(spark, color=YELLOW, flash_radius=0.2, line_stroke_width=2) for spark in sparks],
            lag_ratio=0.02,
            run_time=3
        ))

        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class MultimodalMerge(Scene):
    def construct(self):
        # Create three icons as Text (using Unicode emoji)
        text_icon = Text("A", font_size=48, color=BLUE)
        image_icon = Text("🖼️", font_size=48, color=GREEN)
        audio_icon = Text("🎵", font_size=48, color=RED)

        # Position them in a triangle
        text_icon.move_to(UP * 2 + LEFT * 2.5)
        image_icon.move_to(DOWN * 1.5 + LEFT * 1)
        audio_icon.move_to(DOWN * 1.5 + RIGHT * 1)

        # Create target sphere (as a circle with label)
        sphere = Circle(color=WHITE, radius=1.2, stroke_width=3)
        label = Text("Multimodal", font_size=24, color=YELLOW).move_to(sphere.get_center())

        # Animate merge: icons move toward center and transform into sphere + label
        self.play(
            Write(text_icon),
            Write(image_icon),
            Write(audio_icon),
            run_time=1.5
        )
        self.wait(0.5)

        self.play(
            text_icon.animate.move_to(sphere.get_center()).scale(0.01).set_opacity(0),
            image_icon.animate.move_to(sphere.get_center()).scale(0.01).set_opacity(0),
            audio_icon.animate.move_to(sphere.get_center()).scale(0.01).set_opacity(0),
            Create(sphere),
            Write(label),
            run_time=2,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *

class LLMNameReveal(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BLACK

        # Full name text
        full_name = Text("Large Language Model", font="Fira Code", weight=MEDIUM, font_size=36, color=WHITE)
        
        # Acronym text
        acronym = Text("LLM", font="Fira Code", weight=BOLD, font_size=64, color=WHITE)

        # Position full name at top
        full_name.move_to(UP * 2)

        # Position acronym at bottom center
        acronym.move_to(DOWN * 2)

        # Connection line (glowing effect)
        line = Line(full_name.get_bottom(), acronym.get_top(), stroke_width=2, color=BLUE_D)
        line.set_stroke(width=4)
        line.set_z_index(-1)

        # Glow effect via multiple copies with fading opacity and increasing width
        glow_lines = VGroup()
        for i in range(5):
            gline = line.copy()
            gline.set_stroke(opacity=0.3 - 0.05*i, width=4 + i*2, color=BLUE_A)
            glow_lines.add(gline)

        # Animate reveal
        self.play(Write(full_name), run_time=1.5)
        self.wait(0.5)
        self.play(
            Create(line),
            FadeIn(glow_lines),
            run_time=1.2,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(0.5)
        self.play(
            TransformMatchingShapes(full_name.copy(), acronym),
            run_time=1.8,
            rate_func=rate_functions.ease_out_cubic
        )
        self.wait(1)

        # Optional: subtle pulse on acronym
        self.play(
            acronym.animate.scale(1.05).set_color(BLUE_B),
            run_time=0.6,
            rate_func=rate_functions.there_and_back
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
import numpy as np

class PhysicsVsLanguage(Scene):
    def construct(self):
        # Split screen
        left_rect = Rectangle(height=7, width=6, color=WHITE, stroke_width=1).to_edge(LEFT, buff=0.5)
        right_rect = Rectangle(height=7, width=6, color=WHITE, stroke_width=1).to_edge(RIGHT, buff=0.5)
        
        # Left: Physics — cannonball trajectory
        axes_left = Axes(
            x_range=[-3, 3, 1],
            y_range=[-9, 1, 1],
            x_length=5,
            y_length=5,
            axis_config={"color": GRAY},
            tips=False
        ).move_to(left_rect.get_center())
        
        # Parabola y = -x²
        parabola = axes_left.plot(lambda x: -x**2, x_range=[-2.5, 2.5], color=BLUE, stroke_width=3)
        ball = Dot(axes_left.c2p(0, 0), color=YELLOW, radius=0.12)
        
        # Animate trajectory
        tracker = ValueTracker(-2.5)
        ball.add_updater(lambda m: m.move_to(axes_left.c2p(tracker.get_value(), -tracker.get_value()**2)))
        
        # Right: Language — word cloud + heatmap
        # "hello world" as text group with size variation
        hello = Text("hello", font_size=48, color=GREEN).shift(UP * 1.2)
        world = Text("world", font_size=64, color=ORANGE).shift(DOWN * 0.5)
        word_group = VGroup(hello, world)
        
        # Heatmap under 'world': semi-transparent red rectangle fading toward edges
        heatmap_base = Rectangle(
            width=world.width * 1.4,
            height=world.height * 0.6,
            fill_color=RED,
            fill_opacity=0.0,
            stroke_width=0
        ).next_to(world, DOWN, buff=0.2)
        
        # Create gradient-like heatmap using multiple stacked rectangles with varying opacity
        heatmap_layers = VGroup()
        for i in range(5):
            alpha = 0.3 - 0.05 * i
            layer = Rectangle(
                width=heatmap_base.width * (0.8 - 0.1 * i),
                height=heatmap_base.height * (0.8 - 0.1 * i),
                fill_color=RED,
                fill_opacity=alpha,
                stroke_width=0
            ).move_to(heatmap_base.get_center())
            heatmap_layers.add(layer)
        
        # Animation sequence
        self.play(
            Create(left_rect),
            Create(right_rect),
            run_time=0.8
        )
        self.wait(0.2)
        
        # Left side: draw axes and parabola
        self.play(
            Create(axes_left),
            Create(parabola),
            run_time=1.5
        )
        
        # Right side: reveal words
        self.play(
            Write(hello),
            Write(world),
            run_time=1.2
        )
        
        # Add heatmap layers smoothly
        self.play(
            FadeIn(heatmap_layers, shift=UP * 0.3, scale=0.8),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        
        # Animate ball along trajectory
        self.play(
            tracker.animate.set_value(2.5),
            run_time=3.0,
            rate_func=rate_functions.ease_out_quad
        )
        
        # Final hold
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class ProbabilityDistribution(Scene):
    def construct(self):
        # Set up axes
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1.1, 0.2],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": False},
        )
        axes_labels = axes.get_axis_labels(x_label="", y_label="")

        # Bar data: (label, height, color)
        bars_data = [
            ("你", 0.99, GREEN),
            ("吃", 0.001, RED),
            ("睡", 0.0005, BLUE),
        ]

        # Create bar chart manually
        bar_width = 0.6
        bars = VGroup()
        labels = VGroup()
        values = VGroup()

        for i, (label_text, height, color) in enumerate(bars_data):
            # Position x
            x_pos = i + 1
            # Bar
            bar = Rectangle(
                width=bar_width,
                height=height * axes.y_length,
                fill_color=color,
                fill_opacity=0.8,
                stroke_color=color,
                stroke_width=1,
            )
            bar.move_to(axes.c2p(x_pos, height / 2), aligned_edge=DOWN)

            # Label
            label = Text(label_text, font="Microsoft YaHei", font_size=24).next_to(bar, DOWN, buff=0.3)

            # Value text
            if height >= 0.01:
                value_str = f"{height * 100:.1f}%"
            else:
                value_str = f"{height * 100:.2f}%"
            value = Text(value_str, font="Microsoft YaHei", font_size=20, color=color).next_to(bar, UP, buff=0.1)

            bars.add(bar)
            labels.add(label)
            values.add(value)

        # Add background grid
        axes.add_coordinate_labels(font_size=20)
        self.add(axes, axes_labels)

        # Animate bars growing
        self.play(
            *[GrowFromBottom(bar, rate_func=rate_functions.smooth) for bar in bars],
            run_time=2
        )
        self.wait(0.5)

        # Animate labels and values appearing
        self.play(
            Write(labels),
            Write(values),
            run_time=1.5
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
import random

class TextOnlyFlow(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BLACK

        # Create crossed-out icons
        photo_icon = Text("📷", font_size=60)
        audio_icon = Text("🎧", font_size=60)
        check_note_icon = Text("✅📝", font_size=60)

        # Cross out photo and audio
        photo_cross = Line(
            photo_icon.get_corner(UL), 
            photo_icon.get_corner(DR), 
            color=RED, 
            stroke_width=6
        )
        audio_cross = Line(
            audio_icon.get_corner(UL), 
            audio_icon.get_corner(DR), 
            color=RED, 
            stroke_width=6
        )

        # Group icons with crosses
        photo_group = VGroup(photo_icon, photo_cross)
        audio_group = VGroup(audio_icon, audio_cross)
        check_note_group = VGroup(check_note_icon)

        # Position icons horizontally centered
        icons = VGroup(photo_group, audio_group, check_note_group).arrange(RIGHT, buff=2)
        icons.move_to(ORIGIN + UP * 2)

        # Fade in icons
        self.play(
            FadeIn(photo_group),
            FadeIn(audio_group),
            FadeIn(check_note_group),
            run_time=1.5
        )
        self.wait(0.5)

        # Animate glowing effect on ✅📝
        self.play(
            check_note_icon.animate.set_color(YELLOW).scale(1.1),
            rate_func=there_and_back,
            run_time=2
        )

        # ASCII stream: generate a long string of random ASCII chars (letters, digits, symbols)
        ascii_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
        stream_length = 120
        stream_text = Text(
            "".join(random.choice(ascii_chars) for _ in range(stream_length)),
            font_size=24,
            color=GREY_A
        ).move_to(DOWN * 2.5)

        # Animate left-to-right flow by shifting x-position
        # We'll animate the text moving from right to left across screen
        stream_text.shift(RIGHT * config.frame_width / 2)
        self.play(
            stream_text.animate.shift(LEFT * config.frame_width * 1.5),
            run_time=8,
            rate_func=linear
        )
        self.wait(0.5)


# ==================== Auto-Generated ====================
from manim import *
import numpy as np

class LanguageVsPhysics(Scene):
    def construct(self):
        # Split screen
        left_rect = Rectangle(height=7, width=6, color=WHITE, stroke_width=1).to_edge(LEFT, buff=0.5)
        right_rect = Rectangle(height=7, width=6, color=WHITE, stroke_width=1).to_edge(RIGHT, buff=0.5)
        divider = Line(UP * 3.5, DOWN * 3.5, stroke_width=2).move_to(ORIGIN)

        # Titles
        physics_title = Text("Physics: Projectile Motion", font_size=24, weight=BOLD).to_edge(UP).shift(LEFT * 3)
        lang_title = Text("Language: Word Probability", font_size=24, weight=BOLD).to_edge(UP).shift(RIGHT * 3)

        self.add(left_rect, right_rect, divider, physics_title, lang_title)

        # === LEFT: Newton's parabola & projectile animation ===
        # Axes
        ax_phys = Axes(
            x_range=[0, 8, 2],
            y_range=[0, 5, 1],
            axis_config={"color": GRAY, "stroke_width": 1},
            tips=False
        ).scale(0.6).move_to(LEFT * 2.5 + DOWN * 0.5)

        # Parabola: y = -0.2x² + 2x (approx. projectile path, g=4, v₀=4√2, θ=45°)
        parabola = ax_phys.plot(lambda x: -0.2*x**2 + 2*x, x_range=[0, 8], color=BLUE, stroke_width=2)

        # Projectile dot
        proj_dot = Dot(color=YELLOW, radius=0.08).move_to(ax_phys.c2p(0, 0))

        # Label equation
        eq_physics = MathTex("y = -\\frac{g}{2v_{0x}^2}x^2 + \\tan\\theta\\,x", font_size=28, color=BLUE)
        eq_physics.next_to(ax_phys, DOWN, buff=0.3)

        self.add(ax_phys, parabola, eq_physics)

        # === RIGHT: Language probability curve ===
        ax_lang = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 1.2, 0.2],
            axis_config={"color": GRAY, "stroke_width": 1},
            tips=False
        ).scale(0.6).move_to(RIGHT * 2.5 + DOWN * 0.5)

        # Smooth unimodal curve peaking at x=5 ("next word")
        def lang_curve(x):
            return 1.0 * np.exp(-0.3 * (x - 5)**2)

        curve_lang = ax_lang.plot(lang_curve, x_range=[0, 10], color=GREEN, stroke_width=2)

        # "next word" label at peak
        next_word_label = Text("next word", font_size=20, color=GREEN).next_to(ax_lang.c2p(5, lang_curve(5)), UP, buff=0.2)

        # X-axis labels
        x_labels = VGroup(
            Text("context", font_size=16).next_to(ax_lang.c2p(0, 0), DOWN, buff=0.15),
            Text("prediction", font_size=16).next_to(ax_lang.c2p(10, 0), DOWN, buff=0.15)
        )

        self.add(ax_lang, curve_lang, next_word_label, x_labels)

        # Animate synchronized:
        # — Projectile moves along parabola
        # — Language curve rises and peaks in sync

        # Create time parameter for smooth sync
        t_max = 8.0
        tracker = ValueTracker(0)

        # Projectile position updater
        def update_proj(mob):
            x = tracker.get_value()
            if 0 <= x <= t_max:
                y = -0.2 * x**2 + 2 * x
                mob.move_to(ax_phys.c2p(x, y))
            else:
                mob.move_to(ax_phys.c2p(t_max, -0.2*t_max**2 + 2*t_max))

        proj_dot.add_updater(update_proj)

        # Language curve opacity/height morph (simplified: scale y-values with time)
        curve_lang_copy = curve_lang.copy()
        curve_lang_copy.set_opacity(0)
        self.add(curve_lang_copy)

        def update_curve(mob):
            t = tracker.get_value()
            # Ramp up to peak at t=5, then hold
            alpha = min(t / 5.0, 1.0) if t <= 5 else 1.0
            mob.become(
                ax_lang.plot(
                    lambda x: alpha * lang_curve(x),
                    x_range=[0, 10],
                    color=GREEN,
                    stroke_width=2
                )
            )

        curve_lang_copy.add_updater(update_curve)

        # Animate both together
        self.add(proj_dot, curve_lang_copy)
        self.play(
            tracker.animate.set_value(t_max),
            run_time=6.0,
            rate_func=rate_functions.smooth
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
import random

class TextStream(Scene):
    def construct(self):
        # Dark background
        self.camera.background_color = BLACK

        # Subtle grid
        grid = NumberPlane(
            background_line_style={"stroke_color": GRAY, "stroke_width": 1, "stroke_opacity": 0.15},
            axis_config={"stroke_opacity": 0},
            x_range=[-16, 16, 2],
            y_range=[-9, 9, 2]
        )
        self.add(grid)

        # ASCII character pool (letters, digits, punctuation)
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Generate stream of glowing text objects
        stream_mobs = VGroup()
        n_chars = 120
        for i in range(n_chars):
            char = random.choice(chars)
            text = Text(char, font="Monospace", color=BLUE_A, weight=BOLD)
            text.scale(0.8)
            # Random vertical position across screen height
            y_pos = random.uniform(-4, 4)
            # Staggered horizontal start positions to avoid clumping
            x_pos = -16 + i * 0.5 + random.uniform(-0.5, 0.5)
            text.move_to([x_pos, y_pos, 0])
            
            # Add glow effect via multiple copies with fading opacity
            glow_group = VGroup()
            for j in range(3):
                glow = text.copy()
                glow.set_opacity(0.3 - j * 0.15)
                glow.scale(1.0 + j * 0.15)
                glow.set_color(interpolate_color(BLUE_A, YELLOW, j * 0.5))
                glow_group.add(glow)
            glow_group.add(text)
            stream_mobs.add(glow_group)

        # LLM gate: clean white rectangle with centered 'LLM'
        llm_gate = RoundedRectangle(
            width=4.0,
            height=2.0,
            corner_radius=0.3,
            fill_color=WHITE,
            fill_opacity=0.05,
            stroke_color=WHITE,
            stroke_width=1.5
        )
        llm_text = Text("LLM", font="Monospace", weight=BOLD, color=WHITE)
        llm_text.scale(1.2)
        llm_gate.move_to([0, 0, 0])
        llm_text.move_to([0, 0, 0])

        # Animate stream flowing rightward
        self.play(
            stream_mobs.animate.shift(RIGHT * 32),
            run_time=8,
            rate_func=linear
        )

        # Add gate and text mid-animation
        self.play(
            FadeIn(llm_gate, shift=UP * 0.2, scale=0.8),
            Write(llm_text, run_time=1.5),
            rate_func=smooth
        )
        self.wait(0.5)

        # Final hold
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class VisionVsLanguageDualAxis(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BLACK

        # Define positions
        left_pos = LEFT * 4
        right_pos = RIGHT * 4
        center_pos = ORIGIN

        # Left pathway: Text → LLM
        text_label = Text("Text", font="Arial", weight=BOLD, color=BLUE).scale(0.8)
        llm_label = Text("LLM", font="Arial", weight=BOLD, color=GREEN).scale(0.8)
        left_group = VGroup(text_label, llm_label).arrange(RIGHT, buff=1.5)
        left_group.move_to(left_pos)

        # Right pathway: Image → CV
        image_label = Text("Image", font="Arial", weight=BOLD, color=RED).scale(0.8)
        cv_label = Text("CV", font="Arial", weight=BOLD, color=ORANGE).scale(0.8)
        right_group = VGroup(image_label, cv_label).arrange(RIGHT, buff=1.5)
        right_group.move_to(right_pos)

        # Center node
        center_label = Text("Multimodal Understanding", font="Arial", weight=BOLD, color=YELLOW).scale(0.7)
        center_label.move_to(center_pos + UP * 0.5)

        # Arrows
        left_arrow = Arrow(
            start=left_group.get_right(),
            end=center_label.get_left() + LEFT * 0.3,
            buff=0.1,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.08,
            color=BLUE
        )
        right_arrow = Arrow(
            start=right_group.get_left(),
            end=center_label.get_right() + RIGHT * 0.3,
            buff=0.1,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.08,
            color=RED
        )

        # Optional subtle background elements (optional visual depth)
        left_path_bg = Rectangle(
            width=6, height=1.2, fill_opacity=0.1, fill_color=BLUE, stroke_width=0
        ).move_to(left_pos)
        right_path_bg = Rectangle(
            width=6, height=1.2, fill_opacity=0.1, fill_color=RED, stroke_width=0
        ).move_to(right_pos)

        # Add all elements
        self.add(left_path_bg, right_path_bg)
        self.play(
            Write(text_label),
            Write(llm_label),
            Write(image_label),
            Write(cv_label),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            GrowArrow(left_arrow),
            GrowArrow(right_arrow),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(Write(center_label), run_time=1.2)
        self.wait(1.5)


# ==================== Auto-Generated ====================
from manim import *

class PixelMatrixReveal(Scene):
    def construct(self):
        # Simulated low-res 5x4 pixel grid (grayscale values 0–255)
        pixel_values = [
            [120, 85, 160, 90, 130],
            [75, 140, 60, 110, 80],
            [180, 95, 210, 105, 170],
            [65, 125, 70, 150, 85]
        ]
        
        rows, cols = len(pixel_values), len(pixel_values[0])
        cell_size = 0.6
        grid = VGroup()
        text_grid = VGroup()
        
        # Create pixel cells and value labels
        for i in range(rows):
            for j in range(cols):
                rect = Rectangle(
                    width=cell_size,
                    height=cell_size,
                    fill_color=grayscale_color(pixel_values[i][j]),
                    fill_opacity=1,
                    stroke_width=0.5,
                    stroke_color=GREY_A
                )
                rect.move_to(np.array([(j - (cols-1)/2) * cell_size, -(i - (rows-1)/2) * cell_size, 0]))
                grid.add(rect)
                
                txt = Text(
                    str(pixel_values[i][j]),
                    font_size=16,
                    color=BLACK if pixel_values[i][j] > 127 else WHITE
                )
                txt.move_to(rect.get_center())
                text_grid.add(txt)
        
        # Group all pixel elements
        pixel_group = VGroup(grid, text_grid)
        pixel_group.scale(1.5).move_to(ORIGIN)
        
        # Placeholder cat image — represented as a smooth grayscale gradient rectangle
        # Since we can't load external images, simulate the "revealed photo" with a soft-shaded rounded rectangle
        cat_photo = RoundedRectangle(
            width=8.0,
            height=5.0,
            corner_radius=0.3,
            fill_color=GREY_B,
            fill_opacity=1,
            stroke_width=0
        )
        # Add subtle internal shading to suggest feline features (e.g., ears via small ellipses)
        left_ear = Ellipse(width=0.8, height=1.2, fill_color=GREY_C, fill_opacity=1, stroke_width=0).rotate(0.3).shift(LEFT*2.8 + UP*1.4)
        right_ear = Ellipse(width=0.8, height=1.2, fill_color=GREY_C, fill_opacity=1, stroke_width=0).rotate(-0.3).shift(RIGHT*2.8 + UP*1.4)
        face_shade = Circle(radius=1.6, fill_color=GREY_D, fill_opacity=0.3, stroke_width=0).move_to(ORIGIN)
        cat_photo_group = VGroup(cat_photo, left_ear, right_ear, face_shade)
        cat_photo_group.scale(0.01).move_to(ORIGIN)  # Start tiny
        
        # Animate: show pixel grid, then zoom out while fading numbers and sharpening image
        self.play(FadeIn(pixel_group), run_time=1.5)
        self.wait(0.5)
        
        # Simultaneous transform: grid zooms out → becomes photo; numbers fade; photo scales up & sharpens (opacity/fill refines)
        self.play(
            pixel_group.animate.scale(0.01).move_to(ORIGIN),
            text_grid.animate.set_opacity(0),
            FadeIn(cat_photo_group),
            cat_photo_group.animate.scale(100).set_opacity(1),
            run_time=3.5,
            rate_func=rate_functions.ease_out_quad
        )
        
        # Final sharpen: replace low-res with clean high-res appearance
        self.play(
            cat_photo.animate.set_fill(GREY_A, opacity=1),
            left_ear.animate.set_fill(GREY_B),
            right_ear.animate.set_fill(GREY_B),
            face_shade.animate.set_fill(GREY_E, opacity=0.4),
            run_time=1.5
        )
        self.wait(1)

def grayscale_color(value):
    # Map 0–255 → [0,1] for Manim grayscale
    gray_level = value / 255.0
    return rgb_to_color([gray_level, gray_level, gray_level])


# ==================== Auto-Generated ====================
from manim import *

class HierarchicalFeatureExtraction(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Title
        title = Text("Hierarchical Feature Extraction", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)

        # Layer labels
        layer_labels = VGroup(
            Text("Edges", font_size=24, color=BLUE),
            Text("Textures", font_size=24, color=TEAL),
            Text("Parts", font_size=24, color=GOLD),
            Text("Full Object (Cat)", font_size=24, color=RED)
        ).arrange(DOWN, buff=1.2).shift(DOWN * 0.5)

        # Feature map placeholders (simplified as colored rectangles with labels)
        feature_maps = VGroup()
        for i, label in enumerate(layer_labels):
            rect = RoundedRectangle(height=1.0, width=2.0, corner_radius=0.2, fill_opacity=0.7,
                                   fill_color=[BLUE, TEAL, GOLD, RED][i], stroke_width=1.5)
            rect.next_to(label, DOWN, buff=0.5)
            feature_maps.add(rect)

        # Add labels and maps
        self.play(LaggedStart(*[Write(lbl) for lbl in layer_labels], lag_ratio=0.3), run_time=2)
        self.wait(0.5)
        self.play(LaggedStart(*[Create(fm) for fm in feature_maps], lag_ratio=0.3), run_time=2)
        self.wait(0.5)

        # CNN and ViT icons (stylized)
        cnn_icon = VGroup(
            Rectangle(height=0.8, width=0.8, fill_color=BLUE_E, fill_opacity=1, stroke_width=0),
            Text("CNN", font_size=16, weight=BOLD).move_to(ORIGIN)
        ).scale(0.7).to_edge(DL, buff=0.8)

        vit_icon = VGroup(
            Circle(radius=0.4, fill_color=PURPLE_E, fill_opacity=1, stroke_width=0),
            Text("ViT", font_size=16, weight=BOLD).move_to(ORIGIN)
        ).scale(0.7).to_edge(DR, buff=0.8)

        # Add icons
        self.play(FadeIn(cnn_icon), FadeIn(vit_icon), run_time=1)
        self.wait(0.5)

        # Pulsing animation for both icons synchronized
        pulse_anim = AnimationGroup(
            cnn_icon.animate.scale(1.15).set_fill(opacity=0.9),
            vit_icon.animate.scale(1.15).set_fill(opacity=0.9),
            rate_func=there_and_back_with_pause,
            run_time=2
        )
        self.play(pulse_anim)
        self.play(pulse_anim)
        self.wait(0.5)

        # Highlight progression with arrows
        arrows = VGroup()
        for i in range(len(feature_maps)-1):
            arrow = Arrow(
                feature_maps[i].get_bottom(),
                feature_maps[i+1].get_top(),
                buff=0.1,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
                color=GREY_A
            )
            arrows.add(arrow)
        self.play(LaggedStart(*[Create(arrow) for arrow in arrows], lag_ratio=0.4), run_time=1.5)
        self.wait(1)

        # Final emphasis: cat silhouette in last feature map
        cat_silhouette = SVGMobject("https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat_silhouette.svg", fill_color=RED, fill_opacity=0.8, stroke_width=0).scale(0.3)
        cat_silhouette.move_to(feature_maps[-1].get_center())
        self.play(FadeIn(cat_silhouette, scale=0.8), run_time=1.2)
        self.wait(1.5)

        # Fade out all except title and final cat
        self.play(
            FadeOut(VGroup(layer_labels[:-1], feature_maps[:-1], arrows, cnn_icon, vit_icon)),
            feature_maps[-1].animate.set_fill(opacity=0.3),
            run_time=1.5
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class SiloToBridge(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Towers
        vision_tower = Rectangle(height=4, width=1.2, color=BLUE, fill_opacity=0.8)
        language_tower = Rectangle(height=4, width=1.2, color=GREEN, fill_opacity=0.8)
        vision_tower.shift(LEFT * 4)
        language_tower.shift(RIGHT * 4)

        vision_label = Text("Vision", font="Arial", weight=BOLD, color=WHITE).next_to(vision_tower, UP, buff=0.3)
        language_label = Text("Language", font="Arial", weight=BOLD, color=WHITE).next_to(language_tower, UP, buff=0.3)

        # Initial state: towers only
        self.play(
            Create(vision_tower),
            Create(language_tower),
            Write(vision_label),
            Write(language_label),
            run_time=1.5
        )
        self.wait(0.5)

        # Bridge (glowing line + highlight)
        bridge_line = Line(
            vision_tower.get_right(),
            language_tower.get_left(),
            stroke_width=6,
            color=YELLOW
        )
        bridge_glow = bridge_line.copy().set_stroke(YELLOW_E, width=12).set_opacity(0.6)

        # Arrows
        arrow1 = Arrow(
            vision_tower.get_right(),
            language_tower.get_left(),
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.08,
            color=YELLOW
        )
        arrow2 = Arrow(
            language_tower.get_left(),
            vision_tower.get_right(),
            buff=0,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.08,
            color=YELLOW
        )

        # VLM emblem
        vlm_emblem = Text("VLM", font="Arial", weight=BOLD, color=WHITE, font_size=36)

        # Animate bridge formation
        self.play(
            FadeIn(bridge_glow, scale=0.8),
            Create(bridge_line),
            run_time=1.2,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.play(
            GrowArrow(arrow1),
            GrowArrow(arrow2),
            run_time=1
        )
        self.play(
            Write(vlm_emblem.move_to(bridge_line.get_center())),
            vlm_emblem.animate.scale(1.2).set_color(YELLOW_D),
            run_time=0.8
        )
        self.wait(1.5)


# ==================== Auto-Generated ====================
from manim import *

class DiscriminativeSorter(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BLACK

        # Left half screen: robotic arm and sorting visuals
        left_rect = Rectangle(
            width=config.frame_width / 2,
            height=config.frame_height,
            fill_opacity=0.05,
            stroke_color=GRAY,
            stroke_width=1
        ).to_edge(LEFT, buff=0)

        # Robotic arm base and arm (simplified)
        base = Circle(radius=0.3, color=BLUE_E, fill_opacity=1)
        arm = Rectangle(width=2.5, height=0.15, color=BLUE_D, fill_opacity=1).next_to(base, RIGHT, buff=0)
        gripper_left = Rectangle(width=0.1, height=0.4, color=BLUE_B, fill_opacity=1).move_to(arm.get_right() + RIGHT*0.1 + UP*0.1)
        gripper_right = Rectangle(width=0.1, height=0.4, color=BLUE_B, fill_opacity=1).move_to(arm.get_right() + RIGHT*0.1 + DOWN*0.1)
        arm_group = VGroup(base, arm, gripper_left, gripper_right).move_to(LEFT * 2.5)

        # Cat and dog icons (simple text-based for portability)
        cat = Text("🐱", font_size=48).shift(LEFT * 4 + UP * 1.5)
        dog = Text("🐶", font_size=48).shift(LEFT * 4 + DOWN * 1.5)

        # Arrows showing motion toward arm
        arrow_cat = Arrow(start=cat.get_right(), end=arm_group.get_left() + UP*0.3, buff=0.1, stroke_width=2, color=YELLOW_A)
        arrow_dog = Arrow(start=dog.get_right(), end=arm_group.get_left() + DOWN*0.3, buff=0.1, stroke_width=2, color=YELLOW_A)

        # Labels for images
        cat_label = Text("猫", font="Microsoft YaHei", font_size=24).next_to(cat, DOWN, buff=0.2)
        dog_label = Text("狗", font="Microsoft YaHei", font_size=24).next_to(dog, DOWN, buff=0.2)

        # Overlay formula: P(Y|X) in glowing blue
        formula = MathTex(r"P(Y|X)", color=BLUE_C, font_size=60)
        formula.set_stroke(BLUE_A, width=2, opacity=0.7)
        formula.to_edge(UP, buff=0.8).to_edge(LEFT, buff=1.0)

        # Label '分类员' below formula
        classifier_label = Text("分类员", font="Microsoft YaHei", font_size=32, color=WHITE)
        classifier_label.next_to(formula, DOWN, buff=0.5)

        # Animate
        self.play(
            Create(left_rect),
            Create(arm_group),
            Write(cat), Write(dog),
            Write(cat_label), Write(dog_label),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(
            GrowArrow(arrow_cat),
            GrowArrow(arrow_dog),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(
            Write(formula),
            run_time=1.2
        )
        self.wait(0.3)
        self.play(
            Write(classifier_label),
            formula.animate.set_stroke(opacity=1.0),
            run_time=1.0
        )
        self.wait(1.5)


# ==================== Auto-Generated ====================
from manim import *

class GenerativePainter(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Right half screen: abstract cat drawing (simplified geometric cat)
        cat_group = VGroup()
        
        # Cat head (circle)
        head = Circle(radius=1.2, color=WHITE, stroke_width=3)
        cat_group.add(head)
        
        # Ears (triangles)
        ear_left = Polygon(
            [-0.8, 0.8, 0], [-1.4, 1.6, 0], [-0.2, 1.6, 0],
            fill_opacity=1, fill_color=WHITE, stroke_width=2
        )
        ear_right = Polygon(
            [0.8, 0.8, 0], [0.2, 1.6, 0], [1.4, 1.6, 0],
            fill_opacity=1, fill_color=WHITE, stroke_width=2
        )
        cat_group.add(ear_left, ear_right)
        
        # Eyes (small circles)
        eye_left = Circle(radius=0.15, color=BLACK, fill_opacity=1).move_to([-0.4, 0.2, 0])
        eye_right = Circle(radius=0.15, color=BLACK, fill_opacity=1).move_to([0.4, 0.2, 0])
        cat_group.add(eye_left, eye_right)
        
        # Nose (small triangle)
        nose = Polygon(
            [-0.2, -0.2, 0], [0.2, -0.2, 0], [0, -0.45, 0],
            fill_opacity=1, fill_color=BLACK
        )
        cat_group.add(nose)
        
        # Mouth (curved line)
        mouth = ArcBetweenPoints(
            [-0.3, -0.5, 0], [0.3, -0.5, 0],
            angle=-PI/2,
            stroke_width=2, color=BLACK
        )
        cat_group.add(mouth)
        
        # Position cat on right half
        cat_group.move_to(RIGHT * 3.5 + UP * 0.5)
        
        # Glowing pen effect: animate drawing with glowing stroke
        pen_glow = head.copy().set_stroke(YELLOW, width=6, opacity=0.7).set_fill(opacity=0)
        pen_glow.scale(1.05)

        # Draw sequence: head → ears → eyes → nose → mouth
        draw_order = [
            head,
            ear_left, ear_right,
            eye_left, eye_right,
            nose,
            mouth
        ]
        
        # Animate drawing with glow
        for obj in draw_order:
            self.play(
                Create(obj, rate_func=rate_functions.ease_in_out_sine),
                FadeIn(pen_glow.copy().replace(obj), scale=0.8),
                run_time=0.8
            )
        self.wait(0.5)

        # Left half: pulsing 'P(X)' in gold
        px_formula = Text("P(X)", font_size=64, color=GOLD, weight=BOLD)
        px_formula.move_to(LEFT * 4)
        
        # Pulsing animation using scale and opacity
        self.play(
            px_formula.animate.scale(1.0).set_opacity(1),
            run_time=0.1
        )
        for _ in range(3):
            self.play(
                px_formula.animate.scale(1.15).set_opacity(0.9),
                rate_func=rate_functions.there_and_back,
                run_time=1.2
            )
            self.play(
                px_formula.animate.scale(1.0).set_opacity(1),
                rate_func=rate_functions.there_and_back,
                run_time=1.2
            )

        # Label '创作家' below the cat
        creator_label = Text("创作家", font="Microsoft YaHei", font_size=36, color=WHITE)
        creator_label.next_to(cat_group, DOWN, buff=0.8)

        self.play(FadeIn(creator_label, shift=UP * 0.3))
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class TextFormulaAnimation(Scene):
    def construct(self):
        # Use clean, bold sans-serif font; avoid LaTeX for cartoon style
        text = Text("Large Language Model (LLM)", font="Arial", weight=BOLD, font_size=42)
        text.set_color_by_gradient(BLUE, PURPLE)

        # Glowing underline
        underline = Line(
            start=text.get_left() + DOWN * 0.3,
            end=text.get_right() + DOWN * 0.3,
            stroke_width=6,
            color=BLUE
        )
        # Add glow effect via multiple copies with decreasing opacity and size
        glow = VGroup()
        for i in range(5):
            u = underline.copy()
            u.set_stroke(width=6 - i*1.2, opacity=0.2 - i*0.04)
            u.shift(IN * 0.02 * i)
            glow.add(u)

        # Group text and glow
        group = VGroup(text, glow).move_to(ORIGIN)

        # Subtle zoom-in effect with gentle ease
        self.play(
            group.animate.scale(1.05).shift(UP * 0.1),
            rate_func=rate_functions.ease_in_sine,
            run_time=2
        )
        self.wait(0.5)
        self.play(
            group.animate.scale(0.98).shift(DOWN * 0.05),
            rate_func=rate_functions.ease_out_sine,
            run_time=1.5
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
# Colors are already imported via 'from manim import *'

class MathModelingDiagram(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Left side: speech bubbles with Chinese words
        bubble1 = SVGMobject("assets/speech_bubble.svg").scale(0.8).set_fill(WHITE, opacity=1).set_stroke(BLUE, width=2)
        bubble2 = SVGMobject("assets/speech_bubble.svg").scale(0.6).set_fill(WHITE, opacity=1).set_stroke(GREEN, width=2)
        bubble1.shift(LEFT * 4 + UP * 1.5)
        bubble2.shift(LEFT * 4 + DOWN * 1.5)

        # Chinese text (using Text with fallback font; avoid Tex for CJK)
        text1 = Text("语音识别", font="Microsoft YaHei", color=BLACK, weight=BOLD).scale(0.6)
        text2 = Text("情感分析", font="Microsoft YaHei", color=BLACK, weight=BOLD).scale(0.6)
        text1.move_to(bubble1.get_center())
        text2.move_to(bubble2.get_center())

        # Right side: abstract probability curves and P_w
        # Axes for curve sketch
        axes = Axes(
            x_range=[-1, 3, 1],
            y_range=[0, 1.2, 0.2],
            axis_config={"color": GRAY, "include_numbers": False},
            x_length=4,
            y_length=2.5
        ).shift(RIGHT * 3)

        # Curve: stylized probability density (e.g., two overlapping bumps)
        curve1 = axes.plot(lambda x: 0.5 * np.exp(-2*(x - 0.5)**2) + 0.3 * np.exp(-4*(x - 1.8)**2),
                           color=BLUE, stroke_width=3)
        curve2 = axes.plot(lambda x: 0.7 * np.exp(-3*(x - 1.2)**2),
                           color=GREEN, stroke_width=3)

        # P_w label
        p_w = MathTex(r"P_{w}", color=WHITE).scale(1.4).next_to(axes, UP, buff=0.5)

        # Arrow from left to right
        arrow = Arrow(
            start=bubble1.get_right(),
            end=axes.get_left(),
            buff=0.3,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.1,
            color=YELLOW
        )
        arrow_label = Text("数学建模", font="Microsoft YaHei", color=YELLOW, weight=BOLD).scale(0.6).next_to(arrow, UP, buff=0.2)

        # Group and animate
        left_group = VGroup(bubble1, bubble2, text1, text2)
        right_group = VGroup(axes, curve1, curve2, p_w)

        self.play(FadeIn(left_group), run_time=1.2)
        self.wait(0.5)
        self.play(Create(arrow), Write(arrow_label), run_time=1.2)
        self.wait(0.5)
        self.play(FadeIn(right_group), run_time=1.5)
        self.wait(1)

        # Subtle zoom/rotate for 3D cartoon feel — use perspective shift via camera
        self.play(
            self.camera.frame.animate.scale(0.95).move_to(ORIGIN),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=2
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
# Colors are already imported via 'from manim import *'

class PhysicsVsLMAnalogy(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BLACK

        # Split screen: left and right
        left_rect = Rectangle(height=6, width=6, color=BLUE, stroke_width=2).shift(LEFT * 3.5)
        right_rect = Rectangle(height=6, width=6, color=GREEN, stroke_width=2).shift(RIGHT * 3.5)

        # Left side: Physics — parabola trajectory
        axes_left = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-0.5, 4, 0.5],
            axis_config={"color": WHITE, "include_numbers": False},
            x_length=5,
            y_length=4.5,
        ).move_to(LEFT * 3.5)

        # Parabola: y = x² (simplified a=1, b=0, c=0) — upward opening
        parabola = axes_left.plot(lambda x: x**2, x_range=[-1.8, 1.8], color=YELLOW, stroke_width=3)
        trajectory_dots = VGroup(*[
            Dot(axes_left.c2p(x, x**2), color=RED, radius=0.06)
            for x in np.linspace(-1.8, 1.8, 12)
        ])
        trajectory_path = VMobject(color=RED, stroke_width=2)
        trajectory_path.set_points_as_corners([dot.get_center() for dot in trajectory_dots])

        # Equation label
        eq_label = MathTex("y = ax^2 + bx + c", color=YELLOW).scale(0.9).next_to(axes_left, UP, buff=0.3)

        # Left title
        physics_title = Text("Physics", font="Arial", weight=BOLD, color=BLUE).scale(0.8).next_to(left_rect, UP, buff=0.2)

        # Right side: LM — word sequence with probability bars
        # Word sequence
        words = ["今天", "天气", "很", "好"]
        word_mobs = VGroup(*[
            Text(word, font="Microsoft YaHei", weight=BOLD, color=WHITE).scale(0.9)
            for word in words
        ]).arrange(RIGHT, buff=1.0).move_to(RIGHT * 3.5)

        # Probability bars (rising heights: 0.3 → 0.5 → 0.7 → 0.9)
        bar_heights = [0.3, 0.5, 0.7, 0.9]
        bars = VGroup()
        labels = VGroup()
        for i, (word_mob, h) in enumerate(zip(word_mobs, bar_heights)):
            bar = Rectangle(
                height=h * 2.5,
                width=0.4,
                fill_color=GREEN,
                fill_opacity=0.7,
                stroke_color=GREEN,
                stroke_width=1.5
            ).next_to(word_mob, UP, buff=0.3)
            label = Text(f"{int(h*100)}%", font="Arial", color=WHITE).scale(0.5).next_to(bar, UP, buff=0.1)
            bars.add(bar)
            labels.add(label)

        # Arrow between words
        arrows = VGroup(*[
            Arrow(word_mobs[i].get_right(), word_mobs[i+1].get_left(), buff=0.1, stroke_width=2, color=WHITE)
            for i in range(len(word_mobs)-1)
        ])

        # Right title
        lm_title = Text("Language Model", font="Arial", weight=BOLD, color=GREEN).scale(0.8).next_to(right_rect, UP, buff=0.2)

        # Shared bottom label
        shared_label = Text("modeling reality", font="Arial", weight=BOLD, color=WHITE).scale(0.9).to_edge(DOWN, buff=0.5)

        # Animation
        self.play(
            Create(left_rect),
            Create(right_rect),
            Write(physics_title),
            Write(lm_title),
            run_time=1
        )
        self.wait(0.5)

        # Left: draw axes & equation
        self.play(
            Create(axes_left),
            Write(eq_label),
            run_time=1.5
        )
        self.wait(0.5)

        # Left: animate trajectory dots one by one along path
        for dot in trajectory_dots:
            self.play(FadeIn(dot), run_time=0.2)
        self.play(Create(trajectory_path), run_time=1.5)
        self.wait(0.5)

        # Right: show words and arrows
        self.play(
            Write(word_mobs),
            Create(arrows),
            run_time=1.5
        )
        self.wait(0.5)

        # Right: grow bars with labels
        for bar, label in zip(bars, labels):
            self.play(
                DrawBorderThenFill(bar),
                FadeIn(label),
                run_time=0.8
            )
        self.wait(0.5)

        # Shared label
        self.play(FadeIn(shared_label), run_time=1)
        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *

class ParametersLabel(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Gear icon (simplified 3D cartoon-style using layered circles and rectangles)
        gear = VGroup()
        outer_circle = Circle(radius=0.6, color=YELLOW, fill_opacity=0.8).set_stroke(YELLOW_E, width=2)
        inner_circle = Circle(radius=0.2, color=YELLOW_D, fill_opacity=1)
        teeth = VGroup()
        for i in range(8):
            angle = i * TAU / 8
            tooth = Rectangle(width=0.2, height=0.3, fill_color=YELLOW, fill_opacity=0.9, stroke_width=1.5).rotate(angle)
            tooth.move_to(outer_circle.get_center() + rotate_vector(RIGHT * 0.45, angle))
            teeth.add(tooth)
        gear.add(outer_circle, inner_circle, teeth)
        gear.scale(0.7)

        # "Parameters" text
        params_text = Text("Parameters", font="Comic Sans MS", weight=BOLD, color=WHITE, font_size=48)
        params_text.next_to(gear, RIGHT, buff=0.5)

        # Group label + gear
        label_group = VGroup(gear, params_text).move_to(ORIGIN).shift(UP * 1.5)

        # Numeric scale: "1B → 10B → 100B → 1T"
        scale_texts = [
            Text("1B", font="Comic Sans MS", weight=BOLD, color=BLUE_A, font_size=36),
            Text("10B", font="Comic Sans MS", weight=BOLD, color=TEAL_A, font_size=36),
            Text("100B", font="Comic Sans MS", weight=BOLD, color=GREEN_A, font_size=36),
            Text("1T", font="Comic Sans MS", weight=BOLD, color=PURPLE_A, font_size=36),
        ]
        arrows = VGroup()
        scale_group = VGroup()
        for i, txt in enumerate(scale_texts):
            if i == 0:
                txt.move_to(DOWN * 1.0)
            else:
                prev = scale_texts[i-1]
                txt.next_to(prev, RIGHT, buff=1.2)
                # Glowing arrow
                arrow = Arrow(
                    prev.get_right(),
                    txt.get_left(),
                    stroke_width=6,
                    color=GREY_A,
                    max_tip_length_to_length_ratio=0.15,
                    buff=0.1
                )
                arrow.set_stroke(opacity=0.9)
                # Glow effect via multiple copies with increasing size & decreasing opacity
                glow_arrows = VGroup()
                for j in range(3, 0, -1):
                    a = arrow.copy().scale(1 + 0.3*j).set_stroke(opacity=0.25/j, color=arrow.get_color()).set_z_index(-j)
                    glow_arrows.add(a)
                arrows.add(glow_arrows)
                arrows.add(arrow)
            scale_group.add(txt)

        # Assemble full scale line
        scale_group.move_to(DOWN * 1.0)

        # Add all to scene
        self.play(
            FadeIn(label_group, shift=UP * 0.5, scale=0.8),
            run_time=1.5,
            rate_func=rate_functions.ease_out_back
        )
        self.wait(0.5)

        self.play(
            LaggedStart(
                *[Write(t, stroke_color=t.get_color()) for t in scale_texts],
                lag_ratio=0.4
            ),
            run_time=2
        )
        self.play(
            Create(arrows, run_time=2.5, rate_func=rate_functions.smooth)
        )

        # Subtle float animation
        self.play(
            label_group.animate.shift(UP * 0.05).scale(1.01),
            scale_group.animate.shift(DOWN * 0.03).scale(0.995),
            run_time=2,
            rate_func=rate_functions.there_and_back_with_pause
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
import random

class ScaleComparison(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BLACK

        # Create stylized brain icon (simplified 2D cartoon-style, since true 3D icons aren't supported without assets)
        brain = VGroup()
        # Main brain shape — rounded lobes
        left_lobe = Circle(radius=0.8, color=BLUE_E, fill_opacity=0.7).shift(LEFT * 0.6)
        right_lobe = Circle(radius=0.8, color=BLUE_E, fill_opacity=0.7).shift(RIGHT * 0.6)
        center_lobe = Circle(radius=0.5, color=BLUE_D, fill_opacity=0.8).move_to(ORIGIN)
        brain.add(left_lobe, right_lobe, center_lobe)
        # Add simple folds (cartoon style)
        fold1 = ArcBetweenPoints(LEFT*0.4 + UP*0.2, RIGHT*0.4 + UP*0.2, radius=2, color=BLUE_B, stroke_width=2)
        fold2 = ArcBetweenPoints(LEFT*0.3 + DOWN*0.2, RIGHT*0.3 + DOWN*0.2, radius=-2, color=BLUE_B, stroke_width=2)
        brain.add(fold1, fold2)

        # Create neuron network icon: interconnected nodes
        network = VGroup()
        nodes = [
            Dot(point=[-2, 0.5, 0], color=YELLOW, radius=0.15),
            Dot(point=[-1, 1.2, 0], color=YELLOW, radius=0.15),
            Dot(point=[0, 0.8, 0], color=YELLOW, radius=0.15),
            Dot(point=[1, 1.3, 0], color=YELLOW, radius=0.15),
            Dot(point=[2, 0.4, 0], color=YELLOW, radius=0.15),
            Dot(point=[-0.5, -0.8, 0], color=YELLOW, radius=0.15),
            Dot(point=[0.5, -1.0, 0], color=YELLOW, radius=0.15),
        ]
        edges = [
            Line(nodes[0].get_center(), nodes[1].get_center(), color=TEAL_A, stroke_width=1.5),
            Line(nodes[1].get_center(), nodes[2].get_center(), color=TEAL_A, stroke_width=1.5),
            Line(nodes[2].get_center(), nodes[3].get_center(), color=TEAL_A, stroke_width=1.5),
            Line(nodes[3].get_center(), nodes[4].get_center(), color=TEAL_A, stroke_width=1.5),
            Line(nodes[2].get_center(), nodes[5].get_center(), color=TEAL_A, stroke_width=1.5),
            Line(nodes[5].get_center(), nodes[6].get_center(), color=TEAL_A, stroke_width=1.5),
            Line(nodes[6].get_center(), nodes[2].get_center(), color=TEAL_A, stroke_width=1.5),
        ]
        network.add(*nodes, *edges)

        # Position side by side
        brain.move_to(LEFT * 3.5)
        network.move_to(RIGHT * 3.5)

        # Labels
        label_text = Text("100B+ connections", font="Arial", weight=BOLD, color=WHITE, font_size=24)
        brain_label = label_text.copy().next_to(brain, DOWN, buff=0.5)
        network_label = label_text.copy().next_to(network, DOWN, buff=0.5)

        # Sparkles: small rotating stars around each icon
        def make_sparkle(center, size=0.1, color= YELLOW):
            sparkle = Star(n_points=5, outer_radius=size, inner_radius=size*0.3, color=color, fill_opacity=0.9)
            sparkle.move_to(center)
            return sparkle

        sparkles_brain = VGroup(*[
            make_sparkle(brain.get_corner(UL) + random.uniform(-0.3, 0.3) * RIGHT + random.uniform(-0.3, 0.3) * DOWN)
            for _ in range(6)
        ])
        sparkles_network = VGroup(*[
            make_sparkle(network.get_corner(UR) + random.uniform(-0.3, 0.3) * LEFT + random.uniform(-0.3, 0.3) * DOWN)
            for _ in range(6)
        ])

        # Animate
        self.play(
            FadeIn(brain, scale=0.8), 
            FadeIn(network, scale=0.8),
            run_time=1.5
        )
        self.wait(0.5)
        
        self.play(
            FadeIn(sparkles_brain, shift=UP * 0.2, scale=1.5),
            FadeIn(sparkles_network, shift=UP * 0.2, scale=1.5),
            run_time=1.2
        )
        self.wait(0.5)

        # Zoom effect: scale up both icons and labels slightly, with gentle pulse
        self.play(
            brain.animate.scale(1.15).set_color(BLUE_C),
            network.animate.scale(1.15).set_color(YELLOW_C),
            brain_label.animate.scale(1.1),
            network_label.animate.scale(1.1),
            sparkles_brain.animate.scale(1.2),
            sparkles_network.animate.scale(1.2),
            rate_func=rate_functions.there_and_back,
            run_time=2
        )

        # Final reveal of labels
        self.play(
            Write(brain_label),
            Write(network_label),
            run_time=1.2
        )
        self.wait(1.5)


# ==================== Auto-Generated ====================
from manim import *

class TextOnlyBoundary(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Create cartoon-style signboard (3D-like with depth via shading)
        sign_width, sign_height = 8, 5
        sign = RoundedRectangle(
            width=sign_width,
            height=sign_height,
            corner_radius=0.5,
            fill_color="#2c3e50",
            fill_opacity=1,
            stroke_color="#3498db",
            stroke_width=6,
        )
        sign.set_z_index(0)

        # Add subtle 3D effect: light top edge and dark bottom edge
        highlight = RoundedRectangle(
            width=sign_width - 0.4,
            height=0.6,
            corner_radius=0.2,
            fill_color=WHITE,
            fill_opacity=0.2,
            stroke_width=0,
        ).next_to(sign.get_top(), DOWN, buff=0)
        highlight.align_to(sign, LEFT).shift(RIGHT * 0.4)
        shadow = RoundedRectangle(
            width=sign_width - 0.4,
            height=0.8,
            corner_radius=0.2,
            fill_color=BLACK,
            fill_opacity=0.3,
            stroke_width=0,
        ).next_to(sign.get_bottom(), UP, buff=0)
        shadow.align_to(sign, RIGHT).shift(LEFT * 0.4)

        # Camera icon (cartoon-style, simplified)
        camera_body = Circle(radius=0.6, color=WHITE, fill_opacity=1, fill_color=GREY_A)
        lens = Circle(radius=0.3, color=WHITE, fill_opacity=1, fill_color=GREY_C)
        viewfinder = Rectangle(width=0.2, height=0.4, color=WHITE, fill_opacity=1, fill_color=GREY_E).rotate(PI/6)
        camera = VGroup(camera_body, lens, viewfinder).scale(0.8)
        camera.move_to(LEFT * 2.5 + UP * 0.8)

        # Speaker icon (cartoon-style)
        speaker_base = Rectangle(width=0.3, height=0.8, color=WHITE, fill_opacity=1, fill_color=GREY_A)
        speaker_cone = Triangle().scale(0.4).set_fill(GREY_C, 1).set_stroke(width=0)
        speaker_cone.rotate(-PI/2).next_to(speaker_base, RIGHT, buff=0)
        speaker = VGroup(speaker_base, speaker_cone).scale(0.8)
        speaker.move_to(RIGHT * 2.5 + UP * 0.8)

        # Cross-out line (diagonal red slash)
        cross_line = Line(
            start=sign.get_corner(UL) + UR * 0.5,
            end=sign.get_corner(DR) - UR * 0.5,
            stroke_color=RED,
            stroke_width=12,
            stroke_opacity=0.9,
        )

        # Central glowing 'ABC' stream — animated vertical text flow
        abc_texts = VGroup()
        for i in range(7):
            t = Text("ABC", font="Arial", weight=BOLD, color=WHITE, font_size=36)
            t.move_to(UP * (2.5 - i * 1.2))
            # Add glow effect via multiple copies with fading opacity/radius
            glow = t.copy().set_color(YELLOW).set_opacity(0.3).scale(1.15)
            glow2 = t.copy().set_color(ORANGE).set_opacity(0.15).scale(1.3)
            abc_texts.add(VGroup(t, glow, glow2))
        abc_texts.arrange(DOWN, buff=0.1).move_to(ORIGIN)

        # Animate entrance
        self.play(
            Create(sign),
            FadeIn(highlight),
            FadeIn(shadow),
            run_time=1.2,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.wait(0.3)
        self.play(
            FadeIn(camera),
            FadeIn(speaker),
            run_time=1.0,
        )
        self.wait(0.3)
        self.play(
            Create(cross_line),
            run_time=1.0,
            rate_func=rate_functions.ease_out_sine,
        )
        self.wait(0.5)
        self.play(
            LaggedStart(
                *[FadeIn(t, shift=DOWN * 0.5, scale=0.8) for t in abc_texts],
                lag_ratio=0.15,
                run_time=2.5,
            ),
            rate_func=rate_functions.smooth,
        )

        # Gentle upward float + pulse glow for ABC
        self.play(
            abc_texts.animate.shift(UP * 0.05).scale(1.01),
            rate_func=rate_functions.there_and_back_with_pause,
            run_time=3.0,
        )

        self.wait(1.5)


# ==================== Auto-Generated ====================
from manim import *

class MultimodalFusion(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Icons (simplified cartoon-style using geometric shapes + labels)
        text_icon = VGroup(
            Rectangle(height=1.2, width=1.0, fill_color=BLUE, fill_opacity=0.8, stroke_color=WHITE, stroke_width=2),
            Text("T", font_size=32, color=WHITE, weight=BOLD).move_to(UP * 0.1),
            Text("ext", font_size=20, color=WHITE).move_to(DOWN * 0.4)
        ).shift(LEFT * 4)

        image_icon = VGroup(
            Rectangle(height=1.2, width=1.0, fill_color=GREEN, fill_opacity=0.8, stroke_color=WHITE, stroke_width=2),
            Circle(radius=0.2, color=YELLOW, fill_opacity=0.7).move_to(UP * 0.3),
            Text("Img", font_size=20, color=WHITE).move_to(DOWN * 0.4)
        ).shift(RIGHT * 4)

        # Center badge
        badge = VGroup(
            RoundedRectangle(corner_radius=0.3, height=1.6, width=3.0, fill_color=PURPLE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=2.5),
            Text("Multimodal", font_size=30, color=WHITE, weight=BOLD),
            Text("Fusion", font_size=24, color=WHITE)
        ).arrange(DOWN, buff=0.2).move_to(ORIGIN)

        # '+' symbol in center
        plus = Text("+", font_size=64, color=YELLOW, weight=BOLD).move_to(ORIGIN)

        # Glow lines (curved, animated)
        line_left = Line(text_icon.get_right(), badge.get_left(), stroke_width=4, color=BLUE).set_opacity(0.7)
        line_right = Line(image_icon.get_left(), badge.get_right(), stroke_width=4, color=GREEN).set_opacity(0.7)

        # Add subtle glow effect via multiple copies with fading opacity
        glow_lines = VGroup()
        for i in range(3):
            alpha = 0.4 - i * 0.15
            offset = i * 0.1
            glow_line_l = line_left.copy().set_opacity(alpha).shift(DOWN * offset + LEFT * offset)
            glow_line_r = line_right.copy().set_opacity(alpha).shift(DOWN * offset + RIGHT * offset)
            glow_lines.add(glow_line_l, glow_line_r)

        # Animate
        self.play(
            FadeIn(text_icon, shift=LEFT),
            FadeIn(image_icon, shift=RIGHT),
            run_time=1.2
        )
        self.wait(0.5)

        self.play(
            Create(line_left, rate_func=rate_functions.ease_in_out_sine),
            Create(line_right, rate_func=rate_functions.ease_in_out_sine),
            FadeIn(glow_lines, run_time=1.5),
            run_time=1.5
        )

        self.play(
            FadeIn(badge, scale=0.8, rate_func=rate_functions.ease_out_back),
            Write(plus, rate_func=rate_functions.there_and_back_with_pause),
            run_time=1.8
        )
        self.wait(1)

        # Subtle pulse on badge and '+' to emphasize fusion
        self.play(
            badge.animate.scale(1.05).set_fill(opacity=1.0),
            plus.animate.scale(1.1).set_color(GOLD),
            rate_func=rate_functions.there_and_back,
            run_time=1.2
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
import numpy as np

class VisionArchitectureEvolution(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Title
        title = Text("Vision Architecture Evolution", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Split screen: left (CNN), right (Transformer)
        divider = Line(UP * 3, DOWN * 3, stroke_width=2, color=GRAY)
        divider.move_to(ORIGIN)
        
        cnn_label = Text("CNN Pipeline", font_size=24, color=BLUE).to_corner(UL, buff=0.3)
        cnn_label.shift(RIGHT * 2.5)
        trans_label = Text("Transformer Attention", font_size=24, color=GREEN).to_corner(UR, buff=0.3)
        trans_label.shift(LEFT * 2.5)

        self.play(
            Write(cnn_label),
            Write(trans_label),
            Create(divider)
        )
        self.wait(0.5)

        # === LEFT SIDE: CNN ===
        # Input image placeholder (grayscale cat-like patch)
        input_grid = VGroup()
        for i in range(5):
            for j in range(5):
                cell = Square(side_length=0.4, fill_opacity=0.7, fill_color=GREY_A if (i+j) % 2 == 0 else GREY_C)
                cell.move_to(LEFT * 4 + RIGHT * j * 0.4 + DOWN * i * 0.4)
                input_grid.add(cell)
        input_label = Text("Input", font_size=16).next_to(input_grid, UP, buff=0.2)

        # Kernel (3x3)
        kernel = VGroup()
        for i in range(3):
            for j in range(3):
                kcell = Square(side_length=0.3, fill_opacity=0.9, fill_color=RED)
                kcell.move_to(LEFT * 4 + RIGHT * (j + 0.5) * 0.4 + DOWN * (i + 0.5) * 0.4)
                kernel.add(kcell)
        kernel_label = Text("3×3 Kernel", font_size=14, color=RED).next_to(kernel, UP, buff=0.1)

        # Edge map (output)
        edge_map = VGroup()
        for i in range(3):
            for j in range(3):
                ecell = Square(side_length=0.4, fill_opacity=0.8, fill_color=BLUE if (i==0 and j==1) or (i==1 and j==0) or (i==1 and j==2) or (i==2 and j==1) else DARK_GREY)
                ecell.move_to(LEFT * 1.5 + RIGHT * j * 0.4 + DOWN * i * 0.4)
                edge_map.add(ecell)
        edge_label = Text("Edge Map", font_size=16, color=BLUE).next_to(edge_map, UP, buff=0.2)

        # Shape map (simplified contour)
        shape_map = VGroup()
        for i in range(3):
            for j in range(3):
                scell = Square(side_length=0.4, fill_opacity=0.8, fill_color=TEAL if (i==1 and j==1) else DARK_GREY)
                scell.move_to(LEFT * 1.5 + RIGHT * j * 0.4 + DOWN * i * 0.4)
                shape_map.add(scell)
        shape_label = Text("Shape", font_size=16, color=TEAL).next_to(shape_map, UP, buff=0.2)

        # Object map (highlighted center)
        object_map = VGroup()
        for i in range(3):
            for j in range(3):
                ocell = Square(side_length=0.4, fill_opacity=0.8, fill_color=YELLOW if (i==1 and j==1) else DARK_GREY)
                ocell.move_to(LEFT * 1.5 + RIGHT * j * 0.4 + DOWN * i * 0.4)
                object_map.add(ocell)
        object_label = Text("Object", font_size=16, color=YELLOW).next_to(object_map, UP, buff=0.2)

        # Arrows for CNN flow
        cnn_arrow1 = Arrow(input_grid.get_right(), edge_map.get_left(), buff=0.2, stroke_width=2, color=BLUE)
        cnn_arrow2 = Arrow(edge_map.get_right(), shape_map.get_left(), buff=0.2, stroke_width=2, color=TEAL)
        cnn_arrow3 = Arrow(shape_map.get_right(), object_map.get_left(), buff=0.2, stroke_width=2, color=YELLOW)

        # === RIGHT SIDE: TRANSFORMER ===
        # Input patch grid (same size as left input)
        trans_input = VGroup()
        for i in range(5):
            for j in range(5):
                tcell = Square(side_length=0.4, fill_opacity=0.7, fill_color=GREY_A if (i+j) % 2 == 0 else GREY_C)
                tcell.move_to(RIGHT * 4 + RIGHT * j * 0.4 + DOWN * i * 0.4)
                trans_input.add(tcell)
        trans_input_label = Text("Input Patches", font_size=16).next_to(trans_input, UP, buff=0.2)

        # Attention heatmap — initial (ears focus)
        attn_ears = VGroup()
        for i in range(5):
            for j in range(5):
                # Simulate attention: high on top corners (cat ears)
                intensity = 0.2 + 0.6 * (1 if (i==0 and (j==1 or j==3)) else 0)
                acell = Square(side_length=0.4, fill_opacity=intensity, fill_color=GREEN)
                acell.move_to(RIGHT * 4 + RIGHT * j * 0.4 + DOWN * i * 0.4)
                attn_ears.add(acell)
        attn_ears_label = Text("Focus: Ears", font_size=16, color=GREEN).next_to(attn_ears, UP, buff=0.2)

        # Attention heatmap — later (whole cat)
        attn_cat = VGroup()
        for i in range(5):
            for j in range(5):
                # High on central region (cat head/body)
                intensity = 0.2 + 0.6 * (1 if (i in [0,1,2] and j in [1,2,3]) else 0)
                acell = Square(side_length=0.4, fill_opacity=intensity, fill_color=GREEN_E)
                acell.move_to(RIGHT * 4 + RIGHT * j * 0.4 + DOWN * i * 0.4)
                attn_cat.add(acell)
        attn_cat_label = Text("Focus: Whole Cat", font_size=16, color=GREEN_E).next_to(attn_cat, UP, buff=0.2)

        # Arrows for Transformer flow
        trans_arrow1 = Arrow(trans_input.get_right(), attn_ears.get_left(), buff=0.2, stroke_width=2, color=GREEN)
        trans_arrow2 = Arrow(attn_ears.get_right(), attn_cat.get_left(), buff=0.2, stroke_width=2, color=GREEN_E)

        # Layer labels
        cnn_layers = VGroup(
            Text("Conv", font_size=14, color=BLUE).next_to(input_grid, DOWN, buff=0.3),
            Text("ReLU", font_size=14, color=BLUE).next_to(edge_map, DOWN, buff=0.3),
            Text("Pool", font_size=14, color=TEAL).next_to(shape_map, DOWN, buff=0.3),
            Text("FC", font_size=14, color=YELLOW).next_to(object_map, DOWN, buff=0.3),
        )
        trans_layers = VGroup(
            Text("Embed", font_size=14, color=GREEN).next_to(trans_input, DOWN, buff=0.3),
            Text("QKV", font_size=14, color=GREEN).next_to(attn_ears, DOWN, buff=0.3),
            Text("Softmax", font_size=14, color=GREEN_E).next_to(attn_cat, DOWN, buff=0.3),
        )

        # Animate left side first
        self.play(
            FadeIn(input_grid), Write(input_label),
            FadeIn(kernel), Write(kernel_label),
        )
        self.wait(0.5)

        # Slide kernel and reveal edge map
        self.play(
            kernel.animate.shift(RIGHT * 2.5),
            run_time=1.5,
            rate_func=rate_functions.smooth
        )
        self.play(
            FadeIn(edge_map), Write(edge_label),
            FadeOut(kernel), FadeOut(kernel_label),
        )
        self.play(Write(cnn_layers[0]))
        self.wait(0.5)

        # Edge → Shape
        self.play(
            Transform(edge_map, shape_map),
            Transform(edge_label, shape_label),
            Write(cnn_layers[1]),
            Create(cnn_arrow1)
        )
        self.wait(0.5)

        # Shape → Object
        self.play(
            Transform(shape_map, object_map),
            Transform(shape_label, object_label),
            Write(cnn_layers[2]),
            Create(cnn_arrow2)
        )
        self.wait(0.5)

        # Final object layer
        self.play(
            Write(cnn_layers[3]),
            Create(cnn_arrow3)
        )
        self.wait(0.5)

        # === Right side animation ===
        self.play(
            FadeIn(trans_input), Write(trans_input_label),
        )
        self.wait(0.5)

        # First attention (ears)
        self.play(
            FadeIn(attn_ears), Write(attn_ears_label),
            Write(trans_layers[0]),
            Create(trans_arrow1)
        )
        self.wait(0.5)

        # Transition to full cat attention
        self.play(
            Transform(attn_ears, attn_cat),
            Transform(attn_ears_label, attn_cat_label),
            Write(trans_layers[1]),
            Create(trans_arrow2)
        )
        self.wait(0.5)

        # Final softmax layer
        self.play(
            Write(trans_layers[2])
        )
        self.wait(1.0)

        # Highlight both final outputs
        final_cnn = object_map.copy().set_stroke(YELLOW, width=3).set_fill(opacity=0)
        final_trans = attn_cat.copy().set_stroke(GREEN_E, width=3).set_fill(opacity=0)
        self.play(
            Create(final_cnn),
            Create(final_trans),
            run_time=1.2
        )
        self.wait(1.0)

        # Fade out all except labels
        self.play(
            FadeOut(VGroup(
                input_grid, input_label,
                edge_map, edge_label,
                shape_map, shape_label,
                object_map, object_label,
                trans_input, trans_input_label,
                attn_ears, attn_ears_label,
                attn_cat, attn_cat_label,
                cnn_arrow1, cnn_arrow2, cnn_arrow3,
                trans_arrow1, trans_arrow2,
                cnn_layers, trans_layers,
                final_cnn, final_trans,
                divider
            )),
            FadeOut(title),
            FadeOut(cnn_label),
            FadeOut(trans_label),
        )

        # Summary text
        summary = VGroup(
            Text("CNN: Local, Hierarchical, Fixed Receptive Field", font_size=24, color=BLUE),
            Text("Transformer: Global, Adaptive, Context-Aware Attention", font_size=24, color=GREEN),
        ).arrange(DOWN, buff=0.8).move_to(ORIGIN)
        self.play(Write(summary[0]))
        self.wait(0.8)
        self.play(Write(summary[1]))
        self.wait(2.0)


# ==================== Auto-Generated ====================
from manim import *
from manim.utils.rate_functions import ease_in_out_sine

class CvNlpDualRole(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Split screen: left (NLP) and right (CV)
        divider = Line(UP * 3.5, DOWN * 3.5, stroke_width=2, color=GRAY)
        self.add(divider)

        # --- LEFT SIDE: NLP / Speech → LLM Brain ---
        # Speech bubbles (stacked, slightly offset) - using built-in shapes
        def create_speech_bubble():
            # Create speech bubble using RoundedRectangle + Triangle
            bubble_body = RoundedRectangle(
                width=1.8, height=0.8, corner_radius=0.2,
                fill_color=WHITE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1
            )
            bubble_tail = Triangle(fill_color=WHITE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1)
            bubble_tail.scale(0.15).rotate(-PI/2).next_to(bubble_body, DOWN, buff=-0.05).shift(LEFT * 0.5)
            return VGroup(bubble_body, bubble_tail).scale(0.5)

        bubble1 = create_speech_bubble()
        bubble2 = create_speech_bubble().shift(DOWN * 0.8)
        bubble3 = create_speech_bubble().shift(DOWN * 1.6)
        speech_bubbles = VGroup(bubble1, bubble2, bubble3).to_edge(LEFT, buff=0.5).shift(UP * 0.5)

        # Text inside bubbles (simplified Chinese + English mix for clarity)
        text1 = Text("你好！", font="Microsoft YaHei", font_size=20, color=BLACK).move_to(bubble1.get_center())
        text2 = Text("What is AI?", font_size=20, color=BLACK).move_to(bubble2.get_center())
        text3 = Text("Explain like I'm five.", font_size=18, color=BLACK).move_to(bubble3.get_center())

        # LLM brain icon (stylized, abstract brain with neural glow) - using built-in shapes
        # Create a stylized brain using ellipses and curves
        brain_left = Ellipse(width=0.6, height=0.8, fill_color=BLUE_E, fill_opacity=0.8, stroke_color=BLUE_C, stroke_width=1.5)
        brain_right = Ellipse(width=0.6, height=0.8, fill_color=BLUE_E, fill_opacity=0.8, stroke_color=BLUE_C, stroke_width=1.5)
        brain_left.shift(LEFT * 0.2)
        brain_right.shift(RIGHT * 0.2)
        # Add some wavy lines to represent brain folds
        brain_fold1 = Arc(radius=0.3, angle=PI, stroke_color=BLUE_C, stroke_width=1).shift(UP * 0.1)
        brain_fold2 = Arc(radius=0.25, angle=PI, stroke_color=BLUE_C, stroke_width=1).shift(DOWN * 0.1).rotate(PI)
        brain = VGroup(brain_left, brain_right, brain_fold1, brain_fold2).scale(0.7)
        brain_icon = brain.to_edge(RIGHT, buff=1.2).shift(UP * 0.5)

        # Glow effect for brain (pulsing)
        brain_glow = Circle(radius=0.9, color=BLUE_A, fill_opacity=0.3).move_to(brain_icon.get_center())
        brain_glow.set_z_index(-1)

        # --- RIGHT SIDE: CV / Camera → Eye Icon ---
        # Camera lens (circle with inner ring)
        lens_outer = Circle(radius=0.6, color=WHITE, stroke_width=2)
        lens_inner = Circle(radius=0.3, color=WHITE, stroke_width=1.5)
        camera = VGroup(lens_outer, lens_inner).to_edge(RIGHT, buff=1.2).shift(DOWN * 1.5)

        # Photo placeholder (simple grid + face outline)
        photo_frame = RoundedRectangle(height=1.2, width=1.6, corner_radius=0.1, stroke_color=GRAY, stroke_width=1)
        photo_grid = VGroup(*[
            Line(LEFT * 0.7 + UP * (0.5 - i * 0.25), RIGHT * 0.7 + UP * (0.5 - i * 0.25), stroke_width=0.5, color=GREY_D)
            for i in range(5)
        ] + [
            Line(LEFT * 0.7 + UP * 0.5 + DOWN * i * 0.25, LEFT * 0.7 + UP * 0.5 + DOWN * i * 0.25 + RIGHT * 1.4, stroke_width=0.5, color=GREY_D)
            for i in range(5)
        ])
        face_outline = Circle(radius=0.25, color=RED, stroke_width=1.2).move_to(photo_frame.get_center())
        photo = VGroup(photo_frame, photo_grid, face_outline).move_to(camera.get_center() + DOWN * 1.2)

        # Feature dots (abstract image features)
        features = VGroup(*[
            Dot(radius=0.05, color=YELLOW).move_to(
                photo.get_center() + np.array([np.cos(theta), np.sin(theta), 0]) * 0.3
            )
            for theta in np.linspace(0, TAU, 8, endpoint=False)
        ]).scale(0.8)

        # Eye icon (simple stylized eye)
        eye_white = Circle(radius=0.4, color=WHITE, fill_opacity=1, stroke_width=1)
        eye_iris = Circle(radius=0.2, color=BLUE_D, fill_opacity=1)
        eye_pupil = Circle(radius=0.08, color=BLACK, fill_opacity=1)
        eye_icon = VGroup(eye_white, eye_iris, eye_pupil).to_edge(LEFT, buff=1.2).shift(DOWN * 1.5)

        # Glow for eye (pulsing sync with brain)
        eye_glow = Circle(radius=0.5, color=BLUE_A, fill_opacity=0.3).move_to(eye_icon.get_center())
        eye_glow.set_z_index(-1)

        # --- ANIMATION ---
        # Initial state
        self.add(speech_bubbles, text1, text2, text3, brain_icon, brain_glow, camera, photo, eye_icon, eye_glow)

        # Animate text flowing into brain (one by one, with fade)
        self.play(
            FadeIn(text1, shift=RIGHT * 0.3, rate_func=ease_in_out_sine),
            run_time=0.8
        )
        self.wait(0.3)
        self.play(
            FadeIn(text2, shift=RIGHT * 0.3, rate_func=ease_in_out_sine),
            run_time=0.8
        )
        self.wait(0.3)
        self.play(
            FadeIn(text3, shift=RIGHT * 0.3, rate_func=ease_in_out_sine),
            run_time=0.8
        )
        self.wait(0.5)

        # Simultaneous pulse & flow:
        # — Brain glows brighter
        # — Camera focuses (lens shrinks slightly + photo zooms in)
        # — Features appear and connect to eye
        self.play(
            brain_glow.animate.scale(1.3).set_opacity(0.6),
            eye_glow.animate.scale(1.3).set_opacity(0.6),
            camera.animate.scale(0.95).shift(UP * 0.1),
            photo.animate.scale(1.15).shift(UP * 0.15),
            run_time=1.2,
            rate_func=ease_in_out_sine
        )

        # Reveal features
        self.play(FadeIn(features, scale=0.5, lag_ratio=0.1), run_time=1.0)

        # Features fly toward eye icon
        feature_arcs = [
            ArcBetweenPoints(
                f.get_center(),
                eye_icon.get_center() + 0.2 * (f.get_center() - eye_icon.get_center()),
                angle=-PI/4,
                stroke_color=YELLOW,
                stroke_width=1.5
            ) for f in features
        ]
        self.play(
            *[Create(arc, run_time=1.0, rate_func=ease_in_out_sine) for arc in feature_arcs],
            run_time=1.0
        )

        # Final synchronized pulse: brain and eye glow brighten and contract
        self.play(
            brain_glow.animate.scale(0.8).set_opacity(0.8),
            eye_glow.animate.scale(0.8).set_opacity(0.8),
            run_time=1.0,
            rate_func=ease_in_out_sine
        )
        self.wait(0.5)

        # Optional: subtle sustained pulse (2 cycles)
        self.play(
            brain_glow.animate.scale(1.1).set_opacity(0.6),
            eye_glow.animate.scale(1.1).set_opacity(0.6),
            run_time=1.0,
            rate_func=ease_in_out_sine
        )
        self.play(
            brain_glow.animate.scale(0.9).set_opacity(0.7),
            eye_glow.animate.scale(0.9).set_opacity(0.7),
            run_time=1.0,
            rate_func=ease_in_out_sine
        )
        self.wait(0.5)


# ==================== Auto-Generated ====================
from manim import *
import numpy as np

class CrossModalLink(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Photo box (left)
        photo_box = RoundedRectangle(
            corner_radius=0.2,
            width=4.0,
            height=3.0,
            color=GREY_A,
            stroke_width=2,
            fill_opacity=0.1
        )
        photo_label = Text("Photo", font_size=24, color=GREY_C).next_to(photo_box, UP, buff=0.2)
        photo_group = VGroup(photo_box, photo_label).shift(LEFT * 4)

        # Caption box (right)
        caption_box = RoundedRectangle(
            corner_radius=0.2,
            width=4.0,
            height=3.0,
            color=GREY_A,
            stroke_width=2,
            fill_opacity=0.1
        )
        caption_label = Text("Caption", font_size=24, color=GREY_C).next_to(caption_box, UP, buff=0.2)
        caption_group = VGroup(caption_box, caption_label).shift(RIGHT * 4)

        # Bidirectional arrow between boxes
        arrow = DoubleArrow(
            photo_box.get_right() + RIGHT * 0.2,
            caption_box.get_left() + LEFT * 0.2,
            stroke_width=6,
            color=BLUE_D,
            max_tip_length_to_length_ratio=0.1,
            tip_length=0.25
        )
        link_label = Text("semantic link", font_size=28, color=BLUE_A, weight=BOLD).next_to(arrow, UP, buff=0.3)

        # Animate pulse on arrow + label
        arrow.save_state()
        link_label.save_state()
        self.play(
            Create(photo_group),
            Create(caption_group),
            Create(arrow),
            Write(link_label),
            run_time=1.5
        )
        self.wait(0.5)

        # Pulse animation (scale + color shift)
        for _ in range(3):
            self.play(
                arrow.animate.scale(1.15).set_color(BLUE_B),
                link_label.animate.set_color(BLUE),
                rate_func=there_and_back,
                run_time=1.2
            )
            self.wait(0.3)

        # Morph sequence: photo → sketch → text → emoji → photo (loop)
        # Use simple stylized representations (no external images)
        # Photo: camera icon (simplified)
        photo_icon = VGroup(
            Circle(radius=0.8, color=WHITE, fill_opacity=0.1, stroke_width=2),
            Rectangle(width=1.2, height=0.8, color=WHITE, fill_opacity=0.1, stroke_width=2).move_to(ORIGIN),
            Circle(radius=0.15, color=RED, fill_opacity=1).move_to(UP * 0.3 + RIGHT * 0.2)
        ).scale(0.7).move_to(photo_box.get_center())

        # Sketch: hand-drawn style rectangle with wobbly lines
        sketch_lines = VGroup()
        # Approximate wobbly rectangle
        points = [
            [-0.8, -0.6, 0], [0.8, -0.6, 0], [0.8, 0.6, 0], [-0.8, 0.6, 0], [-0.8, -0.6, 0]
        ]
        for i in range(4):
            p1 = np.array(points[i])
            p2 = np.array(points[i+1])
            mid = (p1 + p2) / 2
            offset = rotate_vector(p2 - p1, PI/2) * 0.05 * np.random.uniform(-1, 1)
            sketch_lines.add(
                Line(p1, mid + offset, stroke_width=2, color=YELLOW_A),
                Line(mid + offset, p2, stroke_width=2, color=YELLOW_A)
            )
        sketch = sketch_lines.scale(0.7).move_to(photo_box.get_center())

        # Text: "scene" in bold
        text_repr = Text("scene", font_size=36, color=GREEN_A, weight=BOLD).move_to(photo_box.get_center())

        # Emoji: simple smiley (circle + arcs)
        emoji = VGroup(
            Circle(radius=0.6, color=ORANGE, fill_opacity=0.2, stroke_width=3),
            Arc(start_angle=PI/4, angle=PI*0.5, radius=0.3, color=RED, stroke_width=3).move_to(ORIGIN + DOWN*0.15),
            Dot(color=BLACK, radius=0.07).shift(UP*0.2 + LEFT*0.2),
            Dot(color=BLACK, radius=0.07).shift(UP*0.2 + RIGHT*0.2),
        ).scale(0.7).move_to(photo_box.get_center())

        # Sequence morphs (smooth transitions)
        morph_targets = [sketch, text_repr, emoji, photo_icon]
        current_morph = photo_icon.copy()
        self.play(FadeIn(current_morph), run_time=0.8)
        self.wait(0.5)

        for target in morph_targets:
            self.play(
                Transform(current_morph, target.copy()),
                run_time=1.4,
                rate_func=smooth
            )
            self.wait(0.6)

        # Final loop back to photo (already at photo_icon, but re-emphasize)
        self.play(
            current_morph.animate.scale(1.05).set_color(WHITE),
            rate_func=there_and_back,
            run_time=1.0
        )

        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
# Note: Colors are directly available from manim (e.g., RED, BLUE, etc.)

class LLMWithSenses(Scene):
    def construct(self):
        # Background
        self.camera.background_color = "#0f1a2b"

        # Lab-like grid floor (subtle)
        grid = NumberPlane(
            x_range=[-10, 10, 2],
            y_range=[-6, 6, 2],
            background_line_style={"stroke_color": "#1a2d45", "stroke_width": 1, "stroke_opacity": 0.3},
            axis_config={"stroke_opacity": 0},
        )
        grid.set_z_index(-1)

        # Brain using built-in shapes (ellipses to form brain-like shape)
        brain_left = Ellipse(width=1.0, height=1.4, fill_color=PURPLE_E, fill_opacity=0.8, stroke_color=PURPLE_A, stroke_width=0.5)
        brain_right = Ellipse(width=1.0, height=1.4, fill_color=PURPLE_E, fill_opacity=0.8, stroke_color=PURPLE_A, stroke_width=0.5)
        brain_left.shift(LEFT * 0.35)
        brain_right.shift(RIGHT * 0.35)
        brain_fold1 = Arc(radius=0.4, angle=PI, stroke_color=PURPLE_A, stroke_width=1).shift(UP * 0.2)
        brain_fold2 = Arc(radius=0.35, angle=PI, stroke_color=PURPLE_A, stroke_width=1).shift(DOWN * 0.2).rotate(PI)
        brain = VGroup(brain_left, brain_right, brain_fold1, brain_fold2).scale(1.2)

        # Glowing neural connections (curved lines around brain)
        connections = VGroup()
        np.random.seed(42)
        for i in range(12):
            angle1 = i * TAU / 12
            angle2 = (i + np.random.randint(3, 6)) * TAU / 12
            start = np.array([np.cos(angle1) * 0.8, np.sin(angle1) * 1.0, 0])
            end = np.array([np.cos(angle2) * 0.8, np.sin(angle2) * 1.0, 0])
            arc = ArcBetweenPoints(start, end, angle=np.random.uniform(-PI/4, PI/4))
            arc.set_stroke(color=TEAL_A, width=1.5, opacity=0.9)
            connections.add(arc)
        connections.set_z_index(1)

        # Eyes using built-in shapes (circles)
        def create_eye():
            eye_white = Circle(radius=0.3, fill_color=WHITE, fill_opacity=0.95, stroke_color=GREY_B, stroke_width=1)
            eye_iris = Circle(radius=0.15, fill_color=BLUE_D, fill_opacity=1, stroke_width=0)
            eye_pupil = Circle(radius=0.06, fill_color=BLACK, fill_opacity=1, stroke_width=0)
            return VGroup(eye_white, eye_iris, eye_pupil)

        left_eye = create_eye().shift(LEFT * 3.5 + UP * 1.2)
        right_eye = create_eye().shift(RIGHT * 3.5 + UP * 1.2)
        left_eye.set_z_index(2)
        right_eye.set_z_index(2)

        # Ears using built-in shapes (ellipse + arc)
        def create_ear():
            ear_outer = Ellipse(width=0.4, height=0.7, fill_color=GREY_C, fill_opacity=0.85, stroke_color=GREY_B, stroke_width=1)
            ear_inner = Arc(radius=0.2, angle=PI*0.8, stroke_color=GREY_B, stroke_width=1).rotate(-PI/4).shift(LEFT * 0.05)
            return VGroup(ear_outer, ear_inner)

        left_ear = create_ear().flip().shift(LEFT * 4.2 + DOWN * 0.5)
        right_ear = create_ear().shift(RIGHT * 4.2 + DOWN * 0.5)
        left_ear.set_z_index(2)
        right_ear.set_z_index(2)

        # Labels
        label = Text("LLM Brain", font="Arial", weight=BOLD, color=WHITE).scale(0.8)
        label.next_to(brain, DOWN, buff=0.8)

        # Add all elements
        self.add(grid)
        self.play(
            Create(brain, run_time=1.5),
            FadeIn(connections, run_time=1.5),
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(0.5)
        self.play(
            FadeIn(left_eye, right_eye, run_time=0.8),
            FadeIn(left_ear, right_ear, run_time=0.8),
            Write(label, run_time=1.2)
        )
        self.wait(2)

        # Subtle pulse glow effect on brain & connections
        self.play(
            brain.animate.set_fill(PURPLE_D, opacity=0.95),
            connections.animate.set_stroke(opacity=1.0),
            rate_func=rate_functions.there_and_back,
            run_time=2.5
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class HumanAIBridge(Scene):
    def construct(self):
        # Background
        bg = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=GREY_D,
            fill_opacity=1,
            stroke_width=0
        )
        self.add(bg)

        # Soft focus effect: large blurred circle behind content
        blur_circle = Circle(
            radius=12,
            fill_color=GREY_E,
            fill_opacity=0.7,
            stroke_width=0
        )
        blur_circle.move_to(ORIGIN)
        self.add(blur_circle)

        # Human figure (simplified stylized 3D cartoon)
        human_body = Rectangle(
            width=0.8, height=2.0,
            fill_color="#FFB6C1",
            fill_opacity=1,
            stroke_width=0
        )
        human_head = Circle(
            radius=0.6,
            fill_color="#FFDAB9",
            fill_opacity=1,
            stroke_width=0
        )
        human_head.move_to(human_body.get_top() + UP * 0.4)
        human_arms = VGroup(
            Line(ORIGIN, UP * 0.8, stroke_width=6, color="#FFB6C1").rotate(-PI/6).move_to(human_body.get_center() + LEFT * 0.4 + UP * 0.5),
            Line(ORIGIN, UP * 0.8, stroke_width=6, color="#FFB6C1").rotate(PI/6).move_to(human_body.get_center() + RIGHT * 0.4 + UP * 0.5),
        )
        human = VGroup(human_body, human_head, human_arms).move_to(LEFT * 4)

        # Speech bubble
        bubble = RoundedRectangle(
            width=3.0, height=1.6,
            corner_radius=0.4,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=2,
            stroke_color=BLUE_C
        )
        bubble_tip = Polygon(
            bubble.get_bottom() + DOWN * 0.2,
            bubble.get_bottom() + LEFT * 0.2 + DOWN * 0.2,
            bubble.get_bottom() + RIGHT * 0.2 + DOWN * 0.2,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=2,
            stroke_color=BLUE_C
        )
        speech_text = Text("Hello!", font_size=24, color=BLACK, weight=BOLD)
        speech_text.move_to(bubble.get_center())
        bubble_group = VGroup(bubble, bubble_tip, speech_text)
        bubble_group.next_to(human, RIGHT, buff=0.5)

        # AI robot figure
        robot_body = Rectangle(
            width=0.9, height=2.2,
            fill_color="#415A77",
            fill_opacity=1,
            stroke_width=0
        )
        robot_head = Square(
            side_length=0.8,
            fill_color="#778DA9",
            fill_opacity=1,
            stroke_width=0
        )
        robot_head.move_to(robot_body.get_top() + UP * 0.3)
        # Eyes
        eye_left = Circle(radius=0.12, fill_color=BLUE_A, fill_opacity=1).move_to(robot_head.get_center() + LEFT * 0.2 + UP * 0.1)
        eye_right = Circle(radius=0.12, fill_color=BLUE_A, fill_opacity=1).move_to(robot_head.get_center() + RIGHT * 0.2 + UP * 0.1)
        # Antenna
        antenna = Line(ORIGIN, UP * 0.6, stroke_width=2, color=YELLOW).move_to(robot_head.get_top() + UP * 0.1)
        antenna_dot = Circle(radius=0.07, fill_color=YELLOW, fill_opacity=1).move_to(antenna.get_end())
        robot = VGroup(robot_body, robot_head, eye_left, eye_right, antenna, antenna_dot).move_to(RIGHT * 4)

        # Text input box
        input_box = RoundedRectangle(
            width=3.2, height=0.8,
            corner_radius=0.2,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=2,
            stroke_color=TEAL_C
        )
        input_text = Text("type here...", font_size=20, color=GREY_A, italic=True)
        input_text.move_to(input_box.get_center())
        input_group = VGroup(input_box, input_text)
        input_group.next_to(robot, LEFT, buff=0.5)

        # Glowing bridge: flowing words along a curved path
        bridge_curve = ArcBetweenPoints(
            bubble.get_right(),
            input_box.get_left(),
            angle=-PI/4,
            stroke_width=6,
            stroke_color=BLUE_B,
            stroke_opacity=0.7
        )
        # Words to flow: "understand", "learn", "connect", "evolve", "collaborate"
        words = ["understand", "learn", "connect", "evolve", "collaborate"]
        word_mobs = VGroup()
        for i, word in enumerate(words):
            w = Text(word, font_size=22, color=WHITE, weight=MEDIUM)
            # Position along curve using parametric interpolation
            alpha = i / (len(words) - 1) if len(words) > 1 else 0.5
            point = bridge_curve.point_at_alpha(alpha)
            w.move_to(point + UP * 0.3)
            w.set_z_index(2)
            word_mobs.add(w)

        # Add glow effect to bridge and words
        bridge_glow = bridge_curve.copy().set_stroke(width=16, opacity=0.3, color=BLUE_A)
        bridge_glow.set_z_index(1)
        word_mobs.set_z_index(3)

        # Assemble scene
        self.play(
            FadeIn(human, shift=UP * 0.5, scale=0.9),
            FadeIn(robot, shift=UP * 0.5, scale=0.9),
            run_time=1.5,
            rate_func=rate_functions.smooth
        )
        self.wait(0.5)
        self.play(
            FadeIn(bubble_group, shift=RIGHT * 0.3),
            FadeIn(input_group, shift=LEFT * 0.3),
            run_time=1.2
        )
        self.wait(0.5)
        self.play(
            Create(bridge_glow),
            Create(bridge_curve),
            FadeIn(word_mobs, shift=UP * 0.2),
            run_time=2
        )
        self.wait(2)

        # Gentle pulse animation on bridge and words
        self.play(
            bridge_curve.animate.set_stroke(opacity=1),
            bridge_glow.animate.set_stroke(opacity=0.5),
            word_mobs.animate.set_opacity(1),
            rate_func=rate_functions.there_and_back,
            run_time=2
        )
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
import random

class ConfusedLLM(Scene):
    def construct(self):
        # Dim ambient background
        self.camera.background_color = "#1a1a2e"

        # Draw a stylized 3D-like AI brain (simplified cartoon version)
        brain = SVGMobject("brain").scale(2).set_color("#4cc9f0").set_stroke(width=1.5)
        # Since we can't rely on external SVG files, replace with a custom shape:
        # Approximate brain using two overlapping ellipses and organic curves
        left_lobe = Ellipse(width=2.0, height=2.8, color="#4cc9f0", fill_opacity=0.3).rotate(-0.2)
        right_lobe = Ellipse(width=2.0, height=2.8, color="#4cc9f0", fill_opacity=0.3).rotate(0.2)
        top_bulge = Circle(radius=0.7, color="#4cc9f0", fill_opacity=0.3).shift(UP * 1.2)
        brain_group = VGroup(left_lobe, right_lobe, top_bulge).move_to(ORIGIN)

        # Add subtle inner folds (lighter lines)
        fold1 = Arc(start_angle=PI/4, angle=-PI/2, radius=0.8, color="#4361ee", stroke_width=1).shift(UP*0.3 + LEFT*0.2)
        fold2 = Arc(start_angle=PI, angle=PI/3, radius=0.6, color="#4361ee", stroke_width=1).shift(DOWN*0.2 + RIGHT*0.3)
        brain_group.add(fold1, fold2)

        # Question marks swirling around (orbiting)
        question_marks = VGroup()
        swirl_radius = 3.0
        for i in range(8):
            angle = TAU * i / 8 + self.time
            x = swirl_radius * np.cos(angle)
            y = swirl_radius * np.sin(angle) * 0.6  # flatten orbit
            q = Text("?", font_size=36, color="#f72585", weight=BOLD).move_to([x, y, 0])
            q.rotate(angle + PI/2, about_point=q.get_center())
            question_marks.add(q)

        # Broken gears: two mismatched gears (simplified)
        gear1 = RegularPolygon(n=12, radius=0.6, color="#f8961e", fill_opacity=0.2).rotate(PI/12)
        gear1.set_stroke(color="#f8961e", width=2)
        gear2 = RegularPolygon(n=8, radius=0.4, color="#7209b7", fill_opacity=0.2).rotate(PI/8)
        gear2.set_stroke(color="#7209b7", width=2)
        gear1.move_to(RIGHT * 4 + UP * 1.5)
        gear2.move_to(LEFT * 3.5 + DOWN * 2)

        # Mismatched icons: lightbulb, puzzle, cloud, bug
        icons = VGroup(
            Text("💡", font_size=40).move_to(RIGHT * 3 + DOWN * 1.5),
            Text("🧩", font_size=40).move_to(UP * 2.5 + LEFT * 2),
            Text("☁️", font_size=42).move_to(UP * 1 + RIGHT * 1.5),
            Text("🐛", font_size=38).move_to(DOWN * 2.5 + RIGHT * 0.5),
        )

        # Animate entrance
        self.play(
            Create(brain_group, run_time=2, rate_func=rate_functions.ease_in_out_sine),
            FadeIn(question_marks, shift=UP, run_time=2.5),
            FadeIn(gear1, gear2, run_time=1.5),
            FadeIn(icons, shift=DOWN, run_time=2),
        )
        self.wait(0.5)

        # Subtle rotation & orbit animation
        self.play(
            brain_group.animate.rotate(0.2),
            question_marks.animate.shift(0.1 * UP).rotate(0.1),
            gear1.animate.rotate(0.3),
            gear2.animate.rotate(-0.4),
            run_time=3,
            rate_func=rate_functions.linear
        )

        # Slight wobble to emphasize confusion
        self.play(
            brain_group.animate.scale(1.03).set_color("#4895ef"),
            question_marks.animate.scale(1.05).set_color("#ff6b6b"),
            run_time=0.6,
            rate_func=rate_functions.there_and_back
        )

        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class GIGOFlow(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BLACK

        # Create trash cans
        trash_in = Text("Garbage In", font="Arial", weight=BOLD, font_size=24).set_color(WHITE)
        trash_in_box = Rectangle(height=1.2, width=2.0, color=GRAY, fill_opacity=0.1, stroke_width=2)
        trash_in_group = VGroup(trash_in_box, trash_in).arrange(DOWN, buff=0.2)

        trash_out = Text("Garbage Out", font="Arial", weight=BOLD, font_size=24).set_color(WHITE)
        trash_out_box = Rectangle(height=1.2, width=2.0, color=GRAY, fill_opacity=0.1, stroke_width=2)
        trash_out_group = VGroup(trash_out_box, trash_out).arrange(DOWN, buff=0.2)

        # LLM icon: simplified spinning gear-like symbol (using concentric circles + rotating lines)
        llm_center = Dot(point=ORIGIN, radius=0.05, color=BLUE)
        llm_circles = VGroup(
            Circle(radius=0.4, color=BLUE, stroke_width=2),
            Circle(radius=0.6, color=BLUE, stroke_width=2),
        )
        llm_spokes = VGroup(*[
            Line(ORIGIN, 0.6 * UP, color=BLUE, stroke_width=2).rotate_about_origin(i * PI/3)
            for i in range(6)
        ])
        llm_icon = VGroup(llm_circles, llm_spokes, llm_center).scale(0.8)

        # Position elements horizontally
        total_width = 8.0
        trash_in_group.move_to(LEFT * total_width/3)
        llm_icon.move_to(ORIGIN)
        trash_out_group.move_to(RIGHT * total_width/3)

        # Arrows
        arrow_left = Arrow(trash_in_group.get_right(), llm_icon.get_left(), buff=0.2, stroke_width=3, max_tip_length_to_length_ratio=0.1)
        arrow_right = Arrow(llm_icon.get_right(), trash_out_group.get_left(), buff=0.2, stroke_width=3, max_tip_length_to_length_ratio=0.1)

        # Assemble full flow
        flow = VGroup(trash_in_group, arrow_left, llm_icon, arrow_right, trash_out_group)

        # Animate
        self.play(FadeIn(trash_in_group), run_time=1)
        self.wait(0.5)
        self.play(GrowArrow(arrow_left), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(llm_icon), run_time=1)
        
        # Spin LLM icon
        self.play(
            Rotate(llm_icon, angle=2*PI, about_point=ORIGIN, rate_func=rate_functions.linear),
            run_time=3,
            rate_func=rate_functions.linear
        )
        
        self.play(GrowArrow(arrow_right), run_time=0.8)
        self.wait(0.5)
        self.play(FadeIn(trash_out_group), run_time=1)
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *
import numpy as np

class PromptConstraint(Scene):
    def construct(self):
        # Set background
        self.camera.background_color = BLACK

        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 1.5, 0.5],
            axis_config={"color": GRAY, "stroke_width": 1},
            num_axis_pieces=1,
        )

        # Bell-shaped probability distribution (Gaussian) — 3D surface
        def gauss_surface(u, v):
            x = u
            y = v
            z = np.exp(-0.5 * (x**2 + y**2))
            return np.array([x, y, z])

        # Use Surface with resolution for smoothness
        surface = Surface(
            lambda u, v: axes.c2p(*gauss_surface(u, v)),
            u_range=[-2.5, 2.5],
            v_range=[-2.5, 2.5],
            resolution=(24, 24),
            fill_opacity=0.8,
            stroke_width=0.5,
            fill_color=BLUE,
            stroke_color=BLUE_E,
        )
        surface.set_fill_by_value(axes=axes, colors=[(BLUE, 0), (PURPLE, 1.0)])

        # Spotlight beam: a narrowing cone (as translucent purple-to-white radial gradient)
        # We'll animate a shrinking circular cross-section at z=1.2, projecting down
        spotlight_base = Circle(
            radius=2.0,
            color=PURPLE,
            fill_opacity=0.2,
            stroke_width=0,
        ).move_to(axes.c2p(0, 0, 1.2))

        # Add to scene
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES, zoom=0.9)
        self.add(axes)
        self.play(Create(surface), run_time=2)
        self.wait(0.5)

        # Animate spotlight narrowing
        self.play(
            spotlight_base.animate.scale(0.3).set_fill(opacity=0.35),
            run_time=2,
            rate_func=rate_functions.ease_in_sine,
        )

        # 'Prompt' text appears above
        prompt_text = Text("Prompt", font="Arial", weight=BOLD, font_size=48, color=WHITE)
        prompt_text.move_to(axes.c2p(0, 0, 1.6))
        self.play(FadeIn(prompt_text, scale=0.8), run_time=1.5)

        # Optional subtle zoom-in or rotate for visual emphasis
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(2)
        self.stop_ambient_camera_rotation()
        self.wait(1)


# ==================== Auto-Generated ====================
from manim import *

class BadPromptExample(Scene):
    def construct(self):
        # Background: dark desaturated
        self.camera.background_color = "#222222"

        # Chaotic cloud of random story fragments
        fragments = [
            Text("dragon", font_size=24, color=GREY_A),
            Text("spaceship", font_size=24, color=GREY_A),
            Text("cupcake", font_size=24, color=GREY_A),
            Text("castle", font_size=24, color=GREY_A),
            Text("robot", font_size=24, color=GREY_A),
            Text("ocean", font_size=24, color=GREY_A),
            Text("forest", font_size=24, color=GREY_A),
            Text("time travel", font_size=24, color=GREY_A),
        ]
        
        cloud = VGroup()
        for frag in fragments:
            frag.move_to(
                3 * (np.random.random(3) - 0.5)
            )
            frag.rotate(np.random.uniform(-0.3, 0.3))
            cloud.add(frag)

        # Desaturate & lower contrast: already using GREY_A and dark bg; add slight blur effect via opacity
        for frag in cloud:
            frag.set_opacity(0.6)

        # Floating text "写个故事。"
        prompt_text = Text("写个故事。", font_size=36, font="Microsoft YaHei", color=GREY_C)

        # Red ❌ icon
        cross = Text("❌", font_size=48, color=RED)

        # Arrange: cross left, text right, both centered vertically
        group = VGroup(cross, prompt_text).arrange(RIGHT, buff=0.8)
        group.move_to(UP * 1.5)

        # Add subtle floating animation
        def float_updater(mob, dt):
            mob.shift(0.2 * dt * UP * np.sin(2 * self.time))

        prompt_text.add_updater(float_updater)
        cross.add_updater(float_updater)

        # Animate in
        self.play(
            FadeIn(cloud, scale=0.8, rate_func=rate_functions.ease_in_out_sine),
            run_time=2
        )
        self.wait(0.5)
        self.play(
            FadeIn(group, shift=DOWN * 0.5, scale=0.9),
            run_time=1.5
        )
        self.wait(3)

        # Clean up updaters
        prompt_text.clear_updaters()
        cross.clear_updaters()


# ==================== Auto-Generated ====================
from manim import *
import random

class AILostInQuestions(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Cartoon AI head (simplified: circle + eyes + smile)
        head = Circle(radius=1.2, color=BLUE_E, fill_opacity=0.8, stroke_width=3)
        left_eye = Circle(radius=0.2, color=WHITE, fill_opacity=1).shift(LEFT * 0.4 + UP * 0.3)
        right_eye = Circle(radius=0.2, color=WHITE, fill_opacity=1).shift(RIGHT * 0.4 + UP * 0.3)
        left_pupil = Circle(radius=0.08, color=BLACK, fill_opacity=1).move_to(left_eye.get_center() + LEFT * 0.05 + DOWN * 0.03)
        right_pupil = Circle(radius=0.08, color=BLACK, fill_opacity=1).move_to(right_eye.get_center() + RIGHT * 0.05 + DOWN * 0.03)
        mouth = Arc(start_angle=PI, angle=PI, radius=0.5, stroke_width=4, color=RED_E).shift(DOWN * 0.2)

        ai_head = VGroup(head, left_eye, right_eye, left_pupil, right_pupil, mouth)

        # Position head at center
        ai_head.move_to(ORIGIN)

        # Question texts
        questions = ["Theme?", "Audience?", "Length?", "Style?"]
        colors = [YELLOW, GREEN, PURPLE, ORANGE]
        positions = [
            UP * 2.5,
            RIGHT * 3,
            DOWN * 2.5,
            LEFT * 3
        ]

        q_marks = VGroup()
        for i, (q, pos, col) in enumerate(zip(questions, positions, colors)):
            text = Text(q, font_size=32, color=col, weight=BOLD, font="Arial")
            text.move_to(pos)
            # Slight initial offset for pop-in animation
            text.shift(pos * 0.8)
            q_marks.add(text)

        # Add head first
        self.play(FadeIn(ai_head), run_time=1.2)
        self.wait(0.5)

        # Animate each question mark popping up with bounce
        for i, q_mark in enumerate(q_marks):
            self.play(
                q_mark.animate.shift(-q_mark.get_center() + positions[i]).scale(0),
                run_time=0.1
            )
            self.play(
                q_mark.animate.scale(1.0).shift(UP * 0.1),
                rate_func=rate_functions.ease_out_bounce,
                run_time=0.8
            )
            self.wait(0.3)

        # Subtle head wobble to emphasize confusion
        self.play(
            ai_head.animate.rotate(0.05, about_point=ORIGIN),
            rate_func=rate_functions.there_and_back,
            run_time=1.5
        )

        self.wait(1.5)


# ==================== Auto-Generated ====================
from manim import *

class GoodPromptBreakdown(Scene):
    def construct(self):
        # Robot icon (simplified geometric robot)
        robot_body = Rectangle(height=2.0, width=1.2, fill_color=GRAY, fill_opacity=1, stroke_color=WHITE)
        robot_head = Circle(radius=0.5, fill_color=GRAY, fill_opacity=1, stroke_color=WHITE).shift(UP * 1.2)
        robot_eye_left = Circle(radius=0.12, fill_color=BLUE, fill_opacity=1).shift(UP * 1.25 + LEFT * 0.15)
        robot_eye_right = Circle(radius=0.12, fill_color=BLUE, fill_opacity=1).shift(UP * 1.25 + RIGHT * 0.15)
        robot_antenna = Line(UP * 1.7, UP * 2.3, stroke_color=WHITE, stroke_width=2)
        robot_antenna_dot = Circle(radius=0.07, fill_color=RED, fill_opacity=1).move_to(UP * 2.3)
        robot = VGroup(robot_body, robot_head, robot_eye_left, robot_eye_right, robot_antenna, robot_antenna_dot)
        robot.shift(LEFT * 4)

        # Checklist items
        items = [
            "Role: Sci-Fi Writer",
            "Style: Concise",
            "Topic: Lying Robot",
            "Length: 300 words",
            "Twist Ending"
        ]
        
        # Create checklist with green checkmarks
        checklist = VGroup()
        for i, item in enumerate(items):
            text = Text(item, font_size=24, color=WHITE)
            check = Text("✓", font_size=28, color=GREEN)
            entry = VGroup(check, text).arrange(RIGHT, buff=0.3)
            entry.shift(DOWN * (i - 2) * 0.8)  # vertically spaced
            checklist.add(entry)
        
        checklist.move_to(RIGHT * 2.5)

        # Add all elements
        self.add(robot)
        self.add(checklist)

        # Animate appearance
        self.play(
            FadeIn(robot, shift=LEFT),
            FadeIn(checklist, shift=RIGHT),
            run_time=1.5
        )
        self.wait(2)


# ==================== Auto-Generated ====================
from manim import *

class CodeToPromptTransition(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Split screen: left (code) and right (chat)
        left_rect = Rectangle(height=6, width=6, color=GRAY, stroke_width=1).to_edge(LEFT, buff=0.5)
        right_rect = Rectangle(height=6, width=6, color=GRAY, stroke_width=1).to_edge(RIGHT, buff=0.5)

        # Code block (Python-like)
        code_lines = [
            "def compute_gradient(x, y):",
            "    z = x ** 2 + y ** 2",
            "    return [2*x, 2*y]",
            "",
            "# Input:",
            "x, y = 3.0, 4.0"
        ]
        code_text = Text(
            "\n".join(code_lines),
            font="Fira Code",
            font_size=18,
            color=GREEN,
            line_spacing=1.2
        ).move_to(left_rect.get_center()).align_to(left_rect, LEFT).shift(RIGHT * 0.5)

        # Chat interface
        chat_bubble = RoundedRectangle(
            corner_radius=0.2,
            height=5.2,
            width=5.6,
            fill_color=GRAY_E,
            fill_opacity=0.3,
            stroke_color=BLUE,
            stroke_width=1
        ).move_to(right_rect.get_center())

        # Prompt text (natural language)
        prompt_lines = [
            "You are a math assistant.",
            "Compute the gradient of f(x,y) = x² + y²",
            "at point (3, 4). Show steps clearly."
        ]
        prompt_text = Text(
            "\n".join(prompt_lines),
            font="Segoe UI",
            font_size=20,
            color=WHITE,
            line_spacing=1.4,
            t2c={"gradient": BLUE, "x² + y²": YELLOW, "(3, 4)": TEAL}
        ).move_to(chat_bubble.get_center()).align_to(chat_bubble, LEFT).shift(RIGHT * 0.4)

        # Arrow from center of left to center of right
        arrow = Arrow(
            start=left_rect.get_right(),
            end=right_rect.get_left(),
            buff=0.2,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.1,
            color=YELLOW
        )

        # Add elements
        self.add(left_rect, right_rect, code_text, chat_bubble, prompt_text)
        
        # Animate arrow
        self.play(
            Create(arrow, run_time=1.5, rate_func=rate_functions.ease_out_sine),
            code_text.animate.set_opacity(0.7),
            prompt_text.animate.set_opacity(0.7)
        )
        self.wait(0.5)

        # Highlight transition: fade in arrow glow, pulse effect
        arrow_glow = arrow.copy().set_stroke(YELLOW, width=8, opacity=0.4)
        self.play(
            FadeIn(arrow_glow, scale=1.2),
            code_text.animate.set_opacity(0.5),
            prompt_text.animate.set_opacity(1.0),
            run_time=0.8
        )
        self.play(FadeOut(arrow_glow), run_time=0.5)

        self.wait(1)
