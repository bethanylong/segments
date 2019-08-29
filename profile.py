#!/usr/bin/env python3

import math

import svgwrite

import sketch

RECTANGLE_FILL = 'none'
RECTANGLE_STROKE = 'green'


def draw_base(drawing, origin, radius, height):
    origin_x, origin_y = origin
    left_upper_x = origin_x - radius
    left_upper_y = origin_y - height
    width = radius * 2
    rect = drawing.rect((left_upper_x, left_upper_y), (width, height),
            fill=RECTANGLE_FILL, stroke=RECTANGLE_STROKE)
    drawing.add(rect)


def draw_ring(drawing, origin, altitude, radius, height, thickness):
    """Altitude is the distance between the bottom of this ring and the x axis."""
    # Two rectangles, mirrored across y axis
    origin_x, origin_y = origin

    # Rectangle 1
    left_upper_x_1 = origin_x - radius
    left_upper_y_1 = origin_y - altitude - height

    # Rectangle 2
    left_upper_x_2 = origin_x + radius - thickness
    left_upper_y_2 = left_upper_y_1

    rect1 = drawing.rect((left_upper_x_1, left_upper_y_1), (thickness, height),
            fill=RECTANGLE_FILL, stroke=RECTANGLE_STROKE)
    rect2 = drawing.rect((left_upper_x_2, left_upper_y_2), (thickness, height),
            fill=RECTANGLE_FILL, stroke=RECTANGLE_STROKE)
    drawing.add(rect1)
    drawing.add(rect2)


if __name__ == '__main__':
    def mm(inches, mm_per_inch=50):
        return inches * mm_per_inch

    size = 500
    filename = 'profile.svg'
    horizontal_division = 0.9
    # Maybe better to pass origin than horizontal_division...
    origin = (size * 0.5, size * horizontal_division)
    d = sketch.set_up_drawing(size, filename, horizontal_division=horizontal_division)

    #base_radius = 150
    #base_height = 50
    base_radius = mm((4 + 3/4) / 2)
    base_height = mm(1 / 2)

    # Radii are specifically the outer radii. Subtract the ring thickness to get
    # the inner radius.
    rings = [
        {'radius': mm(5.5 / 2), 'height': mm(1 + 1/8), 'thickness': mm(1 + 3/8)},
        {'radius': mm(6.5 / 2), 'height': mm(1 + 1/8), 'thickness': mm(1 + 3/8)},
        {'radius': mm((6 + 5/8) / 2), 'height': mm(1 + 1/4), 'thickness': mm(3 / 4)},
        {'radius': mm(6.5 / 2), 'height': mm(1 + 1/8), 'thickness': mm(1 + 3/8)},
    ]

    # Just draw rectangles!
    draw_base(d, origin, base_radius, base_height)

    altitude = base_height
    for ring in rings:
        draw_ring(d, origin, altitude, **ring)
        altitude += ring['height']

    # Write the SVG
    d.save()
