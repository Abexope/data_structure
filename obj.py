"""数据节点定义模块"""


class LinearNode:
	"""线性节点"""

	def __init__(self, elem, next_=None):
		self.elem = elem
		self.next = next_
		
	def __str__(self):
		return str(self.elem)
