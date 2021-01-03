from manim import *
from manim.utils.bezier import interpolate


NUM_BLACK_SCREENS = 0

def align_group_text(group, dir=LEFT):
    for g in group[1:]:
        g.align_to(group[0], dir)
    return group


def stack_group_text(group, dir=DOWN, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER):
    for g_prev, g in zip(group, group[1:]):
        g.next_to(g_prev, dir, buff=buff)
    return group


def add_black_screen(scene, timeout=1):
    global NUM_BLACK_SCREENS
    NUM_BLACK_SCREENS += 1
    print("Blackish Screen: ", NUM_BLACK_SCREENS)
    color = BLACK
    rect = Rectangle(fill_color=color, strole_color=color, fill_opacity=1).scale(100)
    # make unaffected by camera
    scene.wait(timeout)
    try:
        scene.add_fixed_in_frame_mobjects(rect)
    except AttributeError:
        # we are not in 3D
        scene.add(rect)
    scene.wait(timeout)
    scene.remove(rect)


def add_2d_axes(x_min=-1, x_max=1,y_min=-1, y_max=1, origin=0*RIGHT):
    o_axis = origin
    x_axis = NumberLine(x_min=x_min, x_max=x_max).shift(o_axis)
    y_axis = NumberLine(x_min=y_min, x_max=y_max).shift(o_axis)
    y_axis.rotate(np.pi / 2, about_point=o_axis)
    coords_to_point = lambda x, y: [
        x_axis.number_to_point(x)[0],
        y_axis.number_to_point(y)[1],
        0]
    return x_axis, y_axis, coords_to_point

def add_2d_func(axis, f, x_min=None, x_max=None):
    x_axis, y_axis, coords_to_point = axis
    def parameterized_function(alpha):
        x = interpolate(x_min if x_min else x_axis.x_min,
                        x_max if x_max else x_axis.x_max,
                        alpha)
        y = f(x)
        return coords_to_point(x, y)

    graph = ParametricFunction(parameterized_function, color=BLUE)
    graph.underlying_function = f
    return graph
