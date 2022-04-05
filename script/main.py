#!/usr/bin/python
"""Script to help build svg."""
import argparse
from decimal import ROUND_DOWN
import os
import random
import string

from isort import file

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
# CORNER_RADIUS = MAX_WIDTH * 12 / 192
# CORNER_RADIUS_SMALL = 2

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

DEFAULT_CORNER_RADIUS = 2

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

    DEFAULT_VIEW_WIDTH = 900
    DEFAULT_VIEW_HEIGHT = DEFAULT_VIEW_WIDTH
    # PIXEL_WIDTH_SMALL = 24

    DEFAULT_SCALE_FACTOR = 1  # Scale pixel drawing
    DEFAULT_PIXEL_WIDTH =  48.
    # MAX_WIDTH = PIXEL_WIDTH * SCALE_FACTOR
    # MAX_HEIGHT = MAX_WIDTH

    
    # CORNER_RADIUS_SMALL = 2

    SYSTEM_ICON_LAYOUT_SIZE = 24
    SYSTEM_ICON_DENSE_LAYOUT_SIZE = 20
    PRODUCT_ICON_SIZE = 48
    LIVE_AREA = 20
    LIVE_AREA_DENSE = 16
    PADDING = 2


    def __init__(self, pixel_width=DEFAULT_PIXEL_WIDTH):
        """Initalize new Deimension object."""
        self.pixel_width = pixel_width
        self.scale_factor = self.DEFAULT_SCALE_FACTOR
        self.view_width = self.DEFAULT_VIEW_WIDTH
        self.view_height = self.DEFAULT_VIEW_HEIGHT


    @property
    def max_width(self):
        return self.pixel_width * self.scale_factor

    @property
    def max_height(self):
        return self.max_width

    @property
    def cir_radius(self):
        """Define radius of great circle."""
        ratio = 88 / 192

        if self.pixel_width == 8:
            return 4
        elif self.pixel_width == self.SYSTEM_ICON_DENSE_LAYOUT_SIZE:
            return (self.pixel_width - self.PADDING * 2 ) / 2
        elif self.pixel_width == self.SYSTEM_ICON_LAYOUT_SIZE:
            return (self.pixel_width - self.PADDING * 2 ) / 2
        elif self.pixel_width == 29:
            return (self.pixel_width - self.PADDING * 2 ) / 2
        # elif self.pixel_width == 38:
        #     return (self.pixel_width - self.PADDING * 2.5 ) / 2
        elif self.pixel_width <= 40:
            return (self.pixel_width - self.PADDING  * 2 ) / 2
        elif self.pixel_width == 60:
            ratio = 27 / 60
        elif self.pixel_width == 87:
            return 39.5
        elif self.pixel_width == 167:
            return 76.5

        return round(self.max_width * ratio) 

    @property
    def live_area_width(self):
        """Define the live area width."""
        live_area_width = self.cir_radius * 2
        return live_area_width
    
    @property
    def live_area_height(self):
        """Define the live area height."""
        live_area_height = self.cir_radius * 2
        return live_area_height

    @property
    def padding(self):
        """Define the padding around the logo."""
        live_area_width = self.cir_radius * 2
        padding = round((self.max_width - live_area_width) / 2)
        return padding

    @property
    def tri_factor(self):
        """Define the trifactor to divide the shape."""
        tri_factor = 0.35412
        tri_factor = 1. / 3

        if self.pixel_width == self.SYSTEM_ICON_LAYOUT_SIZE:
            tri_factor = 3. / 10
        # if self.pixel_width == self.PRODUCT_ICON_SIZE * 4:
        #     tri_factor = 60. / 176

        return  tri_factor

    @property
    def square_width(self):
        """Define width of keyline square."""   
        ratio = 152 / 192

        if self.pixel_width == 8:
            ratio = 6. / 8
        elif self.pixel_width <= self.SYSTEM_ICON_DENSE_LAYOUT_SIZE:
            ratio =  14. / self.SYSTEM_ICON_DENSE_LAYOUT_SIZE
        elif self.pixel_width <= self.SYSTEM_ICON_LAYOUT_SIZE:
            ratio =  18. / self.SYSTEM_ICON_LAYOUT_SIZE
        elif self.pixel_width <= 38:
            ratio =  30. / 38
        elif self.pixel_width <= 40:
            ratio = 30. / 40
        elif self.pixel_width <= 76:
            ratio = 62. / 76
        elif self.pixel_width <= 80:
            ratio = 64. / 80
        elif self.pixel_width == 120:
            ratio = 96. / 120
        elif self.pixel_width == 167:
            ratio = 133. / 167
        
       
        
        return round(self.max_width * ratio)

    @property
    def short_side(self):
        """Define the short side of a rectangle."""

        ratio =  128 / 192

        if self.pixel_width == 8:
            ratio = 6. / 8
        elif self.pixel_width <= self.SYSTEM_ICON_DENSE_LAYOUT_SIZE:
            ratio = 12. / self.SYSTEM_ICON_DENSE_LAYOUT_SIZE
        elif self.pixel_width < self.SYSTEM_ICON_LAYOUT_SIZE:
            ratio = 12. / self.SYSTEM_ICON_LAYOUT_SIZE
        elif self.pixel_width <= 38:
            ratio =  26. / 38
        elif self.pixel_width == 40:
            ratio = 26. / 40
        elif self.pixel_width == 58:
            ratio = 38. / 58
        elif self.pixel_width == 76:
            ratio = 52. / 76
        elif self.pixel_width == 80:
            ratio = 54. / 80
        elif self.pixel_width == 87:
            ratio = 59. / 87
        elif self.pixel_width == 152:
            ratio = 100. / 152
        elif self.pixel_width == 167:
            ratio = 111. / 167
    
        short_side = round(self.max_width * ratio) 
        return short_side

    @property
    def corner_offset(self):
        """Define the corner offset."""
        corner_offset = self.max_width * 1 / 6

        corner_offset = ((self.max_width - self.square_width) / 2) + self.corner_radius

        return corner_offset

    
    @property
    def corner_radius(self):
        """Define the corner radius."""
        ratio =  12 / 192

        corner_radius = self.max_width * ratio

        if self.pixel_width == 8:
            corner_radius = 0.5
        elif self.pixel_width <= self.SYSTEM_ICON_DENSE_LAYOUT_SIZE:
            corner_radius = 1.5
        elif self.pixel_width <= self.SYSTEM_ICON_LAYOUT_SIZE:
            corner_radius = 2

        return corner_radius










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


def build_keyline_rect(height=MAX_HEIGHT, width=MAX_WIDTH, bold=False, corner_radius=DEFAULT_CORNER_RADIUS, size=None):
    """Build a keyline rectangle."""
    key_rx = corner_radius
    key_ry = key_rx

    shape_top = (size.max_height / 2) - (height / 2)
    shape_left = (size.max_width / 2) - (width / 2)

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


def build_grid_lines(size):
    """Build grid lines."""
    lines = []

    # Background
    background_string = build_rectangle(
        width=size.max_width, height=size.max_height, stroke="None"
    )
    lines.append(background_string)

    # Vertical lines
    for x in range(0, int(size.max_width + size.scale_factor), size.scale_factor):
        lines.append(
            build_line(
                x1=x,
                x2=x,
                y2=size.max_height,
                stroke=COLOR_DIM_GREY,
                stroke_width=STROKE_WIDTH_GRID,
            )
        )

    # horizontal lines
    for y in range(0, int(size.max_height +  size.scale_factor),  size.scale_factor):
        lines.append(
            build_line(
                x2=size.max_width ,
                y1=y,
                y2=y,
                stroke=COLOR_DIM_GREY,
                stroke_width=STROKE_WIDTH_GRID,
            )
        )

    return "\n".join(lines)


def build_border(size):
    """Build a Border."""
    lines = []

    # Border
    lines.append(
        build_line(
            x2=size.max_width, stroke=COLOR_DARK_GRAY, stroke_width=STROKE_WIDTH_BORDER
        )
    )
    lines.append(
        build_line(
            y1=size.max_height,
            x2=size.max_width,
            y2=size.max_height,
            stroke=COLOR_DARK_GRAY,
            stroke_width=STROKE_WIDTH_BORDER,
        )
    )
    lines.append(
        build_line(
            y2=size.max_height, stroke=COLOR_DARK_GRAY, stroke_width=STROKE_WIDTH_BORDER
        )
    )
    lines.append(
        build_line(
            x1=size.max_width,
            x2=size.max_width,
            y2=size.max_height,
            stroke=COLOR_DARK_GRAY,
            stroke_width=STROKE_WIDTH_BORDER,
        )
    )

    return "\n".join(lines)


def build_keyline(square=False, wide=False, tall=False, circle=False, size=None):
    """Generate Keyline Shapes."""
    # tri_factor = 0.35412
    # tri_factor = 0.33333
    tri_factor = size.tri_factor
    lines = []

    keyline_lines = (
        (
            size.max_width / 2,
            0,
            size.max_width / 2,
            size.max_height,
        ),
        (
            size.padding + round(size.live_area_width * tri_factor),
            0,
            size.padding + round(size.live_area_width * tri_factor),
            size.max_height,
        ),
        (
            size.padding + round(size.live_area_width * (1 - tri_factor)),
            0,
            size.padding + round(size.live_area_width * (1 - tri_factor)),
            size.max_height,
        ),
        (
            0,
            size.max_height / 2,
            size.max_width,
            size.max_height / 2,
        ),
        (
            0,
            size.padding + round(size.live_area_height * tri_factor),
            size.max_width,
            size.padding + round(size.live_area_height * tri_factor),
        ),
        (
            0,
            size.padding + round(size.live_area_height * (1 - tri_factor)),
            size.max_width,
            size.padding + round(size.live_area_height * (1 - tri_factor)),
        ),
        (
            0,
            0,
            size.max_width,
            size.max_height,
        ),
        (
            0,
            size.max_height,
            size.max_width,
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

    # sqr_width = round(size.max_width * 152 / 192)
    sqr_width = size.square_width
    corner_radius = size.corner_radius  
    corner_offset = size.corner_offset
    # rect_wide = round(size.max_height * 176 / 192)
    # rect_short = round(size.max_width * 128 / 192)
    rect_short = size.short_side
    rect_wide =  size.cir_radius * 2
    # cir_radius = size.max_width * (88 / 192)    
    cir_radius = size.cir_radius    
    cir_small_radius = round(size.max_width * (40 / 192) )  

    # if size.pixel_width == 8:
        # sqr_width = 6
        # corner_radius = .5
        # corner_offset = 1.5
        # rect_wide = 8
        # rect_short = 6
        # cir_radius = 4
        # cir_small_radius = 2
    # elif size.pixel_width < PIXEL_WIDTH_SMALL:
        # sqr_width = 14
        # corner_radius = 1.5
        # corner_offset = 4.5
        # rect_wide = 16
        # rect_short = 12
        # cir_radius = 8 
        # cir_small_radius = 4
        
    # elif size.pixel_width == PIXEL_WIDTH_SMALL:
        # corner_radius = CORNER_RADIUS_SMALL
        # sqr_width = 18        
        # corner_radius = CORNER_RADIUS_SMALL
        # corner_offset = 5
        # rect_wide = 20
        # rect_short = round(size.max_width * 128 / 192)
        # cir_radius = 10 
        # cir_small_radius = size.max_width * (40 / 192) 
    
    # elif size.pixel_width == 192:
        # corner_radius = 4 * CORNER_RADIUS 
        # corner_offset = size.max_width * 1 / 6
        # cir_small_radius = 4 * size.max_width * (40 / 192) 
       

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
                corner_radius=corner_radius, 
                size=size
            )
        )

    keyline_circles = (
        # cx, cy, r
        (size.max_width / 2, size.max_width / 2, cir_radius, circle),
        (size.max_width / 2, size.max_width / 2, cir_small_radius, False),
        (corner_offset, corner_offset, corner_radius , False),
        (size.max_width - corner_offset, corner_offset, corner_radius , False),
        (corner_offset, size.max_height - corner_offset, corner_radius, False),
        (size.max_width - corner_offset, size.max_height - corner_offset, corner_radius, False),
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
        f'<svg viewBox="0 0 {size.max_width} {size.max_height}" width="{size.view_width}" height="{size.view_height}"'
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


def keyline_image(square=False, wide=False, tall=False, circle=False, size=None):
    """Build keyline Box svg."""
    lines = []

    lines.append(svg_header(size=size))
    lines.append(build_grid_lines(size=size))
    lines.append(build_keyline(square=square, wide=wide, tall=tall, circle=circle, size=size))
    lines.append(build_border(size=size))
    lines.append(svg_footer())

    return lines


def logo_image(size=None):
    """Build Logo svg."""
    COLOR_RED = "#CE1126"
    COLOR_BLUE = "#002654"

    # RED_WIDTH = 1. / 3
    # RED_INSIDE_POINT_WIDTH = 1. / 6
    # red_polygon = [(0, 33.33), (16.66, 83.33), (66.66, 100), (0, 100)]

    # BLUE_POINT_TOP = 2. / 3
    # BLUE_POINT_LEFT = 1. / 3

    # 16x16
    # 32x32
    # 48x48
    # 256x256

    # if size.pixel_width == 8:
    #     width_ratio = 1
    # elif size.pixel_width == 20:
    #     width_ratio = 16 / 20
    # elif size.pixel_width == PIXEL_WIDTH_SMALL:
    #     width_ratio = 20 / 24
    # elif size.pixel_width == 60:
    #     width_ratio = 54 / 60
    # else:
    #     width_ratio = 44 / 48

    # Set bounds for image
    # max_width = round(size.max_width * width_ratio)
    # max_height = round(size.max_height * width_ratio)
    live_area_width = size.live_area_width
    live_area_height = size.live_area_width
    x_offset = size.padding
    y_offset = size.padding

    # red_width =  round(live_area_width - (live_area_width * RED_WIDTH))
    red_width =  round(live_area_width - (live_area_width * size.tri_factor))
    red_height =  red_width
    # red_inside_point = round(live_area_width * RED_INSIDE_POINT_WIDTH)
    red_inside_point = round(live_area_width *  size.tri_factor / 2)

    # Blue Polygon
    # blue_point_top = round(live_area_height * BLUE_POINT_TOP)
    # blue_point_left = round(live_area_height * BLUE_POINT_LEFT)
    blue_point_top = round(live_area_height - live_area_height * size.tri_factor )
    blue_point_left = round(live_area_height * size.tri_factor)

    # if size.pixel_width == size.SYSTEM_ICON_LAYOUT_SIZE:
    #     blue_point_top = blue_point_top + 1
    #     blue_point_left = blue_point_left - 1
    # if size.pixel_width == 40:
    #     blue_point_top = blue_point_top + 1
    #     blue_point_left = blue_point_left - 1


    
    lines = []

    lines.append(svg_header(size=size))
    lines.append(build_grid_lines(size=size))
    lines.append(build_keyline(size=size))

    # Background
    lines.append(
        f'\t<rect x="0" y="0" width="100%" height="100%" stroke="None" fill="{COLOR_WHITE}" />'
    )    
    lines.append(
        f'\t<polygon stroke="None" fill="{COLOR_RED}" points="{x_offset},{y_offset + live_area_height - red_height} {x_offset + red_inside_point},{y_offset + live_area_height - red_inside_point} {x_offset + red_width},{y_offset + live_area_height} {x_offset},{y_offset + live_area_height}" />'
    )    
    lines.append(
        f'\t<polygon stroke="None" fill="{COLOR_BLUE}" points="{x_offset},{y_offset} {x_offset + live_area_width},{y_offset} {x_offset + live_area_width},{y_offset + live_area_height} {x_offset + blue_point_left},{y_offset + blue_point_top}" />'
    )

    # Border

    lines.append(build_border(size))
    lines.append(svg_footer())

    return lines


def save_svg(file_name, svg_string):
    """Save svg to file."""
    with open(file_name, "w", encoding="utf-8") as svg_file:
        svg_file.writelines("\n".join(svg_string))


def main(image, highlight, size, save):
    """Build logo image."""

    size = Dimensions(int(size))

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

    if save:
        file_name = file_name.replace('.svg', f"_{size.pixel_width}.svg")
    
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
        choices=[8, 20, 24, 29, 38, 40, 48, 58, 60, 76, 80, 87, 114, 120, 152, 167, 180, 192, 1024],
        type=int,
        default="48"
    )
    parser.add_argument(
        "--save",
        help='Save the image to a new filename,'
    )

    args = parser.parse_args()

    print(args.image, args.highlight, args.size, args.save)
    main(args.image, args.highlight, args.size, args.save)
