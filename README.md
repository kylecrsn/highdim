# highdim

> A simple tool for analyzing Gaussians in high-order dimensional space


## About

The geometric behavior of data in high dimensional space can be quite counter-intuitive. This tool provides a simple abstraction of the unit sphere whose points makeup a Gaussian distribution with variably large dimensionality. It calculates the PDF for various metrics such as the pairwise distance between all points, the distance between points and the origin, and so on. Additionally, it can project a dataset to a lower-dimensional representation in order to study the relationship between projected and scaled distributions.

Some demo output can be found in `example/`. Here, we start with a zero-mean, unit-variance sphere with 250 points in d=400 dimensions. We then project the dataset down to k=40 dimensions, and compare the various metrics of our original dataset scaled by a factor of sqrt(k) to the data in the projected set. Finally, we compute some error percentages between the expected and actual outputs.


## Getting Started

#### Linux (Ubuntu)

1. Make sure Python 2.7 is installed
```bash
python --version
# If not installed:
sudo apt-get update
sudo apt-get install python
```

2. Install pip and virtualenv
```bash
sudo apt-get install python-pip
pip install virtualenv
```

3. Clone the repo and setup a virtual environment for it
```bash
git@github.com:carsonkk/highdim.git
cd highdim/
virtualenv venv
source venv/bin/activate
```

4. Use `requirements.txt` to install dependencies
```bash
pip install -r requirements.txt
```

*NOTE: If this fails, the primary dependencies are numpy, scipy, and matplotlib. Look up articles/guides for how to get these installed if you're having problems*

5. Run `main.py -h` to check the command-line options. The `-v` flag will dump text ouput to the console in addition to the files created in the `output_*/` directory
```bash
# Check command-line options
python main.py -h

# Run with the default values:
# 50 points, 400 dimensions, no projection, 0-mean, 1-variance
python main.py

# Specify arguments to match the example/ output:
# 250 points, 400 dimensions, projected to 40 dimensions, 0-mean, 1-variance
python main.py -c 200 -d 400 -p 40 -m 0.0 -s 1.0
```


## API

#### GaussianPoint
Describes a single point in multi-dimensional space according to some Gaussian distribution

**\_\_init\_\_(self, ...)**
Constructor method

Parameters:

- dimension: The dimensionality of the distribution
- mean: The target mean to be used when generating the Gaussian values that make of the point-vector
- standard_deviation: The target standard deviation to be used when generating the Gaussian values that make of the point-vector

Additional Fields:

- values: The list of Gaussian values which represents the point, length is equal to the dimension (empty by default)

**generate_values(self)**
Populates the `values` field of the calling GaussianPoint instance

**pairwise_distance(GaussianPoint, GaussianPoint)**
Static method to determine the distance between two GaussianPoint's belonging to the same cluster (ie created with the same dimensionality, mean, standard deviation)

**pairwise_angle(GaussianPoint, GaussianPoint)**
Static method to determine the angle with respect to the origin between two GaussianPoint's belonging to the same cluster (ie created with the same dimensionality, mean, standard deviation)

#### GaussianCluster
Some number of GaussianPoint instances which make up a dataset

**\_\_init\_\_(self, ...)**
Constructor method

Parameters:

- count: The number of GaussianPoint instances that make up the cluster
- dimension: The dimensionality of the distribution
- mean: The target mean to be used when generating the Gaussian values that make of the point-vector
- standard_deviation: The target standard deviation to be used when generating the Gaussian values that make of the point-vector

Additional Fields:

- points: The list of GaussianPoint instances, length is equal to the count (empty by default)

**generate_points(self)**
Populates the `points` field of the calling GaussianCluster instance with GaussianPoint's

**origin_distances(self)**
Computes the Euclidean distance between each point in the cluster and the origin, returns a list of these distances

**cluster_distances(self)**
Computes the Euclidean distance between each pair of points in the cluster. Returns both a list and matrix representation of these distances, with everything below the diagonal in the matrix being 0's

**cluster_angles(self)**
Computes the angle with respect to the origin between each pair of points in the cluster. Returns both a list and matrix representation of these angles, with everything below the diagonal in the matrix being 0's

**project_to_subspace(self, ...)**
Project the current cluster to a lower dimensionality, returning the newly projected cluster

Parameters:

- sdim: The sub-dimension that the current cluster should be projected to

#### GaussianStats
This class provides static methods for computing the percentage error between the theoretical and expected values of the original (scaled) and projected clusters, in addition to a PDF plotter

#### GaussianEncoder
Encodes a GaussianCluster instance to JSON


## Theoretical Background

See Chapter 2 in [Foundations of Data Science](https://www.cs.cornell.edu/jeh/book.pdf) for the full context of studying Gaussians in high dimensions