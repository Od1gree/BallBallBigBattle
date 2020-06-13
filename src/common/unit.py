class Unit(object):
    TYPE_UNIT = 0
    TYPE_BODY = 1
    TYPE_FOOD = 2
    TYPE_WALL = 3

    def __init__(self, x:int, y:int):
        self._x = x
        self._y = y
        self._type = self.TYPE_UNIT
    
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
    
    def get_position(self) -> tuple[int, int]:
        return self._x, self._y


class Body(Unit):
    def __init__(self, x: int, y: int, prev=None, nxt=None):
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