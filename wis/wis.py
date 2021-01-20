"""
    Main wis.py module.
    WIS ~ Where Is Satellite
        ~ Where Is Satellite-spice-kernel
    
    wis.py tells you where a satellite is
    wis.py uses JPL spice kernels, so you need spicypy
    wis.py goes and gets the spice-kernels if you don't have them
    
    wis.py is essentially a means to automate the retrieval of
    useful spice-kernels. All of the positional calculations
    are handled using spice/spiceypy
    
    wis.py is very light & wispy ...
    
    wis.py doesn't know about all satellites.
    So far it only knows about:
    - TESS
    - K2
    
"""

# -----------------------------------------
# Third-party imports
# -----------------------------------------
import spiceypy as sp
import numpy as np
from astropy.time import Time

# -----------------------------------------
# Local imports
# -----------------------------------------
#try:
#    from .kernels import Manager
#    from .satellite_obscodes import obscodeDict
#except:
from kernels            import KernelLoader
from satellite_obscodes import satellite_obscode_dict
from ground_obscodes    import ground_obscode_dict
from excluded_obscodes  import excluded_obscode_dict

# -----------------------------------------
# WIS functions & classes
# -----------------------------------------


def wis(obscode, times,  center="SUN", frame = "ECLIPJ2000", abcorr = "NONE", EXCLUDE_AS_GEO = False, UNKNOWN_AS_GEO = False):
    """
    WIP Code to generalize from Satellite Obs-Codes to *Any* Obs-Code
    
    NB, the input variables could do with having more user-friendly names
    """
    
        
    # If the obscode is a satellite one that we can work with, return Satellite class
    if obscode in satellite_obscode_dict:
        return Satellite(obscode, times,  center=center, frame=frame,abcorr =abcorr)
    
    # If the obscode is a ground-based site that we can work with, return Ground class
    elif obscode in ground_obscode_dict:
        return Ground(obscode, times,  center=center, frame=frame,abcorr =abcorr)
    
    # Allow for the possibility of treating some obs-codes differently
    # (I am thinking of roving code 247)
    elif obscode in excluded_obscode_dict:
        print('That obscode is listed as being one that wis.py should specifically exclude')
        if EXCLUDE_AS_GEO:
            print('Proceeding as if from the geocenter')
            return Ground('500', times,  center=center, frame=frame,abcorr =abcorr)
        else:
            return None

    # Catch unknown obscodes
    else:
        print('That obscode is unknown by wis.py')
        if UNKNOWN_AS_GEO:
            print('Proceeding as if from the geocenter')
            return Ground('500', times,  center=center, frame=frame,abcorr =abcorr)
        else:
            return None


class Satellite(object):
    """
        Object to manage the calculation of satellite locations.
        
        Parameters
        ----------
        obscode : MPC observation code
            3 or 4 character string
        times   : astropy Time object
            http://docs.astropy.org/en/stable/time/
        center  : coordinate center
            ...
       
        Attributes
        ----------
        ??? : ???
            ???

        Notes
        -----

        """
    
    def __init__(self, obscode, times,  center="SUN", frame = "ECLIPJ2000", abcorr = "NONE"):
        """
            Initialize the Satellite object
            
            Does formatting-checks on the supplied variables
            
            Uses "Kernel" to manage loading of required spice-kernels
            
            Calls get_posns() to evaluate the satellite position(s)
        
            Parameters
            ----------
            obscode : MPC observation code
                3 or 4 character string
            times   : astropy Time object
                http://docs.astropy.org/en/stable/time/
            center  : coordinate center
                ...
            
        """
        

        # Assert that the inputs are formatted correctly
        # -----------------------------------------------
        self.obscode, self.time, self.center = self._check_input_formats(obscode, times, center)

        # Try to load the spiceypy kernels
        # NB: We are passing in an obscode-specific-KernelDownloader from the dicts
        # -----------------------------------------------
        K = KernelLoader( satellite_obscode_dict[self.obscode] )

        # Convert the supplied time to the required format for spiceypy
        # -----------------------------------------------
        self.epochs = np.array([sp.utc2et('JD'+str(jdutc)) for jdutc in self.time.utc.jd])
        
        # Evaluate the position of the satellite using the loaded kernels
        # -----------------------------------------------
        posns, ltts = sp.spkpos(obscode, self.epochs, frame ,abcorr, center )
        self.posns, self.ltts = np.asarray(posns), np.asarray(ltts)



    def states(self, obscode, epochs, center , frame = "ECLIPJ2000", abcorr = "NONE" ):
        """
            Evaluate the entire (6D) state of the satellite at epochs
            Uses spkezr()
            Uses loaded spice-kernels
            
            Parameters
            ----------
            obscode : MPC observation code
                3 or 4 character string
            epochs : array of epochs
                as returned by the spiceypy utc2et() function
            center : Observing body name.
                type obs: str
            frame: Reference frame of output state vector.
                type ref: str
            abcorr: Aberration correction flag.
                type abcorr: str
            
            Returns
            ----------
            posns: positions of satellite
                6xN vector of XYZ in [km]
            ltts: light travel times
                1xN vector of one way light time between observer and target in [s]
            
            *** Not used in default init ***
            ----------
            
        """
        states, ltts = [],[]
        for epoch in epochs:
            state, ltt = sp.spkpos(obscode, epoch, frame ,abcorr, center )
            states.append(state)
            ltts.append(ltt)
        return np.array(states), np.array(ltts)


    def _check_input_formats(self, obscode, time, center):
        """
            Assert that the inputs are formatted correctly
            
            Parameters
            ----------
            obscode : MPC observation code
                3 or 4 character string
            time   : astropy Time object
                http://docs.astropy.org/en/stable/time/
            center  : coordinate center
                ...
            
            Returns
            ----------
            obscode, jdutc, center
            
            
        """

        # Assert that the obscode is formatted correctly
        # -----------------------------------------------
        assert isinstance(obscode, str), 'Supplied obscode [%r] is not a string' % obscode
        assert len(obscode) in [3,4], 'Supplied obscode [%r] is not of length 3 or 4 ' % obscode
            
        # Assert that the obscode is one that we know how to handle
        # -----------------------------------------------
        assert obscode in satellite_obscode_dict, 'Supplied obscode [%r] is not in known/allowed codes [%r] from file.' % (obscode,list(satellite_obscode_dict.keys()) )
        
        # Assert supplied time is of the correct format
        # -----------------------------------------------
        assert isinstance(time , Time )
        time = time.utc

        return obscode, time, center





class Ground(object):
    """
        Object to manage the calculation of ground-based station locations.
    
    """
    
    def __init__(self, obscode, times,  center="SUN", frame = "ECLIPJ2000", abcorr = "NONE"):
        """ May want/need to change the variables later"""

        # For now I am just initializing these variables to make them comparable to the Satellite class.
        self.obscode, self.time, self.center = None, None, None
        self.epochs = None
        self.posns, self.ltts = None, None

