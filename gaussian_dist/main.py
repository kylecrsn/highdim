import math
import numpy as np
import matplotlib.pyplot as plt

# Generate a spherical Gaussain distribution
#   d - The dimension of the space
#   x - The number of points to generate
#   m - The mean (default is 0)
#   v - The variance (default is 1)
def generator(d, x, m, v):
  points = []
  calc_mean = 0
  calc_var = 0
  for i in range(x):
    vec = np.random.multivariate_normal(m, v)
    points.append(vec)
    calc_mean += vec[0]

  calc_mean /= x
  print calc_mean

  for i in range(x):
    calc_var += np.power((points[i] - calc_mean), 2)[0]
  calc_var /= x
  print calc_var

  print("Test complete")

if __name__ == '__main__':
  dimension = 1
  points = 10000
  mean = 0
  var = 1

  mean_arr = []
  var_arr = []
  cov_arr = []

  for i in range(dimension):
    mean_arr.append(mean)
    var_arr.append(var)

  for i in range(dimension):
    cov_arr.append(var_arr)

  generator(dimension, points, mean_arr, cov_arr)