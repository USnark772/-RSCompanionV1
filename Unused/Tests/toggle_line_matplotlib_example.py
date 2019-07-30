"""
Enable picking on the legend to toggle the original line on and off
"""
import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0.0, 0.2, 0.1)
y1 = 2*np.sin(2*np.pi*t)
y2 = 4*np.sin(2*np.pi*2*t)
y3 = 4*np.sin(9*np.pi**t)
y4 = 6*np.sin(7*np.pi*t)

fig, ax = plt.subplots()
ax.set_title('Click on legend line to toggle line on/off')
test_lines = {}
test_lines["plot"] = []
line1, = ax.plot(t, y1, lw=2, color='red', label='1 HZ')
test_lines["plot"].append(line1)
line2, = ax.plot(t, y2, lw=2, color='blue', label='2 HZ')
test_lines["plot"].append(line2)
line3, = ax.plot(t, y3, lw=2, color='green', label='_nolegend_')
test_lines["plot"].append(line3)
line4, = ax.plot(t, y4, lw=2, color='orange', label='_nolegend_')
test_lines["plot"].append(line4)
print(test_lines)
leg = fig.legend('upper left')
#leg = fig.legend(test_lines["plot"], ("1 HZ", "2 HZ"), 'upper left')
#leg = ax.legend(loc='upper left', fancybox=True, shadow=True)
leg.get_frame().set_alpha(0.4)


# we will set up a dict mapping legend line to orig line, and enable
# picking on the legend line
lines = [[line1, line3], [line2, line4]]
lined = dict()
for legline, origline in zip(leg.get_lines(), lines):
    legline.set_picker(5)  # 5 pts tolerance
    lined[legline] = origline


def onpick(event):
    # on the pick event, find the orig line corresponding to the
    # legend proxy line, and toggle the visibility
    legline = event.artist
    origlines = lined[legline]
    for line in origlines:
        vis = not line.get_visible()
        line.set_visible(vis)
    # Change the alpha on the line in the legend so we can see what lines
    # have been toggled
    if vis:
        legline.set_alpha(1.0)
    else:
        legline.set_alpha(0.2)
    fig.canvas.draw()


fig.canvas.mpl_connect('pick_event', onpick)

plt.show()
