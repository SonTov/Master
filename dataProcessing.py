import matplotlib.pyplot as plt
import detectRegion as dr
from functions import *
import numpy as np
import scipy as sp
from scipy.stats import linregress, norm
import seaborn as sns


class DataProcessing:
    def __init__(self, data_16Hz, data_FAC, region_parameters, magnetic=False):
        self.ratio_dataset = None
        self.dataset = None
        self.closest_latitudes = None
        self.timestamp_16Hz = data_16Hz['Timestamp']
        self.timestamp_FAC = data_FAC['Timestamp']
        self.latitude_16Hz = data_16Hz['Latitude']
        self.longitude_16Hz = data_16Hz['Longitude']
        self.latitude_FAC = data_FAC['Latitude']
        self.longitude_FAC = data_FAC['Longitude']
        self.ne = data_16Hz['Density']
        self.fac = data_FAC['FAC']

        working_data = dr.DetectRegion(data_16Hz, data_FAC, region_parameters=region_parameters, magnetic=magnetic).return_region()

        ne_region = working_data['Ne']
        fac_region = working_data['FAC']

        time_interval = working_data['time_interval']
        magnetic_coordinates = working_data['magnetic_coordinates']

        self.ne_region = ne_region
        self.fac_region = fac_region

        self.time_interval = time_interval
        self.magnetic_coordinates = magnetic_coordinates

    def calculate_structure_function(self, region='all', seconds='auto', m='all', normalize_data=False, calculate_empirical_flatness=True):
        try:
            if region == 'all':
                region = self.ne_region
            elif region == 'A':
                region = self.ne_region['A']
            elif region == 'B':
                region = self.ne_region['B']
            elif region == 'C':
                region = self.ne_region['C']
        except IndexError:
            return self.dataset

        region = region[region != None]
        dataset = {}
        slope_dataset = {}
        structure_function_dataset = {}
        regression_dataset = {}

        if seconds == 'auto':
            seconds = len(region)
            tau = np.arange(1, int(seconds))
        elif seconds == 'auto_half':
            seconds = len(region) / 2
            tau = np.arange(1, int(seconds))
        elif isinstance(seconds, int) or isinstance(seconds, float):
            tau = np.arange(1, int(seconds * 16))

        dataset['seconds'] = int(seconds / 16)
        if m == 'all':
            for m in range(1, 5):
                sf = structure_function(region, tau, m)

                sf = np.log10(sf.astype(float))

                if normalize_data:
                    sf = normalize(sf)

                g = linregress(np.log10(tau.astype(float)), sf.astype('float'))

                structure_function_dataset[m] = sf
                slope_dataset[m] = g.slope
                regression_dataset[m] = g.intercept + g.slope * np.log10(tau.astype(float))

                print(f'{m} of 4 complete')

        elif isinstance(m, int):
            sf = structure_function(region, tau, m)

            sf = np.log10(sf.astype(float))

            if normalize_data:
                sf = normalize(sf)

            g = linregress(np.log10(tau.astype(float)), sf.astype('float'))

            structure_function_dataset[m] = sf
            slope_dataset[m] = g.slope
            regression_dataset[m] = g.intercept + g.slope * np.log10(tau.astype(float))

            print('Done')

        elif isinstance(m, tuple):
            for elem in m:
                sf = structure_function(region, tau, elem)

                sf = np.log10(sf.astype(float))

                g = linregress(np.log10(tau.astype(float)), sf.astype('float'))

                structure_function_dataset[elem] = sf
                slope_dataset[elem] = g.slope
                regression_dataset[elem] = g.intercept + g.slope * np.log10(tau.astype(float))

                print('Done')

        del sf

        dataset['structure_function'] = structure_function_dataset

        if calculate_empirical_flatness:
            ef = empirical_flatness(region, tau)

            if normalize_data:
                ef = normalize(ef)

        elif isinstance(m, tuple):
            try:
                ef = (10 ** dataset['structure_function'][4]) / ((10 ** dataset['structure_function'][2]) ** 2)
            except KeyError:
                ef = None


        else:
            ef = None

        dataset['slope'] = slope_dataset
        dataset['regression'] = regression_dataset
        dataset['empirical_flatness'] = ef
        dataset['tau'] = tau / 16
        self.dataset = dataset
        return dataset

    def calculate_structure_function_at_specific_time(self, start_time, stop_time):
        new_dataset = {}

        new_slope_dataset = {}
        new_structure_function_dataset = {}
        new_regression_dataset = {}

        start_tau = int(start_time * 16) if start_time != 0 else 1
        stop_tau = int(stop_time * 16)

        new_dataset['tau'] = self.dataset['tau'][start_tau:stop_tau]
        if self.dataset['empirical_flatness'] is not None:
            new_dataset['empirical_flatness'] = self.dataset['empirical_flatness'][start_tau:stop_tau]
        for key in self.dataset['structure_function'].keys():
            new_structure_function_dataset[key] = self.dataset['structure_function'][key][start_tau:stop_tau]

            g = linregress(np.log10(new_dataset['tau']).astype('float'), new_structure_function_dataset[key].astype('float'))
            new_regression_dataset[key] = g.intercept + g.slope * np.log10(new_dataset['tau']).astype('float')
            new_slope_dataset[key] = g.slope

        new_dataset['structure_function'] = new_structure_function_dataset
        new_dataset['slope'] = new_slope_dataset
        new_dataset['regression'] = new_regression_dataset
        new_dataset['seconds'] = stop_time
        return new_dataset

    def calculate_structure_function_ratios(self, seconds='auto_half', m=2):
        region = self.ne_region
        region_A = region['A'][region['A'] != None]
        region_B = region['B'][region['B'] != None]
        region_C = region['C'][region['C'] != None]

        if seconds == 'auto':
            region_lengths = [len(region_A), len(region_B), len(region_C)]
            seconds = int(np.min(region_lengths))
            tau = np.arange(1, int(seconds - 1))
        if seconds == 'auto_half':
            region_lengths = [len(region_A), len(region_B), len(region_C)]
            seconds = int(np.min(region_lengths) / 2)
            tau = np.arange(1, int(seconds))
        elif isinstance(seconds, int) or isinstance(seconds, float):
            tau = np.arange(1, int(seconds * 16))

        dataset = {'B/A': structure_function(region_B, tau, m) / structure_function(region_A, tau, m),
                   'B/C': structure_function(region_B, tau, m) / structure_function(region_C, tau, m),
                   'A/C': structure_function(region_A, tau, m) / structure_function(region_C, tau, m),
                   'tau': tau,
                   'seconds': int(seconds / 16)}

        self.ratio_dataset = dataset
        return dataset

    def calculate_structure_function_ratios_at_specific_time(self, start_time, stop_time):
        new_dataset = {}

        start_tau = int(start_time * 16) if start_time != 0 else 1
        stop_tau = int(stop_time * 16)

        new_dataset['tau'] = self.ratio_dataset['tau'][start_tau:stop_tau]
        new_dataset['B/A'] = self.ratio_dataset['B/A'][start_tau:stop_tau]
        new_dataset['B/C'] = self.ratio_dataset['B/C'][start_tau:stop_tau]
        new_dataset['A/C'] = self.ratio_dataset['A/C'][start_tau:stop_tau]

        new_dataset['seconds'] = stop_time
        return new_dataset

    def calculate_power_spectral_density(self, region='all', start_time=False, stop_time=False):  # Calculate slope
        if region == 'all':
            region = self.ne_region
        elif region == 'A':
            region = self.ne_region['A']
        elif region == 'B':
            region = self.ne_region['B']
        elif region == 'C':
            region = self.ne_region['C']

        idx = np.where(region != None)
        new_region = region[idx]

        if start_time and stop_time:
            start_tau = int(start_time * 16) if start_time != 0 else 1
            stop_tau = int(stop_time * 16)
            new_region = new_region[start_tau: stop_tau]

        region_fft = sp.fft.rfft(new_region)  # https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.rfft.html
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html#scipy.fft.fft
        amplitude = np.log10(np.abs(region_fft) ** 2)
        frequency = sp.fft.rfftfreq(new_region.size, d=1/16)
        frequency_dummy = frequency
        frequency_dummy[0] = 1E-5
        p = linregress(np.log10(frequency_dummy).astype(float), amplitude.astype('float'))
        regression = p.intercept + p.slope * np.log10(frequency_dummy).astype('float')

        return {'power_spectral_density': amplitude, 'frequency': frequency, 'slope': p.slope, 'regression': regression}

    def plot_probability_density_fluctuations(self, fig, axes, region='all', limit=False):

        if region == 'A':
            region = self.ne_region['A']
        elif region == 'B':
            region = self.ne_region['B']
        elif region == 'C':
            region = self.ne_region['C']
        elif region == 'all':
            region = self.ne_region

        idx = np.where(region != None)

        increments = np.array([0.5, 1, 2, 4, 8, 16, 32]) * 16
        increments = np.array(increments, dtype=int)

        mean_sets = []
        std_sets = []

        for increment in increments:
            dne = delta_n(region[idx], increment)
            data = dne / np.std(dne)

            sns.kdeplot(data, ax=axes, linewidth=4, ls='dotted', label=f'$\delta$t = {increment / 16}')
            x = np.linspace(np.min(data), np.max(data), len(data))
            mean_sets.append(np.mean(data))
            std_sets.append(np.std(data))

        gaussian = norm.pdf(x, np.mean(mean_sets), np.mean(std_sets))
        axes.plot(x, gaussian, color='black')  # Normal distribution https://stackoverflow.com/questions/10138085/how-to-plot-normal-distribution
        axes.legend()
        axes.set_yscale('log')
        if limit:
            axes.set_ylim(limit[0], limit[1])
            axes.set_xlim(-6, 6)
        fig.tight_layout()

    def plot_trajectory(self, name, latitude_limit=0, other_day=False, all_orbits=False):
        from mpl_toolkits.basemap import Basemap
        from itertools import chain
        try:
            longitude = self.longitude_FAC[self.fac_region['B'] != None]
            latitude = self.latitude_FAC[self.fac_region['B'] != None]
        except IndexError:
            longitude = self.longitude_FAC[self.fac_region != None]
            latitude = self.latitude_FAC[self.fac_region != None]
        latitude_limit = np.abs(latitude_limit)
        if np.max(latitude) > 0:
            north = True
            viewing_latitude = 50
        else:
            north = False
            viewing_latitude = -50

        # https://jakevdp.github.io/PythonDataScienceHandbook/04.13-geographic-data-with-basemap.html
        def draw_map(m, scale=0.2):
            # draw a shaded-relief image
            m.shadedrelief(scale=scale)

            # lats and longs are returned as a dictionary
            lats = m.drawparallels(np.linspace(-90, 90, 13))
            lons = m.drawmeridians(np.linspace(-180, 180, 13))

            # keys contain the plt.Line2D instances
            lat_lines = chain(*(tup[1][0] for tup in lats.items()))
            lon_lines = chain(*(tup[1][0] for tup in lons.items()))
            all_lines = chain(lat_lines, lon_lines)

            # cycle through these lines and set the desired style
            for line in all_lines:
                line.set(linestyle='-', alpha=0.3, color='w')


        fig = plt.figure(figsize=(12, 8))
        m = Basemap(projection='ortho', resolution=None,
                    lon_0=0, lat_0=viewing_latitude)
        draw_map(m)
        longitude = longitude[np.abs(latitude) >= latitude_limit]
        latitude = latitude[np.abs(latitude) >= latitude_limit]
        coordinates = np.column_stack((latitude, longitude))
        x, y = m(longitude, latitude)
        m.scatter(x, y, marker='D', color='m', s=0.5, label='High Activity Trajectory')

        if other_day:
            latitude_other = other_day['Latitude_FAC']
            longitude_other = other_day['Longitude_FAC']

            if north:
                latitude_other_limit = np.where(latitude_other >= latitude_limit, latitude_other, None)
                longitude_other_limit = np.where(latitude_other >= latitude_limit, longitude_other, None)
            else:
                latitude_other_limit = np.where(latitude_other <= latitude_limit, latitude_other, None)
                longitude_other_limit = np.where(latitude_other <= latitude_limit, longitude_other, None)
            latitude_other_idx = np.where(latitude_other_limit == None)[0]
            latitude_other_subarrays = np.split(latitude_other_limit, latitude_other_idx)
            longitude_other_subarrays = np.split(longitude_other_limit, latitude_other_idx)
            latitude_other_new = [np.array(subarray[subarray != None], dtype=np.float64) for subarray in latitude_other_subarrays if len(subarray) > 1]
            longitude_other_new = [np.array(subarray[subarray != None], dtype=np.float64) for subarray in longitude_other_subarrays if len(subarray) > 1]
            closest_indices_set = []
            mean_dist = []
            for subarray_lat, subarray_lon in zip(latitude_other_new, longitude_other_new):
                coordinates_other_new = np.column_stack((subarray_lat[subarray_lat != None], subarray_lon[subarray_lon != None]))
                distances = np.linalg.norm(coordinates[:, None, :] - coordinates_other_new, axis=2)
                closest_indices = np.argmin(distances, axis=1)
                closest_indices_set.append(closest_indices)
                coordinates_other_new_2 = coordinates_other_new[closest_indices]
                distance = np.abs(coordinates - coordinates_other_new_2).sum()
                mean_dist.append(distance)
            for latitude_other_subarray, longitude_other_subarray, closest_indices, i in zip(latitude_other_new, longitude_other_new, closest_indices_set, range(len(mean_dist))):
                if i == np.argmin(mean_dist):
                    self.closest_latitudes = latitude_other_subarray[closest_indices]
                    x_other, y_other = m(longitude_other_subarray[closest_indices], latitude_other_subarray[closest_indices])
                    m.scatter(x_other, y_other, marker='D', color='black', s=0.5, label='Closest Low Activity Trajectory')
                else:
                    if all_orbits:
                        x_other, y_other = m(longitude_other_subarray[closest_indices], latitude_other_subarray[closest_indices])
                        m.scatter(x_other, y_other, marker='D', color='grey', s=0.5)
        plt.legend(fontsize=14, markerscale=14, loc='upper right', bbox_to_anchor=(1.4, 1.1))
        plt.savefig(f'{name}')
        plt.close()

    def find_closest_region(self, other_day):
        try:
            idx_start = np.where([other_day['Latitude_FAC'] == self.closest_latitudes[0]])[-1][0]
            idx_stop = np.where([other_day['Latitude_FAC'] == self.closest_latitudes[-1]])[-1][0]
            print(other_day['Timestamp_FAC'][idx_start])
            print(other_day['Timestamp_FAC'][idx_stop])
        except TypeError:
            print('closest trajectory for previous/next day not calculated, or region_num parameter in other_day is not set to false')

    def return_data(self):
        return {'Density_Full': self.ne, 'FAC_Full': self.fac,
                'Density': self.ne_region, 'FAC': self.fac_region,
                'Latitude_FAC': self.latitude_FAC, 'Longitude_FAC': self.longitude_FAC,
                'Latitude_16Hz': self.latitude_16Hz, 'Longitude_16Hz': self.longitude_16Hz,
                'Timestamp_FAC': self.timestamp_FAC, 'Timestamp_16Hz': self.timestamp_16Hz,
                'time_interval': self.time_interval,
                'magnetic_coordinates': self.magnetic_coordinates}
