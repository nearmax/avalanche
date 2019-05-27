import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mpl


class Plot:
    def __init__(self, title, splits, bars):
        self.title = title
        self.splits = splits
        self.fig = plt.figure(figsize=(8, 2))
        self.ax = self.fig.add_axes([0.05, 0.80, 0.9, 0.15])
        cmap = LinearSegmentedColormap.from_list('redblue', colors=[(1, 0, 0), (0, 0, 1)])
        norm = mpl.colors.Normalize(vmin=0, vmax=1)
        _cbar = mpl.colorbar.ColorbarBase(self.ax, cmap=cmap, norm=norm, orientation='horizontal')
        for bar in bars:
            self.ax.plot([bar, bar], [0.0, 1.0], 'k:', linewidth=3)
        self.line = self.ax.plot([0.5, 0.5], [0.0, 1.0], 'k-', linewidth=3)[0]

    def update(self, i):
        round, split = self.splits[i]
        self.line.set_xdata(split)
        self.ax.set_xlabel('{0} round {1} split {2:.3f}'.format(self.title, round, split))
        return self.line, self.ax


def plot(splits, bars, title, filename):
    p = Plot(title, splits, bars)
    anim = FuncAnimation(p.fig, p.update, frames=np.arange(0, len(splits)), interval=100)
    anim.save(filename, dpi=80,  writer="imagemagick")
