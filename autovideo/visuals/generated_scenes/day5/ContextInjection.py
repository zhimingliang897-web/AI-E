from manim import *

class ContextInjection(Scene):
    def construct(self):
        # System Prompt Container
        system_box = Rectangle(height=5, width=9, color=GREY, stroke_width=2)
        system_box.set_z_index(-1)
        
        # User Query Container
        user_box = Rectangle(height=1.5, width=4, color=BLUE, stroke_width=3)
        user_box.set_z_index(1)
        
        # Text Elements
        system_label = Text("System Prompt", font_size=28, color=GREY)
        system_label.to_edge(UP).shift(DOWN * 0.5)
        
        user_text = Text("User Query", font_size=36, color=BLUE, weight=BOLD)
        
        # Constraint Text Parts (to allow highlighting specific words without Tex)
        constraint_pre = Text("Adhere to ", font_size=24, color=WHITE)
        constraint_highlight = Text("strict output format", font_size=24, color=YELLOW, weight=BOLD)
        constraint_post = Text(" constraints", font_size=24, color=WHITE)
        
        # Arrange constraint parts horizontally
        constraint_group = VGroup(constraint_pre, constraint_highlight, constraint_post)
        constraint_group.arrange(RIGHT, buff=0.1)
        constraint_group.to_edge(DOWN).shift(UP * 0.5)
        
        # Positioning
        user_text.move_to(user_box.get_center())
        user_box.move_to(ORIGIN)
        
        # Top context text inside system box
        top_context = Text("Context: Injection Mode Active", font_size=24, color=GREY)
        top_context.next_to(user_box, UP, buff=0.5)
        
        # Bottom context (constraint) inside system box
        constraint_group.next_to(user_box, DOWN, buff=0.5)
        
        # Grouping for animation
        system_content = VGroup(system_label, top_context, constraint_group)
        
        # Animation Sequence
        # 1. Show System Boundary
        self.play(Create(system_box), Write(system_label), rate_func=smooth, run_time=2)
        self.wait(1)
        
        # 2. Show Top Context
        self.play(FadeIn(top_context), rate_func=smooth, run_time=1)
        self.wait(0.5)
        
        # 3. Show User Query (in front)
        self.play(Create(user_box), Write(user_text), rate_func=smooth, run_time=2)
        self.wait(1)
        
        # 4. Show Constraint Text
        self.play(FadeIn(constraint_group), rate_func=smooth, run_time=2)
        self.wait(1)
        
        # 5. Highlight Pulse Effect on Constraint
        self.play(
            constraint_highlight.animate.scale(1.2).set_color(RED),
            rate_func=smooth,
            run_time=1
        )
        self.play(
            constraint_highlight.animate.scale(1.0).set_color(YELLOW),
            rate_func=smooth,
            run_time=1
        )
        
        self.wait(1)
