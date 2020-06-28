from .unit import Body
import logging
from typing import List


class _QueueNode(object):
    def __init__(self, content=None, prev=None, nxt=None):
        self._content = content
        self.prev: _QueueNode = prev
        self.next: _QueueNode = nxt

    def is_head(self):
        return (self.prev is None) and (self.next is not None)

    def is_tail(self):
        return (self.prev is not None) and (self.next is None)

    def get_content(self):
        """
        :return: Body类型的浅拷贝
        """
        return self._content


class _BodyQueue(object):
    def __init__(self, body_list: List[Body]):
        self._length = len(body_list)
        if self._length == 0:
            logging.error("length of snake is 0")
            return
        self._head: _QueueNode = _QueueNode(content=body_list[0])
        step = self._head
        for node in body_list[1:]:
            step.next = _QueueNode(content=node, prev=step)
            step = step.next
        self._tail: _QueueNode = step

    def  __del__(self):
        logging.debug("[_BodyQueue] Destroying body.")
        current_node = self._head
        while current_node is not None:
            nxt_node = current_node.next
            current_node.next = current_node.prev = None
            current_node = nxt_node
    
    def _del_tail(self):
        old_tail = self._tail
        self._tail = self._tail.prev
        self._length -= 1
        if self._tail is None:
            logging.error("[_BodyQueue]tail of snake is null, length of snake after delete tail is:" + str(self._length))
            return
        self._tail.next = None
        return old_tail.get_content()

    def step_on(self, body: Body, had_eaten=False):
        """
        前进一步, 如果上一次行动吃过食物则不缩短尾巴
        :param body: 新的蛇头Body
        :param had_eaten: 上次行动是否吃过食物
        :return: 蛇尾Body
        """
        new_head = _QueueNode(content=body, nxt=self._head)
        self._head.prev = new_head
        self._head = new_head
        if had_eaten:
            return self._del_tail()
        else:
            return None
    
    def get_points(self, destory=False) -> list:
        """
        获得链表的所有点
        :return: list<Body>
        """
        cur = self._head
        point_list = []
        while cur is not None:
            point_list.append(cur.get_content())
            nxt_node = cur.next
            if destory:
                cur.prev = cur.next = None
            cur = nxt_node
        return point_list

    def get_tuples(self):
        result = []
        for item in self.get_points():
            result.append(item.get_position())
        return result

    def get_head(self) -> Body:
        return self._head.get_content()


class ReadOnlySnake(object):
    DIRECT_UP = 8
    DIRECT_DOWN = 2
    DIRECT_LEFT = 4
    DIRECT_RIGHT = 6

    def __init__(self, snake_id, body_list: List[Body], direction: int, is_exist: bool):
        """
        初始化蛇对象.
        :param snake_id: str类型, 代表蛇唯一性的ID
        :param body_list: List[Body]类型, 是Map类中_unit_dict的Body的引用
        :param direction: 在ReadOnlySnake的常量成员中定义: ReadOnlySnake.DIRECT_XXX
        """
        self._body: _BodyQueue = _BodyQueue(body_list)
        self._ttl: int = 10
        self.ID: str = snake_id
        self._is_exist: bool = is_exist
        self._direction: int = direction
        logging.debug("[ReadonlySnake] Initialize snake %s, direction %d" % (snake_id, direction))

    @staticmethod
    def import_from_dict(snake_dict, max_x):
        return ReadOnlySnake(snake_dict['id'],
                             body_list=[Body(x, y) for x, y in map(Body.int_to_tuple(max_x), snake_dict['body'])],
                             direction=snake_dict['direction'],
                             is_exist=snake_dict['is_exist'])

    def to_dict(self, max_x):
        """
        将成员转换为字典, 用于序列化.
        :param max_x: 地图X的宽度, 用于将坐标转化为int
        :return: 预序列化的字典
        """
        snake_dict = {"ttl": self._ttl,
                      "id": self.ID,
                      "body": list(map(Body.tuple_to_int(max_x), self._body.get_tuples())),
                      "direction": self._direction,
                      "is_exist": self._is_exist}
        return snake_dict

    def get_direction(self):
        return self._direction

    def get_body(self) -> list:
        """
        获得身体所有节点的对象列表
        :return: list[Body]
        """
        return self._body.get_points()

    def get_ttl(self):
        return self._ttl

    def get_head(self):
        """
        get head object
        :return: Body
        """
        return self._body.get_head()


class WritableSnake(ReadOnlySnake):
    def __init__(self, snake_id, body_queue: list, direction: int):
        super().__init__(snake_id, body_queue, direction, is_exist=True)
        self._is_eat = False

    def calc_next_position(self, new_direct):
        if new_direct is not None:
            self._direction = new_direct
        current_head = self._body.get_head()
        current_head_x, current_head_y = current_head.get_position()
        if self._direction is self.DIRECT_DOWN:
            current_head_y += 1
        elif self._direction is self.DIRECT_UP:
            current_head_y -= 1
        elif self._direction is self.DIRECT_LEFT:
            current_head_x -= 1
        elif self._direction is self.DIRECT_RIGHT:
            current_head_x += 1
        else:
            logging.error("无方向记录, id为:" + self.ID)
            exit(1)
        new_head = Body(current_head_x, current_head_y)
        logging.debug("[WritableSnake] snake %s step to (%d, %d)" % (self.ID, current_head_y, current_head_x))
        tail_del = self._body.step_on(body=new_head, had_eaten=self._is_eat)
        return tail_del, new_head

    def set_die(self):
        self._is_exist = False
        self._body = None

    def set_eat(self):
        self._is_eat = True

    def execute_die(self):
        self._is_exist = False
        self._body = None

