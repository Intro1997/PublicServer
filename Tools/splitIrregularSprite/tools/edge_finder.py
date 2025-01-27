from PIL import Image
from tools.box import Box
from tools.vec import Vec2D, Vec3D, Vec4D, vec_from_tuple, common_equals
from typing import List

IMG_RGBA_MODE = 1
IMG_RGB_MODE = 2


class SpriteEdgeStartFinder:
    def __init__(self, image: Image, background_color: Vec3D | Vec4D = Vec4D(0, 0, 0, 0)):
        image_mode = image.mode
        if image_mode == 'RGBA':
            self._image_mode = IMG_RGBA_MODE
        elif image_mode == 'RGB':
            self._image_mode = IMG_RGB_MODE
        else:
            raise f"Unsupport format {image_mode}"

        self._image = image
        self._ignore_area: List[Box] = []  # list of Box
        self._sline_pos = Vec2D(0, 0)  # sline: scanner line
        img_size = image.size
        self._img_width = img_size[0]
        self._img_height = img_size[1]
        self._invalid_color = background_color

    def is_end(self) -> bool:
        return self._is_scan_end()

    def add_ignore_area(self, ignore_box: Box):
        self._ignore_area.append(ignore_box)

    def get_new_edge_start_pos(self) -> Vec2D:
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
        sl_x = self._sline_pos.x
        sl_y = self._sline_pos.y
        i_w = self._img_width - 1
        i_h = self._img_height - 1
        return sl_x == i_w and sl_y == i_h

    def _update_sline_pos(self):
        self._sline_pos.x += 1
        self._safe_clamp_pos()

    def _safe_clamp_pos(self):
        if self._sline_pos.x >= self._img_width:
            self._sline_pos.x = 0
            self._sline_pos.y += 1
            if self._sline_pos.y >= self._img_height:
                self._sline_pos.y -= 1

    def _update_sline_to_skip_box(self, box_id: int):
        if box_id < 0:
            return
        self._sline_pos.x = self._ignore_area[box_id].right_bottom_corner.x + 1
        self._safe_clamp_pos()

    def _is_scanner_in_ignore_area(self) -> int:
        box_idx = -1
        del_idx_list = []

        index = 0
        for box in self._ignore_area:
            if box.has_position(self._sline_pos):
                box_idx = index
                break
            elif box.right_bottom_corner.y < self._sline_pos.y:
                del_idx_list.append(index)
            index += 1

        # print(del_idx_list)
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

    def _is_pos_has_valid_color(self, pos: Vec2D):
        # t = self._image.getpixel(pos.to_tuple())
        t = self._image.getpixel((pos.x, pos.y))
        # pixel_vec = vec_from_tuple(t)
        if self._image_mode == IMG_RGBA_MODE:
            pixel_vec = Vec4D(t[0], t[1], t[2], t[3])
        else:
            pixel_vec = Vec3D(t[0], t[1], t[2])

        flag = (not common_equals(pixel_vec, self._invalid_color))
        if pixel_vec.channel_count == 4:
            return flag and pixel_vec.w != 0
        return flag
