#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wis` package."""

# -----------------------------------------
# Third-party imports
# -----------------------------------------
import spiceypy as sp
import pytest
import os
import sys
import shutil
import numpy as np
from astropy.time import Time
from timeit import default_timer as timer

# -----------------------------------------
# Local imports
# -----------------------------------------
test_dir = os.path.dirname(os.path.realpath(__file__))
wis_dir  = os.path.dirname(test_dir)
code_dir = os.path.join(wis_dir, 'wis')
sys.path.insert(0,code_dir)
import wis

# -----------------------------------------
# Test Functions
# -----------------------------------------

def test_speed_Ground_A():
    """
    Test speed of execution of multiple calls to get positions from the ground
    Initial tests suggest 0.3s for 10^4 evaluations
    """

    # Select some obs-codes
    from kernel_spec_ground     import ground_obscode_dict , GRND
    n_o = 100
    rand_obscodes = np.random.choice( list(ground_obscode_dict.keys()) , n_o)
    
    # Select some dates
    n_t = 100
    JD0 = 2451545.0
    rand_times = JD0 + np.random.choice( 100, n_t)
    times   = Time( rand_times, format='jd', scale='tdb')
    
    # Initialize ...
    start_times = Time( rand_times[:2], format='jd', scale='tdb')
    W = wis.wis(rand_obscodes[0], start_times)
    
    # Query each obscode for all times
    start = timer()
    for obscode in rand_obscodes:
        W.get_posns(obscode , times )
    end = timer()
    elapsed = end - start
    assert elapsed < 1.0
    
test_speed_Ground_A()
