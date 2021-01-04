import sys
import os
import itertools as it
import numpy as np
from scipy import linalg
from scipy.stats import norm
from manim import *
config.max_files_cached = 10000
config.background_color = "#1f303e"

PROJECT_DIR = '/home/bachir/Dropbox/Job_Applications/Academia/Application_Fall_2020/Application_By_School/UCLouvain/Presentations/newton/manim/'
sys.path.append(PROJECT_DIR)
from helper_functions import *
from opt_parameters import *



DEBUG = False
COLOR_CURVE = BLUE
COLOR_TANGENT = YELLOW
COLOR_QUAD = RED

def run_newton(f, df, x0, num_iter=10000):
    xk = x0
    history = [x0]
    for k in range(num_iter):
        xk -= f(xk) / df(xk)
        history.append(xk)
    return history



xks_newton = run_newton(f, df, x0)

class GradientDescent1D(ZoomedScene):
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
        self.add_graph_f()

        ###############
        # show x0 and f(x0)
        ###############
        self.play(Write(self.mark(x0, label="x_0")))
        dashed_lines_fx0 = VGroup(
            self.dashed_line([x0, 0], f(x0) * UP),
            self.dashed_line([0, f(x0)], x0 * RIGHT),
            self.mark(0, f(x0), label="f(x_0)", direction=RIGHT/2),
        )
        self.play(Write(dashed_lines_fx0))
        self.wait()

        dashed_lines_fx0.set_opacity(.2)
        self.wait()

        ###############
        # show approximation formula
        ###############
        approx_formulas = stack_group_text(self.add_approximation_formula())
        approx_formulas = VGroup(*approx_formulas)
        approx_formulas.scale(.7).to_corner(DL)
        self.add(approx_formulas)
        self.wait()


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
        Dx = 2
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

        for mobj in self.zoomed_frame_objects:
            self.remove(mobj)

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


        # Draw quad approximation

        graph = add_2d_func(self.axes, quad_f(x0), -2, 3.)
        graph.set_stroke(width=2, color=COLOR_QUAD)
        self.play(ShowCreation(graph))


        self.wait()
        for mobj in self.zoomed_frame_objects:
            self.add(mobj)


        self.wait()

        # Draw quad minimizer
        x_quad = x0 - df(x0) / ddf(x0)
        xfx_quad = [x_quad, quad_f(x0)(x_quad)]
        self.play(ShowCreation(self.mark(*xfx_quad).set_color(COLOR_QUAD)))
        self.wait()

        # Draw dashed line to x1
        self.play(Write(self.dashed_line(xfx_quad, xfx_quad[1]*DOWN)))

        # Figure out the math

        return

    def add_str_f(self):
        self.play(Write(MathTex(f_str).to_corner(UP)))


    def add_graph_f(self):
        x_min, x_max = -4, 4
        y_min, y_max = -2, 4

        origin = 2 * DOWN + 2 * RIGHT
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
        DfDx /= np.linalg.norm(DfDx)
        xfx = (x, f(x))
        self.play(Write(self.mark(*xfx)))
        self.play(*[
            ShowCreation(self.dashed_line(xfx, i * DfDx).set_color(COLOR_TANGENT))
            for i in (2, -3)])

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
        """
        Return a line in the graph coordinates.
        Args:
          s: start poitn
          d: direction
        """
        return Vector(d)\
                    .shift(self.coords_to_point(*s[:2]))

    def add_approximation_formula(self):
        return [
            MathTex(r"f'(x_0) \approx \frac{f(x) - f(x_0)}{x - x_0}"),
            MathTex(r"f(x) \approx f(x_0) + f'(x_0)(x - x_0)")]



    # def move_x_along_curves([x0, x0-2], lambda x: 0, f, lambda x: f(x0) + (x-x0)*df(x0)):
    #     pass



# Local Variables:
# bachir-prog-local-mode: t
# eval: (setenv "WORKON_HOME" "/home/bachir/miniconda3/envs")
# eval: (pyvenv-workon "manim")
# End:
