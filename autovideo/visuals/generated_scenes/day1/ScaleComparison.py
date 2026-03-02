from manim import *

class ScaleComparison(Scene):
    def construct(self):
        # Background remains black (default)

        # --- Brain icon (cartoon-style, 2D) ---
        # Base brain shape: two symmetrical lobes
        left_lobe = Ellipse(width=2.0, height=1.6, color=PURPLE_E).shift(LEFT * 0.8)
        right_lobe = Ellipse(width=2.0, height=1.6, color=PURPLE_E).shift(RIGHT * 0.8)
        brain_center = Circle(radius=0.6, color=PURPLE_E).move_to(ORIGIN)
        brain = VGroup(left_lobe, right_lobe, brain_center).set_fill(PURPLE_A, opacity=1).set_stroke(width=0)
        
        # Add simple cartoon "folds" with curved arcs
        fold1 = ArcBetweenPoints(
            start=LEFT * 0.6 + UP * 0.4,
            end=RIGHT * 0.6 + UP * 0.4,
            angle=-PI/3,
            color=GREY_C,
            stroke_width=2
        )
        fold2 = ArcBetweenPoints(
            start=LEFT * 0.5 + DOWN * 0.3,
            end=RIGHT * 0.5 + DOWN * 0.3,
            angle=PI/4,
            color=GREY_C,
            stroke_width=2
        )
        brain.add(fold1, fold2)

        # --- Neuron network icon (digital, 2D stylized) ---
        # Central node
        center_node = Circle(radius=0.2, color=TEAL_A).set_fill(TEAL_A, opacity=1)
        # Surrounding nodes
        nodes = VGroup()
        connections = VGroup()
        for i in range(6):
            angle = TAU * i / 6
            pos = np.array([np.cos(angle), np.sin(angle), 0]) * 1.4
            node = Circle(radius=0.12, color=TEAL_A).set_fill(TEAL_A, opacity=1).move_to(pos)
            nodes.add(node)
            # Connect to center
            conn = Line(center_node.get_center(), node.get_center(), color=TEAL_A, stroke_width=1.5)
            connections.add(conn)
        # Add a few cross-links for "network" feel
        cross1 = Line(nodes[0].get_center(), nodes[2].get_center(), color=TEAL_A, stroke_width=1)
        cross2 = Line(nodes[3].get_center(), nodes[5].get_center(), color=TEAL_A, stroke_width=1)
        neuron_net = VGroup(center_node, nodes, connections, cross1, cross2).scale(0.9)

        # --- Labels ---
        label_text = Text("100B+ connections", font_size=24, color=WHITE)
        brain_label = label_text.copy().next_to(brain, DOWN, buff=0.3)
        net_label = label_text.copy().next_to(neuron_net, DOWN, buff=0.3)

        # --- Sparkles (small rotating stars) ---
        def make_sparkle(color, scale=0.3):
            star = RegularPolygon(n=5, radius=0.1 * scale, color=color, fill_opacity=1)
            star.set_fill(color, opacity=1)
            return star

        sparkles = VGroup()
        for _ in range(8):
            s = make_sparkle(YELLOW, scale=0.4)
            s.move_to(np.random.uniform(-3, 3, 3))
            s.rotate(np.random.uniform(0, TAU))
            sparkles.add(s)

        # --- Layout: brain on left, network on right, centered vertically ---
        group = VGroup(brain, neuron_net).arrange(RIGHT, buff=2.5).move_to(ORIGIN)
        brain.move_to(group[0])
        neuron_net.move_to(group[1])
        brain_label.next_to(brain, DOWN, buff=0.3)
        net_label.next_to(neuron_net, DOWN, buff=0.3)

        # --- Animation sequence ---
        # 1. Fade in both icons and labels
        self.play(
            FadeIn(brain, shift=UP * 0.5, scale=0.8),
            FadeIn(neuron_net, shift=UP * 0.5, scale=0.8),
            Write(brain_label, run_time=1.2),
            Write(net_label, run_time=1.2),
            lag_ratio=0.3
        )
        self.wait(0.5)

        # 2. Animate sparkles: fade in + twinkle + slight rotation
        self.play(
            LaggedStart(*[
                FadeIn(s, scale=1.5) for s in sparkles
            ], lag_ratio=0.05),
            run_time=1.5
        )
        self.play(
            Rotate(sparkles, angle=PI/6, about_point=ORIGIN, run_time=2, rate_func=smooth),
            *[s.animate.scale(1.2).set_opacity(0.7) for s in sparkles[:4]],
            *[s.animate.scale(0.8).set_opacity(1.0) for s in sparkles[4:]],
            run_time=2
        )
        self.wait(0.5)

        # 3. Zoom effect: scale up both icons slightly, then back — with emphasis
        self.play(
            brain.animate.scale(1.15).set_z_index(10),
            neuron_net.animate.scale(1.15).set_z_index(10),
            brain_label.animate.scale(1.1),
            net_label.animate.scale(1.1),
            run_time=0.8,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.play(
            brain.animate.scale(1/1.15),
            neuron_net.animate.scale(1/1.15),
            brain_label.animate.scale(1/1.1),
            net_label.animate.scale(1/1.1),
            run_time=0.8,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(1)

        # 4. Final subtle pulse on both icons
        self.play(
            brain.animate.scale(1.05).set_color(PURPLE_E),
            neuron_net.animate.scale(1.05).set_color(TEAL_A),
            run_time=0.6,
            rate_func=smooth
        )
        self.wait(1)
