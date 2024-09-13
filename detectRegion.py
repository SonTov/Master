from datetime import timedelta
from functions import normalize, geographic_to_magnetic
import numpy as np


class DetectRegion:
    def __init__(self, dataset_ne, dataset_fac, region_parameters=None, normalize_data=False, magnetic=False):
        """

        :param dataset_ne: dataset for electron density (dictionary)
        :param dataset_fac: dataset for field-aligned currents (dictionary)
        :param region_parameters: threshold, time between peaks, etc... (dictionary)
        :param normalize_data: (Boolean)
        :param magnetic: magnetic coordinates (Boolean)
        """
        if region_parameters is None:
            region_parameters = {'time_interval': 2, 'threshold': 0.5, 'region_num': False, 'total_region': False}

        self.timestamp_16hz = dataset_ne['Timestamp']
        self.ne = dataset_ne['Density']

        self.timestamp_fac = dataset_fac['Timestamp']
        self.fac = dataset_fac['FAC']

        self.normalize_data = normalize_data

        self.region_parameters = region_parameters

        self.ne_region = self.detect_region(self.ne, self.region_parameters['region_num'])
        self.fac_region = self.detect_region(self.fac, self.region_parameters['region_num'])

        time_interval = {}

        if isinstance(self.ne_region, dict):
            for key in self.ne_region.keys():
                time_interval_region = {}
                time = self.timestamp_16hz[self.ne_region[key] != None]
                time_interval_region['start'] = "{}h {}m {}s".format(np.min(time).hour, np.min(time).minute, np.min(time).second)
                time_interval_region['stop'] = "{}h {}m {}s".format(np.max(time).hour, np.max(time).minute, np.max(time).second)
                time_interval[key] = time_interval_region

        else:
            time = self.timestamp_16hz[self.ne_region != None]
            time_interval['start'] = "{}h {}m {}s".format(np.min(time).hour, np.min(time).minute, np.min(time).second)
            time_interval['stop'] = "{}h {}m {}s".format(np.max(time).hour, np.max(time).minute, np.max(time).second)

        self.time_interval = time_interval


        self.magnetic_coordinates = None
        if magnetic:
            altitude = dataset_fac['Radius'][self.fac_region != None]
            latitude = dataset_fac['Latitude'][self.fac_region != None]
            longitude = dataset_fac['Longitude'][self.fac_region != None]
            time = dataset_fac['Timestamp'][self.fac_region != None]

            self.magnetic_coordinates = geographic_to_magnetic(altitude, latitude, longitude, time)


    def detect_region(self, arr, region_num):
        """
        Uses the FAC to detect auroral regions and potentially polar cap region.
        Finds each element above threshold value and calculates amount of time between each of said elements.
        Elements below threshold value but inside the time interval are
        added to array along with the elements above the threshold to avoid unnecessary amounts of very small regions.

        :param arr: array of either Ne or FAC.
        :param region_num: Boolean/integer/tuple - which region (from 1 to n) to return. False for all regions (in 1 array)
        :return: region_num = False --> one array containing all regions.
                 region_num = integer --> one array containing one region.
                 region_num = tuple --> three arrays, one between regions in tuple (polar cap) and the other two as these regions
        """
        if isinstance(region_num, tuple) and self.normalize_data:
            self.normalize_data = 'regular_for_polar_cap'
        if arr.shape == self.fac.shape:
            if (arr == self.fac).all:
                self.normalize_data = False  # Only normalizes Ne
        time_diff = []
        datetime_arr = self.timestamp_fac[np.abs(self.fac) >= self.region_parameters['threshold']]
        for i in range(1, len(datetime_arr)):
            diff = datetime_arr[i] - datetime_arr[i - 1]
            if diff <= timedelta(minutes=self.region_parameters['time_interval']):
                time_diff.append(datetime_arr[i])
        if len(arr) == len(self.timestamp_16hz):
            timestamp = self.timestamp_16hz
        elif len(arr) == len(self.timestamp_fac):
            timestamp = self.timestamp_fac
        new_time_diff = [time_diff[0]]
        for i in range(0, len(time_diff)):
            diff = time_diff[i] - time_diff[i - 1]
            if diff >= timedelta(minutes=2):
                new_time_diff.append(time_diff[i - 1])
                new_time_diff.append(time_diff[i])
            elif i == len(time_diff) - 1:
                new_time_diff.append(time_diff[i])  # Last FAC region have no timedelta to compare with, but knows it's > threshold so is in time_diff
        result = np.zeros(len(timestamp))
        max_range = int(np.ceil(len(new_time_diff) / 2))  # Round up
        for i in range(max_range):
            result[np.where((new_time_diff[2 * i] <= timestamp) & (timestamp <= new_time_diff[2 * i + 1]))] = i + 1
        if not region_num:
            if self.normalize_data == 'regular':
                region = np.where(np.isin(result, range(1, max_range + 1)), arr, None)
                region[region != None] = normalize(region)
                return region
            else:
                return np.where(np.isin(result, range(1, max_range + 1)), arr, None)
        elif isinstance(region_num, int):
            if self.normalize_data == 'regular':
                region = np.where(result == region_num, arr, None)
                region[region != None] = normalize(region)
                return region
            else:
                return np.where(result == region_num, arr, None)
        elif isinstance(region_num, tuple):
            region = np.where(np.isin(result, region_num), arr, None)  # Regions m,n and area between
            polar_cap = np.where(np.isin(result, region_num), None, None)  # Only region between m and n
            region_idx = np.where(region != None)
            for idx in range(np.min(region_idx), np.max(region_idx)):
                if region[idx] is None:
                    polar_cap[idx] = arr[idx]
            pre_polar_cap = self.detect_region(arr, region_num=region_num[0])
            post_polar_cap = self.detect_region(arr, region_num=region_num[1])
            if self.normalize_data == 'regular_for_polar_cap':
                result_new = np.concatenate((pre_polar_cap[pre_polar_cap != None], polar_cap[polar_cap != None], post_polar_cap[post_polar_cap != None]))
                new_normalize = 1 / np.max(result_new)
                pre_polar_cap[pre_polar_cap != None] *= new_normalize
                polar_cap[polar_cap != None] *= new_normalize
                post_polar_cap[post_polar_cap != None] *= new_normalize
            elif self.normalize_data == 'independent':
                pre_polar_cap[pre_polar_cap != None] = normalize(pre_polar_cap)
                polar_cap[polar_cap != None] = normalize(polar_cap)
                post_polar_cap[post_polar_cap != None] = normalize(post_polar_cap)
            if self.region_parameters['total_region']:
                complete_region = polar_cap
                complete_region[pre_polar_cap != None] = pre_polar_cap[pre_polar_cap != None]
                complete_region[post_polar_cap != None] = post_polar_cap[post_polar_cap != None]
                return complete_region
            elif not self.region_parameters['total_region']:
                return {'A': pre_polar_cap, 'B': polar_cap, 'C': post_polar_cap}

    def return_region(self):
        return {'Ne': self.ne_region, 'FAC': self.fac_region, 'time_interval': self.time_interval, 'magnetic_coordinates': self.magnetic_coordinates}
