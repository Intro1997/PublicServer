from tools.vec import Vec2D


class Box:
    def __init__(self, left_top_corner=Vec2D(), right_bottom_corner=Vec2D()):
        self.left_top_corner = left_top_corner
        self.right_bottom_corner = right_bottom_corner

    def has_position(self, pos: Vec2D):
        # return self._x_in_box(pos.x) and self._y_in_box(pos.y)
        x = pos.x
        y = pos.y
        return (self.left_top_corner.x <= x and x <= self.right_bottom_corner.x)\
            and (self.left_top_corner.y <= y and y <= self.right_bottom_corner.y)

    def to_string(self):
        return f"Box: left_top_corner {self.left_top_corner.to_string()}, right_bottom_corner {self.right_bottom_corner.to_string()}"

    def _x_in_box(self, x):
        return self.left_top_corner.x <= x and x <= self.right_bottom_corner.x

    def _y_in_box(self, y):
        return self.left_top_corner.y <= y and y <= self.right_bottom_corner.y
