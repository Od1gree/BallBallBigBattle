from .unit import Body
import logging


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
    def __init__(self, body_list: list):
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
    
    def _del_tail(self):
        # TODO: 核实是否真的需要在删除时记录蛇尾坐标
        # old_tail = self._tail.get_content()
        self._tail = self._tail.prev
        self._length -= 1
        if self._tail is None:
            logging.error("tail of snake is null, length of snake after delete tail is:" + str(self._length))
            return
        self._tail.next = None
        # return old_tail

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
            self._del_tail()
    
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

    def get_head(self) -> Body:
        return self._head.get_content()


class ReadOnlySnake(object):
    DIRECT_UP = 8
    DIRECT_DOWN = 2
    DIRECT_LEFT = 4
    DIRECT_RIGHT = 6

    def __init__(self, snake_id, body_queue:list, direction: int):
        self._body: _BodyQueue = _BodyQueue(body_queue)
        self._ttl: int = 10
        self._ID: str = snake_id
        self._isExist: bool = True
        self._direction: int = direction

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


class WritableSnake(ReadOnlySnake):
    def __init__(self, snake_id, body_queue: list, direction: int):
        super().__init__(snake_id, body_queue, direction)
        self._has_eat = False

    def calc_next_position(self):
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
            logging.error("无方向记录, id为:" + self._ID)
            exit(1)
        new_head = Body(current_head_x, current_head_y, nxt=current_head)
        self._body.step_on(body=new_head, had_eaten=self._has_eat)

    def die(self):
        self._isExist = False
        self._body = None


