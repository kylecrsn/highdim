from gdstlib import gen_point_set, dists_from_origin, dists_btwn_pts, angles_btwn_pts, plot_distribution

# Main entry point
if __name__ == '__main__':
  dimension = 1000
  count = 250
  radius = 1
  mean = 0
  deviation = 1

  # Get the set of basis points
  points = gen_point_set(count, dimension, radius, mean, deviation)

  # Compute the distribution of distances from the origin for each point and plot it
  origin_distances = dists_from_origin(points)
  plot_distribution(origin_distances, dimension, count, "Distribution From Origin", "Distance", "Probability", 
    "figs/origin_distance_distribution_d-" + str(dimension) + "_n-" + str(count) + ".svg")

  # Compute the distribution of the distances bettwen each pairwaise grouping of points
  pairwise_distances, pairwise_distances_matrix = dists_btwn_pts(points)
  plot_distribution(pairwise_distances, dimension, count, "Distribution Between Pairs", "Distance", "Probability", 
    "figs/pairwise_distance_distribution_d-" + str(dimension) + "_n-" + str(count) + ".svg")

  # Compute the distribution of the angles bettwen each pairwaise grouping of points
  pairwise_angles, pairwise_angles_matrix = angles_btwn_pts(points)
  plot_distribution(pairwise_angles, dimension, count, "Distribution Between Pairs", "Angle (degrees)", 
    "Probability", "figs/pairwise_angle_distribution_d-" + str(dimension) + "_n-" + str(count) + ".svg")