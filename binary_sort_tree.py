"""二叉排序树"""

from obj import BinaryNode
from dictionary import Assoc
from queue_stack import Stack


class DictBinTree:
	"""二叉排序树（字典）类"""
	
	def __init__(self):
		self._root = None
	
	def is_empty(self):
		return self._root is None
	
	def search(self, key):
		bt = self._root
		while bt is not None:
			entry = bt.elem
			if key < entry.key:
				bt = bt.left
			elif key > entry.key:
				bt = bt.right
			else:
				return entry.value
		return None
	
	def insert(self, key, value):
		bt = self._root
		if bt is None:      # 空树
			self._root = BinaryNode(Assoc(key, value))
			return
		while True:
			entry = bt.elem
			if key < entry.key:     # 左分支
				if bt.left is None:
					bt.left = BinaryNode(Assoc(key, value))
					return
				bt = bt.left
			elif key > entry.key:       # 右分支
				if bt.right is None:
					bt.right = BinaryNode(Assoc(key, value))
					return
				bt = bt.right
			else:                   # 替换已有值
				bt.elem.value = value
				return
	
	def values(self):
		"""字典迭代器，中序遍历和返回二叉排序树中的元素"""
		t, s = self._root, Stack()
		while t is not None or not s.is_empty():
			while t is not None:
				s.push(t)
				t = t.left
			t = s.pop()
			yield t.elem.key, t.elem.value
			t = t.right

	def delete(self, key):
		p, q = None, self._root     # 维持p为q的父节点
		
		while q is not None and q.elem.key != key:
			p = q
			if key < q.elem.key:
				q = q.left
			else:
				q = q.right
		if q is None:   # 树中不存在关键码key
			return
		
		# 到此处，q指向的是要删除的节点，p是其父节点
		if q.left is None:      # 如果q没有左子节点
			if p is None:       # 若此时p仍是None，说明q指向的值根节点
				self._root = q.right    # 删去p，q成为新的根节点
			elif q is p.left:
				p.left = q.right
			else:
				p.right = q.right
			return
		
		# 如果q有左子节点
		r = q.left      # 找左子树的最右节点
		while r.right is not None:
			r = r.right
		r.right = q.right
		if p is None:   # q指向根节点
			self._root = q.left     # 修改_root
		elif p.left is q:
			p.left = q.left
		else:
			p.right = q.left
	
	def print(self):
		for k, v in self.values():
			print(k, v)


def build_dict_bin_tree(entries):
	"""构造二叉排序树字典"""
	dic = DictBinTree()
	for k, v in entries:
		dic.insert(k, v)
	return dic


class DictOptBinTree(DictBinTree):
	"""最佳二叉排序树"""
	
	def __init__(self, seq):
		super(DictOptBinTree, self).__init__()
		data = sorted(seq)
		self._root = DictOptBinTree.buildOBT(data, 0, len(data) - 1)
	
	@staticmethod
	def buildOBT(data, start, end):
		if start > end:
			return None
		mid = (end + start) // 2
		left = DictOptBinTree.buildOBT(data, start, mid - 1)
		right = DictOptBinTree.buildOBT(data, mid + 1, end)
		return BinaryNode(Assoc(*data[mid]), left, right)
	

if __name__ == '__main__':
	from random import randint
	from random import seed
	seed(0)
	e = [(randint(0, 100), randint(0, 100)) for i in range(20)]
	# d = build_dict_bin_tree(e)
	d = DictOptBinTree(e)
	d.print()
	print(d.search(100), d.search(87), d.search(0))
	pass
