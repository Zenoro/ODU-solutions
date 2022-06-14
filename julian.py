import matplotlib.pyplot as plt
import time
import math as m

print('Hello! This program will plot Julian display!\nver1.0\n')
# ввод условий
print('x1=x^2-y^2+a')
print('y1=2xy-b\n')
x0 = float(input('Enter the x0: '))
x1 = float(input('Enter the x1: '))
y0 = float(input('Enter the y0: '))
y1 = float(input('Enter the y1: '))
#chose = input("Custom number of iterations? (y/n)    ")
#if chose == 'y':
#    n = int(input('Enter number of iterations: '))
#else:
#    n = 1000
choose = input('Custom coefficients? (y/n):     ')
if choose == 'y' or choose == 'yes' or choose == 'н':
    a = float(input('Enter a coefficient: '))
    b = float(input('Enter b coefficient: '))
else:
    a = -0.0
    b = 0.0

"""""
мне нравится
 a = 0
 b = -0.6
"""""

# ставим таймер работы программы
start_time = time.time()

h = 0.01
#задаем переменные по которым будем строить косяк
x_list = []
y_list = []
x0temp = x0
y0temp = y0
y0cikl = y0
x0cikl = x0

#заполняем их тут
while y0cikl < y1:
    while x0cikl < x1:
        for i in range(0, 150):
            xtemp = x0temp*x0temp-y0temp*y0temp+a
            ytemp = 2*x0temp*y0temp+b
            x0temp = xtemp
            y0temp = ytemp
            if (m.isnan(xtemp) == True) or (m.isnan(ytemp) == True) or (m.isinf(xtemp) == True) or (m.isinf(ytemp) == True):
                break
        if (m.isnan(x0temp) == False) and (m.isnan(y0temp) == False) and (m.isinf(x0temp) == False) and (m.isinf(y0temp) == False):
            x_list.append(x0cikl)
            y_list.append(y0cikl)
        x0cikl += h
        x0temp = x0cikl
        y0temp = y0cikl
    x0cikl = x0
    x0temp = x0cikl
    y0cikl += h
    y0temp = y0cikl

#print('X list: ', x_list)
#print('Y list: ', y_list)

plt.title("Julian display")
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.xlim([-3, 3])
plt.ylim([-3, 3])
plt.plot(x_list, y_list, linestyle='', marker='.', color='r', label='Henon trajectory')
plt.legend(loc=u'upper center', mode='expand', borderaxespad=0, ncol=3)
plt.grid()
print("time elapsed:", (time.time() - start_time))
plt.show()
