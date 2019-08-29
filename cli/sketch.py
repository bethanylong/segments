import svgwrite

def set_up_drawing(size, filename, horizontal_division=0.5):
    size_str = f'{size}px'
    d = svgwrite.Drawing(filename=filename, size=(size_str, size_str))

    # Sketching out a Cartesian plane like this: +
    vertical_half = size * 0.5
    vertical_bar = d.line(start=(vertical_half, 0), end=(vertical_half, size), stroke='black')
    d.add(vertical_bar)
    horizontal_half = size * horizontal_division
    horizontal_bar = d.line(start=(0, horizontal_half), end=(size, horizontal_half), stroke='black')
    d.add(horizontal_bar)

    return d
