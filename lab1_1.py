import copy

class Process: #вспомогательный класс для создания записи процесса 
	def __init__(self, name, act, time_act, time_stop):
		self.name = name
		self.act = act
		self.time_act = time_act
		self.time_stop = time_stop
	def __repr__(self):
		return "(%s, %r, %r, %r)" % (self.name, self.act, self.time_act, self.time_stop)


def activation(n): #вспомогательная функция для сортировки
	return n.act

def CreatePrcs(count):

	prcs = [] 

	for i in range(count):
		prc = Process(str(input("Имя процесса: ")), int(input('Момент активации: ',)), int(input('Время выполнения: ', )), int(input('Время остановки: ', ))) #ввод имени процесса, момента активации, времени выполнения, времени остановки 
		print(prc.name, prc.act, prc.time_act, prc.time_stop) #вывод на экран введенных значений
		prcs.append(prc) #вставляем запись в массив

	a = sorted(prcs, key = activation) #сортировка массива в порядке возрастания по act 
	return a


count = 3 #Кол-во процессов
prcs = CreatePrcs(count) #создаем список процессов, в качестве аргумента передаем ранее созданную переменную count=3
prcsBackup = copy.deepcopy(prcs)

ready = [] #Массив процессов, перешедших в состояние готовности
cpu = [] #Массив процессов, выполняемыx в данный момент 

tact = 0 #такт

execution = 0 #вспомогательная переменная для определения оставшегося времени выполнения процесса

queue = [] #очередь с именами для последующего восстановления процессов

p = 0 # вспомогательная переменная для хранения индекса массива

print("Nтакта    CPU    Готовность");

while 1:

	#Переход процессов в состояние готовности
	for i in range(len(prcs)):
		if prcs[i].act == tact: #если кол-во тактов дошло до момента активации какого то процесса
			ready.append(prcs[i])

	tact += 1 #увеличение такта

	#Переход процесса из состояния готовности к выполнению
	if (len(ready) > 0) and (len(cpu) == 0):

		time_act = ready[0].time_act # извлекаем время элемента из массива ready c нулевым индексом для последующего сравнения
		#находим процесс с наименьшим количеством заказанного времени
		for i in range(len(prcs)):
			if(prcs[i].time_stop > 0) and (prcs[i].time_act - prcs[i].time_stop) > 0:
				if(prcs[i].time_stop < time_act):
					time_act = prcs[i].time_stop
					p = i
			else:
				if(prcs[i].time_act < time_act):
					time_act = prcs[i].time_act
					p = i

		name = prcs[p].name

		cpu.append(prcs[p]) #помещаем процесс на cpu

		ready.pop(p) #удаление элемента из состояния готовности

		prcs.pop(p) 

		#проверяем указано ли время останова (на ввод/вывод, например), на котором процесс должен остановиться 
		if(cpu[0].time_stop > 0) and (cpu[0].time_act - cpu[0].time_stop) > 0:

			execution = cpu[0].time_stop

			for i in range(count):
				if prcsBackup[i].name == name:
					p = i

			queue.append([p, execution]) #если задано время останова и оно меньше time_act, то автоматически помещаем элемент в очередь
		else:
			execution = cpu[0].time_act #если не задано время останова или оно больше или равно time_act, то просто задаем в execution time_act

	#Вывод Nтакта, имени выполняемого процесса и имен процессов находящихся в состоянии готовности 
	s = ''

	for i in range(len(ready)):
		s += str(ready[i].name)

	if len(cpu) > 0:
		print(str(tact) + "         ", str(cpu[0].name) + "         ", str(s) + " ")
	else:
		if len(queue) > 0: 

			#если в очереди (queue) есть элементы, то определяем процесс в очереди с наименьшим оставшимся временем и помещаем его на cpu 
			#почти тот же алгоритм, что и с массивом ready

			p = 0

			time_act = queue[0][1]
 
			for i in range(len(queue)):
				if(queue[i][1] < time_act):
					time_act = queue[i][1]
					p = i 

			cpu.append(prcsBackup[queue[p][0]]) #помещаем на cpu
	
			execution = prcsBackup[queue[p][0]].time_act - queue[p][1]

			queue.pop(p) #удаляем из очереди

			print(str(tact) + "         ", str(cpu[0].name) + "         ", str(s) + " ")
		else:
			#если на cpu и в очереди пусто, то останавливаем цикл
			break

	execution -= 1 #уменьшаем оставшееся время выполнения на 1 такт

	#Если предыдущий процесс прекратил свое выполнение или был прерван, убираем его с cpu
	if execution == 0:
		cpu.pop(0)


