"""
二叉树模块
"""

from obj import BinaryNode as BNode


class BaseTree:
	"""二叉树基类接口"""

	def __init__(self):
		self._root = None

	def is_empty(self):
		"""判断是否是空树"""
		return self._root is None

	def root(self):
		"""获取root节点"""
		return self._root

	def left_child(self):
		"""获取root节点的左子树"""
		return self._root.left

	def right_child(self):
		"""获取root节点的右子树"""
		return self._root.right

	def set_root(self, root_node):
		"""设置root节点对象"""
		self._root = root_node

	def set_left(self, left):
		"""设置root节点的左指针"""
		self._root.left = left

	def set_right(self, right):
		"""设置root节点的右指针"""
		self._root.right = right

	pass


if __name__ == '__main__':
	tree = BaseTree()
	print(tree.is_empty())
	tree.set_root(BNode(2))
	tree.set_left(BNode(3))
	tree.set_right(BNode(4))
	print(tree.root())
	print(tree.root().right)
	pass

