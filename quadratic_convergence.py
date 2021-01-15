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


f = lambda x: (x**3 - 2)/5.
df = lambda x: 3/5*x**2
NUM_DIGITS=30
x0 = 2.5
solution = 10**(1/3)
a0, b0 = 0., 12.

def run_newton(f, df, x0, num_iter=10000):
    xk = x0
    history = [x0]
    for k in range(num_iter):
        xk -= f(xk) / df(xk)
        history.append(xk)
    return history



xks_newton = run_newton(f, df, x0)

def num_correct_digit(guess, solution):
    if abs(guess - solution) > 1:
        return 0
    digits = list(format(round(abs(guess - solution), NUM_DIGITS), f'.{NUM_DIGITS}f'))
    digits = digits[2:]
    r = next(i for i, c in enumerate(digits + ['1']) if c != '0') + 1
    return r

def fit_digits(dec_number, value):
    return lambda m: m.surround(dec_number[:1+num_correct_digit(value(), solution)], buff=0.1).set_height(1., stretch=True)

class QuadConvergence(Scene):

    def construct(self):
        # self.add_graph_f()
        # self.wait()
        # return

        tracker = ValueTracker(0.)
        newton_xk = DecimalNumber(float(x0), num_decimal_places=NUM_DIGITS).shift(3*UP).scale(.5)

        timer = DecimalNumber(0, num_decimal_places=0).shift(2*DOWN)

        label_timer = MathTex("k = ").next_to(timer, LEFT)
        timer_with_label = VGroup(label_timer, timer)

        # updaters
        newton_xk.add_updater(lambda m: m.set_value(float(xks_newton[int(tracker.get_value())])))
        timer.add_updater(lambda m: m.set_value(int(tracker.get_value())))

        self.add(newton_xk, )
        self.add(timer_with_label)
        self.play(tracker.set_value, 10., run_time=.1, rate_func=linear)
        self.wait()

    def add_graph_f(self):
        x_min, x_max = -2, 3
        y_min, y_max = -2, 2


        axes = add_2d_axes(x_min, x_max, y_min, y_max)
        graph = add_2d_func(axes, f, -2, 2.5)
        cross = lambda: VGroup(Line(UP + LEFT, DOWN + RIGHT),
                Line(UP + RIGHT, DOWN + LEFT)).scale(.1)
        self.add(graph)

        self.add(cross().shift(axes[2](2**(1/3), 0)))

        self.add(cross().shift(axes[2](x0, 0)))
        self.add(*axes[:2])

# Local Variables:
# bachir-prog-local-mode: t
# eval: (setenv "WORKON_HOME" "/home/bachir/miniconda3/envs")
# eval: (pyvenv-workon "manim")
# End:
