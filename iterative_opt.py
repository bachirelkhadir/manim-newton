import sys

import os
import itertools as it
import numpy as np
from scipy import linalg
from scipy.stats import norm
from manim import *

config.max_files_cached = 10000
config.background_color = "#1f303e"

DEBUG = config.quality == "low_quality"
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

if DEBUG:
    print("BLACK SCREENS not shown")
    add_black_screen = lambda scene: scene.wait()

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
        self.set_camera_orientation(phi=65 * DEGREES, theta=-30 * DEGREES, distance=20)
        # self.set_camera_orientation(phi=0, theta=0, distance=100)

        def param_f(u, v):
            x = u
            y = v
            z = f(u, v)
            return np.array([x, y, z])

        def param_f_curved(u, v):
            x = u
            y = v
            z = f(u*1.4, v*1.4)
            return np.array([x, y, z])

        graph = ParametricSurface(
            param_f,
            resolution=(resolution_fa, resolution_fa),
            u_min=-1.,
            u_max=2,
            v_min=-2,
            v_max=+1.5,
        )


        graph_curved = ParametricSurface(
            param_f_curved,
            resolution=(resolution_fa, resolution_fa),
            u_min=-1.,
            u_max=2,
            v_min=-2,
            v_max=+1.5,
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


        for g in (graph, graph_curved):
            g.set_style(stroke_color=GREEN)
            g.set_fill_by_checkerboard(GREEN, BLUE, opacity=0.3)

        plane.set_style(fill_color=BLACK, fill_opacity=.8, stroke_color=BLUE)
        axes = self.axes = ThreeDAxes(x_min=-3,
                                      y_min=-3,
                                      z_min=-1)



        # fix axis labels
        axes.add(axes.get_axis_labels(x_label_tex="x_1", y_label_tex="x_2"))
        axes.axis_labels[0].rotate(PI/2,axis=RIGHT)
        axes.axis_labels[0].rotate(PI/2,axis=OUT)
        axes.axis_labels[1].rotate(PI/2,axis=RIGHT)
        axes.axis_labels[1].rotate(PI/2,axis=OUT)

        z_label = axes.get_axis_label(r"f({\bf x})", axes.get_z_axis(), edge=OUT, direction=RIGHT)
        z_label.rotate(PI/2,axis=RIGHT)
        z_label.rotate(PI/2,axis=OUT)
        z_label.shift(UP)
        axes.add(z_label)


        top_label = Tex("An example with n=2").to_corner(UL)
        self.add_fixed_in_frame_mobjects(top_label)
        self.play(Write(top_label))
        self.play(Write(axes))
        self.add(plane)
        add_black_screen(self)
        self.play(Write(graph))
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

        #########################
        # Iterative Opt algorithms
        ##########################
        label_iter_algorithms = Tex("Iterative Optimization Algorithms").scale(.8)
        label_iter_algorithms.to_corner(DL).shift(UP)
        self.add_fixed_in_frame_mobjects(label_iter_algorithms)
        self.remove(top_label)
        self.play(Write(label_iter_algorithms))
        add_black_screen(self)

        ####################
        # add x0
        ####################
        self.remove(vert_line_xstar)
        self.add(x(*x0[:2]).set_color(COLOR_ARROW),)
        self.add(add_label_x(x0, 0).set_color(COLOR_ARROW),)
        vert_line_x0 = DashedLine(x(*x0[:2]), fx(*x0[:2])).set_color(COLOR_ARROW)
        self.play(ShowCreation(vert_line_x0))
        self.add(fx(*x0[:2]).set_color(COLOR_ARROW),)
        add_black_screen(self)
        self.remove(vert_line_x0)

        #######################
        # Plot trajectory
        ######################

        xk = x0
        self.arrows_and_curves = []
        for k, d in enumerate(directions):
            dot_x, dot_fx, vec_d, animations = self.create_path(xk, d, f)
            xk += d
            self.play(animations['vec'][0])
            lab_d = add_label_d(vec_d, k).set_color(COLOR_ARROW)
            self.arrows_and_curves.append(lab_d)
            self.add(lab_d)
            self.play(*animations['vec'][1:])
            lab_x = add_label_x(xk, k+1).set_color(COLOR_ARROW)
            self.arrows_and_curves.append(lab_x)
            self.add(lab_x)
            add_black_screen(self)
            self.play(*animations['curve'])
            add_black_screen(self)

        iter_formula = MathTex(r"\bf x_{k+1} = x_k +", "d_k").to_corner(DL)
        self.add_fixed_in_frame_mobjects(iter_formula)
        add_black_screen(self)

        ####################
        # Add quesiton about direction
        ####################
        self.play(Indicate(iter_formula[1]))
        add_black_screen(self)


        ####################
        # Add gradient and hessian
        ####################
        self.play(*[ApplyMethod(mobj.set_opacity, .1)
            for mobj in self.arrows_and_curves])

        lab_grad_f = MathTex(r"\nabla f({\bf x}) = ", )

        vec_grad_f = Matrix([
            [r"\partial f({\bf x}) \over \partial x_1"],
            [r"\vdots"],
            [r"\partial f({\bf x})\over \partial x_n"],
        ], element_alignment_corner=0*UP, v_buff=1.2)
        grad_f = VGroup(*stack_group_text([lab_grad_f, vec_grad_f], RIGHT))
        grad_f.to_corner(DR).scale(.8)
        self.add_fixed_in_frame_mobjects(grad_f)
        self.play(Write(grad_f))
        add_black_screen(self)


        self.remove(grad_f)
        lab_H_f = MathTex(r"\nabla^2 f({\bf x}) = ", )

        vec_H_f = Matrix([
            [r"\frac{\partial^2 f({\bf x})}{\partial x_1\partial x_1}, \ldots, \frac{\partial^2 f({\bf x})}{\partial x_1\partial x_n}"],
            [r"\vdots"],

            [r"\frac{\partial^2 f({\bf x})}{\partial x_n\partial x_1}, \ldots, \frac{\partial^2 f({\bf x})}{\partial x_n\partial x_n}"],
        ], element_alignment_corner=0*UP, v_buff=1.2)
        H_f = VGroup(*stack_group_text([lab_H_f, vec_H_f], RIGHT))
        H_f.scale(.6).to_corner(DR)
        self.add_fixed_in_frame_mobjects(H_f)
        self.play(ShowCreation(H_f))
        add_black_screen(self)




        ##############
        # To curved and back
        ##############
        saved_graph = graph.copy()
        self.play(Transform(graph, graph_curved))
        self.play(Transform(graph, saved_graph))
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

        self.arrows_and_curves.extend([traj_on_curve, traj_on_plane,
                                       traj_on_curve_tracker, traj_on_plane_tracker,
                                       dot_on_curve, dot_on_plane,
                                       vec_d])
        return dot_on_plane, dot_on_curve, vec_d, animations
# Local Variables:
# bachir-prog-local-mode: t
# eval: (setenv "WORKON_HOME" "/home/bachir/miniconda3/envs")
# eval: (pyvenv-workon "manim")
# End:
