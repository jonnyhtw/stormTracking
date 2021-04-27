'''

  Software for the tracking of storms
  based on detected storm position data.

'''

# Load required modules

import numpy as np
import storm_functions as storm
import glob

#
# Automated storm tracking
#

model_data = True

if model_data:

    suite = 'u-bo721'

    # Load in detected positions and date/hour information
    filenames = sorted(glob.glob('/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/'+suite+'/'+suite+'-storm_det_slp*'))

else:

    filenames = sorted(glob.glob('/nesi/project/niwa00013/williamsjh/NZESM/storm/data/NCEP/20CRv2c/prmsl/6hourly/storm_det_slp*'))

firstiteration = True

for filename in filenames:

    print(filename)

    data = np.load(filename, allow_pickle=True)

    if firstiteration:

        det_storms = data['storms']
        year = data['year']
        month = data['month']
        day = data['day']
        hour = data['hour']

    else:

        det_storms = np.concatenate((det_storms, data['storms']))
        year = np.concatenate((year, data['year']))
        month = np.concatenate((month, data['month']))
        day = np.concatenate((day, data['day']))
        hour = np.concatenate((hour, data['hour']))

    firstiteration = False  

# Initialize storms discovered at first time step

storms = storm.storms_init(det_storms, year, month, day, hour)

# Stitch storm tracks together at future time steps

T = len(det_storms) # number of time steps
for tt in range(1, T-1):
    print(tt, T)
    # Track storms from time step tt-1 to tt and update corresponding tracks and/or create new storms
    storms = storm.track_storms(storms, det_storms, tt, year, month, day, hour, dt=6)

# Add keys for storm age and flag if storm was still in existence at end of run
for ed in range(len(storms)):
    storms[ed]['age'] = len(storms[ed]['lon'])

# Strip storms based on track lengths
storms = storm.strip_storms(storms, dt=6, d_tot_min=0., d_ratio=0., dur_min=0)

# Save tracked storm data

if model_data:
    np.savez('/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/'+suite+'/'+suite+'-storm_track_slp', storms=storms)
else:
    np.savez('/nesi/project/niwa00013/williamsjh/NZESM/storm/data/NCEP/20CRv2c/prmsl/6hourly/storm_track_slp', storms=storms)

