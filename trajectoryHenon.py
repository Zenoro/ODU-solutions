import matplotlib.pyplot as plt
import time
import math as maf

print('Hello! This program will plot Henon trajectory!\nver1.0\n')
#ввод условий
print('x1=1+y-ax^2')
print('y1=bx\n')
x0 = float(input('Enter the x0: '))
y0 = float(input('Enter the y0: '))
chose = input("Custom number of iterations? (y/n)    ")
if chose == 'y':
    n = int(input('Enter number of iterations: '))
else:
    n = 10000
choose1 = input('Custom coefficients? (y/n):     ')
if choose1 == 'y':
    a = float(input('Enter a coefficient: '))
    b = float(input('Enter b coefficient: '))
else:
    a = 1.4
    b = 0.3

#ставим таймер работы программы
start_time = time.time()

#задаем переменные по которым будем строить косяк
x_list = []
y_list = []
counter = 0
temp = x0

#заполняем их тут
while counter < n:
    x1 = 1+y0-a*x0*x0
    x_list.append(x1)
    y1 = b*x0
    y_list.append(y1)
    x0 = x1
    y0 = y1
    counter += 1

#print('Y list: ', y_list)
#print('X list: ', x_list)
plt.title("Henon trajectory")
plt.xlabel('X axis')
plt.ylabel('Y axis')
#plt.xlim([-1000,10])
#plt.ylim([-5,5])
plt.plot(x_list, y_list, linestyle='', marker='.', markersize=1, color='r', label='Henon trajectory')
plt.legend(loc=u'upper center', mode='expand', borderaxespad=0, ncol=3)
plt.grid()
print("time elapsed:", (time.time() - start_time))
plt.show()