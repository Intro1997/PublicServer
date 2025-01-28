from typing import Tuple


class Box:
    def __init__(self, left_top_corner: Tuple[int, int],
                 right_bottom_corner: Tuple[int, int]):
        self.left_top_corner = left_top_corner
        self.right_bottom_corner = right_bottom_corner

    def to_string(self):
        return f"Box: left_top_corner {str(self.left_top_corner)}, right_bottom_corner {str(self.right_bottom_corner)}"
