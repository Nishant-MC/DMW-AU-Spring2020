# K-means clustering

Lab assignment 3: K-means clustering implementation.

The assignment code has two important Python scripts:

```
data-generator.py
k-means.py
```

* **data-generator.py** is able to generate random coordinate data of arbitrary dimensionality over arbitrary ranges. It is thus able to generate a robust suite of tests for our k-means algorithm implementation. It accepts up to 6 kwargs: cmin, cmax, dimensionality, # of pts LB, # of pts UB, output file name. You can specify an exact number of points (5 kwargs instead of 6) and it will still work. It has default behavior in case no kwargs are specified.

Example usage(s):

```
python3 data-generator.py -- initiates default behavior (see code for more details)
python3 data-generator.py 0 1000 2 100 2d-data.txt —- exactly 100 2-d pts in (0,1k) range, piped to a file test-data.txt
python3 data-generator.py 0 100000 2 1000 2000 2d-data.txt —— somewhere b/w 1k-2k 2-d pts in (0,1m) range, piped to a file 2d-data.txt
```


* **k-means.py** is our implementation of the k-means algorithm. It randomly selects points in the given dataset (space-delimited file) as cluster centroids and proceeds with the algorithm until convergence or a specified execution limit is reached. It can produce a simple scatterplot visualization of its computations.


Example usage(s):

```
python3 k-means.py 2d-data.txt 5 100 —— Performs k-means clustering on the dataset in 2d-data.txt. Sets number of clusters (k) = 5, execution limit = 100
```

Errata:

* RSS (residual sum of squares) threshold testing was not implemented. We have no way to know good RSS values for arbitrary datasets so it seemed pointless to implement support for it.

* Scatterplots become very crowded after 2k+ points are plotted, so the visualization becomes quite useless for very big data sets. That said, the algorithm should efficiently run for arbitrarily large datasets quite well.