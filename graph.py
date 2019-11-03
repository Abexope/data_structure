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


def dfs_span_forest(graph):
	"""DFS生成树，递归法"""
	vnum = graph.vertex_num()
	span_forest = [None] * vnum     # 记录顶点是否被找到

	def dfs(graph, v):
		"""递归遍历函数，在递归中记录经由边"""
		nonlocal span_forest    # 声明 span_forest 是 nonlocal 变量
		for u, w in graph.out_edges(v):
			if span_forest[u] is None:
				span_forest[u] = (v, w)
				dfs(graph, u)

	for v in range(vnum):
		if span_forest[v] is None:
			span_forest[v] = (v, 0)
			dfs(graph, v)
	return span_forest


def kruskal(graph):
	"""构造最小生成树的Kruskal算法"""
	vnum = graph.vertex_num()
	reps = [i for i in range(vnum)]     # 储存顶点编号，作为表示两点是否连通的代表元
	mst, edges = [], []                 # mst保存最小生成树(林)，edges保存升序排列的边
	for vi in range(vnum):              # 所有的边加入表edges
		for vj, w in graph.out_edges(vi):
			edges.append((w, vi, vj))    # 保存(权值，出点，入点)
	edges.sort()                        # 边按权值排序，O(n log n)时间
	for w, vi, vj in edges:
		if reps[vi] != reps[vj]:        # 两端点属于不同连通分量
			mst.append(((vi, vj), w))     # 记录这条边
			if len(mst) == vnum - 1:        # 如果已经构造了 |V| - 1 条边，构造完成
				break
			rep, orep = reps[vi], reps[vj]
			for i in range(vnum):       # 合并连通分量，统一代表元
				if reps[i] == orep:
					reps[i] = rep
	return mst


def prim(graph):
	"""构造最小生成树的Prim算法"""
	from priority_queue import PriorQue2
	from priority_queue import PriorQue
	vnum = graph.vertex_num()
	mst = [None] * vnum
	cands = PriorQue2([(0, 0, 0)])              # 使用优先队列记录侯选边 (w, vi, vj)
	count = 0
	while count < vnum and not cands.is_empty():
		w, u, v = cands.dequeue()               # 取出当前的最短边
		if mst[v]:
			continue                           # 邻接顶点 v 已在 mst 中，继续
		mst[v] = ((u, v), w)                   # 记录新的MST边和顶点
		count += 1
		for vi, w in graph.out_edges(v):        # 考虑 v 的邻接点 vi
			if not mst[vi]:                     # 如果 vi 不在 mst 中则这条边是侯选边
				cands.enqueue((w, v, vi))
	return mst


if __name__ == '__main__':
	"""
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
	# bfs_seq = bfs_graph(graph_al_7, 0)
	# dfs_seq = dfs_graph(graph_al_7, 0)
	# print("宽度优先遍历：", bfs_seq)
	# print("深度优先遍历：", dfs_seq)
	print()
	sf = dfs_span_forest(graph_al_7)
	print(sf)
	"""
	"""
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
	"""

	# G9图
	graph9 = GraphAL([])
	for _ in range(7):
		graph9.add_vertex()
	for ver in [(1, 5), (2, 11), (3, 5)]:
		graph9.add_edge(0, ver[0], val=ver[1])
	for ver in [(0, 5), (3, 3), (4, 9), (6, 7)]:
		graph9.add_edge(1, ver[0], val=ver[1])
	for ver in [(0, 11), (3, 7), (5, 6)]:
		graph9.add_edge(2, ver[0], val=ver[1])
	for ver in [(0, 5), (1, 3), (2, 7), (6, 20)]:
		graph9.add_edge(3, ver[0], val=ver[1])
	for ver in [(1, 9), (6, 8)]:
		graph9.add_edge(4, ver[0], val=ver[1])
	for ver in [(2, 6), (6, 8)]:
		graph9.add_edge(5, ver[0], val=ver[1])
	for ver in [(1, 7), (3, 20), (4, 8), (5, 8)]:
		graph9.add_edge(6, ver[0], val=ver[1])
	print(graph9)
	kr = kruskal(graph9)    # Kruskal算法
	print(kr)
	pr = prim(graph9)       # Prim算法
	print(pr)
