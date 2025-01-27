import sys  # noqa
sys.path.append("..")  # noqa

from tools.sprite_spliter import AlphaSpriteSpliter
from PIL import Image
from test_tools import draw_box_tuple

import cProfile
import pstats
from pstats import SortKey
import timeit

# img_path = "assets/multiple_test0.png"
# img_path = "assets/multiple_test1.png"
# img_path = "assets/multiple_test2.png"
img_path = "assets/tmp.png"


def class_test_func():
    spliter = AlphaSpriteSpliter(img_path)
    sprite_boxes = spliter.get_sprite_boxes()
    # return sprite_boxes

    image = Image.open(img_path).convert("RGBA")
    for box in sprite_boxes:
        draw_box_tuple(image, box, (255, 0, 0, 255), 1)
    image.show()


# api_test_func()
# class_test_func()

execution_time = timeit.timeit(class_test_func, number=1)
print(f"Execution time: {execution_time} seconds")

# cProfile.run('class_test_func()', './test_profile.txt')
# p = pstats.Stats('./test_profile.txt')
# p.strip_dirs().sort_stats('cumtime').print_stats()
