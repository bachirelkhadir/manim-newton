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

DEBUG = False

class UnconstrainedOpt(MovingCameraScene):

    NUM_BLACK_SCREENS = 0
    def wait(self, timeout=1):
        self.NUM_BLACK_SCREENS += 1
        print("Blackish Screen: ", self.NUM_BLACK_SCREENS)
        color = BLACK
        rect = Rectangle(fill_color=color, strole_color=color, fill_opacity=1).scale(100)
        Scene.wait(self, timeout)

        if not DEBUG:
            self.add(rect)
            Scene.wait(self, timeout)
            self.remove(rect)

    def construct(self):
        self.play(Write(Tex("Unconstrained Optimization").shift(UP)))
        self.wait()
        self.play(Write(MathTex(r"f: \mathbb R^n \rightarrow \mathbb R")))
        self.wait()

        lab_min_fx = MathTex(r"\min", "f(x)").shift(DOWN)
        self.play(Write(lab_min_fx))
        self.wait()

        lab_x_Rn = MathTex(r"x", r"\in \mathbb R^n")\
            .scale(.6)\
            .next_to(lab_min_fx[0], DOWN)
        self.add(lab_x_Rn)
        self.wait()

        self.play(Indicate(lab_x_Rn[0]))
        self.wait()
        self.play(Indicate(lab_min_fx[1]))
        self.wait()
        return


# Local Variables:
# bachir-prog-local-mode: t
# eval: (setenv "WORKON_HOME" "/home/bachir/miniconda3/envs")
# eval: (pyvenv-workon "manim")
# End:
