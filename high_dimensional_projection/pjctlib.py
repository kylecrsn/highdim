import os
import sys
import math as m
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

sys.path.insert(0, os.path.join(os.path.dirname(sys.path[0]), 'gaussian_distribution'))
import gdstlib as gdst


# Genrate the projection of the given points from d-dimension to k-dimension
def project_point_set(pts, dim, sdim, rad):
  point_set = []

  for i in xrange(len(pts)):
    point = []
    for j in xrange(sdim):
      point.append(np.dot(pts[i], gdst.gen_point(dim, 1, 0, 1)))
    point_set.append(point)

  return point_set


# Generate the scaled pairwise distances along with the overall and max percentage of error between vectors
def projection_difference(distances_dim, distances_sdim, dim, sdim, rad):
  distances_dim_scaled = np.array(distances_dim) * m.sqrt(sdim)
  expected_distance = (m.sqrt(2 * dim) * m.sqrt(sdim)) * rad
  max_distance_dim_scaled = 0
  max_distance_sdim = 0

  for i in xrange(len(distances_dim_scaled)):
    if abs(distances_dim_scaled[i] - expected_distance) > max_distance_dim_scaled:
      max_distance_dim_scaled = abs(distances_dim_scaled[i] - expected_distance)

  for i in xrange(len(distances_sdim)):
    if abs(distances_sdim[i] - expected_distance) > max_distance_sdim:
      max_distance_sdim = abs(distances_sdim[i] - expected_distance)

  avg_distance_dim_scaled = np.sum(distances_dim_scaled) / len(distances_dim_scaled)
  avg_distance_sdim = np.sum(distances_sdim) / len(distances_sdim)

  pct_avg_dim_scaled = percent_error(expected_distance, avg_distance_dim_scaled)
  pct_avg_sdim = percent_error(expected_distance, avg_distance_sdim)
  pct_max_dim_scaled = percent_error(expected_distance, expected_distance - max_distance_dim_scaled)
  pct_max_sdim = percent_error(expected_distance, expected_distance - max_distance_sdim)

  return distances_dim_scaled, pct_avg_dim_scaled, pct_avg_sdim, pct_max_dim_scaled, pct_max_sdim


# Compute the percent error between an expected and given value
def percent_error(expected, given):
  return 100 * (abs(given - expected) / expected)