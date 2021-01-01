import manim as m

NUM_BLACK_SCREENS = 0

def align_group_text(group, dir=m.LEFT):
    for g in group[1:]:
        g.align_to(group[0], dir)
    return group


def stack_group_text(group, dir=m.DOWN, buff=m.DEFAULT_MOBJECT_TO_MOBJECT_BUFFER):
    for g_prev, g in zip(group, group[1:]):
        g.next_to(g_prev, dir, buff=buff)
    return group


def add_black_screen(scene, timeout=1):
    global NUM_BLACK_SCREENS
    NUM_BLACK_SCREENS += 1
    print("Blackish Screen: ", NUM_BLACK_SCREENS)
    color = m.BLACK
    rect = m.Rectangle(fill_color=color, strole_color=color, fill_opacity=1).scale(100)
    # make unaffected by camera
    scene.wait(timeout)
    try:
        scene.add_fixed_in_frame_mobjects(rect)
    except AttributeError:
        # we are not in 3D
        scene.add(rect)
    scene.wait(timeout)
    scene.remove(rect)
