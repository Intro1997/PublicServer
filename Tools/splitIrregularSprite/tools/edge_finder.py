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
        # self._sline_pos.x += 1
        # self._safe_clamp_pos()
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
        # self._sline_pos.x = self._ignore_area[box_id].right_bottom_corner.x + 1
        # self._safe_clamp_pos()
        rbc_x, _ = self._ignore_area[box_id].right_bottom_corner
        self._sline_pos = self._get_clamp_pos(rbc_x+1, self._sline_pos[1])

    def _is_scanner_in_ignore_area(self) -> int:
        box_idx = -1
        del_idx_list = []

        index = 0
        for box in self._ignore_area:
            if box.has_position(self._sline_pos):
                box_idx = index
                break
            elif box.right_bottom_corner[1] < self._sline_pos[1]:
                del_idx_list.append(index)
            index += 1
        self._remove_ignore_area_by_list(del_idx_list)

        return box_idx

    def _remove_ignore_area_by_list(self, idx_list: List[int]):
        tmp_buffer = []
        # print(f"before {self._ignore_area}")
        for idx in range(len(self._ignore_area)):
            if idx not in idx_list:
                tmp_buffer.append(self._ignore_area[idx])
        self._ignore_area = tmp_buffer
        # print(f"after {self._ignore_area}")

    def _is_pos_has_valid_color(self, pos: Tuple[int, int]):
        # t = self._image.getpixel((pos.x, pos.y))
        # if self._image_mode == IMG_RGBA_MODE:
        #     pixel_vec = Vec4D(t[0], t[1], t[2], t[3])
        # else:
        #     pixel_vec = Vec3D(t[0], t[1], t[2])

        # flag = (not common_equals(pixel_vec, self._invalid_color))
        # if pixel_vec.channel_count == 4:
        #     return flag and pixel_vec.w != 0
        # return flag
        pixel_tuple: Tuple[int, int, int, int] = self._image_pixel[pos]
        return pixel_tuple[3] != 0
