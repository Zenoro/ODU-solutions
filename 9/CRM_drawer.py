import time
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as patches
import math as m
import os



def hyperloop(xdown, xup, ydown, yup, h, leng, pt, a, b):
    G = nx.DiGraph()
    xfunc = lambda x, y: x*x-y*y+a
    yfunc = lambda x, y: 2*x*y+b
    cou = 1
    xtmp = xdown
    ytmp = yup
    xckl = xdown
    yckl = yup
    cell_list = []
    while yckl > ydown:
        while xckl < xup:
            for i in range(0, pt):
                ytmp -= 1 / pt*h

                for j in range(0, pt):
                    xtmp += 1 / pt*h

                    xrz = round(xfunc(xtmp, ytmp), 6)
                    yrz = round(yfunc(xtmp, ytmp), 6)

                    if xrz < xdown or xrz > xup or yrz < ydown or yrz > yup:
                        continue
                    cell = m.floor(((yup - yrz) / h)) * leng + m.ceil((xrz - xdown) / h) // 1 + 1
                    if cell not in cell_list:
                        cell_list.append(cell)

                xtmp = xckl

            xckl += h
            xtmp = xckl
            ytmp = yckl

            for el in cell_list:
                G.add_edge(int(cou), int(el))
            cou += 1
            cell_list = []
        yckl -= h
        xckl = xdown
        xtmp = xckl
        ytmp = yckl
    return G


def main(x0:float, x1:float, y0:float, y1:float, h:float, iterc:int, a:float, b:float):
    lengx = abs(x1 - x0) / h
    # for _ in range(iterc-1):
    #     h /= 2
    #     lengx *= 2
    G = hyperloop(x0, x1, y0, y1, h, lengx, 5, a, b)
    print(f"{iterc} is done!")
    xposition = lambda cell, leng: x0 + h * (cell - (cell - 1) // leng * leng - 1)
    yposition = lambda cell, leng: y1 - h * ((cell - 1) // leng + 1)
    plt.xlim((x0), (x1))
    plt.ylim((y0), (y1))
    ax = plt.gca()
    total_cells = 0
    for c in nx.strongly_connected_components(G):
        if len(c) > 1:
            total_cells += len(c)
            for elem in list(c):
                ss = patches.Rectangle((xposition(elem, lengx), 
                                        yposition(elem, lengx)), 
                                        h, h, color = 'blue', fill=True)
                ax.add_patch(ss)
    print(f"Total number of cells: {total_cells}")
    plt.axis('off')
    if os.path.exists(f"CRM{iterc}.png"):
        os.remove(f"CRM{iterc}.png")
    plt.savefig(f"CRM{iterc}.png")
    plt.clf()
    plt.close()

if __name__ == "__main__":
    main(-2, 2, -2, 2, 0.0078125, 9, 0.0, -0.6)