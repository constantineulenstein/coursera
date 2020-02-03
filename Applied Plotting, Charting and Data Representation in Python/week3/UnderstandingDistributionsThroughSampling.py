
# coding: utf-8

# # Practice Assignment: Understanding Distributions Through Sampling
#
# ** *This assignment is optional, and I encourage you to share your solutions with me and your peers in the discussion forums!* **
#
#
# To complete this assignment, create a code cell that:
# * Creates a number of subplots using the `pyplot subplots` or `matplotlib gridspec` functionality.
# * Creates an animation, pulling between 100 and 1000 samples from each of the random variables (`x1`, `x2`, `x3`, `x4`) for each plot and plotting this as we did in the lecture on animation.
# * **Bonus:** Go above and beyond and "wow" your classmates (and me!) by looking into matplotlib widgets and adding a widget which allows for parameterization of the distributions behind the sampling animations.
#
#
# Tips:
# * Before you start, think about the different ways you can create this visualization to be as interesting and effective as possible.
# * Take a look at the histograms below to get an idea of what the random variables look like, as well as their positioning with respect to one another. This is just a guide, so be creative in how you lay things out!
# * Try to keep the length of your animation reasonable (roughly between 10 and 30 seconds).

# In[5]:

import matplotlib.pyplot as plt
import numpy as np

get_ipython().magic('matplotlib notebook')

# generate 4 random variables from the random, gamma, exponential, and uniform distributions
x1 = np.random.normal(-2.5, 1, 10000)
x2 = np.random.gamma(2, 1.5, 10000)
x3 = np.random.exponential(2, 10000)+7
x4 = np.random.uniform(14,20, 10000)

# plot the histograms
plt.figure(figsize=(9,3))
plt.hist(x1, normed=True, bins=20, alpha=0.5)
plt.hist(x2, normed=True, bins=20, alpha=0.5)
plt.hist(x3, normed=True, bins=20, alpha=0.5)
plt.hist(x4, normed=True, bins=20, alpha=0.5);
plt.axis([-7,21,0,0.6])

plt.text(x1.mean()-1.5, 0.5, 'x1\nNormal')
plt.text(x2.mean()-1.5, 0.5, 'x2\nGamma')
plt.text(x3.mean()-1.5, 0.5, 'x3\nExponential')
plt.text(x4.mean()-1.5, 0.5, 'x4\nUniform')


# In[ ]:

from random import sample
import matplotlib.animation as animation
fig, ((normal, gamma), (exponential, uniform)) = plt.subplots(2, 2)

sample_size = 200
bins = 20
x1 = sample(list(x1), sample_size)
x2 = sample(list(x2), sample_size)
x3 = sample(list(x3), sample_size)
x4 = sample(list(x4), sample_size)

def update(curr):
    # check if animation is at the last frame, and if so, stop the animation a
    if curr == sample_size:
        a.event_source.stop()
    normal.cla()
    gamma.cla()
    exponential.cla()
    uniform.cla()
    normal.hist(x1[:curr], bins=bins)
    normal.axis([-6, 1, 0, 30])
    gamma.hist(x2[:curr], bins=bins)
    gamma.axis([0, 17, 0, 30])
    exponential.hist(x3[:curr], bins=bins)
    exponential.axis([7, 20, 0, 30])
    uniform.hist(x4[:curr], bins=bins)
    uniform.axis([14, 20, 0, 30])
    normal.title.set_text('Normal')
    gamma.title.set_text('Gamma')
    exponential.title.set_text('Exponential')
    uniform.title.set_text('Uniform')
    normal.annotate('n = {}'.format(curr), [-1, 27])
    if curr == 1:
        fig.tight_layout()

a = animation.FuncAnimation(fig, update, interval=20)


# In[ ]:



