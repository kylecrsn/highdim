import math as m
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from gaussian_distribution.main import *


# Main entry point
if __name__ == '__main__':
  dimension = 1000
  count = 20

  # Get the set of basis points
  points = gen_point_set(count, dimension, 0, 1)

  # Compute the distribution of distances from the origin for each point and plot it
  origin_distances = dists_from_origin(points)
  plot_distribution(origin_distances, dimension, count, "Distribution From Origin", "Distance", "Frequency", "origin_distance_distribution.svg")

  # Compute the distribution of the distances bettwen each pairwaise grouping of points
  pairwise_distances, pairwise_distances_matrix = dists_btwn_pts(points)
  plot_distribution(pairwise_distances, dimension, count, "Distribution Between Pairs", "Distance", "Frequency", "pairwise_distance_distribution.svg")

  # Compute the distribution of the angles bettwen each pairwaise grouping of points
  pairwise_angles, pairwise_angles_matrix = angles_btwn_pts(points)
  plot_distribution(pairwise_angles, dimension, count, "Distribution Between Pairs", "Angle (degrees)", "Frequency", "pairwise_angle_distribution.svg")