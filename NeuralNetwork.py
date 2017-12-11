import urllib
from numpy import linalg
from urllib import request
import numpy as np

fname = "https://stepic.org/media/attachments/lesson/16462/boston_houses.csv"
f = urllib.request.urlopen(fname)  # open file from URL
data = np.loadtxt(f, delimiter=',', skiprows=1)  # load data to work with
X = np.hstack((np.ones_like(data[:, 0:1]), data[:, 1:]))
X = linalg.inv(X.T.dot(X)).dot(X.T).dot(data[:, 0])
print(" ".join(map(str, X)))
