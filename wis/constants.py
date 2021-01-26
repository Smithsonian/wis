# Define a handy dictionary containing all of the obs-codes we explicitly
# don't want to handle in wis.py
# (at present I am thinking of roving obs-codes)
# --------------------------------------------------------------------------
excluded_obscode_dict = {'247':True}

# Physical constants
# --------------------------------------------------------------------------
Rearth_km = 6378.1363
au_km = 149597870.700 # This is now a definition
Rearth_AU = Rearth_km/au_km
day_s = 86400
