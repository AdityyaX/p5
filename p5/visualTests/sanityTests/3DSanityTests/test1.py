from p5 import (
    background,
    blinn_phong_material,
    box,
    fill,
    lights,
    no_fill,
    no_stroke,
    push_matrix,
    rotate_x,
    rotate_y,
    size,
    sphere,
    stroke,
    translate,
)


def setup():
    size(640, 360)


def draw():
    background(0)
    lights()

    with push_matrix():
        translate(-130, 0, 0)
        rotate_y(1.25)
        rotate_x(-0.4)
        no_stroke()
        fill(255)
        blinn_phong_material()
        box(100, 100, 100)

    with push_matrix():
        translate(250, 0, -200)
        no_fill()
        stroke(255)
        sphere(280)
