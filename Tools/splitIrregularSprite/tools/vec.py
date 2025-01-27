
def vec_from_tuple(obj: tuple):
    obj_l = list(obj)
    while len(obj_l) < 2:
        obj_l.append(0)

    if len(obj_l) == 2:
        return Vec2D(*obj_l)
    elif len(obj_l) == 3:
        return Vec3D(*obj_l)
    elif len(obj_l) == 4:
        return Vec4D(*obj_l)
    else:
        return Vec2D(0, 0)


class Vec2D:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.channel_count = 2

    def equals_to(self, vec2d):
        return self.x == vec2d.x and self.y == vec2d.y

    def to_tuple(self) -> tuple:
        return (self.x, self.y)

    def __add__(self, vec2d):
        return Vec2D(self.x + vec2d.x, self.y + vec2d.y)

    def to_string(self):
        return f"{self.x, self.y}"

    def to_tuple(self):
        return (self.x, self.y)


class Vec3D(Vec2D):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y)
        self.z = z
        self.channel_count = 3

    def equals_to(self, vec3d):
        # return super().equals_to(vec3d) and (self.z == vec3d.z)
        return self.x == vec3d.x and\
            self.y == vec3d.y and\
            self.z == vec3d.z

    def to_tuple(self) -> tuple:
        return (self.x, self.y, self.z)

    def __add__(self, vec3d):
        return Vec2D(self.x + vec3d.x, self.y + vec3d.y, self.z + vec3d.z)

    def to_string(self):
        return f"{self.x, self.y, self.z}"

    def to_tuple(self):
        return (self.x, self.y, self.z)


class Vec4D(Vec3D):
    def __init__(self, x=0, y=0, z=0, w=0):
        super().__init__(x, y, z)
        self.w = w
        self.channel_count = 4

    def equals_to(self, vec4d):
        # return super().equals_to(vec4d) and (self.w == vec4d.w)
        return self.x == vec4d.x and \
            self.y == vec4d.y and \
            self.z == vec4d.z and \
            self.w == vec4d.w

    def to_tuple(self) -> tuple:
        return (self.x, self.y, self.z, self.w)

    def __add__(self, vec4d):
        return Vec4D(self.x + vec4d.x, self.y + vec4d.y, self.z + vec4d.z, self.w + vec4d.w)

    def to_string(self):
        return f"{self.x, self.y, self.z, self.w}"

    def to_tuple(self):
        return (self.x, self.y, self.z, self.w)


class Vec2dMap:
    def __init__(self):
        self.value_table = {}

    def set(self, vec2d: Vec2D, value):
        if not self.value_table.get(vec2d.x):
            self.value_table[vec2d.x] = {}
        self.value_table[vec2d.x][vec2d.y] = value

    def has(self, vec2d: Vec2D) -> bool:
        if self.value_table.get(vec2d.x) and self.value_table[vec2d.x].get(vec2d.y):
            return True
        return False

    def get(self, vec2d: Vec2D):
        if self.has(vec2d):
            return self.value_table[vec2d.x][vec2d.y]
        return None

    def delete(self, vec2d: Vec2D):
        if self.has(vec2d):
            self.value_table.pop(vec2d.x)


def common_equals(left: Vec2D | Vec3D | Vec4D, right: Vec2D | Vec3D | Vec4D) -> bool:
    if left.channel_count < right.channel_count:
        return left.equals_to(right)
    return right.equals_to(left)
