=====
Usage
=====

To use wis.py in a project::

    import wis

    import numpy as np 
    from astropy.time import Time

    # Time & Obscode of interest
    # NB '-95' == TESS 
    time    = Time([2458337.829157830, 2458338.829157830], format='jd', scale='tdb')
    obscode = '-95'

    # Call wis.wis
    W = wis.wis(obscode, time)

    # Position info is available in the posn variable ...
    print( W.posns )
