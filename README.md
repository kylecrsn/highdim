# highdim

> A simple tool for analyzing Gaussians in high-order dimensional space


## About

The geometric behavior of data in high dimensional space can be quite counter-intuitive. This tool provides a simple abstraction of the unit sphere whose points makeup a Gaussian distribution with variably large dimensionality. It calculates the PDF for various metrics such as the pairwise distance between all points, the distance between points and the origin, and so on. Additionally, it can project a dataset to a lower-dimensional representation in order to study the relationship between projected and scaled distributions

Some demo output can be found in `example/`. Here, we start with a zero-mean, unit-variance sphere with 250 points in d=400 dimensions. We then project the dataset down to k=40 dimensions, and compare the various metrics of our original dataset scaled by a factor of sqrt(k) to the data in the projected set. Finally, we compute some error percentages between the expected and actual outputs. For more perspective on the significance of all this, check out the primer in the [Theoretical Background](#theoretical-background) section below


## Getting Started

#### Linux (Ubuntu)

1. Make sure Python 2.7.x is installed
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

5. Run `main.py -h` to check the CLI options/defaults. the `-v` flag will dump text ouput to the console in addition to the files created in the `output-*` directory
```bash
python main.py -h
```


## API



## Theoretical Background

