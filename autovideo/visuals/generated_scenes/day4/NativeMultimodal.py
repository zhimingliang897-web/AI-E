from manim import *
import numpy as np
import random

class NativeMultimodal(Scene):
    def construct(self):
        # Title
        title = Text("Native Multimodal", weight=BOLD, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)

        # Modality Groups representing Text, Image, Sound
        text_group = VGroup(
            Text("Text", color=BLUE, weight=BOLD),
            Rectangle(color=BLUE, height=0.6, width=1.0, fill_opacity=0.2, fill_color=BLUE)
        ).arrange(RIGHT, buff=0.2)
        text_group.move_to(LEFT * 4)

        image_group = VGroup(
            Text("Image", color=GREEN, weight=BOLD),
            Square(color=GREEN, side_length=0.7, fill_opacity=0.2, fill_color=GREEN)
        ).arrange(RIGHT, buff=0.2)
        image_group.move_to(RIGHT * 4)

        sound_group = VGroup(
            Text("Sound", color=YELLOW, weight=BOLD),
            Circle(color=YELLOW, radius=0.35, fill_opacity=0.2, fill_color=YELLOW)
        ).arrange(RIGHT, buff=0.2)
        sound_group.move_to(UP * 3)

        # Show initial modalities
        self.play(FadeIn(text_group), FadeIn(image_group), FadeIn(sound_group))
        self.wait(1)

        # Generate Brain Network (Interconnected Nodes)
        dots = VGroup()
        lines = VGroup()
        positions = []
        
        # Generate points within an ellipse resembling a brain shape
        random.seed(42) # For reproducibility
        for _ in range(50):
            while True:
                x = random.uniform(-2.5, 2.5)
                y = random.uniform(-2, 2)
                # Ellipse equation check to constrain shape
                if (x**2 / 2.5**2) + (y**2 / 1.8**2) <= 1:
                    positions.append(np.array([x, y, 0]))
                    break
        
        for pos in positions:
            dots.add(Dot(pos, radius=0.12, color=WHITE))
        
        # Connect nearby dots to form network
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                dist = np.linalg.norm(positions[i] - positions[j])
                if 0.4 < dist < 1.0:
                    line = Line(positions[i], positions[j], stroke_width=1.5, color=WHITE, stroke_opacity=0.5)
                    lines.add(line)
        
        brain_network = VGroup(dots, lines)
        brain_network.set_opacity(0)
        brain_network.set_z_index(-1)

        # Merge Animation: Modalities converge to center
        self.play(
            text_group.animate.move_to(ORIGIN).set_opacity(0.2),
            image_group.animate.move_to(ORIGIN).set_opacity(0.2),
            sound_group.animate.move_to(ORIGIN).set_opacity(0.2),
            run_time=2,
            rate_func=smooth
        )

        # Transform into Brain Network
        self.play(
            FadeOut(text_group),
            FadeOut(image_group),
            FadeOut(sound_group),
            FadeIn(brain_network),
            run_time=1.5
        )

        # Glow/Pulse Effect to simulate activity
        glow_layer = brain_network.copy().set_color(WHITE).set_opacity(0.4).scale(1.0)
        self.add(glow_layer)
        
        # Pulse outward
        self.play(
            glow_layer.animate.scale(1.3).set_opacity(0.0),
            brain_network.animate.set_color(WHITE),
            rate_func=smooth,
            run_time=2
        )
        
        # Reset glow for loop effect
        glow_layer.set_opacity(0.4).scale(1.0/1.3)
        self.play(
            glow_layer.animate.scale(1.1).set_opacity(0.2),
            rate_func=smooth,
            run_time=2
        )

        self.wait(1)
