"""
二叉树应用：离散事件系统模拟
模拟抽象离散事件的发生，以及事件之间的连锁反应，可用于对真实系统的模拟和评价
·系统运行中可能不断发生一些事件（带有一定的随机性）
·一个事件在某个时刻发生，其发生有可能导致其它事件在未来发生

示例：海关检查站
负责车辆过境检查
·车辆按一定时间间隔到达，间隔具有一定随机性，设其范围为[a, b]分钟
·由于车辆的不同情况，每辆车的检查时间为[c, d]分钟
·海关可以开 k 个通道
·希望理解开通不同数量的通道数对车辆通行的影响

在考虑建设海关时，通过模拟海关的运行情况，分析需要建几条检查通道等。目标是提供更好的服务，保证合理的车辆等待时间和海关建设成本
模拟时间经常需要排队，队列结构适合用于记录事件
涉及到时间或其它排序因素时，优先队列更加实用
"""

from random import randint
from priority_queue import PriorQue2
from queue_stack import Queue


class Simulation:
	"""
	通用模拟框架接口
		事件的具体处理由具体的模拟问题确定。
		在一些事件的处理中可能引发另一个或一些新的事件，这些事件应该放入优先队列，在应该发生的时刻运行
		在模拟过程中，系统始终维护一个当前时间
	"""

	def __init__(self, duration):
		self._eventq = PriorQue2(elist=[])
		self._time = 0
		self._duration = duration

	def run(self):
		while not self._eventq.is_empty():      # 模拟时间队列空
			# 只要事件队列不为空，就从中取下第一个事件，用该事件的事件设置系统的当前时间，然后领该事件运行
			event = self._eventq.dequeue()
			self._time = event.time()           # 事件时间是当前时间
			if self._time > self._duration:     # 时间用完就结束
				break
			event.run()                         # 模拟这个事件，其运行可能生成新事件

	def add_event(self, event):
		self._eventq.enqueue(event)

	def cur_time(self):
		return self._time


class Event:
	"""
	通用事件框架接口
	"""

	def __init__(self, event_time, host):
		self._ctime = event_time
		self._host = host

	def __lt__(self, other_event):
		return self._ctime < other_event._ctime

	def __le__(self, other_event):
		return self._ctime <= other_event._ctime

	def host(self):
		"""有关事件的发生所在的模拟系统（宿主系统），在事件执行时，可能需要访问其宿主系统"""
		return self._host

	def time(self):
		return self._ctime

	def run(self):
		"""定义具体事件类必须定义这个方法"""
		pass


class Car:
	"""车辆类"""

	def __init__(self, arrive_time):
		self.time = arrive_time

	def arrive_time(self):
		return self.time


class Arrive(Event):
	"""到达事件类"""

	def __init__(self, arrive_time, customs):
		super(Arrive, self).__init__(arrive_time, customs)
		customs.add_event(self)

	def run(self):
		time, customs = self.time(), self.host()
		event_log(time, "car arrive")
		# 生成下一个Arrive事件
		Arrive(time + randint(*customs.arrive_interval), customs)
		# 本到达车辆事件的行为
		car = Car(time)
		if customs.has_queued_car():    # 有车辆在等进入等待队列
			customs.enqueue(car)
			return
		i = customs.find_gate()     # 检查空闲通道
		if i is not None:           # 有通道，进入检查
			event_log(time, "car check")
			Leave(time + randint(*customs.check_interval), i, car, customs)
		else:
			customs.enqueue(car)


class Leave(Event):
	"""离开事件类"""

	def __init__(self, leave_time, gate_num, car, customs):
		super(Leave, self).__init__(leave_time, customs)
		self.car = car
		self.gate_num = gate_num
		customs.add_event(self)

	def run(self):
		time, customs = self.time(), self.host()
		event_log(time, "car leave")
		customs.free_gate(self.gate_num)
		customs.car_count_1()
		customs.total_time_acc(time - self.car.arrive_time())
		if customs.has_queued_car():
			car = customs.next_car()
			i = customs.find_gate()
			event_log(time, "car check")
			customs.wait_time_acc(time - car.arrive_time())
			Leave(time + randint(*customs.check_interval), self.gate_num, car, customs)


class Customs:
	"""
	海关检查站模拟系统
	"""

	def __init__(self, gate_num, duration, arrive_interval, check_interval):
		self.simulation = Simulation(duration)
		self.waitline = Queue()
		self.duration = duration
		self.gates = [0] * gate_num
		self.total_wait_time = 0
		self.total_used_time = 0
		self.car_num = 0
		self.arrive_interval = arrive_interval
		self.check_interval = check_interval

	def wait_time_acc(self, n):
		self.total_wait_time += n

	def total_time_acc(self, n):
		self.total_used_time += n

	def car_count_1(self):
		self.car_num += 1

	def add_event(self, event):
		self.simulation.add_event(event)

	def cur_time(self):
		return self.simulation.cur_time()

	def enqueue(self, car):
		self.waitline.enqueue(car)

	def has_queued_car(self):
		return not self.waitline.is_empty()

	def next_car(self):
		return self.waitline.dequeue()

	def find_gate(self):
		for i in range(len(self.gates)):
			if self.gates[i] == 0:
				self.gates[i] = 1
				return i
		return None

	def free_gate(self, i):
		if self.gates[i] == 1:
			self.gates[i] = 0
		else:
			raise ValueError("Clear gate error")

	def simulate(self):
		Arrive(0, self)     # 生成车辆
		self.simulation.run()
		self.statistics()

	def statistics(self):
		print("Simulate " + str(self.duration) + " minutes, for " + str(len(self.gates)) + " gates")
		print(self.car_num, "cars pass the customs")
		print("Average waiting time: {:.4f}".format(self.total_wait_time / self.car_num))
		print("Average passing time: {:.4f}".format(self.total_used_time / self.car_num))
		i = 0
		while not self.waitline.is_empty():
			self.waitline.dequeue()
			i += 1
		print(i, "cars are in waiting line.")


def event_log(time, name):
	print("Event: " + name + ", happens at " + str(time))
	pass


if __name__ == '__main__':
	car_arrive_interval = (2, 3)
	car_check_time = (1, 2)
	cus = Customs(30, 480, car_arrive_interval, car_check_time)
	cus.simulate()

