import sys  # noqa
sys.path.append("..")  # noqa

from tools.edge_finder import SpriteEdgeStartFinder
from tools.sprite_spliter import get_single_sprite_box_coord, AlphaSpriteSpliter
from PIL import Image
import traceback
from tools.vec import Vec4D
from test_tools import draw_box_vec, draw_box_tuple, split_to_file
import time

import cProfile
import pstats
from pstats import SortKey
import timeit

# img_path = "assets/multiple_test0.png"
img_path = "assets/multiple_test1.png"
# img_path = "assets/multiple_test2.png"
# img_path = "assets/tmp.png"


def api_test_func():
    try:
        image = Image.open(img_path)
        background_color = Vec4D(0, 0, 0, 0)
        ses_finder = SpriteEdgeStartFinder(image, background_color)
        sprite_boxes = []

        edge_find_time = 0
        create_box_time = 0

        while not ses_finder.is_end():
            start_time = time.time()
            edge_start_pos = ses_finder.get_new_edge_start_pos()
            end_time = time.time()
            edge_find_time += (end_time - start_time)

            if edge_start_pos is None:
                break

            start_time = time.time()
            box = get_single_sprite_box_coord(
                image, edge_start_pos, background_color)
            end_time = time.time()
            create_box_time += (end_time - start_time)
            ses_finder.add_ignore_area(box)

            sprite_boxes.append(box)

        for box in sprite_boxes:
            draw_box_vec(image, box, Vec4D(255, 0, 0, 255), 1)
        image.show()

    except Exception as e:
        print("Test failed. ", e)
        traceback.print_exc()


def class_test_func():
    spliter = AlphaSpriteSpliter(img_path)
    sprite_boxes = spliter.get_sprite_boxes()
    # return sprite_boxes

    # image = Image.open(img_path).convert("RGBA")
    # for box in sprite_boxes:
    #     draw_box_tuple(image, box, (255, 0, 0, 255), 1)
    # image.show()


# api_test_func()
# class_test_func()


# execution_time = timeit.timeit(api_test_func, number=1)
# print(f"Execution time: {execution_time} seconds")

# cProfile.run('api_test_func()', './test_profile.txt')
# p = pstats.Stats('./test_profile.txt')
# p.strip_dirs().sort_stats('cumtime').print_stats()

# execution_time = timeit.timeit(class_test_func, number=1)
# print(f"Execution time: {execution_time} seconds")

cProfile.run('class_test_func()', './test_profile.txt')
p = pstats.Stats('./test_profile.txt')
p.strip_dirs().sort_stats('cumtime').print_stats()
