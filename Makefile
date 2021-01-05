##
# Newton animation
#
# @file
# @version 0.1

# filename =newton_frac.py
# scene =NewtonFractal

# filename = iterative_opt.py
# scene = IterativeOpt


filename = gradient_descent_1d.py
scene = GradientDescent1d

N = 0
q = l

image:
	manim $(filename)  $(scene) -q$q -s -n $N --leave_progress_bars && sleep 1

video:
	manim $(filename)  $(scene) -p -q$q  -n $N  --leave_progress_bars && sleep 1

play:
	xdg-open media/videos/newton/480p15/ThreeDFunction.mp4

iterativeopt:
	manim iterative_opt.py  IterativeOpt -p -qm  --leave_progress_bars && sleep 1

quadconvergence:
	manim quadratic_convergence.py  QuadConvergence -p -qm  --leave_progress_bars && sleep 1

newtonfractal:
	manim newton_frac.py   NewtonFractal -p -qm  --leave_progress_bars && sleep 1

gradientdescent:
	manim gradient_descent_1d.py   GradientDescent1D -p -qm  --leave_progress_bars && sleep 1

#end
