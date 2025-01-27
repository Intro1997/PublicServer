import sys  # noqa
sys.path.append("..")  # noqa


from PIL import Image, ImageDraw
from tools.box import Box


def draw_box(image: Image, left_top_pos: tuple, right_bottom_pos: tuple, color, line_width):
    draw = ImageDraw.Draw(image)
    draw.rectangle([left_top_pos, right_bottom_pos],
                   outline=color, width=line_width)
    # image.save("draw_box_output.png")


def draw_box_tuple(image: Image, box: Box, color: tuple, line_width: int):
    draw = ImageDraw.Draw(image)
    draw.rectangle([box.left_top_corner, box.right_bottom_corner],
                   outline=color, width=line_width)
    # image.save("draw_box_output.png")
