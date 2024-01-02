from p5 import (
    background,
    color_mode,
    fill,
    height,
    mouse_x,
    mouse_y,
    no_stroke,
    rect,
    size,
    title,
    width,
)

bar_width = 20
last_bar = None


def setup():
    size(640, 360)
    title("Brightness")
    color_mode("HSB", width, 100, height)
    no_stroke()
    background(0)


def draw():
    global last_bar
    which_bar = mouse_x // bar_width
    if which_bar is not last_bar:
        bar_x = which_bar * bar_width
        fill(bar_x, 100, mouse_y)
        rect((bar_x, 0), bar_width, height)
        last_bar = which_bar
