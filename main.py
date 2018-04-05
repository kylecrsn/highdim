import sys
import os
import io
import argparse
import json
from datetime import datetime
import highdim


# Main entry point
if __name__ == '__main__':
  # Parse command line arguments
  parser = argparse.ArgumentParser(description='Tool for analyzing Gaussians in high dimension')
  parser.add_argument('-v', '--verbose', action='store_true', help='detailed console logging')
  parser.add_argument('-c', '--count', type=int, help='number of points in the distribution', default=50)
  parser.add_argument('-d', '--dimension', type=int, help='dimensional size of the space, number of axes', default=400)
  parser.add_argument('-p', '--projected', type=int, help='projected dimensional size of the space')
  parser.add_argument('-m', '--mean', type=float, help='target mean of the distribution', default=0.0)
  parser.add_argument('-s', '--standard_deviation', type=float, help='target standard deviation of the distribution', default=1.0)
  args = parser.parse_args()

  # Error handling of arguments
  if args.count < 1:
    print('Error: Must specify a positive, non-zero number of points')
    sys.exit(1)
  if args.dimension < 1:
    print('Error: Must specify a positive, non-zero dimension')
    sys.exit(1)
  if (args.projected and args.projected >= args.dimension):
    print('Error: The projected dimension must be smaller than the value specified by --dimension')
    sys.exit(1)
  if args.mean < 0.0:
    print('Error: Must specify a positive mean')
    sys.exit(1)
  if args.standard_deviation < 0.0:
    print('Error: Must specify a positive standard deviation')
    sys.exit(1)

  count = args.count
  dimension = args.dimension
  mean = args.mean
  standard_deviation = args.standard_deviation
  cluster = highdim.GaussianCluster(count, dimension, mean, standard_deviation)
  output_dir = 'output_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
  try:
    os.makedirs(output_dir)
  except OSError as e:
    print('An error occurred while attempting to create the output directory')
  details = output_dir + '/c' + str(count) + '_d' + str(dimension) + '_m' + str(mean) + '_s' + str(standard_deviation)
  legend = "Dimension: " + str(dimension) + "\nNumber of Points: " + str(count)

  # Generate the cluster
  cluster.generate_cluster()
  tfn = details + '_cluster.json'
  with io.open(tfn, 'w', encoding='utf-8') as f:
    f.write(unicode(json.dumps(cluster, cls=highdim.GaussianEncoder, sort_keys=True, indent=4, ensure_ascii=False)))
  if args.verbose:
    print json.dumps(cluster, cls=highdim.GaussianEncoder, sort_keys=True, indent=4, ensure_ascii=False)

  # Calculate the distances from origin
  o_dists = cluster.origin_distances()
  tfn = details + '_origin_dists.json'
  ifn = details + '_origin_dists.png'
  with io.open(tfn, 'w', encoding='utf-8') as f:
    f.write(unicode(json.dumps(o_dists, sort_keys=True, indent=4, ensure_ascii=False)))
  highdim.GaussianStats.plot_distribution(o_dists, 'Distances From Origin', 'Distance', 'PDF', legend, ifn)
  if args.verbose:
    print json.dumps(o_dists, sort_keys=True, indent=4, ensure_ascii=False)

  # Calculate the distances between each pair of points
  list_dists, matrix_dists = cluster.cluster_distances()
  tfn = details + '_cluster_dists.json'
  ifn = details + '_cluster_dists.png'
  with io.open(tfn, 'w', encoding='utf-8') as f:
    f.write(unicode(json.dumps(list_dists, sort_keys=True, indent=4, ensure_ascii=False)))
  highdim.GaussianStats.plot_distribution(list_dists, 'Distances Between Pairs', 'Distance', 'PDF', legend, ifn)
  if args.verbose:
    print json.dumps(list_dists, sort_keys=True, indent=4, ensure_ascii=False)

  # Calculate the angles between each pair of points relative to the origin
  list_angles, matrix_angles = cluster.cluster_angles()
  tfn = details + '_cluster_angles.json'
  ifn = details + '_cluster_angles.png'
  with io.open(tfn, 'w', encoding='utf-8') as f:
    f.write(unicode(json.dumps(list_angles, sort_keys=True, indent=4, ensure_ascii=False)))
  highdim.GaussianStats.plot_distribution(list_angles, 'Angles Between Pairs', 'Angle (degrees)', 'PDF', legend, ifn)
  if args.verbose:
    print json.dumps(list_angles, sort_keys=True, indent=4, ensure_ascii=False)

  if not args.projected:
    print 'Analysis Complete'
    print 'Check ' + output_dir + '/ for results'
    sys.exit(0)

  original_list_dists = list_dists
  projected = args.projected
  details = output_dir + '/c' + str(count) + '_d' + str(projected) + '_m' + str(mean) + '_s' + str(standard_deviation)
  legend = "Dimension: " + str(projected) + "\nNumber of Points: " + str(count)

  # Generate the projection of the cluster as a new cluster in lower-dimensional space
  projected_cluster = cluster.project_to_subspace(projected)
  tfn = details + '_projected_cluster.json'
  with io.open(tfn, 'w', encoding='utf-8') as f:
    f.write(unicode(json.dumps(projected_cluster, cls=highdim.GaussianEncoder, sort_keys=True, indent=4, ensure_ascii=False)))
  if args.verbose:
    print json.dumps(projected_cluster, cls=highdim.GaussianEncoder, sort_keys=True, indent=4, ensure_ascii=False)

  # Calculate the projected distances from origin
  o_dists = projected_cluster.origin_distances()
  tfn = details + '_projected_origin_dists.json'
  ifn = details + '_projected_origin_dists.png'
  with io.open(tfn, 'w', encoding='utf-8') as f:
    f.write(unicode(json.dumps(o_dists, sort_keys=True, indent=4, ensure_ascii=False)))
  highdim.GaussianStats.plot_distribution(o_dists, 'Distances From Origin', 'Distance', 'PDF', legend, ifn)
  if args.verbose:
    print json.dumps(o_dists, sort_keys=True, indent=4, ensure_ascii=False)

  # Calculate the projected distances between each pair of points
  list_dists, matrix_dists = projected_cluster.cluster_distances()
  tfn = details + '_projected_cluster_dists.json'
  ifn = details + '_projected_cluster_dists.png'
  with io.open(tfn, 'w', encoding='utf-8') as f:
    f.write(unicode(json.dumps(list_dists, sort_keys=True, indent=4, ensure_ascii=False)))
  highdim.GaussianStats.plot_distribution(list_dists, 'Distances Between Pairs', 'Distance', 'PDF', legend, ifn)
  if args.verbose:
    print json.dumps(list_dists, sort_keys=True, indent=4, ensure_ascii=False)
  projected_list_dists = list_dists

  # Calculate the projected angles between each pair of points relative to the origin
  list_angles, matrix_angles = projected_cluster.cluster_angles()
  tfn = details + '_projected_cluster_angles.json'
  ifn = details + '_projected_cluster_angles.png'
  with io.open(tfn, 'w', encoding='utf-8') as f:
    f.write(unicode(json.dumps(list_angles, sort_keys=True, indent=4, ensure_ascii=False)))
  highdim.GaussianStats.plot_distribution(list_angles, 'Angles Between Pairs', 'Angle (degrees)', 'PDF', legend, ifn)
  if args.verbose:
    print json.dumps(list_angles, sort_keys=True, indent=4, ensure_ascii=False)

  # Calculate the scaled distances between each pair of points
  # NOTE: The original dimension scaled should be similar to the projected
  list_dists = highdim.GaussianStats.generate_scaled_distances(original_list_dists, projected).tolist()
  tfn = details + '_scaled_cluster_dists.json'
  ifn = details + '_scaled_cluster_dists.png'
  with io.open(tfn, 'w', encoding='utf-8') as f:
    f.write(unicode(json.dumps(list_dists, sort_keys=True, indent=4, ensure_ascii=False)))
  highdim.GaussianStats.plot_distribution(list_dists, 'Distances Between Pairs (Scaled)', 'Distance', 'PDF', legend, ifn)
  if args.verbose:
    print json.dumps(list_dists, sort_keys=True, indent=4, ensure_ascii=False)

  # Calculate percentage error comparsing the scaled and projected characteristics
  details = output_dir + '/c' + str(count) + '_d' + str(dimension) + '_p' + str(projected) + '_m' + str(mean) + '_s' + str(standard_deviation)
  tfn = details + '_percent_error.json'
  err = {'Average': {'Original Dimension Scaled': None, 'Projected Dimension': None}, 
        'Max': {'Original Dimension Scaled': None, 'Projected Dimension': None}}
  err['Average']['Original Dimension Scaled'] = \
    str(highdim.GaussianStats.pct_err_distance_average(list_dists, dimension, projected))
  err['Average']['Projected Dimension'] = \
    str(highdim.GaussianStats.pct_err_distance_average(projected_list_dists, dimension, projected))
  err['Max']['Original Dimension Scaled'] = \
    str(highdim.GaussianStats.pct_err_distance_max(list_dists, dimension, projected))
  err['Max']['Projected Dimension'] = \
    str(highdim.GaussianStats.pct_err_distance_max(projected_list_dists, dimension, projected))
  with io.open(tfn, 'w', encoding='utf-8') as f:
    f.write(unicode(json.dumps(err, sort_keys=True, indent=4, ensure_ascii=False)))
  if args.verbose:
    print json.dumps(err, sort_keys=True, indent=4, ensure_ascii=False)

  print 'Analysis Complete'
  print 'Check ' + output_dir + '/ for results'
  sys.exit(0)
