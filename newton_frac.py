import sys
import os
import itertools as it
import numpy as np
from scipy import linalg
from scipy.stats import norm
from manim import *
from helper_functions import *


config.max_files_cached = 10000
config.background_color = "#1f303e"

DEBUG = config.quality == "low_quality"

f = lambda x: (x**3 - 2)/5.
df = lambda x: 3/5*x**2
x0 = 2.

SIZE_GRID = 200
ZOOM_LEVEL = 1.
RUN_TIME = .1
COLORS_DICT = [YELLOW, BLUE, RED]

cross = lambda: VGroup(Line(UP + LEFT, DOWN + RIGHT),
                Line(UP + RIGHT, DOWN + LEFT)).scale(.1)
class NewtonFractal(MovingCameraScene):

    NUM_BLACK_SCREENS = 0
    def wait(self, timeout=1):
        self.NUM_BLACK_SCREENS += 1
        print("Blackish Screen: ", self.NUM_BLACK_SCREENS)
        color = BLACK
        rect = Rectangle(fill_color=color, strole_color=color, fill_opacity=1).scale(100)
        super(NewtonFractal, self).wait(timeout)

        if not DEBUG:
            self.add(rect)
            super(NewtonFractal, self).wait(timeout)
            self.remove(rect)

    def construct(self):

        self.camera_frame.scale(.7).shift(1.5*LEFT)
        self.construct_grid()
        self.grid.set_stroke(opacity=.05)

        unit_circle   = Circle(WHITE, stroke_opacity=.5)

        self.play(FadeIn(MathTex(r"z^3 - 1 = 0").to_corner(LEFT).shift(RIGHT/2)))
        self.wait()
        self.add_axes()
        self.wait()
        self.play(ShowCreation(unit_circle))
        self.wait()

        label_groups = []
        labels = list(map(MathTex, ["1", r"e^{\frac{2i\pi}3}", r"e^{\frac{4i\pi}3}"]))
        next_to = [ DR, UL, DL ]
        for theta, c, lab, n  in zip((0, 2*PI/3, 4*PI/3), COLORS_DICT, labels, next_to):
            cr = cross().move_to(np.cos(theta) *RIGHT + np.sin(theta) * UP)
            cr.set_color(c)
            lab.next_to(cr, n, SMALL_BUFF).set_color(c)
            label_groups.append(VGroup(cr, lab))

        for lab in label_groups:
            self.play(Write(lab))
        self.wait()

        for lab in label_groups:
            self.remove(lab)
        self.remove(unit_circle)
        self.play(ShowCreation(Rectangle(width=4, height=4)))
        self.wait()

        self.play(ShowCreation(self.grid))
        self.remove(self.ax_objects)
        self.wait()

        self.grid.set_stroke(opacity=0)
        self.wait()

    def get_grid(self, n, m, height=4):
        grid = VGroup(*[
            VGroup(
                *[Square() for x in range(m)]
            ).arrange(RIGHT, buff=0)
            for y in range(n)
        ]).arrange(DOWN, buff=0)
        grid.set_height(height)
        grid.set_stroke(WHITE, 2)
        return grid

    def construct_grid(self):

        m = np.load(open("newton_fractal.np", "rb"))
        grid = self.grid = self.get_grid(SIZE_GRID, SIZE_GRID)
        offset = int((len(m) - SIZE_GRID) / 2)
        print("OFFSET:", offset)
        for i in range(SIZE_GRID):
            for j in range(SIZE_GRID):
                grid[i][j].set_opacity(.5)
                grid[i][j].set_color(COLORS_DICT[int(m[i+offset, j+offset])])

    def add_axes(self):
        x_min, x_max = -2, 2
        y_min, y_max = -2, 2

        x_axis, y_axis, coords_to_point = axes = add_2d_axes(x_min, x_max, y_min, y_max)


        self.ax_objects = VGroup(
            x_axis, y_axis,
            MathTex(r"\Re(z)").next_to(x_axis, RIGHT),
            MathTex(r"\Im(z)").shift(2.3*UP))
        self.add(self.ax_objects)


# Local Variables:
# bachir-prog-local-mode: t
# eval: (setenv "WORKON_HOME" "/home/bachir/miniconda3/envs")
# eval: (pyvenv-workon "manim")
# End:
