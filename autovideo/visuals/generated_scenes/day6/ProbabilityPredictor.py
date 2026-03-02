from manim import *

class ProbabilityPredictor(Scene):
    def construct(self):
        # Background remains black (default)

        # Dice icon: stylized 2D cartoon dice using squares and dots
        dice = Square(side_length=2, color=GREY_C, fill_opacity=1)
        dot_positions = [
            [0, 0, 0],  # center
            [-0.6, 0.6, 0], [0.6, -0.6, 0],  # diagonal pair
            [-0.6, 0.6, 0], [0, 0, 0], [0.6, -0.6, 0],  # three for "3"
        ]
        dots = VGroup(*[Dot(point=p, color=WHITE, radius=0.15) for p in dot_positions[:3]])
        dice_group = VGroup(dice, dots).shift(RIGHT * 4)

        # Neural network: 3-layer stylized 2D cartoon network (no 3D objects allowed)
        # Input layer (4 neurons)
        input_neurons = VGroup(*[Circle(radius=0.2, color=BLUE, fill_opacity=1) for _ in range(4)])
        input_neurons.arrange(DOWN, buff=0.5).shift(LEFT * 5)

        # Hidden layer (5 neurons)
        hidden_neurons = VGroup(*[Circle(radius=0.2, color=TEAL_A, fill_opacity=1) for _ in range(5)])
        hidden_neurons.arrange(DOWN, buff=0.5).shift(LEFT * 1.5)

        # Output layer (3 neurons)
        output_neurons = VGroup(*[Circle(radius=0.2, color=PURPLE_A, fill_opacity=1) for _ in range(3)])
        output_neurons.arrange(DOWN, buff=0.5).shift(RIGHT * 1.5)

        # Connect layers with arrows (light gray, thin)
        connections = VGroup()
        for i in range(4):
            for j in range(5):
                arrow = Arrow(
                    input_neurons[i].get_right(),
                    hidden_neurons[j].get_left(),
                    stroke_width=1,
                    buff=0.1,
                    color=GREY_C
                )
                connections.add(arrow)
        for i in range(5):
            for j in range(3):
                arrow = Arrow(
                    hidden_neurons[i].get_right(),
                    output_neurons[j].get_left(),
                    stroke_width=1,
                    buff=0.1,
                    color=GREY_C
                )
                connections.add(arrow)

        # Label for the neural network
        nn_label = Text("Neural Network", font_size=24, color=WHITE).next_to(input_neurons, UP, buff=0.8)

        # Arrow from output layer to dice, labeled "next token probability"
        prob_arrow = Arrow(
            output_neurons[1].get_right(),
            dice_group.get_left(),
            buff=0.2,
            stroke_width=2,
            color=YELLOW
        )
        label = Text("next token probability", font_size=20, color=YELLOW).next_to(prob_arrow, UP, buff=0.2)

        # Add all elements
        self.play(
            Create(input_neurons),
            Create(hidden_neurons),
            Create(output_neurons),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(Create(connections), run_time=2)
        self.play(Write(nn_label), run_time=1)
        self.wait(0.5)
        self.play(Create(prob_arrow), Write(label), run_time=1.5)
        self.wait(0.5)
        self.play(FadeIn(dice_group), run_time=1)
        self.wait(2)
