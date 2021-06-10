# wrf_extract_tools

根据经纬度信息批量提取WRF模拟站点结果。

# wrf_extract_temperature_2m.py & wrf_extract_wind_speed_10m.py

程序目的：用于提取2温度变量 & 10米风速。

在程序尾部找到`if __name__ == '__main__':`,此后为输入参数区域。

输入参数介绍：
1.wrfname：wrfout的相对路径或者绝对路径。

2.output_name：提取结果的输出路径。

3.site_data：站点配置，即所需要提取的站点信息。由CSV表格给出，具体格式见*scb_site.csv*。

4.time_format：时间格式，可选择世界时间`time_format = 'UTC'`或选择北京时间`time_format = 'BJT'`。

5.stime：提取时间范围的起始时间。格式：YYYY-MM-DD_hh

6.etime：提取时间范围的结束时间。格式：YYYY-MM-DD_hh


