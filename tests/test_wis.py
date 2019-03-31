#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `wis` package."""

# -----------------------------------------
# Third-party imports
# -----------------------------------------
import spiceypy as sp
import pytest

# -----------------------------------------
# Local imports
# -----------------------------------------
from wis import wis

# -----------------------------------------
# Test Functions
# -----------------------------------------

def test_obscodeDict_A():
    
    """Test obscodeDict exists and has content."""
    assert isinstance(wis.obscodeDict, dict), 'Problem with wis.obscodeDict: not a dict? '
    assert len(wis.obscodeDict) > 0 ,         'Problem with wis.obscodeDict: no entries? %r' % wis.obscodeDict

def test_obscodeDict_B():

    """Test obscodeDict has all expected entries"""
    assert '-95' in wis.obscodeDict,          'TESS key (-95) not in wis.obscodeDict'
    assert '-227' in wis.obscodeDict,         'K2  key (-227) not in wis.obscodeDict'
    assert '-82' in wis.obscodeDict,         'CASSINI  key (-82) not in wis.obscodeDict'

def test_obscodeDict_C():
    """Test obscodeDict values are Instructions-objects"""
    for k,v in wis.obscodeDict.items():
        assert isinstance(v, wis.Instructions), '[%r] for [%r] not an Instructions-object' % (v,k)

def test_obscodeDict_D():
    """Test Instructions-objects contain minimum requirements"""
    for k,v in wis.obscodeDict.items():
        for requiredKey in ['obscode','name', 'files']:
            assert hasattr(v, requiredKey), 'requiredKey [%r] not in (%r, %r)' % (requiredKey,k,v)



def test_Manager_download_dir_A():
    """Test that a download directory can be created/accessed"""
    dd = wis.Manager().define_download_dir()
    assert os.path.isdir(dd), 'Results of _define_download_dir [%r] not a path' % dd

def test_Manager_download_dir_B():
    """Test that a download sub-directory can be created/accessed"""
    obscode = '-95'
    # Need to define an obscode & JD to allow the Manager-object to be created
    dd = wis.Manager().define_download_dir()
    # Use the method to get the subdirectory
    sd = dd.define_download_subdir(obscode)
    # Assert that the returned subdirectory has the expected name
    expectedName = os.path.join(dd,obscode)
    assert sd == expectedName, ' Sub-dir names not the same: [%r],[%r]' % (sd , expectedName)

    # Deliberately delete the subdirectory
    if os.path.isdir(sd):
        os.remove(sd)
    assert not os.path.isdir(sd), 'Unexpectedly could not remove path [%r]' % sd

    # Now call the define_download_subdir method again and check that the directory is created
    sd = dd.define_download_subdir(obscode)
    assert os.path.isdir(sd), 'download_subdir [%r] not a path' % sd



### Add in direct tests of INSTRUCTIONS ###




def test_Instructions_kernels_have_been_downloaded_A():
    """Test that local file access works (full directory) """
    
    # *** SET-UP : CREATE EMPTY SUB-DIRECTORY ********************
    # Need to define an obscode to allow the objects to be created
    obscode = '-95'
    # Create an Instructions-object
    I  = wis.Instructions()
    # Lets also define a "Manager" to get the download_dir name
    dd = wis.Manager().define_download_dir()
    sd = dd.define_download_subdir(obscode)
    assert os.path.isdir(sd), 'could not make path : [%r]' % sd
    # Forcibly delete destination sub-directory
    os.remove(sd)
    # Recreate sub-dir (now must be empty)
    sd = dd.define_download_subdir(obscode)
    
    # *** SET-UP : CREATE EMPTY FILES ****************************
    # "Touch" a file in the sub-directory (to create something)
    for f in wis.obscodeDict[obscode].files:
        fp = os.path.join(sd,f)
        open(x, 'a').close()
    for f in wis.obscodeDict[obscode].values().replace("*","_"):
        fp = os.path.join(sd,f)
        open(x, 'a').close()
    
    # *** ACTUAL TEST ********************************************
    # Assert that files exist
    downloaded, kernelFiles =  I.kernels_have_been_downloaded(sd)
    assert downloaded , ' Expected downloaded to be True, but : [%r]'% downloaded
    for f in wis.obscodeDict[obscode].files:
        assert f in kernelFiles
    for f in wis.obscodeDict[obscode].values().replace("*","_"):
        assert f in kernelFiles




def test_Instructions_download_dir_B():
    """Test that local file access works (empty directory)"""
    
    # *** SET-UP : CREATE EMPTY SUB-DIRECTORY ********************
    # Need to define an obscode to allow the objects to be created
    obscode = '-95'
    # Create an Instructions-object
    I  = wis.Instructions()
    # Lets also define a "Manager" to get the download_dir name
    dd = wis.Manager().define_download_dir()
    sd = dd.define_download_subdir(obscode)
    assert os.path.isdir(sd), 'could not make path : [%r]' % sd
    # Forcibly delete destination sub-directory
    os.remove(sd)
    # Recreate sub-dir (now must be empty)
    sd = dd.define_download_subdir(obscode)

    # *** ACTUAL TEST ********************************************
    # Assert that the files have NOT been downloaded (because the directory is empty)
    downloaded, kernelFiles =  I.kernels_have_been_downloaded(sd)
    assert not downloaded , ' Expected downloaded to be == False, but : [%r]'% downloaded

def test_Instructions_download_dir_C():
    pass

def test_Satellite_A():
    """Test that a Satellite-object can be created/accessed"""
    obscode, jdutc = -95', 2458337.8283571
    returnedOC     = wis.Satellite(obscode, jdutc).obscode
    assert returnedOC == obscode, 'Returned obscode [%r] does not match input [%r]' % (returnedOC , obscode)
    returnedOC     = wis.Satellite(obscode, jdutc, center = 'SUN').obscode
    assert returnedOC == obscode, 'Returned obscode [%r] does not match input [%r]' % (returnedOC , obscode)


def test_Satellite_B():
    """Test that a Satellite-object correctly calculates internal epochs (consistent with sp.utc2et() )"""
    # Make a Satellite-object and get the epochs
    obscode, jdutc = -95', [2458337.8283571, 2458337.9]
    returnedEpochs = wis.Satellite(obscode, jdutc).epochs
    # Check epoch calcs are correct
    for i, jd in enumerate(jdutc):
        assert returnedEpochs[i] == sp.utc2et('JD'+str(jd)), 'Returned epoch [%r] does not match calculatoin from spiceypy [%r]' % (returnedEpochs[i] , jd)

def test_Satellite_C():
    """Test that a Satellite-object returns posns and ltts"""
    # Make a Satellite-object
    obscode, jdutc = -95', [2458337.8283571, 2458337.9]
    S = wis.Satellite(obscode, jdutc)
    # Assert that the returned quantities are of the correct shape and type
    assert S.posns.shape = (3,2), 'Returned posns not of expected shape: [%r]' % S.posns.shape
    assert S.ltts.shape  = (2,),  'Returned ltts  not of expected shape: [%r]' % S.ltts.shape

def test_Satellite_D():
    """Test that a Satellite-object returns posns and ltts"""
    # Make a Satellite-object
    obscode, jdutc = -95', [2458337.8283571, 2458337.9]
    S = wis.Satellite(obscode, jdutc)
    # Assert that the returned quantities have the expected numerical values
    print("S.posns=",S.posns)
    assert np.allclose(S.posns , np.array( [ [], [] ] ) )


'''
def test_download_data():
    TESS = wis.obscodeDict['-95']
    TESS.download_data()
'''
