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


class GraphAL:
	"""基于邻接表实现的图结构"""

	def __init__(self, mat=None, unconn=0):
		if mat is None:
			mat = []
		vnum = len(mat)
		for x in mat:
			if len(x) != vnum:      # 行数与列数做对比，检查邻接矩阵是否为合法的方阵
				raise GraphError("Argument for 'Graph'.")
		self._mat = [self._out_edges(mat[i], unconn) for i in range(vnum)]
		self._vnum = vnum
		self._unconn = unconn

	def __str__(self):
		return "[\n\t" + ",\n\t".join(map(str, self._mat)) + "\n]" + "\nUnconnected: {}".format(self._unconn)

	def vertex_num(self):
		return self._vnum   # 获取邻接矩阵维数

	def add_vertex(self):
		self._mat.append([])    # 增加新节点是安排一个新编号
		self._vnum += 1
		return self._vnum - 1

	def _invalid(self, v):
		"""检查下标合法性"""
		return 0 > v or v >= self._vnum

	def add_edge(self, vi, vj, val=1):
		if self._vnum == 0:
			raise GraphError("Cannot add edge to empty graph.")
		if self._invalid(vi) or self._invalid(vj):
			raise GraphError("{} or {} is not a valid vertex".format(vi, vj))
		row = self._mat[vi]
		i = 0
		while i < len(row):
			if row[i][0] == vj:     # 如果原图存在 vi 到 vj 的边，则用新的 vi 到 vj 的权值覆盖掉原有的权值
				self._mat[vi][i] = (vj, val)    # 修改 mat[vi][vj] 的权值
				return
			if row[i][0] > vj:      # 如果原图中没有到vj的边，跳出循环后加入此边
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


def dfs_graph(graph, v0):
	"""深度优先图遍历"""
	from queue_stack import Stack
	vnum = graph.vertex_num()
	visited = [0] * vnum        # visited 记录已访问顶点
	visited[v0] = 1
	DFS_seq = [v0]              # DFS_seq 记录遍历序列
	st = Stack()
	st.push((0, graph.out_edges(v0)))       # 入栈 (i, edges)
	while not st.is_empty():    # 下次访问边edges[i]
		i, edges = st.pop()
		if i < len(edges):
			v, e = edges[i]
			st.push((i + 1, edges))     # 下次回来访问边edges[i+1]
			if not visited[v]:
				DFS_seq.append(v)
				visited[v] = 1
				st.push((0, graph.out_edges(v)))
	return DFS_seq


def bfs_graph(graph, v0):
	"""宽度优先图遍历"""
	from queue_stack import Queue
	vnum = graph.vertex_num()
	visited = [0] * vnum
	visited[v0] = 1
	BFS_seq = [v0]
	qu = Queue()
	qu.enqueue((0, graph.out_edges(v0)))        # 入队 (i, edges)
	while not qu.is_empty():
		i, edges = qu.dequeue()
		if i < len(edges):
			v, e = edges[i]
			qu.enqueue((i + 1, edges))
			if not visited[v]:
				BFS_seq.append(v)
				visited[v] = 1
				qu.enqueue((0, graph.out_edges(v)))

	return BFS_seq


if __name__ == '__main__':

	# G7图
	graph_al_7 = GraphAL([])
	for _ in range(7):
		graph_al_7.add_vertex()
	graph_al_7.add_edge(0, 2)
	graph_al_7.add_edge(0, 3)
	graph_al_7.add_edge(1, 0)
	graph_al_7.add_edge(1, 2)
	graph_al_7.add_edge(1, 5)
	graph_al_7.add_edge(2, 1)
	graph_al_7.add_edge(2, 4)
	graph_al_7.add_edge(3, 4)
	graph_al_7.add_edge(4, 6)
	graph_al_7.add_edge(5, 6)
	print(graph_al_7)
	bfs_seq = bfs_graph(graph_al_7, 0)
	dfs_seq = dfs_graph(graph_al_7, 0)
	print("宽度优先遍历：", bfs_seq)
	print("深度优先遍历：", dfs_seq)
	print()

	# G8图
	graph8 = GraphAL()
	for _ in range(7):
		graph8.add_vertex()
	for ver in [2, 1]:
		graph8.add_edge(0, ver)
	for ver in [0, 3, 4, 6]:
		graph8.add_edge(1, ver)
	for ver in [0, 3, 5]:
		graph8.add_edge(2, ver)
	for ver in [1, 2, 6]:
		graph8.add_edge(3, ver)
	for ver in [1, 6]:
		graph8.add_edge(4, ver)
	for ver in [2, 6]:
		graph8.add_edge(5, ver)
	for ver in [1, 3, 4, 5]:
		graph8.add_edge(6, ver)
	print(graph8)
	bfs_seq = bfs_graph(graph8, 0)
	dfs_seq = dfs_graph(graph8, 0)
	print("宽度优先遍历：", bfs_seq)
	print("深度优先遍历：", dfs_seq)
