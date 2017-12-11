import urllib
from numpy import linalg
from urllib import request
import numpy as np

fname = "https://stepic.org/media/attachments/lesson/16462/boston_houses.csv"
f = urllib.request.urlopen(fname)  # open file from URL
data = np.loadtxt(f, delimiter=',', skiprows=1)  # load data to work with
b = linalg.inv(data[:, 1:].T.dot(data[:, 1:])).dot(data[:, 1:].T).dot(data[:, 0])
print(" ".join(map(str, b)))
