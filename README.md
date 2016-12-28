# TCX-to-text

A couple of Python scripts to join and transform TCX files into one text file.

*TCXtoTSVpoints.py* joins one or several TCX files into one TSV text file. Each row contains the ''ID'' of the track, ''date'' when logged the track, and a pair of lat-long coordinates.

*TCXtoTSVwithKML.py* joins one or several TCX files into one TSV text file. Each row contains the ''ID'' of the track, ''date'' when logged the track, and a KML-styled line with several pairs of coordinates (+ altitude).

This code was forked from this [bspauld's project](https://github.com/bspauld/TCXtoShape). In order to execute it you would need some python libraries:
* [Fiona](http://toblerity.org/fiona/manual.html)
* [Shapely](http://toblerity.org/shapely/manual.html)
* [pyproj](https://pypi.python.org/pypi/pyproj/)

