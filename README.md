Sample Overlap
==============

overlap.py filters a set of files based on common column names. overlap.py requires at least two files, but will work with more. overlap.py produces new files with the extension ```.out```.

Currently overlap.py only works with tab delimited files.

Usage:
```
overlap.py file1 file2 [file3 ...]
overlap.py file1 file2 [file3 ...] -k 1
```

The ```-k``` flag can be used for keeping any columns that don't have overlapping IDs. If, for example, the first columns of your file contain rownames which you want to keep, but the headers don't match, you can use ```-k 1```.

Install:
```
git clone https://github.com/shilab/sample_overlap
cd sample_overlap
python setup.py install
```

