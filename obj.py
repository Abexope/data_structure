"""
数据节点定义模块

继承关系
	·LinearNode <- DuplexLinearNode
	·BinaryNode
"""


class LinearNode:
	"""线性节点"""

	def __init__(self, elem, next_=None):
		self.elem = elem
		self.next = next_
		
	def __str__(self):
		return str(self.elem)


class DuplexLinearNode(LinearNode):
	"""带有双向指针的线性节点"""

	def __init__(self, elem, prev=None, next_=None):
		super(DuplexLinearNode, self).__init__(elem, next_)
		self.prev = prev


class BinaryNode:
	"""二叉节点"""

	def __init__(self, elem, left=None, right=None):
		self.elem = elem
		self.left = left
		self.right = right

	def __str__(self):
		return str(self.elem)
