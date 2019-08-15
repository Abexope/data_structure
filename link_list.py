"""
链接表模块

"""

from exception import LinkListUnderflow as Underflow
from obj import LinearNode as Node


class LinkList:
	"""基本单向链表"""
	
	def __init__(self):
		"""对象构造方法"""
		self._head = None
		self._count = 0
		
	def __str__(self):
		"""自定义链表可视化方法"""
		p = self._head
		res = ""
		if self._head is not None:
			while p:
				res += "{} -> ".format(p)
				p = p.next
			else:
				res += "{}".format(p)
		return "[{}]".format(res)
		
	def __len__(self):
		"""返回链表长度方法"""
		return self._count
	
	def __iter__(self):
		"""链表迭代器"""
		p = self._head
		while p is not None:
			yield p.elem
			p = p.next
	
	def is_empty(self):
		"""判断链表是否为空"""
		return self._head is None
	
	def prepend(self, elem):
		"""
		链表表头插入对象方法
		:param elem: 待插入对象
		:return: None
		"""
		self._head = Node(elem=elem, next_=self._head)
		self._count += 1
		
	def pop(self, get_elem=False):
		"""
		链表表头删除对象方法
		:param get_elem:
			·Python.bool    default:False
			·是（True）否（False）返回已经删除的表头对象
		:return: 已经删除的表头对象
		"""
		
		# 空链表情况
		if self._head is None:
			raise Underflow("In pop() method: link list object is empty. Nothing can be returned.")
		
		# 一般情况
		e = self._head.elem
		self._head = self._head.next
		self._count -= 1
		if get_elem:
			return e
	
	def append(self, elem):
		"""
		链表表尾插入对象方法
		:param elem: 待插入对象
		:return: None
		"""
		
		# 空链表情况
		if self._head is None:
			self._head = Node(elem=elem)
			self._count += 1
			return
		
		# 一般情况
		p = self._head
		while p.next is not None:   # O(n)时间复杂度
			p = p.next
		p.next = Node(elem=elem)
		self._count += 1
		
	def pop_last(self, get_elem=False):
		"""
		链表表尾删除对象方法
		:param get_elem:
			·Python.bool    default:False
			·是（True）否（False）返回已经删除的表尾对象
		:return: 已经删除的表尾对象
		"""
		
		# 空链表情况
		if self._head is None:
			raise Underflow("In pop_last() method: link list object is empty. Nothing can be returned.")
		
		# 链表中仅有一个元素的情况
		p = self._head
		if p.next is None:
			e, self._head = p.elem, None    # 表头指针指向None
			self._count -= 1
			if get_elem:
				return e
		
		# 一般情况
		while p.next.next is not None:  # O(n)时间复杂度
			p = p.next
		e, p.next = p.next.elem, None
		self._count -= 1
		if get_elem:
			return e
		
	def filter(self, cond):
		"""
		链表筛选方法
			筛选满足指定筛选条件的对象
		:param cond:
			·Python.lambda function
			·筛选条件表达式
			·例如：cond = lambda x: x > 10
		:return: 所有满足筛选条件的对象
		"""
		p = self._head
		while p is not None:
			if cond(p.elem):
				yield p.elem
			p = p.next
	
	def batch_process(self, fun):
		"""
		链表对象批处理方法
		:param fun:
			·Python.lambda function，Python.function
			·批处理方式
			·例如：fun = lambda x: x ** 2
		:return:
		"""
		p = self._head
		while p is not None:
			fun(p.elem)
			p = p.next
	
	def insert(self, index, elem):
		"""
		链表指定位置插入对象方法
		:param index: 指定位置索引
			·Python.int
			·index >= 0 and index <= self._count - 1
		:param elem: 待插入对象
		:return: None
		"""
		
		# 特殊情况
		if index > self._count:
			raise Underflow("In insert() method: index is out of range.")
		if index == 0:              # 相当于在表头插入元素
			self.prepend(elem)
			return
		if index == self._count:    # 相当于在表尾插入元素
			self.append(elem)
			return
		
		# 一般情况
		idx, p = 0, self._head      # 链表头索引，滑动指针
		while p:
			if idx + 1 == index:    # 找到待插入元素的前一个元素的位置
				next_p = p.next     # 提取当前指针所指元素的下一个元素
				p.next = Node(elem=elem, next_=next_p)  # 将当前指针指向新生成的节点对象，同时令其指向先前的下一个元素
				self._count += 1
				return
			idx, p = idx + 1, p.next
	
	def remove(self, index, get_elem=False):
		"""
		链表指定位置删除对象方法
		:param index: 指定位置索引
			·Python.int
			·index >= 0 and index <= self._count - 1
		:param get_elem:
			·Python.bool    default:False
			·是（True）否（False）返回已经删除的表尾对象
		:return: 已经被删除的对象
		"""
		
		# 特殊情况
		if index > self._count:
			raise Underflow("In remove() method: index is out of range")
		if index == 0:              # 相当于删除表头元素
			self.pop(get_elem=get_elem)
			return
		if index == self._count:    # 相当于在表尾删除元素
			self.pop_last(get_elem=get_elem)
			return
		
		# 一般情况
		idx, p = 0, self._head
		while p:
			if idx + 1 == index:
				e = p.next
				p.next = p.next.next    # 直接将指针指向的位置改为下一个元素的下一个元素，实现删除操作
				self._count -= 1
				if get_elem:
					return e
			idx, p = idx + 1, p.next
			
	def reverse(self):
		"""链表反转方法"""
		p = None
		while self._head is not None:
			q = self._head
			self._head = q.next     # 摘下原始首节点
			q.next = p
			p = q                   # 将刚摘下的节点介入p指向的节点序列
		self._head = p              # 反转链表完成，将表头指针指向新的表头节点


if __name__ == '__main__':
	pass
