from manim import *

class GANBattle(Scene):
    def construct(self):
        # Create Robots using primitives
        gen_robot = self.create_robot(color=BLUE, label="Generator")
        disc_robot = self.create_robot(color=RED, label="Discriminator")
        
        gen_robot.move_to(LEFT * 4)
        disc_robot.move_to(RIGHT * 4)
        
        self.play(Create(gen_robot), Create(disc_robot))
        self.wait(0.5)
        
        # Labels
        gen_label = Text("Generator", weight=BOLD, color=BLUE).next_to(gen_robot, DOWN)
        disc_label = Text("Discriminator", weight=BOLD, color=RED).next_to(disc_robot, DOWN)
        self.play(Write(gen_label), Write(disc_label))
        self.wait(0.5)
        
        # Battle Loop
        current_face = None
        current_mark = None
        
        for i in range(3):
            # Clean up previous iteration
            if current_face:
                self.play(FadeOut(current_face), FadeOut(current_mark))
            
            # Generate Fake Face
            quality = 0.5 + (i * 0.15)
            current_face = self.create_face(perfect=False, quality=quality)
            current_face.move_to(ORIGIN)
            
            self.play(Create(current_face))
            self.wait(0.3)
            
            # Arrow from Gen to Face
            arrow = Arrow(gen_robot.get_right(), current_face.get_left(), color=BLUE, buff=0.2)
            self.play(Create(arrow))
            self.wait(0.2)
            self.play(FadeOut(arrow))
            
            # Discriminator Rejects
            current_mark = self.create_cross()
            current_mark.set_color(RED)
            current_mark.scale(1.5)
            current_mark.next_to(current_face, RIGHT)
            
            self.play(Create(current_mark))
            self.wait(0.5)
            
        # Final Perfect Face
        if current_face:
            self.play(FadeOut(current_face), FadeOut(current_mark))
            
        perfect_face = self.create_face(perfect=True)
        perfect_face.move_to(ORIGIN)
        self.play(Create(perfect_face))
        self.wait(0.5)
        
        # Discriminator Accepts
        accept_mark = self.create_check()
        accept_mark.set_color(GREEN)
        accept_mark.scale(1.5)
        accept_mark.next_to(perfect_face, RIGHT)
        
        self.play(Create(accept_mark))
        self.wait(0.5)
        
        # Celebration
        self.play(
            perfect_face.animate.set_color(YELLOW),
            accept_mark.animate.set_color(GREEN),
            run_time=1
        )
        self.wait(1)

    def create_robot(self, color, label):
        head = Circle(radius=0.5, color=color, fill_opacity=0.5)
        body = Rectangle(height=1.5, width=1, color=color, fill_opacity=0.5)
        body.next_to(head, DOWN, buff=0)
        arm_l = Line(body.get_left() + UP * 0.5, body.get_left() + LEFT * 0.5 + DOWN * 0.5, color=color)
        arm_r = Line(body.get_right() + UP * 0.5, body.get_right() + RIGHT * 0.5 + DOWN * 0.5, color=color)
        eye = Circle(radius=0.1, color=WHITE, fill_opacity=1).move_to(head.get_center() + UP * 0.1)
        
        robot = VGroup(head, body, arm_l, arm_r, eye)
        return robot

    def create_face(self, perfect=False, quality=1.0):
        outline = Circle(radius=1, color=WHITE, fill_opacity=0.1)
        
        # Eyes
        eye_offset = 0.3 * quality
        eye_y = 0.2 * quality
        left_eye = Circle(radius=0.15, color=WHITE, fill_opacity=1).move_to(LEFT * eye_offset + UP * eye_y)
        right_eye = Circle(radius=0.15, color=WHITE, fill_opacity=1).move_to(RIGHT * eye_offset + UP * eye_y)
        
        # Mouth
        if perfect:
            # Smile Arc
            mouth = Arc(radius=0.5, start_angle=PI, angle=-PI, color=WHITE).shift(UP * 0.2)
        else:
            # Imperfect mouth (line)
            mouth = Line(LEFT * 0.3, RIGHT * 0.3, color=WHITE).shift(UP * 0.3 + DOWN * 0.1)
            
        face = VGroup(outline, left_eye, right_eye, mouth)
        if not perfect:
            face.set_opacity(0.7)
        return face

    def create_cross(self):
        l1 = Line(UP + LEFT, DOWN + RIGHT)
        l2 = Line(UP + RIGHT, DOWN + LEFT)
        return VGroup(l1, l2)

    def create_check(self):
        l1 = Line(LEFT * 0.5 + UP * 0.5, ORIGIN)
        l2 = Line(ORIGIN, RIGHT * 0.5 + UP * 1.0)
        return VGroup(l1, l2)
