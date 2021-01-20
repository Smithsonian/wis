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

# -----------------------------------------
# Local imports
# -----------------------------------------
# None

# -----------------------------------------
# WIS functions & classes
# -----------------------------------------

class KernelDownloader(object):
    """
        KernelDownloader-Object
        
        Holds the specification of where data is online for a given satellite
        
        Provides method to download the data to local machine
    """
    
    def __init__(self,):
        pass
        ''' NB, we will need to set the following variables when we define each instantiation '''
        '''
        self.obscode        = None
        self.name           = None
        self.files          = []
        self.wildcards      = {}
        '''
        
    def download_data(self, destinationDirectory):
        
        # Download explicitly named files
        for f in self.files:
            try:
                wget.download(f, out=destinationDirectory)
            except:
                print("Failed to download %r" % f)
                    
        # Download files using wildcards
        for url,wildcard in self.wildcards.items():
            for f in self._listFD(url, wildcard = wildcard):
                wget.download(f, out=destinationDirectory)
            
    
        # Check whether the download worked
        downloaded, downloadedKernelFiles = self.kernels_have_been_downloaded(destinationDirectory)

        if downloaded:
            return downloadedKernelFiles
        else:
            #print("destinationDirectory", destinationDirectory)
            #print("downloaded, downloadedKernelFiles", downloaded, downloadedKernelFiles)
            sys.exit('download unsuccessful ... ')
            

    def kernels_have_been_downloaded(self, destinationDirectory):
        
        # Check what files exist locally
        # -----------------------------------------------
        downloadedKernelFiles = [ f[f.rfind("/")+1:] for f in glob.glob("%s/*" % destinationDirectory) ]
        
        # Check what files *need* to exist (if wildcards exist, we demand at least 1 download per wildcard)
        # - if they don't, then download
        # -----------------------------------------------
        requiredFiles = [ f[f.rfind("/")+1:] for f in self.files ]
        if len(downloadedKernelFiles) < len(requiredFiles)+len(self.wildcards) or \
                not np.all( [ rf in downloadedKernelFiles for rf in requiredFiles] ):
            return False, []
        else:
            return True, downloadedKernelFiles


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
        return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').startswith(wildcardStart) and node.get('href').endswith(wildcardEnd) ]





class KernelLoader(object):
    """
        Object to manage the loading of JPL spice-kernels into memory.
         - NB: it will also download from the interwebs if not available locally
        
        Parameters
        ----------
        obscode : MPC observation code
            3 or 4 character string
        
        Attributes
        ----------
        ??? : ???
        ???
        
        Notes
        -----
        """
    
    def __init__(self, obscode_specific_KernelDownloader):

        # Directory for downloaded kernels
        # -----------------------------------------------
        self.download_dir = self.define_download_dir()
                
        # Manage sub-directory for obscode downloads
        # -----------------------------------------------
        self.download_subdir = self.define_download_subdir(obscode_specific_KernelDownloader.obscode)
        
        # Try to get the specific desired kernel-files locally ...
        # If not available locally, do remote download of kernels
        # -----------------------------------------------
        downloaded, kernelFiles = obscode_specific_KernelDownloader.kernels_have_been_downloaded(self.download_subdir)
        if not downloaded:
            kernelFiles = obscode_specific_KernelDownloader.download_data(self.download_subdir)

        # Load the satellite-specific kernels
        # -----------------------------------------------
        kernelFilepaths = [ os.path.join(self.download_subdir , f) for f in kernelFiles ]
        sp.furnsh(kernelFilepaths)




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

    def define_download_subdir(self, obscode):
        """
            Returns the default path to the subdirectory where files will be saved
            or loaded for a specific obscode
            
            Uses define_download_dir() to get its parent directly
            
            Returns
            -------
            download_subdir : str
                Path to location of `download_subdir` where kernels will be downloaded
                
        """
        # Get the main download-dir
        d = self.define_download_dir()
        # define a sub-dir path for this obscode
        download_subdir = os.path.join(d, obscode)
        if not os.path.isdir(download_subdir):
            os.mkdir(download_subdir)
        return download_subdir
