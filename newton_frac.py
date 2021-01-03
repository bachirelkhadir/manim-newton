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
x0 = 2.

SIZE_GRID = 400
ZOOM_LEVEL = 0
COLORS_DICT = [YELLOW, BLUE, RED]

class NewtonFractal(MovingCameraScene):

    def construct(self):
        self.add_fractal()
        self.wait()
        self.grid.set_stroke(opacity=.1)
        self.play(self.camera_frame.scale, ZOOM_LEVEL, run_time=4)
        self.wait()
        return

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

    def add_fractal(self):
        x_min, x_max = -2, 3
        y_min, y_max = -2, 2

        x_axis, y_axis, coords_to_point = axes = add_2d_axes(x_min, x_max, y_min, y_max)

        cross = lambda: VGroup(Line(UP + LEFT, DOWN + RIGHT),
                Line(UP + RIGHT, DOWN + LEFT)).scale(.1)

        m = np.load(open("newton_fractal.np", "rb"))
        grid = self.grid = self.get_grid(SIZE_GRID, SIZE_GRID, ZOOM_LEVEL/2  * config.frame_width)
        offset = 0
        for i in range(SIZE_GRID):
            for j in range(SIZE_GRID):
                grid[i][j].set_opacity(.5)
                grid[i][j].set_color(COLORS_DICT[int(m[i+offset, j+offset])])

        self.add(x_axis, y_axis)
        self.add(MathTex("Re(x)").next_to(x_axis, RIGHT))
        self.add(MathTex("Im(x)").next_to(y_axis, UP))
        self.add(grid)

# Local Variables:
# bachir-prog-local-mode: t
# eval: (setenv "WORKON_HOME" "/home/bachir/miniconda3/envs")
# eval: (pyvenv-workon "manim")
# End:
