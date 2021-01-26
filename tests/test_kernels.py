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
import kernels

# -----------------------------------------
# Test Functions
# -----------------------------------------



# ------- KernelDownloader ----------------


def test_KernelDownloader_A():
    """ Test that direct file download works (using 'download_data()' )  """
    """ N.B. This also tests underlying 'kernels_have_been_downloaded()' """
    
    # *** SET-UP : CREATE EMPTY SUB-DIRECTORY ********************
    # Need to define an obscode to allow the objects to be created
    obscode = '-95'
    sd = convenience_function_to_create_empty_subdirectory(obscode)
    
    # *** SET-UP Instructions-Object *****************************
    I = wis.obscodeDict[obscode]
    
    # *** TEST "download_data()" *********************************
    # Assert that the required files exist
    downloadedKernelFiles =  I.download_data(sd)
    for f in I.files :
        assert f[f.rfind("/")+1:] in downloadedKernelFiles
        
    # *** TEST "kernels_have_been_downloaded()"*******************
    # Assert that the required files exist
    downloaded, downloadedKernelFiles =  I.kernels_have_been_downloaded(sd)
    assert downloaded , ' Expected downloaded to be True, but : [%r]'% downloaded
    for f in I.files:
        assert f[f.rfind("/")+1:] in downloadedKernelFiles
    
    


# ------- KernelLoader --------------------

def test_KernelLoader_A():
    """Test that a download directory can be created/accessed"""
    dd = wis.KernelLoader().define_download_dir()
    assert os.path.isdir(dd), 'Results of _define_download_dir [%r] not a path' % dd


def test_KernelLoader_B():
    """Test that a download sub-directory can be created/accessed"""
    obscode = '-95'
    # Need to define an obscode & JD to allow the Manager-object to be created
    M = wis.KernelLoader()
    dd = M.define_download_dir()
    # Use the method to get the subdirectory
    sd = M.define_download_subdir(obscode)
    # Assert that the returned subdirectory has the expected name
    expectedName = os.path.join(dd,obscode)
    assert sd == expectedName, ' Sub-dir names not the same: [%r],[%r]' % (sd , expectedName)

    # Deliberately delete the subdirectory
    if os.path.isdir(sd):
        shutil.rmtree(sd)
    assert not os.path.isdir(sd), 'Unexpectedly could not remove path [%r]' % sd

    # Now call the define_download_subdir method again and check that the directory is created
    sd = M.define_download_subdir(obscode)
    assert os.path.isdir(sd), 'download_subdir [%r] not a path' % sd






# -----------------------------------------
# Convenience Functions
# -----------------------------------------

def convenience_function_to_create_empty_subdirectory(obscode):
    """ A few of the tests need an empty directory. This creates a correctly named directory"""
    # Manager-object
    M = wis.Manager()
    # Main directory
    dd = M.define_download_dir()
    # subdirectory
    sd = M.define_download_subdir(obscode)
    # Assert that the returned subdirectory has the expected name
    expectedName = os.path.join(dd,obscode)
    assert sd == expectedName, ' Sub-dir names not the same: [%r],[%r]' % (sd , expectedName)
    
    # Deliberately delete the subdirectory
    if os.path.isdir(sd):
        shutil.rmtree(sd)
    assert not os.path.isdir(sd), 'Unexpectedly could not remove path [%r]' % sd

    # Now call the define_download_subdir method again and check that the directory is created
    sd = M.define_download_subdir(obscode)
    assert os.path.isdir(sd), 'download_subdir [%r] not a path' % sd
    
    # return the filepath to the subdirectory
    return sd

def convenience_function_for_loading_spicepy_kernels():
    kernelFilepaths = []
    sp.furnsh(kernelFilepaths)


