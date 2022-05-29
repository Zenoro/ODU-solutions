import math as maf
import matplotlib.pyplot as plt
import time

print('Hello! This is an Euler Calculator for Duffings equation.\nver.1.0.\nProcess started!\n')
# начальные условия
print("Solution for x(2)+δx(1)-x+x^3=γcos(ωt)")
t0 = float(input("Enter the t0:  "))
x0 = float(input("Enter the x0:  "))
y0 = float(input("Enter x'0: "))
h = float(input("Enter the step h:  "))
xUp = float(input("Enter the tmax of segment: "))         # отрезок [t0, xUp]
chose = input("Custom coefficients?(y/n)   ")
if chose == "yes" or chose == "y":
    omeg = float(input("Enter ω: "))
    delta = float(input("Enter δ: "))
    gamma = float(input("Enter γ: "))
else:
    omeg = 1
    delta = 0.25
    gamma = 0.03

choos = input("Do you need X(t) graph? (y/n)    ")

start_time = time.time()
f = lambda y, x, t: x-x**3-delta*y+gamma*maf.cos(omeg*t)

t_list = [t0]
x_list = [x0]
y_list = [y0]

while t0 <= xUp:
    x1 = x0+h*y0
    x_list.append(x1)
    y1 = y0+h*f(y0, x0, t0)
    y_list.append(y1)
    t0 += h
    t_list.append(t0)
    x0 = x1
    y0 = y1

plt.rc('font', **{'family': 'arial'})
plt.xlabel("X axis")
plt.ylabel("Y axis")
plt.figure(1)
plt.plot(x_list, y_list, "g-", marker='.', label="Euler method")            #строим график Метода Эйлера
plt.legend(loc=u'upper center', mode='expand', borderaxespad=0, ncol=3)
plt.grid()
if choos == 'y' or choos == 'yes':
    plt.figure(2)
    plt.xlabel("T axis")
    plt.ylabel("X axis")
    plt.plot(t_list, x_list, "b-", marker='o', label="x(t)")                       #строим график Х(t)
    plt.legend(loc=u'upper center', mode='expand', borderaxespad=0, ncol=3)
    plt.grid()
print("time elapsed:", (time.time() - start_time))
plt.show()

