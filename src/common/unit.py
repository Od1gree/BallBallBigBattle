from typing import Tuple

class Unit(object):
    TYPE_UNIT = 0
    TYPE_BODY = 1
    TYPE_FOOD = 2
    TYPE_WALL = 3

    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._type = self.TYPE_UNIT

    def __str__(self):
        if self._type is self.TYPE_UNIT:
            return "(%d, %d), TYPE=%d" % (self._y, self._x, self._type)
    
    def get_type(self) -> int:
        """
        type共四种
        Unit.TYPE_UNIT = 0
        Unit.TYPE_BODY = 1
        Unit.TYPE_FOOD = 2
        Unit.TYPE_WALL = 3
        :return: int类型的type
        """
        return self._type
    
    def get_position(self) -> Tuple[int, int]:
        return self._x, self._y

    @staticmethod
    def tuple_to_int(max_x):
        return lambda x, y: x + max_x * y

    @staticmethod
    def int_to_tuple(max_x):
        # 这里int()会向下取整
        return lambda i: (i % max_x, int(i/max_x))


class Body(Unit):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self._type = self.TYPE_BODY


class Food(Unit):
    def __init__(self, x:int, y:int):
        super().__init__(x, y)
        self._type = self.TYPE_FOOD


class Wall(Unit):
    def __init__(self, x:int, y:int):
        super().__init__(x, y)
        self._type = self.TYPE_WALL
