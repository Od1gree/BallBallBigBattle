from typing import Tuple, Dict
import logging

from ..common.map import Map
from ..common.snake import WritableSnake
from ..common.unit import *

class ServerMap(Map):
    def __init__(self):
        super().__init__()

    def _add_food(self, x, y):
        new_food = Food(x, y)
        self._unit_dic[(x, y)].append(new_food)
        self._food_set.add(new_food)

    def _del_food(self, x, y):
        """

        :param x:
        :param y:
        :return:
        """
        old_list = self._unit_dic[(x, y)]
        new_list = []

        # 重新建立list, 并把food_set的相应unit删掉
        for unit in old_list:
            if unit.get_type() is unit.TYPE_FOOD:
                self._food_set.remove(unit)
            else:
                new_list.append(unit)

        self._unit_dic[(x, y)] = new_list

    def _del_body(self, body_del):
        """
        在删除body时, 确保body不被_QueueNode引用.
        :param body_del: 将要删除的body对象
        :return: None
        """
        x, y = body_del.get_position()
        new_list = []
        for unit in self._unit_dic[(x, y)]:
            if unit is body_del:
                continue
            else:
                new_list.append(unit)

        self._unit_dic[(x, y)] = new_list

    def _add_head(self, body_add):
        x, y = body_add.get_position()
        self._unit_dic[(x, y)].append(body_add)

    def _judge_eat_death(self, x, y) -> (bool, bool):
        """
        judge if a snake has eaten or death in a specific time slot
        :param x: 蛇头坐标x
        :param y: 蛇头坐标y
        :return: (is_eaten, is_death)
        """
        judge_list = self._unit_dic[(x, y)]
        num_body = 0
        num_food = 0
        for unit in judge_list:
            if unit.get_type() is Unit.TYPE_FOOD:
                num_food += 1
            elif unit.get_type() is Unit.TYPE_WALL:
                return False, True
            elif unit.get_type() is Unit.TYPE_BODY:
                num_body += 1
            else:
                logging.error("found unit type in list: %s" % str(unit))
                exit(1)
        return num_food > 0, num_body > 1

    def cal_map(self, direction_dic):
        """
        计算地图下一秒时的状态, 计算完成后返回地图信息.
        :param direction_dic: 存储方向的
        :return:
        """

        # step1 计算每条蛇的下一秒位置
        for snake_id in self._snake_dic:
            new_direct = None
            if snake_id in direction_dic:
                new_direct = direction_dic[snake_id]
            snake: WritableSnake = self._snake_dic[snake_id]
            tail, head = snake.calc_next_position(new_direct)
            if tail is not None:
                self._del_body(tail)
            self._add_head(head)

        # step2 更新蛇的吃食物和死亡状态
        dead_set = []
        for snake_id in self._snake_dic:
            # 利用字典浅拷贝特性直接修改Value
            current_snake = self._snake_dic[snake_id]
            x, y = current_snake.get_head().get_position()
            is_eat, is_dead = self._judge_eat_death(x, y)
            logging.debug("[cal_map] snake: %s, is_eaten: %s, is_dead: %s" % (snake_id, is_eat, is_dead))
            if is_eat:
                current_snake.set_eat()
            if is_dead:
                current_snake.set_dead()
                dead_set.append(snake_id)

        # step3 执行死亡, 从头后面一格开始转化为Food, 每次间隔一格
        for corpse_id in dead_set:
            corpse = self._snake_dic.pop(corpse_id)

            body_list = corpse.get_body()
            for unit in body_list[1::2]:
                x, y = unit.get_position()
                self._add_food(x, y)

            for unit in body_list:
                self._del_body(unit)
            corpse.execute_die()
