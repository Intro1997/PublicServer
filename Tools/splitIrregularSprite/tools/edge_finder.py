from PIL import Image
from tools.box import Box
from typing import List, Tuple


class AlphaSpriteEdgeStartFinder:
    """
    If the alpha channel of image is 0, it will be treated as background; 
    otherwise it will be treated as edge.
    """

    def __init__(self, image: Image):
        if not image or image is None:
            raise ValueError("Image object is invalid!")
        self._image_size = image.size
        self._image_pixel = image.convert("RGBA").load()
        self._ignore_area: List[Box] = []  # list of Box
        self._sline_pos: Tuple[int, int] = (0, 0)  # sline: scanner line
        img_size = image.size
        self._img_width = img_size[0]
        self._img_height = img_size[1]

    def is_end(self) -> bool:
        return self._is_scan_end()

    def add_ignore_area(self, ignore_box: Box):
        self._ignore_area.append(ignore_box)
        rx, ry = ignore_box.right_bottom_corner
        iw, ih = self._image_size
        if rx >= iw - 1 and ry >= ih - 1:
            self._sline_pos = (rx, ry)

    def get_new_edge_start_pos(self) -> Tuple[int, int]:
        while not self._is_scan_end():
            box_idx = self._is_scanner_in_ignore_area()
            if box_idx >= 0:
                self._update_sline_to_skip_box(box_idx)
                continue
            if self._is_pos_has_valid_color(self._sline_pos):
                return self._sline_pos
            self._update_sline_pos()
        return None

    def _is_scan_end(self) -> bool:
        sl_x, sl_y = self._sline_pos
        i_w = self._img_width - 1
        i_h = self._img_height - 1
        return sl_x == i_w and sl_y == i_h

    def _update_sline_pos(self):
        x, y = self._sline_pos
        self._sline_pos = self._get_clamp_pos(x + 1, y)

    def _get_clamp_pos(self, x: int, y: int) -> Tuple[int, int]:
        retx, rety = x, y
        if retx >= self._img_width:
            retx = 0
            rety += 1
            if rety >= self._img_height:
                rety -= 1
        return (retx, rety)

    def _update_sline_to_skip_box(self, box_id: int):
        if box_id < 0:
            return

        rbc_x, _ = self._ignore_area[box_id].right_bottom_corner
        self._sline_pos = self._get_clamp_pos(rbc_x+1, self._sline_pos[1])

    def _is_scanner_in_ignore_area(self) -> int:
        box_idx = -1
        del_list = []

        index = 0
        x, y = self._sline_pos
        for box in self._ignore_area:
            if (box.left_top_corner[0] <= x and x <= box.right_bottom_corner[0])\
                    and (box.left_top_corner[1] <= y and y <= box.right_bottom_corner[1]):
                box_idx = index
                break
            elif box.right_bottom_corner[1] < self._sline_pos[1]:
                del_list.append(box)
            index += 1
        for box in del_list:
            self._ignore_area.remove(box)

        return box_idx

    def _is_pos_has_valid_color(self, pos: Tuple[int, int]):
        pixel_tuple: Tuple[int, int, int, int] = self._image_pixel[pos]
        return pixel_tuple[3] != 0
