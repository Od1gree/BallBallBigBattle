from typing import List, Dict, Tuple
import json

from .unit import *
from .snake import ReadOnlySnake


class Map(object):
    def __init__(self, size_x=50, size_y=50, wall_surround=True):
        self.SIZE_X = size_x
        self.SIZE_Y = size_y
        self._snake_dic = {}
        self._unit_dic: Dict[Tuple[int, int], List[Unit]] = {(x, y): []
                                                             for y in range(self.SIZE_Y) for x in range(self.SIZE_X)}
        # TODO: 确定FoodList与WallList存储的内容
        self._wall_list = []
        self._food_set = set()
        if wall_surround:
            for y in range(self.SIZE_Y):
                self._add_wall(0, y)
                self._add_wall(self.SIZE_X-1, y)

            # 注意四个角不能重复生成
            for x in range(1, self.SIZE_X-1):
                self._add_wall(x, 0)
                self._add_wall(x, self.SIZE_Y-1)

    def get_info(self):
        """
        注意这里返回值类型为字典的 **浅拷贝**
        :return: 蛇字典, unit字典
        """
        return self._snake_dic, self._unit_dic

    def init_from_json(self, json_str: str):
        map_dict = json.loads(json_str)
        self.SIZE_X = map_dict["SIZE_X"]
        self.SIZE_Y = map_dict["SIZE_Y"]
        for item in map_dict["snake_list"]:
            snake = ReadOnlySnake.import_from_dict(item, self.SIZE_X)
            self._snake_dic[snake.ID] = snake
            for unit in snake.get_body():
                self._unit_dic[unit.get_position()] = unit
        self._wall_list = map_dict["wall_list"]
        for unit in self._wall_list:
            self._unit_dic[unit.get_position()] = unit
        for unit in self._food_set:
            self._unit_dic[unit.get_position()] = unit
            self._food_set.add(unit)

    def export_to_str(self):
        converter = Unit.tuple_to_int(self.SIZE_X)
        map_dict = {"SIZE_X": self.SIZE_X,
                    "SIZE_Y": self.SIZE_Y,
                    "snake_list": [snake.to_dic(self.SIZE_X) for snake in self._snake_dic.values()],
                    "wall_list": [converter(x, y) for (x, y) in [wall.get_position() for wall in self._wall_list]],
                    "food_set": [converter(x, y) for (x, y) in [food.get_position() for food in self._food_set]]
                    }
        return json.dumps(map_dict)

    def _add_wall(self, x, y):
        new_wall = Wall(x, y)
        self._unit_dic[(x, y)].append(new_wall)
        self._wall_list.append(new_wall)


