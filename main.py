import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
from scipy.integrate import simpson


#Loads calculated data from.csv - files
#Faster to analyse data

region = 'C'

#Instance
i = 4

#Scales (found out too late that m comes before n in the alphabet)
n = 10
m = 10 * 16
j = 100 * 16
k = -1

active_directory = f'Active_{region}_files_North'
inactive_directory = f'Inactive_{region}_files_North'

dates = []

active_slopes_m2_1_10 = []
inactive_slopes_m2_1_10 = []
active_slopes_m2_10_100 = []
inactive_slopes_m2_10_100 = []

active_slopes_m4_1_10 = []
inactive_slopes_m4_1_10 = []
active_slopes_m4_10_100 = []
inactive_slopes_m4_10_100 = []

active_sf_m2 = []
active_sf_m4 = []

inactive_sf_m2 = []
inactive_sf_m4 = []

active_ef = []
inactive_ef = []

active_tau = []
inactive_tau = []

for f, g in zip(os.listdir(active_directory), os.listdir(inactive_directory)):
    with open(f'{active_directory}/{f}', 'r') as active_data, open(f'{inactive_directory}/{g}', 'r') as inactive_data:
        active_dataset = pd.read_csv(active_data)
        inactive_dataset = pd.read_csv(inactive_data)

        if not np.all(active_dataset['structure_function_M2']) == 0:

            active_tau.append(active_dataset.index)
            inactive_tau.append(inactive_dataset.index)

            active_sf_m2.append(np.array(active_dataset['structure_function_M2']))
            active_sf_m4.append(active_dataset['structure_function_M4'])

            inactive_sf_m2.append(np.array(inactive_dataset['structure_function_M2']))
            inactive_sf_m4.append(inactive_dataset['structure_function_M4'])

            active_ef.append(active_dataset['empirical_flatness'])
            inactive_ef.append(inactive_dataset['empirical_flatness'])

            dates.append(str(f))

            try:
                active_g_m2_1_10 = linregress(np.log10(active_dataset.index[n:m].astype(float)),
                                              active_dataset['structure_function_M2'][n:m].astype('float'))
                active_slopes_m2_1_10.append(active_g_m2_1_10.slope)
                active_g_m4_1_10 = linregress(np.log10(active_dataset.index[n:m].astype(float)),
                                              active_dataset['structure_function_M4'][n:m].astype('float'))
                active_slopes_m4_1_10.append(active_g_m4_1_10.slope)

                active_g_m2_10_100 = linregress(np.log10(active_dataset.index[m:j].astype(float)),
                                                active_dataset['structure_function_M2'][m:j].astype('float'))
                active_slopes_m2_10_100.append(active_g_m2_10_100.slope)
                active_g_m4_10_100 = linregress(np.log10(active_dataset.index[m:j].astype(float)),
                                                active_dataset['structure_function_M4'][m:j].astype('float'))
                active_slopes_m4_10_100.append(active_g_m4_10_100.slope)


            except ValueError:
                pass
            try:
                inactive_g_m2_1_10 = linregress(np.log10(inactive_dataset.index[n:m].astype(float)),
                                                inactive_dataset['structure_function_M2'][n:m].astype('float'))
                inactive_slopes_m2_1_10.append(inactive_g_m2_1_10.slope)
                inactive_g_m4_1_10 = linregress(np.log10(inactive_dataset.index[n:m].astype(float)),
                                                inactive_dataset['structure_function_M4'][n:m].astype('float'))
                inactive_slopes_m4_1_10.append(inactive_g_m4_1_10.slope)
                inactive_g_m2_10_100 = linregress(np.log10(inactive_dataset.index[m:j].astype(float)),
                                                  inactive_dataset['structure_function_M2'][m:j].astype('float'))
                inactive_slopes_m2_10_100.append(inactive_g_m2_10_100.slope)
                inactive_g_m4_10_100 = linregress(np.log10(inactive_dataset.index[m:j].astype(float)),
                                                  inactive_dataset['structure_function_M4'][m:j].astype('float'))
                inactive_slopes_m4_10_100.append(inactive_g_m4_10_100.slope)
            except ValueError:
                pass

# Uncomment to specify exact instance
# also used to find index for data
# as it is loaded in random order

"""i = 0
for elem in dates:
    if elem == '20151231_1':
        break
    else:
        i+=1
"""
#i=14
print(i)
#Redundant
d = i



def plotting():
    """
    Plots area of structure function by integration
    Both as normal plot high vs low activity and histogram.
    """
    area_active = []
    area_inactive = []

    area_active_100 = []
    area_inactive_100 = []

    maximas_active = []
    maximas_inactive = []

    maximas_active_100 = []
    maximas_inactive_100 = []

    fig, axes = plt.subplots(figsize=(9, 6), tight_layout=True)

    for x in range(len(active_sf_m2)):

        active_tau_ = active_tau[x][n:m]
        inactive_tau_ = inactive_tau[x][n:m]

        active_tau_100 = active_tau[x][m:j]
        inactive_tau_100 = inactive_tau[x][m:j]

        if x == len(active_sf_m2) - 1:
            axes.plot(active_tau[x][n:m] / 16, active_sf_m2[x][n:m], label='structure function active', color='C0')
            axes.plot(inactive_tau[x][n:m] / 16, inactive_sf_m2[x][n:m], label='structure function inactive',
                      color='C1')
            axes.legend()
        else:
            axes.plot(active_tau[x][n:m] / 16, active_sf_m2[x][n:m], color='C0')
            axes.plot(inactive_tau[x][n:m] / 16, inactive_sf_m2[x][n:m], color='C1')

        area_active.append(simpson(active_sf_m2[x][n:m], active_tau[x][n:m] / 16))
        area_inactive.append(simpson(inactive_sf_m2[x][n:m], inactive_tau[x][n:m] / 16))

        area_active_100.append(simpson(active_sf_m2[x][m:j], active_tau[x][m:j] / 16))
        area_inactive_100.append(simpson(inactive_sf_m2[x][m:j], inactive_tau[x][m:j] / 16))

        axes.set_xscale('log')
        axes.grid()
        axes.set_title(f'Structure Function and Maxima {region} [{int(n / 16)}, {int(m / 16)}]')
        a = active_sf_m2[x][n:m]
        b = inactive_sf_m2[x][n:m]

        a_100 = active_sf_m2[x][m:j]
        b_100 = inactive_sf_m2[x][m:j]

        maxima_active = np.argmax(a)
        maxima_inactive = np.argmax(b)

        maxima_active_100 = np.argmax(a_100)
        maxima_inactive_100 = np.argmax(b_100)

        maximas_active.append(active_tau_[maxima_active] / 16)
        maximas_inactive.append(inactive_tau_[maxima_inactive] / 16)

        maximas_active_100.append(active_tau_100[maxima_active_100] / 16)
        maximas_inactive_100.append(inactive_tau_100[maxima_inactive_100] / 16)

        axes.scatter(active_tau_[maxima_active] / 16, a[maxima_active], color='C0')
        axes.scatter(inactive_tau_[maxima_inactive] / 16, b[maxima_inactive], color='C1')
    fig.savefig(f'Structure_Function_{region}_{int(n / 16)}_{int(m / 16)}')

    bins = 20

    fig, axes = plt.subplots(2, figsize=(9, 6), tight_layout=True, sharex=False, sharey=True)
    if region != 'All':
        axes[0].set_title(r'a) Area of S(2, $\tau$), $\tau$=[1s, 10s] in' + f' Region {region}', fontsize=24)
        axes[1].set_title(r'b) Area of S(2, $\tau$), $\tau$=[10s, 100s] in' + f' Region {region}', fontsize=24)
    else:
        axes[0].set_title(r'a) Area of S(2, $\tau$), $\tau$=[1s, 10s] in' + ' Polar Region', fontsize=24)
        axes[1].set_title(r'b) Area of S(2, $\tau$), $\tau$=[10s, 100s] in' + ' Polar Region', fontsize=24)
    axes[0].hist(area_active, edgecolor='black', linewidth=1, label=f'High Activity Days', color='C0', bins=bins)
    axes[0].hist(set(area_inactive), edgecolor='black', linewidth=1, label=f'Low Activity Days', color='C1', alpha=0.5, bins=bins)

    axes[1].hist(area_active_100, edgecolor='black', linewidth=1, color='C0', bins=bins)
    axes[1].hist(set(area_inactive_100), edgecolor='black', linewidth=1, color='C1', alpha=0.5, bins=bins)
    axes[1].set_xlabel('Area', fontsize=20, labelpad=20)
    axes[0].legend()
    for ax in axes:
        ax.set_ylabel(r'S(2, $\tau$)', fontsize=20, labelpad=20)
        #ax.grid()
        ax.tick_params(axis='both', which='major', labelsize=20)
        ax.legend(fontsize=20)
    fig.savefig(f'Structure_Function_Area_Histogram_{region}')


    fig, axes = plt.subplots(2, figsize=(12, 6), tight_layout=True, sharex=True)
    if region != 'All':
        axes[0].set_title(f'a) Area of Structure Function' + r'$\tau$=[1s, 10s] in ' + f' Region {region}', fontsize=20)
        axes[1].set_title(f'b) Area of Structure Function' + r'$\tau$=[10s, 100s] in ' + f' Region {region}', fontsize=20)
    else:
        axes[0].set_title(f'a) Area of Structure Function' + r'$\tau$=[1s, 10s] in ' + f'Polar Region', fontsize=20)
        axes[1].set_title(f'b) Area of Structure Function' + r'$\tau$=[10s, 100s] in ' + f'Polar Region', fontsize=20)
    axes[0].plot(area_active, label=f'High Activity Days', linewidth=4)
    axes[0].plot(area_inactive, label=f'Low Activity Days', linewidth=4)

    axes[1].plot(area_active_100, linewidth=4)
    axes[1].plot(area_inactive_100, linewidth=4)
    axes[0].legend()
    axes[1].set_xlabel('Instance', fontsize=20, labelpad=20)
    for ax in axes:
        ax.set_ylabel(r'S(2, $\tau$)', fontsize=20, labelpad=20)
        ax.grid()
        ax.tick_params(axis='both', which='major', labelsize=20)
        ax.legend(fontsize=14)
    fig.savefig(f'Structure_Function_Area_Alternate_{region}', dpi=100)


def get_slopes():
    """
    Plot slopes in histogram
    """
    bins = 10
    fig, axes = plt.subplots(2, 2, figsize=(9, 6), tight_layout=True, sharex=True, sharey=True)
    axes[0][0].set_title(r'a) High Activity Day $\tau$=' + f'[{n/16}s, {m/16}s] \n' + r'vs $\tau$=' + f'[{m/16}s, {j/16}s]', fontsize=14)
    axes[0][0].hist(active_slopes_m4_1_10, edgecolor='black', linewidth=1, label=f'tau=[1s, 10s]', color='C0', bins=bins)
    axes[1][0].hist(set(inactive_slopes_m4_1_10), edgecolor='black', linewidth=1, color='C0', bins=bins)  # https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset
    axes[1][0].set_title(r'c) Low Activity Day $\tau$=' + f'[{n/16}s, {m/16}s]\n' + r'vs $\tau$=' + f'[{m/16}s, {j/16}s]', fontsize=14)
    axes[0][0].hist(active_slopes_m4_10_100, edgecolor='black', linewidth=1, label=f'tau=[10s, 100s]', color='C1', alpha=0.5, bins=bins)
    axes[1][0].hist(set(inactive_slopes_m4_10_100), edgecolor='black', linewidth=1, color='C1', alpha=0.5, bins=bins)
    axes[0][0].legend()
    axes[0][1].set_title(f'b) High Activity Days vs Low Activity Days \n' + r'$\tau$ = ' + f'[{n/16}s, {m/16}s]', fontsize=14)
    axes[0][1].hist(active_slopes_m4_1_10, edgecolor='black', linewidth=1, color='C0', bins=bins, label='High Activity Days')
    axes[0][1].hist(set(inactive_slopes_m4_1_10), edgecolor='black', linewidth=1, color='C1', bins=bins, alpha=0.5, label='Low Activity Days')
    axes[1][1].set_title(f'd) High Activity Days vs Low Activity Days \n' + r'$\tau$ = ' + f'[{m/16}s, {j/16}s]', fontsize=14)
    axes[1][1].hist(active_slopes_m4_10_100, edgecolor='black', linewidth=1, label=f'tau=[10s, 100s]', color='C0', bins=bins)
    axes[1][1].hist(set(inactive_slopes_m4_10_100), edgecolor='black', linewidth=1, color='C1', bins=bins, alpha=0.5)
    axes[0][1].legend()
    axes[1][0].set_xlabel(r'Slope', fontsize=14, labelpad=20)
    axes[1][0].set_ylabel(r'Counts', fontsize=14, labelpad=20)
    for axy in axes:
        for ax in axy:
            ax.tick_params(axis='both', which='major', labelsize=10)
    fig.savefig(f'Histogram_{region}', dpi=100)

    fig, axes = plt.subplots(figsize=(12, 6), tight_layout=True, sharex=True, sharey=True)
    axes.plot(active_slopes_m2_1_10, color='C0', linewidth=2)
    axes.plot(active_slopes_m4_1_10, color='C0', linewidth=2, ls='dashed')
    axes.plot(inactive_slopes_m2_1_10, color='C1', linewidth=2)
    axes.plot(inactive_slopes_m4_1_10, color='C1', linewidth=2, ls='dashed')
    axes.plot(np.ones(len(active_slopes_m2_1_10)) * np.mean(active_slopes_m2_1_10), color='black', linewidth=2)
    axes.plot(np.ones(len(inactive_slopes_m2_1_10)) * np.mean(inactive_slopes_m2_1_10), color='black', linewidth=2, ls='dotted')
    axes.plot(np.ones(len(active_slopes_m4_1_10)) * np.mean(active_slopes_m4_1_10), color='black', linewidth=2)
    axes.plot(np.ones(len(inactive_slopes_m4_1_10)) * np.mean(inactive_slopes_m4_1_10), color='black', linewidth=2, ls='dotted')
    plt.grid()
    fig.savefig(f'Histogram_{region}', dpi=100)

def plotting_ef():
    """
    plots empirical flatness and area in histogram and as regular plot
    """
    area_active = []
    area_inactive = []

    area_active_100 = []
    area_inactive_100 = []

    bins = 10
    fig, axes = plt.subplots(2, 2, figsize=(12, 6), tight_layout=True)
    for x in range(len(active_ef)):
        active = active_ef[x][n:m]
        inactive = inactive_ef[x][n:m]
        active_100 = active_ef[x][m:j]
        inactive_100 = inactive_ef[x][m:j]
        if x == 1:
            axes[0, 0].plot(active_tau[x][n:m] / 16, active, color='C0', label=f'High Activity Days')
            axes[0, 0].plot(inactive_tau[x][n:m] / 16, inactive, color='C1', label=f'Low Activity Days')
            area_active.append(simpson(active, active_tau[x][n:m] / 16))
            area_inactive.append(simpson(inactive, inactive_tau[x][n:m] / 16))
            axes[0, 1].plot(active_tau[x][m:j] / 16, active_100, color='C0', label=f'High Activity Days')
            axes[0, 1].plot(inactive_tau[x][m:j] / 16, inactive_100, color='C1', label=f'Low Activity Days')
            area_active_100.append(simpson(active_100, active_tau[x][m:j] / 16))
            area_inactive_100.append(simpson(inactive_100, inactive_tau[x][m:j] / 16))
        else:
            axes[0, 0].plot(active_tau[x][n:m] / 16, active, color='C0')
            axes[0, 0].plot(inactive_tau[x][n:m] / 16, inactive, color='C1')
            area_active.append(simpson(active, active_tau[x][n:m] / 16))
            area_inactive.append(simpson(inactive, inactive_tau[x][n:m] / 16))
            axes[0, 1].plot(active_tau[x][m:j] / 16, active_100, color='C0')
            axes[0, 1].plot(inactive_tau[x][m:j] / 16, inactive_100, color='C1')
            area_active_100.append(simpson(active_100, active_tau[x][m:j] / 16))
            area_inactive_100.append(simpson(inactive_100, inactive_tau[x][m:j] / 16))
    axes[0, 0].plot(active_tau[x][n:m] / 16, np.ones(len(active_tau[x][n:m])) * 3, color='black', linewidth=2, ls='dashed', label=r'F($\tau$) = 3')
    axes[0, 1].plot(active_tau[x][m:j] / 16, np.ones(len(active_tau[x][m:j])) * 3, color='black', linewidth=2, ls='dashed')


    axes[1, 0].hist(area_active, edgecolor='black', linewidth=1, label=f'Active Day {region}', color='C0', bins=bins)
    axes[1, 0].hist(area_inactive, edgecolor='black', linewidth=1, label=f'Inactive Day {region}', color='C1', alpha=0.5, bins=bins)
    axes[1, 1].hist(area_active_100, edgecolor='black', linewidth=1, label=f'Active Day {region}', color='C0', bins=bins)
    axes[1, 1].hist(area_inactive_100, edgecolor='black', linewidth=1, label=f'Inactive Day {region}', color='C1', alpha=0.5, bins=bins)
    axes[0, 0].set_xscale('log')
    axes[0, 1].set_xscale('log')
    axes[0, 0].grid()
    if region != 'All':
        axes[1, 0].set_title(f'c) Area in Region {region} \n' + r'for $\tau$=' + f'[{n/16}s, {m/16}s]', fontsize=15)
        axes[0, 0].set_title(f'a) Empirical Flatness in Region {region}\n' + r'for $\tau$=' + f'[{n/16}s, {m/16}s]', fontsize=17)
        axes[1, 1].set_title(f'd) Area in Region {region} \n' + r'for $\tau$=' + f'[{n/16}s, {m/16}s]', fontsize=15)
        axes[0, 1].set_title(f'b) Empirical Flatness in Region {region}\n' + r'for $\tau$=' + f'[{m/16}s, {j/16}s]', fontsize=17)
    else:
        axes[1, 0].set_title(f'c) Area in Polar Region \n' + r'for $\tau$=' + f'[{n/16}s, {m/16}s]', fontsize=15)
        axes[0, 0].set_title(f'a) Empirical Flatness in Region {region}\n' + r'for $\tau$=' + f'[{n/16}s, {m/16}s]', fontsize=17)
        axes[1, 1].set_title(f'd) Area in Polar Region \n' + r'for $\tau$=' + f'[{n/16}s, {m/16}s]', fontsize=15)
        axes[0, 1].set_title(f'b) Empirical Flatness in Region {region}\n' + r'for $\tau$=' + f'[{m/16}s, {j/16}s]', fontsize=17)
    axes[0, 0].set_ylabel(r'S(4, $\tau$) / S²(2, $\tau$)', fontsize=14)
    axes[0, 0].set_xlabel(r'$\tau$ (seconds)', fontsize=14)
    axes[0, 1].set_xlabel(r'$\tau$ (seconds)', fontsize=14)
    axes[1, 0].set_ylabel('Counts', fontsize=14)
    axes[1, 0].set_xlabel('Area', fontsize=14, labelpad=20)
    axes[1, 1].set_xlabel('Area', fontsize=14, labelpad=20)
    for axy in axes:
        for ax in axy:
            ax.tick_params(axis='both', which='major', labelsize=14)
    axes[0, 0].legend(fontsize=11)
    fig.savefig(f'Empirical_Flatness_and_Histogram_{region}')

    fig, axes = plt.subplots(2, figsize=(9, 6), tight_layout=True, sharex=True)
    if region != 'All':
        axes[0].set_title(r'a) Area of Empirical Flatness, ' + f'[{n/16}s, {m/16}s] of ' + f'Region {region}', fontsize=18)
        axes[1].set_title(r'b) Area of Empirical Flatness, ' + f'[{m/16}s, {j/16}s] of ' + f'Region {region}', fontsize=18)
    else:
        axes[0].set_title(f'a) Area of Empirical Flatness, [{n/16}s, {m/16}s] of Polar Region', fontsize=18)
        axes[1].set_title(f'b) Area of Empirical Flatness, [{m / 16}s, {j / 16}s] of Polar Region', fontsize=18)
    axes[0].plot(area_active, label=f'High Activity Days', linewidth=4)
    axes[0].plot(area_inactive, label=f'Low Activity Days', linewidth=4)
    axes[1].plot(area_active_100, linewidth=4)
    axes[1].plot(area_inactive_100, linewidth=4)
    axes[0].legend()
    axes[1].set_xlabel('Instance', fontsize=20, labelpad=20)
    axes[0].plot(np.ones(len(area_active)) * np.mean(area_active), color='C0', ls='dotted', linewidth=4, label='High Mean')
    axes[0].plot(np.ones(len(area_inactive)) * np.mean(area_inactive), color='C1', ls='dotted', linewidth=4, label='Low Mean')
    axes[1].plot(np.ones(len(area_active_100)) * np.mean(area_active_100), color='C0', ls='dotted', linewidth=4)
    axes[1].plot(np.ones(len(area_inactive_100)) * np.mean(area_inactive_100), color='C1', ls='dotted', linewidth=4)
    for ax in axes:
        ax.set_ylabel(r'S(4, $\tau$) / S²(2, $\tau$)', fontsize=16, labelpad=20)
        ax.grid()
        ax.tick_params(axis='both', which='major', labelsize=20)
        ax.legend(fontsize=12)
    fig.savefig(f'Empirical_Fatness_Area_Alternate_{region}', dpi=100)


# Calculates regression at intervals
ga1 = linregress(np.log10(active_tau[i][n:m].astype(float)), active_sf_m2[i][n:m].astype('float'))
ga2 = linregress(np.log10(active_tau[i][m:j].astype(float)), active_sf_m2[i][m:j].astype('float'))
#ga3 = linregress(np.log10(active_tau[i][j:k].astype(float)), active_sf_m2[i][j:k].astype('float'))
gi1 = linregress(np.log10(inactive_tau[i][n:m].astype(float)), inactive_sf_m2[i][n:m].astype('float'))
gi2 = linregress(np.log10(inactive_tau[i][m:j].astype(float)), inactive_sf_m2[i][m:j].astype('float'))
#gi3 = linregress(np.log10(inactive_tau[i][j:k].astype(float)), inactive_sf_m2[i][j:k].astype('float'))



fig, axes = plt.subplots(figsize=(9, 6), tight_layout=True)


#Set either of the if blocks to true to plot empirical flatness or strucutre function for specific case
if True:
    #axes.plot(active_tau[d][1:m] / 16, active_ef[d][1:m], color='C0', linewidth=4, label=f'High Activity Day')
    #axes.plot(inactive_tau[d][1:m] / 16, inactive_ef[d][1:m], color='C1', linewidth=4, label=f'Low Activity Day')
    axes.plot(active_tau[d][m:j] / 16, active_ef[d][m:j], color='C0', linewidth=4)
    axes.plot(inactive_tau[d][m:j] / 16, inactive_ef[d][m:j], color='C1', linewidth=4)
    #axes.plot(active_tau[d][j:-1] / 16, active_ef[d][j:-1], color='C0', linewidth=4)
    #axes.plot(inactive_tau[d][j:-1] / 16, inactive_ef[d][j:-1], color='C1', linewidth=4)
    #axes.plot(active_tau[d] / 16, np.ones(len(active_tau[d])) * 3, color='black', linewidth=2, ls='dashed', label=r'S(4, $\tau$) / S²(2, $\tau$) = 3')
    axes.set_ylabel(r'S(4, $\tau$) / S²(2, $\tau$)', fontsize=20, labelpad=20)

if False:
    axes.plot(active_tau[d][n:m] / 16, active_sf_m2[d][n:m], color='C0', linewidth=4, label=f'High Activity Day M2')
    axes.plot(inactive_tau[d][n:m] / 16, inactive_sf_m2[d][n:m], color='C1', linewidth=4, label=f'Low Activity Day M2')
    axes.plot(active_tau[d][m:j] / 16, active_sf_m2[d][m:j], color='C0', linewidth=4)
    axes.plot(inactive_tau[d][m:j] / 16, inactive_sf_m2[d][m:j], color='C1', linewidth=4)
    axes.plot(active_tau[d][j:k] / 16, active_sf_m2[d][j:k], color='C0', linewidth=4)
    axes.plot(inactive_tau[d][j:k] / 16, inactive_sf_m2[d][j:k], color='C1', linewidth=4)

    axes.plot(active_tau[d][k:-1] / 16, active_sf_m2[d][k:-1], color='C0', linewidth=4)
    axes.plot(inactive_tau[d][k:-1] / 16, inactive_sf_m2[d][k:-1], color='C1', linewidth=4)

    #axes.plot(active_tau[d][n:m] / 16, ga1.intercept + ga1.slope * np.log10(active_tau[d][n:m].astype(float)), color='black', linewidth=4, ls='dashed')
    #axes.plot(inactive_tau[d][n:m] / 16, gi1.intercept + gi1.slope * np.log10(inactive_tau[d][n:m].astype(float)), color='black', linewidth=4, ls='dashed')
    #axes.plot(active_tau[d][m:j] / 16, ga2.intercept + ga2.slope * np.log10(active_tau[d][m:j].astype(float)), color='black', linewidth=4, ls='dashed')
    #axes.plot(inactive_tau[d][m:j] / 16, gi2.intercept + gi2.slope * np.log10(inactive_tau[d][m:j].astype(float)), color='black', linewidth=4, ls='dashed')
    #axes.plot(active_tau[d][j:k] / 16, ga3.intercept + ga3.slope * np.log10(active_tau[d][j:k].astype(float)), color='black', linewidth=4, ls='dashed')
    #axes.plot(inactive_tau[d][j:k] / 16, gi3.intercept + gi3.slope * np.log10(inactive_tau[d][j:k].astype(float)), color='black', linewidth=4, ls='dashed')

    axes.plot(active_tau[d][n:m] / 16, active_sf_m4[d][1:m], color='C2', linewidth=4, label=f'High Activity Day M4')
    axes.plot(inactive_tau[d][n:m] / 16, inactive_sf_m4[d][1:m], color='C3', linewidth=4, label=f'Low Activity Day M4')
    axes.plot(active_tau[d][m:j] / 16, active_sf_m4[d][m:j], color='C2', linewidth=4)
    axes.plot(inactive_tau[d][m:j] / 16, inactive_sf_m4[d][m:j], color='C3', linewidth=4)
    axes.plot(active_tau[d][j:k] / 16, active_sf_m4[d][j:-1], color='C2', linewidth=4)
    axes.plot(inactive_tau[d][j:k] / 16, inactive_sf_m4[d][j:-1], color='C3', linewidth=4)
    """correction_active = np.abs(np.log10((active_tau[d][1] / 16) ** (2 / 3)))
    correction_inactive = np.abs(np.log10((inactive_tau[d][1] / 16) ** (2 / 3)))
    scaling_active = np.log10((active_tau[d][1:n] / 16) ** (2 / 3)) + correction_active + active_sf_m2[d][1]
    scaling_inactive = np.log10((inactive_tau[d][1:n] / 16)**(2 / 3)) + correction_inactive + inactive_sf_m2[d][1]
    axes.plot(active_tau[d][1:n] / 16, scaling_active, color='black', ls='dashed', linewidth=2, label=r'Power Law = $\tau^\frac{2}{3}$')
    axes.plot(inactive_tau[d][1:n] / 16, scaling_inactive, color='black', ls='dashed', linewidth=2)
    axes.set_ylabel(r'S(2, $\tau$)', fontsize=20, labelpad=20)"""

if region != 'All':
    axes.set_title(f'Empirical Flatness of Region {region}', fontsize=24)
    axes.set_title(f'Structure Function of Region {region} for m=2', fontsize=24)
else:
    axes.set_title(r'Structure Function of Polar Region for m=2', fontsize=24)
    axes.set_title(r'Empirical Flatness of Polar Region', fontsize=24)

axes.set_xscale('log')
axes.grid()
axes.set_xlabel(r'$\tau$ (seconds)', fontsize=20, labelpad=20)
axes.tick_params(axis='both', which='major', labelsize=20)
axes.legend(fontsize=14)
fig.savefig('test')

get_slopes()
