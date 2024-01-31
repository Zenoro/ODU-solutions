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
    # G = nx.DiGraph()
    start_time = time.time()
    lengx = abs(x1 - x0) / h
    for gh in range(iterc):
        h /= 2
        lengx *= 2
    G = hyperloop(x0, x1, y0, y1, h*2, lengx/2, 4, a, b)
    nx.write_graphml_xml(G,'tmpgraph')
    print(iterc, " iteration is done! Time elapsed: ", (time.time() - start_time))
    with open('buf', 'w') as f:
        f.write(f'{h} {lengx} {iterc}')


def new_iterat(x0,x1,y0,y1,a,b, iterc):
    start = time.time()
    with open('buf', 'r') as f:
        h, lengx, _ = map(float, f.readline().split())
    newG = hyperloop(x0,x1,y0,y1,h,lengx,4,a,b)
    os.remove('tmpgraph')
    nx.write_graphml_xml(newG, 'tmpgraph')
    print(f"{int(iterc)} iteration is done! Time elapsed: {time.time() - start}")
    with open('buf', 'w') as f:
        f.write(f'{h/2} {lengx*2} {iterc}')


def draw(x0, x1, y0, y1, is_grid):
    G = nx.read_graphml('tmpgraph', node_type=int, edge_key_type=int)
    with open('buf', 'r') as f:
        h, lengx, gh = map(float, f.readline().split())
        h*=2
        lengx/=2
    xposition = lambda cell, leng: x0 + h * (cell - (cell - 1) // leng * leng - 1)
    yposition = lambda cell, leng: y1 - h * ((cell - 1) // leng + 1)
    plt.title(f'{int(gh)} iteration')
    plt.xlim((x0-0.5), (x1+0.5))
    plt.ylim((y0-0.5), (y1+0.5))
    ax = plt.gca()
    # fd = open('buf', 'w')
    total_cells = 0
    for c in nx.strongly_connected_components(G):
        if len(c) > 1:
            total_cells += len(c)
            for elem in list(c):
                # fd.write(f"{xposition(alist[k], lengx)} {yposition(alist[k], lengx)}\n")
                ss = patches.Rectangle((xposition(elem, lengx), 
                                        yposition(elem, lengx)), 
                                        h, h, color = 'blue', fill=True)
                ax.add_patch(ss)
    print(f"Total number of cells: {total_cells}")
    if is_grid:
        plt.grid()
    # fd.close()
    plt.show()


