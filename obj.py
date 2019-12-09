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


class BinaryNode2:
	"""带有父节点引用的二叉节点"""

	def __init__(self, elem, parent=None, left=None, right=None):
		self.elem = elem
		self.parent = parent
		self.right = right
		self.left = left

	def __str__(self):
		return str(self.elem)


class AVLNode(BinaryNode):
	"""AVL树节点"""
	
	def __init__(self, elem):
		super(AVLNode, self).__init__(elem)
		self.bf = 0     # 平衡因子（balance factor, BF）取值范围：{-1，0，1}
