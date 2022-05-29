import time
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as patches
import math as m

# julian presentation
a = 0.0
b = -0.6
xfunc = lambda x, y: x*x-y*y+a
yfunc = lambda x, y: 2*x*y+b

                # henon presentation
# a = 1.4
# b = 0.3
# xfunc = lambda x, y: 1+y-a*x*x
# yfunc = lambda x, y: b*x

# x,y position fuctions
xposition = lambda cell, leng: x0+h*(cell-(cell-1)//leng*leng-1)
yposition = lambda cell, leng: y1-h*((cell-1)//leng+1)

def cell_dribling(item, leng):
    lengnew = leng*2
    new1 = 2*item-1+(item-1)//leng*lengnew
    new2 = new1+1
    new3 = new1+lengnew
    new4 = new2+lengnew
    return [new1, new2, new3, new4]

def hyperloop(xdown, xup, ydown, yup, h, leng, G, s_list, pt):
    cou = 1
    xtmp = xdown
    ytmp = yup
    xckl = xdown
    yckl = yup
    cell_list = []
    while yckl > ydown:
        while xckl < xup:
            for i in range(0, pt):
                for j in range(0, pt):
                    xrz = round(xfunc(xtmp, ytmp), 5)
                    yrz = round(yfunc(xtmp, ytmp), 5)
                    xtmp += 1 / pt*h
                    # случай вылета за рамки
                    if xrz < xdown or xrz > xup or yrz < ydown or yrz > yup:
                        continue
                    cell = m.floor(((yup - yrz) / h)) * leng + m.ceil((xrz - xdown) / h) // 1 + 1
                    # для оптимизации
                    if cell_list != [] and cell_list.count(cell) != 0 or not(cell in s_list):
                        continue
                    elif yrz == ydown:  # случай попадения на нижнюю строку
                        if not ((cell - leng) in cell_list):
                            cell_list.append(cell - leng)
                    elif xrz == xdown:  # попал на левую границу
                        if not ((cell+1) in cell_list):
                            cell_list.append(cell+1)
                    elif not (cell in cell_list):   # default
                        cell_list.append(cell)
                xtmp = xckl
                ytmp -= 1 / pt*h
            xckl += h
            xtmp = xckl
            ytmp = yckl
            # print(cou,": ",cell_list)
            for i in range(0, len(cell_list)):
                G.add_edge(cou, cell_list[i])
            cou += 1
            cell_list.clear()
        yckl -= h
        xckl = xdown
        xtmp = xckl
        ytmp = yckl
    return G

# изменяемые параметры (область, шаг, точность)
choose = input("Custom parameters?    (y/n): ")
if choose == 'yes' or choose == 'y' or choose == 'e' or choose =='н':
    x0 = float(input('Enter x0: '))
    x1 = float(input('Enter x1: '))
    y0 = float(input('Enter y0: '))
    y1 = float(input('Enter y1: '))
    h = float(input('Enter the step h = '))
    iterc = int(input("Enter the number of iterations:   "))
    choose = input("Custom coefficients?    (y/n): ")
    if choose == 'yes' or choose == 'y' or choose == 'e' or choose == 'н':
        a = float(input('Enter a: '))
        b = float(input('Enter b: '))
else:
    # x min
    x0 = -1.5
    # x max
    x1 = 1.5
    # y min
    y0 = -1.5
    # y max
    y1 = 1.5
    # step
    h = 0.5
    # number of iteration
    iterc = 6
#кол-во точек из таблицы в строке - ТОЧНОСТЬ
    pointcounter = 10

# задаем таймер
start_time = time.time()

# int main ()
lengx = abs(x1 - x0) / h
lengy = abs(y1 - y0) / h
sq = lengx*lengy
sugar = [q for q in range(1, int(sq))]
G = nx.DiGraph()
for gh in range(1, (iterc+1)):
    G = hyperloop(x0, x1, y0, y1, h, lengx, G, sugar, pointcounter)
    sugar = list(G.nodes())  # номера ячеек, которые попали
    plt.figure(gh)
    plt.title(str(gh)+" iteration")
    plt.xlim((x0-1), (x1+1))
    plt.ylim((y0-1), (y1+1))
    plt.grid()
    ax = plt.gca()
    for c in nx.strongly_connected_components(G):#, key=len, reverse=True):
        if len(c) > 1:
            # print("Кол-во возвратных вершин для ", gh, "итерации: ", len(c))
            alist = list(c)
            for k in range(0, len(alist)):
                ss = patches.Rectangle((xposition(alist[k], lengx), yposition(alist[k], lengx)), h, h, color = 'blue', fill=True)
                ax.add_patch(ss)
    G.clear()
    newbuf = sugar
    sugar = []
    for i in range(0, len(newbuf)):
        r1 = cell_dribling(newbuf[i], lengx)
        sugar += r1
    h *= 0.5
    lengx *= 2
    pointcounter -= 1
    print(gh, " iteration is done! Time elapsed: ", (time.time() - start_time))

plt.show()
