'''

  Software for the tracking of storms
  based on detected storm position data.

'''

# Load required modules

import numpy as np
import storm_functions as storm
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--startyear', required=True, type=int)
parser.add_argument('--dataset', required=True, type=str)
parser.add_argument('--model_data',required=True, type=bool)

args = parser.parse_args()
startyear=args.startyear
print('startyear = ', startyear)

dataset=args.dataset
print('dataset = ', dataset)

#
# Automated storm tracking
#

model_data = args.model_data

if model_data:
    
    # Load in detected positions and date/hour information
    filenames = sorted(glob.glob('/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/'+dataset+'/'+dataset+'-storm_det_slp*'+str(startyear)+'*'))

else:
    #ncep
    if dataset == 'NCEP_20CRV2C':
        filenames = sorted(glob.glob('/nesi/project/niwa00013/williamsjh/NZESM/storm/data/NCEP/20CRv2c/prmsl/6hourly/storm_det_slp*'))
    #jra
    if dataset == 'jra':
        filenames = sorted(glob.glob('/nesi/project/niwa00013/williamsjh/NZESM/storm/data/jra/storm_det_slp*'+str(startyear)+'*'))
        #era5
    if dataset == 'era5':
        filenames = sorted(glob.glob('/nesi/project/niwa00013/williamsjh/NZESM/storm/data/era5/storm_det_slp*'+str(startyear)+'*'))

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
storms = storm.strip_storms(storms, dt=6, d_tot_min=0., d_ratio=0., dur_min=12)

# Save tracked storm data

if model_data:
    np.savez('/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/'+dataset+'/'+dataset+'-storm_track_slp'+'_'+str(startyear), storms=storms)

else:
    if dataset == 'NCEP_20CRV2C':
        np.savez('/nesi/project/niwa00013/williamsjh/NZESM/storm/data/NCEP/20CRv2c/prmsl/6hourly/storm_track_slp', storms=storms)
    if dataset == 'jra':
        np.savez('/nesi/project/niwa00013/williamsjh/NZESM/storm/data/jra/storm_track_slp'+'_'+str(startyear), storms=storms)
    if dataset == 'era5':
        np.savez('/nesi/project/niwa00013/williamsjh/NZESM/storm/data/era5/storm_track_slp'+'_'+str(startyear), storms=storms)

