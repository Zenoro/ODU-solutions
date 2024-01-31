import matplotlib.patches as patches
import matplotlib.pyplot as plt

plot_names = ["(oY, oZ)", "(oX, oZ)", "(oX, oY)"]
plt.figure(figsize=(10,3))
for i in range(1,4):
    plt.subplot(1, 3, i)
    plt.title(plot_names[i-1])
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    ax = plt.gca()
    with open(f"{i}buf", 'r') as fd:
        for line in fd.readlines():
            x, y, d = map(float, line.split())
            ss = patches.Rectangle((x, y), d, d)
            ax.add_patch(ss)

plt.savefig("res.png")
