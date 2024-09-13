import matplotlib.pyplot as plt
import numpy as np


def plot_ne_and_fac_(data, name, target=False, polar_region='all'):
    """
    plots electron density and
    field-aligned currents

    :param data: (dictionary)
    :param name: (string)
    :param target: entire region or just specified polar region (boolean)
    :param polar_region: if target is True,
    can choose one or more subregions
    (region A, B, C) (string)
    :return: figure
    """
    fig, axes = plt.subplots(2, figsize=(9, 6), tight_layout=True, sharex=True)
    if not target:
        axes[0].plot(data['Timestamp_16Hz'], data['Density_Full'])
        axes[1].plot(data['Timestamp_FAC'], data['FAC_Full'])

    if isinstance(data['FAC'], dict):
        if polar_region == 'A' or polar_region == 'AC' or polar_region == 'AB' or polar_region == 'all':
            axes[0].plot(data['Timestamp_16Hz'], data['Density']['A'], label='A')
            axes[1].plot(data['Timestamp_FAC'], data['FAC']['A'])
        if polar_region == 'B' or polar_region == 'AB' or polar_region == 'BC' or polar_region == 'all':
            axes[0].plot(data['Timestamp_16Hz'], data['Density']['B'], label='B')
            axes[1].plot(data['Timestamp_FAC'], data['FAC']['B'])
        if polar_region == 'C' or polar_region == 'AC' or polar_region == 'BC' or polar_region == 'all':
            axes[0].plot(data['Timestamp_16Hz'], data['Density']['C'], label='C')
            axes[1].plot(data['Timestamp_FAC'], data['FAC']['C'])

    else:
        axes[0].plot(data['Timestamp_16Hz'], data['Density'], label='Polar Region')
        axes[1].plot(data['Timestamp_FAC'], data['FAC'], label='Polar Region')

    for ax in axes:
        ax.grid()
        ax.legend()
    axes[0].set_title('a) Plasma Density', fontsize=16)
    axes[0].set_ylabel('$cm^{-3}$', fontsize=14)
    axes[1].set_xlabel('Time', fontsize=14)
    axes[1].set_ylabel('μA/$m^2$', fontsize=14)
    axes[1].set_title('b) Field-Aligned Current', fontsize=16)
    fig.savefig(f'{name}')
    plt.close(fig)


def plot_structure_function(data, m, axes, tau_interval='tau', keyword=''):
    """
    Commented out scaling exponent plot

    :param data: (dictionary)
    :param m: m-th order (tuple or int)
    :param axes: as in fig, axes = plt.subplots()
    :param tau_interval: for labeling (string)
    :param keyword: for labeling (string)
    :return: figure
    """
    if isinstance(m, tuple):
        for elem in m:
            axes[0].plot(data['tau'], data['structure_function'][elem], label=f'S({elem}, {tau_interval}) {keyword}')
            axes[0].plot(data['tau'], data['regression'][elem], ls='dotted', c='black')
            # axes[2].scatter(m, data['slope'][elem], label=f'm = {elem}')
            slope = data['slope'][elem]
            print(f'Slope = {slope}')

    elif isinstance(m, int):
        axes[0].plot(data['tau'], data['structure_function'][m], label=f'{keyword} S({m}, {tau_interval}) {keyword}')
        axes[0].plot(data['tau'], data['regression'][m], ls='dotted', c='black')
        #axes[2].scatter(m, data['slope'][m], label=f'm = {m}')
        slope = data['slope'][m]
        print(f'Slope = {slope}')

    axes[0].legend(bbox_to_anchor=(1.0, 1.0), prop={'size': 6})
    axes[0].legend(prop={'size': 6})
    axes[0].set_xscale('log')

    axes[1].plot(data['tau'], data['empirical_flatness'])
    axes[1].set_xscale('log')


def plot_structure_function_ratios(data, m, axes, limit=False, tau_interval='tau', keyword=''):
    """

    :param data: (dictionary)
    :param m: m-th order (tuple or int)
    :param axes: as in fig, axes = plt.subplots()
    :param limit: optional tuple if axes should be shared (tuple)
    :param tau_interval: for labeling (string)
    :param keyword: for labeling (string)
    :return:
    """
    axes[0].plot(data['tau'] / 16, data['B/A'], label=f'{keyword} S({m}, {tau_interval}) B/A')
    axes[1].plot(data['tau'] / 16, data['B/C'], label=f'{keyword} S({m}, {tau_interval}) B/C')
    axes[2].plot(data['tau'] / 16, data['A/C'], label=f'{keyword} S({m}, {tau_interval}) A/C')
    for ax in axes:
        ax.grid()
        ax.set_xscale('log')
        ax.legend()
        if limit:
            ax.set_ylim(0, limit)


def plot_power_spectral_density(data, fig, axes, label='', region='all', p_value=False, color='C0', dt='', inertial_sub_range=False):
    """

    :param data: (dictionary)
    :param fig: as in fig, axes = plt.subplots()
    :param axes: as in fig, axes = plt.subplots()
    :param label: (string)
    :param region: Either region A, B, C or All (string)
    :param p_value: displays p value of regression (boolean)
    :param color: (string)
    :param dt: displays dt if used (int)
    :param inertial_sub_range: fits kolmogorov scaling exponent k⁻⁵/³ (boolean)
    :return:
    """
    psd = data['power_spectral_density']
    frequency = data['frequency']
    if region == 'all':
        axes.set_title(f'Power Spectral Density in Polar Region', fontsize=24)
    else:
        axes.set_title(f'Power Spectral Density in Region {region}, dt={dt}s', fontsize=24)
    if inertial_sub_range:
        axes.plot(frequency, np.log10(frequency**(5 / 3)) * psd, label=label, color=color)
    else:
        axes.plot(frequency, psd, label=label, color=color)
        correction = - np.log10(np.abs(frequency**(-5 / 3)))[0]
        axes.plot(frequency, np.log10(frequency**(-5 / 3)) + correction + np.abs(psd[0]), label=r'k^{-5/3}', color='black')
        if p_value:
            p_1 = data['slope'][0]
            p_2 = data['slope'][1]
            print(f'1st p value = {p_1}')
            print(f'2nd p value = {p_2}')
            axes.plot(frequency[:len(data['regression'][0])], data['regression'][0], ls='dotted', c='black')
            axes.plot(frequency[len(data['regression'][0]):], data['regression'][1], ls='dotted', c='black')
    axes.set_xscale('log')
    axes.set_xlabel('Frequency (Hz)', fontsize=20, labelpad=20)
    axes.set_ylabel('P(f)/(Hz)', fontsize=20, labelpad=20)
    axes.set_xlim(1E-1, 1E1)
    axes.tick_params(axis='both', which='major', labelsize=20)
    axes.legend(fontsize=20)
    fig.tight_layout()
