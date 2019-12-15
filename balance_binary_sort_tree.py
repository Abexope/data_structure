"""平衡二叉排序树（AVL树）"""

from obj import AVLNode
from binary_sort_tree import DictBinTree, build_dict_bin_tree
from dictionary import Assoc


class DictAVL(DictBinTree):
	"""AVL树"""
	
	def __init__(self):
		super(DictAVL, self).__init__()
	
	@staticmethod
	def LL(a: AVLNode, b: AVLNode) -> AVLNode:
		"""LL型调整：a的左子树较高，新节点插入在a的左子树的左子树"""
		a.left = b.right
		b.right = a
		a.bf = b.bf = 0
		return b
	
	@staticmethod
	def RR(a: AVLNode, b: AVLNode) -> AVLNode:
		"""RR型调整：a的右子树较高，新节点插入在a右子树的右子树"""
		a.right = b.left
		b.left = a
		a.bf = b.bf = 0
		return b
	
	@staticmethod
	def LR(a: AVLNode, b: AVLNode) -> AVLNode:
		"""LR型调整：a的左子树较高，新节点插入在a的左子树的右子树"""
		c = b.right
		a.left, b.right = c.right, c.left
		c.left, c.right = b, a
		if c.bf == 0:       # c本身就是插入节点
			a.bf = b.bf = 0
		elif c.bf == 1:     # 新节点在c的左子树
			a.bf = -1
			b.bf = 0
		else:               # 新节点在c的右子树
			a.bf = 0
			b.bf = 1
		c.bf = 0
		return c
	
	@staticmethod
	def RL(a: AVLNode, b: AVLNode) -> AVLNode:
		"""RL型调整：a的右子树较高，新节点插入在a的右子树的左子树"""
		c = b.left
		a.right, b.left = c.left, c.right
		c.left, c.right = a, b
		if c.bf == 0:       # c本身就是插入节点
			a.bf = 0
			b.bf = 0
		elif c.bf == 1:     # 新节点在c的左子树
			a.bf = 0
			b.bf = -1
		else:               # 新节点在c的右子树
			a.bf = 1
			b.bf = 0
		c.bf = 0
		return c
	
	def insert(self, key, value):
		a = p = self._root
		
		if a is None:       # 空树
			self._root = AVLNode(Assoc(key, value))
			return
		
		pa = q = None       # 维持pa，q为a，p的父节点
		while p is not None:        # 确定插入位置及最小非平衡子树
			if key == p.elem.key:       # key存在，修改关联值并结束
				p.elem.value = value
				return
			if p.bf != 0:
				pa, a = q, p        # 已知最小非平衡子树
			q = p
			if key < p.elem.key:
				p = p.left
			else:
				p = p.right
		
		# q是待插入节点的父节点，pa，a记录最小非平衡子树
		node = AVLNode(Assoc(key, value))
		if key < q.elem.key:
			q.left = node           # 作为左子节点
		else:
			q.right = node          # 或右节点
		# 新节点已插入，a是最小不平衡子树
		if key < a.elem.key:        # 新节点在a的左子树
			p = b = a.left
			d = 1
		else:                       # 新节点在a的右子树
			p = b = a.right
			d = -1
		
		# 修改b到新节点路径上各节点的BF值，b为a的子节点
		while p != node:            # node一定存在，所以不必判断p是否为空
			if key < p.elem.key:    # p的左子树增高
				p.bf = 1
				p = p.left
			else:                   # p的右子树增高
				p.bf = -1
				p = p.right
		if a.bf == 0:               # a的原BF为0，不会失衡
			a.bf = d
			return
		if a.bf == -d:              # 新节点在较低子树
			a.bf = 0
			return
		
		# 新节点在较高的子树，失衡，需要调整
		if d == 1:                  # 新节点在a的左子树
			if b.bf == 1:
				b = self.LL(a, b)   # LL调整
			else:
				b = self.LR(a, b)   # LR调整
		else:                       # 新节点在a的右子树
			if b.bf == -1:
				b = self.RR(a, b)   # RR调整
			else:
				b = self.RL(a, b)   # RL调整
		
		if pa is None:              # 原a为树根，修改_root
			self._root = b
		else:                       # a非树根，新树接在正确的位置
			if pa.left == a:
				pa.left = b
			else:
				pa.right = b


if __name__ == '__main__':
	from random import randint
	from random import seed
	seed(0)
	e = [(randint(0, 100), randint(0, 100)) for i in range(20)]
	dd = build_dict_bin_tree(e)
	dd.print()
	print(dd.search(100), dd.search(87), dd.search(0))
	pass
