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


f = lambda x: (x**4/4 - 2*x)/5. + 1
df = lambda x: (x**3 - 2)/5.
ddf = lambda x: 2*x**2

quad_f = lambda x: (lambda y: f(x) + df(x) * (y - x) + 1/2 * (y-x)**2 * ddf(x))

f_str = r"f(x) = \frac1{20} x^4 - \frac 25 x + 1"

NUM_DIGITS=30
x0 = -0.5
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

    def __init__(self):
        config = {
            "zoom_factor": 0.7,
            "zoomed_display_height": 4,
            "zoomed_display_width": 4,
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
        self.add(self.mark(x0, label="x_0"))
        dashed_lines_fx0 = VGroup(
            self.mark(0, f(x0), label="f(x_0)", direction=LEFT/2),
            self.dashed_line([0, f(x0)], x0 * RIGHT),
            self.dashed_line([x0, 0], f(x0) * UP)
        )
        self.add(dashed_lines_fx0)

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

        self.zoom_in(self.mark(x0, f(x0)).shift(LEFT/2))
        self.wait()

        ###############
        # move x until it goes under the curve
        ###############
        Dx = 1
        moving_x = self.mark(x0, f(x0))
        moving_xs = [moving_x.copy() for _ in range(3)]
        moving_xs[1].set_color(COLOR_TANGENT)
        moving_xs[2].set_color(COLOR_CURVE)
        path_x_axis = self.line([x0, 0], Dx * LEFT)
        path_tangent = self.line([x0, f(x0)], Dx * LEFT - df(x0)* Dx * UP)
        path_curve = ParametricFunction(lambda t: self.coords_to_point(x0 - t*Dx, f(x0 - t*Dx)))

        self.play(MoveAlongPath(moving_xs[0], path_x_axis),
                  MoveAlongPath(moving_xs[1], path_tangent),
                  MoveAlongPath(moving_xs[2], path_curve),
                  rate_func=rush_into
                  )
        self.wait()

        self.remove(*moving_xs)
        self.wait()

        for mobj in self.zoomed_frame_objects:
            self.remove(mobj)

        ################
        # show gradient
        ################


        grad0 = self.vec(x0 * RIGHT, df(x0)*LEFT/3).set_color(YELLOW).set_stroke(width=5)
        grad0_big = self.vec(x0 * RIGHT, df(x0)*LEFT).set_color(YELLOW).set_stroke(width=5)
        grad0_small = self.vec(x0 * RIGHT, df(x0)*LEFT/6).set_color(YELLOW).set_stroke(width=5)
        self.add(grad0)
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
        self.add(graph)

        for mobj in self.zoomed_frame_objects:
            self.add(mobj)
        return

    def add_str_f(self):
        self.add(MathTex(f_str).to_corner(UP))


    def add_graph_f(self):
        x_min, x_max = -4, 4
        y_min, y_max = -2, 4

        origin = 2 * DOWN
        x_axis, y_axis, coords_to_point = axes = add_2d_axes(x_min, x_max, y_min, y_max, origin)
        self.axes = axes
        self.coords_to_point = coords_to_point
        graph = add_2d_func(axes, f, -2, 3.)

        self.add(graph)

        x_axis.set_opacity(.5)
        y_axis.set_opacity(.5)
        self.add(*axes[:2])

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
        self.add(self.mark(*xfx))
        for i in (2, -3):
            self.add(self.dashed_line(xfx, i * DfDx).set_color(COLOR_TANGENT))


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
