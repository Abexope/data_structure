"""
队列 & 栈模块
"""

from exception import QueueUnderflow
from exception import StackUnderflow
from obj import LinearNode as Node


class Queue:
	"""队列"""
	def __init__(self):
		self._head = None
		self._rear = None
		self._count = 0

	def is_empty(self):
		"""判断队列是否为空"""
		return self._count == 0

	def peek(self):
		"""返回栈顶元素"""
		if self.is_empty():
			raise QueueUnderflow("in peek() method: queue is empty. Nothing can be peeked.")
		return self._head.elem

	def enqueue(self, elem):
		"""
		入队操作
		:param elem: 待插入对象
		:return: None
		"""
		if self.is_empty():  # 空队列情况
			self._head = Node(elem=elem, next_=self._head)
			self._rear = self._head
			self._count += 1
		else:  # 一般情况
			self._rear.next = Node(elem=elem)
			self._rear = self._rear.next
			self._count += 1

	def dequeue(self):
		"""出队操作"""
		if self.is_empty():
			raise QueueUnderflow("in dequeue() method: queue is empty. Nothing can be peeked.")
		# 一般情况
		p = self._head
		self._head = p.next
		self._count -= 1
		return p.elem


class Stack:
	"""栈"""

	def __init__(self):
		self._top = None    # 栈顶指针
		self._depth = 0     # 堆栈深度

	def is_empty(self):
		"""判断栈是否为空"""
		return self._depth == 0

	def get_depth(self):
		"""获取栈深度"""
		return self._depth

	def top(self):
		"""访问栈顶元素"""
		if self._top is None:
			raise StackUnderflow("in top() method: stack is empty. Nothing can be visited.")
		return self._top.elem

	def push(self, elem):
		"""压栈"""
		self._top = Node(elem=elem, next_=self._top)
		self._depth += 1

	def pop(self):
		"""弹栈"""
		if self.is_empty():
			raise StackUnderflow("in pop() method: stack is empty. Nothing can be returned.")
		p = self._top
		self._top = p.next
		self._depth -= 1
		return p.elem


if __name__ == '__main__':

	pass
