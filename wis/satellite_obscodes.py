"""
    This file constructs a dictionary of all of the station-codes/obs-codes
    of artificial satellites for which wis.py knows how to get spice-kernels
    
    The data for each obs-code is specified in a "KernelDownloader" object
    
    Each KernelDownloader-Object is saved into an overall
    obscodeDict
     - The keys defines the set of obscodes that the user can expect to return sensible results
     - The values defines the KernelDownloader-Object that the user can use to download kernels

"""
# -----------------------------------------
# Third-party imports
# -----------------------------------------
# None

# -----------------------------------------
# Local imports
# -----------------------------------------
from kernels import KernelDownloader

# -----------------------------------------
# WIS functions & classes
# -----------------------------------------

# Define the location of the kernels to download for TESS
# NB: This list was created in 2019, so likely out-of-date
# --------------------------------------------------------------------------
TESS = KernelDownloader()
TESS.obscode        = '-95'
TESS.name           = 'TESS'
TESS.files          = ['https://archive.stsci.edu/missions/tess/models/tess2018338154046-41240_naif0012.tls',
                       'https://archive.stsci.edu/missions/tess/models/tess2018338154429-41241_de430.bsp']
TESS.wildcards      = {'https://archive.stsci.edu/missions/tess/models/':'TESS_EPH_DEF*'}

                       
# Define the location of the kernels to download for K2
# NB: This list was created in 2019, so likely out-of-date
# --------------------------------------------------------------------------
K2 = KernelDownloader()
K2.obscode          = '-227'
K2.name             = 'K2'
K2.files            = ['https://archive.stsci.edu/pub/k2/spice/kplr2018134232543.tsc',
                       'https://archive.stsci.edu/pub/k2/spice/naif0012.tls',
                       'https://archive.stsci.edu/pub/k2/spice/spk_2018290000000_2018306220633_kplr.bsp']
K2.wildcards        = {}


# Define the location of the kernels to download for CASSINI
# --------------------------------------------------------------------------
CASSINI = KernelDownloader()
CASSINI.obscode          = '-82'
CASSINI.name             = 'CASSINI'
CASSINI.files            = ['https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/a_old_versions/naif0009.tls',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/sclk/cas00084.tsc',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/pck/cpck05Mar2004.tpc',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/fk/release.11/cas_v37.tf',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/ck/04135_04171pc_psiv2.bc',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/030201AP_SK_SM546_T45.bsp',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/ik/release.11/cas_iss_v09.ti',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/020514_SE_SAT105.bsp',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/981005_PLTEPH-DE405S.bsp']
CASSINI.wildcards        = {}



# Define a handy dictionary containing all of the defined Instruction-Objects
# --------------------------------------------------------------------------
satellite_obscode_dict = {KD.obscode:KD for KD in [TESS, K2, CASSINI]}

