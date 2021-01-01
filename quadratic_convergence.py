import sys
import os
import itertools as it
import numpy as np
from scipy import linalg
from scipy.stats import norm
from manim import *
from decimal import *
getcontext().prec = 30

config.max_files_cached = 10000
config.background_color = "#1f303e"

PROJECT_DIR = '/home/bachir/Dropbox/Job_Applications/Academia/Application_Fall_2020/Application_By_School/UCLouvain/Presentations/newton/manim/'
sys.path.append(PROJECT_DIR)
from helper_functions import *


f = lambda x: x**3 - Decimal(10)
df = lambda x: Decimal(2) * x**2
NUM_DIGITS=30
x0 = Decimal(12.)
solution = Decimal(10)**Decimal(1/3)
a0, b0 = Decimal(0.), Decimal(12.)

def run_newton(f, df, x0, num_iter=10000):
    xk = x0
    history = [x0]
    for k in range(num_iter):
        xk -= f(xk) / df(xk)
        history.append(xk)
    return history


def run_binary(f, a, b, num_iter=10000):
    history = []

    for k in range(num_iter):
        med = a/2 + b/2
        history.append({'a': a, 'b': b, 'med': med})
        if f(med) > 0:
            b = med
        else:
            a = med
    return history


xks_newton = run_newton(f, df, x0)
xks_binary = run_binary(f, a0, b0)

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
        tracker = ValueTracker(0.)
        newton_xk = DecimalNumber(float(x0), num_decimal_places=NUM_DIGITS).shift(3*UP).scale(.5)
        binary_xk = DecimalNumber(float(a0 + b0)/2., num_decimal_places=NUM_DIGITS).shift(3*DOWN).scale(.5)

        timer = DecimalNumber(0, num_decimal_places=0).shift(2*DOWN)

        label_timer = MathTex("k = ").next_to(timer, LEFT)
        timer_with_label = VGroup(label_timer, timer)


        # rects
        newton_rect = Rectangle(color=YELLOW)
        binary_rect = Rectangle(color=ORANGE)

        # updaters
        newton_xk.add_updater(lambda m: m.set_value(float(xks_newton[int(tracker.get_value())])))
        binary_xk.add_updater(lambda m: m.set_value(float(xks_binary[int(tracker.get_value())]['med'])))

        newton_rect.add_updater(fit_digits(newton_xk, lambda: xks_newton[int(tracker.get_value())]))
        binary_rect.add_updater(fit_digits(binary_xk, lambda: xks_binary[int(tracker.get_value())]['med']))

        timer.add_updater(lambda m: m.set_value(int(tracker.get_value())))

        self.add(newton_rect, binary_rect)
        self.add(newton_xk, binary_xk)
        self.add(timer_with_label)
        self.play(tracker.set_value, 10., run_time=2, rate_func=linear)
        self.wait()

# Local Variables:
# bachir-prog-local-mode: t
# eval: (setenv "WORKON_HOME" "/home/bachir/miniconda3/envs")
# eval: (pyvenv-workon "manim")
# End:
