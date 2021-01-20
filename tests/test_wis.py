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




def test_Satellite_E_via_wis():
    """
    Test that a Satellite-object returns the expected positions for multiple jdutc's
    Here we are repeating test_satellites.test_Satellite_E(), but routing it via the top-level "wis.wis" function
    """
    # Time & Obscode of interest
    time    = Time([2458337.829157830, 2458338.829157830], format='jd', scale='tdb')
    obscode = '-95'
    
    # Call wis.wis
    W = wis.wis(obscode, time)
    
    # Because we input a *SATELLITE* obs-code, we expect to get back a Satellite-Class object
    assert isinstance(W, wis.Satellite )

    # Assert that the returned quantities have the expected numerical values
    # -->> We input                   jdutc = [2458337.8283571, 2458337.8283571]
    # -->> So we query horizons using tdb   = [2458338.82915783,2458338.82915783]
    expectedPosns = np.array([
                              [1.062342805938861E+08 ,-1.082364019892699E+08 ,-7.200821989670396E+04],
                              [1.081418885028859E+08 ,-1.064747162599978E+08 ,1.748584038066864E+04]
                              ] )
    assert np.allclose(W.posns , expectedPosns, rtol=1e-05, atol=1e+02), \
        ' Not close enough to expected values: returned=[%r], expected=[%r]' % (W.posns , expectedPosns)


def test_excluded_via_wis():
    """ Test that the 247 obs-code is excluded """
    
    # Time & Obscode of interest
    time    = Time([2458337.829157830, 2458338.829157830], format='jd', scale='tdb')
    obscode = '247'
    
    # Call wis.wis
    W = wis.wis(obscode, time, EXCLUDE_AS_GEO = False )
    
    # Because we input obscode 247, we expect to get back a NoneType object
    assert isinstance(W, type(None) )
