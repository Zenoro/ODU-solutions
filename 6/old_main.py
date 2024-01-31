import time
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as patches
import math as m
import os
# import multiprocessing

def f(t,x,y,alpha,beta,k,B,omega):
    return alpha*x + beta*x**3 - k*y + B*m.cos(omega*t)


def g(t,x,y):
    return y


def euler(x0, y0, alpha, beta, omeg, k, B, step):
    t0 = 0
    while t0<1:
        xrz = x0 + f(t0, x0, y0, alpha, beta, k, B, omeg)*step
        yrz = y0 + g(t0, x0, y0)*step
        t0 += step
        x0 = xrz
        y0 = yrz
    return xrz, yrz


def duffing(x0, y0, alpha, beta, omeg, k, B):
    h = 0.02
    # omeg = 1
    # tmax = 2*m.pi/omeg
    tmax = 1
    # k = 0.25
    # B = 0.03
    # alpha = -0.8
    # beta = 0.3
    t0 = 0
    # f = lambda t, x, y: alpha*x + beta*x**3 - k*y + B*m.cos(omeg*t)
    # g = lambda t, x, y: y
    while t0 <= tmax:
        k1 = h*f(t0, x0, y0, alpha, beta, k, B, omeg)
        q1 = h*g(t0, x0, y0)

        k2 = h*f(t0+h/2.0, x0+q1/2.0, y0+k1/2.0, alpha, beta, k, B, omeg)
        q2 = h*g(t0+h/2.0, x0+q1/2.0, y0+k1/2.0)

        k3 = h*f(t0+h/2.0, x0+q2/2.0, y0+k2/2.0, alpha, beta, k, B, omeg)
        q3 = h*g(t0+h/2.0, x0+q2/2.0, y0+k2/2.0)

        k4 = h*f(t0+h, x0+q3, y0+k3, alpha, beta, k, B, omeg)
        q4 = h*g(t0+h, x0+q3, y0+k3)

        y1 = y0+(k1+2.0*k2+2.0*k3+k4)/6.0
        x1 = x0+(q1+2.0*q2+2.0*q3+q4)/6.0
        t0 += h
        x0 = x1
        y0 = y1
    return x0, y0


def cell_dribling(item, leng):
    lengnew = leng*2
    new1 = 2*item-1+(item-1)//leng*lengnew
    new2 = new1+1
    new3 = new1+lengnew
    new4 = new2+lengnew
    return new1, new2, new3, new4


def hyperloop(xdown:float, xup:float, ydown:float, yup:float, 
              h:float, leng:float, s_list:list[int], 
              pt:int, alph:float, bet:float, omega:float, K:float, B:float, flg=True):
    G = nx.DiGraph()
    cou = 1
    xtmp = xdown
    ytmp = yup
    xckl = xdown
    yckl = yup
    counter_the_one_we_are_on_now = 0
    while yckl > ydown:
        while xckl < xup:
            counter_the_one_we_are_on_now += 1
            if counter_the_one_we_are_on_now in s_list:
                for _ in range(0, pt):
                    ytmp -= 1 / pt*h

                    for _ in range(0, pt):
                        xtmp += 1 / pt*h

                        xrz, yrz = duffing(xtmp, ytmp, alph, bet, omega, K, B)
                        # xrz = round(xfunc(xtmp, ytmp), 6)
                        # yrz = round(yfunc(xtmp, ytmp), 6)

                        if xrz < xdown or xrz > xup or yrz < ydown or yrz > yup:
                            continue
                        cell = m.floor(((yup - yrz) / h)) * leng + m.ceil((xrz - xdown) / h) // 1 + 1
                        # if cell not in cell_list:
                            # cell_list.append(cell)
                        G.add_edge(int(cou), int(cell))

                    xtmp = xckl

            xckl += h
            xtmp = xckl
            ytmp = yckl
            cou += 1
        yckl -= h
        xckl = xdown
        xtmp = xckl
        ytmp = yckl
    if flg:
        for _ in range(5):
            nodesbeforethat = G.number_of_nodes()
            nodes_to_remove = [node for node, in_degree in G.in_degree() if in_degree <= 0]
            G.remove_nodes_from(nodes_to_remove)
            if G.number_of_nodes() == nodesbeforethat:
                break
    return G


def main(x0:float, x1:float, y0:float, y1:float, h:float, pts:int,
         iterc:int, alpha:float, beta:float, omega:float, k:float, B:float):
    G = nx.DiGraph()
    start = time.time()
    lengx = abs(x1 - x0) / h
    lengy = abs(y1 - y0) / h
    list_good_dots = [q for q in range(1, int(lengx*lengy))]
    for gh in range(iterc):
        h /= 2
        lengx *= 2
        G = hyperloop(x0, x1, y0, y1, h*2, lengx/2, list_good_dots, pts, alpha, beta, omega, k, B)
        list_good_dots = list(G.nodes())
        if gh != iterc-1:
            G.clear()
        newbuf = list_good_dots
        list_good_dots = []
        for i in range(len(newbuf)):
            list_good_dots += cell_dribling(newbuf[i], lengx)
        print(gh+1, " iteration is done! Time elapsed: ", (time.time() - start))
    with open('time.out', 'w') as ff:
        ff.write(f"{time.time() - start}")
    nx.write_graphml_xml(G,'tmpgraph')
    with open('buf', 'w') as f:
        f.write(f'{h} {lengx} {iterc}\n')
        f.write(f"{' '.join(map(str, map(int, list_good_dots)))}")


def new_iterat(x0, x1, y0, y1, iterc, alpha, beta, omega, k, B):
    newG = nx.DiGraph()
    start = time.time()
    with open('buf', 'r') as f:
        h, lengx, _ = map(float, f.readline().split())
        list_good_dots = list(map(int, f.readline().split()))
    newG = hyperloop(x0, x1, y0, y1, h, lengx, list_good_dots, 5, alpha, beta, omega, k, B)
    h /= 2
    lengx *= 2
    list_good_dots = list(newG.nodes())
    newbuf = list_good_dots
    """????"""
    list_good_dots = []
    for i in range(len(newbuf)):
        list_good_dots += cell_dribling(newbuf[i], lengx)
    os.remove('tmpgraph')
    nx.write_graphml_xml(newG, 'tmpgraph')
    print(f"{int(iterc)} iteration is done! Time elapsed: {time.time() - start}")
    with open('time.out', 'w') as ff:
        ff.write(f"{time.time() - start}")
    with open('buf', 'w') as f:
        f.write(f'{h} {lengx} {iterc}\n')
        f.write(f"{' '.join(map(str, map(int, list_good_dots)))}")


def draw(x0, x1, y0, y1, is_grid):
    G = nx.read_graphml('tmpgraph', node_type=int, edge_key_type=int)
    with open('buf', 'r') as f:
        h, lengx, gh = map(float, f.readline().split())
        h*=2
        lengx/=2
    xposition = lambda cell, leng: x0 + h * (cell - (cell - 1) // leng * leng - 1)
    yposition = lambda cell, leng: y1 - h * ((cell - 1) // leng + 1)
    # plt.title(f'{int(gh)} iteration')
    plt.xlim(x0, x1)
    plt.ylim(y0, y1)
    ax = plt.gca()
    # fd = open('buf', 'w')
    total_cells = 0
    print("Creating matplotlib graph...")
    for c in nx.kosaraju_strongly_connected_components(G):
        total_cells += len(c)
        if len(c) > 1:
            for elem in list(c):
                # fd.write(f"{xposition(alist[k], lengx)} {yposition(alist[k], lengx)}\n")
                ss = patches.Rectangle((xposition(elem, lengx), 
                                        yposition(elem, lengx)), 
                                        h, h, color = 'blue', fill=True)
                ax.add_patch(ss)
        else:
            for elem in list(c):
                ss = patches.Rectangle((xposition(elem, lengx), 
                                        yposition(elem, lengx)), 
                                        h, h, color = 'black', fill=True)
                ax.add_patch(ss)
    ss = patches.Rectangle((0, 0), h, h, color = 'black', fill=True)
    with open("sys.out", 'w') as ff:
        ff.write(f"{total_cells}")
    if is_grid:
        plt.grid()
    plt.savefig(f"res{int(gh)}.png")
    plt.clf()
    plt.close()


def main_for_place(x0:float, x1:float, y0:float, y1:float, h:float, pts:int,
         iterc:int, alpha:float, beta:float, omega:float, k:float, B:float):
    G = nx.DiGraph()
    start = time.time()
    lengx = abs(x1 - x0) / h
    lengy = abs(y1 - y0) / h
    list_good_dots = [q for q in range(1, int(lengx*lengy))]
    for gh in range(iterc):
        h /= 2
        lengx *= 2
        G = hyperloop(x0, x1, y0, y1, h*2, lengx/2, list_good_dots, pts, alpha, beta, omega, k, B, False)
        list_good_dots = list(G.nodes())
        if gh != iterc-1:
            G.clear()
        newbuf = list_good_dots
        list_good_dots = []
        for i in range(len(newbuf)):
            list_good_dots += cell_dribling(newbuf[i], lengx)
        print(gh+1, " iteration is done! Time elapsed: ", (time.time() - start))
    h*=2
    lengx /= 2
    max_component = max(nx.kosaraju_strongly_connected_components(G), key=len)
    odnaych = list(max_component)[0]
    nodes_with_route_to_odnaych = nx.ancestors(G, odnaych)
    print("Creating matplotlib graph...")
    xposition = lambda cell, leng: x0 + h * (cell - (cell - 1) // leng * leng - 1)
    yposition = lambda cell, leng: y1 - h * ((cell - 1) // leng + 1)
    plt.xlim(x0, x1)
    plt.ylim(y0, y1)
    ax = plt.gca()
    for e in nodes_with_route_to_odnaych:
        x, y = xposition(e, lengx), yposition(e, lengx)
        ss = patches.Rectangle((x, y), h, h, color = 'black', fill=True)
        ax.add_patch(ss)
    plt.savefig(f"area{iterc}.png")
    plt.clf()
    plt.close()