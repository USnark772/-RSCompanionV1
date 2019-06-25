# This is an example of using sliders on the graph

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

fig = plt.figure()
ax = fig.add_subplot(111)
fig.subplots_adjust(left=0.25, bottom=0.25)
min0 = 0
max0 = 10

x = np.arange(10)
y = np.arange(10)
im1 = plt.scatter(x,y, s=3, c=u'b', edgecolor='None',alpha=.75)
# most examples here return something iterable

plt.ylim([0,10])#initial limits

axmin = fig.add_axes([0.25, 0.1, 0.65, 0.03])
axmax  = fig.add_axes([0.25, 0.15, 0.65, 0.03])

smin = Slider(axmin, 'Min', 0, 10, valinit=min0)
smax = Slider(axmax, 'Max', 0, 10, valinit=max0)


def update(val):
    plt.ylim([smin.val, smax.val])

plt.subplot(111)
smin.on_changed(update)
smax.on_changed(update)

plt.show()