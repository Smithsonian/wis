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

'''
def test_satellite_obscode_dict_A():
    
    """Test obscodeDict exists and has content."""
    assert isinstance(wis.satellite_obscode_dict, dict), 'Problem with wis.satellite_obscode_dict: not a dict? '
    assert len(wis.satellite_obscode_dict) > 0 ,         'Problem with wis.satellite_obscode_dict: no entries? %r' % wis.obscodeDict

def test_satellite_obscode_dict_B():

    """Test obscodeDict has all expected entries"""
    assert '-95' in wis.satellite_obscode_dict,          'TESS key (-95) not in wis.satellite_obscode_dict'
    assert '-227' in wis.satellite_obscode_dict,         'K2  key (-227) not in wis.satellite_obscode_dict'
    assert '-82' in wis.satellite_obscode_dict,         'CASSINI  key (-82) not in wis.satellite_obscode_dict'

def test_satellite_obscode_dict_C():
    """Test obscodeDict values are Instructions-objects"""
    for k,v in wis.satellite_obscode_dict.items():
        print('type=', type(v) )
        assert isinstance(v, kernels.KernelSpecifier ), '[%r] for [%r] not an Instructions-object' % (v,k)

def test_satellite_obscode_dict_D():
    """Test Instructions-objects contain minimum requirements"""
    for k,v in wis.satellite_obscode_dict.items():
        for requiredKey in ['obscode','name', 'files']:
            assert hasattr(v, requiredKey), 'requiredKey [%r] not in (%r, %r)' % (requiredKey,k,v)
'''

'''
    
def test_Manager_download_dir_A():
    """Test that a download directory can be created/accessed"""
    dd = wis.Manager().define_download_dir()
    assert os.path.isdir(dd), 'Results of _define_download_dir [%r] not a path' % dd


def test_Manager_download_dir_B():
    """Test that a download sub-directory can be created/accessed"""
    obscode = '-95'
    # Need to define an obscode & JD to allow the Manager-object to be created
    M = wis.Manager()
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





def test_Instructions_download_A():
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
    
    
'''



def test_Satellite_A():
    """Test that a Satellite-object can be created/accessed"""
    time    = Time([2458337.8283571], format='jd', scale='tdb')
    obscode = '-95'
    returnedOC     = wis.Satellite(obscode, time).obscode
    assert returnedOC == obscode, 'Returned obscode [%r] does not match input [%r]' % (returnedOC , obscode)
    returnedOC     = wis.Satellite(obscode, time, center = 'SUN').obscode
    assert returnedOC == obscode, 'Returned obscode [%r] does not match input [%r]' % (returnedOC , obscode)





def test_Satellite_B():
    """Test that a Satellite-object correctly calculates internal epochs (consistent with sp.utc2et() )"""
    # Make a Satellite-object and get the epochs
    time    = Time([2458337.8283571, 2458337.9], format='jd', scale='tdb')
    obscode = '-95'
    returnedEpochs = wis.Satellite(obscode, time).epochs
    
    # Check epoch calcs are correct
    for i, jd in enumerate(time.utc.jd):
        assert returnedEpochs[i] == sp.utc2et('JD'+str(jd)), \
            'Returned epoch [%r] does not match calculation from spiceypy [%r]' % (returnedEpochs[i] , jd)


def test_Satellite_C():
    """Test that a Satellite-object returns posns and ltts"""
    # Make a Satellite-object
    time    = Time([2458337.8283571, 2458337.9], format='jd', scale='tdb')
    obscode = '-95'
    S = wis.Satellite(obscode, time)
    # Assert that the returned quantities are of the correct shape and type
    assert S.posns.shape == (2,3), 'Returned posns not of expected shape: [%r]' % S.posns
    assert S.ltts.shape  == (2,),  'Returned ltts  not of expected shape: [%r]' % S.ltts


    
def test_Satellite_D():
    """Test that a Satellite-object returns the expected positions"""
    # Make a Satellite-object
    time    = Time([2458337.829157830], format='jd', scale='tdb')
    obscode = '-95'
    S = wis.Satellite(obscode, time)
    
    # *** DATA FROM EXPLICIT HORIZONS QUERY -------------
    """
*******************************************************************************
Ephemeris / WWW_USER Tue Jan 26 06:45:47 2021 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: TESS (spacecraft) (-95)         {source: TESS_merged}
Center body name: Sun (10)                        {source: TESS_merged}
Center-site name: BODY CENTER
*******************************************************************************
Start time      : A.D. 2018-Aug-07 07:53:59.2365 TDB
Stop  time      : A.D. 2018-Aug-08 07:53:59.2365 TDB
Step-size       : 1440 minutes
*******************************************************************************
Center geodetic : 0.00000000,0.00000000,0.0000000 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 0.00000000,0.00000000,0.0000000 {E-lon(deg),Dxy(km),Dz(km)}
Center radii    : 696000.0 x 696000.0 x 696000.0 k{Equator, meridian, pole}
Output units    : AU-D
Output type     : GEOMETRIC cartesian states
Output format   : 3 (position, velocity, LT, range, range-rate)
Reference frame : ICRF
*******************************************************************************
JDTDB
   X     Y     Z
   VX    VY    VZ
   LT    RG    RR
*******************************************************************************
$$SOE
2458337.829157830 = A.D. 2018-Aug-07 07:53:59.2365 TDB
 X = 7.101323039968829E-01 Y =-6.636211705364583E-01 Z =-2.882396266749596E-01
 VX= 1.257944923527931E-02 VY= 1.028735601134911E-02 VZ= 4.995535623042180E-03
 LT= 5.855142406578412E-03 RG= 1.013786481242387E+00 RR= 6.571943104235539E-04
2458338.829157830 = A.D. 2018-Aug-08 07:53:59.2365 TDB
 X = 7.228838752596055E-01 Y =-6.530547342937241E-01 Z =-2.830064804389050E-01
 VX= 1.290427841664855E-02 VY= 1.104448197596006E-02 VZ= 5.494559966538393E-03
 LT= 5.859047013408399E-03 RG= 1.014462542957702E+00 RR= 5.526546773311499E-04
$$EOE
*******************************************************************************
Coordinate system description:

  International Celestial Reference Frame (ICRF)

    The ICRF is an adopted reference frame whose axes are defined relative to
    fixed extragalactic radio sources distributed across the sky.

    The ICRF was aligned with the prior FK5/J2000 dynamical system at the ~0.02
    arcsecond level but is not identical and has no associated standard epoch.

  Symbol meaning [1 au= 149597870.700 km, 1 day= 86400.0 s]:

    JDTDB    Julian Day Number, Barycentric Dynamical Time
      X      X-component of position vector (au)
      Y      Y-component of position vector (au)
      Z      Z-component of position vector (au)
      VX     X-component of velocity vector (au/day)
      VY     Y-component of velocity vector (au/day)
      VZ     Z-component of velocity vector (au/day)
      LT     One-way down-leg Newtonian light-time (day)
      RG     Range; distance from coordinate center (au)
      RR     Range-rate; radial velocity wrt coord. center (au/day)

Geometric states/elements have no aberrations applied.


 Computations by ...
     Solar System Dynamics Group, Horizons On-Line Ephemeris System
     4800 Oak Grove Drive, Jet Propulsion Laboratory
     Pasadena, CA  91109   USA
     Information  : https://ssd.jpl.nasa.gov/
     Documentation: https://ssd.jpl.nasa.gov/?horizons_doc
     Connect      : https://ssd.jpl.nasa.gov/?horizons (browser)
                    telnet ssd.jpl.nasa.gov 6775       (command-line)
                    e-mail command interface available
                    Script and CGI interfaces available
     Author       : Jon.D.Giorgini@jpl.nasa.gov
*******************************************************************************
    """
    # ---------------------------------------------------
    
    # Assert that the returned quantities have the expected numerical values
    # -->> We query horizons using tdb=2458337.82915783
    # X = 7.101323039968829E-01 Y =-6.636211705364583E-01 Z =-2.882396266749596E-01
    expectedPosns = np.array([
            [7.101323039968829E-01, -6.636211705364583E-01, -2.882396266749596E-01]
            ] )
    assert np.allclose(S.posns , expectedPosns, rtol=1e-06, atol=1e+02), \
        ' Not close enough to expected values:\n S.posns returned=...\n[%r]\n, expected=...\n[%r]' % (S.posns , expectedPosns)

def test_Satellite_E():
    """Test that a Satellite-object returns the expected positions for multiple jdutc's """
    # Make a Satellite-object
    time    = Time([2458337.829157830, 2458338.829157830], format='jd', scale='tdb')
    obscode = '-95'
    S = wis.Satellite(obscode, time)

    # Assert that the returned quantities have the expected numerical values
    # -->> So we query horizons using tdb   = [2458338.82915783,2458338.82915783]
    #X = 7.101323039968829E-01 Y =-6.636211705364583E-01 Z =-2.882396266749596E-01
    #X = 7.228838752596055E-01 Y =-6.530547342937241E-01 Z =-2.830064804389050E-01
    expectedPosns = np.array([
                              [7.101323039968829E-01, -6.636211705364583E-01, -2.882396266749596E-01],
                              [7.228838752596055E-01, -6.530547342937241E-01, -2.830064804389050E-01]
                              ] )
    assert np.allclose(S.posns , expectedPosns, rtol=1e-06, atol=1e+02), \
        ' Not close enough to expected values:\n S.posns returned=...\n[%r]\n, expected=...\n[%r]' % (S.posns , expectedPosns)



def test_Satellite_F():
    """Test that the position of K2 is as expected """
    # Make a Satellite-object
    time    = Time([2458337.829157830 , 2458338.829157830], format='jd', scale='tdb')
    obscode = '-227'
    S = wis.Satellite(obscode, time)

    # *** DATA FROM EXPLICIT HORIZONS QUERY -------------
    """
*******************************************************************************
Ephemeris / WWW_USER Tue Jan 26 10:10:35 2021 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: Kepler (spacecraft) (-227)      {source: KEPLER_FINAL_56_traj}
Center body name: Sun (10)                        {source: DE431mx}
Center-site name: BODY CENTER
*******************************************************************************
Start time      : A.D. 2018-Aug-07 07:53:59.2365 TDB
Stop  time      : A.D. 2018-Aug-08 07:53:59.2365 TDB
Step-size       : 1440 minutes
*******************************************************************************
Center geodetic : 0.00000000,0.00000000,0.0000000 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 0.00000000,0.00000000,0.0000000 {E-lon(deg),Dxy(km),Dz(km)}
Center radii    : 696000.0 x 696000.0 x 696000.0 k{Equator, meridian, pole}
Output units    : AU-D
Output type     : GEOMETRIC cartesian states
Output format   : 3 (position, velocity, LT, range, range-rate)
Reference frame : ICRF
*******************************************************************************
JDTDB
   X     Y     Z
   VX    VY    VZ
   LT    RG    RR
*******************************************************************************
$$SOE
2458337.829157830 = A.D. 2018-Aug-07 07:53:59.2365 TDB
 X =-3.247439631457193E-01 Y =-9.176995632113913E-01 Z =-3.890277674336675E-01
 VX= 1.564193719517850E-02 VY=-4.835645979156440E-03 VZ=-2.114261529378122E-03
 LT= 6.054588378363500E-03 RG= 1.048319480765473E+00 RR= 1.722299096179222E-04
2458338.829157830 = A.D. 2018-Aug-08 07:53:59.2365 TDB
 X =-3.090609977353972E-01 Y =-9.224171671345395E-01 Z =-3.910919864336775E-01
 VX= 1.572331588778283E-02 VY=-4.599378850291082E-03 VZ=-2.014096133749677E-03
 LT= 6.055556118004938E-03 RG= 1.048487039690214E+00 RR= 1.628815283630382E-04
$$EOE
*******************************************************************************
Coordinate system description:

  International Celestial Reference Frame (ICRF)

    The ICRF is an adopted reference frame whose axes are defined relative to
    fixed extragalactic radio sources distributed across the sky.

    The ICRF was aligned with the prior FK5/J2000 dynamical system at the ~0.02
    arcsecond level but is not identical and has no associated standard epoch.

  Symbol meaning [1 au= 149597870.700 km, 1 day= 86400.0 s]:

    JDTDB    Julian Day Number, Barycentric Dynamical Time
      X      X-component of position vector (au)
      Y      Y-component of position vector (au)
      Z      Z-component of position vector (au)
      VX     X-component of velocity vector (au/day)
      VY     Y-component of velocity vector (au/day)
      VZ     Z-component of velocity vector (au/day)
      LT     One-way down-leg Newtonian light-time (day)
      RG     Range; distance from coordinate center (au)
      RR     Range-rate; radial velocity wrt coord. center (au/day)

Geometric states/elements have no aberrations applied.


 Computations by ...
     Solar System Dynamics Group, Horizons On-Line Ephemeris System
     4800 Oak Grove Drive, Jet Propulsion Laboratory
     Pasadena, CA  91109   USA
     Information  : https://ssd.jpl.nasa.gov/
     Documentation: https://ssd.jpl.nasa.gov/?horizons_doc
     Connect      : https://ssd.jpl.nasa.gov/?horizons (browser)
                    telnet ssd.jpl.nasa.gov 6775       (command-line)
                    e-mail command interface available
                    Script and CGI interfaces available
     Author       : Jon.D.Giorgini@jpl.nasa.gov
*******************************************************************************
    """

    # Assert that the returned quantities have the expected numerical values
    #X =-3.247439631457193E-01 Y =-9.176995632113913E-01 Z =-3.890277674336675E-01
    #X =-3.090609977353972E-01 Y =-9.224171671345395E-01 Z =-3.910919864336775E-01
    # -->> So we query horizons using tdb   = [2458338.82915783,2458338.82915783]
    expectedPosns = np.array([
                              [-3.247439631457193E-01, -9.176995632113913E-01, -3.890277674336675E-01],
                              [-3.090609977353972E-01, -9.224171671345395E-01, -3.910919864336775E-01]
                              ] )
    assert np.allclose(S.posns , expectedPosns, rtol=1e-06, atol=1e+02), \
        ' Not close enough to expected values: returned=[%r], expected=[%r]' % (S.posns , expectedPosns)

'''

def test_Satellite_G():
    """ Test that the position of CASSINI is as expected """
    """ Here I am repeating some of the numbers/tests from ... """
    """ ... https://spiceypy.readthedocs.io/en/master/exampleone.html """

    # Input dates ...
    time    = Time([2453176.5], format='jd', scale='utc')
    et    = sp.str2et('JD'+str(time.utc.jd[0]) )
    assert np.allclose(et, 140961664.18440723), 'time transformation inaccurate: [%r]' % et0

    # Make a Satellite-object (implicitly calculates positions):
    # - *** NOTE THE USE OF A DIFFERENT BARYCENTER & A DIFFERENT FRAME (NOT ECLIPTIC)***
    obscode ='-82'
    S = wis.Satellite(obscode, time, center='SATURN BARYCENTER', frame = "J2000")

    # Expected posnitions & ltts :
    # positions, lightTimes = spice.spkpos('Cassini', times, 'J2000', 'NONE', 'SATURN BARYCENTER')
    expectedPositions   = [-5461446.61080924, -4434793.40785864, -1200385.93315424]
    expectedLTT         = 23.8062238783
    

    # Assert calculated is close to expected ...
    assert np.allclose(S.posns , expectedPositions, rtol=1e-05, atol=1e+02), \
        ' Not close enough to expected values: returned=[%r], expected=[%r]' % (S.posns , expectedPositions)
    assert np.allclose(S.ltts  , expectedLTT, rtol=1e-05, atol=1e+02), \
    ' Not close enough to expected values: returned=[%r], expected=[%r]' % (S.ltts , expectedLTT)


'''


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


