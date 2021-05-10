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

args = parser.parse_args()
startyear=args.startyear
print('startyear = ', startyear)

#
# Load in slp data and lat/lon coordinates

model_data = True

if model_data:
    dataset = 'u-bh162'
else:
    dataset = 'NCEP_20CRV2C'

# Parameters
pathroot = {'NCEP_20CRV2C': '/nesi/project/niwa00013/williamsjh/NZESM/storm/data/NCEP/20CRv2c/prmsl/6hourly/', 'u-bl658': '/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/u-bl658/','u-bb075': '/nesi/project/niwa00013/williamsjh/MASS/u-bb075/apc.pp/m01s16i222/','u-bh162': '/nesi/project/niwa00013/williamsjh/MASS/u-bh162/apc.pp/m01s16i222/','u-bd483': '/nesi/project/niwa00013/williamsjh/MASS/u-bd483/apc.pp/m01s16i222/','u-bf656': '/nesi/project/niwa00013/williamsjh/MASS/u-bf656/apc.pp/m01s16i222/','u-bc179': '/nesi/project/niwa00013/williamsjh/MASS/u-bc179/apc.pp/m01s16i222/','u-bo721': '/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/u-bo721/','u-bx226': '/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/u-bx226/','u-bw947': '/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/u-bw947/'}
var = {'NCEP_20CRV2C': 'prmsl', 'u-bl658': 'air_pressure_at_sea_level', 'u-bb075': 'air_pressure_at_sea_level', 'u-bd483': 'air_pressure_at_sea_level', 'u-bf656': 'air_pressure_at_sea_level',  'u-bo721': 'air_pressure_at_sea_level',  'u-bx226': 'air_pressure_at_sea_level',  'u-bc179': 'air_pressure_at_sea_level',  'u-bx226': 'air_pressure_at_sea_level',  'u-bc179': 'air_pressure_at_sea_level',  'u-bw947': 'air_pressure_at_sea_level',  'u-bh162': 'air_pressure_at_sea_level'}

# Generate date and hour vectors
yearStart = {'NCEP_20CRV2C': startyear,  'u-bl658': startyear, 'u-bb075': startyear, 'u-bd483': startyear, 'u-bf656': startyear, 'u-bo721': startyear, 'u-bx226': startyear, 'u-bc179': startyear, 'u-bw947': startyear, 'u-bh162': startyear}
yearEnd = {'NCEP_20CRV2C': startyear,  'u-bl658': startyear, 'u-bb075': startyear, 'u-bd483': startyear, 'u-bf656': startyear, 'u-bo721': startyear, 'u-bx226': startyear, 'u-bc179': startyear, 'u-bw947': startyear, 'u-bh162': startyear}

# Load lat, lon
filename = {'NCEP_20CRV2C': pathroot['NCEP_20CRV2C'] + 'prmsl.' + str(yearStart['NCEP_20CRV2C']) + '.nc',
            'u-bl658': pathroot['u-bl658'] + 'regrid-bl658a.pc' + str(yearStart['u-bl658']) + '.nc', 
            'u-bo721': pathroot['u-bo721'] + 'regrid-bo721a.pc' + str(yearStart['u-bo721']) + '.nc',
            'u-bx226': pathroot['u-bx226'] + 'regrid-bx226a.pc' + str(yearStart['u-bx226']) + '.nc',
            'u-bw947': pathroot['u-bw947'] + 'regrid-bw947a.pc' + str(yearStart['u-bw947']) + '.nc',
            'u-bh162': pathroot['u-bh162'] + 'regrid-bh162a.pc' + str(yearStart['u-bh162']) + '.nc',
            'u-bb075': pathroot['u-bb075'] + 'regrid-bb075a.pc' + str(yearStart['u-bb075']) + '.nc',
            'u-bf656': pathroot['u-bf656'] + 'regrid-bf656a.pc' + str(yearStart['u-bf656']) + '.nc',
            'u-bc179': pathroot['u-bc179'] + 'regrid-bc179a.pc' + str(yearStart['u-bc179']) + '.nc',
            'u-bd483': pathroot['u-bd483'] + 'regrid-bd483a.pc' + str(yearStart['u-bd483']) + '.nc' }
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

        filename = {'u-bl658': pathroot['u-bl658'] + 'regrid-bl658a.pc' + str(yearStart['u-bl658']) + '.nc',
                    'u-bo721': pathroot['u-bo721'] + 'regrid-bo721a.pc' + str(yearStart['u-bo721']) + '.nc',
                    'u-bx226': pathroot['u-bx226'] + 'regrid-bx226a.pc' + str(yearStart['u-bx226']) + '.nc',
                    'u-bw947': pathroot['u-bw947'] + 'regrid-bw947a.pc' + str(yearStart['u-bw947']) + '.nc',
                    'u-bh162': pathroot['u-bh162'] + 'regrid-bh162a.pc' + str(yearStart['u-bh162']) + '.nc',
                    'u-bb075': pathroot['u-bb075'] + 'regrid-bb075a.pc' + str(yearStart['u-bb075']) + '.nc',
                    'u-bf656': pathroot['u-bf656'] + 'regrid-bf656a.pc' + str(yearStart['u-bf656']) + '.nc',
                    'u-bc179': pathroot['u-bc179'] + 'regrid-bc179a.pc' + str(yearStart['u-bc179']) + '.nc',
                    'u-bd483': pathroot['u-bd483'] + 'regrid-bd483a.pc' + str(yearStart['u-bd483']) + '.nc'}

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
