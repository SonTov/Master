import matplotlib.pyplot as plt
import detectRegion as dr
from functions import *
import numpy as np
import scipy as sp
from scipy.stats import linregress


class DataProcessing:
    def __init__(self, data_16Hz, data_FAC, region_parameters):
        self.closest_latitudes = None
        self.timestamp_16Hz = data_16Hz['Timestamp']
        self.timestamp_FAC = data_FAC['Timestamp']
        self.latitude_16Hz = data_16Hz['Latitude']
        self.longitude_16Hz = data_16Hz['Longitude']
        self.latitude_FAC = data_FAC['Latitude']
        self.longitude_FAC = data_FAC['Longitude']
        self.ne = data_16Hz['Density']
        self.fac = data_FAC['FAC']

        working_data = dr.DetectRegion(data_16Hz, data_FAC, region_parameters=region_parameters,
                                       normalize_data=False).return_region()

        ne_region = working_data['Ne']
        fac_region = working_data['FAC']

        self.ne_region = ne_region
        self.fac_region = fac_region

    def plot_ne_and_fac(self, name, x_axis_limit_Ne=False, x_axis_limit_FAC=False):
        fig, axes = plt.subplots(2, figsize=(12, 8))
        axes[0].plot(self.timestamp_16Hz, self.ne, label='Ne')
        axes[1].plot(self.timestamp_FAC, self.fac, label='FAC')
        if isinstance(self.fac_region, dict):
            axes[0].plot(self.timestamp_16Hz, self.ne_region['A'], label='Auroral region 1 of Ne')
            axes[0].plot(self.timestamp_16Hz, self.ne_region['B'], label='Polar cap region of Ne')
            axes[0].plot(self.timestamp_16Hz, self.ne_region['C'], label='Auroral region 2 of Ne')
            axes[1].plot(self.timestamp_FAC, self.fac_region['A'], label='Auroral region 1 of FAC')
            axes[1].plot(self.timestamp_FAC, self.fac_region['B'], label='Polar cap region of FAC')
            axes[1].plot(self.timestamp_FAC, self.fac_region['C'], label='Auroral region 2 of FAC')
        else:
            axes[0].plot(self.timestamp_16Hz, self.ne_region, label='')
            axes[1].plot(self.timestamp_FAC, self.fac_region, label='')
        for ax in axes:
            ax.legend()
            ax.grid()
        # axes[0].set_xlabel('Time')
        if x_axis_limit_Ne:
            axes[0].set_ylim(0, x_axis_limit_Ne)
        if x_axis_limit_FAC:
            axes[1].set_ylim(-x_axis_limit_FAC, x_axis_limit_FAC)
        axes[0].set_ylabel('Ne')
        axes[1].set_xlabel('TIme')
        axes[1].set_ylabel('FAC')
        fig.tight_layout()
        fig.savefig(f'plots/{name}')

    def plot_regions(self, name, x_axis_limit_Ne=False, x_axis_limit_FAC=False):
        fig, axes = plt.subplots(2, figsize=(12, 8))
        if isinstance(self.fac_region, dict):
            axes[0].plot(self.timestamp_16Hz, self.ne_region['A'], label='Auroral region 1 of Ne')
            axes[0].plot(self.timestamp_16Hz, self.ne_region['B'], label='Polar cap region of Ne')
            axes[0].plot(self.timestamp_16Hz, self.ne_region['C'], label='Auroral region 2 of Ne')
            axes[1].plot(self.timestamp_FAC, self.fac_region['A'], label='Auroral region 1 of FAC')
            axes[1].plot(self.timestamp_FAC, self.fac_region['B'], label='Polar cap region of FAC')
            axes[1].plot(self.timestamp_FAC, self.fac_region['C'], label='Auroral region 2 of FAC')
        else:
            axes[0].plot(self.timestamp_16Hz, self.ne_region, label='Auroral Region of Ne')
            axes[1].plot(self.timestamp_FAC, self.fac_region, label='Auroral Region of FAC')
        for ax in axes:
            ax.legend()
            ax.grid()
        # axes[0].set_xlabel('Time')
        if x_axis_limit_Ne:
            axes[0].set_ylim(0, x_axis_limit_Ne)
        if x_axis_limit_FAC:
            axes[1].set_ylim(-x_axis_limit_FAC, x_axis_limit_FAC)
        axes[0].set_ylabel('Ne')
        axes[1].set_xlabel('TIme')
        axes[1].set_ylabel('FAC')

        fig.tight_layout()
        fig.savefig(f'plots/{name}')

    def plot_structure_function(self, name, region='all', seconds=120, start_seconds=False, ignore_start=False, plot_regression=False, label=False, equal_axes=True):
        if region == 'all':
            region = self.ne_region
        elif region == 'A':
            region = self.ne_region['A']
        elif region == 'B':
            region = self.ne_region['B']
        elif region == 'C':
            region = self.ne_region['C']
        if seconds * 16 - int(seconds * 16) != 0:
            print('The chosen seconds does not give an integer as indices.')
            print(f'{int(seconds * 16) / 16} seconds have been set.')
        tau_full_range = np.arange(1, int(seconds * 16))
        start_tau = int(start_seconds * 16) if start_seconds else 1
        structure_function_values = []
        slope_values = []
        empirical_flatness_values = []

        def structure_function_helper(m, n=False, start_seconds=start_seconds, from_seconds=True, ignore_start=ignore_start):
            sf_full = structure_function(region_n, tau_full_range, m)
            if from_seconds:
                sf = sf_full[start_tau:]
                tau = tau_full_range[start_tau:]
            elif not from_seconds:
                sf = sf_full[:start_tau]
                tau = tau_full_range[:start_tau]
            sf = np.log10(sf.astype(float))
            g = linregress(tau, sf.astype('float'))
            if n:
                axes[0][n - 1].plot(tau / 16, sf, label=f'm={m}')
                axes[1][n - 1].scatter(m, g.slope, s=100, marker='X', label=f'g({m})')
                if plot_regression:
                    axes[0][n - 1].plot(tau / 16, g.intercept + g.slope * tau, c='b', ls='dotted', label='fitted line')

                if start_seconds and not ignore_start:
                    structure_function_helper(m, n, start_seconds=False, from_seconds=False)  # To avoid infinite loop
                print(f'Progress: {n / 3}')

                structure_function_values.append(np.min(sf))
                structure_function_values.append(np.max(sf))
                slope_values.append(g.slope)

                del sf

                axes[0][n - 1].set_xscale('log')
                axes[0][n - 1].set_xlabel(r'$\tau$')
                axes[0][n - 1].set_ylabel(r'S($\tau$,m)')
                if m == 1:
                    ef_full = empirical_flatness(region_n, tau_full_range)
                    if from_seconds:
                        ef = ef_full[start_tau:]
                    elif not from_seconds:
                        ef = ef_full[:start_tau]
                    empirical_flatness_values.append(np.min(ef))
                    empirical_flatness_values.append(np.max(ef))
                    axes[2][n - 1].plot(tau / 16, ef, label=r'S(4, $\tau$) / S²(2, $\tau$)')
                    axes[2][n - 1].set_xscale('log')
            else:
                axes[0].plot(tau / 16, sf, label=f'm={m}')
                axes[1].scatter(m, g.slope, s=100, marker='X', label=f'g({m})')
                if plot_regression:
                    axes[0].plot(tau / 16, g.intercept + g.slope * tau, c='b', ls='dotted', label='fitted line')

                if start_seconds and not ignore_start:
                    structure_function_helper(m, start_seconds=False, from_seconds=False)  # To avoid infinite loop
                print(f'Progress: {m} of 4')

                del sf

                axes[0].set_xscale('log')
                axes[0].set_xlabel(r'$\tau$')
                axes[0].set_ylabel(r'S($\tau$,m)')

                if m == 1:
                    ef_full = empirical_flatness(region_n, tau_full_range)
                    if from_seconds:
                        ef = ef_full[start_tau:]
                    elif not from_seconds:
                        ef = ef_full[:start_tau]
                    axes[2].plot(tau / 16, ef, label=r'S(4, $\tau$) / S²(2, $\tau$)')
                    axes[2].set_xscale('log')

        if isinstance(region, dict):
            fig, axes = plt.subplots(3, 3, figsize=(12, 8))
            for n, key in zip(range(1, 4), region.keys()):
                region_n = region[key][region[key] != None]
                for m in range(1, 5):
                    structure_function_helper(m, n)
                for ax in axes:
                    # ax[n - 1].legend(bbox_to_anchor=(1.0, 1.0), prop={'size': 6})
                    ax[n - 1].grid()
                    if label:
                        ax[n - 1].legend(prop={'size': 6})

            if equal_axes:
                min_lim_sf = np.min(structure_function_values) - 1 / 10 * np.min(structure_function_values)
                max_lim_sf = np.max(structure_function_values) + 1 / 10 * np.min(structure_function_values)
                min_lim_slope = np.min(slope_values) - 1 / 4 * np.max(slope_values)
                max_lim_slope = np.max(slope_values) + 1 / 8 * np.max(slope_values)
                min_lim_ef = np.min(empirical_flatness_values) - 1 / 4 * np.max(empirical_flatness_values)
                max_lim_ef = np.max(empirical_flatness_values) + 1 / 4 * np.max(empirical_flatness_values)
                for n in range(3):
                    axes[0][n].set_ylim(min_lim_sf, max_lim_sf)
                    axes[1][n].set_ylim(min_lim_slope, max_lim_slope)
                    axes[2][n].set_ylim(min_lim_ef, max_lim_ef)

        else:
            fig, axes = plt.subplots(3, figsize=(12, 8))
            region_n = region[region != None]
            for m in range(1, 5):
                structure_function_helper(m)
            for ax in axes:
                # ax.legend(bbox_to_anchor=(1.0, 1.0), prop={'size': 6})
                ax.grid()
                if label:
                    ax.legend(prop={'size': 6})

        fig.tight_layout()
        fig.savefig(f'plots/{name}')

    def plot_ratio(self, name, seconds=120, m_value=False):
        region = self.ne_region
        if seconds * 16 - int(seconds * 16) != 0:
            print('The chosen seconds does not give an integer as indices.')
            print(f'{int(seconds * 16) / 16} seconds have been set.')
        tau = np.arange(1, int(seconds * 16))
        fig, axes = plt.subplots(3, figsize=(12, 8))
        sf_values = {}
        labels = {0: 'A', 1: 'B', 2: 'C'}
        for n, key in zip(range(3), region.keys()):
            region_n = region[key][region[key] != None]
            for m in range(1, 5):
                sf = structure_function(region_n, tau, m)
                sf = np.log10(sf.astype(float))
                print(f'Progress: {m} of 4 and {n + 1} of 3')
                sf_values[f'{m} and {n}'] = sf
                del sf
        if not m_value:
            for m in range(1, 5):
                axes[0].plot(sf_values[f'{m} and {0}'] / sf_values[f'{m} and {2}'],
                             label=f'm = {m}')
                axes[1].plot(sf_values[f'{m} and {1}'] / sf_values[f'{m} and {0}'],
                             label=f'm = {m}')
                axes[2].plot(sf_values[f'{m} and {1}'] / sf_values[f'{m} and {2}'],
                             label=f'm = {m}')
        elif isinstance(m_value, int):
            axes[0].plot(sf_values[f'{m} and {0}'] / sf_values[f'{m} and {2}'],
                         label=f'm = {m_value}')
            axes[1].plot(sf_values[f'{m_value} and {1}'] / sf_values[f'{m_value} and {0}'],
                         label=f'm = {m_value}')
            axes[2].plot(sf_values[f'{m_value} and {1}'] / sf_values[f'{m_value} and {2}'],
                         label=f'm = {m_value}')
        for ax in axes:
            # ax[n].legend(bbox_to_anchor=(1.0, 1.0), prop={'size': 6})
            ax.set_xscale('log')
            ax.set_xlabel(r'$\tau$')
            ax.legend(prop={'size': 6})
            ax.grid()

            for n in range(3):
                x = 2 if n == 0 or n == 2 else 0
                n_dummy = 0 if n == 0 else 1 if n == 2 else n
                axes[n].set_ylabel(f'{labels[n_dummy]} / {labels[x]}')

        fig.tight_layout()
        fig.savefig(f'plots/{name}')

    def plot_power_spectral_density(self, name, region='all'):  # Calculate slope
        if region == 'A':
            region = self.ne_region['A']
        elif region == 'B':
            region = self.ne_region['B']
        elif region == 'C':
            region = self.ne_region['C']
        elif region == 'all':
            region = self.ne_region
        idx = np.where(region != None)

        region_fft = sp.fft.rfft(region[idx])  # https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.rfft.html
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html#scipy.fft.fft
        amplitude = np.abs(region_fft) ** 2
        fig, axes = plt.subplots(2, figsize=(12, 8))
        axes[0].plot(self.timestamp_16Hz[idx], region[idx])
        # https://stackoverflow.com/questions/10514315/how-to-add-a-second-x-axis
        dummy = np.ones(len(region[idx])) * np.mean(region[idx])
        latitude = self.latitude_16Hz[idx]
        ax_lat = axes[0].twiny()
        ax_lat.plot(latitude, dummy, alpha=0.0)
        if latitude[0] > latitude[-1]:
            plt.xlim(max(latitude), min(latitude))
        axes[1].plot(amplitude)
        axes[1].set_xscale('log')
        axes[1].set_yscale('log')
        # axes[1].set_ylim(5 * 10E-4)
        for ax in axes:
            ax.grid()
        fig.tight_layout()
        fig.savefig(f'plots/{name}')

    def probability_density_fluctuations(self, name, region='all'):
        import seaborn as sns
        from scipy.stats import norm
        if region == 'A':
            region = self.ne_region['A']
        elif region == 'B':
            region = self.ne_region['B']
        elif region == 'C':
            region = self.ne_region['C']
        elif region == 'all':
            region = self.ne_region
        idx = np.where(region != None)
        fig, ax = plt.subplots(figsize=(12, 8))
        increments = np.array([0.5, 1, 2, 4, 8, 16, 32]) * 16
        increments = np.array(increments, dtype=int)
        mean_sets = []
        std_sets = []
        for increment in increments:
            dne = delta_n(region[idx], increment)
            data = dne / np.std(dne)
            #ax.hist(data, density=True, alpha=0.6, color='blue')
            sns.kdeplot(data, ax=ax, linewidth=4, ls='dotted', label=f'$\delta$t = {increment}')
            x = np.linspace(np.min(data), np.max(data), len(data))
            mean_sets.append(np.mean(data))
            std_sets.append(np.std(data))
        gaussian = norm.pdf(x, np.mean(mean_sets), np.mean(std_sets))
        ax.plot(x, gaussian, color='black')  # Normal distribution https://stackoverflow.com/questions/10138085/how-to-plot-normal-distribution
        ax.legend()
        ax.grid()
        ax.set_yscale('log')
        fig.tight_layout()
        fig.savefig(f'plots/{name}')

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
        m.scatter(x, y, marker='D', color='m', s=0.5)

        if other_day:
            latitude_other = other_day['Latitude']
            longitude_other = other_day['Longitude']

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
                    m.scatter(x_other, y_other, marker='D', color='black', s=0.5)
                else:
                    if all_orbits:
                        x_other, y_other = m(longitude_other_subarray[closest_indices], latitude_other_subarray[closest_indices])
                        m.scatter(x_other, y_other, marker='D', color='grey', s=0.5)

        plt.savefig(f'plots/{name}')
        plt.close()

    def find_closest_region(self, other_day):
        try:
            idx_start = np.where([other_day['Latitude'] == self.closest_latitudes[0]])[-1][0]
            idx_stop = np.where([other_day['Latitude'] == self.closest_latitudes[-1]])[-1][0]
            print(other_day['Timestamp'][idx_start])
            print(other_day['Timestamp'][idx_stop])
        except TypeError:
            print('closest trajectory for previous/next day not calculated, or region_num parameter in other_day is not set to false')

    def return_region_data(self):
        return {'Ne': self.ne_region, 'FAC': self.fac_region, 'Latitude': self.latitude_FAC, 'Longitude': self.longitude_FAC, 'Timestamp': self.timestamp_FAC}