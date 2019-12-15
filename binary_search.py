"""线性表的二分查找"""


def bi_search(alist: list, item):
	"""递归二分查找"""
	n = len(alist)
	if n > 0:
		mid = n // 2
		if alist[mid] == item:
			return True
		elif item < alist[mid]:
			return bi_search(alist[:mid], item)
		else:
			return bi_search(alist[mid + 1:], item)
	return False


def bi_search2(alist: list, item):
	"""循环二分查找"""
	n = len(alist)
	first, last = 0, n - 1
	while first <= last:
		mid = (first + last) // 2
		if alist[mid] == item:
			return True
		elif item < alist[mid]:
			last = mid - 1
		else:
			first = mid + 1
	return False


if __name__ == '__main__':
	a = [7, 19, 23, 34, 45, 51, 56, 59, 62, 81, 94]
	print(a)
	print(bi_search2(a, 7))
	print(bi_search2(a, 45))
	print(bi_search2(a, 50))
