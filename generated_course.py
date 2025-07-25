from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.coqui import CoquiService

class Generated_Course(VoiceoverScene):
    """An educational animation on Arithmetic Progressions."""
    def setup(self):
        """Set up the scene with voiceover and background color."""
        self.set_speech_service(CoquiService())
        self.camera.background_color = BLACK

    def construct(self):
        """The main construction method for the animation."""
        config.frame_width = 16.0
        config.frame_height = 9.0

        self._scene_01_intro() # Actions 1
        self._scene_02_define_ap() # Actions 2-6
        self._scene_03_derive_nth_term() # Actions 7-9
        self._scene_04_example_nth_term() # Actions 10-11
        self._scene_05_sum_intro() # Actions 12-13
        self._scene_06_sum_formulas() # Actions 14-15
        self._scene_07_example_sum() # Actions 16-17
        self._scene_08_real_world_and_summary() # Actions 18-19
        self._scene_09_outro() # Action 20

        self.wait(1)

    def _scene_01_intro(self):
        """Action 1: Title card."""
        narration = """Welcome! Today, we're unlocking the secrets of one of the most fundamental concepts in sequences: the Arithmetic Progression. Understanding these patterns is key to solving a wide range of problems, from simple puzzles to complex engineering challenges."""
        title = Text("Understanding Arithmetic Progressions", font_size=48)

        bg_seq = VGroup(*[MathTex(f"{i*2}") for i in range(1, 8)])
        bg_seq.arrange(RIGHT, buff=1.0)
        bg_seq.set_opacity(0.2)

        with self.voiceover(text=narration) as tracker:
            self.play(FadeIn(bg_seq, shift=UP), run_time=1.5)
            self.play(ScaleIn(title), run_time=2.0)
            self.wait(tracker.duration - 3.5 if tracker.duration > 3.5 else 1)

        self.play(FadeOut(title), FadeOut(bg_seq))

    def _scene_02_define_ap(self):
        """Actions 2-6: Define AP, common difference, and first term."""
        narration_2 = """Let's start with a simple sequence: 2, 4, 6, 8, 10. Can you spot the pattern? Each number increases by the same amount to get to the next."""
        num_mobs = [MathTex(str(n)) for n in [2, 4, 6, 8, 10]]
        dots = MathTex(r"...")
        example_sequence_terms = VGroup(*num_mobs, dots)
        example_sequence_terms.arrange(RIGHT, buff=1.0)
        example_sequence_terms.to_center()

        with self.voiceover(text=narration_2) as tracker:
            self.play(Write(example_sequence_terms), run_time=tracker.duration)

        narration_3 = """Indeed, you add 2 to each term to get the next one. This constant value, which we add or subtract, is crucial."""
        arrows = VGroup()
        labels = VGroup()
        for i in range(len(num_mobs) - 1):
            arrow = CurvedArrow(num_mobs[i].get_top(), num_mobs[i+1].get_top(), angle=-PI/2)
            arrows.add(arrow)
            label = MathTex(r"+2", font_size=36)
            label.next_to(arrow, UP, buff=0.2)
            labels.add(label)

        with self.voiceover(text=narration_3) as tracker:
            self.play(LaggedStart(*[Create(arrow) for arrow in arrows], lag_ratio=0.5), run_time=tracker.duration * 0.5)
            self.play(LaggedStart(*[Write(label) for label in labels], lag_ratio=0.5), run_time=tracker.duration * 0.5)

        narration_4 = """This unchanging difference between consecutive terms is known as the 'Common Difference,' and we denote it with the letter 'd'. In our example, d equals 2. Arithmetic progressions are defined by this consistent 'd'."""
        common_diff_label = Text("Common Difference (d)", font_size=36, color=YELLOW)
        common_diff_label.next_to(labels[1], UP, buff=1.0)

        with self.voiceover(text=narration_4) as tracker:
            self.play(Indicate(labels, color=YELLOW, scale_factor=1.2), run_time=tracker.duration * 0.5)
            self.play(Write(common_diff_label), run_time=tracker.duration * 0.5)
        self.wait(1)

        example_ap_group = VGroup(example_sequence_terms, arrows, labels, common_diff_label)
        
        narration_5 = """Every arithmetic progression starts somewhere. We call the very first number in our sequence the 'First Term'."""
        general_sequence = MathTex(r"a_1, a_2, a_3, \dots, a_n, \dots", font_size=40)
        general_sequence.to_edge(RIGHT, buff=2.0)

        with self.voiceover(text=narration_5) as tracker:
            self.play(example_ap_group.animate.scale(0.8).to_edge(LEFT, buff=2.0), run_time=1.0)
            self.play(Write(general_sequence), run_time=tracker.duration - 1.0 if tracker.duration > 1.0 else 0.5)
        
        narration_6 = """The first term is typically denoted by 'a', or sometimes 'a sub 1'. So, in our 2, 4, 6, 8... sequence, 'a' is 2. The term 'a sub n' simply refers to any term at position 'n' in the sequence."""
        a1_hook = general_sequence.get_part_by_tex("a_1")
        first_term_label = Text("First Term (a)", font_size=36, color=CYAN)
        first_term_label.next_to(a1_hook, DOWN, buff=1.0)

        with self.voiceover(text=narration_6) as tracker:
            self.play(Indicate(a1_hook, color=CYAN, scale_factor=1.2), run_time=tracker.duration * 0.4)
            self.play(Write(first_term_label), run_time=tracker.duration * 0.6)
        
        self.wait(1)
        self.play(FadeOut(VGroup(example_ap_group, general_sequence, first_term_label)))

    def _scene_03_derive_nth_term(self):
        """Actions 7-9: Derive the formula for the nth term."""
        narration_7_8 = """Now, how can we find any term in an arithmetic progression without listing them all out? Let's generalize. The first term is 'a'. The second is 'a plus d'. The third is 'a plus two d'. Notice the pattern? For the 'nth' term, 'd' is added 'n minus one' times."""
        general_sequence = MathTex(r"a_1, a_2, a_3, \dots, a_n", font_size=48)
        general_sequence.to_edge(UP, buff=1.5)
        
        expanded_terms = VGroup(
            MathTex(r"a_1"),
            MathTex(r"a_1 + d"),
            MathTex(r"a_1 + 2d"),
            MathTex(r"\dots"),
            MathTex(r"a_1 + (n-1)d")
        )
        expanded_terms.arrange(RIGHT, buff=1.0)
        expanded_terms.next_to(general_sequence, DOWN, buff=1.5)

        with self.voiceover(text=narration_7_8) as tracker:
            self.play(Write(general_sequence), run_time=tracker.duration * 0.2)
            self.play(LaggedStart(*[FadeIn(term, shift=UP) for term in expanded_terms]), lag_ratio=0.5, run_time=tracker.duration * 0.5)
            an_hook = general_sequence.get_part_by_tex("a_n")
            target_term_hook = expanded_terms[-1]
            arrow_to_an = Arrow(target_term_hook.get_bottom(), an_hook.get_top(), buff=0.2)
            self.play(Create(arrow_to_an), run_time=tracker.duration * 0.3)
        self.wait(1)

        narration_9 = """This leads us to the general formula for the 'nth' term of an arithmetic progression: 'a sub n equals a plus the quantity n minus one, times d'. Here, 'a sub n' is the term you want to find, 'a' is the first term, 'n' is its position, and 'd' is the common difference."""
        self.an_formula = MathTex(r"a_n = a + (n-1)d", font_size=60)
        formula_group = VGroup(general_sequence, expanded_terms, arrow_to_an)

        with self.voiceover(text=narration_9) as tracker:
            self.play(ReplacementTransform(formula_group, self.an_formula), run_time=2.0)
            self.wait(0.5)
            a_part = self.an_formula.get_part_by_tex("a")
            n_part = self.an_formula.get_part_by_tex("n")
            d_part = self.an_formula.get_part_by_tex("d")
            self.play(Indicate(a_part, color=CYAN), run_time=1.0)
            self.play(Indicate(n_part, color=YELLOW), run_time=1.0)
            self.play(Indicate(d_part, color=GREEN), run_time=1.0)
        self.wait(1)

    def _scene_04_example_nth_term(self):
        """Actions 10-11: Example of finding the nth term."""
        narration_10 = """Let's use this formula! Consider the sequence 5, 8, 11, 14, and so on. Here, the first term 'a' is 5, and the common difference 'd' is 3."""
        narration_11 = """What if we need to find the 8th term of this sequence? Using our formula, we substitute: 'a sub 8' equals 5 plus '8 minus 1' times 3. That simplifies to 5 plus 7 times 3, which is 5 plus 21. So, the 8th term, 'a sub 8', is 26."""
        
        self.play(self.an_formula.animate.scale(0.7).to_corner(UP + RIGHT, buff=1.5))

        example_seq = MathTex(r"5, 8, 11, 14, \dots", font_size=48)
        example_seq.to_edge(LEFT, buff=2.0)
        
        a_val = MathTex(r"a=5", color=CYAN, font_size=48)
        d_val = MathTex(r"d=3", color=GREEN, font_size=48)
        vals = VGroup(a_val, d_val)
        vals.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        vals.next_to(example_seq, RIGHT, buff=2.0)

        with self.voiceover(text=narration_10) as tracker:
            self.play(Write(example_seq), run_time=tracker.duration * 0.5)
            self.play(FadeIn(vals), run_time=tracker.duration * 0.5)
        self.wait(0.5)

        question = Text("Find the 8th term (a_8)?", font_size=40)
        question.to_edge(LEFT, buff=2.0)
        question.shift(DOWN * 1.5)

        calc1 = MathTex(r"a_8 = 5 + (8-1)3", font_size=48)
        calc1.next_to(question, DOWN, buff=1.0, aligned_edge=LEFT)
        calc2 = MathTex(r"a_8 = 5 + 7 \times 3", font_size=48)
        calc2.move_to(calc1, aligned_edge=LEFT)
        calc3 = MathTex(r"a_8 = 5 + 21 = 26", font_size=48)
        calc3.move_to(calc2, aligned_edge=LEFT)

        with self.voiceover(text=narration_11) as tracker:
            self.play(Write(question), run_time=1.5)
            self.play(Write(calc1), run_time=2.0)
            self.wait(0.5)
            self.play(TransformMatchingTex(calc1, calc2), run_time=2.0)
            self.wait(0.5)
            self.play(TransformMatchingTex(calc2, calc3), run_time=2.0)
            
        calc_final = MathTex(r"a_8 = 26", font_size=48, color=YELLOW)
        calc_final.move_to(calc3)
        highlight_box = SurroundingRectangle(calc_final, color=YELLOW, buff=0.2)
        self.play(TransformMatchingTex(calc3, calc_final), Create(highlight_box))
        self.wait(2)
        self.play(FadeOut(VGroup(self.an_formula, example_seq, vals, question, calc_final, highlight_box)))

    def _scene_05_sum_intro(self):
        """Actions 12-13: Introduce the concept of summing an AP."""
        narration_11_again = """Beyond finding individual terms, what if we need to sum up all the numbers in an arithmetic progression? Imagine adding hundreds or thousands of terms."""
        narration_12 = """A clever trick, famously attributed to young Gauss, involves pairing the first and last terms, the second and second-to-last, and so on. Each pair sums to the same value, and you have 'n over 2' such pairs."""

        gen_seq = MathTex(r"a_1, a_2, \dots, a_n", font_size=48)
        gen_seq.to_center()
        term_count_label = MathTex(r"n \text{ terms}", color=YELLOW)
        term_count_label.next_to(gen_seq, DOWN, buff=1.0)
        
        with self.voiceover(text=narration_11_again) as tracker:
            self.play(Write(gen_seq), run_time=tracker.duration * 0.5)
            self.play(FadeIn(term_count_label, shift=UP), run_time=tracker.duration * 0.5)
        self.wait(1)
        self.play(FadeOut(gen_seq), FadeOut(term_count_label))

        gauss_seq = MathTex(r"1, 2, 3, \dots, 98, 99, 100", font_size=48)
        gauss_seq.to_edge(UP, buff=1.5)
        
        with self.voiceover(text=narration_12) as tracker:
            self.play(Write(gauss_seq), run_time=2.0)
            rt = (tracker.duration - 2.0) / 2
            
            term1_hook = gauss_seq.get_part_by_tex("1")
            term100_hook = gauss_seq.get_part_by_tex("100")
            arc1 = ArcBetweenPoints(term1_hook.get_bottom(), term100_hook.get_bottom(), angle=-PI)
            label1 = MathTex(r"101", font_size=36, color=YELLOW)
            label1.next_to(arc1, DOWN, buff=0.5)
            
            term2_hook = gauss_seq.get_part_by_tex("2")
            term99_hook = gauss_seq.get_part_by_tex("99")
            arc2 = ArcBetweenPoints(term2_hook.get_bottom(), term99_hook.get_bottom(), angle=-PI*0.9)
            label2 = MathTex(r"101", font_size=36, color=YELLOW)
            label2.next_to(arc2, DOWN, buff=0.5)

            self.play(Create(arc1), Write(label1), run_time=rt)
            self.play(Create(arc2), Write(label2), run_time=rt)

        self.wait(2)
        self.play(FadeOut(VGroup(gauss_seq, arc1, label1, arc2, label2)))

    def _scene_06_sum_formulas(self):
        """Actions 14-15: Present the two formulas for the sum of an AP."""
        narration_13 = """This brings us to the sum formula: 'S sub n equals n over 2, multiplied by the quantity 'a' plus 'a sub n'. Here, 'S sub n' is the sum, 'n' is the number of terms, 'a' is the first term, and 'a sub n' is the last term in the sum."""
        self.sum_formula_1 = MathTex(r"S_n = \frac{n}{2}(a + a_n)", font_size=60)
        self.sum_formula_1.to_center()

        with self.voiceover(text=narration_13) as tracker:
            self.play(Write(self.sum_formula_1), run_time=2.0)
            self.wait(0.2)
            n_parts = self.sum_formula_1.get_parts_by_tex("n")
            a_part = self.sum_formula_1.get_part_by_tex("a")
            an_part = self.sum_formula_1.get_part_by_tex("a_n")
            self.play(Indicate(n_parts, color=YELLOW), run_time=1.5)
            self.play(Indicate(a_part, color=CYAN), run_time=1.5)
            self.play(Indicate(an_part, color=ORANGE), run_time=1.5)
        self.wait(0.5)

        narration_14 = """Alternatively, if you don't know the last term, you can substitute the 'a sub n' formula into the sum formula, giving us 'S sub n equals n over 2, multiplied by the quantity '2a' plus 'n minus one, times d'."""
        self.sum_formula_2 = MathTex(r"S_n = \frac{n}{2}(2a + (n-1)d)", font_size=60)
        self.sum_formula_2.next_to(self.sum_formula_1, DOWN, buff=1.5)
        self.arrow_sum_deriv = CurvedArrow(self.sum_formula_1.get_corner(DR), self.sum_formula_2.get_corner(UR), angle=-PI/3)

        with self.voiceover(text=narration_14) as tracker:
            self.play(Write(self.sum_formula_2), Create(self.arrow_sum_deriv), run_time=tracker.duration)
        self.wait(1)

    def _scene_07_example_sum(self):
        """Actions 16-17: Example of calculating the sum."""
        self.formulas_group = VGroup(self.sum_formula_1, self.sum_formula_2, self.arrow_sum_deriv)
        self.play(self.formulas_group.animate.scale(0.6).to_corner(UP + RIGHT, buff=1.5))
        
        narration_15 = """Let's calculate the sum of the first 5 terms of the sequence 3, 7, 11, 15, 19. Here, 'a' is 3, 'd' is 4, 'n' is 5, and 'a sub n' (the 5th term) is 19."""
        example_seq = MathTex(r"3, 7, 11, 15, 19", font_size=48)
        example_seq.to_edge(UP, buff=1.5)

        vals = VGroup(
            MathTex(r"a=3", color=CYAN, font_size=36),
            MathTex(r"d=4", color=GREEN, font_size=36),
            MathTex(r"n=5", color=YELLOW, font_size=36),
            MathTex(r"a_5=19", color=ORANGE, font_size=36)
        )
        vals.arrange(RIGHT, buff=1.0)
        vals.next_to(example_seq, DOWN, buff=1.0)

        with self.voiceover(text=narration_15) as tracker:
            self.play(Write(example_seq), run_time=tracker.duration * 0.4)
            self.play(Write(vals), run_time=tracker.duration * 0.6)

        narration_16 = """Using our first sum formula, 'S sub 5' equals 5 over 2, times the quantity 3 plus 19. That's 5 over 2 times 22, which is 5 times 11. Therefore, the sum of the first 5 terms is 55."""
        calc_start = MathTex(r"S_5 = \frac{5}{2}(3 + 19)", font_size=48)
        calc_start.next_to(vals, DOWN, buff=1.5)
        calc_mid = MathTex(r"S_5 = \frac{5}{2}(22)", font_size=48)
        calc_mid.move_to(calc_start, aligned_edge=LEFT)
        calc_end = MathTex(r"S_5 = 5 \times 11 = 55", font_size=48)
        calc_end.move_to(calc_start, aligned_edge=LEFT)
        
        with self.voiceover(text=narration_16) as tracker:
            self.play(Write(calc_start), run_time=tracker.duration / 3)
            self.play(TransformMatchingTex(calc_start, calc_mid), run_time=tracker.duration / 3)
            self.play(TransformMatchingTex(calc_mid, calc_end), run_time=tracker.duration / 3)
        
        final_answer = MathTex(r"S_5 = 55", font_size=48, color=YELLOW)
        final_answer.move_to(calc_end)
        highlight_box = SurroundingRectangle(final_answer, color=YELLOW, buff=0.2)

        self.play(TransformMatchingTex(calc_end, final_answer))
        self.play(Create(highlight_box))
        self.wait(2)
        self.play(FadeOut(VGroup(self.formulas_group, example_seq, vals, final_answer, highlight_box)))

    def _scene_08_real_world_and_summary(self):
        """Actions 18-19: Real-world application and summary."""
        narration_17 = """Arithmetic progressions appear everywhere! From the pricing structure of certain products that increase by a fixed amount, to the height of steps on a staircase, or even the growth of investments with simple interest."""
        narration_18 = """In summary, an arithmetic progression is a sequence where each term differs from the previous by a constant 'common difference', 'd'. We have powerful formulas to find any 'nth' term, 'a sub n equals a plus n minus one d', and to efficiently calculate the sum of terms, 'S sub n equals n over 2 times a plus a sub n'."""

        staircase = VGroup()
        for i in range(4):
            step = Rectangle(width=1.5, height=0.5, fill_color=BLUE, fill_opacity=0.7, stroke_width=2)
            step.move_to(DOWN * 1.5 + LEFT * 3.0)
            step.shift(UP * i * 0.5 + RIGHT * i * 1.5)
            label = Text(f"{(i + 1) * 20}ft", font_size=24)
            label.move_to(step.get_center())
            staircase.add(VGroup(step, label))

        with self.voiceover(text=narration_17) as tracker:
            self.play(Create(staircase), run_time=tracker.duration)
        self.wait(1)
        self.play(FadeOut(staircase))

        summary_title = Text("Arithmetic Progressions:", font_size=40, color=YELLOW)
        summary_title.to_edge(UP, buff=1.5)

        summary_points = VGroup(
            Text("- Constant Difference (d)", font_size=36),
            MathTex(r"- a_n = a + (n-1)d", font_size=42),
            MathTex(r"- S_n = \frac{n}{2}(a + a_n)", font_size=42)
        )
        summary_points.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        summary_points.next_to(summary_title, DOWN, buff=1.0)

        with self.voiceover(text=narration_18) as tracker:
            self.play(Write(summary_title), run_time=tracker.duration * 0.2)
            self.play(LaggedStart(*[FadeIn(point, shift=RIGHT) for point in summary_points]), lag_ratio=0.7, run_time=tracker.duration * 0.8)
        self.wait(2)
        self.play(FadeOut(VGroup(summary_title, summary_points)))

    def _scene_09_outro(self):
        """Action 20: Concluding message."""
        narration_19 = """Mastering arithmetic progressions is a vital step in your mathematical journey, providing a solid foundation for more complex sequence and series concepts. Thank you for watching!"""
        outro_text = Text("A Fundamental Building Block in Mathematics", font_size=40)
        
        with self.voiceover(text=narration_19) as tracker:
            self.play(Write(outro_text), run_time=tracker.duration)
        
        self.wait(2)
        self.play(FadeOut(outro_text))