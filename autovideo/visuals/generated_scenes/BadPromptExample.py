from manim import *

class BadPromptExample(Scene):
    def construct(self):
        # Background: subtle desaturated grey cloud-like base
        cloud_base = Circle(radius=6, color=GREY_C, fill_opacity=0.1, stroke_width=0.5)
        cloud_base.set_z_index(-1)

        # Chaotic cloud of random story fragments — hand-crafted minimal icons using primitives
        fragments = VGroup()

        # Dragon: simplified using arcs and triangles
        dragon = VGroup()
        dragon_body = Ellipse(width=1.2, height=0.6, color=TEAL_A).rotate(PI/6)
        dragon_head = Circle(radius=0.3, color=TEAL_A).move_to(dragon_body.get_right() + RIGHT*0.2)
        dragon_eye = Dot(color=YELLOW).scale(0.7).move_to(dragon_head.get_center() + UL*0.1)
        dragon_horn = Triangle().scale(0.15).set_fill(RED, 1).set_stroke(width=0).rotate(PI/3).move_to(dragon_head.get_top() + UP*0.2)
        dragon.add(dragon_body, dragon_head, dragon_eye, dragon_horn)

        # Spaceship: rectangle + triangle + circle window
        spaceship = VGroup()
        ship_body = Rectangle(width=1.4, height=0.5, color=BLUE_E, fill_opacity=0.8)
        ship_nose = Triangle().set_fill(BLUE_E, 1).set_stroke(width=0).scale(0.4).next_to(ship_body, RIGHT, buff=0)
        ship_window = Circle(radius=0.12, color=YELLOW_E, fill_opacity=0.9)
        spaceship.add(ship_body, ship_nose, ship_window)

        # Cupcake: circle (frosting) + rectangle (cup) + zigzag (sprinkles)
        cupcake = VGroup()
        frosting = Circle(radius=0.4, color=PINK).move_to(UP*0.2)
        cup = Rectangle(width=0.5, height=0.6, color=BROWN).move_to(DOWN*0.1)
        sprinkle = VGroup(*[
            Line(ORIGIN, UP*0.1, stroke_width=2, color=YELLOW_E).rotate(angle)
            for angle in [PI/4, -PI/4, PI/3, -PI/3]
        ]).move_to(frosting.get_center())
        cupcake.add(frosting, cup, sprinkle)

        # Scatter fragments randomly with rotation and low opacity
        for i in range(12):
            frag = None
            if i % 3 == 0:
                frag = dragon.copy()
            elif i % 3 == 1:
                frag = spaceship.copy()
            else:
                frag = cupcake.copy()
            frag.scale(0.4)
            frag.move_to(
                np.array([
                    (np.random.random() - 0.5) * 10,
                    (np.random.random() - 0.5) * 6,
                    0
                ])
            )
            frag.rotate(np.random.uniform(0, TAU))
            frag.set_opacity(0.3 + np.random.random() * 0.2)
            fragments.add(frag)

        # Floating text: '写个故事。' — desaturated, low contrast
        prompt_text = Text("写个故事。", font="Microsoft YaHei", weight=NORMAL, color=GREY_C)
        prompt_text.scale(1.4)

        # Red ❌ icon next to it — built from two crossed lines
        cross = VGroup(
            Line(UL * 0.4, DR * 0.4, stroke_color=RED, stroke_width=8),
            Line(UR * 0.4, DL * 0.4, stroke_color=RED, stroke_width=8)
        )

        # Group icon + text
        bad_prompt = VGroup(cross, prompt_text).arrange(RIGHT, buff=0.4)
        bad_prompt.move_to(UP * 2.5)

        # Animate gently floating up/down + slight sway
        self.add(cloud_base, fragments)
        self.play(
            FadeIn(bad_prompt, shift=DOWN * 0.5),
            run_time=2,
            rate_func=smooth
        )
        self.wait(0.5)

        # Gentle float animation
        self.play(
            bad_prompt.animate.shift(UP * 0.3).set_opacity(0.85),
            run_time=2,
            rate_func=smooth
        )
        self.play(
            bad_prompt.animate.shift(DOWN * 0.3).set_opacity(0.75),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)
