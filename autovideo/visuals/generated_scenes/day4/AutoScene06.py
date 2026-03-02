from manim import *

class AutoScene06(Scene):
    def construct(self):
        # Title
        title = Text("Neural Network Inference", font_size=32, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(0.5)

        # Left side: Grid of image thumbnails (10x10)
        thumbnail_grid = VGroup()
        for i in range(10):
            for j in range(10):
                # Small square thumbnail
                thumb = Square(side_length=0.2, fill_color=GREY_C, fill_opacity=0.7, stroke_width=0.5)
                thumb.move_to(LEFT * 4 + RIGHT * j * 0.25 + DOWN * i * 0.25)
                thumbnail_grid.add(thumb)
        
        grid_label = Text("10,000 Images", font_size=20).next_to(thumbnail_grid, UP, buff=0.3)
        
        self.play(FadeIn(thumbnail_grid), Write(grid_label))
        self.wait(1)

        # Right side: Neural network schematic (3-layer stylized)
        # Input layer (small circles)
        input_neurons = VGroup(*[Circle(radius=0.08, fill_color=BLUE, fill_opacity=1, stroke_width=1) 
                                for _ in range(6)])
        for i, n in enumerate(input_neurons):
            n.move_to(LEFT * 1 + UP * (1.2 - i * 0.4))

        # Hidden layer (medium circles)
        hidden_neurons = VGroup(*[Circle(radius=0.1, fill_color=TEAL_A, fill_opacity=1, stroke_width=1) 
                                  for _ in range(5)])
        for i, n in enumerate(hidden_neurons):
            n.move_to(ORIGIN + UP * (1.0 - i * 0.5))

        # Output layer (larger circle)
        output_neuron = Circle(radius=0.15, fill_color=PURPLE_E, fill_opacity=1, stroke_width=1).move_to(RIGHT * 1.2)

        # Arrows between layers
        arrows = VGroup()
        for in_n in input_neurons:
            for hid_n in hidden_neurons:
                arrows.add(Arrow(in_n.get_right(), hid_n.get_left(), buff=0.1, stroke_width=1))
        for hid_n in hidden_neurons:
            arrows.add(Arrow(hid_n.get_right(), output_neuron.get_left(), buff=0.1, stroke_width=1))

        # Label arrow P(Y|X)
        p_label = Text("P(Y|X)", font_size=20).next_to(arrows[-1], UP, buff=0.2)

        # Group neural net
        nn_group = VGroup(input_neurons, hidden_neurons, output_neuron, arrows, p_label)
        nn_group.move_to(RIGHT * 2.5)

        self.play(FadeIn(nn_group))
        self.wait(1)

        # Output text: "Cat" with checkmark
        cat_text = Text("Cat", font_size=28, color=GREEN).next_to(output_neuron, RIGHT, buff=0.5)
        checkmark = Text(r"\checkmark", color=GREEN, font_size=36).next_to(cat_text, RIGHT, buff=0.3)

        self.play(Write(cat_text))
        self.wait(0.5)
        self.play(Write(checkmark))
        self.wait(1)

        # Optional subtle highlight pulse on output neuron
        self.play(output_neuron.animate.set_stroke(color=YELLOW, width=3), run_time=0.5)
        self.play(output_neuron.animate.set_stroke(width=1), run_time=0.5)

        self.wait(1)
