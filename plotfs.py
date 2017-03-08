# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 14:58:07 2017

@author: User327
"""

def plotHist(x, nh=50):
    # http://matplotlib.org/1.2.1/examples/pylab_examples/histogram_demo.html
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt
    import numpy as np
    # the histogram of the data
    n, bins, patches = plt.hist(x, bins=nh, normed=1, facecolor='green', alpha=0.75)

    
    # add a 'best fit' line
    mu = np.mean(x)
    sigma = np.sqrt(np.var(x))
    y = mlab.normpdf( bins, mu, sigma)
    l = plt.plot(bins, y, 'r--', linewidth=1)

    plt.xlabel('Scores')
    plt.ylabel('Frequency')
    plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    plt.axis([min(x) - 0.1*abs(min(x)), max(x) + 0.1*abs(max(x)), 0, 1.1*max(y)])
    plt.grid(True)

    plt.show()
    
def plot1Curve(x,y):
    from pylab import plot
    plot(x, y, color="blue", linewidth=2.5, linestyle='-')
    