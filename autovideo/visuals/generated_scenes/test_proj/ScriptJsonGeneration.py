from manim import *

class ScriptJsonGeneration(Scene):
    def construct(self):
        # Background subtle grid
        plane = NumberPlane(
            background_line_style={"stroke_color": GREY_C, "stroke_width": 1},
            axis_config={"stroke_opacity": 0},
            faded_line_ratio=4
        )
        plane.set_z_index(-1)
        self.add(plane)

        # Folder icon: project/
        folder_rect = RoundedRectangle(
            corner_radius=0.2,
            width=3.0,
            height=1.8,
            fill_color=TEAL_A,
            fill_opacity=0.9,
            stroke_color=TEAL_E,
            stroke_width=2
        )
        folder_tab = Rectangle(
            width=1.2,
            height=0.5,
            fill_color=TEAL_E,
            fill_opacity=0.95,
            stroke_width=0
        ).next_to(folder_rect, UP, buff=0).align_to(folder_rect, LEFT).shift(RIGHT * 0.3)
        folder_label = Text("project/", font="monospace", font_size=24, color=WHITE).move_to(folder_rect.get_center())

        project_folder = VGroup(folder_rect, folder_tab, folder_label)
        project_folder.shift(UP * 0.5)

        # File icon: script.json
        file_rect = RoundedRectangle(
            corner_radius=0.08,
            width=3.2,
            height=0.9,
            fill_color=GREY_C,
            fill_opacity=0.85,
            stroke_color=GREY_C,
            stroke_width=1.5
        )
        file_label = Text("script.json", font="monospace", font_size=22, color=BLUE).move_to(file_rect.get_center())
        file_icon = VGroup(file_rect, file_label)
        file_icon.next_to(project_folder, DOWN, buff=0.8)

        # Simple checkmark built from two lines (replaces SVGMobject)
        checkmark_line1 = Line(
            start=LEFT * 0.3 + UP * 0.1,
            end=ORIGIN,
            stroke_color=GREEN,
            stroke_width=6
        )
        checkmark_line2 = Line(
            start=ORIGIN,
            end=RIGHT * 0.3 + DOWN * 0.3,
            stroke_color=GREEN,
            stroke_width=6
        )
        checkmark = VGroup(checkmark_line1, checkmark_line2)
        checkmark.next_to(file_icon, RIGHT, buff=0.5)

        # Glow animation using multiple expanding circles
        glow_circles = VGroup()
        for i in range(5):
            circ = Circle(
                radius=0.2 + i * 0.15,
                stroke_color=GREEN,
                stroke_width=2 - i * 0.3,
                fill_opacity=0.15 - i * 0.03,
                fill_color=GREEN
            ).move_to(checkmark.get_center())
            glow_circles.add(circ)

        # Tech UI styling: clean lines, monospace fonts, subtle shadows
        title = Text("File System Tree", font="monospace", font_size=32, weight=BOLD).to_edge(UP, buff=0.5)
        title.set_color_by_gradient(BLUE, PURPLE)

        # Animation sequence
        self.play(
            Write(title),
            run_time=1.2
        )
        self.wait(0.5)

        # Draw folder
        self.play(
            Create(folder_rect),
            Create(folder_tab),
            FadeIn(folder_label),
            run_time=1.4
        )
        self.wait(0.5)

        # Draw file (faded in)
        self.play(
            FadeIn(file_icon, shift=DOWN * 0.2, scale=0.95),
            run_time=1.2
        )
        self.wait(0.5)

        # Animate checkmark + glow
        self.play(
            FadeIn(checkmark, scale=1.5),
            run_time=0.8
        )
        self.play(
            Create(glow_circles),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine
        )
        self.wait(0.5)

        # Pulse glow effect
        self.play(
            glow_circles.animate.scale(1.1).set_opacity(0.2),
            rate_func=smooth,
            run_time=1.2
        )
        self.wait(1)

        # Final subtle emphasis
        self.play(
            project_folder.animate.set_stroke(TEAL_E, width=3),
            file_icon.animate.set_stroke(GREY_C, width=2),
            run_time=0.8
        )
        self.wait(1)
