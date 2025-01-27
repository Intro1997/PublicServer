import sys  # noqa
sys.path.append("..")  # noqa

import traceback
from PIL import Image, ImageDraw
from tools.sprite_spliter import get_single_sprite_box_coord, AlphaSpriteSpliter
from tools.vec import Vec2D
import time
from test_tools import draw_box, split_to_file


test_img_path = "assets/single_test0.png"


def api_test():
    start_pos = Vec2D(12, 4)
    try:
        image = Image.open(test_img_path).convert("RGBA")
        start_time = time.time()
        bounding_box = get_single_sprite_box_coord(image, start_pos)
        end_time = time.time()
        print(f"api: spliter spend {(end_time - start_time):.10f}second")
        print(f"api: image is in ({bounding_box.left_top_corner.to_string()}, {
            bounding_box.right_bottom_corner.to_string()})")
        # draw_box(image, left_top_pos.to_tuple(),
        #          right_bottom_pos.to_tuple(), (255, 0, 0, 255), 1)
        # split_to_file(image, bounding_box.left_top_corner,
        #               bounding_box.right_bottom_corner)

    except Exception as e:
        print(f"Test failed! ", e)
        traceback.print_exc()


def class_test():
    start_pos = (12, 4)
    try:
        spliter = AlphaSpriteSpliter(test_img_path)
        start_time = time.time()
        box = spliter.get_single_sprite_box_coord(start_pos)
        end_time = time.time()
        print(f"class: spliter spend {(end_time - start_time):.10f}second")
        print(
            f"class: image is in ({str(box.left_top_corner)}, {str(box.right_bottom_corner)})")

    except Exception as e:
        print(f"Test failed! ", e)
        traceback.print_exc()


api_test()
class_test()
