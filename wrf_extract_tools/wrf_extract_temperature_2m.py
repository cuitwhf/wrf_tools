from wrf import getvar, ll_to_xy, ALL_TIMES, extract_times
from netCDF4 import Dataset
import pandas as pd
import datetime


def getDatesByTimes(sDateStr, eDateStr):
    # 根据开始日期、结束日期返回这段时间里所有天的集合
    list = []
    datestart = datetime.datetime.strptime(sDateStr, '%Y-%m-%d_%H')
    dateend = datetime.datetime.strptime(eDateStr, '%Y-%m-%d_%H')
    list.append(datestart.strftime('%Y-%m-%d_%H'))
    while datestart < dateend:
        datestart += datetime.timedelta(hours=1)
        list.append(datestart.strftime('%Y-%m-%d_%H'))
    return list


def wrf_extract(
        wrfname,  # wrfname.WRF产生的输出结果.通常以wrfout为前缀
        extract_lat,  # extract_lat.提取点纬度.
        extract_lon,  # extract_lon.提取点经度.
        stime,  # stime.提取数据的时间限制.开始时间 格式：%Y-%m-%d_%H.
        etime,  # etime.提取数据的时间限制.结束时间 格式：%Y-%m-%d_%H.
        tformat):
    # 程序名称：提取WRF中的点
    # 功能：将提取出来的点数据保存为csv
    # 更新时间：Feb.22, 2021

    time_list = getDatesByTimes(stime, etime)  # 获取需要提取的时间列表
    ncfile = Dataset(wrfname)  # 打开wrfout文件
    data = getvar(ncfile, 'T2', timeidx=ALL_TIMES)  # 获取变量集
    data = data.__array__()

    # print(data)
    data_times = extract_times(ncfile, timeidx=ALL_TIMES)  # 获取数据时间
    nt = data.shape[0]  # 获取时间维度.用于循环查找在提取时间范围内的数据

    # f = open(output_name, 'w', encoding='utf-8', newline="")  # 创建输出文件对象
    # csv_writer = csv.writer(f)  # 创建写入器
    date_list = []
    data_list = []

    for time_id in range(0, nt):  # 遍历时间
        temp_time = pd.to_datetime(data_times[time_id])

        if tformat == 'UTC':  # 对时间格式进行转换
            temp_time = temp_time
        elif tformat == 'BJT':
            temp_time = temp_time + datetime.timedelta(hours=8)  # 北京时间则往后推8小时

        temp_time = temp_time.strftime('%Y-%m-%d_%H')  # 将日期转换为字符串格式

        for ext_time in time_list:  # 判断当前时间是否在需要提取的时间范围内
            if temp_time == ext_time:
                ext_pos = ll_to_xy(
                    ncfile,
                    extract_lat,
                    extract_lon,
                    timeidx=time_id).__array__()  # 获取提取点行列号

                data_list.append(
                    data[time_id, ext_pos[0], ext_pos[1]] - 273.15)
                ext_time = datetime.datetime.strptime(ext_time, '%Y-%m-%d_%H')
                ext_time = ext_time.strftime('%Y/%m/%d %H:%M')
                date_list.append(ext_time)
                break
    return date_list, data_list


if __name__ == '__main__':

    wrfname = r'DEM_LU/wrfout_d03_2020-07-15'
    output_name = r'wrf_extract_temperature_2m_july.csv'
    site_data = r'scb_site.csv'
    time_format = 'UTC'  # 时间格式选取.当前可供选择为 UTC BJT
    stime = '2020-07-15_00'  # 数据提取起始时间 格式：YYYY-MM-DD_hh
    etime = '2020-07-31_23'  # 数据提取结束时间 格式：YYYY-MM-DD_hh

    site = pd.read_csv(site_data, sep=',')
    site = pd.DataFrame(site)

    site_lat = site['LAT']
    site_lon = site['LON']
    site_id = site['NAME']

    record_book = dict()

    for site_i in range(0, len(site_id)):
        date, data = wrf_extract(
            wrfname,  # wrfname.WRF产生的输出结果.通常以wrfout为前缀
            site_lat[site_i],  # extract_lat.提取点纬度.
            site_lon[site_i],  # extract_lon.提取点经度.
            stime,  # stime.提取数据的时间限制.开始时间 格式：%Y-%m-%d_%H.
            etime,  # etime.提取数据的时间限制.结束时间 格式：%Y-%m-%d_%H.
            time_format)
        if site_i == 0:
            record_book.update([('Date', date)])
        record_book.update([(site_id[site_i], data)])

    df = pd.DataFrame(record_book)
    df.to_csv(output_name, index=False)
    print('处理完毕: %s' % output_name)