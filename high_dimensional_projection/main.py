import os
import sys
from pjctlib import project_point_set, projection_difference

sys.path.insert(0, os.path.join(os.path.dirname(sys.path[0]), 'gaussian_distribution'))
import gdstlib as gdst


# Main entry point
if __name__ == '__main__':
  dimension = 900
  subdimension = 1
  count = 20
  radius = 30
  mean = 0
  deviation = 1

  # Get the set of basis points
  points = gdst.gen_point_set(count, dimension, radius, mean, deviation)

  # Compute the distribution of the distances between each pairwaise grouping of points in d-dim
  pairwise_distances_d, pairwise_distances_k_matrix = gdst.dists_btwn_pts(points)
  gdst.plot_distribution(pairwise_distances_d, dimension, count, "Distribution Between Pairs [d-dim]", "Distance", "Probability", 
    "figs/pairwise_distance_distribution_d-dim_d-" + str(dimension) + "_k-" + str(subdimension)+ "_n-" + str(count) + ".png")

  # Project the set of basis points from d-dimensions to k-dimensions
  projection_points = project_point_set(points, dimension, subdimension, radius)

  # Compute the distribution of the distances between each pairwaise grouping of points in k-dim
  pairwise_distances_k, pairwise_distances_k_matrix = gdst.dists_btwn_pts(projection_points)
  gdst.plot_distribution(pairwise_distances_k, dimension, count, "Distribution Between Pairs [k-dim]", "Distance", "Probability", 
    "figs/pairwise_distance_distribution_k-dim_d-" + str(dimension) + "_k-" + str(subdimension)+ "_n-" + str(count) + ".png", subdimension)

  # Compute the difference between the original distance values * root(subdimension) and the distance values for the subdimension
  pairwaise_distances_d_scaled, avg_distance_d_scaled, avg_distance_k, max_distance_d_scaled, max_distance_k = projection_difference(
    pairwise_distances_d, pairwise_distances_k, dimension, subdimension, radius)
  gdst.plot_distribution(pairwaise_distances_d_scaled, dimension, count, "Distribution Between Pairs [d-dim scaled]", "Distance", "Probability", 
    "figs/pairwise_distance_distribution_d-dim_scaled_d-" + str(dimension) + "_k-" + str(subdimension)+ "_n-" + str(count) + ".png", subdimension)
  print("Average Distance % Error")
  print("d-dim scaled: {}".format(avg_distance_d_scaled))
  print("k-dim: {}".format(avg_distance_k))
  print("\nMax Distance % Error")
  print("d-dim scaled: {}".format(max_distance_d_scaled))
  print("k-dim: {}".format(max_distance_k))
