# This example has the most of what I want. One issue is there might be too much freedom?

import datetime
import random
import matplotlib.pyplot as plt

# make up some data
x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]
y = [i+random.gauss(0, 1) for i, _ in enumerate(x)]

# plot
plt.plot(x, y)
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()
