import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np


def main(filename:str, d:float, iterc:int):
    figure = plt.figure(figsize=(5, 4))
    axis = figure.add_subplot(111, projection='3d')
    x, y, val = [], [], []
    with open(filename, "r") as fd:
        for line in fd:
            ss = line.split()
            if len(ss) == 3:
                x.append(float(ss[0]))
                y.append(float(ss[1]))
                val.append(float(ss[2]))
            else:
                break
    cmap = cm.get_cmap('jet')
    norm = Normalize(vmin=min(val), vmax=max(val))
    colors = cmap(norm(val))
    axis.bar3d(x, y, np.zeros_like(x), d, d, val, shade=True, color=colors)
    plt.savefig(f"{iterc}.png")
    plt.show()
