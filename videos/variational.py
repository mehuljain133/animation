from manimlib.imports import *


class EQScene(Scene):
    def construct(self):
        eq = TexMobject(self.eq)
        eq.scale(2)
        self.play(Write(eq))
        self.wait()


class Intro(Scene):
    def construct(self):
        axes = Axes(
            x_min=-2,
            x_max=4,
            y_min=-2,
            y_max=4,
            number_line_config={"include_tip": False}
        )

        f = FunctionGraph(
            self.func,
            x_min=-2,
            x_max=4
        )

        s = [-0.904, 0.904, 3.528]

        lbl = TexMobject("f(x)", color=YELLOW).move_to(f, RIGHT)
        xlbl = TexMobject("x").shift(4.5 * RIGHT)
        ylbl = TexMobject("y").shift(4.5 * UP)

        lines = VGroup(*[self.get_lines(i) for i in s])
        graph = VGroup(axes, f, lbl, xlbl, ylbl)

        grp = VGroup(graph, lines)
        grp.scale(0.9)
        grp.move_to(3 * LEFT)

        self.play(Write(graph))
        self.wait()

        head1 = TextMobject("Stationary Points", color=GOLD_B)
        head1.shift(3.5 * RIGHT + 3 * UP)
        head1.scale(1.25)

        self.play(Write(head1))

        eq1 = TexMobject("f'(x) = 0")
        eq1.scale(1)
        eq1.shift(3.5 * RIGHT + 1.5 * UP)

        self.wait()

        brect1 = BackgroundRectangle(
            eq1, buff=0.25, stroke_opacity=1, fill_opacity=0, stroke_width=4, color=BLUE)

        self.play(Write(eq1))
        self.play(Write(brect1), Write(lines))
        self.wait()

        head2 = TextMobject("Local min/max", color=GREEN)
        head2.shift(3.5 * RIGHT + 1 * DOWN)
        head2.scale(1.25)

        eq2 = TexMobject(r"\text{sign of } f''(x)")
        eq2.shift(3.5 * RIGHT + 2.5 * DOWN)

        brect2 = BackgroundRectangle(
            eq2, buff=0.25, stroke_opacity=1, fill_opacity=0, stroke_width=4, color=PURPLE)

        self.play(Write(head2))
        self.play(Write(brect2), Write(eq2))
        self.wait()

    def func(self, x):
        return x * np.sin(np.cos(x)) + 2

    def get_lines(self, point):
        ret = VGroup()
        ret.add(DashedLine(ORIGIN, self.func(point) * UP,
                           dash_length=0.1, stroke_opacity=0.7).shift(point * RIGHT))
        ret.add(Line(0.75 * LEFT, 0.75 * RIGHT,
                     color=BLUE).shift([point, self.func(point), 0]))

        return ret


class Functional(Scene):
    def construct(self):
        eq1 = TexMobject("D(f(x))", tex_to_color_map={
                         "f": RED, "D": BLUE, "x": GREEN})
        eq1.scale(3)

        eq2 = TexMobject("D(f)", tex_to_color_map={
                         "f": RED, "D": BLUE, "x": GREEN})
        eq2.scale(3)

        self.play(Write(eq1))
        self.wait()

        self.play(Transform(eq1, eq2))
        self.play(eq1.scale, 1.5/3)
        self.play(eq1.shift, 3 * UP)

        axes = Axes(
            x_min=-3,
            x_max=3,
            y_min=-2,
            y_max=2,
            number_line_config={"include_tip": False}
        )

        tracker = ValueTracker(-1)

        func = ParametricFunction(
            self.f_r(theta=PI/4), color=RED, t_min=-2, t_max=2)
        func.add_updater(lambda x: x.become(
            ParametricFunction(
                self.f_r(theta=PI/4, alpha=np.sin(tracker.get_value())), color=RED, t_min=-2, t_max=2)
        ).shift(0.5 * DOWN))
        grp = VGroup(axes, func)
        grp.shift(0.5 * DOWN)

        p1 = Circle(radius=0.05, fill_opacity=1, color=YELLOW)
        p1.shift([-np.sqrt(2), -np.sqrt(2) - 0.5, 0])

        p2 = Circle(radius=0.05, fill_opacity=1, color=YELLOW)
        p2.shift([np.sqrt(2), np.sqrt(2) - 0.5, 0])

        lbl1 = TexMobject("A").move_to(p1).shift(0.5 * DOWN)
        lbl2 = TexMobject("B").move_to(p2).shift(0.5 * UP)

        points = VGroup(p1, p2, lbl1, lbl2)

        self.play(Write(points))
        self.wait()

        self.bring_to_back(grp)
        self.play(Write(grp))
        self.wait()

        self.play(tracker.increment_value, 8, rate_func=linear,
                  run_time=4*DEFAULT_ANIMATION_RUN_TIME)
        self.wait()

        head1 = TextMobject(r"Distance from \( A \) to \( B \) along \( f \)", tex_to_color_map={
                            r"\( f \)": RED, r"\( A \)": GREEN, r"\( B \)": GREEN})
        head1.scale(1.25)
        head1.shift(3 * UP + 1.75 * RIGHT)

        self.play(eq1.shift, 5 * LEFT)

        arrow = Arrow(4 * LEFT, 2.5 * LEFT, color=GOLD).shift(3 * UP)
        self.play(Write(arrow), FadeInFromDown(head1))

        self.wait()

    def f(self, x, alpha=0):
        return alpha * np.cos(PI/4 * x)

    def f_r(self, theta=PI/4, alpha=0):
        return lambda t: [
            t * np.cos(theta) - self.f(t, alpha=alpha) * np.sin(theta),
            t * np.sin(theta) + self.f(t, alpha=alpha) * np.cos(theta),
            0]

    def func(self, t):
        return [t - self.f(t), t + self.f(t), 0]


class Difference(Scene):
    def construct(self):
        t1 = TextMobject("Traditional Calculus", color=GOLD)
        t2 = TextMobject("Variational Calculus", color=PURPLE)

        t1.shift(3.5 * LEFT + 3 * UP)
        t2.shift(3.5 * RIGHT + 3 * UP)

        t1.scale(1.25)
        t2.scale(1.25)

        l1 = Line(6 * UP, 6 * DOWN)
        l2 = Line(10 * LEFT, 10 * RIGHT).shift(2 * UP)

        grp = VGroup(t1, t2, l1, l2)

        self.play(Write(grp))
        self.wait()

        f1 = TexMobject("f", color=RED)
        i1 = TexMobject(r"\mathbb{R}", color=YELLOW).shift(1.5 * LEFT)
        o1 = TexMobject(r"\mathbb{R}", color=YELLOW).shift(1.5 * RIGHT)

        a1 = Arrow(1.25 * LEFT, 0.25 * LEFT, color=GREEN)
        a2 = Arrow(0.25 * RIGHT, 1.25 * RIGHT, color=GREEN)

        eq1 = VGroup(f1, i1, o1, a1, a2)
        eq1.shift(3.5 * LEFT)
        eq1.scale(1.5)

        f2 = TexMobject("f", color=RED)
        i2 = TexMobject(r"f(x)", color=BLUE).shift(1.5 * LEFT)
        o2 = TexMobject(r"\mathbb{R}", color=YELLOW).shift(1.5 * RIGHT)

        a3 = Arrow(1 * LEFT, 0 * LEFT, color=GREEN)
        a4 = Arrow(0.25 * RIGHT, 1.25 * RIGHT, color=GREEN)

        eq2 = VGroup(f2, i2, o2, a3, a4)
        eq2.shift(3.5 * RIGHT)
        eq2.scale(1.5)

        self.play(Write(eq1))
        self.play(Write(eq2))
        self.wait()


class DistanceFunc(Scene):
    def construct(self):
        eq1 = TexMobject("D(f)", tex_to_color_map={
                         "f": RED, "D": BLUE, "x": GREEN})
        eq1.scale(1.5)
        eq1.shift(3 * UP + 5 * LEFT)
        head1 = TextMobject(r"Distance from \( A \) to \( B \) along \( f \)", tex_to_color_map={
                            r"\( f \)": RED, r"\( A \)": GREEN, r"\( B \)": GREEN})
        head1.scale(1.25)
        head1.shift(3 * UP + 1.75 * RIGHT)

        arrow = Arrow(4 * LEFT, 2.5 * LEFT, color=GOLD).shift(3 * UP)

        self.play(Write(eq1), Write(arrow), FadeInFromDown(head1))
        self.wait()

        axes = Axes(
            x_min=-3,
            x_max=3,
            y_min=-2,
            y_max=2,
            number_line_config={"include_tip": False}
        )

        tracker = ValueTracker(-1)

        func = ParametricFunction(
            self.f_r(theta=PI/4), color=RED, t_min=-2, t_max=2)
        func.add_updater(lambda x: x.become(
            ParametricFunction(
                self.f_r(theta=PI/4, alpha=np.sin(tracker.get_value())), color=RED, t_min=-2, t_max=2)
        ).shift(0.5 * DOWN))
        grp = VGroup(axes, func)
        grp.shift(0.5 * DOWN)

        p1 = Circle(radius=0.05, fill_opacity=1, color=YELLOW)
        p1.shift([-np.sqrt(2), -np.sqrt(2) - 0.5, 0])

        p2 = Circle(radius=0.05, fill_opacity=1, color=YELLOW)
        p2.shift([np.sqrt(2), np.sqrt(2) - 0.5, 0])

        lbl1 = TexMobject("A").move_to(p1).shift(0.5 * DOWN)
        lbl2 = TexMobject("B").move_to(p2).shift(0.5 * UP)

        points = VGroup(p1, p2, lbl1, lbl2)

        self.play(Write(points))
        self.wait()

        self.bring_to_back(grp)
        self.play(Write(grp))
        self.wait()

        self.play(tracker.increment_value, 1 + 3 * PI, rate_func=linear,
                  run_time=4*DEFAULT_ANIMATION_RUN_TIME)
        self.wait()

        f2 = ParametricFunction(
            self.f_r(theta=PI/4), color=RED, t_min=-2, t_max=2).shift(0.5 * DOWN)
        graph = VGroup(axes, f2, points)
        self.add(f2)
        self.remove(func)

        self.play(ApplyMethod(graph.shift, 3.5 * LEFT))
        eq2 = TexMobject(r"D(f) ", r"= \int_{ x_1 }^{ x_2 } \text{d}s", tex_to_color_map={
                         "f": RED, "D": BLUE, r"\text{d}s": GREEN, "_{ x_1 }": YELLOW, "^{ x_2 }": YELLOW})
        eq2.scale(1.25)
        eq2.shift(1.25 * UP + 3 * RIGHT)

        self.play(TransformFromCopy(eq1, eq2[:4]))
        self.play(FadeInFromDown(eq2[4:]))
        self.wait()

        eq3 = TexMobject(r"=", r"\int_{ x_1 }^{ x_2 } \sqrt{1 +f'(x)^2 }  \ \text{d}x", tex_to_color_map={
                         "_{ x_1 }": YELLOW, "^{ x_2 }": YELLOW, r"\text{d}x": GREEN})
        eq3.scale(1)
        eq3.shift(1 * DOWN + 3 * RIGHT)

        self.play(FadeInFromDown(eq3))
        self.wait()

        rect = BackgroundRectangle(eq3[1:], stroke_width=DEFAULT_STROKE_WIDTH,
                                   stroke_opacity=1, color=GOLD, fill_opacity=0, buff=0.1)

        self.play(Write(rect))

        txt = TextMobject("Minimize this", color=ORANGE)
        txt.next_to(rect, DOWN)

        self.play(Write(txt))
        self.wait()

    def f(self, x, alpha=0):
        return alpha * np.cos(PI/4 * x)

    def f_r(self, theta=PI/4, alpha=0):
        return lambda t: [
            t * np.cos(theta) - self.f(t, alpha=alpha) * np.sin(theta),
            t * np.sin(theta) + self.f(t, alpha=alpha) * np.cos(theta),
            0]

    def func(self, t):
        return [t - self.f(t), t + self.f(t), 0]


class Brac(Scene):
    def construct(self):
        br1 = ScreenRectangle(height=3, width=4).shift(3.5 * LEFT)
        br2 = ScreenRectangle(height=3, width=4).shift(3.5 * RIGHT)

        t1 = TextMobject("3blue1brown", color=BLUE).shift(
            3.5 * LEFT + 2.5 * UP).scale(1.5)
        t2 = TextMobject("VSauce", color=GREEN).shift(
            3.5 * RIGHT + 2.5 * UP).scale(1.5)

        self.play(Write(t1), Write(t2))
        self.play(Write(br1), Write(br2))
        self.wait()


class IntroToProblem(Scene):
    def construct(self):
        head = TextMobject("Variational Calculus",
                           color=GOLD).scale(1.5).shift(3 * UP)

        self.play(Write(head))
        self.wait()

        p1 = TextMobject(r"Find some function \( f \) such that:",
                         tex_to_color_map={r"\( f \)": RED})
        p1.shift(1 * UP)

        self.play(Write(p1))

        eq1 = TexMobject(r"I[f] = \int_{ x_1 }^{ x_2 } F({x}, f({x}), f'({x})) \ \text{d}x",  tex_to_color_map={
                         r"f": RED, "_{ x_1 }": YELLOW, "^{ x_2 }": YELLOW, r"\text{d}x": GREEN, r"{x}": BLUE, "I": BLUE, "F": PURPLE})
        eq1.scale(1.25)
        eq1.shift(0.5 * DOWN)
        self.play(Write(eq1))

        p2 = TextMobject(r"is stationary")
        p2.shift(2 * DOWN)
        self.play(Write(p2))
        self.wait()


class Proof(Scene):
    def construct(self):
        axes = Axes(
            x_min=-1,
            x_max=5,
            y_min=0,
            y_max=4,
            number_line_config={"include_tip": False}
        )

        func1 = ParametricFunction(
            self.f_r(alpha=1), color=TEAL, t_min=-2, t_max=2)
        func2 = ParametricFunction(
            self.f_r(alpha=0.6), color=RED, t_min=-2, t_max=2)
        func3 = ParametricFunction(
            self.f_r(alpha=0.2), color=TEAL, t_min=-2, t_max=2)

        p1 = Circle(radius=0.05, fill_opacity=1, color=YELLOW)
        p1.shift([-np.sqrt(3), -1, 0])

        p2 = Circle(radius=0.05, fill_opacity=1, color=YELLOW)
        p2.shift([np.sqrt(3), 1, 0])

        points = VGroup(p1, p2)
        f = VGroup(func1, func2, func3)
        f.shift(2.5 * RIGHT + 2.5 * UP)
        points.shift(2.5 * RIGHT + 2.5 * UP)

        l1 = DashedLine((-np.sqrt(3) + 2.5) * RIGHT,
                        (-np.sqrt(3) + 2.5) * RIGHT + 1.5 * UP,
                        dash_length=0.075, stroke_opacity=0.75)
        l2 = DashedLine((np.sqrt(3) + 2.5) * RIGHT,
                        (np.sqrt(3) + 2.5) * RIGHT + 3.5 * UP,
                        dash_length=0.075, stroke_opacity=0.75)

        eq1 = TexMobject("q(x)", color=RED).scale(0.75)
        eq1.move_to(p2).shift(0.75 * RIGHT)

        eq2 = TexMobject(r"q(x) + s \cdot \delta q(x)", color=TEAL).scale(0.75)
        eq2.move_to(func1).shift(1.5 * UP)

        everything = VGroup(axes, func1, func2, func3, l1, l2,
                            points, eq1, eq2).center().scale(1.5)

        self.play(Write(axes))
        self.play(Write(func2), Write(eq1))
        self.wait()

        self.play(Write(func3), Write(func1), Write(eq2))
        self.play(Write(points), Write(VGroup(l1, l2)))
        self.wait()

    def f(self, x, alpha=0):
        return alpha * np.cos(PI/4 * x)

    def f_r(self, theta=PI/6, alpha=0):
        return lambda t: [
            t * np.cos(theta) - self.f(t, alpha=alpha) * np.sin(theta),
            t * np.sin(theta) + self.f(t, alpha=alpha) * np.cos(theta),
            0]

    def func(self, t):
        return [t - self.f(t), t + self.f(t), 0]


class FEq(EQScene):
    CONFIG = {
        "eq": r"I[f] = \int_{ x_1 }^{ x_2 } F({x}, f({x}), f'({x})) \ \text{d}x"
    }


class EulerLagrangeScene(Scene):
    def get_eq(self):
        eqq = TexMobject(r"{{\partial F}", r" \over {\partial y}}", r" -\frac{d}{d x} {{\partial F} \over {\partial y'}}=0",
                         tex_to_color_map={r"y": GREEN})
        eqq.scale(1.25)

        eqq2 = TexMobject(r"{{\partial {F}} \over ", r"{\partial y}}", r" -\frac{d}{d x} {{\partial F} \over {\partial y'}}=0",
                          tex_to_color_map={r"{F}": YELLOW})
        eqq2.scale(1.25)

        eqq3 = TexMobject(r"{{\partial F} \over ", r"{\partial y}}", r" -\frac{d}{d x} ", r"{{\partial {F}} ", r"\over {\partial y'}}=0",
                          tex_to_color_map={r"{F}": YELLOW})
        eqq3.scale(1.25)

        eqq4 = TexMobject(r"{{\partial F} \over ", r"{\partial y}}", r" -\frac{d}{d x} ", r"{{\partial {F}} ", r"\over {\partial y'}}=0",
                          tex_to_color_map={r"x": BLUE})
        eqq4.scale(1.25)

        grp = VGroup()
        grp.add(eqq[1:], eqq2[:3], eqq3[-3:-2], eqq4[3])
        return grp


class EulerLagrange(EulerLagrangeScene):
    def construct(self):
        eq = self.get_eq()
        eq.scale(0.75)
        eq.shift([1.25, 0.75, 0])

        self.play(FadeIn(eq))
        self.wait()

        self.play(eq.shift, [-1.25, -0.75, 0])
        self.play(eq.scale, 1.5 * 1.333)
        self.wait()

        title = TextMobject("Euler-Lagrange Equation", color=GOLD)
        title.scale(1.5)
        title.shift(2.5 * UP)

        self.play(FadeInFromDown(title))
        self.wait()


class DistanceFunc2(EulerLagrangeScene):
    def construct(self):
        eq2 = TexMobject(r"D(y) ", r"=", r"\int_{ x_1 }^{ x_2 } \sqrt{1 +y'(x)^2 } ", r"\ \text{d}x", tex_to_color_map={
                         "y": GREEN, "D": BLUE, r"\text{d}s": GREEN, "_{ x_1 }": YELLOW, "^{ x_2 }": YELLOW}).scale(1.5)
        eq3 = TexMobject(r"F = ", tex_to_color_map={"F": YELLOW}).scale(1.5)
        eq3.shift(1.5 * LEFT)

        self.play(Write(eq2))
        self.wait()

        self.play(Transform(eq2[:8], eq3), Uncreate(eq2[-1]))
        self.wait()

        eq = self.get_eq()

        self.play(VGroup(*self.mobjects).center)
        self.play(VGroup(*self.mobjects).shift, 2.5 * UP)
        self.play(VGroup(*self.mobjects).scale, 0.75)
        self.wait()

        self.play(FadeIn(eq))
        self.wait()

        eq2 = self.get_eq2()

        self.play(Transform(eq, eq2))
        self.wait()

    def get_eq2(self):
        eqq = TexMobject(r"0", r" -\frac{d}{d x} {{\partial F} \over {\partial y'}}=0",
                         tex_to_color_map={r"y": GREEN})
        eqq.scale(1.25)

        eqq2 = TexMobject(r"0", r" -\frac{d}{d x} {{\partial F} \over {\partial y'}}=0",
                          tex_to_color_map={r"F": YELLOW})
        eqq2.scale(1.25)

        eqq4 = TexMobject(r"0", r" -\frac{d}{d x} ", r"{{\partial {F}} ", r"\over {\partial y'}}=0",
                          tex_to_color_map={r"x": BLUE})
        eqq4.scale(1.25)

        grp = VGroup()
        grp.add(eqq[1:], eqq2[:3], eqq4[2])
        return grp


class Wolfram(Scene):
    def construct(self):
        img = ImageMobject("./img/wolfram.png")
        img.scale(2.75)
        img.shift(1.25 * UP)

        self.play(ShowCreation(img))
        self.wait()

        rect1 = Rectangle(height=1, width=2, color=RED)
        rect1.shift(2.75 * LEFT + 0.75 * DOWN)

        eq1 = TexMobject("= 0", color=BLACK).scale(1.5)
        eq1.shift(0.75 * DOWN + 1 * LEFT)

        self.play(Write(rect1))
        self.play(Write(eq1))
        self.wait()

        eq2 = TexMobject(r"f''(x) = 0", tex_to_color_map={
                         r"f": RED, "x": BLUE})
        eq2.scale(1.5)
        eq2.shift(2.5 * DOWN + 3.5 * LEFT)

        self.play(FadeInFromDown(eq2))
        self.wait()

        eq3 = TexMobject(r"f(x) = c_0 + c_1 x",
                         tex_to_color_map={r"f": RED, "x": BLUE})
        eq3.scale(1.5)
        eq3.shift(2.5 * DOWN + 4 * RIGHT)

        arrow = Arrow(LEFT, RIGHT, color=GREEN)
        arrow.shift(2.5 * DOWN)

        self.play(Write(arrow))
        self.play(FadeInFromDown(eq3))
        self.wait()
