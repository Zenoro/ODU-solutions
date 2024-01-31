import math as maf
import matplotlib.pyplot as plt
import time, os
import tkinter as tk
from tkinter import messagebox


def main(t0, xUp, x0, y0, h, alpha, beta, omeg, k, B):
    # начальные условия
    # print("Solution for x(2)+δx(1)-x+x^3=γcos(ωt)")
    # t0 = float(input("Enter the t0:  "))
    # xUp = float(input("Enter the tmax of segment: "))         # отрезок [x0, xUp]
    # x0 = float(input("Enter the x0:  "))
    # y0 = float(input("Enter x'0: "))
    # h = float(input("Enter the step h:  "))
    # chose = input("Custom coefficients?(y/n)   ")
    # omeg = 1
    # delta = 0.25
    # gamma = 0.3
    start_time = time.time()
    f = lambda t, x, y:  -k * y + alpha * x + beta * x * x * x + B * maf.cos(h * t)
    g = lambda t, x, y: y

    t_list = [t0]
    x_list = [x0]
    y_list = [y0]

    while t0 <= xUp:
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
        t_list.append(t0)
        x0 = x1
        y0 = y1

    with open('buf.txt', 'w') as f:
        f.write(str((time.time() - start_time)*1000))

    #строим график Метода Рунге-Кутта
    # plt.title("Runge-Kutta method")
    plt.clf()
    plt.rc('font', **{'family': 'arial'})
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.plot(x_list, y_list, "g-", marker='.', label="Runge-Kutta method")
    plt.legend(loc=u'upper center', mode='expand', borderaxespad=0, ncol=3)
    plt.grid()
    if os.path.exists('res.png'):
        os.remove('res.png')
    plt.savefig('res.png')
