#!/usr/bin/env python3

import math

import svgwrite

def degree_sin(degrees):
    return math.sin(math.radians(degrees))

def degree_cos(degrees):
    return math.cos(math.radians(degrees))

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

d = svgwrite.Drawing(filename='test.svg', size=('500px', '500px'))

origin = (250, 250)
ring_radius = 200
ring_thickness = 50
inner_ring_radius = ring_radius - ring_thickness

c_outer = d.circle(center=origin, r=ring_radius, fill='none', stroke='black')
d.add(c_outer)
c_inner = d.circle(center=origin, r=inner_ring_radius, fill='none', stroke='black')
d.add(c_inner)
vertical_bar = d.line(start=(250, 0), end=(250, 500), stroke='black')
d.add(vertical_bar)
horizontal_bar = d.line(start=(0, 250), end=(500, 250), stroke='black')
d.add(horizontal_bar)

step = 30

# We need to calculate a bigger radius to draw chords on, since we want to
# circumscribe a polygon on the outer circle, not inscribe.
theta = step / 2
big_radius = ring_radius / degree_cos(theta)

outer_segment_length = 2 * ring_radius * math.tan(math.radians(theta))
print(f'outer_segment_length: {outer_segment_length}')
segments = 360 / step
print(f'segments: {segments}')

inner_segment_length = (inner_ring_radius * math.sin(math.radians(step))) / math.sin(math.radians((180 - step) / 2))
print(f'inner_segment_length: {inner_segment_length}')

all_segments_length = (outer_segment_length + inner_segment_length) / 2 * segments
print(f'all_segments_length: {all_segments_length}')

ring_circumference = 2 * math.pi * ring_radius
print(f'ring_circumference: {ring_circumference}')

for begin_arc in range(0, 360, step):
    end_arc = begin_arc + step

    # Segment boundaries for a line segment on the inside of the ring
    inner_begin_coords, inner_end_coords = chord_dimensions((begin_arc, end_arc), origin, inner_ring_radius)

    # Segment boundaries for a line segment on the outside of the ring
    outer_begin_coords, outer_end_coords = chord_dimensions((begin_arc, end_arc), origin, big_radius)

    points = [inner_begin_coords, outer_begin_coords, outer_end_coords, inner_end_coords]
    polygon = d.polygon(points=points, fill='none', stroke='blue')
    d.add(polygon)

d.save()
