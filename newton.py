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



directions = np.array([
    [0, -2, 0],
    [-1.5, .5, 0],
    [1, 1, 0],
])

x0 = np.array([1, 1, 0], dtype=float)

def add_label_x(x, k):
    label_x = MathTex(f"x_{k}")
    label_x.next_to(x, -OUT)\
            .rotate(PI/2, axis=RIGHT)\
            .rotate(PI/2, axis=OUT)
    return label_x

class IterativeOpt(ThreeDScene):
    # def __init__(self):
    #    super(LyapunovScene, self).__init__(x_axis_label="$x$")

    def construct(self):
        resolution_fa = 10
        self.set_camera_orientation(phi=65 * DEGREES, theta=-30 * DEGREES, distance=10)
        # self.set_camera_orientation(phi=0, theta=0, distance=100)

        f = lambda u,v: u**2/2 + v**2/3 + .3
        def param_f(u, v):
            x = u
            y = v
            z = f(u, v)
            return np.array([x, y, z])

        graph = ParametricSurface(
            param_f,
            resolution=(resolution_fa, resolution_fa),
            v_min=-1.5,
            v_max=+1.5,
            u_min=-1.5,
            u_max=+1.5,
        )
        plane = ParametricSurface(
            lambda u, v: np.array([u, v, -0.01]),
            resolution=(resolution_fa, resolution_fa),
            v_min=-3,
            v_max=+3,
            u_min=-3,
            u_max=+3,
            checkerboard_colors=None,
        )


        graph.set_style(stroke_color=GREEN)
        graph.set_fill_by_checkerboard(GREEN, BLUE, opacity=0.3)

        plane.set_style(fill_color=BLACK, fill_opacity=.8, stroke_color=BLUE)
        axes = self.axes = ThreeDAxes()



        # fix axis labels
        axes.add(axes.get_axis_labels(x_label_tex="x_1", y_label_tex="x_2"))
        axes.axis_labels[0].rotate(PI/2,axis=RIGHT)
        axes.axis_labels[0].rotate(PI/2,axis=OUT)
        axes.axis_labels[1].rotate(PI/2,axis=RIGHT)
        axes.axis_labels[1].rotate(PI/2,axis=OUT)

        z_label = axes.get_axis_label("f(x)", axes.get_z_axis(), edge=OUT, direction=RIGHT)
        z_label.rotate(PI/2,axis=RIGHT)
        z_label.rotate(PI/2,axis=OUT)
        z_label.shift(RIGHT)
        axes.add(z_label)


        self.play(Write(axes))
        add_black_screen(self)
        self.play(Write(graph))
        add_black_screen(self)
        self.add(plane)
        add_black_screen(self)


        x = lambda u,v: Dot(color=RED).move_to([u, v, 0])
        fx = lambda u,v: Dot().move_to([u, v, f(u, v)])
        # self.add(Rectangle(fill_color=BLUE, strok_color=YELLOW, fill_opacity=1), axes)
        self.add(x(*x0[:2]),)
        self.add(add_label_x(x0, 0),)
        self.add(fx(*x0[:2]),)
        add_black_screen(self)

        #######################
        # Plot trajectory
        ######################

        xk = x0
        self.add(add_label_x(x0, 0))
        for k, d in enumerate(directions):
            dot_x, dot_fx = self.create_path(xk, d, f)
            xk += d
            self.add(add_label_x(xk, k+1))

        self.wait()
    def create_path(self, x0, d, f, run_time=1):
        def traj_on_plane_at(t):
            return x0 + t * d


        def traj_on_curve_at(t):
            x1, x2, _ = traj_on_plane_at(t)
            return [x1, x2, f(x1, x2)]


        vec_d = Arrow(x0, x0+d)
        self.play(ShowCreation(vec_d))

        # Trajectory on plane
        dot_on_plane = Dot()
        traj_on_plane = ParametricFunction(traj_on_plane_at,
                                  t_max=1, fill_opacity=1)
        traj_on_plane_tracker = CurvesAsSubmobjects(traj_on_plane.copy())
        traj_on_plane_tracker.set_color(RED)
        dot_on_plane.add_updater(lambda m: m.move_to(traj_on_plane.get_end()))
        traj_on_plane.fade(1)
        self.add(dot_on_plane, self.axes)

        self.play(
            ShowCreation(traj_on_plane),
            ShowCreation(traj_on_plane_tracker),
            run_time=run_time
        )

        add_black_screen(self)
        # Lifted trajectory on graph of f
        dot_on_curve = Dot()
        traj_on_curve = ParametricFunction(traj_on_curve_at,
                                  t_max=1, fill_opacity=1)
        traj_on_curve_tracker = CurvesAsSubmobjects(traj_on_curve.copy())
        traj_on_curve_tracker.set_color(RED)
        dot_on_curve.add_updater(lambda m: m.move_to(traj_on_curve.get_end()))
        traj_on_curve.fade(1)
        self.add(dot_on_curve, self.axes)

        self.play(
            ShowCreation(traj_on_curve),
            ShowCreation(traj_on_curve_tracker),
            run_time=run_time
        )

        add_black_screen(self)
        return dot_on_plane, dot_on_curve
# Local Variables:
# bachir-prog-local-mode: t
# eval: (setenv "WORKON_HOME" "/home/bachir/miniconda3/envs")
# eval: (pyvenv-workon "manim")
# End:
