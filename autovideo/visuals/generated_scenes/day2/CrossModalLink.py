from manim import *

class CrossModalLink(Scene):
    def construct(self):
        # Background
        self.camera.background_color = BLACK

        # Photo box (left)
        photo_box = RoundedRectangle(corner_radius=0.2, height=3, width=4, color=GREY_C, stroke_width=2)
        photo_label = Text("Photo", font_size=24, color=GREY_C).next_to(photo_box, UP, buff=0.2)
        photo_group = VGroup(photo_box, photo_label)

        # Caption box (right)
        caption_box = RoundedRectangle(corner_radius=0.2, height=3, width=4, color=TEAL_A, stroke_width=2)
        caption_label = Text("Caption", font_size=24, color=TEAL_A).next_to(caption_box, UP, buff=0.2)
        caption_group = VGroup(caption_box, caption_label)

        # Position boxes
        photo_group.shift(LEFT * 4.5)
        caption_group.shift(RIGHT * 4.5)

        # Bidirectional arrow (center)
        arrow_start = photo_box.get_right()
        arrow_end = caption_box.get_left()
        bi_arrow = DoubleArrow(
            start=arrow_start,
            end=arrow_end,
            buff=0.1,
            stroke_width=6,
            tip_length=0.2,
            color=YELLOW
        )
        bi_arrow.set_z_index(1)

        # Semantic link label
        link_label = Text("semantic link", font_size=28, color=YELLOW, weight=BOLD)
        link_label.next_to(bi_arrow, UP, buff=0.3)

        # Pulse animation for arrow + label
        def pulse_anim(mob, dt):
            scale = 1 + 0.1 * np.sin(2 * TAU * self.time)
            mob.become(mob.copy().scale(scale).set_opacity(0.9 + 0.1 * np.cos(2 * TAU * self.time)))

        # Morph sequence: photo → sketch → text → emoji → photo
        # Use simple stylized representations (no external assets)

        # Photo: camera icon (circle + lens)
        photo_icon = VGroup(
            Circle(radius=1.0, color=WHITE, stroke_width=2),
            Circle(radius=0.3, color=WHITE, stroke_width=2).move_to(UP * 0.2),
            Line(LEFT * 0.4, RIGHT * 0.4, stroke_width=2).move_to(DOWN * 0.3),
        ).set_z_index(2)

        # Sketch: simplified line drawing (e.g., house outline)
        sketch_icon = VGroup(
            Polygon(ORIGIN, UP * 1.2, RIGHT * 1, LEFT * 1, color=GREY, fill_opacity=0, stroke_width=2.5),
            Line(UP * 0.4 + LEFT * 0.3, UP * 0.4 + RIGHT * 0.3, stroke_width=2.5),
            Line(UP * 0.1 + LEFT * 0.2, UP * 0.1 + RIGHT * 0.2, stroke_width=2.5),
        ).set_z_index(2)

        # Text: "scene" in bold sans-serif
        text_icon = Text("scene", font_size=36, color=BLUE, weight=BOLD).set_z_index(2)

        # Emoji: simple smiley (circle + arcs)
        emoji_icon = VGroup(
            Circle(radius=1.0, color=ORANGE, stroke_width=2.5),
            Arc(start_angle=PI / 4, angle=PI / 2, radius=0.4, stroke_width=2.5).shift(UP * 0.2 + LEFT * 0.3),
            Arc(start_angle=-PI / 4, angle=-PI / 2, radius=0.4, stroke_width=2.5).shift(UP * 0.2 + RIGHT * 0.3),
            Dot(UP * 0.4 + LEFT * 0.2, radius=0.08, color=BLACK),
            Dot(UP * 0.4 + RIGHT * 0.2, radius=0.08, color=BLACK),
        ).set_z_index(2)

        # Scale and position all icons inside photo_box
        icon_scale = 0.7
        photo_icon.scale(icon_scale).move_to(photo_box.get_center())
        sketch_icon.scale(icon_scale).move_to(photo_box.get_center())
        text_icon.scale(icon_scale).move_to(photo_box.get_center())
        emoji_icon.scale(icon_scale).move_to(photo_box.get_center())

        # Add static elements first
        self.add(photo_group, caption_group)
        self.wait(0.5)

        # Animate bidirectional arrow + label with pulse
        self.play(
            Create(bi_arrow),
            Write(link_label),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(0.5)

        # Start pulsing arrow & label
        bi_arrow.add_updater(pulse_anim)
        link_label.add_updater(pulse_anim)

        # Morph sequence (looped seamlessly)
        morphs = [
            (photo_icon, sketch_icon, 1.2),
            (sketch_icon, text_icon, 1.2),
            (text_icon, emoji_icon, 1.2),
            (emoji_icon, photo_icon, 1.2),
        ]

        # Initial photo
        self.play(FadeIn(photo_icon), run_time=0.8)
        self.wait(0.5)

        # Loop morphs
        for i, (start, target, dur) in enumerate(morphs):
            self.play(
                Transform(start, target),
                run_time=dur,
                rate_func=smooth
            )
            if i < len(morphs) - 1:
                self.wait(0.3)
            else:
                self.wait(0.5)

        # Remove updaters
        bi_arrow.clear_updaters()
        link_label.clear_updaters()

        # Final hold
        self.wait(1.5)
