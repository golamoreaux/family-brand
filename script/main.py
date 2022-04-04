#!/usr/bin/python
"""Script to help build svg."""
import argparse
import os
import random
import string

# Consts
IMAGE_GRID = "grid"
IMAGE_KEYLINE = "keyline"
IMAGE_LOGO = "logo"
CMD_IMAGES = [IMAGE_GRID, IMAGE_KEYLINE, IMAGE_LOGO]

VIEW_WIDTH = 900
VIEW_HEIGHT = VIEW_WIDTH
PIXEL_WIDTH_SMALL = 24

SCALE_FACTOR = 1  # Scale pixel drawing
PIXEL_WIDTH =  48
MAX_WIDTH = PIXEL_WIDTH * SCALE_FACTOR
MAX_HEIGHT = MAX_WIDTH
CORNER_RADIUS = MAX_WIDTH * 12 / 192
CORNER_RADIUS_SMALL = 2

GRID_SCALE_FACTOR = 10

COLOR_DIM_GREY = "#d3d3d3"
COLOR_LIGHT_GREY = "#efefef"
COLOR_GRAY = "#999999"
COLOR_DARK_GRAY = "#8d8d8d"
COLOR_RED = "#ff4081"
COLOR_WHITE = "#fefefe"

STROKE_WIDTH_MEDIUM = 1
STROKE_WIDTH_THIN = STROKE_WIDTH_MEDIUM / 2
STROKE_WIDTH_THICK = STROKE_WIDTH_MEDIUM * 2
STROKE_WIDTH_GRID = PIXEL_WIDTH * 0.001
STROKE_WIDTH_KEYLINE = (STROKE_WIDTH_THIN * ( PIXEL_WIDTH / PIXEL_WIDTH_SMALL) / GRID_SCALE_FACTOR) / 2
# All lines are drawn on center
# This makes outside border lines visually half of inside lines
STROKE_WIDTH_BORDER = 2 * STROKE_WIDTH_KEYLINE

print(PIXEL_WIDTH, STROKE_WIDTH_KEYLINE, STROKE_WIDTH_BORDER )
# Defaults
DEFAULT_OPACITY = 0.5
DEFAULT_STROKE = COLOR_GRAY
DEFAULT_STROKE_WIDTH = STROKE_WIDTH_MEDIUM
DEFAULT_FILL = COLOR_LIGHT_GREY

# Files
BASE_FOLDER = "assets"
LOGO_FILE_NAME = "logo.svg"
LOGO_FILE = os.path.join(BASE_FOLDER, LOGO_FILE_NAME)
GRID_FILE_NAME = "grid.svg"
GRID_FILE = os.path.join(BASE_FOLDER, GRID_FILE_NAME)
KEYLINE_FILE_NAME = "keyline_gen.svg"
KEYLINE_FILE = os.path.join(BASE_FOLDER, KEYLINE_FILE_NAME)
# KEYLINE_HIGHLIGHT_FILE_NAME = "keyline_highlight_gen.svg"
KEYLINE_HIGHLIGHT_FILE = KEYLINE_FILE
# KEYLINE_SQUARE_FILE_NAME = "keyline_square_gen.svg"
# KEYLINE_SQUARE_FILE = os.path.join(BASE_FOLDER, KEYLINE_SQUARE_FILE_NAME)



class Dimensions():
    """Available image dimensions."""


class SvgDraw():
    """Create an SVG drawing instance."""


def gen_id():
    """Generate an id"""
    characters = string.ascii_letters.lower() + string.digits
    return "_" + "".join(random.choice(characters) for i in range(8))


def build_line(
    id=None,
    x1=0,
    y1=0,
    x2=0,
    y2=0,
    stroke=DEFAULT_STROKE,
    stroke_width=DEFAULT_STROKE_WIDTH,
):
    """Build a line."""
    if id is None:
        id = gen_id()

    return f'\t<line id="{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}"/>'


def build_rectangle(
    id=None,
    x=0,
    y=0,
    width=100,
    height=100,
    stroke=DEFAULT_STROKE,
    stroke_width=DEFAULT_STROKE_WIDTH,
    fill=DEFAULT_FILL,
    rx=0,
    ry=0,
):
    """Build a rectangle."""
    if id is None:
        id = gen_id()

    lines = []
    lines.append(
        f'\t<rect id="{id}" x="{x}" y="{y}" width="{width}" height="{height}" rx="{rx}" ry="{ry}"'
    )
    if stroke:
        lines.append(f'stroke="{stroke}"')
    if stroke_width:
        lines.append(f'stroke-width="{stroke_width}"')
    if fill:
        lines.append(f'fill="{fill}"')
    lines.append("/>")

    return " ".join(lines)


def build_circle(
    id=None,
    r=0,
    cy=0,
    cx=0,
    stroke=DEFAULT_STROKE,
    stroke_width=DEFAULT_STROKE_WIDTH,
    fill=DEFAULT_FILL,
):
    """Build a circle."""
    if id is None:
        id = gen_id()
    svg_string = []
    svg_string.append(f'\t<circle id="{id}" r="{r}" cx="{cx}" cy="{cy}"')
    if stroke:
        svg_string.append(f'stroke="{stroke}"')
    if stroke_width:
        svg_string.append(f'stroke-width="{stroke_width}"')
    if fill:
        svg_string.append(f'fill="{fill}"')
    svg_string.append("/>")
    return " ".join(svg_string)


def inside_border_shape(
    id,
    shape_str,
    fill=DEFAULT_FILL,
    stroke=DEFAULT_STROKE,
    stroke_width=DEFAULT_STROKE_WIDTH,
):
    """Create object with inside border."""
    lines = []
    lines.append("\t<defs>")
    lines.append("\t" + shape_str)
    lines.append(
        f'\t\t<clipPath  id="{id}_clip"><use xlink:href="#{id}" x="0" y="0" width="100%" height="100%" /></clipPath>'
    )
    lines.append("\t</defs>")
    lines.append(
        f'\t<use clip-path="url(#{id}_clip)" xlink:href="#{id}" x="0" y="0" width="100%" height="100%"'
    )

    lines.append(
        f'\t\tstyle="fill:{fill};fill-opacity:0.1;stroke:{stroke};stroke-width:{stroke_width};stroke-opacity:1"/>'
    )
    return "\n".join(lines)


def build_keyline_circle(
    cir_radius=MAX_WIDTH,
    cir_top=MAX_WIDTH / 2,
    cir_left=MAX_HEIGHT / 2,
    bold=False,
):
    """Build a keyline circle."""
    if bold:
        stroke = COLOR_RED
        stroke_width = STROKE_WIDTH_MEDIUM
        fill = COLOR_RED
    else:
        stroke = DEFAULT_STROKE
        stroke_width=STROKE_WIDTH_KEYLINE * 2
        fill = None

    shape_id = gen_id()
    shape_string = build_circle(
        id=shape_id,
        cx=cir_top,
        cy=cir_left,
        r=cir_radius,
        stroke=None,
        stroke_width=None,
        fill=None,
    )

    return inside_border_shape(
        shape_id,
        shape_string,
        fill=fill,
        stroke=stroke,
        stroke_width=stroke_width,
    )


def build_keyline_rect(height=MAX_HEIGHT, width=MAX_WIDTH, bold=False, corner_radius=CORNER_RADIUS):
    """Build a keyline rectangle."""
    key_rx = corner_radius
    key_ry = key_rx

    shape_top = (MAX_HEIGHT / 2) - (height / 2)
    shape_left = (MAX_WIDTH / 2) - (width / 2)

    if bold:
        stroke = COLOR_RED
        stroke_width = STROKE_WIDTH_MEDIUM
        fill = COLOR_RED
    else:
        stroke = DEFAULT_STROKE
        stroke_width=STROKE_WIDTH_KEYLINE * 2
        fill = None

    shape_id = gen_id()
    shape_string = build_rectangle(
        id=shape_id,
        x=shape_left,
        y=shape_top,
        width=width,
        height=height,
        stroke=None,
        stroke_width=None,
        fill=None,
        rx=key_rx,
        ry=key_ry,
    )

    return inside_border_shape(
        shape_id,
        shape_string,
        fill=fill,
        stroke=stroke,
        stroke_width=stroke_width,
    )


def build_grid_lines():
    """Build grid lines."""
    lines = []

    # Background
    background_string = build_rectangle(
        width=MAX_WIDTH, height=MAX_HEIGHT, stroke="None"
    )
    lines.append(background_string)

    # Vertical lines
    for x in range(0, int(MAX_WIDTH + SCALE_FACTOR), SCALE_FACTOR):
        lines.append(
            build_line(
                x1=x,
                x2=x,
                y2=MAX_HEIGHT,
                stroke=COLOR_DIM_GREY,
                stroke_width=STROKE_WIDTH_GRID,
            )
        )

    # horizontal lines
    for y in range(0, int(MAX_HEIGHT + SCALE_FACTOR), SCALE_FACTOR):
        lines.append(
            build_line(
                x2=MAX_WIDTH,
                y1=y,
                y2=y,
                stroke=COLOR_DIM_GREY,
                stroke_width=STROKE_WIDTH_GRID,
            )
        )

    return "\n".join(lines)


def build_border():
    """Build a Border."""
    lines = []

    # Border
    lines.append(
        build_line(
            x2=MAX_WIDTH, stroke=COLOR_DARK_GRAY, stroke_width=STROKE_WIDTH_BORDER
        )
    )
    lines.append(
        build_line(
            y1=MAX_HEIGHT,
            x2=MAX_WIDTH,
            y2=MAX_HEIGHT,
            stroke=COLOR_DARK_GRAY,
            stroke_width=STROKE_WIDTH_BORDER,
        )
    )
    lines.append(
        build_line(
            y2=MAX_HEIGHT, stroke=COLOR_DARK_GRAY, stroke_width=STROKE_WIDTH_BORDER
        )
    )
    lines.append(
        build_line(
            x1=MAX_WIDTH,
            x2=MAX_WIDTH,
            y2=MAX_HEIGHT,
            stroke=COLOR_DARK_GRAY,
            stroke_width=STROKE_WIDTH_BORDER,
        )
    )

    return "\n".join(lines)


def build_keyline(square=False, wide=False, tall=False, circle=False):
    """Generate Keyline Shapes."""
    tri_factor = 0.35412
    # tri_factor = 0.33333
    lines = []

    keyline_lines = (
        (
            MAX_WIDTH / 2,
            0,
            MAX_WIDTH / 2,
            MAX_HEIGHT,
        ),
        (
            round(MAX_WIDTH * tri_factor),
            0,
            round(MAX_WIDTH * tri_factor),
            MAX_HEIGHT,
        ),
        (
            round(MAX_WIDTH * (1 - tri_factor)),
            0,
            round(MAX_WIDTH * (1 - tri_factor)),
            MAX_HEIGHT,
        ),
        (
            0,
            MAX_HEIGHT / 2,
            MAX_WIDTH,
            MAX_HEIGHT / 2,
        ),
        (
            0,
            round(MAX_HEIGHT * tri_factor),
            MAX_WIDTH,
            round(MAX_HEIGHT * tri_factor),
        ),
        (
            0,
            round(MAX_HEIGHT * (1 - tri_factor)),
            MAX_WIDTH,
            round(MAX_HEIGHT * (1 - tri_factor)),
        ),
        (
            0,
            0,
            MAX_WIDTH,
            MAX_HEIGHT,
        ),
        (
            0,
            MAX_HEIGHT,
            MAX_WIDTH,
            0,
        ),
    )
    for keyline in keyline_lines:
        lines.append(
            build_line(
                x1=keyline[0],
                y1=keyline[1],
                x2=keyline[2],
                y2=keyline[3],
                stroke_width=STROKE_WIDTH_KEYLINE,
            )
        )

    # Shapes
    if PIXEL_WIDTH < PIXEL_WIDTH_SMALL:
        sqr_width = 14
        corner_radius = 1.5
        corner_offset = 4.5
        rect_wide = 16
        rect_short = 12
        cir_radius = 8 
        cir_small_radius = 4
        
    elif PIXEL_WIDTH == PIXEL_WIDTH_SMALL:
        # corner_radius = CORNER_RADIUS_SMALL
        sqr_width = 18        
        corner_radius = CORNER_RADIUS_SMALL
        corner_offset = 5
        rect_wide = 20
        rect_short = round(MAX_WIDTH * 128 / 192)
        cir_radius = 10 
        cir_small_radius = MAX_WIDTH * (40 / 192) 
    
    else:
        sqr_width = round(MAX_WIDTH * 152 / 192)
        corner_radius = CORNER_RADIUS  
        corner_offset = MAX_WIDTH * 1 / 6
        rect_wide = round(MAX_HEIGHT * 176 / 192)
        rect_short = round(MAX_WIDTH * 128 / 192)
        cir_radius = MAX_WIDTH * (88 / 192)
        
        cir_small_radius = MAX_WIDTH * (40 / 192)   
        

    keyline_rectangles = (
        (sqr_width, sqr_width, square),
        (rect_short, rect_wide, wide),
        (rect_wide, rect_short, tall),
    )
    for rect in keyline_rectangles:
        lines.append(
            build_keyline_rect(
                height=rect[0],
                width=rect[1],
                bold=rect[2],
                corner_radius=corner_radius
            )
        )

    keyline_circles = (
        # cx, cy, r
        (MAX_WIDTH / 2, MAX_WIDTH / 2, cir_radius, circle),
        (MAX_WIDTH / 2, MAX_WIDTH / 2, cir_small_radius, False),
        (corner_offset, corner_offset, corner_radius , False),
        (MAX_WIDTH - corner_offset, corner_offset, corner_radius , False),
        (corner_offset, MAX_HEIGHT - corner_offset, corner_radius, False),
        (MAX_WIDTH - corner_offset, MAX_HEIGHT - corner_offset, corner_radius, False),
    )
    for circ in keyline_circles:
        lines.append(
            build_keyline_circle(
                cir_left=circ[0],
                cir_top=circ[1],
                cir_radius=circ[2],
                bold=circ[3],
            )
        )

    return "\n".join(lines)


def svg_header(size):
    """Return the svg header."""
    lines = []
    lines.append(
        f'<svg viewBox="0 0 {MAX_WIDTH} {MAX_HEIGHT}" width="{VIEW_WIDTH}" height="{VIEW_HEIGHT}"'
    )
    lines.append(
        'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"'
    )
    lines.append(f'stroke="{DEFAULT_STROKE}"')
    lines.append(f'stroke-width="{DEFAULT_STROKE_WIDTH}"')
    lines.append(f'fill-opacity="{DEFAULT_OPACITY}">')
    return "\n".join(lines)


def svg_footer():
    """Return the svg footer."""
    return "</svg>"


def grid_box_image(size):
    """Build Grid Box svg."""
    lines = []

    lines.append(svg_header(size=size))
    lines.append(build_grid_lines(size=size))
    lines.append(build_border(size=size))
    lines.append(svg_footer())

    return lines


def keyline_image(square=False, wide=False, tall=False, circle=False):
    """Build keyline Box svg."""
    lines = []

    lines.append(svg_header())
    lines.append(build_grid_lines())
    lines.append(build_keyline(square=square, wide=wide, tall=tall, circle=circle))
    lines.append(build_border())
    lines.append(svg_footer())

    return lines


def logo_image():
    """Build Logo svg."""
    COLOR_RED = "#CE1126"
    COLOR_BLUE = "#002654"

    RED_WIDTH = 1. / 3
    RED_HEIGTH = RED_WIDTH
    RED_INSIDE_POINT_WIDTH = 1. / 6
    RED_INSIDE_POINT_HEIGHT = RED_INSIDE_POINT_WIDTH
    red_polygon = [(0, 33.33), (16.66, 83.33), (66.66, 100), (0, 100)]

    BLUE_POINT_TOP = 2. / 3
    BLUE_POINT_LEFT = 1. / 3

    # 16x16
    # 32x32
    # 48x48
    # 256x256

    if PIXEL_WIDTH == 20:
        width_ratio = 16 / 20
    elif PIXEL_WIDTH == PIXEL_WIDTH_SMALL:
        width_ratio = 20 / 24
    else:
        width_ratio = 44 / 48

    # Set bounds for image
    max_width = round(MAX_WIDTH * width_ratio)
    max_height = round(MAX_HEIGHT * width_ratio)
    x_offset = round((MAX_WIDTH - max_width) / 2)
    y_offset = round((MAX_WIDTH - max_width) / 2)

    red_width =  round(max_width - (max_width * RED_WIDTH))
    red_height =  red_width
    red_inside_point = round(max_width * RED_INSIDE_POINT_WIDTH)

    # Blue Polygon
    blue_point_top = round(max_height * BLUE_POINT_TOP)
    blue_point_left = round(max_height * BLUE_POINT_LEFT)

    
    lines = []

    lines.append(svg_header())
    lines.append(build_grid_lines())
    lines.append(build_keyline())

    # Background
    lines.append(
        f'\t<rect x="0" y="0" width="100%" height="100%" stroke="None" fill="{COLOR_WHITE}" />'
    )    
    lines.append(
        f'\t<polygon stroke="None" fill="{COLOR_RED}" points="{x_offset},{y_offset + max_height - red_height} {x_offset + red_inside_point},{y_offset + max_height - red_inside_point} {x_offset + red_width},{y_offset + max_height} {x_offset},{y_offset + max_height}" />'
    )    
    lines.append(
        f'\t<polygon stroke="None" fill="{COLOR_BLUE}" points="{x_offset},{y_offset} {x_offset + max_width},{y_offset} {x_offset + max_width},{y_offset + max_height} {x_offset + blue_point_left},{y_offset + blue_point_top}" />'
    )

    # Border

    lines.append(build_border())
    lines.append(svg_footer())

    return lines


def save_svg(file_name, svg_string):
    """Save svg to file."""
    with open(file_name, "w", encoding="utf-8") as svg_file:
        svg_file.writelines("\n".join(svg_string))


def main(image, highlight, size):
    """Build logo image."""

    PIXEL_WIDTH = size

    if image == IMAGE_GRID:
        file_name = GRID_FILE
        image_svg = grid_box_image(size=size)
    elif image == IMAGE_KEYLINE:
        file_name = KEYLINE_HIGHLIGHT_FILE
        if highlight == 'square':            
            image_svg = keyline_image(square=True, size=size)
        elif highlight == 'wide-rect':
            image_svg = keyline_image(wide=True, size=size)
        elif highlight == 'tall-rect':
            image_svg = keyline_image(tall=True, size=size)
        elif highlight == 'circle':
            image_svg = keyline_image(circle=True, size=size)
        else:
            file_name = KEYLINE_FILE
            image_svg = keyline_image(size=size)
    else: 
        file_name = LOGO_FILE
        image_svg = logo_image(size=size)
    
    save_svg(file_name, image_svg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="main.py",
        usage="%(prog)s [image] [options]",
        description="Generate standard brand images at various sizes",
        epilog=f"Examples:\n\tmain.py {IMAGE_KEYLINE} --highlight square\n\tmain.py {IMAGE_GRID} --size 192",
        add_help=True,
    )
    parser.add_argument(
        'image', 
        help='Specify the image to create.',
        choices=CMD_IMAGES,
        )
    parser.add_argument(
        "--highlight",
        help=f"[{IMAGE_KEYLINE}] command arg. Specify the shape to highlight in the keyline image.",
        choices=['square', 'wide-rect', 'tall-rect', 'circle'],
        # metavar='SHAPE',

    )
    parser.add_argument(
        "--size",
        help='Size of the image in pixels. (Default: %(default)s)',
        choices=['20', '24', '48', '192'],
        default="48"
    )

    args = parser.parse_args()

    print(args.image, args.highlight, args.size)
    main(args.image, args.highlight, args.size)
