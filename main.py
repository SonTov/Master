import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress, gaussian_kde
from scipy.integrate import simps

region = 'All'

active_directory = f'Active_{region}_files_North'
inactive_directory = f'Inactive_{region}_files_North'

n = 1 * 16
m = 10 * 16

dates = []

active_slopes_m2 = []
inactive_slopes_m2 = []

active_slopes_m4 = []
inactive_slopes_m4 = []

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
                active_g_m2 = linregress(np.log10(active_dataset.index[n:m].astype(float)), active_dataset['structure_function_M2'][n:m].astype('float'))
                active_slopes_m2.append(active_g_m2.slope)
                active_g_m4 = linregress(np.log10(active_dataset.index[n:m].astype(float)), active_dataset['structure_function_M4'][n:m].astype('float'))
                active_slopes_m4.append(active_g_m4.slope)


            except ValueError:
                pass
            try:
                inactive_g_m2 = linregress(np.log10(inactive_dataset.index[n:m].astype(float)), inactive_dataset['structure_function_M2'][n:m].astype('float'))
                inactive_slopes_m2.append(inactive_g_m2.slope)
                inactive_g_m4 = linregress(np.log10(inactive_dataset.index[n:m].astype(float)), inactive_dataset['structure_function_M4'][n:m].astype('float'))
                inactive_slopes_m4.append(inactive_g_m4.slope)
            except ValueError:
                pass

def plotting(same_slope, m):
    area_active = []
    area_inactive = []
    maximas_active = []
    maximas_inactive = []
    fig, axes = plt.subplots(figsize=(12, 8), tight_layout=True)
    if same_slope:
        m = int(np.min([len(inactive_sf_m2[x]) for x in range(len(inactive_sf_m2))]))
    for x in range(len(active_sf_m2)):
        active_tau_ = active_tau[x][n:m]
        inactive_tau_ = inactive_tau[x][n:m]

        if x == len(active_sf_m2) - 1:
            axes.plot(active_tau[x][n:m] / 16, active_sf_m2[x][n:m], label='structure function active', color='C0')
            axes.plot(inactive_tau[x][n:m] / 16, inactive_sf_m2[x][n:m], label='structure function inactive', color='C1')
            axes.legend()
        else:
            axes.plot(active_tau[x][n:m] / 16, active_sf_m2[x][n:m], color='C0')
            axes.plot(inactive_tau[x][n:m] / 16, inactive_sf_m2[x][n:m], color='C1')

        area_active.append(simps(active_sf_m2[x][n:m], active_tau[x][n:m] / 16))
        area_inactive.append(simps(inactive_sf_m2[x][n:m], inactive_tau[x][n:m] / 16))
        axes.set_xscale('log')
        axes.grid()
        axes.set_title(f'Structure Function and Maxima {region} [{int(n/16)}, {int(m/16)}]')
        a = active_sf_m2[x][n:m]
        b = inactive_sf_m2[x][n:m]
        maxima_active = np.argmax(a)
        maxima_inactive = np.argmax(b)
        maximas_active.append(active_tau_[maxima_active] / 16)
        maximas_inactive.append(inactive_tau_[maxima_inactive] / 16)
        axes.scatter(active_tau_[maxima_active] / 16, a[maxima_active], color='C0')
        axes.scatter(inactive_tau_[maxima_inactive] / 16, b[maxima_inactive], color='C1')
    fig.savefig(f'Structure_Function_{region}_{int(n/16)}_{int(m/16)}')

    fig, axes = plt.subplots(figsize=(12, 8), tight_layout=True)
    axes.scatter(np.zeros(len(area_active)), area_active, label='Active')
    axes.scatter(np.zeros(len(area_inactive)), area_inactive, label='Inactive')
    axes.legend()
    axes.set_title(f'Structure Function Area {region} [{int(n/16)}, {int(m/16)}]')
    fig.savefig(f'Structure_Function_Area_{region}_{int(n/16)}_{int(m/16)}')

    fig, axes = plt.subplots(figsize=(12, 8), tight_layout=True)
    axes.set_title(f'Structure Function Area {region} [{int(n/16)}, {int(m/16)}]')
    axes.plot(area_active, label='Active')
    axes.plot(area_inactive, label='Active')
    axes.legend()
    fig.savefig(f'Structure_Function_Area_Alternate_{region}_{int(n/16)}_{int(m/16)}')

def get_slopes(same_slope, m, remove_small_tau=False):
    if same_slope:
        m_active = int(np.min([len(active_sf_m2[x]) for x in range(len(active_sf_m2))]))
        m_inactive = int(np.min([len(inactive_sf_m2[x]) for x in range(len(inactive_sf_m2))]))
        m = np.min([m_active, m_inactive])
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html
    # https://numpy.org/doc/stable/reference/generated/numpy.histogram.html
    bins = 'auto'

    if remove_small_tau:
        for x in range(len(active_sf_m2)):
            print(len(active_sf_m2[x]) / 16)
            print(len(inactive_sf_m2[x]) / 16)
            if len(inactive_sf_m2[x]) / 16 < 50:
                active_slopes_m2[x] = np.NaN
                inactive_slopes_m2[x] = np.NaN
            print(len(active_sf_m4[x]) / 16)
            print(len(inactive_sf_m4[x]) / 16)
            if len(inactive_sf_m4[x]) / 16 < 50:
                active_slopes_m4[x] = np.NaN
                inactive_slopes_m4[x] = np.NaN

    fig, axes = plt.subplots(2, figsize=(12, 8), tight_layout=True, sharex=True, sharey=True)
    axes[0].set_title(f'M2  tau interval=[{n/16}, {m/16}]')
    axes[0].hist(active_slopes_m2, edgecolor='black', linewidth=1, label=f'Active Day {region}', color='C0', bins=bins)
    axes[0].hist(set(inactive_slopes_m2), edgecolor='black', linewidth=1, label=f'Inactive Day {region}', color='C1', alpha=0.4, bins=bins)  # https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset
    axes[1].set_title(f'M4  tau interval=[{n/16}, {m/16}]')
    axes[1].hist(active_slopes_m4, edgecolor='black', linewidth=1, color='C0', bins=bins)
    axes[1].hist(set(inactive_slopes_m4), edgecolor='black', linewidth=1, color='C1', alpha=0.4, bins=bins)
    axes[1].set_xlabel('Slope')
    axes[0].legend()
    fig.savefig(f'Histogram_{region}_{int(n/16)}_{int(m/16)}')


def plotting_ef():
    area_active = []
    area_inactive = []
    fig, axes = plt.subplots(2, figsize=(12, 8), tight_layout=True)
    for x in range(len(active_sf_m2)):
        active = active_ef[x][n:m]
        inactive = inactive_ef[x][n:m]
        axes[0].plot(active_tau[x][n:m] / 16, active, color='C0')
        axes[0].plot(inactive_tau[x][n:m] / 16, inactive, color='C1')
        area_active.append(simps(active, active_tau[x][n:m] / 16))
        area_inactive.append(simps(inactive, inactive_tau[x][n:m] / 16))
        axes[1].scatter(0, simps(active, active_tau[x][n:m] / 16), color='C0')
        axes[1].scatter(0, simps(inactive, inactive_tau[x][n:m] / 16), color='C1')
    axes[0].set_xscale('log')
    axes[0].grid()
    axes[0].set_title(f'Empirical Flatness {region} [{int(n/16)}, {int(m/16)}]')
    axes[1].set_title(f'Empirical Flatness Area {region} [{int(n/16)}, {int(m/16)}]')
    fig.savefig(f'Empirical_Flatness_{region}_{int(n/16)}_{int(m/16)}')

    bins = 'auto'

    fig, axes = plt.subplots(figsize=(12, 8), tight_layout=True)
    axes.set_title(f'M2  tau interval=[{n / 16}, {m / 16}]')
    axes.hist(area_active, edgecolor='black', linewidth=1, label=f'Active Day {region}', color='C0', bins=bins)
    axes.hist(area_inactive, edgecolor='black', linewidth=1, label=f'Inactive Day {region}', color='C1', alpha=0.4, bins=bins)
    axes.legend()
    axes.set_title(f'Empirical Flatness Area {region} [{int(n/16)}, {int(m/16)}]')
    fig.savefig(f'Histogram_Empirical_Flatness_{region}_{int(n / 16)}_{int(m / 16)}')

inactive_ = []
for x in range(len(active_ef)):
    active = active_ef[x][n:m]
    inactive = inactive_ef[x][n:m]

    inactive_.append(np.mean(inactive))
    #plt.plot(active_tau[x][n:m] / 16, active_ef[x][n:m], color='C0')
    #plt.plot(inactive_tau[x][n:m] / 16, inactive_ef[x][n:m], color='C1')
    #plt.xscale('log')

    #plt.scatter(0, inactive_)

idx = int(np.arange(0, len(inactive_))[inactive_ == np.max(inactive_)])

plt.plot(inactive_tau[idx][n:m] / 16, active_sf_m4[idx][n:m])
plt.plot(inactive_tau[idx][n:m] / 16, inactive_sf_m2[idx][n:m])
plt.xscale('log')
plt.yscale('log')
plt.show()
print(dates[idx])
#inactive_ef
#plotting(False, m)
#get_slopes(False, m, False)
#plotting_ef()

# hist_freq, bin_edges_active = np.histogram(active_slopes_m2, bins=bins, density=False)
# hist_freq2, bin_edges_inactive = np.histogram(inactive_slopes_m2, bins=bins, density=False)

# bin_width_active = np.diff(bin_edges_active)[0]
# scaling_factor_active = len(active_slopes_m2) * bin_width_active

# bin_width_inactive = np.diff(bin_edges_inactive)[0]
# scaling_factor_inactive = len(inactive_slopes_m2) * bin_width_inactive

# kde_active = gaussian_kde(active_slopes_m2, bw_method=0.25)
# x_range_active = np.linspace(min(active_slopes_m2), max(active_slopes_m2), 1000)
# kde_values_active = kde_active(x_range_active) * scaling_factor_active

# kde_inactive = gaussian_kde(inactive_slopes_m2, bw_method=0.25)
# x_range_inactive = np.linspace(min(inactive_slopes_m2), max(inactive_slopes_m2), 1000)
# kde_values_inactive = kde_inactive(x_range_inactive) * scaling_factor_inactive

"""plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(x_range_active, kde_values_active, label='KDE Active')
plt.hist(active_slopes_m2, bins=bins, density=False, alpha=0.5, label='Histogram Active', edgecolor='black')
plt.hist(inactive_slopes_m2, bins=bins, density=False, alpha=0.5, label='Histogram Inactive', edgecolor='black')
plt.plot(x_range_inactive, kde_values_inactive, label='KDE Inactive')
plt.legend()
plt.show()"""

"""import seaborn as sns

plt.subplot(1, 2, 2)
sns.kdeplot(active_slopes_m2, bw_adjust=0.5, fill=True, label='KDE Active')
sns.kdeplot(inactive_slopes_m2, bw_adjust=0.5, fill=True, label='KDE Inactive')
plt.legend()
plt.tight_layout()
plt.show()


active_slopes_m2 = active_ef[0][n:m]
inactive_slopes_m2 = inactive_ef[0][n:m]
print(len(active_slopes_m2))
print(active_slopes_m2)
print(sp.fft.fft(active_slopes_m2))

for tau, sf in zip(active_tau, active_sf_m2):
    #plt.plot(tau[n:m] / 16, sf[n:m], color='C0')
    g = linregress(np.log10(tau[n:m].astype(float)), sf[n:m].astype('float'))
    plt.plot(tau[n:m] / 16, g.intercept + g.slope * np.log10(tau[n:m].astype(float)), ls='dotted', color='C2')
for tau, sf in zip(inactive_tau, inactive_sf_m2):
    #plt.plot(tau[n:m] / 16, sf[n:m], color='C1')
    g = linregress(np.log10(tau[n:m].astype(float)), sf[n:m].astype('float'))
    plt.plot(tau[n:m] / 16, g.intercept + g.slope * np.log10(tau[n:m].astype(float)), ls='dotted', color='C3')
plt.xscale('log')
plt.grid()
plt.show()

for tau_a, sf_a, tau_ia, sf_ia in zip(active_tau, active_sf_m2, inactive_tau, inactive_sf_m2):
    new_length = len(tau_a[n:]) - len(tau_ia[n:])
    a = tau_a[n:] / 16
    b = sf_a[n:]
    c = tau_ia[n:] / 16
    d = sf_ia[n:]

    if len(tau_a[n:]) - len(tau_ia[n:]) > 0:
        new_length = len(tau_a[n:]) - len(tau_ia[n:])
        a = tau_a[n+new_length:] / 16
        b = sf_a[n+new_length:]
    elif len(tau_ia[n:]) - len(tau_a[n:]) > 0:
        new_length = len(tau_ia[n:]) - len(tau_a[n:])
        c = tau_ia[n+new_length:] / 16
        d = sf_ia[n+new_length:]

    #plt.scatter(0, np.mean(b / d), color='black')
    plt.scatter(0, np.mean(b), color='C1')
    plt.scatter(0, np.mean(d), color='C2')
    #plt.plot(a, d, color='C1')
#plt.xscale('log')
plt.grid()
plt.show()

a = sp.fft.rfft(active_slopes_m2)[0:]
b = sp.fft.rfft(inactive_slopes_m2)[0:]

#a2 = np.insert(a, 0, 0, axis=None)
#b2 = np.insert(b, 0, 0, axis=None)

plt.plot(a)
plt.plot(b)
plt.xscale('log')
plt.yscale('log')
plt.show()
"""