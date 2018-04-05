# Example Output

The files above were generated with the following:

| Parameter           | Flag | Value |
| ------------------- |:----:| ----- |
| count               | -c   | 200   |
| dimension           | -d   | 400   |
| projected dimension | -p   | 40    |
| mean                | -m   | 0.0   |
| standard deviation  | -s   | 1.0   |

This information is representend by the combination of the flag letter followed by the value at the beginning of each file. After this is what the file's data actually represents, in JSON and PNG formats. The JSON files represent the actual data computed/generated for the cluster, while the PNG files are images showing the PDF's for various metrics.

JSON files:

- **\*\_cluster.json**: The data contained by the original cluster object, including each Gaussian value of each point
- **\*\_cluster\_angles.json**: The list of angles between each pair of points in the original cluster
- **\*\_cluster\_dists.json**: The list of distances between each pair of points in the original cluster
- **\*\_origin_\_dists.json**: The list of distances between each point and the origin in the original cluster
- **\*\_percent\_error.json**: The average and max percentage errors in the theoretical versus original scaled distances and theoretical versus projected distances
- **\*\_projected\_cluster.json**: The data contained by the projected cluster object, including each Gaussian value of each point
- **\*\_projected\_cluster\_angles.json**: The list of angles between each pair of points in the projected cluster
- **\*\_projected\_cluster\_dists.json**: The list of distances between each pair of points in the projected cluster
- **\*\_projected\_origin\_dists.json**: The list of distances between each point and the origin in the projected cluster
- **\*\_scaled\_cluster\_dists.json**: The list of distances between each pair of points in the original cluster *multiplied* by the square root of the projected dimension, so as to scale the values to the theorical expectation (and use them to compare to the projected cluster)

PNG files:

- **\*\_cluster\_angles.png**: The distribution of angle values in the original cluster
- **\*\_cluster\_dists.png**: The distribution of pairwise distance values in the original cluster
- **\*\_origin_\_dists.png**: The distribution of distance-from-origin values in the original cluster
- **\*\_projected\_cluster\_angles.png**: The distribution of angle values in the projected cluster
- **\*\_projected\_cluster\_dists.png**: The distribution of pairwise distance values in the projected cluster
- **\*\_projected\_origin\_dists.png**: The distribution of distance-from-origin values in the projected cluster
- **\*\_scaled\_cluster\_dists.png**: The distribution of pairwise distance values in the original cluster *multiplied* by the square root of the projected dimension