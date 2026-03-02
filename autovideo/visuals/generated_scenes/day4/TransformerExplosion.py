from manim import *

class TransformerExplosion(Scene):
    def construct(self):
        # 1. Input Nodes (Representing Text and Image inputs)
        text_node = RoundedRectangle(color=GREEN, height=1.0, width=2.0, corner_radius=0.1, fill_opacity=0.1)
        text_label = Text("Text", font_size=24, color=WHITE, weight=BOLD)
        text_group = VGroup(text_node, text_label)
        text_group.move_to(LEFT * 4 + UP * 1.5)

        image_node = RoundedRectangle(color=GREEN, height=1.0, width=2.0, corner_radius=0.1, fill_opacity=0.1)
        image_label = Text("Image", font_size=24, color=WHITE, weight=BOLD)
        image_group = VGroup(image_node, image_label)
        image_group.move_to(LEFT * 4 + DOWN * 1.5)

        # 2. Transformer Core Block
        core_outer = Rectangle(color=BLUE, height=3.5, width=4.5, fill_opacity=0.1, fill_color=BLUE)
        core_inner = Rectangle(color=BLUE_A, height=2.5, width=3.5, fill_opacity=0.3, fill_color=BLUE)
        core_label = Text("Transformer\nBlock", font_size=30, color=WHITE, weight=BOLD)
        core_group = VGroup(core_outer, core_inner, core_label)
        core_group.set_z_index(1)

        # 3. Connections (Arrows)
        arrow1 = Arrow(text_group.get_right(), core_group.get_left(), color=WHITE, buff=0.2)
        arrow2 = Arrow(image_group.get_right(), core_group.get_left(), color=WHITE, buff=0.2)

        # 4. Application Nodes (Initially hidden/small at center)
        app_names = ["GPT", "ViT", "BERT", "DALL-E", "CLIP"]
        app_colors = [YELLOW, PURPLE, RED, TEAL, ORANGE]
        target_dirs = [UP, DOWN, LEFT, RIGHT, UR] # UR is Up-Right
        
        app_groups = VGroup()
        for i, name in enumerate(app_names):
            circ = Circle(radius=0.5, color=app_colors[i], fill_opacity=0.8)
            label = Text(name, font_size=20, color=BLACK, weight=BOLD)
            group = VGroup(circ, label)
            group.move_to(ORIGIN)
            group.scale(0.1) # Start very small
            app_groups.add(group)

        # 5. Radiation Lines (Visual effect for explosion)
        radiating_lines = VGroup()
        for direction in target_dirs:
            line = Line(ORIGIN, direction * 4, color=WHITE, stroke_width=1)
            radiating_lines.add(line)
        radiating_lines.set_z_index(0)

        # --- Animation Sequence ---

        # Step 1: Create Inputs
        self.play(Create(text_group), Create(image_group), run_time=1.5)
        self.wait(0.5)

        # Step 2: Create Core
        self.play(Create(core_group), run_time=1.5)
        self.wait(0.5)

        # Step 3: Create Connections
        self.play(Create(arrow1), Create(arrow2), run_time=1.0)
        self.wait(0.5)

        # Step 4: Pulse Core (Processing)
        self.play(core_group.animate.scale(1.05).set_color(BLUE_E), run_time=0.4)
        self.play(core_group.animate.scale(1/1.05).set_color(BLUE), run_time=0.4)
        self.wait(0.5)

        # Step 5: Explosion Setup
        # Add app groups to scene at center (small)
        self.add(app_groups)
        self.add(radiating_lines)
        
        # Send core and arrows to back/fade out
        self.play(
            FadeOut(core_group), 
            FadeOut(arrow1), 
            FadeOut(arrow2),
            run_time=0.5
        )

        # Step 6: Explode Applications
        animations = []
        for i, group in enumerate(app_groups):
            direction = target_dirs[i]
            target_pos = direction * 3.5
            # Animate move to position and scale up from 0.1 to 1.0 (scale factor 10)
            animations.append(
                group.animate.move_to(target_pos).scale(10).set_z_index(10)
            )
        
        # Show radiation lines
        animations.append(radiating_lines.animate.set_stroke(width=3, opacity=0.5))

        self.play(*animations, run_time=2.0, rate_func=smooth)

        # Step 7: Final Polish (Ensure labels are crisp)
        self.wait(1.0)
