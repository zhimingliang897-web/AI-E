from manim import *

class TransformerBase(Scene):
    def construct(self):
        # Title
        title = Text("Transformer Architecture", weight=BOLD, font_size=48)
        title.to_edge(UP)
        self.play(Write(title), rate_func=smooth)
        self.wait(0.5)

        # Colors
        text_color = BLUE
        vision_color = GREEN
        connect_color = YELLOW

        # Create Text Module Blocks (Left)
        text_blocks = VGroup()
        for i in range(3):
            block = RoundedRectangle(height=0.8, width=2.5, color=text_color, corner_radius=0.1)
            label = Text(f"Text Layer {i+1}", font_size=24, weight=BOLD)
            label.move_to(block.get_center())
            group = VGroup(block, label)
            group.shift(LEFT * 2.5 + DOWN * (1.5 - i * 1.2))
            text_blocks.add(group)

        # Create Vision Module Blocks (Right)
        vision_blocks = VGroup()
        for i in range(3):
            block = RoundedRectangle(height=0.8, width=2.5, color=vision_color, corner_radius=0.1)
            label = Text(f"Vision Layer {i+1}", font_size=24, weight=BOLD)
            label.move_to(block.get_center())
            group = VGroup(block, label)
            group.shift(RIGHT * 2.5 + DOWN * (1.5 - i * 1.2))
            vision_blocks.add(group)

        # Save Final States
        text_blocks.save_state()
        vision_blocks.save_state()

        # Move to Start Positions (Off-screen for Lego Assembly)
        text_blocks.shift(LEFT * 4)
        vision_blocks.shift(RIGHT * 4)

        # Add to Scene
        self.add(text_blocks, vision_blocks)

        # Animate Assembly
        self.play(
            text_blocks.animate.restore(),
            vision_blocks.animate.restore(),
            rate_func=smooth,
            run_time=2
        )
        self.wait(0.5)

        # Create Connections
        arrows = VGroup()
        for i in range(3):
            start = text_blocks[i][0].get_right()
            end = vision_blocks[i][0].get_left()
            arrow = Arrow(start, end, color=connect_color, buff=0.1, stroke_width=4)
            arrows.add(arrow)

        # Set arrows behind blocks if needed, but here we want them visible
        # Using set_z_index to ensure proper layering if overlaps occur
        arrows.set_z_index(-1)

        self.play(Create(arrows), rate_func=smooth, run_time=1.5)
        self.wait(0.5)

        # Glowing Connections Effect
        for arrow in arrows:
            flash = ShowPassingFlash(
                arrow.copy().set_stroke(WHITE, width=8),
                time_width=0.4,
                run_time=0.8
            )
            self.play(flash)

        self.wait(1)
