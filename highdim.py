import json
import math
import numpy as np
import matplotlib.pyplot as mplt
import scipy.stats as stats


# A Gaussian distribution in d-dimensional space
class GaussianPoint:

  def __init__(self, dim, mean, sdev):
    self.dimension = dim
    self.mean = mean
    self.standard_deviation = sdev
    self.values = []

  # Generate a single point, which is a vector with its length determined by the dimension and
  # its values determined by the Gaussian distribution parameterized on the given mean and
  # standard deviation
  def generate_values(self):
    self.values = list(np.random.normal(self.mean, self.standard_deviation, self.dimension))

  # Calculate the pairwise Euclidean distance between two points
  @staticmethod
  def pairwise_distance(x, y):
    distance = 0.0

    for i in xrange(x.dimension):
      distance += math.pow(x.values[i] - y.values[i], 2)
    distance = math.sqrt(distance)

    return distance

  # Calculate the pairwise angle between two points with respect to the origin using Law of Cosines
  @staticmethod
  def pairwise_angle(x, y):
    origin = GaussianPoint(x.dimension, x.mean, x.standard_deviation)
    origin.values = [0.0] * x.dimension
    angle = 0.0

    xo_dist = GaussianPoint.pairwise_distance(x, origin)
    yo_dist = GaussianPoint.pairwise_distance(y, origin)
    xy_dist = GaussianPoint.pairwise_distance(x, y)

    # angle = cos^-1((xo^2 + yo^2 - xy^2) / (2 * xo * yo))
    length_sum = math.pow(xo_dist, 2) + math.pow(yo_dist, 2) - math.pow(xy_dist, 2)
    angle = math.degrees(math.acos(length_sum / (2 * xo_dist * yo_dist)))

    return angle


# A cluster of N Gaussian distributions in d-dimensional space
class GaussianCluster:

  def __init__(self, ct, dim, mean, sdev):
    self.count = ct
    self.dimension = dim
    self.mean = mean
    self.standard_deviation = sdev
    self.points = []

  # Generate a cluster of the specified size
  def generate_cluster(self):
    for i in xrange(self.count):
      p = GaussianPoint(self.dimension, self.mean, self.standard_deviation)
      p.generate_values()
      self.points.append(p)

  # Calculate the pairwise distances between each point in the cluster and the origin
  def origin_distances(self):
    origin = GaussianPoint(self.dimension, self.mean, self.standard_deviation)
    origin.values = [0.0] * self.dimension
    o_dists = []

    for i in xrange(self.count):
      o_dists.append(GaussianPoint.pairwise_distance(self.points[i], origin))

    return o_dists

  # Calculate the pairwise Euclidean distances of all the points in the cluster
  # Returns the distances as both a list (list_dists) and a matrix (matrix_dists)
  def cluster_distances(self):
    matrix_dists = np.zeros((self.count, self.count))
    list_dists = []

    for i in xrange(self.count):
      for j in xrange(i + 1, self.count):
        dist = GaussianPoint.pairwise_distance(self.points[i], self.points[j])
        matrix_dists[i][j] = dist
        list_dists.append(dist)

    return list_dists, matrix_dists

  # Calculate the pairwise angles of all the points with respect to the origin
  # Returns the angles as both a list (list_angles) and a matrix (matrix_angles)
  def cluster_angles(self):
    matrix_angles = np.zeros((self.count, self.count))
    list_angles = []

    for i in xrange(self.count):
      for j in xrange(i + 1, self.count):
        angle = GaussianPoint.pairwise_angle(self.points[i], self.points[j])
        matrix_angles[i][j] = angle
        list_angles.append(angle)

    return list_angles, matrix_angles

  # Project a cluster from d-dimensional space to k-dimensional space where k << d
  # Returns a projected copy of the original cluster
  def project_to_subspace(self, sdim):
    projected_cluster = GaussianCluster(self.count, sdim, self.mean, self.standard_deviation)

    for i in xrange(self.count):
      projected_point = GaussianPoint(sdim, self.mean, self.standard_deviation)
      for j in xrange(sdim):
        unit_point = GaussianPoint(self.dimension, 0.0, 1.0)
        unit_point.generate_values()
        dot = np.dot(self.points[i].values, unit_point.values)
        projected_point.values.append(dot)
      projected_cluster.points.append(projected_point)

    return projected_cluster


# Statistics on the Gaussian cluster data
class GaussianStats:

  # Calculate the percentage error between expected and sampled values
  @staticmethod
  def pct_err(expected, sampled):
    return 100.0 * (abs(sampled - expected) / expected)

  # Apply theoretical projection scaling on the d-dimensional distances
  @staticmethod
  def generate_scaled_distances(distances, sdim):
    return np.array(distances) * math.sqrt(sdim)

  # Compute the theoretical expected value for the distance between two points in a projected 
  # cluster
  @staticmethod
  def generate_expected_distance(dim, sdim):
    return math.sqrt(2 * dim * sdim)

  # Calculate the percentage error between the expected distance value and the average of
  # some given distances
  @staticmethod
  def pct_err_distance_average(distances, dim, sdim):
    average = np.sum(distances) / len(distances)
    return GaussianStats.pct_err(GaussianStats.generate_expected_distance(dim, sdim), average)

  # Calculate the percentage error between the expected distance value and the max of some
  # given distances
  @staticmethod
  def pct_err_distance_max(distances, dim, sdim):
    expected_distance = GaussianStats.generate_expected_distance(dim, sdim)
    max_distance = 0

    for i in xrange(len(distances)):
      dist = abs(distances[i] - expected_distance)
      if dist > max_distance:
        max_distance = dist

    return GaussianStats.pct_err(expected_distance, expected_distance - max_distance)

  # Create a plot visualizing the distribution of data
  @staticmethod
  def plot_distribution(points, title, x_label, y_label, legend, fname):
    sorted_points = sorted(points)
    mean = np.mean(sorted_points)
    deviation = np.std(sorted_points)
    variance = np.var(sorted_points)
    fitted_curve = stats.norm.pdf(sorted_points, mean, deviation)
    padding = -0.1

    mplt.title(title)
    mplt.xlabel(x_label)
    mplt.ylabel(y_label)
    mplt.figtext(0.5, padding, legend, horizontalalignment='center', fontsize=12, multialignment='left', 
                bbox=dict(boxstyle="round", facecolor='#FFFFFF', ec="0.5", pad=0.5, alpha=1))
    mplt.plot(sorted_points, fitted_curve, '-o')
    mplt.hist(sorted_points, density=True)
    mplt.savefig(fname, bbox_inches='tight')
    mplt.show()


# Custom JSON encoder class for GaussianCluster and GaussianPoint objects
class GaussianEncoder(json.JSONEncoder):

  def default(self, o):
    if isinstance(o, GaussianCluster):
      cluster = {'count': o.count, 'dimension': o.dimension, 'mean': o.mean, 'standard_deviation': o.standard_deviation, 'points': []}
      for i in xrange(o.count):
        src = o.points[i]
        point = {'dimension': src.dimension, 'mean': src.mean, 'standard_deviation': src.standard_deviation, 'values': []}
        for j in xrange(src.dimension):
          point['values'].append(src.values[j])
        cluster['points'].append(point)
      return cluster
    return super(GaussianEncoder, self).default(o)
