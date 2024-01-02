from p5 import (
    background,
    color_mode,
    fill,
    height,
    mouse_x,
    no_stroke,
    rect,
    size,
    stroke,
)

barWidth = 20
lastBar = -1


def setup():
    size(640, 360)
    stroke(255, 160)
    color_mode("HSB", height, height, height)
    no_stroke()
    background(0)


def draw():
    global barWidth, lastBar

    whichBar = mouse_x / barWidth
    if whichBar != lastBar:
        barX = whichBar * barWidth
        fill(mouse_x, height, height)
        rect(barX, 0, barWidth, height)
        lastBar = whichBar
