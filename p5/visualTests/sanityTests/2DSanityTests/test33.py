from p5 import color_mode, fill, height, millis, no_stroke, rect, size, width

scale = 0


def setup():
    size(640, 360)
    no_stroke()

    global scale
    scale = width / 20


def draw():
    global scale
    for i in range(int(scale)):
        color_mode("RGB", (i + 1) * scale * 10)
        fill(millis() % ((i + 1) * scale * 10))
        rect([i * scale, 0], scale, height)
