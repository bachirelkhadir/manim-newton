import sys
import os
import itertools as it
import numpy as np
from scipy import linalg
from scipy.stats import norm
from manim import *
config.max_files_cached = 10000
config.background_color = "#1f303e"
from helper_functions import *
from opt_parameters import *



DEBUG = config.quality == "low_quality"

COLOR_OPT = RED
COLOR_CURVE = BLUE
COLOR_TANGENT = YELLOW
COLOR_QUAD = MAROON_A

color_map = {
    "f'(x_0)": COLOR_TANGENT,
    "f'(x_k)": COLOR_TANGENT,
    r"\nabla f(x_k)": COLOR_TANGENT,
    "f''(x_k)": COLOR_QUAD,
    "f''(x_0)": COLOR_QUAD,
    r"\nabla^2 f(x_k)": COLOR_QUAD,
}

def run_newton(f, df, x0, num_iter=10000):
    xk = x0
    history = [x0]
    for k in range(num_iter):
        xk -= f(xk) / df(xk)
        history.append(xk)
    return history



xks_newton = run_newton(f, df, x0)

class GradientDescent1D(ZoomedScene, MovingCameraScene):
    NUM_BLACK_SCREENS = 0
    def wait(self, timeout=1):
        self.NUM_BLACK_SCREENS += 1
        print("Blackish Screen: ", self.NUM_BLACK_SCREENS)
        color = BLACK
        rect = Rectangle(fill_color=color, strole_color=color, fill_opacity=1).scale(100)
        super(GradientDescent1D, self).wait(timeout)

        if not DEBUG:
            self.add(rect)
            super(GradientDescent1D, self).wait(timeout)
            self.remove(rect)

    def __init__(self):
        config = {
            "zoom_factor": 0.4,
            "zoomed_display_height": 4,
            "zoomed_display_width": 6,
            "image_frame_stroke_width": 20,
            "zoomed_display_corner": UL,
            "zoomed_camera_config": {
                "default_frame_stroke_width": 3,
            },
        }
        super(GradientDescent1D, self).__init__(**config)

    def construct(self):
        self.add_str_f()
        self.wait()
        self.add_graph_f()
        self.wait()

        #####################
        # Show x star
        #####################
        dot_xstar = self.mark(xstar, label="x^*").set_color(COLOR_OPT)
        self.play(Write(dot_xstar))
        self.add(dot_xstar)
        self.wait()
        dot_xstar.set_opacity(.2)
        self.wait()

        ###############
        # show x0 and f(x0)
        ###############
        self.play(Write(self.mark(x0, label="x_k")))
        self.wait()
        dashed_lines_fx0 = VGroup(
            self.dashed_line([x0, 0], f(x0) * UP),
            self.dashed_line([0, f(x0)], x0 * RIGHT),
            self.mark(0, f(x0), label="f(x_k)", direction=RIGHT/2),
        )
        self.play(Write(dashed_lines_fx0))
        self.wait()

        dashed_lines_fx0.set_opacity(.2)
        self.wait()


        ###############
        # show approximation formula
        ###############
        approx_formulas = self.add_approximation_formula()
        VGroup(*approx_formulas).scale(.9).to_corner(DL)
        self.add(approx_formulas[0])
        self.wait()
        self.play(Transform(*approx_formulas))
        self.wait()
        taylor_approx = approx_formulas[0]


        ###############
        # show_tangent
        ###############

        self.add_tangent(x0)
        self.wait()

        ###############
        # show_zoom_in
        ###############

        self.zoom_in(self.mark(x0, f(x0)))#.shift(RIGHT/2))
        self.wait()

        ###############
        # move x until it goes under the curve
        ###############
        Dx = 3.4
        moving_x = self.mark(x0, f(x0))
        moving_xs = [moving_x.copy() for _ in range(3)]
        moving_xs[1].set_color(COLOR_TANGENT)
        moving_xs[2].set_color(COLOR_CURVE)
        path_x_axis = self.line([x0, 0], Dx * RIGHT)
        path_tangent = self.line([x0, f(x0)], Dx * RIGHT + df(x0)* Dx * UP)
        path_curve = ParametricFunction(lambda t: self.coords_to_point(x0 + t*Dx, f(x0 +     t*Dx)))

        self.play(MoveAlongPath(moving_xs[0], path_x_axis),
                  MoveAlongPath(moving_xs[1], path_tangent),
                  MoveAlongPath(moving_xs[2], path_curve),
                  rate_func=rush_into,
                  run_time=3,
                  )
        self.wait()

        self.remove(*moving_xs)
        self.wait()

        ###############
        # Rotate tangent
        ###############
        for i, theta in enumerate((PI/3, -PI/3)):
            self.play(*[Rotate(t, theta, about_point=t.get_start()) for t in self.tangent_line])
            self.wait()

            moving_x = self.mark(x0, f(x0))
            self.play(MoveAlongPath(moving_x, Line(self.tangent_line[1-i].get_start(),
                                                   self.tangent_line[1-i].get_end(),
                                                   )))
            self.wait()
            self.remove(moving_x)


        for mobj in self.zoomed_frame_objects:
            self.remove(mobj)

        ###############
        # Show GD
        ###############
        gd_formula= MathTex(r"x_{k+1}", " = x_k - \quad ", r"\alpha", "\quad f'(x_k)").set_color_by_tex_to_color_map(color_map)
        gd_formula.to_corner(LEFT)
        self.add(gd_formula)
        self.wait()

        ################
        # show gradient
        ################

        dfx0 = df(x0) * LEFT
        grad0 = self.vec(x0 * RIGHT, dfx0).set_color(YELLOW).set_stroke(width=5)
        grad0_big = self.vec(x0 * RIGHT, 5*dfx0).set_color(YELLOW).set_stroke(width=5)
        grad0_small = self.vec(x0 * RIGHT, dfx0/2).set_color(YELLOW).set_stroke(width=5)
        self.play(ShowCreation(grad0))
        self.wait()


        ################
        # move_x0_to_x1
        ################

        self.play(Transform(grad0, grad0_big))
        self.wait()
        self.play(Transform(grad0, grad0_small))
        self.wait()
        self.remove(grad0)



        #############################
        # Quadratics
        #############################
        self.play(Indicate(taylor_approx))
        quad_term = MathTex(r"+", "f''(x_k)", r"\frac{(x-x_k)^2}2").scale(.9)
        quad_term.next_to(taylor_approx, RIGHT).set_color_by_tex_to_color_map(color_map)
        self.add(quad_term)
        self.wait()

        # Draw quad approximation
        quad_line = add_2d_func(self.axes, lambda x: f(x0) + df(x0) * (x-x0), -3, 3.)
        quad = add_2d_func(self.axes, quad_f(x0), -3, 3.)
        quad_line.set_stroke(width=3, color=COLOR_QUAD)
        quad.set_stroke(width=3, color=COLOR_QUAD)
        self.add(quad_line)
        self.play(Transform(quad_line, quad))
        self.wait()

        # for mobj in self.zoomed_frame_objects:
        #     self.add(mobj)
        # self.wait()

        # Draw quad minimizer
        x_quad = x0 - df(x0) / ddf(x0)
        xfx_quad = [x_quad, quad_f(x0)(x_quad)]
        self.play(ShowCreation(self.mark(*xfx_quad).set_color(COLOR_QUAD)))
        self.wait()

        # Draw dashed line to x1
        self.play(Write(self.dashed_line(xfx_quad, xfx_quad[1]*DOWN).set_color(COLOR_QUAD)))
        new_xkk = self.mark(x_quad, label=r"x_{k+1}", direction=DOWN).set_color(COLOR_QUAD)
        self.add(new_xkk)
        self.wait()

        ## Correct GD formula
        self.play(Transform(new_xkk.copy(), gd_formula[0]))
        self.wait()

        new_alpha = MathTex(r"1 \over {f''(x_k)}").scale(.8)
        new_alpha.move_to(gd_formula[2]).set_color_by_tex_to_color_map(color_map)
        self.play(Transform(gd_formula[2], new_alpha))
        self.wait()

        # Zoom in formula
        zoomed_in_frame = self.camera_frame.copy()
        zoomed_in_frame.scale(.5).shift(4*LEFT)
        self.play(Transform(self.camera_frame, zoomed_in_frame))
        self.wait()


        # Make high dimension

        new_alpha = MathTex(r"\nabla^2 f(x_k)^{-1}").scale(.7)
        new_alpha.move_to(gd_formula[2]).shift(RIGHT/3).set_color_by_tex_to_color_map(color_map)
        new_grad = MathTex(r"\nabla f(x_k)").scale(.7)
        new_grad.move_to(gd_formula[3]).shift(2/3 * RIGHT).set_color_by_tex_to_color_map(color_map)
        self.play(
            Transform(gd_formula[3], new_grad),
            Transform(gd_formula[2], new_alpha))
        self.wait()


    def add_str_f(self):
        self.play(Write(MathTex(f_str).to_corner(UP)))


    def add_graph_f(self):
        x_min, x_max = -4, 4
        y_min, y_max = -1, 3

        origin = 1 * DOWN + 2 * RIGHT
        x_axis, y_axis, coords_to_point = axes = add_2d_axes(x_min, x_max, y_min, y_max, origin)
        self.axes = axes
        self.coords_to_point = coords_to_point
        graph = add_2d_func(axes, f, -2, 3.)


        x_axis.set_opacity(.5)
        y_axis.set_opacity(.5)
        self.play(Write(VGroup(*axes[:2])))
        self.play(Write(graph))

    def zoom_in(self, dot):

        # Set camera
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(dot)
        frame.set_color(RED)

        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        # brackground zoomed_display
        zd_rect = BackgroundRectangle(
            zoomed_display,
            fill_opacity=0,
            buff=MED_SMALL_BUFF,
        )

        self.add_foreground_mobject(zd_rect)

        # animation of unfold camera
        unfold_camera = UpdateFromFunc(
            zd_rect,
            lambda rect: rect.replace(zoomed_display)
        )


        self.play(
            ShowCreation(frame),
        )

        # Activate zooming
        self.activate_zooming()

        self.play(
            # You have to add this line
            self.get_zoomed_display_pop_out_animation(),
            unfold_camera
        )

        self.zoomed_frame_objects = [frame, zoomed_display]


    def add_tangent(self, x):
        DfDx = RIGHT + df(x) * UP
        DfDx *= 2 / np.linalg.norm(DfDx)
        xfx = (x, f(x))
        self.play(Write(self.mark(*xfx)))

        self.tangent_line = [self.dashed_line(xfx, i * DfDx).set_color(COLOR_TANGENT)
                            for i in (2, -3)]
        self.play(*map(ShowCreation, self.tangent_line))

    def mark(self, x, y=0, label=None, direction=DOWN):
        mark_group = [Line(UL, DR, stroke_width=2),
                      Line(UR, DL, stroke_width=2),]

        mark = VGroup(*mark_group[:2]).scale(.1)\
                .shift(self.coords_to_point(x, y))

        if label:
            label_mobj = MathTex(label).next_to(mark, direction)
            mark.add(label_mobj)
        return mark

    def line(self, s, d):
        """
        Return a line in the graph coordinates.
        Args:
          s: start poitn
          d: direction
        """
        return Line(0*RIGHT, d)\
                    .shift(self.coords_to_point(*s[:2]))


    def dashed_line(self, s, d):
        return DashedLine(0*RIGHT, d)\
                    .shift(self.coords_to_point(*s[:2]))


    def vec(self, s, d):
        return Vector(d)\
                    .shift(self.coords_to_point(*s[:2]))

    def add_approximation_formula(self):
        return [
            MathTex(r"f'(x_k)", r"\approx \frac{f(x) - f(x_k)}{x - x_k}").set_color_by_tex_to_color_map(color_map, substring=False),
            MathTex(r"f(x)", r"\approx f(x_k) + ", "f'(x_k)", r"(x - x_k)").set_color_by_tex_to_color_map(color_map, substring=False)]



    # def move_x_along_curves([x0, x0-2], lambda x: 0, f, lambda x: f(x0) + (x-x0)*df(x0)):
    #     pass



# Local Variables:
# bachir-prog-local-mode: t
# eval: (setenv "WORKON_HOME" "/home/bachir/miniconda3/envs")
# eval: (pyvenv-workon "manim")
# End:
