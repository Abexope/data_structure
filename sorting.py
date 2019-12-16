"""线性表的排序算法"""
from random import randint, seed
seed(100)


def bubble_sort(alist: list):
	"""冒泡排序"""
	n = len(alist)
	for j in range(n - 1):
		flag = True     # 交换行为标识
		for i in range(n - j - 1):
			if alist[i] > alist[i + 1]:
				alist[i], alist[i + 1] = alist[i + 1], alist[i]
				flag = False    # 执行交换行为
		if flag:        # 若未发生交换，说明已经有序，提前退出
			return


def select_sort(alist: list):
	"""选择排序"""
	n = len(alist)
	for j in range(n - 1):
		min_index = j
		for i in range(j + 1, n):
			min_index = i if alist[min_index] > alist[i] else min_index
		alist[j], alist[min_index] = alist[min_index], alist[j]


def insert_sort(alist: list):
	"""插入排序(希尔排序gap=1)"""
	n = len(alist)
	for j in range(1, n):
		for i in range(j, 0, -1):
			if alist[i] < alist[i - 1]:
				alist[i], alist[i - 1] = alist[i - 1], alist[i]


def shell_sort(alist: list):
	"""希尔排序"""
	n = len(alist)
	gap = n // 2
	while gap > 0:
		for j in range(gap, n):
			for i in range(j, 0, -gap):
				if alist[i] < alist[i - gap]:
					alist[i], alist[i - gap] = alist[i - gap], alist[i]
		gap //= 2   # 缩短gap步长


def quick_sort(alist: list, first, last):
	"""原地快速排序"""
	if first >= last:
		return

	low, high = first, last
	mid_value = alist[first]

	while low < high:       # 原地写法

		# high指针左移
		while low < high and alist[high] >= mid_value:
			high -= 1
		alist[low] = alist[high]

		# low指针右移
		while low < high and alist[low] < mid_value:
			low += 1
		alist[high] = alist[low]

	# 退出循环时low == high
	alist[low] = mid_value

	quick_sort(alist, first, low - 1)   # 左侧快排
	quick_sort(alist, low + 1, last)    # 右侧快排


def quick_sort2(alist: list):
	"""非原地快速排序"""
	if len(alist) < 2:
		return alist
	else:
		tmp = alist[0]
		less = [item for item in alist[1:] if item < tmp]       # 占用额外空间！
		more = [item for item in alist[1:] if item >= tmp]      # 占用额外空间！
		return quick_sort2(less) + [tmp] + quick_sort2(more)


def merge_sort(alist: list):
	"""归并排序"""
	n = len(alist)

	# 递归停止条件
	if n <= 1:
		return alist

	# 递归拆分
	mid = n // 2
	left_li = merge_sort(alist[:mid])      # left：采用归并排序后形成的新的有序列表
	right_li = merge_sort(alist[mid:])     # right：采用归并排序后形成的新的有序列表

	# 交替合并
	res = []                               # 归并要占用额外的空间复杂度
	while left_li and right_li:
		if left_li[0] <= right_li[0]:
			res.append(left_li.pop(0))
		else:
			res.append(right_li.pop(0))
	if left_li:
		res += left_li
	if right_li:
		res += right_li
	return res


def gnome_sort(alist: list):
	"""侏儒排序"""
	i = 0
	while i < len(alist):
		if i == 0 or alist[i - 1] <= alist[i]:
			i += 1
		else:
			alist[i], alist[i - 1] = alist[i - 1], alist[i]
			i -= 1


if __name__ == '__main__':
	a = [19, 59, 34, 62, 23, 81, 51, 94, 45, 56, 7]
	print(a)
	gnome_sort(a)
	print(a)
	print(merge_sort(a))
