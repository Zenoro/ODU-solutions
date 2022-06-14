import math as maf
import matplotlib.pyplot as plt
import time


print('This is a Runge-Kutt Calculator for Duffings equation.\nProcess started!\n')
print("ẍ+δẋ-x+x³=γcos(ωt)\n")

# начальные условия
t0 = float(input("t0 =  "))
tmax = float(input("tmax = "))         # временной отрезок [t0, tmax]
x0 = float(input("x0 =  "))
y0 = float(input("ẋ0 = "))
h = float(input("h =  "))

# coefficients
omeg = 1
delta = 0.25
gamma = 0.03

start_time = time.time()

f = lambda t, x, y: x-x**3-delta*y+gamma*maf.cos(omeg*t)
g = lambda t, x, y: y

x_list = [x0]
y_list = [y0]
plt.scatter(x0, y0, color='red')    # отображение начальной точки

while t0 <= tmax:
    k1 = h*f(t0, x0, y0)
    q1 = h*g(t0, x0, y0)

    k2 = h*f(t0+h/2.0, x0+q1/2.0, y0+k1/2.0)
    q2 = h*g(t0+h/2.0, x0+q1/2.0, y0+k1/2.0)

    k3 = h*f(t0+h/2.0, x0+q2/2.0, y0+k2/2.0)
    q3 = h*g(t0+h/2.0, x0+q2/2.0, y0+k2/2.0)

    k4 = h*f(t0+h, x0+q3, y0+k3)
    q4 = h*g(t0+h, x0+q3, y0+k3)

    y1 = y0+(k1+2.0*k2+2.0*k3+k4)/6.0
    x1 = x0+(q1+2.0*q2+2.0*q3+q4)/6.0
    x_list.append(x1)
    y_list.append(y1)
    t0 += h
    x0 = x1
    y0 = y1

#строим
plt.title("Метод Рунге-Кутта")
plt.xlabel("X")
plt.ylabel("Y")
plt.figure(1)
plt.plot(x_list, y_list, "b-", marker='')
plt.grid()

print("time elapsed:", (time.time() - start_time))
plt.show()
