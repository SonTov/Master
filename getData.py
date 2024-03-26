import os

os.environ["CDF_LIB"] = '/home/sondre/.local/lib'
from spacepy import pycdf
import numpy as np


class GetData:
    def __init__(self, start_time, stop_time, measured_data='FAC'):
        self.start_time = start_time
        self.stop_time = stop_time
        main_directory = 'swarm_data'
        sub_directory = start_time.strftime('%Y%m%d')
        file_path = os.path.join(main_directory, sub_directory)
        for f in os.listdir(file_path):
            if 'EXTD' in f:
                plasma_density = f
            elif 'OPER' in f:
                fac = f
        if measured_data == 'Ne':
            filename = os.path.join(file_path, plasma_density)
        elif measured_data == 'FAC':
            filename = os.path.join(file_path, fac)
        self.cdf = pycdf.CDF(filename)
        try:
            self.timestamp = self.cdf['Timestamp'][:]
        except KeyError:
            print('Error: No timestamp')

    def get_info(self):
        print(self.cdf)
        return

    def time(self, arr=None):
        if arr is None:
            arr = self.timestamp
        idx = np.where((self.start_time <= arr) & (arr <= self.stop_time))[0]
        dict_data = {}
        for key in self.cdf.keys():
            dict_data[key] = self.cdf[key][:][idx]
        return dict_data
