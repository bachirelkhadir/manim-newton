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


COLOR_STAR = RED
COLOR_ARROW = YELLOW

directions = np.array([
    [0.5, -2, 0],
    [-1.5, -.5, 0],
    [-1, 1, 0],
])

f = lambda u,v: (u-.5)**2/2 + (v+.5)**2/3 + .5
x_star = np.array([.5, -.5, 0])
x0 = np.array([1, 1, 0], dtype=float)

# def add_black_screen(scene):
#     scene.wait()

def add_label_x(x, k):
    label_x = MathTex(f"\\bf x_{k}")
    label_x.next_to(x, -OUT)\
            .rotate(PI/2, axis=RIGHT)\
            .rotate(PI/2, axis=OUT)
    return label_x

def add_label_d(d, k):
    label_d = MathTex(f"\\bf d_{k}")
    label_d.next_to(d, -OUT)\
            .rotate(PI/2, axis=RIGHT)\
            .rotate(PI/2, axis=OUT)
    return label_d

class IterativeOpt(ThreeDScene):
    # def __init__(self):
    #    super(LyapunovScene, self).__init__(x_axis_label="$x$")

    def construct(self):
        resolution_fa = 10
        self.set_camera_orientation(phi=65 * DEGREES, theta=-30 * DEGREES, distance=10)
        # self.set_camera_orientation(phi=0, theta=0, distance=100)

        def param_f(u, v):
            x = u
            y = v
            z = f(u, v)
            return np.array([x, y, z])

        graph = ParametricSurface(
            param_f,
            resolution=(resolution_fa, resolution_fa),
            v_min=-2.,
            v_max=+1.5,
            u_min=-1.5,
            u_max=+2,
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

        z_label = axes.get_axis_label(r"f({\bf x})", axes.get_z_axis(), edge=OUT, direction=RIGHT)
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


        # helper functions to plot on graph
        x = lambda u,v: Dot(color=RED).move_to([u, v, 0])
        fx = lambda u,v: Dot().move_to([u, v, f(u, v)])

        ####################
        # add xstar
        ####################

        self.add(x(*x_star[:2]),)
        self.add(add_label_x(x_star, "*").set_color(COLOR_STAR),)
        vert_line_xstar = DashedLine(x(*x_star[:2]), fx(*x_star[:2])).set_color(COLOR_STAR)
        self.play(ShowCreation(vert_line_xstar))
        self.add(fx(*x_star[:2]).set_color(COLOR_STAR),)
        add_black_screen(self)

        ####################
        # add x0
        ####################
        self.remove(vert_line_xstar)
        self.add(x(*x0[:2]).set_color(COLOR_ARROW),)
        self.add(add_label_x(x0, 0).set_color(COLOR_ARROW),)
        self.add(fx(*x0[:2]).set_color(COLOR_ARROW),)
        add_black_screen(self)

        #########################
        # Add formula
        ##########################

        #######################
        # Plot trajectory
        ######################

        xk = x0
        for k, d in enumerate(directions):
            if k==1:
                iter_formula = MathTex(r"\bf x_{k+1} = x_k +", "d_k").to_corner(DL)
                self.add_fixed_in_frame_mobjects(iter_formula)
                add_black_screen(self)
            dot_x, dot_fx, vec_d, animations = self.create_path(xk, d, f)
            xk += d
            self.play(animations['vec'][0])
            self.add(add_label_d(vec_d, k+1).set_color(COLOR_ARROW))
            self.play(*animations['vec'][1:])
            self.add(add_label_x(xk, k+1).set_color(COLOR_ARROW))
            add_black_screen(self)
            self.play(*animations['curve'])
            add_black_screen(self)

        ####################
        # Add quesiton about direction
        ####################
        self.play(Indicate(iter_formula[1]))
        add_black_screen(self)

    def create_path(self, x0, d, f, run_time=1):
        def traj_on_plane_at(t):
            return x0 + t * d

        def traj_on_curve_at(t):
            x1, x2, _ = traj_on_plane_at(t)
            return [x1, x2, f(x1, x2)]


        animations = {}
        vec_d = Arrow(x0, x0+d).set_color(COLOR_ARROW)

        # Trajectory on plane
        dot_on_plane = Dot().set_color(COLOR_ARROW)
        traj_on_plane = ParametricFunction(traj_on_plane_at,
                                  t_max=1, fill_opacity=1)
        traj_on_plane_tracker = CurvesAsSubmobjects(traj_on_plane.copy())
        traj_on_plane_tracker.set_color(COLOR_ARROW)
        dot_on_plane.add_updater(lambda m: m.move_to(traj_on_plane.get_end()))
        traj_on_plane.fade(1)


        animations['vec'] = [
            ShowCreation(vec_d),
            Write(dot_on_plane),
            ShowCreation(traj_on_plane),
            ShowCreation(traj_on_plane_tracker),
        ]

        # Lifted trajectory on graph of f
        dot_on_curve = Dot().set_color(COLOR_ARROW)
        traj_on_curve = ParametricFunction(traj_on_curve_at,
                                  t_max=1, fill_opacity=1)
        traj_on_curve_tracker = CurvesAsSubmobjects(traj_on_curve.copy())
        traj_on_curve_tracker.set_color(COLOR_ARROW)
        dot_on_curve.add_updater(lambda m: m.move_to(traj_on_curve.get_end()))
        traj_on_curve.fade(1)

        animations['curve'] = [
            Write(dot_on_curve),
            ShowCreation(traj_on_curve),
            ShowCreation(traj_on_curve_tracker),
        ]

        return dot_on_plane, dot_on_curve, vec_d, animations
# Local Variables:
# bachir-prog-local-mode: t
# eval: (setenv "WORKON_HOME" "/home/bachir/miniconda3/envs")
# eval: (pyvenv-workon "manim")
# End:
