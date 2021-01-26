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



def test_Ground_A():
    """
    Test observatory position calculation against Horizons (km)
    """
    
    # *** DATA FROM EXPLICIT HORIZONS QUERY -------------
    """
*******************************************************************************
Ephemeris / WWW_USER Tue Jan 26 11:12:25 2021 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: Earth (399)                     {source: DE431mx}
Center body name: Earth (399)                     {source: DE431mx}
Center-site name: Pan-STARRS 1, Haleakala
*******************************************************************************
Start time      : A.D. 2000-Jan-01 12:01:04.1839 TDB
Stop  time      : A.D. 2000-Jan-02 12:01:04.1839 TDB
Step-size       : 0 steps
*******************************************************************************
Center geodetic : 203.744100,20.7071888,3.0763821 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 203.744100,5971.48324,2242.1878 {E-lon(deg),Dxy(km),Dz(km)}
Center pole/equ : High-precision EOP model        {East-longitude positive}
Center radii    : 6378.1 x 6378.1 x 6356.8 km     {Equator, meridian, pole}
Output units    : KM-S
Output type     : GEOMETRIC cartesian states
Output format   : 3 (position, velocity, LT, range, range-rate)
EOP file        : eop.210125.p210418
EOP coverage    : DATA-BASED 1962-JAN-20 TO 2021-JAN-25. PREDICTS-> 2021-APR-17
Reference frame : ICRF
*******************************************************************************
JDTDB
   X     Y     Z
   VX    VY    VZ
   LT    RG    RR
*******************************************************************************
$$SOE
2451545.000742869 = A.D. 2000-Jan-01 12:01:04.1839 TDB [del_T=     64.183904 s]
 X = 3.357062612610595E+03 Y =-4.938472797753120E+03 Z =-2.242238952821062E+03
 VX= 3.601236917337654E-01 VY= 2.447964660859150E-01 VZ= 1.654269866964587E-05
 LT= 2.127658354697273E-02 RG= 6.378559279389312E+03 RR=-4.126854789751626E-17
2451546.000742869 = A.D. 2000-Jan-02 12:01:04.1839 TDB [del_T=     64.183933 s]
 X = 3.441514318240966E+03 Y =-4.879997205156549E+03 Z =-2.242236596724388E+03
 VX= 3.558595984886408E-01 VY= 2.509548321430072E-01 VZ= 1.651208609599962E-05
 LT= 2.127658354697273E-02 RG= 6.378559279389311E+03 RR= 8.360100975126858E-18
$$EOE
*******************************************************************************
Coordinate system description:

  International Celestial Reference Frame (ICRF)

    The ICRF is an adopted reference frame whose axes are defined relative to
    fixed extragalactic radio sources distributed across the sky.

    The ICRF was aligned with the prior FK5/J2000 dynamical system at the ~0.02
    arcsecond level but is not identical and has no associated standard epoch.

  Symbol meaning:

    JDTDB    Julian Day Number, Barycentric Dynamical Time
    del_T    Time-scale conversion difference TDB - UT (s)
      X      X-component of position vector (km)
      Y      Y-component of position vector (km)
      Z      Z-component of position vector (km)
      VX     X-component of velocity vector (km/sec)
      VY     Y-component of velocity vector (km/sec)
      VZ     Z-component of velocity vector (km/sec)
      LT     One-way down-leg Newtonian light-time (sec)
      RG     Range; distance from coordinate center (km)
      RR     Range-rate; radial velocity wrt coord. center (km/sec)

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
    # Time & Obscode of interest
    time    = Time([2451545.000742869, 2451546.000742869], format='jd', scale='tdb')
    obscode = 'F51'
    
    # Call wis.wis
    W = wis.wis(obscode, time)
    
    # Because we input a *SATELLITE* obs-code, we expect to get back a Satellite-Class object
    assert isinstance(W, wis.Ground )

    # Assert that the returned quantities have the expected numerical values
    # NB The above query is from F51 to Sun, rather than Sun to F51 (limitations of Horizons query)
    # - Hence MINUS SIGN IN FRONT OF EXPECTED POSITIONS ARRAY
    #X = 3.357062612610595E+03 Y =-4.938472797753120E+03 Z =-2.242238952821062E+03
    #X = 3.441514318240966E+03 Y =-4.879997205156549E+03 Z =-2.242236596724388E+03
    expectedPosns = -1.0 * np.array([
                              [3.357062612610595E+03 , -4.938472797753120E+03 , -2.242238952821062E+03],
                              [3.441514318240966E+03 , -4.879997205156549E+03 , -2.242236596724388E+03]
                              ] )
    assert np.allclose(W.obs_vec_rot , expectedPosns, rtol=1e-06, atol=1e+02), \
        ' Not close enough to expected values: returned=[%r], expected=[%r]' % (W.obs_vec_rot , expectedPosns)





def test_Ground_B():
    """
    Test geocenter position calculation against Horizons (AU)
    """
    
    # *** DATA FROM EXPLICIT HORIZONS QUERY -------------
    """
*******************************************************************************
Ephemeris / WWW_USER Tue Jan 26 11:23:52 2021 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: Earth (399)                     {source: DE431mx}
Center body name: Earth (399)                     {source: DE431mx}
Center-site name: Pan-STARRS 1, Haleakala
*******************************************************************************
Start time      : A.D. 2000-Jan-01 12:01:04.1839 TDB
Stop  time      : A.D. 2000-Jan-02 12:01:04.1839 TDB
Step-size       : 0 steps
*******************************************************************************
Center geodetic : 203.744100,20.7071888,3.0763821 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 203.744100,5971.48324,2242.1878 {E-lon(deg),Dxy(km),Dz(km)}
Center pole/equ : High-precision EOP model        {East-longitude positive}
Center radii    : 6378.1 x 6378.1 x 6356.8 km     {Equator, meridian, pole}
Output units    : AU-D
Output type     : GEOMETRIC cartesian states
Output format   : 3 (position, velocity, LT, range, range-rate)
EOP file        : eop.210125.p210418
EOP coverage    : DATA-BASED 1962-JAN-20 TO 2021-JAN-25. PREDICTS-> 2021-APR-17
Reference frame : ICRF
*******************************************************************************
JDTDB
   X     Y     Z
   VX    VY    VZ
   LT    RG    RR
*******************************************************************************
$$SOE
2451545.000742869 = A.D. 2000-Jan-01 12:01:04.1839 TDB [del_T=     64.183904 s]
 X = 2.244057750890565E-05 Y =-3.301165166753353E-05 Z =-1.498844162907635E-05
 VX= 2.079888358049827E-04 VY= 1.413817895325368E-04 VZ= 9.554207946740535E-09
 LT= 2.462567540158880E-07 RG= 4.263803521763170E-05 RR=-1.238731504259479E-20
2451546.000742869 = A.D. 2000-Jan-02 12:01:04.1839 TDB [del_T=     64.183933 s]
 X = 2.300510229281603E-05 Y =-3.262076647429548E-05 Z =-1.498842587954287E-05
 VX= 2.055261158835369E-04 VY= 1.449385435481056E-04 VZ= 9.536527706034836E-09
 LT= 2.462567540158880E-07 RG= 4.263803521763169E-05 RR=-8.937480661616926E-21
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
    del_T    Time-scale conversion difference TDB - UT (s)
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
    # Time & Obscode of interest
    time    = Time([2451545.000742869, 2451546.000742869], format='jd', scale='tdb')
    obscode = 'F51'
    
    # Call wis.wis
    W = wis.wis(obscode, time)
    
    # Because we input a *SATELLITE* obs-code, we expect to get back a Satellite-Class object
    assert isinstance(W, wis.Ground )

    # Assert that the returned quantities have the expected numerical values
    #X = 2.244057750890565E-05 Y =-3.301165166753353E-05 Z =-1.498844162907635E-05
    #X = 2.300510229281603E-05 Y =-3.262076647429548E-05 Z =-1.498842587954287E-05
    expectedPosns = -1.0 * np.array([
                              [2.244057750890565E-05,-3.301165166753353E-05 , -1.498844162907635E-05],
                              [2.300510229281603E-05 , -3.262076647429548E-05 , -1.498842587954287E-05]
                              ] )
    assert np.allclose(W.obs_vec_rot_AU , expectedPosns, rtol=1e-06, atol=1e+02), \
        ' Not close enough to expected values: returned=[%r], expected=[%r]' % (W.obs_vec_rot_AU , expectedPosns)






def test_Ground_C():
    """
    Test the overall heliocentric position of the observatory
    """
    
    # *** DATA FROM EXPLICIT HORIZONS QUERY -------------
    """
*******************************************************************************
Ephemeris / WWW_USER Tue Jan 26 11:29:34 2021 Pasadena, USA      / Horizons
*******************************************************************************
Target body name: Sun (10)                        {source: DE431mx}
Center body name: Earth (399)                     {source: DE431mx}
Center-site name: Pan-STARRS 1, Haleakala
*******************************************************************************
Start time      : A.D. 2000-Jan-01 12:01:04.1839 TDB
Stop  time      : A.D. 2000-Jan-02 12:01:04.1839 TDB
Step-size       : 0 steps
*******************************************************************************
Center geodetic : 203.744100,20.7071888,3.0763821 {E-lon(deg),Lat(deg),Alt(km)}
Center cylindric: 203.744100,5971.48324,2242.1878 {E-lon(deg),Dxy(km),Dz(km)}
Center pole/equ : High-precision EOP model        {East-longitude positive}
Center radii    : 6378.1 x 6378.1 x 6356.8 km     {Equator, meridian, pole}
Output units    : AU-D
Output type     : GEOMETRIC cartesian states
Output format   : 3 (position, velocity, LT, range, range-rate)
EOP file        : eop.210125.p210418
EOP coverage    : DATA-BASED 1962-JAN-20 TO 2021-JAN-25. PREDICTS-> 2021-APR-17
Reference frame : ICRF
*******************************************************************************
JDTDB
   X     Y     Z
   VX    VY    VZ
   LT    RG    RR
*******************************************************************************
$$SOE
2451545.000742869 = A.D. 2000-Jan-01 12:01:04.1839 TDB [del_T=     64.183904 s]
 X = 1.771703233769980E-01 Y =-8.874593810516950E-01 Z =-3.847569536828423E-01
 VX= 1.741557375812744E-02 VY= 3.039755432093662E-03 VZ= 1.256493770641990E-03
 LT= 5.679456288207732E-03 RG= 9.833673728111324E-01 RR=-9.719801362883684E-05
2451546.000742869 = A.D. 2000-Jan-02 12:01:04.1839 TDB [del_T=     64.183933 s]
 X = 1.943505199554981E-01 Y =-8.844221447467095E-01 Z =-3.834405079856051E-01
 VX= 1.735627288621994E-02 VY= 3.320127567567683E-03 VZ= 1.376362758488653E-03
 LT= 5.679426593146453E-03 RG= 9.833622312706550E-01 RR=-9.248567476947815E-05
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
    del_T    Time-scale conversion difference TDB - UT (s)
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
    # Time & Obscode of interest
    time    = Time([2451545.000742869, 2451546.000742869], format='jd', scale='tdb')
    obscode = 'F51'
    
    # Call wis.wis
    W = wis.wis(obscode, time)
    
    # Because we input a *SATELLITE* obs-code, we expect to get back a Satellite-Class object
    assert isinstance(W, wis.Ground )

    # Assert that the returned quantities have the expected numerical values
    # NB The above query is from F51 to Sun, rather than Sun to F51 (limitations of Horizons query)
    # - Hence MINUS SIGN IN FRONT OF EXPECTED POSITIONS ARRAY
    #X = 1.771703233769980E-01 Y =-8.874593810516950E-01 Z =-3.847569536828423E-01
    #X = 1.943505199554981E-01 Y =-8.844221447467095E-01 Z =-3.834405079856051E-01
    expectedPosns = -1.0 * np.array([
                              [1.771703233769980E-01 ,-8.874593810516950E-01 ,-3.847569536828423E-01],
                              [1.943505199554981E-01 ,-8.844221447467095E-01 ,-3.834405079856051E-01]
                              ] )
    assert np.allclose(W.posns , expectedPosns, rtol=1e-06, atol=1e+02), \
        ' Not close enough to expected values: returned=[%r], expected=[%r]' % (W.hXYZ , expectedPosns)





