from tools.vec import Vec2D
from typing import Tuple


class Box:
    def __init__(self, left_top_corner=Vec2D(), right_bottom_corner=Vec2D()):
        self.left_top_corner = left_top_corner
        self.right_bottom_corner = right_bottom_corner

    def has_position(self, pos: Vec2D):
        x = pos.x
        y = pos.y
        return (self.left_top_corner.x <= x and x <= self.right_bottom_corner.x)\
            and (self.left_top_corner.y <= y and y <= self.right_bottom_corner.y)

    def to_string(self):
        return f"Box: left_top_corner {self.left_top_corner.to_string()}, right_bottom_corner {self.right_bottom_corner.to_string()}"


class TupleBox:
    def __init__(self, left_top_corner: Tuple[int, int],
                 right_bottom_corner: Tuple[int, int]):
        self.left_top_corner = left_top_corner
        self.right_bottom_corner = right_bottom_corner

    def has_position(self, pos: Tuple[int, int]):
        x, y = pos
        return (self.left_top_corner[0] <= x and x <= self.right_bottom_corner[0])\
            and (self.left_top_corner[1] <= y and y <= self.right_bottom_corner[1])

    def to_string(self):
        return f"Box: left_top_corner {str(self.left_top_corner)}, right_bottom_corner {str(self.right_bottom_corner)}"
