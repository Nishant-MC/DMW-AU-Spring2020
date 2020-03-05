# K-means clustering

Lab assignment 3: K-means clustering implementation.

The assignment code will have two important Python scripts:

```
data-generator.py
k-means.py
```

* **data-generator.py** is able to generate random coordinate data of arbitrary dimensionality for testing purposes. It has several possible configurations:

**No keyword arguments (kwargs)**: The code will create between 10,000 & 20,000 2-dimension coordinate pairs and output it as a space-delimited text file, output.txt. 
**5 kwargs**: To be filled in later.
**6 kwargs**: To be filled in later.

Examples of usage from the command line:

```
python3 data-generator.py
python3 data-generator.py 0 1000 2 12000 2d-data.txt
python3 data-generator.py 0 1000 3 10000 20000 3d-data.txt
```