"""
二叉树模块
"""

from obj import BinaryNode as BNode
from queue_stack import Queue


class BaseTree:
	"""树基类接口"""

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


class BinaryTree(BaseTree):
	"""二叉树类"""

	def __init__(self):
		super(BinaryTree, self).__init__()

	def add(self, elem):
		"""广度优先法插入元素"""

		node = BNode(elem=elem)

		if self.is_empty():
			self.set_root(root_node=node)
			return

		queue = Queue()
		queue.enqueue(self.root())

		while not queue.is_empty():

			cur_node = queue.dequeue()

			if cur_node.left is None:
				cur_node.left = node
				return
			else:
				queue.enqueue(cur_node.left)

			if cur_node.right is None:
				cur_node.right = node
				return
			else:
				queue.enqueue(cur_node.right)

	def breadth_travel(self):
		"""广度遍历/层次遍历二叉树"""

		# 空树情况
		if self.is_empty():
			return

		# 一般情况
		queue = Queue()
		queue.enqueue(self.root())

		while not queue.is_empty():
			cur_node = queue.dequeue()
			print(cur_node, end=" ")
			if cur_node.left is not None:
				queue.enqueue(cur_node.left)
			if cur_node.right is not None:
				queue.enqueue(cur_node.right)
		print()

	def preorder_travel(self, node):
		"""前序遍历二叉树"""

		if node is None:
			return
		print(node, end=" ")
		self.preorder_travel(node=node.left)
		self.preorder_travel(node=node.right)

	def inorder_travel(self, node):
		"""中序遍历二叉树"""

		if node is None:
			return
		self.inorder_travel(node=node.left)
		print(node, end=" ")
		self.inorder_travel(node=node.right)

	def postorder_travel(self, node):
		"""后序遍历二叉树"""

		if node is None:
			return
		self.postorder_travel(node=node.left)
		self.postorder_travel(node=node.right)
		print(node, end=" ")


if __name__ == '__main__':
	tree = BinaryTree()
	for i in range(10):
		print(i, i, i)
		tree.add(i)
	tree.breadth_travel()
	tree.preorder_travel(tree.root())
	print()
	tree.inorder_travel(tree.root())
	print()
	tree.postorder_travel(tree.root())
	print()
	pass

