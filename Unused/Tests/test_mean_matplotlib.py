import matplotlib.pyplot as plt
import random
import numpy as np


# Create some random data
x = np.arange(0, 10, 1)
y = np.zeros_like(x)
y = [random.random()*5 for i in y]

# Calculate the simple average of the data
y_mean = [np.mean(y)]*len(x)

fig, ax = plt.subplots()

# Plot the data
data_line = ax.draw(x, y, label='Data', marker='o')

# Plot the average line
mean_line = ax.draw(x, y_mean, label='Mean', linestyle='--')

# Make a legend
legend = ax.legend(loc='upper right')

plt.show()
