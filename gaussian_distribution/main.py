import math as m
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


# Generate a random point based on a Gaussian distribution in the given dimension
def gen_point(dim, mean, std):
  return np.random.normal(mean, std, dim)


# Generate a specified number of points for the given dimension
def gen_point_set(ct, dim, mean, std):
  point_set = []

  for i in xrange(ct):
    point_set.append(gen_point(dim, mean, std))

  return point_set


# Compute the distance between two points in d dimension using the Euclidian formula
def dist_btwn_two_pts(x, y):
  summation = 0.0

  for i in xrange(len(x)):
    summation += m.pow(x[i] - y[i], 2)

  return m.sqrt(summation)


# Compute the angle between two points in d dimension using a Law of Cosines formula
def angle_btwn_two_pts(x, y):
  origin = [0.0] * len(x)
  xo_dist = dist_btwn_two_pts(x, origin)
  yo_dist = dist_btwn_two_pts(y, origin)
  xy_dist = dist_btwn_two_pts(x, y)

  return m.degrees(m.acos((m.pow(xo_dist, 2) + m.pow(yo_dist, 2) - m.pow(xy_dist, 2)) / (2 * xo_dist * yo_dist)))


# Compute the distance of each of the given points from the origin
def dists_from_origin(pts):
  distances = []
  origin = [0.0] * len(pts[0])

  for i in xrange(len(pts)):
    distances.append(dist_btwn_two_pts(pts[i], origin))

  return distances


# Compute the distance between each pair of points
def dists_btwn_pts(pts):
  distances = []
  distances_matrix = np.zeros((len(pts), len(pts)))

  for i in xrange(len(pts)):
    for j in xrange(i + 1, len(pts)):
      distances_matrix[i][j] = dist_btwn_two_pts(pts[i], pts[j])
      distances.append(distances_matrix[i][j])

  return distances, distances_matrix


# Compute the angle between each pair of points, where each point forms a line with the origin and the angle is measured at the origin intersection
def angles_btwn_pts(pts):
  angles = []
  angles_matrix = np.zeros((len(pts), len(pts)))

  for i in xrange(len(pts)):
    for j in xrange(i + 1, len(pts)):
      angles_matrix[i][j] = angle_btwn_two_pts(pts[i], pts[j])
      angles.append(angles_matrix[i][j])

  return angles, angles_matrix


# Plot the distribution of the given points
def plot_distribution(pts, dim, ct, title, x_label, y_label, fname):
  sorted_points = sorted(pts)
  mean = np.mean(sorted_points)
  deviation = np.std(sorted_points)
  variance = np.var(sorted_points)
  fitted_curve = stats.norm.pdf(sorted_points, mean, deviation)
  comment = "Dimension: " + str(dim) + "\nNumber of Points: " + str(ct)
  
  print("Mean: {}".format(mean))
  print("Variance: {}".format(variance))
  print("Standard Deviation: {}".format(deviation))

  plt.title(title)
  plt.xlabel(x_label)
  plt.ylabel(y_label)
  plt.figtext(0.5, -0.1, comment, horizontalalignment='center', fontsize=12, multialignment='left', 
    bbox=dict(boxstyle="round", facecolor='#FFFFFF', ec="0.5", pad=0.5, alpha=1))
  plt.plot(sorted_points, fitted_curve, '-o')
  plt.hist(sorted_points, normed=True)
  plt.savefig(fname, bbox_inches='tight')
  plt.show()


# Main entry point
if __name__ == '__main__':
  dimension = 1000
  count = 200

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