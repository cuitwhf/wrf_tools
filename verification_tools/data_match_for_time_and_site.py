'''
程序用于匹配两个csv中的数据。
按时间和站点数据进行匹配。
由于经常将此程序用于验证WRF的结果的准确性。
因此将文件1命名为file_obs，文件2命名为file_mod。
如下：
文件1中内容为：
                  Date  Guangyuan  Mian  ...  Guangan  Bazhong  Dazhou
0     2019-12-31 16:00        6.8   7.8  ...      7.8      6.6     8.4
1     2019-12-31 17:00        6.6   7.7  ...      7.7      6.5     8.3
2     2019-12-31 18:00        6.6   7.6  ...      7.7      6.4     8.1
3     2019-12-31 19:00        6.4   7.5  ...      7.7      6.4     8.0
4     2019-12-31 20:00        6.1   7.3  ...      7.5      6.3     8.0
...                ...        ...   ...  ...      ...      ...     ...
1483  2020-07-31 11:00       25.0  23.8  ...     25.6     26.7    29.2
1484  2020-07-31 12:00       24.1  23.6  ...     25.3     25.2    28.5
1485  2020-07-31 13:00       23.4  23.3  ...     24.6     23.9    28.1
1486  2020-07-31 14:00       23.3  23.2  ...     24.5     23.3    27.6
1487  2020-07-31 15:00       22.8  23.1  ...     24.5     23.5    27.2

文件2中内容为：
                 Date  Guangyuan       Mian  ...    Guangan    Bazhong     Dazhou
0    2020/07/15 00:00  24.088403  25.582239  ...  24.618921  22.544458  22.022821
1    2020/07/15 01:00  24.960596  28.571313  ...  26.666956  24.344812  26.254358
2    2020/07/15 02:00  25.971429  29.399011  ...  27.596246  24.208948  28.421472
3    2020/07/15 03:00  27.095178  30.256006  ...  28.644769  25.702600  29.985956
4    2020/07/15 04:00  27.776910  31.524622  ...  29.617761  27.661218  30.897577
..                ...        ...        ...  ...        ...        ...        ...
403  2020/07/31 19:00  26.748102  26.461847  ...  27.164270  28.930658  28.310754
404  2020/07/31 20:00  26.174524  25.843286  ...  26.525507  27.625879  27.756586
405  2020/07/31 21:00  25.465417  25.726709  ...  26.104425  28.241602  27.509302
406  2020/07/31 22:00  26.350031  25.355981  ...  25.511285  27.779779  27.058740
407  2020/07/31 23:00  26.814569  26.753290  ...  27.772852  29.116998  28.273065

输出结果将会根据file_obs中的站点结果和file_mod中的站点结果的匹配情况决定输出文件数量。
每个站点将输出一个文件。
每个文件中所包含的数据包括站点名称，匹配时间以及数值。
'''

import pandas as pd
import numpy as np
import csv

file_obs = 'meteorological_data_windspeed.csv'
file_mod = 'wrf_extract_wind_speed_10m_july.csv'

data_obs = pd.read_csv(file_obs)
data_mod = pd.read_csv(file_mod)

site_obs = list(data_obs.columns)[1::]
site_mod = list(data_mod.columns)[1::]

date_obs = data_obs[list(data_obs.columns)[0]].values
date_mod = data_mod[list(data_mod.columns)[0]].values

i = 0
for temp_site in site_obs:
    if temp_site in site_mod:
        f = open('data_match_of_%s.csv' % temp_site, 'w', newline="")
        writer = csv.writer(f)

        temp_data_obs = data_obs[temp_site].values
        temp_data_mod = data_mod[temp_site].values

        for i in range(0, date_obs.shape[0]):
            temp_obs_date = date_obs[i]
            # print(temp_obs_date)
            # print(np.where(date_mod == '2020-07-31 09:00'))
            if np.where(date_mod == temp_obs_date)[0].shape[0] != 0:
                match_pos = np.where(date_mod == temp_obs_date)[0][0]
                # print(temp_data_obs[i], temp_data_mod[match_pos])
                writer.writerow([temp_obs_date, temp_data_obs[i], temp_data_mod[match_pos]])
        print('Finish: %s' % 'data_match_of_%s.csv' % temp_site)





