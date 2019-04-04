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

# -----------------------------------------
# Local imports
# -----------------------------------------
from .kernels import Manager
from .satellite_obscodes import obscodeDict, Instructions

# -----------------------------------------
# WIS functions & classes
# -----------------------------------------

class Satellite(object):
    """
        Object to manage the calculation of satellite locations.
        
        Parameters
        ----------
        obscode : MPC observation code
            3 or 4 character string
        jdutc   : float
            Julian date (assumed to be UTC)
            Expected to be of the form 2458337.8283571
        center  : coordinate center
            ...
       
        Attributes
        ----------
        ??? : ???
            ???

        Notes
        -----

        """
    
    def __init__(self, obscode, jdutc, center="SUN", frame = "ECLIPJ2000", abcorr = "NONE"):
        """
            Initialize the Satellite object
            Does formatting-checks on the supplied variables
            
            Uses "Kernel" to manage loading of required spice-kernels
            
            Calls get_posns() to evaluate the satellite position(s)
        
            Parameters
            ----------
            obscode : MPC observation code
                3 or 4 character string
            jdutc   : float
                Julian date (assumed to be UTC)
                Expected to be of the form 2458337.8283571
            center  : coordinate center
                ...
            
        """
        

        # Assert that the inputs are formatted correctly
        # -----------------------------------------------
        self.obscode, self.jdutc, self.center = self._check_input_formats(obscode, jdutc, center)

        # Try to load the spiceypy kernels
        # -----------------------------------------------
        K = Manager(obscode=self.obscode)

        # Convert the supplied jdutc to the required format for spiceypy
        # -----------------------------------------------
        self.epochs = np.array([sp.utc2et('JD'+str(jdutc)) for jdutc in self.jdutc])
        
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
            
            Not used in default init
            ----------
            
        """
        states, ltts = [],[]
        for epoch in epochs:
            state, ltt = sp.spkpos(obscode, epoch, frame ,abcorr, center )
            states.append(state)
            ltts.append(ltt)
        return np.array(states), np.array(ltts)


    def _check_input_formats(self, obscode, jdutc, center):
        """
            Assert that the inputs are formatted correctly
            
            Parameters
            ----------
            obscode : MPC observation code
                3 or 4 character string
            jdutc   : float
                Julian date (assumed to be UTC)
                Expected to be of the form 2458337.8283571
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
        assert obscode in obscodeDict, 'Supplied obscode [%r] is not in known/allowed codes [%r] from file.' % (obscode,list(obscodeDict.keys()) )
        
        # Assert supplied jdutc is likely to be of the form "2458337.8283571"
        # -----------------------------------------------
        jdutc = np.atleast_1d(jdutc)
        # Are the inputs floats ?
        assert np.all( [isinstance(j, float) for j in jdutc ]), ' Supplied jdutc [%r] not a float ' % jdutc
        # Double-checking that there is a decimal point in there
        assert np.all( [ "." in str(j)       for j in jdutc ]), ' Supplied jdutc [%r] does not contain a "." ' % jdutc
        # Check that there are 7 digits to the left of the decimal-point so that we are somewhere in the correct era
        assert np.all( [len(str(j)[:str(j).find('.')]) in [7] for j in jdutc ]), ' Supplied jdutc [%r] has insufficient digits ' % jdutc

        return obscode, jdutc, center
