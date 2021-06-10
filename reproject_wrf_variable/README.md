# Reproject-WRF-variables

This is a IDL program !!!

This program reproject the default such as Lambert of WRF output to the WGS-84.

This program named 'wrf_data_extract.pro', and you can easy to go it.

All the input variable is at the head of the program. Such as here.

```
; ################################################################################
;file_name.数据集文件所在路径
file_name='D:\Ubuntu\WRF-Data\CDE\1980\wrfout_d03_2020-01-15'

;outdir.数据集输出路径
outdir='D:\Ubuntu\WRF-Data\CDE\wrf-raster\'

;dstname.需要提取的数据集名称
dstname=['T2']

;output_resolution.输出分辨率
output_resolution=0.03

;Time_format.
time_format='UTC'; 'BJT'
; ################################################################################
```

`file_name`: The WRF output file.

`outdir`: The output directory.

`dstname`: The dataset name list. program will deal the all variable one by one.

`output_resolution`: The output resolution. The units is degree.

`time_format`: You can set it for 'BJT' or 'BTC'. The program will set the output name by reference this time.

## Note

The default longitude and latitude is checked by 'XLONG' and 'XLAT'. But many variable is not checked by these varibles.

So, you will sure that which geographic varibles is your variables checked for. 

And you can modify here to continue run the program.

```
lon=get_wrf_variable(file_name,'XLONG')
lat=get_wrf_variable(file_name,'XLAT')
```



