import overpy


class Node:
    _node: overpy.Node

    def __init__(self, node: overpy.Node):
        self._node = node
