from datetime import datetime
import getData as gd
import dataProcessing as dp


active_day_start = datetime(2014, 11, 4, 7, 00, 00, 00)
active_day_stop = datetime(2014, 11, 4, 18, 00, 00, 00)

inactive_day_start = datetime(2014, 11, 3, 7, 00, 00, 00)
inactive_day_stop = datetime(2014, 11, 3, 18, 00, 00, 00)

active_day_16Hz = gd.GetData(active_day_start, active_day_stop, 'Ne').time()
active_day_FAC = gd.GetData(active_day_start, active_day_stop, 'FAC').time()

inactive_day_16Hz = gd.GetData(inactive_day_start, inactive_day_stop, 'Ne').time()
inactive_day_FAC = gd.GetData(inactive_day_start, inactive_day_stop, 'FAC').time()

active_day_FAC_parameters = {"time_interval": 2, "threshold": 1, "region_num": (8, 9), 'total_region': False}
inactive_day_FAC_parameters = {"time_interval": 2, "threshold": 0.5, "region_num": (10, 11), 'total_region': False}

active_day = dp.DataProcessing(active_day_16Hz, active_day_FAC, active_day_FAC_parameters)
inactive_day = dp.DataProcessing(inactive_day_16Hz, inactive_day_FAC, inactive_day_FAC_parameters)

t = 120

#active_day.plot_ne_and_fac('Active_Day_Ne_and_FAC', 4E6, 30)
#active_day.plot_regions('Active_Day_Ne_and_FAC_Chosen_Region', 1E6, 30)
#active_day.plot_structure_function('Active_Day_Structure_Function_From_10_Seconds', region='all', seconds=t, ignore_start=True, start_seconds=10, plot_regression=True, label=False)
#active_day.plot_ratio('Active_day_Structure_Function_Ratios', seconds=t, m_value=2) #Only when dividing region into A, B and C
active_day.plot_power_spectral_density('Active_Day_Power_spectral_density', 'A')
active_day.probability_density_fluctuations('Active_Region_pdf', 'A')


#active_day.plot_trajectory('closest_trajectory', other_day=inactive_day.return_region_data(), all_orbits=True) # Does not work at south pole all the time
#active_day.find_closest_region(inactive_day.return_region_data())


#inactive_day.plot_ne_and_fac('Inactive_Day_Ne_and_FAC', 4E6, 30)
#inactive_day.plot_regions('Inactive_Day_Ne_and_FAC_Chosen_Region', 1E6, 30)
#inactive_day.plot_structure_function('inactive_Day_Structure_Function_From_10_Seconds', region='all', seconds=t, ignore_start=True, start_seconds=10, plot_regression=True, label=False)
#inactive_day.plot_ratio('Inactive_day_Structure_Function_Ratios', seconds=t, m_value=2)
inactive_day.plot_power_spectral_density('Inactive_Day_Power_spectral_density', 'A')
inactive_day.probability_density_fluctuations('Inactive_Region_pdf', 'A')
