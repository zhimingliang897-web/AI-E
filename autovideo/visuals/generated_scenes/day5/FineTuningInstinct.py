from manim import *

class FineTuningInstinct(Scene):
    def construct(self):
        # Define layer positions
        input_x = -3
        hidden_x = 0
        output_x = 3

        input_y = [1, 0, -1]
        hidden_y = [1.5, 0.5, -0.5, -1.5]
        output_y = [1, -1]

        # Create Nodes
        input_nodes = VGroup(*[Circle(radius=0.2, color=GREY, fill_opacity=0.5).move_to([input_x, y, 0]) for y in input_y])
        hidden_nodes = VGroup(*[Circle(radius=0.2, color=GREY, fill_opacity=0.5).move_to([hidden_x, y, 0]) for y in hidden_y])
        output_nodes = VGroup(*[Circle(radius=0.2, color=GREY, fill_opacity=0.5).move_to([output_x, y, 0]) for y in output_y])

        all_nodes = VGroup(input_nodes, hidden_nodes, output_nodes)

        # Create Edges (Fully connected for visual)
        edges = VGroup()
        # Input to Hidden
        for i_node in input_nodes:
            for h_node in hidden_nodes:
                edges.add(Line(i_node.get_center(), h_node.get_center(), color=GREY, stroke_opacity=0.3))
        # Hidden to Output
        for h_node in hidden_nodes:
            for o_node in output_nodes:
                edges.add(Line(h_node.get_center(), o_node.get_center(), color=GREY, stroke_opacity=0.3))

        # Put edges behind nodes
        edges.set_z_index(-1)
        all_nodes.set_z_index(0)

        network = VGroup(edges, all_nodes)

        # Input Text
        label = Text("Tool Definition", weight=BOLD, color=BLUE).to_edge(UP)

        # Animation 1: Show Network
        self.play(Create(network), run_time=2)
        self.wait(0.5)

        # Animation 2: Show Input
        self.play(Write(label), run_time=1)
        self.wait(0.5)

        # Define Active Path based on creation order indices
        # Input nodes: 0, 1, 2. Hidden: 0, 1, 2, 3. Output: 0, 1
        # Input->Hidden edges count: 3 * 4 = 12. Indices 0-11.
        # Hidden->Output edges count: 4 * 2 = 8. Indices 12-19.
        
        # Path 1: Input[1] -> Hidden[1] -> Output[0]
        # Edge index = 1 * 4 + 1 = 5
        edge_i1_h1 = edges[5]
        # Edge index = 12 + (1 * 2 + 0) = 14
        edge_h1_o0 = edges[14]

        # Path 2: Input[2] -> Hidden[2] -> Output[1]
        # Edge index = 2 * 4 + 2 = 10
        edge_i2_h2 = edges[10]
        # Edge index = 12 + (2 * 2 + 1) = 17
        edge_h2_o1 = edges[17]

        active_path = VGroup(edge_i1_h1, edge_h1_o0, edge_i2_h2, edge_h2_o1)

        # Animation 3: Light up paths
        self.play(
            active_path.animate.set_color(YELLOW).set_stroke(opacity=1, width=4),
            run_time=2,
            rate_func=smooth
        )
        self.wait(0.5)

        # Animation 4: Output nodes glow
        self.play(
            output_nodes.animate.set_color(GREEN).set_fill_opacity(1),
            run_time=1
        )
        self.wait(1)
