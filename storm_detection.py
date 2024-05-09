'''

  Software for the tracking of storms and high-pressure systems

'''

#
# Load required modules
#

import numpy as np
import copy
from datetime import date
import cf_units as unit
from netCDF4 import Dataset

from matplotlib import pyplot as plt

import storm_functions as storm

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
# Load in slp data and lat/lon coordinates

model_data = args.model_data
model_data = False

print('model_data=',model_data)


if model_data:
    if dataset in ['u-bc179', 'u-bc292', 'u-bc370', 'u-bb075', 'u-az513', 'u-az515', 'u-az524', 'u-bb277', 'u-bc470', 'u-bd288', 'u-bd416', 'u-bd483', 'u-bf647', 'u-bf656', 'u-bf703', 'u-bh162','u-bh409','u-bi805','u-be509','u-be537','u-be647','u-be653','u-bh570','u-bh716','u-bh210','u-bh807','u-be693','u-be686','u-be392','u-be396','u-be679','u-be682','u-be683','u-be606','u-be684','u-be690','u-be393','u-be397','u-be394','u-be398','u-be335','u-be395']:
        model_pathroot = '/nesi/project/niwa00013/williamsjh/MASS/'+dataset+'/apc.pp/m01s16i222/'
    else:
        model_pathroot = '/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/'+dataset+'/'

    suite = copy.deepcopy(dataset)
else:
    suite = 'foo'
    model_pathroot = 'foo'

#if model_data == False:
#    del suite

print('suite=',suite)

# Parameters
pathroot = {'NCEP_20CRV2C': '/nesi/project/niwa00013/williamsjh/NZESM/storm/data/NCEP/20CRv2c/prmsl/6hourly/', suite: model_pathroot, 'jra': '/nesi/project/niwa00013/williamsjh/NZESM/storm/data/jra/', 'era5': '/nesi/project/niwa00013/williamsjh/NZESM/storm/data/era5/'}


var = {'NCEP_20CRV2C': 'prmsl', suite: 'air_pressure_at_sea_level', 'jra': 'var2', 'era5': 'msl'}

# Generate date and hour vectors
yearStart = {'NCEP_20CRV2C': startyear,  suite: startyear, 'jra': startyear, 'era5': startyear}

yearEnd = {'NCEP_20CRV2C': startyear,  suite: startyear, 'jra': startyear, 'era5': startyear}

# Load lat, lon
filename = {'NCEP_20CRV2C': pathroot['NCEP_20CRV2C'] + 'prmsl.' + str(yearStart['NCEP_20CRV2C']) + '.nc',
            'jra': pathroot['jra'] + 'regrid-selhour-fcst_surf.002_prmsl.reg_tl319.' + str(yearStart['jra']) + '.nc',
            'era5': pathroot['era5'] + 'regrid-era5-slp-'+ str(yearStart['jra']) + '.nc',
             suite: pathroot[suite] + 'regrid-'+suite[2:]+'a.pc' + str(yearStart[suite]) + '.nc'}

print('dataset=',dataset)
print('pathroot=',pathroot)
print('model_data=',model_data)
print('filename=',filename[dataset])
print('suite=',suite)

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

        filename = {suite: pathroot[suite] + 'regrid-'+suite[2:]+'a.pc' + str(yearStart[suite]) + '.nc'}

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

        filename = {'NCEP_20CRV2C': pathroot['NCEP_20CRV2C'] + 'prmsl.' + str(yr) + '.nc',  
              'jra': pathroot['jra'] + 'regrid-selhour-fcst_surf.002_prmsl.reg_tl319.' + str(yr) + '.nc',
              'era5': pathroot['era5'] + 'regrid-era5-slp-' + str(yr) + '.nc'}

        fileobj = Dataset(filename[dataset], 'r')
        time = fileobj.variables['time'][:]

        if dataset == 'NCEP_20CRV2C':
            time_ordinalDays = time/24. + date(1800,1,1).toordinal()
        elif dataset == 'era5':
            time_ordinalDays = time/24. + date(1900,1,1).toordinal()
        elif dataset == 'jra':
            time_ordinalDays = time/24. + date(int(yr),1,1).toordinal()

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
            np.savez('/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/'+suite+'/'+suite+'-storm_det_slp_'+str(startyear), storms=storms, year=year, month=month, day=day, hour=hour)

        else:
            np.savez(pathroot[dataset]+'/storm_det_slp_'+str(startyear), storms=storms, year=year, month=month, day=day, hour=hour)
