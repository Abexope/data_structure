"""字典"""


class Assoc:
	"""映射关系描述类"""

	def __init__(self, key, value):
		self.key = key
		self.value = value

	def __lt__(self, other):
		return self.key < other.key

	def __le__(self, other):
		return self.key <= other.key

	def __str__(self):
		return "{0}: {1}".format(self.key, self.value)


class DictList:
	"""基于线性表实现的字典"""

	def __init__(self):
		self._elems = []

	def __str__(self):
		return "{" + ", ".join([str(item) for item in self._elems]) + "}"

	def is_empty(self):
		return not self._elems

	def search(self, key):
		for assoc in self._elems:
			if assoc.key == key:
				return assoc.value

	def insert(self, key, value):
		for i, assoc in enumerate(self._elems):    # 查重
			if key == assoc.key:        # 如果key重复
				assoc.value = value     # 覆盖原来的value
				return
		self._elems.append(Assoc(key, value))       # 否则实例化一个新的Assoc对象

	def delete(self, key):
		for i, assoc in enumerate(self._elems):
			if assoc.key == key:
				self._elems.pop(i)

	def delete_by_value(self, value):
		for i, assoc in enumerate(self._elems):
			if assoc.value == value:
				self._elems.pop(i)


class DictOrdList(DictList):
	"""加持有序列表和二分搜索"""

	def __init__(self):
		super(DictOrdList, self).__init__()

	def bisearch(self, key):
		low, high = 0, len(self._elems) - 1
		while low <= high:
			mid = low + (high - low) // 2
			if key == self._elems[mid].key:
				return self._elems[mid]
			if key < self._elems[mid].key:
				high = mid - 1          # 在低半区继续
			else:
				low = mid + 1           # 在高半区继续

	def search(self, key):
		res = self.bisearch(key)
		return res.value if res else None

	def insert(self, key, value):
		if self.is_empty():
			self._elems.append(Assoc(key, value))
			return
		low, high = 0, len(self._elems) - 1
		while low <= high:
			mid = low + (high - low) // 2
			if key == self._elems[mid].key:
				self._elems[key].value = value
				return
			if key <= self._elems[mid].key:
				high = mid - 1
			else:
				low = mid + 1
		# 跳出循环的唯一可能是low > high，即没有查到key
		self._elems.insert(low, Assoc(key, value))

	def delete(self, key):
		assoc = self.bisearch(key)
		if assoc is not None:
			self._elems.remove(assoc)


if __name__ == '__main__':
	from random import randint
	d = DictOrdList()
	for ii in range(11):
		d.insert(ii, randint(1, 100))
	print(d)
	print(d.search(0))
	print(d.search(11))
	print(d.delete(10))
	print(d)
	print(d.delete(0))
	print(d)
	print(d.delete(5))
	print(d)
	d.insert(5, 10)
	print(d)
	d.insert(50, 10)
	print(d)
