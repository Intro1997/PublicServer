import sys  # noqa
sys.path.append("..")  # noqa

import traceback
from tools.sprite_splitter import AlphaSpriteSplitter
import time
from test_tools import draw_box, split_to_file


test_img_path = "assets/single_test0.png"


def class_test():
    start_pos = (12, 4)
    try:
        splitter = AlphaSpriteSplitter(test_img_path)
        start_time = time.time()
        box = splitter._get_single_sprite_box_coord(start_pos)
        end_time = time.time()
        print(f"class: splitter spend {(end_time - start_time):.10f}second")
        print(
            f"class: image is in ({str(box.left_top_corner)}, {str(box.right_bottom_corner)})")

    except Exception as e:
        print(f"Test failed! ", e)
        traceback.print_exc()


class_test()
