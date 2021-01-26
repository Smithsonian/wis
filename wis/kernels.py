"""
    Functions and Objects used by WIS to download
    data (spice-kernels) for station-codes.
    
    These will typically be for satellite missions
"""
# -----------------------------------------
# Third-party imports
# -----------------------------------------
from bs4 import BeautifulSoup
import requests
import glob
import wget
import numpy as np
import os
import sys
import spiceypy as sp
import warnings
import time

# -----------------------------------------
# Local imports
# -----------------------------------------
# None

# -----------------------------------------
# WIS functions & classes
# -----------------------------------------

class KernelSpecifier(object):
    """
        KernelSpecifier-Object
        
        Holds the specification of where data is online for a given satellite
        
        Provides method to download the data to local machine
        
        *** IT IS RARE THAT THE USER WILL HAVE TO DEFINE OR DECLARE A KernelSpecifier     ***
        *** They will only be defined when providing a new set of kernels for a satellite ***
        
    """
    
    def __init__(self, obscode = None, name = None, files = [] , wildcards = [] , timecritical = [] ):
        
        # Check inputs are as desired
        assert obscode is not None and name is not None and files
        
        # Instantiate class variables from inputs
        self.obscode , self.name, self.files, self.wildcards, self.timecritical = \
            obscode, name, files, wildcards, timecritical
            
        # Define a list of expected local filepaths
        self.expected_local_kernel_filepaths = self.get_expected_local_kernel_filepaths()
        

    # Data directories / filepaths
    # ----------------------------------------------
    def get_expected_local_kernel_filepaths(self, ):
        destinationDirectory = self.define_download_subdir()

        # get the file names from the urls in the .files variable
        expected_filepaths = [ os.path.join( destinationDirectory, _.split('/')[-1] ) for _ in self.files ]

        # if there are any wildcards, get those names too
        for url,wildcard in self.wildcards.items():
            for f in self._listFD(url, wildcard = wildcard):
                expected_filepaths.append( os.path.join( destinationDirectory, f.split('/')[-1] ) )
        
        # return
        return expected_filepaths
        
    
    def define_download_dir(self):
        """
        Returns the default path to the directory where files will be saved
        or loaded.

        By default, this method will return "~/.wispykernels" and create
        this directory if it does not exist.
        
        If the directory cannot be accessed or created, then it returns the local directory (".").
        
        N.B. Code "borrowed" from eleanor/targetData.py

        Returns
        -------
        download_dir : str
            Path to location of `download_dir` where kernels will be downloaded
        """
        download_dir = os.path.join(os.path.expanduser('~'), '.wispykernels')
        if os.path.isdir(download_dir):
            return download_dir
        else:
            # if it doesn't exist, make a new cache directory
            try:
                os.mkdir(download_dir)
            # downloads locally if OS error occurs
            except OSError:
                download_dir = '.'
                warnings.warn('Warning: unable to create {}. '
                              'Downloading TPFs to the current '
                              'working directory instead.'.format(download_dir))

        return download_dir

    def define_download_subdir(self, ):
        """
            Returns the default path to the subdirectory where files will be saved
            or loaded for a specific satellite obscode
            
            Uses define_download_dir() to get its parent directly
            
            Returns
            -------
            download_subdir : str
                Path to location of `download_subdir` where kernels will be downloaded
                
        """
        
        # Manage sub-directory for obscode downloads
        # Ground-based stuff stored at the top-level, satellites get their own sub-dir
        if self.name == 'GROUND':
            download_subdir = self.define_download_dir()
        else:
            download_subdir = os.path.join( self.define_download_dir(), self.obscode)

        # define a sub-dir path for this obscode
        if not os.path.isdir( download_subdir ):
            os.mkdir( download_subdir )
            
        return download_subdir


    # Download methods
    # ----------------------------------------------
    def download_data(self,):
        
        # Download explicitly named files
        for f in self.files:
            print('downloading ...',f)
            try:
                wget.download(f, out=self.define_download_subdir() )
            except:
                print("Failed to download %r" % f)
                    
        # Download files using wildcards
        for url,wildcard in self.wildcards.items():
            for f in self._listFD(url, wildcard = wildcard):
                wget.download(f, out=self.define_download_subdir() )
    
        # Check whether the download worked
        if self.kernels_have_been_downloaded():
            return True
        else:
            sys.exit('download unsuccessful ... ')
            

    def kernels_have_been_downloaded(self,):
        """ Check whether all expected kernel files have been downloaded """
        
        # Check what files exist locally
        # -----------------------------------------------
        downloadedKernelFiles = [ f for f in glob.glob("%s/*" % self.define_download_subdir() ) if os.path.isfile(f) ]
        
        # Compare against the files that *should* exist
        # returns True if all expected files have been downloaded
        # -----------------------------------------------
        return np.all( [ f in downloadedKernelFiles for f in self.expected_local_kernel_filepaths ] )
            


    def _listFD(self , url, wildcard=''):
        '''
            List all the files in a url
            Allows a wildcard of the form stem*end
            Stolen from
            https://stackoverflow.com/questions/11023530/python-to-list-http-files-and-directories
        '''
        
        # Split wildcard (if it contains "*")
        if wildcard.count("*") == 0:
            wildcardStart = wildcard
            wildcardEnd   = ''
        elif wildcard.count("*") == 1:
            wildcardStart = wildcard[ : wildcard.find("*")]
            wildcardEnd   = wildcard[ wildcard.find("*") + 1 :]
        else:
            sys.exit('Cannot parse wildcards with >=2 asterisks in them ... [%r]' % wildcard)

        # Get page ...
        page = requests.get(url).text

        # Parse page
        soup = BeautifulSoup(page, 'html.parser')
        
        # Return matching filenames
        return [url + '/' + node.get('href') for node in soup.find_all('a') if \
            isinstance(node.get('href'), str ) and \
            node.get('href').startswith(wildcardStart) and \
            node.get('href').endswith(wildcardEnd) ]



    def force_timecritical_download(self,):
        """ we may want to ensure we have "fresh" copies of some files """
        for f in self.timecritical:
            filename       = f.split("/")[-1]
            local_filepath = os.path.join( self.define_download_subdir() , filename)
            age_in_days    =  (time.time() - os.path.getmtime(local_filepath))/(3600.*24.)
            if age_in_days > 1.0 :
                try:
                    os.rename(local_filepath , local_filepath+"old")
                    wget.download(f, out=self.define_download_subdir() )
                except:
                    print("Failed to download %r" % f)
         


    # Load method(s)
    # ----------------------------------------------
    def load(self,):
        """ load the kernels into memory """

        # Ensure time-critical files are up-to-date
        # -----------------------------------------------
        self.force_timecritical_download()

        # Try to open the local kernel files
        # -----------------------------------------------
        try:
            sp.furnsh( self.expected_local_kernel_filepaths )

        # If the local files don't exist
        #  - Download from the interwebs
        #  - Attempt to load again
        # -----------------------------------------------
        except:
            self.download_data()
            sp.furnsh(self.expected_local_kernel_filepaths)




    





