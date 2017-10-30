import numpy as np
import random
import matplotlib.pyplot as plt


def func(x):
    return np.array([1.0, x[0], x[1], x[0]*x[1], x[0]**2, x[1]**2])
#region Ввод/Вывод
def makeInput(Count, grid, filename):
    f = open(filename, "w")
    f.write(str(Count) + "\n")

    print("Мно-во X:", grid)
    x = [[random.choice(grid),random.choice(grid)] for _ in range(Count)]
    print("X[i,j]:", x)
    for i in x:
        f.write(str(i[0]) + " " + str(i[1]) + "\n")
    for i in range(Count - 1):
        f.write(str(1 / Count) + "\n")
    f.write((str(1 / Count)))
    f.close()

def read(filename):
    f = open(filename, "r")
    Xmass = []
    Pmass = []
    count = int(f.readline())
    for i in range(count):
        Xmass.append([float(item) for item in f.readline().split(" ")])
    for i in range(count):
        Pmass.append(float(f.readline()))
    return Xmass, Pmass

#Запись в файл, записывается так, чтобы потом считать
def write(filename, x, p):
    f = open(filename, "w")
    f.write(str(len(x)) + "\n")
    for i in x:
        f.write(str(i[0]) + " " + str(i[1]) + "\n")
    f.write(str(p[0]))
    for i in p[1:]:
        f.write("\n" + str(i))
    f.close()
#endregion

def makeM(x, p):
    M = np.zeros((len(func(x[0])), len(func(x[0]))))
    for i in range(len(x)):
        M += p[i] * make_partM(func(x[i]))
    return M

#создание части матрицы, для каждого из весов
def make_partM(fx):
    M = np.zeros((len(fx), len(fx)))
    for i in range(len(fx)):
        for j in range(len(fx)):
            M[i][j] = fx[i] * fx[j]
    return M

#создание матрицы D из матрицы М
def makeD(M):
    return np.linalg.inv(M)
#Рисует график index указывает на изменяемую точку, и на каждой итерации рисуются два графика:
#начальное положение - зеленая точка и измененное положение - красная
def printPlot(x, index, type):

    for i in range(len(x)):
        plt.scatter(x[i][0], x[i][1])
    if type == 1:
        plt.scatter(x[index][0], x[index][1], color = (1, 0, 0))
    else:
        plt.scatter(x[index][0], x[index][1], color=(0, 1, 0))
    plt.show()

#функция d, чтобы она была от одной переменной надо в x и newx кинуть одинаковые значения
def d(x, D, newx):
    return np.dot(np.dot(func(x), D), func( newx).T)

#функция вычисления дельты для точки
def Delta(x, D, N, newx):
    return 1./float(N) * (d(newx, D, newx) - d(x, D, x))\
           - 1./float(N)**2 * (d(x, D, x) * d(newx, D, newx) - d(x, D, newx)**2)

#нахождения максимального значения дельты на для одной точки из плана, но для все сетки.
#возвращает список из максимального значения и точки
def findMaxforOneX(x, D, N, grid):
    maxdot = [grid[0], grid[0]]
    maxvalue = Delta(x, D, N, maxdot)
    for x1 in grid:
        for x2 in grid:
            value = Delta(x, D, N, [x1, x2])
            if value > maxvalue:
                maxvalue = value
                maxdot = [x1, x2]
    return [maxvalue, maxdot]
#функция нахождения максимумов для всех точек плана и выбора из него наибольшего. возвращает значения, точку и индекс
def findMaxforAll(X, D, N, grid):
    listofmax = []
    for x in X:
        listofmax.append(findMaxforOneX(x, D, N, grid))
    return [*max(listofmax),listofmax.index(max(listofmax))]

#Построение сетки. там написано 10х10 и 20х20. тут 11х11 потому что так сетка бьется ровно, а не на периодические
#числа
grid = np.linspace(-1, 1, 21)
#Количество элементов
N = 20
#Построение новых входных данных, для например разных N или для разной сетки
makeInput(N, grid, "input.txt")
x, p = read("input.txt")

eps = 0.001
delta = 1
iteration = 0
while True:
    M = makeM(x, p)
    print(np.around(np.linalg.det(M), 8))
    D = makeD(M)
    #print("Итерация №", iteration)
    delta = findMaxforAll(x, D, N, grid)
    if delta[0] > eps:
        if (iteration == 0):
            printPlot(x, delta[2], 0)
        x[delta[2]] = delta[1]
    else:
        printPlot(x, delta[2], 1)
        break
    iteration += 1
    write("result" + str(iteration) + ".txt", x, p)
