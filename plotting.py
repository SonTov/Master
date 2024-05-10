import matplotlib.pyplot as plt


def plot_ne_and_fac(data, name, target=False, polar_region='all'):
    fig, axes = plt.subplots(2, figsize=(12, 8), tight_layout=True, sharex=True)
    if not target:
        axes[0].plot(data['Timestamp_16Hz'], data['Density_Full'])  #, label='Ne'
        axes[1].plot(data['Timestamp_FAC'], data['FAC_Full'])  #, label='FAC'

    if isinstance(data['FAC'], dict):
        if polar_region == 'A' or polar_region == 'AC' or polar_region == 'AB' or polar_region == 'all':
            axes[0].plot(data['Timestamp_16Hz'], data['Density']['A'], label='A')
            axes[1].plot(data['Timestamp_FAC'], data['FAC']['A'], label='B')
        if polar_region == 'B' or polar_region == 'AB' or polar_region == 'BC' or polar_region == 'all':
            axes[0].plot(data['Timestamp_16Hz'], data['Density']['B'], label='B')
            axes[1].plot(data['Timestamp_FAC'], data['FAC']['B'], label='B')
        if polar_region == 'C' or polar_region == 'AC' or polar_region == 'BC' or polar_region == 'all':
            axes[0].plot(data['Timestamp_16Hz'], data['Density']['C'], label='C')
            axes[1].plot(data['Timestamp_FAC'], data['FAC']['C'], label='C')

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
    axes[0].plot(data['tau'] / 16, data['B/A'], label=f'{keyword} S({m}, {tau_interval}) B/A')
    axes[1].plot(data['tau'] / 16, data['B/C'], label=f'{keyword} S({m}, {tau_interval}) B/C')
    axes[2].plot(data['tau'] / 16, data['A/C'], label=f'{keyword} S({m}, {tau_interval}) A/C')
    for ax in axes:
        ax.grid()
        ax.set_xscale('log')
        ax.legend()
        if limit:
            ax.set_ylim(0, limit)


def plot_power_spectral_density(data, fig, axes, label='', p_value=False):
    psd = data['power_spectral_density']
    frequency = data['frequency']
    axes.plot(frequency, psd, label=label)
    if p_value:
        p = data['slope']
        print(f'p value = {p}')
        axes.plot(frequency, data['regression'], ls='dotted', c='black')
    axes.set_xscale('log')
    axes.set_xlabel('Frequency (Hz)')
    axes.set_ylabel('P(f)/(Hz)')
    axes.legend()
    fig.tight_layout()
