"""
图
"""

from exception import GraphError


class Graph:
	"""基于邻接矩阵实现的图结构"""

	def __init__(self, mat, unconn=0):
		"""
		构造方法
		:param mat: 邻接矩阵，嵌套列表
		:param unconn: 无关联情况的特殊值，默认为0
		"""
		vnum = len(mat)     # 获取邻接矩阵行数
		for x in mat:
			if len(x) != vnum:      # 行数与列数做对比，检查邻接矩阵是否为合法的方阵
				raise GraphError("Argument for 'Graph'.")
		self._mat = [mat[i][:] for i in range(vnum)]    # 拷贝
		self._unconn = unconn
		self._vnum = vnum   # 邻接矩阵维数

	def __str__(self):
		return "[\n\t" + ",\n\t".join(map(str, self._mat)) + "\n]" + "\nUnconnected: {}".format(self._unconn)

	def vertex_num(self):
		return self._vnum   # 获取邻接矩阵维数

	def _invalid(self, v):
		"""检查下标合法性"""
		return 0 > v or v >= self._vnum

	def add_vertex(self):
		raise GraphError("Adj-Matrix does not support 'add_vertex()'.")

	def add_edge(self, vi, vj, val=1):
		if self._invalid(vi) or self._invalid(vj):
			raise GraphError("{} or {} is not a valid vertex".format(vi, vj))
		self._mat[vi][vj] = val

	def get_edge(self, vi, vj):
		if self._invalid(vi) or self._invalid(vj):
			raise GraphError("{} or {} is not a valid vertex".format(vi, vj))
		return self._mat[vi][vj]

	def out_edges(self, vi):
		if self._invalid(vi):
			raise GraphError("{} is not a valid vertex.".format(vi))
		return self._out_edges(self._mat[vi], self._unconn)

	@staticmethod
	def _out_edges(row, unconn):
		"""
		构造静态节点表，顶点v的出边用(v', w)表示
		v'是该边的终点
		w 是边的信息，对于带权图，w是边的权值
		:param row:
		:param unconn:
		:return:
		"""
		edges = []
		for i in range(len(row)):
			if row[i] != unconn:
				edges.append((i, row[i]))
		return edges


class GraphAL(Graph):
	"""基于邻接表实现的图结构"""
	def __init__(self, mat=None, unconn=0):
		super(GraphAL, self).__init__(mat)
		if mat is None:
			mat = []
		vnum = len(mat)
		for x in mat:
			if len(x) != vnum:      # 行数与列数做对比，检查邻接矩阵是否为合法的方阵
				raise GraphError("Argument for 'Graph'.")
		self._mat = [Graph._out_edges(mat[i], unconn) for i in range(vnum)]
		self._vnum = vnum
		self._unconn = unconn

	def add_vertex(self):
		self._mat.append([])    # 增加新节点是安排一个新编号
		self._vnum += 1
		return self._vnum - 1

	def add_edge(self, vi, vj, val=1):
		if self._vnum == 0:
			raise GraphError("Cannot add edge to empty graph.")
		if self._invalid(vi) or self._invalid(vj):
			raise GraphError("{} or {} is not a valid vertex".format(vi, vj))
		row = self._mat[vi]
		i = 0
		while i < len(row):
			if row[i][0] == vj:     # 修改 mat[vi][vj] 的值
				self._mat[vi][i] = (vj, val)
				return
			if row[i][0] > vj:      # 原来没有到vj的边，退出循环后加入边
				break
			i += 1
		self._mat[vi].insert(i, (vj, val))

	def get_edge(self, vi, vj):
		if self._invalid(vi) or self._invalid(vj):
			raise GraphError("{} or {} is not a valid vertex".format(vi, vj))
		for i, val in self._mat[vi]:
			if i == vj:
				return val
		return self._unconn

	def out_edges(self, vi):
		if self._invalid(vi):
			raise GraphError("{} is not a valid vertex.".format(vi))
		return self._mat[vi]


if __name__ == '__main__':
	graph_al = GraphAL([])
	for ii in range(10):
		graph_al.add_vertex()
		graph_al.add_edge(ii, 0, val=13)
	print(graph_al)
