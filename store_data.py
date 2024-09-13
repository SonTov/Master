import getData as gd
import dataProcessing as dp
import plotting as pt
import matplotlib.pyplot as plt
from day_parameters import load_day
import pandas as pd
import numpy as np


def run(date, instance, processing_parameters=None, plotting_trajectory=False,
        plotting_region=False, plotting_structure_function=False,
        plotting_ratios=False, plotting_psd=False, plotting_pdf=False,
        write_to_csv=False):
    """

    Applies all other classes to display and calculate using various tools
    write_to_csv stores as datafram in .csv files.
    """

    if processing_parameters is None:
        processing_parameters = {'merged_region': True,
                                 'region_name': 'B',
                                 'tau_interval': 'auto',
                                 'm': 2,
                                 'comparison': 'all',
                                 'divide_structure_function': False,
                                 'print_time_interval': False,
                                 'target': False,
                                 'polar_region': 'all',
                                 'normalize': False,
                                 'write_to_pole': 'North'}

    year, month, day = date
    merged_region = processing_parameters['merged_region']
    region_name = processing_parameters['region_name']
    t = processing_parameters['tau_interval']
    m = processing_parameters['m']
    comparison = processing_parameters['comparison']
    divide_structure_function = processing_parameters['divide_structure_function']
    target = processing_parameters['target']
    polar_region = processing_parameters['polar_region']
    normalize_data = processing_parameters['normalize']
    write_to_pole = processing_parameters['write_to_pole']

    region = 'all' if merged_region else region_name

    dataset = load_day(year, month, day, instance, merged_region)

    fac_parameters_north = dataset['FAC_parameters_north']
    fac_parameters_north_inactive = dataset['FAC_parameters_north_inactive']
    fac_parameters_south = dataset['FAC_parameters_south']
    fac_parameters_south_inactive = dataset['FAC_parameters_south_inactive']



    date = dataset['date']
    date_inactive = dataset['date_inactive']

    day_start = dataset['day_start']
    day_stop = dataset['day_stop']
    day_start_inactive = dataset['day_start_inactive']
    day_stop_inactive = dataset['day_stop_inactive']


    active_day_16Hz = gd.GetData(day_start, day_stop, 'Ne').time()
    active_day_FAC = gd.GetData(day_start, day_stop, 'FAC').time()

    gd.GetData(day_start, day_stop, 'FAC').get_info()
    gd.GetData(day_start, day_stop, 'Ne').get_info()

    inactive_day_16Hz = gd.GetData(day_start_inactive, day_stop_inactive, 'Ne').time()
    inactive_day_FAC = gd.GetData(day_start_inactive, day_stop_inactive, 'FAC').time()

    active_day_north = dp.DataProcessing(active_day_16Hz, active_day_FAC, fac_parameters_north)
    inactive_day_north = dp.DataProcessing(inactive_day_16Hz, inactive_day_FAC, fac_parameters_north_inactive)
    active_day_south = dp.DataProcessing(active_day_16Hz, active_day_FAC, fac_parameters_south)
    inactive_day_south = dp.DataProcessing(inactive_day_16Hz, inactive_day_FAC, fac_parameters_south_inactive)

    if processing_parameters['print_time_interval']:
        if comparison != 'South' or comparison != 'ActiveInactiveSouth':
            print('North Active')
            print(active_day_north.return_data()['time_interval'])
        if comparison == 'all' or comparison == 'ActiveInactiveNorth':
            print('North Inactive')
            print(inactive_day_north.return_data()['time_interval'])
        if comparison == 'all' or comparison == 'South' or comparison == 'ActiveInactiveSouth':
            print('South Active')
            print(active_day_south.return_data()['time_interval'])
        if comparison == 'all' or comparison == 'ActiveInactiveSouth':
            print('South Inactive')
            print(inactive_day_south.return_data()['time_interval'])


    if plotting_trajectory:
        active_day_north.plot_trajectory(f'plots/_{date}_{instance}', other_day=inactive_day_north.return_data(), all_orbits=True)
        active_day_north.find_closest_region(inactive_day_north.return_data())


    if plotting_region:
        target_name = 'Target_'
        if not target:
            target_name = ''
            polar_region = 'all'

        match comparison:
            case 'NorthSouth':
                pt.plot_ne_and_fac(active_day_north.return_data(), name=f'plots/{target_name}Ne_and_FAC_{date}_{instance}_north', target=target, polar_region=polar_region)
                pt.plot_ne_and_fac(active_day_south.return_data(), name=f'plots/{target_name}Ne_and_FAC_{date}_{instance}_south', target=target, polar_region=polar_region)
            case 'ActiveInactiveNorth':
                pt.plot_ne_and_fac(inactive_day_north.return_data(), name=f'plots/{target_name}Ne_and_FAC_inactive_{date}_{instance}_north', target=target, polar_region=polar_region)
                pt.plot_ne_and_fac(active_day_north.return_data(), name=f'plots/{target_name}Ne_and_FAC_{date}_{instance}_north', target=target, polar_region=polar_region)
            case 'ActiveInactiveSouth':
                pt.plot_ne_and_fac(active_day_south.return_data(), name=f'plots/{target_name}Ne_and_FAC_{date}_{instance}_south', target=target, polar_region=polar_region)
                pt.plot_ne_and_fac(inactive_day_south.return_data(), name=f'plots/{target_name}Ne_and_FAC_inactive_{date}_{instance}_south', target=target, polar_region=polar_region)
            case 'all':
                pt.plot_ne_and_fac(inactive_day_north.return_data(), name=f'plots/{target_name}Ne_and_FAC_inactive_{date}_{instance}_north', target=target, polar_region=polar_region)
                pt.plot_ne_and_fac(active_day_north.return_data(), name=f'plots/{target_name}Ne_and_FAC_{date}_{instance}_north', target=target, polar_region=polar_region)
                pt.plot_ne_and_fac(active_day_south.return_data(), name=f'plots/{target_name}Ne_and_FAC_{date}_{instance}_south', target=target, polar_region=polar_region)
                pt.plot_ne_and_fac(inactive_day_south.return_data(), name=f'plots/{target_name}Ne_and_FAC_inactive_{date}_{instance}_south', target=target, polar_region=polar_region)
            case 'North':
                pt.plot_ne_and_fac(active_day_north.return_data(), name=f'plots/{target_name}Ne_and_FAC_{date}_{instance}_north', target=target, polar_region=polar_region)
            case 'South':
                pt.plot_ne_and_fac(active_day_south.return_data(), name=f'plots/{target_name}Ne_and_FAC_{date}_{instance}_south', target=target, polar_region=polar_region)

    if plotting_structure_function:
        norm_name = 'Normalized_' if normalize_data else ''
        name = f'{norm_name}Structure_Function_{region}_m={m}_{date}_{instance}'
        fig, axes = plt.subplots(2, figsize=(12, 8), tight_layout=True)

        match comparison:
            case 'NorthSouth':
                north = active_day_north.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data)
                south = active_day_south.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data)
            case 'ActiveInactiveNorth':
                north = active_day_north.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data, name='A')
                #breakpoint()
                north_inactive = inactive_day_north.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data)
            case 'ActiveInactiveSouth':
                south = active_day_south.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data)
                south_inactive = inactive_day_south.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data)
            case 'all':
                north = active_day_north.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data)
                north_inactive = inactive_day_north.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data)
                south = active_day_south.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data)
                south_inactive = inactive_day_south.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data)
            case 'North':
                north = active_day_north.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data)
            case 'South':
                south = active_day_south.calculate_structure_function(region=region, seconds=t, m=m, normalize_data=normalize_data)

        if divide_structure_function:
            match comparison:
                case 'NorthSouth':
                    north_0 = active_day_north.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    south_0 = active_day_south.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    north_10 = active_day_north.calculate_structure_function_at_specific_time(start_time=10, stop_time=north['seconds'])
                    south_10 = active_day_south.calculate_structure_function_at_specific_time(start_time=10, stop_time=south['seconds'])

                case 'ActiveInactiveNorth':
                    north_0 = active_day_north.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    north_10 = active_day_north.calculate_structure_function_at_specific_time(start_time=10, stop_time=north['seconds'])
                    north_inactive_0 = inactive_day_north.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    north_inactive_10 = inactive_day_north.calculate_structure_function_at_specific_time(start_time=10, stop_time=north_inactive['seconds'])

                case 'ActiveInactiveSouth':
                    south_0 = active_day_south.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    south_10 = active_day_north.calculate_structure_function_at_specific_time(start_time=10, stop_time=south['seconds'])
                    south_inactive_0 = inactive_day_south.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    south_inactive_10 = inactive_day_south.calculate_structure_function_at_specific_time(start_time=10, stop_time=south_inactive['seconds'])

                case 'all':
                    north_0 = active_day_north.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    south_0 = active_day_south.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    north_inactive_0 = inactive_day_north.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    south_inactive_0 = inactive_day_south.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    north_10 = active_day_north.calculate_structure_function_at_specific_time(start_time=10, stop_time=north['seconds'])
                    south_10 = active_day_south.calculate_structure_function_at_specific_time(start_time=10, stop_time=south['seconds'])
                    north_inactive_10 = inactive_day_north.calculate_structure_function_at_specific_time(start_time=10, stop_time=north_inactive['seconds'])
                    south_inactive_10 = inactive_day_south.calculate_structure_function_at_specific_time(start_time=10, stop_time=south_inactive['seconds'])

                case 'North':
                    north_0 = active_day_north.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    north_10 = active_day_north.calculate_structure_function_at_specific_time(start_time=10, stop_time=north['seconds'])
                case 'South':
                    south_0 = active_day_south.calculate_structure_function_at_specific_time(start_time=0, stop_time=10)
                    south_10 = active_day_south.calculate_structure_function_at_specific_time(start_time=10, stop_time=south['seconds'])

            try:
                pt.plot_structure_function(north_0, m, axes, tau_interval=[0, 10], keyword='North')
                pt.plot_structure_function(north_10, m, axes, tau_interval=[10, north['seconds']], keyword='North')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function(south_0, m, axes, tau_interval=[0, 10], keyword='South')
                pt.plot_structure_function(south_10, m, axes, tau_interval=[10, south['seconds']], keyword='South')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function(north_inactive_0, m, axes, tau_interval=[0, 10], keyword='North Inactive')
                pt.plot_structure_function(north_inactive_10, m, axes, tau_interval=[10, north_inactive['seconds']], keyword='North Inactive')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function(south_inactive_0, m, axes, tau_interval=[0, 10], keyword='South Inactive')
                pt.plot_structure_function(south_inactive_10, m, axes, tau_interval=[10, south_inactive['seconds']], keyword='South Inactive')
            except UnboundLocalError:
                pass

        elif not divide_structure_function:
            try:
                pt.plot_structure_function(north, m, axes, keyword='North')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function(north_inactive, m, axes, keyword='North Inactive')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function(south, m, axes, keyword='South')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function(south_inactive, m, axes, keyword='South Inactive')
            except UnboundLocalError:
                pass

        for ax in axes:
            ax.grid()
        fig.savefig(f'plots/{name}')
        plt.close(fig)

    if plotting_ratios and not merged_region:
        name = f'Ratio_m={m}_{date}_{instance}'
        fig_ratio, axes_ratio = plt.subplots(3, figsize=(12, 8), tight_layout=True)

        match comparison:
            case 'NorthSouth':
                active_ratio_north = active_day_north.calculate_structure_function_ratios(m=m)
                active_ratio_south = active_day_south.calculate_structure_function_ratios(m=m)
            case 'ActiveInactiveNorth':
                active_ratio_north = active_day_north.calculate_structure_function_ratios(m=m)
                inactive_ratio_north = inactive_day_north.calculate_structure_function_ratios(m=m)
            case 'ActiveInactiveSouth':
                active_ratio_south = active_day_south.calculate_structure_function_ratios(m=m)
                inactive_ratio_south = inactive_day_south.calculate_structure_function_ratios(m=m)
            case 'all':
                active_ratio_north = active_day_north.calculate_structure_function_ratios(m=m)
                inactive_ratio_north = inactive_day_north.calculate_structure_function_ratios(m=m)
                active_ratio_south = active_day_south.calculate_structure_function_ratios(m=m)
                inactive_ratio_south = inactive_day_south.calculate_structure_function_ratios(m=m)
            case 'North':
                active_ratio_north = active_day_north.calculate_structure_function_ratios(m=m)
            case 'South':
                active_ratio_south = active_day_south.calculate_structure_function_ratios(m=m)

        if divide_structure_function:
            match comparison:
                case 'NorthSouth':
                    active_ratio_north_0 = active_day_north.calculate_structure_function_ratios_at_specific_time(0, 10)
                    active_ratio_north_10 = active_day_north.calculate_structure_function_ratios_at_specific_time(10, active_ratio_north['seconds'])
                    active_ratio_south_0 = active_day_south.calculate_structure_function_ratios_at_specific_time(0, 10)
                    active_ratio_south_10 = active_day_south.calculate_structure_function_ratios_at_specific_time(10, active_ratio_south['seconds'])
                case 'ActiveInactiveNorth':
                    active_ratio_north_0 = active_day_north.calculate_structure_function_ratios_at_specific_time(0, 10)
                    active_ratio_north_10 = active_day_north.calculate_structure_function_ratios_at_specific_time(10, active_ratio_north['seconds'])
                    inactive_ratio_north_0 = inactive_day_north.calculate_structure_function_ratios_at_specific_time(0, 10)
                    inactive_ratio_north_10 = inactive_day_north.calculate_structure_function_ratios_at_specific_time(10, inactive_ratio_north['seconds'])
                case 'ActiveInactiveSouth':
                    active_ratio_south_0 = active_day_south.calculate_structure_function_ratios_at_specific_time(0, 10)
                    active_ratio_south_10 = active_day_south.calculate_structure_function_ratios_at_specific_time(10, active_ratio_south['seconds'])
                    inactive_ratio_south_0 = inactive_day_south.calculate_structure_function_ratios_at_specific_time(0, 10)
                    inactive_ratio_south_10 = inactive_day_south.calculate_structure_function_ratios_at_specific_time(10, inactive_ratio_south['seconds'])
                case 'all':
                    active_ratio_north_0 = active_day_north.calculate_structure_function_ratios_at_specific_time(0, 10)
                    active_ratio_north_10 = active_day_north.calculate_structure_function_ratios_at_specific_time(10, active_ratio_north['seconds'])
                    inactive_ratio_north_0 = inactive_day_north.calculate_structure_function_ratios_at_specific_time(0, 10)
                    inactive_ratio_north_10 = inactive_day_north.calculate_structure_function_ratios_at_specific_time(10, inactive_ratio_north['seconds'])
                    active_ratio_south_0 = active_day_south.calculate_structure_function_ratios_at_specific_time(0, 10)
                    active_ratio_south_10 = active_day_south.calculate_structure_function_ratios_at_specific_time(10, active_ratio_south['seconds'])
                    inactive_ratio_south_0 = inactive_day_south.calculate_structure_function_ratios_at_specific_time(0, 10)
                    inactive_ratio_south_10 = inactive_day_south.calculate_structure_function_ratios_at_specific_time(10, inactive_ratio_south['seconds'])
                case 'North':
                    active_ratio_north_0 = active_day_north.calculate_structure_function_ratios_at_specific_time(0, 10)
                    active_ratio_north_10 = active_day_north.calculate_structure_function_ratios_at_specific_time(10, active_ratio_north['seconds'])
                case 'South':
                    active_ratio_south_0 = active_day_south.calculate_structure_function_ratios_at_specific_time(0, 10)
                    active_ratio_south_10 = active_day_south.calculate_structure_function_ratios_at_specific_time(10, active_ratio_south['seconds'])


            try:
                pt.plot_structure_function_ratios(active_ratio_north_0, m, axes_ratio, tau_interval=[0, 10], keyword='North')
                pt.plot_structure_function_ratios(active_ratio_north_10, m, axes_ratio, tau_interval=[10, active_ratio_north['seconds']], keyword='North')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function_ratios(inactive_ratio_north_0, m, axes_ratio, tau_interval=[0, 10], keyword='North Inactive')
                pt.plot_structure_function_ratios(inactive_ratio_north_10, m, axes_ratio, tau_interval=[10, inactive_ratio_north['seconds']], keyword='North Inactive')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function_ratios(active_ratio_south_0, m, axes_ratio, tau_interval=[0, 10], keyword='South')
                pt.plot_structure_function_ratios(active_ratio_south_10, m, axes_ratio, tau_interval=[10, active_ratio_south['seconds']], keyword='South')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function_ratios(inactive_ratio_south_0, m, axes_ratio, tau_interval=[0, 10], keyword='South Inactive')
                pt.plot_structure_function_ratios(inactive_ratio_south_10, m, axes_ratio, tau_interval=[10, inactive_ratio_south['seconds']], keyword='South Inactive')
            except UnboundLocalError:
                pass

        elif not divide_structure_function:
            try:
                pt.plot_structure_function_ratios(active_ratio_north, fig_ratio, axes_ratio, keyword='North')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function_ratios(inactive_ratio_north, fig_ratio, axes_ratio, keyword='North Inactive')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function_ratios(active_ratio_south, fig_ratio, axes_ratio, keyword='South')
            except UnboundLocalError:
                pass
            try:
                pt.plot_structure_function_ratios(inactive_ratio_south, fig_ratio, axes_ratio, keyword='South Inactive')
            except UnboundLocalError:
                pass

        for ax in axes_ratio:
            ax.grid()
        fig_ratio.savefig(f'plots/{name}')
        plt.close(fig_ratio)

    if plotting_psd:
        dt = 0
        time_interval = None
        p_value = False
        inertial_sub_range = False
        name = f'Power_Spectral_Density_Active_{region}_{date}_{instance}'
        fig_psd, axes_psd = plt.subplots(figsize=(9, 6), tight_layout=True)
        active_psd_north = active_day_north.calculate_power_spectral_density(region, dt=dt, time_interval=time_interval)
        pt.plot_power_spectral_density(active_psd_north, fig_psd, axes_psd, 'High Activity Day', p_value=p_value, region=region, dt=dt, inertial_sub_range=inertial_sub_range)
        axes_psd.grid()
        fig_psd.savefig(f'plots/{name}')
        plt.close(fig_psd)


        name = f'Power_Spectral_Density_Inactive_{region}_{date}_{instance}'
        fig_psd, axes_psd = plt.subplots(figsize=(9, 6), tight_layout=True)
        inactive_psd_north = inactive_day_north.calculate_power_spectral_density(region, dt=dt, time_interval=time_interval)
        pt.plot_power_spectral_density(inactive_psd_north, fig_psd, axes_psd, 'Low Activity Day', p_value=p_value, color='C1', region=region, dt=dt, inertial_sub_range=inertial_sub_range)
        axes_psd.grid()
        fig_psd.savefig(f'plots/{name}')
        plt.close(fig_psd)

        from scipy.integrate import simpson
        print(simpson(active_psd_north['power_spectral_density'], active_psd_north['frequency']))
        print(simpson(inactive_psd_north['power_spectral_density'], inactive_psd_north['frequency']))

        #active_psd_south = active_day_south.calculate_power_spectral_density(region)
        #inactive_psd_south = inactive_day_south.calculate_power_spectral_density(region)

        #pt.plot_power_spectral_density(active_psd_south, fig_psd, axes_psd, 'South', p_value=True)
        #pt.plot_power_spectral_density(inactive_psd_south, fig_psd, axes_psd, 'South Inactive', p_value=True)

        #active_psd_interval = active_day_north.calculate_power_spectral_density(region, start_time=348, stop_time=355)
        #pt.plot_power_spectral_density(active_psd_interval, fig_psd, axes_psd, 'Active 348-355', p_value=True)

    if plotting_pdf:
        match comparison:
            case 'NorthSouth':
                fig_north_active_pdf, axes_north_active_pdf = plt.subplots(figsize=(9, 6))
                fig_south_active_pdf, axes_south_active_pdf = plt.subplots(figsize=(9, 6))
            case 'ActiveInactiveNorth':
                fig_north_active_pdf, axes_north_active_pdf = plt.subplots(figsize=(9, 6))
                fig_north_inactive_pdf, axes_north_inactive_pdf = plt.subplots(figsize=(9, 6))
            case 'ActiveInactiveSouth':
                fig_south_active_pdf, axes_south_active_pdf = plt.subplots(figsize=(9, 6))
                fig_south_inactive_pdf, axes_south_inactive_pdf = plt.subplots(figsize=(9, 6))
            case 'all':
                fig_north_active_pdf, axes_north_active_pdf = plt.subplots(figsize=(9, 6))
                fig_north_inactive_pdf, axes_north_inactive_pdf = plt.subplots(figsize=(9, 6))
                fig_south_active_pdf, axes_south_active_pdf = plt.subplots(figsize=(9, 6))
                fig_south_inactive_pdf, axes_south_inactive_pdf = plt.subplots(figsize=(9, 6))
            case 'North':
                fig_north_active_pdf, axes_north_active_pdf = plt.subplots(figsize=(9, 6))
            case 'South':
                fig_south_active_pdf, axes_south_active_pdf = plt.subplots(figsize=(9, 6))


        name_active_north = f'Probability_Density_Fluctuations_North_{region}_{date}_{instance}'
        name_inactive_north = f'Probability_Density_Fluctuations_North_Inactive_{region}_{date}_{instance}'
        name_active_south = f'Probability_Density_Fluctuations_South_{region}_{date}_{instance}'
        name_inactive_south = f'Probability_Density_Fluctuations_South_Inactive_{region}_{date}_{instance}'

        try:
            active_day_north.plot_probability_density_fluctuations(fig_north_active_pdf, axes_north_active_pdf, region, limit=(1E-3, 5), name='High Activity Day')
            axes_north_active_pdf.grid()
            fig_north_active_pdf.savefig(f'plots/{name_active_north}')
            plt.close(fig_north_active_pdf)
        except UnboundLocalError:
            pass
        try:
            inactive_day_north.plot_probability_density_fluctuations(fig_north_inactive_pdf, axes_north_inactive_pdf, region, limit=(1E-3, 5), name='Low Activity Day')
            axes_north_inactive_pdf.grid()
            fig_north_inactive_pdf.savefig(f'plots/{name_inactive_north}')
            plt.close(fig_north_inactive_pdf)
        except UnboundLocalError:
            pass
        try:
            active_day_south.plot_probability_density_fluctuations(fig_south_active_pdf, axes_south_active_pdf, region, limit=(1E-3, 5), name='High Activity Day')
            axes_south_active_pdf.grid()
            fig_south_active_pdf.savefig(f'plots/{name_active_south}')
            plt.close(fig_south_active_pdf)
        except UnboundLocalError:
            pass
        try:
            inactive_day_south.plot_probability_density_fluctuations(fig_south_inactive_pdf, axes_south_inactive_pdf, region, limit=(1E-3, 5), name='Low Activity Day')
            axes_south_inactive_pdf.grid()
            fig_south_inactive_pdf.savefig(f'plots/{name_inactive_south}')
            plt.close(fig_south_inactive_pdf)
        except UnboundLocalError:
            pass

    if write_to_csv:

        if write_to_pole == 'North':
            active_north = active_day_north.calculate_structure_function(region=region, seconds=t, m=(2, 4), normalize_data=False, calculate_empirical_flatness=False)
            inactive_north = inactive_day_north.calculate_structure_function(region=region, seconds=t, m=(2, 4), normalize_data=False, calculate_empirical_flatness=False)
        elif write_to_pole == 'South':
            active_north = active_day_south.calculate_structure_function(region=region, seconds=t, m=(2, 4), normalize_data=False, calculate_empirical_flatness=False)
            inactive_north = inactive_day_south.calculate_structure_function(region=region, seconds=t, m=(2, 4), normalize_data=False, calculate_empirical_flatness=False)

        try:
            active = {'structure_function_M2': active_north['structure_function'][2],
                      'structure_function_M4': active_north['structure_function'][4],
                      'empirical_flatness': active_north['empirical_flatness']}
            active_tau = np.asarray(active_north['tau'])
            df_active = pd.DataFrame(active, index=active_tau)
            df_active.to_csv(f'Active_{region_name}_files_{write_to_pole}/{date}_{instance}')
        except TypeError:  # Dummy data frame so both corresponding active and inactive csv files can be loaded simultaneously
            active_dummy = {'structure_function_M2': np.zeros(10),
                            'structure_function_M4': np.zeros(10),
                            'empirical_flatness': np.zeros(10)}
            df_active_dummy = pd.DataFrame(active_dummy, index=np.arange(0, 10))
            df_active_dummy.to_csv(f'Active_{region_name}_files_{write_to_pole}/{date}_{instance}_dummy')

        try:
            inactive = {'structure_function_M2': inactive_north['structure_function'][2],
                        'structure_function_M4': inactive_north['structure_function'][4],
                        'empirical_flatness': inactive_north['empirical_flatness']}

            inactive_tau = np.asarray(inactive_north['tau'])
            df_inactive = pd.DataFrame(inactive, index=inactive_tau)
            df_inactive.to_csv(f'Inactive_{region_name}_files_{write_to_pole}/{date}_{instance}')
        except TypeError:
            inactive_dummy = {'structure_function_M2': np.zeros(10),
                              'structure_function_M4': np.zeros(10),
                              'empirical_flatness': np.zeros(10)}
            df_inactive_dummy = pd.DataFrame(inactive_dummy, index=np.arange(0, 10))
            df_inactive_dummy.to_csv(f'Inactive_{region_name}_files_{write_to_pole}/{date}_{instance}_dummy')

        print(F'DONE {date} {instance} of 3')


if __name__ == '__main__':


    #date = [year, month, day]


    # All available dates during high activity days
    # Corresponding low activity day is automatically detected
    dates = [[2014, 11, 4],
             [2014, 12, 7],
             [2015, 11, 7],
             [2015, 11, 8],
             [2015, 11, 9],
             [2015, 11, 10],
             [2015, 11, 11],
             [2015, 12, 5],
             [2015, 12, 6],
             [2015, 12, 11],
             [2015, 12, 14],
             [2015, 12, 20],
             [2015, 12, 31]]

    instances = [1, 2, 3]
    region_name = 'B'
    m = (2, 4)
    pole = 'North'
    # comparison = 'all', 'North' 'South' 'NorthSouth'(only active) 'ActiveInactiveNorth' 'ActiveInactiveSouth'
    # polar_region = 'all', 'A', 'B', 'C', 'AB', 'AC', 'BC'
    # polar_region overwritten if target=False
    # polar_region should be 'all' if merged_region = True
    # target = only if plotting_region

    processing_parameters = {'merged_region': True,
                             'region_name': region_name,
                             'tau_interval': 1,
                             'm': 2,
                             'comparison': 'ActiveInactiveNorth',
                             'divide_structure_function': False,
                             'print_time_interval': True,
                             'target': True,
                             'polar_region': 'all',
                             'normalize': False,
                             'write_to_pole': pole}

    #Uncomment and indent to iterate through all dates
    #for date in dates:
    #    for instance in instances:
    run([2015, 12, 31], 1, processing_parameters, plotting_trajectory=False, plotting_region=True, plotting_structure_function=False,
        plotting_ratios=False, plotting_psd=False, plotting_pdf=False, write_to_csv=False)
