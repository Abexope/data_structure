"""
链接表模块

继承关系
	·BaseStructure <- LinkList <- DuplexLinkList <- CycleDuplexLinkList
	·CycleLinkList
"""

from exception import LinkListUnderflow as Underflow
from obj import LinearNode as Node
from obj import DuplexLinearNode as DNode


class BaseStructure:
	"""基本单向链表接口"""
	
	def __init__(self):
		"""对象构造方法"""
		self._head = None
		self._count = 0
		
	def __str__(self):
		"""自定义链表可视化方法"""
		
		# 空表情况
		if self.is_empty():
			return "[ -> None]"
		
		# 一般情况
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
		return (self._head is None) and (self._count == 0)
	
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
		if self.is_empty():
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
		if self.is_empty():
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
		if self.is_empty():
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
	
	def apply(self, fun):
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


class LinkList(BaseStructure):
	"""带有表尾指针的单向链表"""
	
	def __init__(self):
		"""对象构造方法"""
		super(LinkList, self).__init__()
		self._rear = None           # 增加表尾节点引用域，提高有关表尾操作的效率
		
	def prepend(self, elem):
		"""
		链表表头插入对象方法
		:param elem: 待插入对象
		:return: None
		"""
		if self.is_empty():         # 空表情况
			self._head = Node(elem=elem, next_=self._head)
			self._rear = self._head
			self._count += 1
		else:                       # 一般情况
			self._head = Node(elem=elem, next_=self._head)
			self._count += 1
	
	def append(self, elem):
		"""
		链表表尾插入对象方法
		:param elem: 待插入对象
		:return: None
		"""
		if self.is_empty():         # 空表情况
			self._head = Node(elem=elem, next_=self._head)
			self._rear = self._head
			self._count += 1
		else:                       # 一般情况
			self._rear.next = Node(elem=elem)
			self._rear = self._rear.next
			self._count += 1
			
	def pop_last(self, get_elem=False):
		"""
		链表表尾删除对象方法
		:param get_elem:
			·Python.bool    default:False
			·是（True）否（False）返回已经删除的表尾对象
		:return: 已经删除的表尾对象
		"""
		
		# 空表情况
		if self.is_empty():
			raise Underflow("In pop_last() method: link list object is empty. Nothing can be returned.")
		
		p = self._head
		
		# 单节点链表情况
		if p.next is None:
			e = p.elem
			self._head = None
			self._count -= 1
			if get_elem:
				return e
			else:
				return
		
		# 一般情况，使用指针p遍历链表，知道p.next是self._rear指向的对象
		while p.next.next is not None:
			p = p.next
		e = p.next.elem
		p.next = None
		self._rear = p
		self._count -= 1
		if get_elem:
			return e
		else:
			return
		
	def reverse(self):
		"""链表反转方法"""
		p = None
		self._rear = self._head     # 重置表尾指针
		while self._head is not None:
			q = self._head
			self._head = q.next     # 摘下原始首节点
			q.next = p
			p = q           # 将刚刚摘下的节点接入指针p指向的节点序列
		self._head = p      # 链表反转完成，重置表头指针


class CycleLinkList:
	"""单向循环链表"""

	def __init__(self):
		self._rear = None
		self._count = 0

	def __str__(self):

		if self.is_empty():
			return "[ -> ]"

		p = self._rear.next
		res = ""
		if self._rear is not None:
			while p is not self._rear:
				res += "->{}".format(p.elem)
				p = p.next
			else:
				"""
				当p指向self._rear的时候会直接跳出循环
				因此主循环中无法实现将指针指向最后一个Node，需要添加else语句补充
				"""
				res += "->{}->".format(p.elem)
		return "[{}]".format(res)

	def __len__(self):
		return self._count

	def __iter__(self):
		p = self._rear.next
		while p is not self._rear:
			yield p.elem
			p = p.next
		else:
			yield p.elem

	def is_empty(self):
		return self._rear is None

	def prepend(self, elem):
		"""
		链表表头插入对象方法
		:param elem: 待插入对象
		:return: None
		"""
		p = Node(elem=elem)
		if self._rear is None:  # 空表情况
			p.next = p          # p.next指针指向p本身，保证循环链表的性质
			self._rear = p
			self._count += 1
		else:                   # 一般情况
			p.next = self._rear.next
			self._rear.next = p
			self._count += 1

	def append(self, elem):
		"""
		链表表尾插入对象方法
		:param elem: 待插入对象
		:return: None
		"""
		p = Node(elem=elem)
		if self.is_empty():     # 空表情况
			p.next = p
			self._rear = p
			self._count += 1
		else:                   # 一般情况
			p.next = self._rear.next
			self._rear.next = p
			self._rear = p
			self._count += 1

	def pop(self, get_elem=False):
		"""
		链表表头删除对象方法
		:param get_elem:
			·Python.bool    default:False
			·是（True）否（False）返回已经删除的表尾对象
		:return: 已经删除的表尾对象
		"""
		if self.is_empty():     # 空表情况
			raise Underflow("in pop() method: cycle link list object is empty. Nothing can be returned.")
		p = self._rear.next
		if self._rear is p:     # 单个节点情况
			self._rear = None
			self._count -= 1
		else:                   # 一般情况
			self._rear.next = p.next
			self._count -= 1
		if get_elem:
			return p.elem
		else:
			return

	def pop_last(self, get_elem=False):
		"""
		链表表尾删除对象方法
		:param get_elem:
			·Python.bool    default:False
			·是（True）否（False）返回已经删除的表尾对象
		:return: 已经删除的表尾对象
		"""
		if self.is_empty():                 # 空表情况
			raise Underflow("in pop_last() method: cycle link list object is empty. Nothing can be returned.")
		e = self._rear.elem
		if self._rear.next is self._rear:   # 单个节点情况
			self._rear = None
			self._count -= 1
			if get_elem:
				return e
			else:
				return
		else:                               # 一般情况
			p = self._rear.next
			while p.next is not self._rear:
				p = p.next
			p.next = self._rear.next
			self._rear = p
			self._count -= 1
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
		p = self._rear.next
		while p is not self._rear:
			if cond(p.elem):
				yield p.elem
			p = p.next

	def apply(self, fun):
		"""
		链表对象批处理方法
		:param fun:
			·Python.lambda function，Python.function
			·批处理方式
			·例如：fun = lambda x: x ** 2
		:return:
		"""
		p = self._rear.next
		while p is not self._rear:
			fun(p.elem)
			p = p.next

	def insert(self, index, elem):
		if index > self._count:
			raise Underflow("in insert() method: index is out of range")
		if index == 0:
			self.prepend(elem)
			return
		if index == self._count:
			self.append(elem)
			return
		idx, p = 0, self._rear.next
		while p:
			if idx + 1 == index:
				next_p = p.next
				p.next = Node(elem, next_p)
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
		if index > self._count:
			raise Underflow("in remove() method: index is out of range")
		if index == 0:
			self.pop(get_elem=get_elem)
			return
		if index == self._count:
			self.pop_last(get_elem=get_elem)
			return
		idx, p = 0, self._rear.next
		while p:
			if idx + 1 == index:
				e = p.next
				p.next = p.next.next
				self._count -= 1
				if get_elem:
					return e
				else:
					return
			idx, p = idx + 1, p.next


class DuplexLinkList(LinkList):
	"""双向链表"""

	def __init__(self):
		super(DuplexLinkList, self).__init__()

	def __str__(self):
		p = self._head
		if self.is_empty():     # 空表情况
			return "[None <-> None]"
		res = "None <-> "        # 一般情况
		while p:
			res += "{} <-> ".format(p.elem)
			p = p.next
		else:
			res += "None"
		return "[{}]".format(res)

	def prepend(self, elem):
		p = DNode(elem=elem, prev=None, next_=self._head)
		if self.is_empty():     # 空表情况
			self._rear = p
		else:                   # 一般情况
			p.next.prev = p
		self._head = p
		self._count += 1

	def append(self, elem):
		p = DNode(elem=elem, prev=self._rear, next_=None)
		if self.is_empty():     # 空表情况
			self._head = p
		else:                   # 一般情况，设置next指针
			p.prev.next = p
		self._rear = p
		self._count += 1

	def pop(self, get_elem=False):
		if self.is_empty():     # 空表情况
			raise Underflow("in pop() method: Duplex link list object is empty. Nothing can be returned.")
		e = self._head.elem
		if self._head is self._rear:    # 单节点链表情况，头指针和尾指针指向同一个元素
			self._head, self._rear = None, None
			"""
			TIP：
				Python的赋值是“指向性赋值”，因此，如果双链表中只有一个元素的情况下，
				改变self._head指针指向时，self._rear指针的指向没有改变，
				因此也需要修改self._rear指针的指向
			"""
			self._count -= 1
			if get_elem:
				return e
			else:
				return
		# 一般情况
		self._head = self._head.next
		self._head.prev = None
		self._count -= 1
		if get_elem:
			return e
		else:
			return

	def pop_last(self, get_elem=False):
		if self.is_empty():     # 空表
			raise Underflow("in pop_last() method: Duplex link list object is empty. Nothing can be returned.")
		e = self._rear.elem
		if self._rear is self._head:    # 单节点情况
			self._rear, self._head = None, None
			self._count -= 1
			if get_elem:
				return e
			else:
				return
		# 一般情况
		self._rear = self._rear.prev
		self._rear.next = None
		self._count -= 1
		if get_elem:
			return e
		else:
			return

	def insert(self, index, elem):
		if index > self._count:
			raise Underflow("in insert() method: index is out of range.")
		if index == 0:      # 相当于在表头插入元素
			self.prepend(elem)
			return
		if index == self._count:    # 相当于在表尾插入元素
			self.append(elem)
			return
		# 一般情况
		if index <= (self._count // 2):   # 前半段插入，利用双向表的特点，插入时间复杂度最大为O(self._count/2)
			idx, idx_p = 0, self._head
			while idx_p:    # 一般情况
				if idx + 1 == index:    # 找到待插入元素的前一个元素的位置
					p = DNode(elem, idx_p, idx_p.next)  # 生成指针p指向一个新节点对象
					idx_p.next.prev = p     # idx_p指针指向元素的“原下一个元素”的prev指针指向p
					idx_p.next = p          # idx_p指针指向元素的“新下一个元素”的next指针指向p
					self._count += 1
					return
				idx, idx_p = idx + 1, idx_p.next
		else:   # 后半段插入
			idx, idx_p = self._count - 1, self._rear
			while idx_p:
				if idx == index:
					p = DNode(elem, idx_p.prev, idx_p)
					idx_p.prev.next = p     # idx_p指针指向元素的“原上一个元素”的next指针指向p
					idx_p.prev = p          # idx_p指针指向元素的“新上一个元素”的prev指针指向p
					self._count += 1
					return
				idx, idx_p = idx - 1, idx_p.prev

	def remove(self, index, get_elem=False):
		if index >= self._count:
			raise Underflow("in remove() method: index is out of range.")
		if index == 0:
			self.pop()
			return
		if index == self._count - 1:
			self.pop_last()
			return
		if index <= self._count // 2:   # 前半段删除
			idx, p = 0, self._head
			while p:
				if idx + 1 == index:
					e = p.next
					p.next = p.next.next
					p.next.prev = p
					self._count -= 1
					return e
				idx, p = idx + 1, p.next
		else:                           # 后半段删除
			idx, p = self._count, self._rear
			while p:
				if idx - 2 == index:    # 减2
					e = p.prev
					p.prev = p.prev.prev
					p.prev.next = p
					self._count -= 1
					return e
				idx, p = idx - 1, p.prev


class CycleDuplexLinkList(DuplexLinkList):
	"""循环双向链表"""

	def __init__(self):
		super(CycleDuplexLinkList, self).__init__()

	def __str__(self):
		if self.is_empty():
			return "[ <-> ]"
		p = self._head
		res = " <-> "
		if self._head is not None:
			while p is not self._rear:
				res += "{} <-> ".format(p.elem)
				p = p.next
			else:
				res += "{} <->".format(p.elem)
		return "[{}]".format(res)

	def __iter__(self):
		p = self._rear.next
		while p is not self._rear:
			yield p.elem
			p = p.next
		else:   # 同理 __str__() 中的 while-else 用法
			yield p.elem

	def is_empty(self):
		return (self._head is None and self._rear is None) and (self._count == 0)

	def prepend(self, elem):
		p = DNode(elem=elem, prev=self._rear, next_=self._head)
		if self.is_empty():         # 空表
			self._rear = p
			p.prev = self._rear
			p.next = p
		else:
			p.prev.next = p
			self._head.prev = p     # 头部的prev指针指向新的头节点
		self._head = p
		self._count += 1

	def append(self, elem):
		p = DNode(elem=elem, prev=self._rear, next_=self._head)
		if self.is_empty():         # 空表
			self._head = p
			p.next = self._head
			p.prev = p
		else:
			p.next.prev = p
			self._rear.next = p     # 尾部的next指针指向新的尾节点
		self._rear = p
		self._count += 1

	def pop(self, get_elem=False):
		if self.is_empty():
			raise Underflow("in pop() method: cycle duplex link list is empty. Nothing can be returned.")
		e = self._head.elem
		if self._head is self._rear:    # 单节点链表情况
			self._head, self._rear = None, None
		else:                           # 一般情况
			self._head = self._head.next
			self._rear.next = self._head
			self._head.prev = self._rear
		self._count -= 1
		if get_elem:
			return e
		else:
			return

	def pop_last(self, get_elem=False):
		if self.is_empty():
			raise Underflow("in pop_last() method: cycle duplex link list is empty. Nothing can be returned.")
		e = self._rear.elem
		if self._rear is self._head:    # 单节点情况
			self._rear, self._head = None, None
		else:                           # 一般情况
			self._rear = self._rear.prev
			self._head.prev = self._rear
			self._rear.next = self._head
		self._count -= 1
		if get_elem:
			return e
		else:
			return

	def insert(self, index, elem):
		if index > self._count:
			raise Underflow("in insert() method: index is out of range.")
		if index == 0:  # 相当于在表头插入元素
			self.prepend(elem)
			return
		if index == self._count:     # 相当于在表尾插入元素
			self.append(elem)
			return
		if index <= (self._count // 2):   # 前半段插入，利用双向表的特点，插入时间复杂度最大为O(self._count/2)
			idx, idx_p = 0, self._head
			while idx_p:    # 一般情况
				if idx + 1 == index:    # 找到待插入元素的前一个元素的位置
					p = DNode(elem=elem, prev=idx_p, next_=idx_p.next)  # 生成指针p指向一个新节点对象
					idx_p.next.prev = p     # idx_p指针指向元素的“原下一个元素”的prev指针指向p
					idx_p.next = p          # idx_p指针指向元素的“新下一个元素”的next指针指向p
					self._count += 1
					return
				idx, idx_p = idx + 1, idx_p.next
		else:   # 后半段插入
			idx, idx_p = self._count - 1, self._rear
			while idx_p:
				if idx == index:
					p = DNode(elem=elem, prev=idx_p, next_=idx_p.next)
					idx_p.prev.next = p     # idx_p指针指向元素的“原上一个元素”的next指针指向p
					idx_p.prev = p          # idx_p指针指向元素的“新上一个元素”的prev指针指向p
					self._count += 1
					return
				idx, idx_p = idx - 1, idx_p.prev

	def remove(self, index, get_elem=False):
		if index >= self._count:
			raise Underflow("in remove() method: index is out of range.")
		if index == 0:
			self.pop()
			return
		if index == self._count - 1:
			self.pop_last()
			return
		if index <= self._count // 2:  # 前半段删除
			idx, p = 0, self._head
			while p:
				if idx + 1 == index:
					e = p.next
					p.next = p.next.next
					p.next.prev = p
					self._count -= 1
					if get_elem:
						return e
					else:
						return
				idx, p = idx + 1, p.next
		else:  # 后半段删除
			idx, p = self._count, self._rear
			while p:
				if idx - 2 == index:  # 减2
					e = p.prev
					p.prev = p.prev.prev
					p.prev.next = p
					self._count -= 1
					if get_elem:
						return e
					else:
						return
				idx, p = idx - 1, p.prev


if __name__ == '__main__':

	pass
