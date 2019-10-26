"""
优先队列
	在任何时候访问或弹出的，总是当时再这个结构里保存的所有元素中优先级最高的。如果该元素不弹出，下次访问还将得到它
	“最优元素先进先出（先用）”
	对于相同优先级的处理：
		1. 严格按照FIFO原则进行，效率较低
		2. 只考虑优先级，效率较高
堆：元素有序排布的完全二叉树
"""

from exception import PriorQueueError


class PriorQue:
	"""基于线性表实现的优先队列"""

	def __init__(self, elist):
		assert isinstance(elist, list)
		self._elems = elist
		self._elems.sort(reverse=True)

	def __str__(self):
		return str(self._elems)

	def enqueue(self, e):
		"""插入元素"""
		i = len(self._elems) - 1
		while i >= 0:
			if self._elems[i] <= e:
				i -= 1
			else:
				break
		self._elems.insert(i + 1, e)

	def is_empty(self):
		return not self._elems

	def peek(self):
		"""获取优先级最高的元素"""
		if self.is_empty():
			raise PriorQueueError("in peek: nothing can be peek in queue.")
		return self._elems[-1]

	def dequeue(self):
		"""获取并弹出优先级最高的元素"""
		if self.is_empty():
			raise PriorQueueError("in peek: nothing can be peeked in queue.")
		return self._elems.pop()


class PriorQue2:
	"""基于堆实现的优先队列"""

	def __init__(self, elist):
		assert isinstance(elist, list)
		self._elems = elist
		if elist:
			self.build_heap()

	def __str__(self):
		return str(self._elems)

	def is_empty(self):
		return not self._elems

	def peek(self):
		if self.is_empty():
			raise PriorQueueError("in peek: nothing can be peeked in queue")
		return self._elems[0]

	def enqueue(self, e):
		self._elems.append(None)    # 先追加一个空元素
		self.siftup(e, len(self._elems) - 1)
		pass

	def siftup(self, e, last):
		"""向上筛选"""
		elems, i, j = self._elems, last, (last - 1) // 2
		while i > 0 and e < elems[j]:
			elems[i] = elems[j]
			i, j = j, (j - 1) // 2
		elems[i] = e

	def dequeue(self):
		if self.is_empty():
			raise PriorQueueError("in dequeue(): nothing can be returned in queue")
		elems = self._elems
		e0 = elems[0]
		e = elems.pop()
		if len(elems) > 0:
			self.siftdown(e, 0, len(elems))
		return e0

	def siftdown(self, e, begin, end):
		"""向下筛选"""
		elems, i, j = self._elems, begin, begin * 2 + 1
		while j < end:                  # 在 j == 2 * i + 1 时跳出循环
			if j + 1 < end and elems[j + 1] < elems[j]:
				j += 1                  # elems[j]不大于其兄弟节点的数据
			if e < elems[j]:            # e在三者中最小，已找到了位置
				break
			elems[i] = elems[j]         # elems[j]在三者中最小，上移
			i, j = j, 2 * j + 1
		elems[i] = e

	def build_heap(self):
		"""构建堆"""
		end = len(self._elems)
		for i in range(end // 2, -1, -1):
			self.siftdown(self._elems[i], i, end)


def heap_sort(elems, reverse=False):
	"""堆排序"""
	if not reverse:
		def siftdown(elems, e, begin, end):
			"""大顶堆"""
			i, j = begin, begin * 2 + 1
			while j < end:
				if j + 1 < end and elems[j + 1] > elems[j]:
					j += 1
				if e > elems[j]:
					break
				elems[i] = elems[j]
				i, j = j, 2 * j + 1
			elems[i] = e
		end = len(elems)
		for i in range(end // 2, -1, -1):
			siftdown(elems, elems[i], i, end)
		for i in range((end - 1), 0, -1):
			e = elems[i]
			elems[i] = elems[0]
			siftdown(elems, e, 0, i)
	else:
		def siftdown(elems, e, begin, end):
			"""小顶堆"""
			i, j = begin, begin * 2 + 1
			while j < end:
				if j + 1 < end and elems[j + 1] < elems[j]:
					j += 1
				if e < elems[j]:
					break
				elems[i] = elems[j]
				i, j = j, 2 * j + 1
			elems[i] = e
		end = len(elems)
		for i in range(end // 2, -1, -1):
			siftdown(elems, elems[i], i, end)
		for i in range((end - 1), 0, -1):
			e = elems[i]
			elems[i] = elems[0]
			siftdown(elems, e, 0, i)


def siftdown(elems, e, begin, end):
	"""小顶堆"""
	i, j = begin, begin * 2 + 1
	while j < end:
		if j + 1 < end and elems[j + 1] < elems[j]:
			j += 1
		if e < elems[j]:
			break
		elems[i] = elems[j]
		i, j = j, 2 * j + 1
		print(i, j, elems)
	elems[i] = e


if __name__ == '__main__':
	# pq = PriorQue2([3, 2, 21, 64, 5])
	# print(pq)
	# pq.enqueue(50)
	# print(pq)
	# print(pq.dequeue())
	# print(pq)
	# print(pq.dequeue())
	# print(pq)
	a = [64, 5, 3, 2, 21, 100]
	for i in range(5, -1, -1):
		siftdown(a, a[i], i, 6)
	# heap_sort(a)
	print(a)
