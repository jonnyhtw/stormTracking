'''

  Software for the tracking of storms and high-pressure systems

'''

#
# Load required modules
#

import numpy as np
from datetime import date
import cf_units as unit
from netCDF4 import Dataset

from matplotlib import pyplot as plt

import storm_functions as storm

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--startyear', required=True, type=int)
parser.add_argument('--dataset', required=True, type=str)

args = parser.parse_args()

startyear=args.startyear
print('startyear = ', startyear)

dataset=args.dataset
print('dataset = ', dataset)



#
# Load in slp data and lat/lon coordinates

model_data = True

if model_data:
        if dataset in ['u-bc179', 'u-bc292', 'u-bc370', 'u-bb075', 'u-az513', 'u-az515', 'u-az524', 'u-bb277', 'u-bc470', 'u-bd288', 'u-bd416', 'u-bd483', 'u-bf647', 'u-bf656', 'u-bf703', 'u-bh162']:
            model_pathroot = '/nesi/project/niwa00013/williamsjh/MASS/'+dataset+'/apc.pp/m01s16i222/'
        else:
            model_pathroot = '/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/'+dataset+'/'
else:
    dataset = 'NCEP_20CRV2C'


# Parameters
pathroot = {'NCEP_20CRV2C': '/nesi/project/niwa00013/williamsjh/NZESM/storm/data/NCEP/20CRv2c/prmsl/6hourly/', dataset: model_pathroot}





var = {'NCEP_20CRV2C': 'prmsl', dataset: 'air_pressure_at_sea_level'}

# Generate date and hour vectors
yearStart = {'NCEP_20CRV2C': startyear,  dataset: startyear}

yearEnd = {'NCEP_20CRV2C': startyear,  dataset: startyear}

# Load lat, lon
filename = {'NCEP_20CRV2C': pathroot['NCEP_20CRV2C'] + 'prmsl.' + str(yearStart['NCEP_20CRV2C']) + '.nc',
        dataset: pathroot[dataset] + 'regrid-'+dataset[2:]+'a.pc' + str(yearStart[dataset]) + '.nc'}
fileobj = Dataset(filename[dataset], 'r')
lon = fileobj.variables['lon'][:].astype(float)
lat = fileobj.variables['lat'][:].astype(float)
fileobj.close()

# Load slp data
slp = np.zeros((0, len(lat), len(lon)))
year = np.zeros((0,))
month = np.zeros((0,))
day = np.zeros((0,))
hour = np.zeros((0,))
for yr in range(yearStart[dataset], yearEnd[dataset]+1):

    if model_data:

        filename = {dataset: pathroot[dataset] + 'regrid-'+dataset[2:]+'a.pc' + str(yearStart[dataset]) + '.nc'}

        fileobj = Dataset(filename[dataset], 'r')
        time = unit.num2date(fileobj.variables['time'][:], 'hours since 1970-01-01 00:00:00', unit.CALENDAR_360_DAY) 
        year = np.append(year, [time[tt].year for tt in range(len(time))])
        month = np.append(month, [time[tt].month for tt in range(len(time))])
        day = np.append(day, [time[tt].day for tt in range(len(time))])
        hour = np.append(hour, [time[tt].hour for tt in range(len(time))])
        print(year, month, hour, day)
        slp0 = fileobj.variables[var[dataset]][:].astype(float)
        slp = np.append(slp, slp0, axis=0)
        fileobj.close()
        print(yr, slp0.shape[0])

    else:

        filename = {'NCEP_20CRV2C': pathroot['NCEP_20CRV2C'] + 'prmsl.' + str(yr) + '.nc'} 

        fileobj = Dataset(filename[dataset], 'r')
        time = fileobj.variables['time'][:]
        time_ordinalDays = time/24. + date(1800,1,1).toordinal()
        year = np.append(year, [date.fromordinal(np.floor(time_ordinalDays[tt]).astype(int)).year for tt in range(len(time))])
        month = np.append(month, [date.fromordinal(np.floor(time_ordinalDays[tt]).astype(int)).month for tt in range(len(time))])
        day = np.append(day, [date.fromordinal(np.floor(time_ordinalDays[tt]).astype(int)).day for tt in range(len(time))])
        hour = np.append(hour, (np.mod(time_ordinalDays, 1)*24).astype(int))
        slp0 = fileobj.variables[var[dataset]][:].astype(float)
        slp = np.append(slp, slp0, axis=0)
        fileobj.close()
        print(yr, slp0.shape[0])

#
# Storm Detection
#

# Initialisation

lon_storms_a = []
lat_storms_a = []
amp_storms_a = []
lon_storms_c = []
lat_storms_c = []
amp_storms_c = []

# Loop over time

T = slp.shape[0]

for tt in range(T):
    #
    print(tt, T)
    #
    # Detect lon and lat coordinates of storms
    #
    lon_storms, lat_storms, amp = storm.detect_storms(slp[tt,:,:], lon, lat, res=2, Npix_min=9, cyc='anticyclonic', globe=True)
    lon_storms_a.append(lon_storms)
    lat_storms_a.append(lat_storms)
    amp_storms_a.append(amp)
    #
    lon_storms, lat_storms, amp = storm.detect_storms(slp[tt,:,:], lon, lat, res=2, Npix_min=9, cyc='cyclonic', globe=True)
    lon_storms_c.append(lon_storms)
    lat_storms_c.append(lat_storms)
    amp_storms_c.append(amp)
    #
    # Save as we go
    #
    if (np.mod(tt, 100) == 0) + (tt == T-1):
        print('Save data...')
    #
    # Combine storm information from all days into a list, and save
    #
        storms = storm.storms_list(lon_storms_a, lat_storms_a, amp_storms_a, lon_storms_c, lat_storms_c, amp_storms_c)

        if model_data:
            np.savez('/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/'+dataset+'/'+dataset+'-storm_det_slp_'+str(startyear), storms=storms, year=year, month=month, day=day, hour=hour)

        else:
            np.savez('/nesi/project/niwa00013/williamsjh/NZESM/storm/data/NCEP/20CRv2c/prmsl/6hourly/storm_det_slp_'+str(startyear), storms=storms, year=year, month=month, day=day, hour=hour)
