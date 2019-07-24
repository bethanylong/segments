#!/usr/bin/env python3

import math

import svgwrite


def distance_between_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def chord_length(segments, origin, radius):
    arc = (0, degrees_per_segment(segments))
    chord = chord_dimensions(arc, origin, radius)
    return distance_between_points(*chord)


def degree_sin(degrees):
    return math.sin(math.radians(degrees))


def degree_cos(degrees):
    return math.cos(math.radians(degrees))


def degree_tan(degrees):
    return math.tan(math.radians(degrees))


def degrees_per_segment(segments):
    return 360.0 / segments


def chord_dimensions(arc_span, origin, radius):
    """Find the endpoints of a chord spanning the given degree tuple in
    arc_span, on a circle with the given origin and radius. Angles are on the
    classic trig unit-style circle, where (with radius 1) 0 degrees is at
    coordinates (1, 0)."""
    origin_x, origin_y = origin
    begin_angle, end_angle = arc_span

    begin_x = radius * degree_cos(begin_angle) + origin_x
    begin_y = origin_y - radius * degree_sin(begin_angle)
    end_x = radius * degree_cos(end_angle) + origin_x
    end_y = origin_y - radius * degree_sin(end_angle)

    return ((begin_x, begin_y), (end_x, end_y))


def circumscribed_radius(ring_radius, segments):
    """If an isosceles triangle with a corner at the origin and the other
    corners incorporating the segment looks like this:
     .  <- origin
    /_\ <- segment

    We need to make it into two right triangles that look like this so we can do
    trigonometry on it:
      , .
    /_| |_\

    This means we have to divide the angle the segment occupies by 2 since we
    split our isosceles triangle in half.

    The purpose of this is that our ring normally lies *within* the segments,
    since we remove material from the segments on a lathe to make the ring. This
    means the ring we make is inscribed in the segments. But we also want to
    imagine a circumscribed circle lying *outside* the segments, which will help
    us draw the segments because the outer border will be chords on the
    circumscribed circle.

    Once we have our right triangle whose angle-by-the-origin we know, the
    (adjacent) long leg of the triangle is the radius of the inscribed ring and
    the hypotenuse is the radius of the circumscribed ring. (We don't care about
    the short leg.)

    From the definition of cosine:
    cos(theta) = adjacent / hypotenuse

    We know angle theta and the adjacent side, and want to find the hypotenuse.
    So:

    hypotenuse * cos(theta) = adjacent
    hypotenuse = adjacent / cos(theta)

    In our terminology:

    circumscribed_radius = inscribed_radius / cos(segment_degrees / 2) 
    """
    degrees_per_segment = 360.0 / segments
    degrees_per_right_triangle = degrees_per_segment / 2
    circumscribed_radius = ring_radius / degree_cos(degrees_per_right_triangle)
    return circumscribed_radius


def set_up_drawing(filename='test.svg'):
    d = svgwrite.Drawing(filename=filename, size=('500px', '500px'))

    # Sketching out a Cartesian plane like this: +
    vertical_bar = d.line(start=(250, 0), end=(250, 500), stroke='black')
    d.add(vertical_bar)
    horizontal_bar = d.line(start=(0, 250), end=(500, 250), stroke='black')
    d.add(horizontal_bar)

    return d


def draw_ring(drawing, origin, radius, thickness):
    """Draw two concentric circles on the given drawing, illustrating the
    circular ring with the given radius and thickness.
    """
    inner_radius = radius - thickness
    outer_circle = drawing.circle(center=origin, r=radius, fill='none', stroke='black')
    drawing.add(outer_circle)
    inner_circle = drawing.circle(center=origin, r=inner_radius, fill='none', stroke='black')
    drawing.add(inner_circle)


def draw_trapezoid(drawing, corner_coords):
    assert len(corner_coords) == 4
    trapezoid = drawing.polygon(points=corner_coords, fill='none', stroke='blue')
    drawing.add(trapezoid)


def draw_segment(drawing, arc, origin, radius, thickness, segments):
    assert len(arc) == 2
    inner_ring_radius = radius - thickness
    big_radius = circumscribed_radius(radius, segments)
    # Arranging the four corners of the trapezoid in the order in which we'll
    # "connect the dots". The inner and outer side of the segment are chords on
    # the inner ring circle (inner_ring_radius) and the circumscribed circle
    # (big_radius), respectively.
    coords = chord_dimensions(arc, origin, inner_ring_radius) \
            + tuple(reversed(chord_dimensions(arc, origin, big_radius)))
    draw_trapezoid(drawing, coords)


if __name__ == '__main__':
    d = set_up_drawing()

    origin = (250, 250)
    ring_radius = 200
    ring_thickness = 50
    inner_ring_radius = ring_radius - ring_thickness

    draw_ring(d, origin, radius=ring_radius, thickness=ring_thickness)

    segments = 12
    step = int(degrees_per_segment(segments))
    print(f'segments: {segments}')

    outer_segment_length = chord_length(segments, origin, circumscribed_radius(ring_radius, segments))
    print(f'outer_segment_length: {outer_segment_length}')

    inner_segment_length = chord_length(segments, origin, inner_ring_radius)
    print(f'inner_segment_length: {inner_segment_length}')

    all_segments_length = (outer_segment_length + inner_segment_length) / 2 * segments
    print(f'all_segments_length: {all_segments_length}')


    # XXX this breaks on non-integer degree steps
    for begin_arc in range(0, 360, step):
        end_arc = begin_arc + step
        arc = (begin_arc, end_arc)
        draw_segment(d, arc, origin, ring_radius, ring_thickness, segments)

    # Write the SVG
    d.save()
