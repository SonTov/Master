from datetime import datetime


def load_day(year, month, day, instance, merged_region):

    dataset = {}

    if year == 2014 and month == 11 and day == 4:
        time_interval_start = 6
        time_interval_stop = 18
        day_inactive = 3
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (10, 11), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (11, 12), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1, "region_num": (8, 9), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (9, 10), 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (18, 19), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (19, 20), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1.2, "region_num": (16, 17), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (17, 18), 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (22, 23), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (23, 24), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1, "region_num": (20, 21), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (21, 22), 'total_region': merged_region}

    if year == 2014 and month == 12 and day == 7:
        time_interval_start = 12
        time_interval_stop = 18
        day_inactive = 6
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (2, 3), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 3, "threshold": 3, "region_num": (5, 6), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 2, "region_num": (1, 2), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 3, "threshold": 0.5, "region_num": 2, 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (5, 6), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 3, "threshold": 3, "region_num": (8, 9), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 6, "region_num": (5, 6), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 3, "threshold": 2, "region_num": 5, 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (8, 9), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 3, "threshold": 3, "region_num": (12, 13), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 3, "region_num": (9, 10), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 3, "threshold": 2, "region_num": (8, 9), 'total_region': merged_region}

    if year == 2015 and month == 11 and day == 7:
        time_interval_start = 4
        time_interval_stop = 18
        day_inactive = 2
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (4, 5), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (4, 5), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 10, "threshold": 5, "region_num": (4, 5), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 2, "region_num": (2, 3), 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.4, "region_num": (8, 9), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (7, 8), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 2, "region_num": (6, 7), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 1, "region_num": (7, 8), 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.4, "region_num": (11, 12), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (10, 11), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 2, "region_num": (10, 11), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": 9, 'total_region': merged_region}

    if year == 2015 and month == 11 and day == 8:
        time_interval_start = 10
        time_interval_stop = 18
        day_inactive = 12
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (8, 9), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (5, 6), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (6, 7), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (3, 4), 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (12, 13), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (9, 10), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (10, 11), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (7, 8), 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (16, 17), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (13, 14), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (14, 15), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (11, 12), 'total_region': merged_region}

    if year == 2015 and month == 11 and day == 9:
        time_interval_start = 6
        time_interval_stop = 18
        day_inactive = 12
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (16, 17), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (13, 14), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (14, 15), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (11, 12), 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (20, 21), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (17, 18), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (18, 19), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (15, 16), 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (24, 25), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (21, 22), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (22, 23), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (19, 20), 'total_region': merged_region}

    if year == 2015 and month == 11 and day == 10:
        time_interval_start = 8
        time_interval_stop = 16
        day_inactive = 12
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (2, 3), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (2, 3), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1, "region_num": (5, 6), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (4, 5), 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (10, 11), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (10, 11), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (12, 13), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (12, 13), 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (14, 15), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (14, 15), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (16, 17), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (16, 17), 'total_region': merged_region}

    if year == 2015 and month == 11 and day == 11:
        time_interval_start = 6
        time_interval_stop = 18
        day_inactive = 12
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (17, 18), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (17, 18), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (15, 16), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (15, 16), 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (23, 24), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (21, 22), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (21, 22), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (19, 20), 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (27, 28), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (24, 25), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (25, 26), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 10, "threshold": 0.5, "region_num": 24, 'total_region': merged_region}

    if year == 2015 and month == 12 and day == 5:
        time_interval_start = 8
        time_interval_stop = 22
        day_inactive = 3
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (7, 8), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (6, 7), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (5, 6), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (4, 5), 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (20, 21), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.6, "region_num": (20, 21), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 1, "threshold": 2, "region_num": (20, 21), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.1, "region_num": 18, 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": 23, 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (22, 23), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": 22, 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": 21, 'total_region': merged_region}

    if year == 2015 and month == 12 and day == 6:
        time_interval_start = 8
        time_interval_stop = 22
        day_inactive = 4
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (9, 10), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (9, 10), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (7, 8), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 1, "region_num": (7, 8), 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (13, 14), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (13, 14), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (11, 12), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (11, 12), 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (21, 22), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (19, 20), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1, "region_num": (19, 20), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": 18, 'total_region': merged_region}

    if year == 2015 and month == 12 and day == 11:
        time_interval_start = 10
        time_interval_stop = 22
        day_inactive = 4
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (15, 16), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 1.2, "region_num": (17, 18), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 2, "region_num": (16, 17), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.2, "region_num": 13, 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (18, 19), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 1.2, "region_num": (19, 20), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1, "region_num": 17, 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.2, "region_num": (15, 16), 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (21, 22), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 1, "region_num": (23, 24), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1, "region_num": 20, 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.2, "region_num": 20, 'total_region': merged_region}

    if year == 2015 and month == 12 and day == 14:
        time_interval_start = 8
        time_interval_stop = 14
        day_inactive = 3
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (5, 6), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (6, 7), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": (3, 4), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (4, 5), 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (8, 9), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (10, 11), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1, "region_num": (7, 8), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (8, 9), 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (11, 12), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (13, 14), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 0.5, "region_num": 10, 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": 12, 'total_region': merged_region}

    if year == 2015 and month == 12 and day == 20:
        time_interval_start = 8
        time_interval_stop = 14
        day_inactive = 19
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (5, 6), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (5, 6), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1, "region_num": (3, 4), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": 4, 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (8, 9), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (9, 10), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1, "region_num": (7, 8), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 1, "region_num": (8, 9), 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (11, 12), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.3, "region_num": (13, 14), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1, "region_num": (11, 12), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (11, 12), 'total_region': merged_region}

    if year == 2015 and month == 12 and day == 31:
        time_interval_start = 8
        time_interval_stop = 18
        day_inactive = 30
        match instance:
            case 1:
                fac_parameters_north = {"time_interval": 2, "threshold": 1, "region_num": (6, 7), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (7, 8), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 5, "region_num": (5, 6), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": 6, 'total_region': merged_region}
            case 2:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (9, 10), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (10, 11), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 3, "region_num": (8, 9), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": 9, 'total_region': merged_region}
            case 3:
                fac_parameters_north = {"time_interval": 2, "threshold": 0.5, "region_num": (12, 13), 'total_region': merged_region}
                fac_parameters_north_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": (13, 14), 'total_region': merged_region}
                fac_parameters_south = {"time_interval": 2, "threshold": 1, "region_num": (11, 12), 'total_region': merged_region}
                fac_parameters_south_inactive = {"time_interval": 2, "threshold": 0.5, "region_num": 12, 'total_region': merged_region}

    dataset['FAC_parameters_north'] = fac_parameters_north
    dataset['FAC_parameters_north_inactive'] = fac_parameters_north_inactive
    dataset['FAC_parameters_south'] = fac_parameters_south
    dataset['FAC_parameters_south_inactive'] = fac_parameters_south_inactive

    day_start = datetime(year, month, day, time_interval_start, 00, 00, 00)
    day_stop = datetime(year, month, day, time_interval_stop, 00, 00, 00)

    day_start_inactive = datetime(year, month, day_inactive, time_interval_start, 00, 00, 00)
    day_stop_inactive = datetime(year, month, day_inactive, time_interval_stop, 00, 00, 00)

    date = day_start.strftime('%Y%m%d')
    date_inactive = day_start_inactive.strftime('%Y%m%d')

    dataset['day_start'] = day_start
    dataset['day_stop'] = day_stop

    dataset['day_start_inactive'] = day_start_inactive
    dataset['day_stop_inactive'] = day_stop_inactive

    dataset['date'] = date
    dataset['date_inactive'] = date_inactive

    return dataset
