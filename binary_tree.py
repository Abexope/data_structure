"""
二叉树模块
"""

from obj import BinaryNode as BNode
from obj import BinaryNode2 as BNode2
from queue_stack import Queue, Stack


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
		"""广度遍历/层次遍历二叉树，非递归法"""

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
		"""前序遍历二叉树，递归法"""

		if node is None:
			return
		print(node, end=" ")
		self.preorder_travel(node=node.left)
		self.preorder_travel(node=node.right)

	def inorder_travel(self, node):
		"""中序遍历二叉树，递归法"""

		if node is None:
			return
		self.inorder_travel(node=node.left)
		print(node, end=" ")
		self.inorder_travel(node=node.right)

	def postorder_travel(self, node):
		"""后序遍历二叉树，递归法"""

		if node is None:
			return
		self.postorder_travel(node=node.left)
		self.postorder_travel(node=node.right)
		print(node, end=" ")

	@staticmethod
	def preorder_travel2(node):
		"""前序遍历，非递归法"""
		stack = Stack()
		while node is not None or not stack.is_empty():
			while node is not None:            # 沿左分支下行
				print(node, end=" ")
				stack.push(node.right)          # 右分支入栈
				node = node.left                # 指针指向左分支
			node = stack.pop()                  # 遇到空树，回溯

	@staticmethod
	def inorder_travel2(node):
		"""中序遍历，非递归法"""
		stack = Stack()
		while node is not None or not stack.is_empty():
			while node is not None:
				stack.push(node)
				node = node.left if node.left is not None else node.right
			node = stack.pop()
			print(node, end=" ")
			node = node.right

	@staticmethod
	def postorder_travel2(node):
		"""后序遍历，非递归法"""
		stack = Stack()
		while node is not None or not stack.is_empty():
			while node is not None:     # 下行循环，直到栈顶元素为空
				stack.push(node)
				node = node.left if node.left is not None else node.right
			node = stack.pop()
			print(node, end=" ")
			if not stack.is_empty() and stack.top().left == node:   # 栈非空且当前节点是栈顶的左子节点
				node = stack.top().right
			else:       # 没有右子树或右子树遍历完毕，强迫退栈
				node = None

	def count_nodes(self, node):
		"""统计树中节点个数，递归法"""
		if node is None:
			return 0
		else:
			return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)

	def sum_nodes(self, node):
		"""设节点里保存数值，求二叉树里所有节点的和，递归法"""
		if node is None:
			return 0
		else:
			return node.elem + self.sum_nodes(node.left) + self.sum_nodes(node.right)


class BinaryTree2(BinaryTree):
	"""使用带有父节点引用二叉节点构建的二叉树"""

	def __init__(self):
		super(BinaryTree2, self).__init__()

	def add(self, elem):
		"""广度优先法插入元素"""

		node = BNode2(elem=elem)

		if self.is_empty():
			self.set_root(root_node=node)
			return

		queue = Queue()
		queue.enqueue(self.root())

		while not queue.is_empty():

			cur_node = queue.dequeue()

			if cur_node.left is None:
				p = node
				cur_node.left = node
				node.parent = p
				return
			else:
				queue.enqueue(cur_node.left)

			if cur_node.right is None:
				p = node
				cur_node.right = node
				node.parent = p
				return
			else:
				queue.enqueue(cur_node.right)


if __name__ == '__main__':
	tree = BinaryTree2()
	for i in range(10):
		# print(i, i, i)
		tree.add(i)
	tree.breadth_travel()
	tree.preorder_travel(tree.root())
	print()
	tree.inorder_travel(tree.root())
	print()
	tree.postorder_travel(tree.root())
	print()
	print(type(tree.root()))
	print(tree.count_nodes(tree.root()))
	print(tree.sum_nodes(tree.root()))
	tree.preorder_travel2(tree.root())
	print()
	tree.inorder_travel2(tree.root())
	print()
	tree.postorder_travel2(tree.root())
	print()
	print(tree.root().left.left.parent)

	pass

