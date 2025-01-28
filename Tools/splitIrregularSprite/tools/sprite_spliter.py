from tools.box import Box
from PIL import Image, ImageDraw
from typing import List, Tuple
from queue import Queue
from tools.edge_finder import AlphaSpriteEdgeStartFinder
import os
from enum import Enum


class Tuple2DMap:
    def __init__(self):
        self.value_table = {}

    def set(self, tuple2d: Tuple[float, float], value):
        if not self.value_table.get(tuple2d[0]):
            self.value_table[tuple2d[0]] = {}
        self.value_table[tuple2d[0]][tuple2d[1]] = value

    def has(self, tuple2d: Tuple[float, float]) -> bool:
        if self.value_table.get(tuple2d[0]) and \
                self.value_table[tuple2d[0]].get(tuple2d[1]):
            return True
        return False

    def get(self, tuple2d: Tuple[float, float]):
        if self.has(tuple2d):
            return self.value_table[tuple2d[0]][tuple2d.y]
        return None

    def delete(self, tuple2d: Tuple[float, float]):
        if self.has(tuple2d):
            self.value_table.pop(tuple2d[0])


class SpliterAlgorithm(Enum):
    """
    Description
        EDGE_DETECT: A stricter algorithm that split any individual pixels as a sprite. But slower.
        SPRITE_SCAN: A more relaxed algorithm will treat two areas separated by a transparent line as 
                     two sprites; this makes it possible for two parts separated by a diagonal line to 
                     be treated as one sprite。

    """
    EDGE_DETECT = 0
    SPRITE_SCAN = 1


class AlphaSpriteSpliter:
    """
    This sprite spliter can only deal with RGBA image and auto convert alpha
    channel of RGB image to 255.

    If the alpha channel of image is 0, it will be treated as background; 
    otherwise it will be treated as edge.
    """

    def __init__(self, image_path: str):
        self._image_path = image_path
        self._image = self._load_image(image_path)
        self._image_pixel = self._image.load()
        self._image_size = (self._image.width, self._image.height)
        self._edge_finder = AlphaSpriteEdgeStartFinder(self._image)
        self._last_sprite_boxes: List[Box] | None = None

    def show_split_result(self, color: Tuple[int, int, int, int],
                          algm: SpliterAlgorithm = SpliterAlgorithm.SPRITE_SCAN):
        self.show_split_result_by_boxes(self.get_sprite_boxes(algm), color)

    def show_split_result_by_boxes(self, boxes: List[Box], color: Tuple[int, int, int, int]):
        image = self._load_image(self._image_path)
        for box in boxes:
            draw = ImageDraw.Draw(image)
            draw.rectangle([box.left_top_corner, box.right_bottom_corner],
                           outline=color, width=1)
        image.show()

    def save_sprites(self, save_dir: str, file_prefix: str = "sprite",
                     algm: SpliterAlgorithm = SpliterAlgorithm.SPRITE_SCAN):
        if self._image is None:
            print(f"Open image {self._image_path} failed.")
            return

        self.save_sprites_by_boxes(save_dir,
                                   self.get_sprite_boxes(algm),  file_prefix)

    def save_sprites_by_boxes(self, save_dir: str, boxes: List[Box],  file_prefix: str = "sprite"):
        if boxes is None or len(boxes) == 0:
            print(f"Invalid or empty box")
            return
        if self._image is None:
            print(f"Open image {self._image_path} failed.")
            return
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
        file_idx = 0
        for box in boxes:
            right_border_corner = (
                box.right_bottom_corner[0] + 1, box.right_bottom_corner[1] + 1)
            cropped_image = self._image.crop(
                box.left_top_corner + right_border_corner)
            save_path = os.path.join(save_dir, f"{file_prefix}_{file_idx}.png")
            cropped_image.save(save_path)
            print(f"Save to file: {save_path}")
            file_idx += 1
        print(f"{file_idx} saved to {save_dir}")

    def get_sprite_boxes(self, algm: SpliterAlgorithm = SpliterAlgorithm.SPRITE_SCAN) -> List[Box]:
        sprite_boxes = self._last_sprite_boxes
        if self._image is not None and sprite_boxes is None:
            sprite_boxes = []
            while not self._edge_finder.is_end():
                edge_start_pos = self._edge_finder.get_new_edge_start_pos()
                if edge_start_pos is None:
                    break
                box = None
                if algm == SpliterAlgorithm.EDGE_DETECT:
                    box = self._get_single_sprite_box_coord_by_edge_detect(
                        edge_start_pos)
                else:
                    box = self._get_single_sprite_box_coord_by_sprite_scan(
                        edge_start_pos)
                self._edge_finder.add_ignore_area(box)

                sprite_boxes.append(box)
            self._last_sprite_boxes = sprite_boxes
        return sprite_boxes

    def _load_image(self, image_path: str):
        image = None
        try:
            image = Image.open(image_path).convert("RGBA")
        except Exception as e:
            print(f"Open image {image_path} failed.", e)
        finally:
            return image

    def _get_single_sprite_box_coord_by_sprite_scan(self, valid_pixel_pos: Tuple[int, int]) -> Box | None:
        """
        Description:
            Get bounding box of single sprite in image by given any colored pixel position in this sprite.
        It starts with a given pixel, find as the order of right, down, left, up, until it find the border
        of four direction. The border is defined as a line which has no colored pixel.

        Parameters:
            valid_pixel_pos: Any colored pixel in sprite

        Return:
            Box | None: Structure contains [left_top_corner_position, right_bottom_corner_position],
                        reutrn None if image load failed.
        """
        iw, ih = self._image_size
        scanner_data = {
            "pos": list(valid_pixel_pos),
            "w": 1,
            "h": 1
        }

        has_colored_edge = True
        while has_colored_edge:
            has_colored_edge = False
            has_colored_edge |= self._rect_scan_right(scanner_data)
            has_colored_edge |= self._rect_scan_down(scanner_data)
            has_colored_edge |= self._rect_scan_left(scanner_data)
            has_colored_edge |= self._rect_scan_up(scanner_data)
            if scanner_data['w'] >= iw and scanner_data['h'] >= ih:
                break
        if has_colored_edge:
            left_top_pos = tuple(scanner_data["pos"])
            return Box(left_top_pos, (left_top_pos[0] + scanner_data["w"] - 1,
                                      left_top_pos[1] + scanner_data['h'] - 1))

        left_top_pos = (scanner_data["pos"][0] + 1, scanner_data["pos"][1] + 1)
        right_bottom_pos = (
            scanner_data["w"]-2 + left_top_pos[0], scanner_data["h"]-2 + left_top_pos[1])
        return Box(left_top_pos, right_bottom_pos)

    def _rect_scan_right(self, scanner_data) -> bool:
        px, py = scanner_data["pos"]
        has_colored_edge = False

        if not self._check_pos_valid((px, py)):
            return has_colored_edge

        h = scanner_data["h"]
        iw, ih = self._image_size
        py_max = min(py + h, ih)

        x = px + scanner_data["w"]
        while x < iw:
            has_colored_pixel = False
            for y in range(py, py_max):
                if self._check_pixel_valid(self._image_pixel[(x, y)]):
                    has_colored_pixel = True
                    break
            if has_colored_pixel:
                has_colored_edge = True
                x += 1
            else:
                break
        scanner_data["w"] = x - px
        return has_colored_edge

    def _rect_scan_down(self, scanner_data) -> bool:
        px, py = scanner_data["pos"]
        has_colored_edge = False

        if not self._check_pos_valid((px, py)):
            return has_colored_edge

        w = scanner_data["w"]
        iw, ih = self._image_size
        px_max = min(px + w, iw)

        y = py + scanner_data["h"]
        while y < ih:
            has_colored_pixel = False
            for x in range(px, px_max):
                if self._check_pixel_valid(self._image_pixel[(x, y)]):
                    has_colored_pixel = True
                    break
            if has_colored_pixel:
                has_colored_edge = True
                y += 1
            else:
                break
        scanner_data["h"] = y - py
        return has_colored_edge

    def _rect_scan_left(self, scanner_data) -> bool:
        px, py = scanner_data["pos"]
        has_colored_edge = False

        if not self._check_pos_valid((px, py)):
            return has_colored_edge

        h = scanner_data["h"]
        _, ih = self._image_size
        py_max = min(py + h, ih)

        x = px
        while x > 0:
            has_colored_pixel = False
            for y in range(py, py_max):
                if self._check_pixel_valid(self._image_pixel[(x, y)]):
                    has_colored_pixel = True
                    break
            if has_colored_pixel:
                has_colored_edge = True
                x -= 1
            else:
                break
        scanner_data["pos"][0] = x
        scanner_data['w'] += px - x
        return has_colored_edge

    def _rect_scan_up(self, scanner_data) -> bool:
        px, py = scanner_data["pos"]
        has_colored_edge = False

        if not self._check_pos_valid((px, py)):
            return has_colored_edge

        w = scanner_data["w"]
        iw, _ = self._image_size
        px_max = min(px + w, iw)

        y = py
        while y > 0:
            has_colored_pixel = False
            for x in range(px, px_max):
                if self._check_pixel_valid(self._image_pixel[(x, y)]):
                    has_colored_pixel = True
                    break
            if has_colored_pixel:
                has_colored_edge = True
                y -= 1
            else:
                break
        scanner_data["pos"][1] = y
        scanner_data['h'] += py - y
        return has_colored_edge

    def _get_single_sprite_box_coord_by_edge_detect(self, a_edge_pixel_pos: Tuple[int, int]) -> Box | None:
        """
        Description:
            Get bounding box of single sprite in image by given any edge pixel position in this sprite.
        It starts with a edge pixel, finds all edge pixels of the edge pixel, then starts from thoes edge 
        pixels, and repeat until all edge pixels are passed.

        Parameters:
            a_edge_pixel_pos: Any edge pixel position on sprite.

        Return:
            Box | None: Structure contains [left_top_corner_position, right_bottom_corner_position],
                        reutrn None if image load failed.
        """
        if self._image is None:
            return None
        # given negative value represent invalid coordinate
        ltc_pos = (-1, -1)  # ltc: left top corner
        rbc_pos = (-1, -1)  # rbc: right bottom corner
        if not self._check_pos_valid(a_edge_pixel_pos):
            print(f'Inavlid edge pos {str(a_edge_pixel_pos)}')
            return (ltc_pos, rbc_pos)
        ltc_pos = (a_edge_pixel_pos[0], a_edge_pixel_pos[1])
        rbc_pos = (a_edge_pixel_pos[0], a_edge_pixel_pos[1])

        edge_queue: Queue[Tuple[int, int]] = Queue()
        edge_queue.put(a_edge_pixel_pos)
        passed_map = Tuple2DMap()
        passed_map.set(a_edge_pixel_pos, True)

        while not edge_queue.empty():
            center_pixel_pos = edge_queue.get()
            edge_pixel_poses = self._get_edge_pixel_poses_in_surround(
                center_pixel_pos)
            for i in range(0, len(edge_pixel_poses)):
                p_pos = edge_pixel_poses[i]
                if not passed_map.has(p_pos):
                    passed_map.set(p_pos, True)
                    edge_queue.put(p_pos)

                    p_x, p_y = p_pos
                    ltc_pos = (min(ltc_pos[0], p_x), min(ltc_pos[1], p_y))
                    rbc_pos = (max(rbc_pos[0], p_x), max(rbc_pos[1], p_y))

        return Box(ltc_pos, rbc_pos)

    def _check_pos_valid(self, pos: Tuple[int, int]):
        width, height = self._image_size
        x, y = pos
        if x < 0 or y < 0:
            return False
        elif x >= width or y >= height:
            return False
        return True

    def _check_pixel_valid(self, pixel: Tuple[int, int, int, int]) -> bool:
        return pixel[3] != 0

    def _is_edge_pixel(self, pixel_pos: Tuple[int, int]) -> bool:
        pixel_tuple = self._image_pixel[pixel_pos]
        if not self._check_pixel_valid(pixel_tuple):
            return False

        valid_pixel_cnt = 0

        for x in range(-1, 2):
            for y in range(-1, 2):
                curr_pos = (pixel_pos[0]+x, pixel_pos[1]+y)
                if curr_pos == pixel_pos:
                    continue
                if self._check_pos_valid(curr_pos) and self._check_pixel_valid(self._image_pixel[curr_pos]):
                    valid_pixel_cnt += 1

        return valid_pixel_cnt > 0 and valid_pixel_cnt < 8

    def _get_edge_pixel_poses_in_surround(self,
                                          center_pos: Tuple[int, int]) \
            -> List[Tuple[int, int]]:
        """
        Search pixel with valid color at following position of center position:
            - left top
            - top
            - right top
            - left
            - right
            - left bottom
            - bottom
            - right bottom
        """
        edge_pixel_poses = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                curr_pos = (center_pos[0]+x, center_pos[1]+y)
                if curr_pos == center_pos:
                    continue
                if self._check_pos_valid(curr_pos) and self._is_edge_pixel(curr_pos):
                    edge_pixel_poses.append(curr_pos)

        return edge_pixel_poses
