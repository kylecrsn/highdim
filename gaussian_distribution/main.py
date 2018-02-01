import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy.stats as stats


# Generate a random point based on a Gaussian distribution in the given dimension
def gen_point(dim, mean, std):
  return np.random.normal(mean, std, dim)


# Generate a certain number of points for the given dimeansion
def gen_point_set(ct, dim, mean, std):
  point_set = []

  for i in xrange(ct):
    point_set.append(gen_point(dim, mean, std))

  return point_set


# Compute the distance of each of the given points from the origin
def dists_from_origin(pts):
  distances = []

  for i in xrange(len(pts)):
    summation = 0.0
    for j in xrange(len(pts[i])):
      summation += (pts[i][j] * pts[i][j])
    distances.append(math.sqrt(summation))

  return distances


# Compute the distance between each pair of points
def dists_between_pts(pts):
  distances = np.zeros((len(pts), len(pts)))

  for i in xrange(len(pts)):
    for j in xrange(i + 1, len(pts)):
      summation = 0.0
      for k in xrange(len(pts[i])):
        summation += (pts[i][k] - pts[j][k]) * (pts[i][k] - pts[j][k])
      distances[i][j] = math.sqrt(summation)

  return distances


# Plot the distribution of the given points
def plot_distribution(pts, dim, ct, title, x_label, y_label):
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
  plt.savefig('distribution_from_origin.svg', bbox_inches='tight')
  plt.show()


# Main entry point
if __name__ == '__main__':
  dimension = 900
  count = 2000

  # Get the set of basis points
  points = gen_point_set(count, dimension, 0, 1)

  # Compute the distribution of distances from the origin for each point and plot it
  distances_from_origin = dists_from_origin(points)
  plot_distribution(distances_from_origin, dimension, count, "Distribution From Origin", "Value", "Frequency")





# Generate a spherical Gaussain distribution
#   d - The dimension of the space
#   x - The number of points to generate
#   m - The mean (default is 0)
#   v - The variance (default is 1)
# def gen_vectors_old(d, x, m, v):
#   points = []
#   calc_mean = np.zeros(d)
#   calc_var = np.zeros(d)

#   # Find the mean
#   for i in range(x):
#     points.append(np.random.multivariate_normal(m, v))
#     calc_mean += (points[i] / x)

#   # Find the variance
#   for i in range(x):
#     calc_var += (np.power((points[i] - calc_mean), 2) / x)

#   # Find the standard deviation
#   calc_sigma = np.sqrt(calc_var)

#   z = np.linspace(calc_mean - 3*calc_sigma, calc_mean + 3*calc_sigma, x)
#   plt.plot(z, mlab.normpdf(z, calc_mean, calc_sigma))

#   plt.show()
#   print("Generation Completed")
#   return points, calc_mean, calc_var

  #target_mean = 0
  #target_variance = 1

  #mean_arr = [target_mean] * dimension
  #var_arr = [target_variance] * dimension
  #cov_arr = [var_arr] * dimension

  #points, calc_mean, calc_var = generator(dimension, sample, mean_arr, cov_arr)

  ##vectors = gen_gaussian_vectors(dimension, count)
  #vectors = sample_spherical(1, 50)
  #printPoints(vectors)
  ##vector_mean = calcVectorMean(vectors)
  ##sorted_mean = sorted(vector_mean)
  ##total_mean= np.mean(sorted_mean)
  ##total_std = np.std(sorted_mean)
  ##print total_mean
  ##print total_std

  ##fit = stats.norm.pdf(sorted_mean, total_mean, total_std)
  ##plt.plot(sorted_mean, fit, '-o')
  ##plt.hist(sorted_mean, normed=True)
  ##plt.show()



# # Generate a single random number according to a unit Gaussian distribution (0-mean, 1-var)
# def gen_gaussian():
#   basis = 0

#   while basis == 0:
#     basis = round(np.random.random() * 100)

#   vals = np.random.random(int(basis))
#   gaussian = (float(np.sum(vals)) - (basis / 2)) / math.sqrt(basis / 12.0)

#   return gaussian


# # Generate a set of Gaussian vector
# def gen_gaussian_vectors(dimension, count):
#   vecs = []

#   for i in xrange(count):
#     dim_vec = []
#     for j in xrange(dimension):
#       dim_vec.append(gen_gaussian())

#     vecs.append(dim_vec)

#   print("Generation Completed")
#   return vecs


# # Calculate the mean
# def calcVectorMean(vectors):
#   return np.divide(np.sum(vectors, axis=0), len(vectors))



# # Print out the list of points
# def printPoints(vectors):
#   for i in range(len(vectors)):
#     print("{}\n".format(vectors[i]))


# def sample_spherical(npoints, ndim=3):
#   vec = np.random.randn(ndim, npoints)
#   vec /= np.linalg.norm(vec, axis=0)
#   return vec