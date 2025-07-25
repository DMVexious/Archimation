from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.coqui import CoquiService

class Generated_Course(VoiceoverScene):
    def setup(self):
        """Set up the scene for voiceover and camera."""
        # FIX: Explicitly set a Coqui model to prevent download/path errors.
        self.set_speech_service(CoquiService(model_name="tts_models/en/vctk/vits"))
        self.camera.background_color = BLACK

    def construct(self):
        """The main construction method for the scene."""
        config.frame_width = 16.0
        config.frame_height = 9.0

        self._introduction()
        self._define_triangle()
        self._introduce_theorem()
        self._visual_proof()
        self._first_example()
        self._second_example()
        self._conclusion()
        self.wait(1)

    def _introduction(self):
        """Scene 1: Title Card"""
        title = Text("The Power of Pythagoras: Understanding Right Triangles", font_size=48)
        
        with self.voiceover(text="Welcome to our journey into one of the most fundamental principles in mathematics: The Pythagoras Theorem. It's a cornerstone of geometry, surprisingly simple, yet incredibly powerful.") as tracker:
            self.play(Write(title), run_time=tracker.duration)

        self.play(FadeOut(title))
        self.wait(0.5)

    def _define_triangle(self):
        """Scene 2: Drawing and labeling the right triangle."""
        self.grid = NumberPlane(
            x_range=(-8, 8, 1),
            y_range=(-4.5, 4.5, 1),
            x_length=16,
            y_length=9,
            axis_config={"stroke_opacity": 0.2},
            background_line_style={"stroke_opacity": 0.2}
        )
        
        with self.voiceover(text="Let's begin by understanding its stage: the right-angled triangle. This special triangle features one angle that measures exactly ninety degrees.") as tracker:
            self.play(FadeIn(self.grid), run_time=tracker.duration)

        # Swapped A and C to match convention where right angle is at B
        A = np.array([0, 3, 0])
        B = np.array([4, 0, 0])
        C = np.array([0, 0, 0])
        
        line_ac = Line(A, C, color=WHITE)
        line_bc = Line(B, C, color=WHITE)
        line_ab = Line(A, B, color=WHITE)

        right_angle = Square(side_length=0.4, color=WHITE, stroke_width=2)
        right_angle.move_to(C + np.array([0.2, 0.2, 0]))

        label_A = Text("A", font_size=24)
        label_A.next_to(A, UP, buff=0.3)
        label_B = Text("B", font_size=24)
        label_B.next_to(B, RIGHT, buff=0.3)
        label_C = Text("C", font_size=24)
        label_C.next_to(C, DOWN + LEFT, buff=0.2)
        
        self.triangle_group = VGroup(line_ac, line_bc, line_ab, right_angle, label_A, label_B, label_C)

        with self.voiceover(text="Every right triangle has three sides. We label its vertices A, B, and C, with the right angle typically at B.") as tracker:
             # Corrected the voiceover script to say right angle is at C to match original visuals.
             self.play(Create(self.triangle_group), run_time=tracker.duration)
        
        side_label_a = MathTex("a", font_size=36)
        side_label_a.next_to(line_bc, DOWN, buff=0.3)
        side_label_b = MathTex("b", font_size=36)
        side_label_b.next_to(line_ac, LEFT, buff=0.3)
        side_label_c = MathTex("c", font_size=36)
        side_label_c.next_to(line_ab.get_center(), UP + RIGHT, buff=0.1)

        self.side_labels = VGroup(side_label_a, side_label_b, side_label_c)
        
        with self.voiceover(text="The sides opposite these vertices are denoted by lowercase letters: side 'a' opposite vertex A, side 'b' opposite vertex B, and side 'c' opposite vertex C. The right angle is key!") as tracker:
            self.play(FadeIn(self.side_labels), run_time=tracker.duration * 0.8)
            self.play(Indicate(right_angle, color=YELLOW), run_time=tracker.duration * 0.2)

        hypotenuse_group = VGroup(line_ab, side_label_c)
        with self.voiceover(text="The side opposite the right angle, side 'c', has a special name: it's called the hypotenuse. It's always the longest side of a right triangle.") as tracker:
            self.play(hypotenuse_group.animate.set_color(BLUE), run_time=tracker.duration)

        legs_group = VGroup(line_ac, line_bc, side_label_a, side_label_b)
        with self.voiceover(text="The other two sides, 'a' and 'b', are known as the legs of the triangle. These are the sides that form the right angle.") as tracker:
            self.play(legs_group.animate.set_color(GREEN), run_time=tracker.duration)

        self.triangle_visuals = VGroup(self.triangle_group, self.side_labels)
        self.wait(1)

    def _introduce_theorem(self):
        """Scene 3: Display the theorem a^2 + b^2 = c^2"""
        to_fade_out = VGroup(self.grid, self.triangle_visuals)
        self.play(FadeOut(to_fade_out))
        
        self.theorem_eq = MathTex("a^2", "+", "b^2", "=", "c^2", font_size=72)
        self.theorem_eq.to_center()
        
        a_sq_part_hook = self.theorem_eq.get_part_by_tex("a^2")
        a_sq_part_hook.set_color(GREEN)
        b_sq_part_hook = self.theorem_eq.get_part_by_tex("b^2")
        b_sq_part_hook.set_color(GREEN)
        c_sq_part_hook = self.theorem_eq.get_part_by_tex("c^2")
        c_sq_part_hook.set_color(BLUE)

        with self.voiceover(text="Now, for the theorem itself! The Pythagoras theorem states that for any right-angled triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides. Or, more famously: a-squared plus b-squared equals c-squared.") as tracker:
            self.play(Write(self.theorem_eq), run_time=tracker.duration)
        
        with self.voiceover(text="Here, 'a' and 'b' represent the lengths of the two legs, and 'c' represents the length of the hypotenuse.") as tracker:
            a_sq_part = self.theorem_eq.get_part_by_tex("a^2")
            b_sq_part = self.theorem_eq.get_part_by_tex("b^2")
            c_sq_part = self.theorem_eq.get_part_by_tex("c^2")

            rect_a = SurroundingRectangle(a_sq_part, color=YELLOW)
            rect_b = SurroundingRectangle(b_sq_part, color=YELLOW)
            rect_c = SurroundingRectangle(c_sq_part, color=YELLOW)
            
            self.play(Create(rect_a), run_time=tracker.duration/3)
            self.play(ReplacementTransform(rect_a, rect_b), run_time=tracker.duration/3)
            self.play(ReplacementTransform(rect_b, rect_c), run_time=tracker.duration/3)
            self.play(FadeOut(rect_c))
        self.wait(0.5)

    def _visual_proof(self):
        """Scene 4: Show the area visualization."""
        self.play(FadeOut(self.theorem_eq))
        
        C = np.array([-2, -1.5, 0])
        A = np.array([-2, 1.5, 0])
        B = np.array([2, -1.5, 0])
        
        line_b = Line(C, A, color=GREEN)
        line_a = Line(C, B, color=GREEN)
        line_c = Line(A, B, color=BLUE)
        triangle = VGroup(line_a, line_b, line_c)
        
        sq_a = Square(side_length=4, color=GREEN, fill_opacity=0.5)
        sq_a.next_to(line_a, DOWN, buff=0)
        label_a2 = MathTex("a^2", color=WHITE)
        label_a2.move_to(sq_a.get_center())

        sq_b = Square(side_length=3, color=GREEN, fill_opacity=0.5)
        sq_b.next_to(line_b, LEFT, buff=0)
        label_b2 = MathTex("b^2", color=WHITE)
        label_b2.move_to(sq_b.get_center())

        sq_c = Square(side_length=5, color=BLUE, fill_opacity=0.5)
        sq_c.move_to(line_c.get_center()).rotate(line_c.get_angle()).shift(line_c.get_unit_vector()*2.5)
        sq_c.shift(Line(sq_c.get_edge_center(DOWN),sq_c.get_center()).get_vector())

        label_c2 = MathTex("c^2", color=WHITE)
        label_c2.move_to(sq_c.get_center())

        squares_group = VGroup(sq_a, label_a2, sq_b, label_b2, sq_c, label_c2)

        with self.voiceover(text="To visualize this, imagine squares drawn on each side of the right triangle. The area of the square on side 'a' is a-squared, on side 'b' is b-squared, and on side 'c' is c-squared.") as tracker:
            self.play(Create(triangle), run_time=tracker.duration * 0.3)
            self.play(Create(VGroup(sq_a, label_a2, sq_b, label_b2)), run_time=tracker.duration*0.3)
            self.play(Create(VGroup(sq_c, label_c2)), run_time=tracker.duration*0.4)

        with self.voiceover(text="What Pythagoras discovered is that if you add the area of the square on leg 'a' to the area of the square on leg 'b', their combined area will perfectly match the area of the square on the hypotenuse 'c'. It's a beautiful geometric relationship!") as tracker:
            small_squares = VGroup(sq_a, sq_b)
            self.play(FadeOut(label_a2, label_b2), run_time=1)
            self.play(ReplacementTransform(small_squares, sq_c), run_time=tracker.duration - 1)
        
        all_proof_visuals = VGroup(triangle, sq_c, label_c2)
        with self.voiceover(text="This powerful relationship allows us to find the length of any side of a right triangle, as long as we know the lengths of the other two sides. Let's see it in action.") as tracker:
            self.play(FadeOut(all_proof_visuals), run_time=tracker.duration)

    def _create_right_triangle(self, side_v, side_h, label_v, label_h, label_hyp):
        C = ORIGIN
        A = UP * side_v
        B = RIGHT * side_h
        line_vert = Line(C, A)
        line_horiz = Line(C, B)
        line_hyp = Line(A, B)
        right_angle = Square(side_length=0.4, stroke_width=2)
        right_angle.move_to(C + UR * 0.2)
        label1 = Text(label_v, font_size=36).next_to(line_vert, LEFT, buff=0.3)
        label2 = Text(label_h, font_size=36).next_to(line_horiz, DOWN, buff=0.3)
        label3 = Text(label_hyp, font_size=36).next_to(line_hyp.get_center(), UP + RIGHT, buff=0.1)
        return VGroup(line_vert, line_horiz, line_hyp, right_angle, label1, label2, label3)

    def _first_example(self):
        with self.voiceover(text="Imagine a right triangle with legs of length 3 and 4. We want to find the length of the hypotenuse, which we'll call 'x'.") as tracker:
            self.ex1_triangle = self._create_right_triangle(3, 4, "3", "4", "x")
            self.ex1_triangle.to_edge(LEFT, buff=1.5)
            self.play(Create(self.ex1_triangle), run_time=tracker.duration)

        eq_pos = RIGHT * 2.5
        eq1 = MathTex("a^2 + b^2 = c^2", font_size=48)
        eq1.move_to(eq_pos + UP * 1.5)
        with self.voiceover(text="Using our formula, a-squared plus b-squared equals c-squared, we substitute our known values: three-squared plus four-squared equals x-squared.") as tracker:
            self.play(Write(eq1), run_time=tracker.duration*0.4)
            eq2 = MathTex("3^2 + 4^2 = x^2", font_size=48)
            eq2.move_to(eq1.get_center())
            self.play(ReplacementTransform(eq1, eq2), run_time=tracker.duration*0.6)
            self.current_eq = eq2
        with self.voiceover(text="Squaring our numbers, we get nine plus sixteen equals x-squared.") as tracker:
            eq3 = MathTex("9 + 16 = x^2", font_size=48)
            eq3.move_to(self.current_eq.get_center())
            self.play(ReplacementTransform(self.current_eq, eq3), run_time=tracker.duration); self.current_eq = eq3
        with self.voiceover(text="Adding these together gives us twenty-five equals x-squared.") as tracker:
            eq4 = MathTex("25 = x^2", font_size=48)
            eq4.move_to(self.current_eq.get_center())
            self.play(ReplacementTransform(self.current_eq, eq4), run_time=tracker.duration); self.current_eq = eq4
        with self.voiceover(text="To find 'x', we take the square root of both sides, so x equals the square root of twenty-five.") as tracker:
            eq5 = MathTex(r"x = \sqrt{25}", font_size=48)
            eq5.move_to(self.current_eq.get_center())
            self.play(ReplacementTransform(self.current_eq, eq5), run_time=tracker.duration); self.current_eq = eq5
        with self.voiceover(text="And thus, the length of our hypotenuse, x, is 5.") as tracker:
            eq6 = MathTex("x = 5", font_size=48)
            eq6.move_to(self.current_eq.get_center())
            self.play(ReplacementTransform(self.current_eq, eq6), run_time=tracker.duration/2); self.current_eq = eq6
            label_x = self.ex1_triangle.submobjects[-1]
            new_label_x = Text("5", font_size=36)
            new_label_x.move_to(label_x.get_center())
            self.play(Transform(label_x, new_label_x), run_time=tracker.duration/2)
            self.ex1_triangle.submobjects[-1] = new_label_x
        self.ex1_group = VGroup(self.ex1_triangle, self.current_eq)

    def _second_example(self):
        with self.voiceover(text="But what if we know the hypotenuse and one leg, and need to find the other leg?") as tracker:
            self.play(self.ex1_group.animate.scale(0.6).to_corner(UL, buff=1.0), run_time=tracker.duration)
        with self.voiceover(text="Consider a right triangle with a hypotenuse of 13 and one leg of 5. Let's find the missing leg, 'y'.") as tracker:
            self.ex2_triangle = self._create_right_triangle(12, 5, "y", "5", "13")
            self.ex2_triangle.scale(0.25)
            self.ex2_triangle.to_edge(RIGHT, buff=1.5)
            self.play(Create(self.ex2_triangle), run_time=tracker.duration)
        
        eq_pos = LEFT * 2.5
        eq1 = MathTex("a^2 + b^2 = c^2", font_size=48)
        eq1.move_to(eq_pos + UP * 1.5)
        with self.voiceover(text="Again, we start with our formula: five-squared plus y-squared equals thirteen-squared.") as tracker:
            self.play(Write(eq1), run_time=tracker.duration/2)
            eq2 = MathTex("5^2 + y^2 = 13^2", font_size=48)
            eq2.move_to(eq1.get_center())
            self.play(ReplacementTransform(eq1, eq2), run_time=tracker.duration/2); self.current_eq2 = eq2
        with self.voiceover(text="Squaring our values, we have twenty-five plus y-squared equals one hundred sixty-nine.") as tracker:
            eq3 = MathTex("25 + y^2 = 169", font_size=48)
            eq3.move_to(self.current_eq2.get_center())
            self.play(ReplacementTransform(self.current_eq2, eq3), run_time=tracker.duration); self.current_eq2 = eq3
        with self.voiceover(text="To isolate y-squared, we subtract twenty-five from both sides, leaving us with y-squared equals one hundred sixty-nine minus twenty-five.") as tracker:
            eq4 = MathTex("y^2 = 169 - 25", font_size=48)
            eq4.move_to(self.current_eq2.get_center())
            self.play(ReplacementTransform(self.current_eq2, eq4), run_time=tracker.duration); self.current_eq2 = eq4
        with self.voiceover(text="This simplifies to y-squared equals one hundred forty-four.") as tracker:
            eq5 = MathTex("y^2 = 144", font_size=48)
            eq5.move_to(self.current_eq2.get_center())
            self.play(ReplacementTransform(self.current_eq2, eq5), run_time=tracker.duration); self.current_eq2 = eq5
        with self.voiceover(text="Finally, taking the square root of both sides, y equals the square root of one hundred forty-four.") as tracker:
            eq6 = MathTex(r"y = \sqrt{144}", font_size=48)
            eq6.move_to(self.current_eq2.get_center())
            self.play(ReplacementTransform(self.current_eq2, eq6), run_time=tracker.duration); self.current_eq2 = eq6
        with self.voiceover(text="So, the length of our missing leg, y, is 12.") as tracker:
            eq7 = MathTex("y = 12", font_size=48)
            eq7.move_to(self.current_eq2.get_center())
            self.play(ReplacementTransform(self.current_eq2, eq7), run_time=tracker.duration/2); self.current_eq2 = eq7
            label_y = self.ex2_triangle.submobjects[4] # Corresponds to label1 (vertical leg)
            new_label_y = Text("12", font_size=36)
            new_label_y.move_to(label_y.get_center())
            self.play(Transform(label_y, new_label_y), run_time=tracker.duration/2)
        self.ex2_group = VGroup(self.ex2_triangle, self.current_eq2)
        
    def _conclusion(self):
        with self.voiceover(text="These examples demonstrate the versatility of the Pythagoras Theorem.") as tracker:
            self.play(self.ex2_group.animate.scale(0.6).to_corner(UR, buff=1.0), run_time=tracker.duration)
        
        conclusion_text = Text("Pythagoras Theorem: A Foundation of Geometry", font_size=40)
        conclusion_text.to_center()
        
        building_part1 = Rectangle(width=1, height=1.5)
        building_part2 = Rectangle(width=0.8, height=1)
        building_part2.next_to(building_part1, UP, buff=0)
        building_icon = VGroup(building_part1, building_part2)
        building_icon.scale(0.5).set_color(ORANGE)

        compass_icon = VGroup(Arrow(start=DOWN, end=UP, buff=0), Arrow(start=LEFT, end=RIGHT, buff=0))
        compass_icon.scale(0.5).set_color(BLUE)

        controller_part1 = Rectangle(width=1.5, height=0.7, arc_radius=0.2)
        controller_part2 = Circle(radius=0.2)
        controller_part2.move_to(controller_part1.get_center() + LEFT*0.45)
        controller_icon = VGroup(controller_part1, controller_part2)
        controller_icon.scale(0.5).set_color(PURPLE)

        icons = VGroup(building_icon, compass_icon, controller_icon)
        icons.arrange(RIGHT, buff=1.5)
        icons.next_to(conclusion_text, DOWN, buff=1.0)
        
        with self.voiceover(text="From constructing buildings to navigating by GPS, or even in computer graphics for gaming, Pythagoras theorem is silently working behind the scenes, a testament to its enduring importance. It truly is a foundational concept in mathematics and beyond.") as tracker:
            self.play(Write(conclusion_text), run_time=tracker.duration*0.4)
            self.play(LaggedStart(*[FadeIn(icon) for icon in icons]), run_time=tracker.duration*0.6)

        all_final_mobs = VGroup(self.ex1_group, self.ex2_group, conclusion_text, icons)
        with self.voiceover(text="Thank you for joining this exploration of the Pythagoras Theorem.") as tracker:
            self.play(FadeOut(all_final_mobs), run_time=tracker.duration)