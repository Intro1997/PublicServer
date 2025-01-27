from tools.vec import Vec2D, Vec3D, Vec4D, Vec2dMap, vec_from_tuple
from tools.box import Box, TupleBox
from PIL import Image
from typing import List, Tuple
from queue import Queue
from tools.edge_finder import AlphaSpriteEdgeStartFinder


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


def check_pos_valid(image: Image, pos: Vec2D):
    width, height = image.size
    if pos.x < 0 or pos.y < 0:
        return False
    elif pos.x >= width or pos.y >= height:
        return False
    return True


def check_pixel_valid(pixel: Vec3D | Vec4D, invalid_color: Vec3D | Vec4D) -> bool:
    p_cnt = pixel.channel_count
    i_cnt = invalid_color.channel_count

    if p_cnt < 3 or i_cnt < 3:
        return False
    elif i_cnt < p_cnt:
        return not invalid_color.equals_to(pixel)
    return not pixel.equals_to(invalid_color) and pixel.w != 0


def is_edge_pixel(image: Image, pixel_pos: Vec2D, invalid_color: Vec3D | Vec4D) -> bool:
    # pixel_vec = vec_from_tuple(image.getpixel((pixel_pos.to_tuple())))
    image_mode = image.mode
    t = image.getpixel((pixel_pos.x, pixel_pos.y))
    if image_mode == "RGBA":
        pixel_vec = Vec4D(t[0], t[1], t[2], t[3])
    elif image_mode == "RGB":
        pixel_vec = Vec3D(t[0], t[1], t[2])
    else:
        raise f"Unsupport image mode {image_mode}"

    if not check_pixel_valid(pixel_vec, invalid_color):
        return False

    valid_pixel_cnt = 0

    image_mode = image.mode
    IMG_MODE_RGBA = 1
    IMG_MODE_RGB = 2
    if image_mode == "RGBA":
        image_mode = IMG_MODE_RGBA
    elif image_mode == "RGB":
        image_mode = IMG_MODE_RGB
    else:
        raise f"Unsupport image mode {image_mode}"

    for x in range(-1, 2):
        for y in range(-1, 2):
            curr_pos = Vec2D(pixel_pos.x+x, pixel_pos.y+y)
            if curr_pos.equals_to(pixel_pos):
                continue
            # t = image.getpixel(curr_pos.to_tuple())
            t = image.getpixel((curr_pos.x, curr_pos.y))
            pixel = None
            if image_mode == IMG_MODE_RGBA:
                pixel = Vec4D(t[0], t[1], t[2], t[3])
            else:
                pixel = Vec3D(t[0], t[1], t[2])

            if check_pos_valid(image, curr_pos) and check_pixel_valid(pixel, invalid_color):
                valid_pixel_cnt += 1

    return valid_pixel_cnt > 0 and valid_pixel_cnt < 8


def get_edge_pixel_poses_in_surround(image: Image, center_pos: Vec2D, invalid_color: Vec3D | Vec4D) -> List[Vec2D]:
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
            curr_pos = Vec2D(center_pos.x + x, center_pos.y + y)
            if curr_pos.equals_to(center_pos):
                continue
            if check_pos_valid(image, curr_pos) and is_edge_pixel(image, curr_pos, invalid_color):
                edge_pixel_poses.append(curr_pos)

    return edge_pixel_poses


def get_single_sprite_box_coord(image: Image, a_edge_pixel_pos: Vec2D, background_color: Vec3D | Vec4D = Vec4D(0, 0, 0, 0)) -> Box:
    """
    Get bounding box of single sprite in image by given any edge pixel position in this sprite.

    Parameters:
    image: Image object contains a sprite.
    a_edge_pixel_pos: Any edge pixel position on sprite.
    background_color: The color will not be recognized as edge.

    Return:
    Union[Vec2D, Vec2D]: A list of [left_top_corner_position, right_bottom_corner_position]
    Negative return value, exp:(-1, -1), means split failed.
    """
    # given negative value represent invalid coordinate
    ltc_pos = Vec2D(-1, -1)  # ltc: left top corner
    rbc_pos = Vec2D(-1, -1)  # rbc: right bottom corner
    if not check_pos_valid(image, a_edge_pixel_pos):
        print(f'Inavlid edge pos {a_edge_pixel_pos.to_string()}')
        return (ltc_pos, rbc_pos)
    ltc_pos = Vec2D(a_edge_pixel_pos.x, a_edge_pixel_pos.y)
    rbc_pos = Vec2D(a_edge_pixel_pos.x, a_edge_pixel_pos.y)

    edge_queue = Queue()
    edge_queue.put(a_edge_pixel_pos)
    passed_map = Vec2dMap()
    passed_map.set(a_edge_pixel_pos, True)
    invalid_color = background_color

    while not edge_queue.empty():
        center_pixel_pos = edge_queue.get()
        edge_pixel_poses = get_edge_pixel_poses_in_surround(
            image, center_pixel_pos, invalid_color)
        for i in range(0, len(edge_pixel_poses)):
            p_pos = edge_pixel_poses[i]
            if not passed_map.has(p_pos):
                passed_map.set(p_pos, True)
                edge_queue.put(p_pos)
                ltc_pos.x = min(ltc_pos.x, p_pos.x)
                ltc_pos.y = min(ltc_pos.y, p_pos.y)
                rbc_pos.x = max(rbc_pos.x, p_pos.x)
                rbc_pos.y = max(rbc_pos.y, p_pos.y)

    return Box(ltc_pos, rbc_pos)


class AlphaSpriteSpliter:
    """
    This sprite spliter can only deal with RGBA image and auto convert alpha
    channel of RGB image to 255.

    If the alpha channel of image is 0, it will be treated as background; 
    otherwise it will be treated as edge.
    """

    def __init__(self, image_path: str):
        self._image = self._load_image(image_path)
        self._image_pixel = self._image.load()
        self._image_size = (self._image.width, self._image.height)
        self._edge_finder = AlphaSpriteEdgeStartFinder(self._image)

    def get_sprite_boxes(self) -> List[TupleBox]:
        sprite_boxes = []
        if self._image is not None:
            while not self._edge_finder.is_end():
                edge_start_pos = self._edge_finder.get_new_edge_start_pos()
                if edge_start_pos is None:
                    break

                box = self.get_single_sprite_box_coord(edge_start_pos)
                self._edge_finder.add_ignore_area(box)

                sprite_boxes.append(box)
        return sprite_boxes

    def _load_image(self, image_path: str):
        image = None
        try:
            image = Image.open(image_path).convert("RGBA")
        except Exception as e:
            print(f"Open image {image_path} failed.", e)
        finally:
            return image

    def get_single_sprite_box_coord(self, a_edge_pixel_pos: Tuple[int, int]) -> Box | None:
        """
        Description:
            Get bounding box of single sprite in image by given any edge pixel position in this sprite.

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

        return TupleBox(ltc_pos, rbc_pos)

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
