"""异常定义模块"""


class LinkListUnderflow(ValueError):
	"""链表异常"""
	pass


class StackUnderflow(ValueError):
	"""栈下溢（空栈访问）"""
	pass


class QueueUnderflow(ValueError):
	"""出队异常"""
	pass


class PriorQueueError(ValueError):
	"""优先队列异常"""
	pass


class GraphError(ValueError):
	"""图结构异常"""
	pass
