# -----------------------------------------
# Third party imports
# -----------------------------------------
import os, sys
import numpy as np

# -----------------------------------------
# Local imports
# -----------------------------------------
from kernels import KernelSpecifier

# Define a handy dictionary containing all of the ground-based obscodes we are
# currently set-up to handle in wis.py
# --------------------------------------------------------------------------
def parseObsCode( line):
    """
        Parses a line from the MPC's ObsCode.txt file
        Eventually we want to be getting this from db/API
    """
    code, longitude, rhocos, rhosin, ObsName = line[0:3], line[4:13], line[13:21], line[21:30], line[30:].rstrip('\n')
    if longitude.isspace():
        longitude = None
    if rhocos.isspace():
        rhocos = None
    if rhosin.isspace():
        rhosin = None
    return code, longitude, rhocos, rhosin, ObsName
    
def get_XYZ_for_all_obscodes( filepath = os.path.join(os.path.dirname(__file__), 'obscode.dat') , GROUND_ONLY = True):
    """
    XYZ posns of all observatories w.r.t. the geocenter
    Eventually we want to be getting this from db/API
    """
    ObservatoryXYZ = {}
    with open(filepath, 'r') as f:
        next(f)
        for line in f:
            code, longitude, rhocos, rhosin, Obsname = parseObsCode(line)

            # Ignore space/roving stuff if GROUND_ONLY == True
            if GROUND_ONLY and "--" in Obsname[-3:] :
                pass
            else:
                if longitude and rhocos and rhosin:
                    rhocos, rhosin, longitude = float(rhocos), float(rhosin), float(longitude)
                    longitude *= np.pi/180.

                    x = rhocos*np.cos(longitude)
                    y = rhocos*np.sin(longitude)
                    z = rhosin
                    ObservatoryXYZ[code]=np.array([x,y,z])
                #else:
                #    ObservatoryXYZ[code]=(None,None,None)

    return ObservatoryXYZ



ground_obscode_dict = get_XYZ_for_all_obscodes(GROUND_ONLY = True)


# Set-up a single downloader to cope with all ground-based obscodes
"""
Notes from Davide ...
For the Earth orientation kernels, see here: https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/

- earth_720101_070426.bpc: reconstruction through 2007
- earth_latest_high_prec.bpc: latest high-precision reconstruction (I suggest getting it daily)
- earth_200101_990628_predict.bpc: future predicts

The readme file contains more details.
With these kernels you can the frame conversion between equatorial J2000 and body-fixed (ITRF93) using pxform: https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/spicelib/pxform.html

Note that the order in which you load kernels matters, later takes precedence for competing data: https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/kernel.html#Kernel%20Priority
Predicts should go first and reconstructions later.
"""
# --------------------------------------------------------------------------
GRND = KernelSpecifier(
    obscode        = 'GROUND',
    name           = 'GROUND',
    files           = ['https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp',
                        'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls',
                        'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_200101_990628_predict.bpc',
                        'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00010.tpc',
                        'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc'],
    wildcards      = {},
    timecritical   = [ 'https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/earth_latest_high_prec.bpc' ]
    )



