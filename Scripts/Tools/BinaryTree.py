from typing import Callable


class Node:
    def __init__(self, item):
        self.item = item
        self.left_child = None  # smaller
        self.right_child = None  # greater


class BinaryTree:
    '''排序二元樹'''

    def __init__(self, key: Callable = lambda item: item):
        '''
        key是從存入的東西中

        取的要比較的值的方法

        預設是直接回傳存入的東西
        '''
        self.root = None
        self.value = key

    def insert(self, item):
        # 判斷tree是否為空
        if self.root == None:
            self.root = Node(item)
        else:
            self._insert(item, self.root)

    def _insert(self, item, cur_node):
        if self.value(item) < self.value(cur_node.item):
            if cur_node.left_child == None:
                cur_node.left_child = Node(item)
            else:
                self._insert(item, cur_node.left_child)

        else:
            if cur_node.right_child == None:
                cur_node.right_child = Node(item)
            else:
                self._insert(item, cur_node.right_child)

    def get_list(self):
        if self.root != None:
            return self._get_list(self.root)
        return []

    def _get_list(self, cur_node) -> list:
        if cur_node != None:
            return [*self._get_list(cur_node.left_child),
                    cur_node.item,
                    *self._get_list(cur_node.right_child)]
        return []

    def clear(self):
        self.root = None


if __name__ == "__main__":

    class test_item:
        def __init__(self, x, y) -> None:
            self.xy = (x, y)

    def get_x(item: test_item):
        return item.xy[0]

    def get_y(item: test_item):
        return item.xy[1]

    def fill_tree(tree, num_elems=10, max_int=50):
        from random import randint
        for _ in range(num_elems):  # 10個 value
            item = test_item(randint(0, max_int), randint(
                0, max_int))  # 隨機0~50(不含50)的值
            tree.insert(item)

    bt = BinaryTree(get_y)
    fill_tree(bt)
    for item in bt.get_list():
        print(item.xy)
    bt.clear()
    print(bt.get_list())
