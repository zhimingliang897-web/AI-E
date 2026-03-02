from manim import *

class BadPromptExample(Scene):
    def construct(self):
        # Background: subtle desaturated grey cloud-like base (using overlapping ellipses)
        cloud_base = VGroup()
        for _ in range(15):
            ellipse = Ellipse(
                width=0.8 + np.random.random() * 1.2,
                height=0.4 + np.random.random() * 0.6,
                fill_opacity=0.08,
                stroke_opacity=0.05,
                color=GREY_C
            )
            ellipse.move_to(
                np.array([
                    (np.random.random() - 0.5) * 10,
                    (np.random.random() - 0.5) * 6,
                    0
                ])
            )
            cloud_base.add(ellipse)
        cloud_base.set_z_index(-1)

        # Random story fragments — simple desaturated icons using primitives
        fragments = VGroup()

        # Dragon: simplified using arcs and triangles
        dragon = VGroup()
        body = Arc(start_angle=PI/2, angle=-PI, radius=0.3, color=TEAL_A).shift(LEFT * 0.2)
        head = Circle(radius=0.15, color=TEAL_A, fill_opacity=0.3)
        head.next_to(body, RIGHT, buff=0)
        horn = Triangle(color=TEAL_A, fill_opacity=0.3).scale(0.1).rotate(PI/6).next_to(head, UP, buff=0)
        dragon.add(body, head, horn)

        # Spaceship: rectangle + triangle
        ship = VGroup()
        fuselage = Rectangle(width=0.5, height=0.2, color=BLUE_A, fill_opacity=0.25)
        nose = Triangle(color=BLUE_A, fill_opacity=0.25).scale(0.15).next_to(fuselage, RIGHT, buff=0)
        ship.add(fuselage, nose)

        # Cupcake: circle + arc + dot
        cupcake = VGroup()
        base = Circle(radius=0.18, color=YELLOW_A, fill_opacity=0.25)
        icing = Arc(start_angle=0, angle=PI, radius=0.22, color=YELLOW_A, fill_opacity=0.25)
        cherry = Dot(radius=0.05, color=RED, fill_opacity=0.4)
        icing.move_to(base.get_center())
        cherry.move_to(icing.point_at_angle(PI/2))
        cupcake.add(base, icing, cherry)

        # Add all fragments with random positions, rotations, and scales
        all_shapes = [dragon, ship, cupcake]
        for _ in range(12):
            shape = all_shapes[np.random.randint(0, len(all_shapes))].copy()
            shape.scale(0.7 + np.random.random() * 0.6)
            shape.rotate(np.random.random() * TAU)
            shape.move_to(
                np.array([
                    (np.random.random() - 0.5) * 8,
                    (np.random.random() - 0.5) * 4.5,
                    0
                ])
            )
            fragments.add(shape)

        # Main text: '写个故事。' — low contrast, desaturated
        prompt_text = Text("写个故事。", font="Microsoft YaHei", weight=NORMAL, color=GREY_C)
        prompt_text.scale(1.4)

        # Red ❌ icon next to it — using two crossed lines
        cross = VGroup()
        line1 = Line(UP * 0.4, DOWN * 0.4, color=RED, stroke_width=8)
        line2 = Line(LEFT * 0.4, RIGHT * 0.4, color=RED, stroke_width=8)
        cross.add(line1, line2)
        cross.scale(0.8)
        cross.next_to(prompt_text, LEFT, buff=0.4)

        # Group text + cross
        text_group = VGroup(cross, prompt_text)
        text_group.move_to(ORIGIN)
        text_group.shift(UP * 0.5)

        # Fade in background cloud
        self.play(FadeIn(cloud_base), run_time=1.5)
        self.wait(0.5)

        # Fade in fragments one by one with slight stagger
        self.play(LaggedStart(
            *[FadeIn(frag, scale=0.8) for frag in fragments],
            lag_ratio=0.03,
            run_time=2.5
        ))
        self.wait(0.5)

        # Fade in text group
        self.play(FadeIn(text_group, shift=UP * 0.3), run_time=1.2)
        self.wait(1.5)

        # Subtle pulse to emphasize low-contrast feel
        self.play(
            text_group.animate.scale(1.02).set_color(GREY),
            rate_func=smooth,
            run_time=2
        )
        self.wait(1)
