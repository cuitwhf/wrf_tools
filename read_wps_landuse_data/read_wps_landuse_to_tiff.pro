pro read_wps_landuse_to_tiff
; word_size = 1
; 目前只支持等经纬度投影二进制文件读取。

; 确定输入目录
input_dir='D:\WRF\modis_landuse_geotiff\2018_modis_landuse_en\'
; 确定输出文件名称
output_name='C:\Users\ASUS\Desktop\wrf1.tiff'

; 检查index
file_name=input_dir+'index'
if file_test(file_name) eq 0 then begin
  print,'缺少index文件！'
  return
endif
openr,1,file_name
; 检查wordsize
n_lines=file_lines(file_name)
data=strarr(1,n_lines)
readf,1,data
;print,data
wordsize_pos=strpos(data,'wordsize')
wordsize_pos=where(wordsize_pos ne -1)
wordsize_info=strsplit(data[wordsize_pos],'=',/extract)
if wordsize_info[1] ne 1 then begin
  print,'wordsize必须被设置成1！'
  free_lun,1
  return
endif
; 检查投影方式
pos=strpos(data,'projection')
pos=where(pos ne -1)
info=strsplit(data[pos],'=',/extract)

if strcompress(info[1],/remove_all) ne 'regular_ll' then begin
  print,'projection 必须被设置成 regular_ll！'
  free_lun,1
  return
endif

; 获取地理信息
pos=strpos(data,'known_lon')
pos=where(pos ne -1)
info=strsplit(data[pos],'=',/extract)
lon_min=double(info[1])

pos=strpos(data,'known_lat')
pos=where(pos ne -1)
info=strsplit(data[pos],'=',/extract)
lat_min=double(info[1])

pos=strpos(data,'dx')
pos=where(pos ne -1)
info=strsplit(data[pos],'=',/extract)
x_res=double(info[1])

pos=strpos(data,'dy')
pos=where(pos ne -1)
info=strsplit(data[pos],'=',/extract)
y_res=double(info[1])

free_lun,1

file_list=file_search(input_dir,'*-*.*-*',count=file_n)
; 确定数据大小
start_col=long(0)
start_row=long(0)
end_col=long(-99999)
end_row=long(-99999)
for file_i=0,file_n-1 do begin
  file_name=file_basename(file_list[file_i])
  temp_end_col=strmid(file_name,6,5)
  temp_end_row=strmid(file_name,18,5)
  if temp_end_col ge end_col then end_col=temp_end_col
  if temp_end_row ge end_row then end_row=temp_end_row
endfor
;print,start_col,end_col,start_row,end_row

; 建立结果数组
result_box=intarr(end_col,end_row)

; 获取最大纬度
pos=strpos(data,'known_x')
pos=where(pos ne -1)
info=strsplit(data[pos],'=',/extract)
known_x=double(info[1])
if known_x eq 1 then lat_max=lat_min+(end_row-1)*y_res
if known_x ne 1 then lat_max=lat_min

; 读取文件 并将结果拼接到结果数组中
for file_i=0,file_n-1 do begin
  ; 文件名称
  file_name=file_list[file_i]
  sname=file_basename(file_name)
  
  ; 获取单个文件在数组中的行列号 *这个地方需要更改 从index中读取
  mosaic_col_start=long(strmid(sname,0,5))-1
  mosaic_col_end=long(strmid(sname,6,5))-1
  mosaic_row_start=long(strmid(sname,12,5))-1
  mosaic_row_end=long(strmid(sname,18,5))-1
  ;print,mosaic_col_start,mosaic_col_end,mosaic_row_start,mosaic_row_end
  
  ; 读取数据
  openr,1,file_name
  data=bytarr(mosaic_col_end-mosaic_col_start+1,mosaic_row_end-mosaic_row_start+1)
  readu,1,data
  free_lun,1
  data=long(data)
  
  ; 写入结果数组
  result_box[mosaic_col_start:mosaic_col_end,mosaic_row_start:mosaic_row_end]=data

  ; 进度查看
  print,file_name
endfor

; 由于WRF二进制文件的储存方式是右下往上 由左往右储存 因此需要将数组进行方向上的调换
result_box=rotate(result_box,7)

geo_info={$
  MODELPIXELSCALETAG:[x_res,y_res,0.0],$
  MODELTIEPOINTTAG:[0.0,0.0,0.0,lon_min,lat_max,0.0],$
  GTMODELTYPEGEOKEY:2,$
  GTRASTERTYPEGEOKEY:1,$
  GEOGRAPHICTYPEGEOKEY:4326,$
  GEOGCITATIONGEOKEY:'GCS_WGS_1984',$
  GEOGANGULARUNITSGEOKEY:9102,$
  GEOGSEMIMAJORAXISGEOKEY:6378137.0,$
  GEOGINVFLATTENINGGEOKEY:298.25722}

write_tiff,output_name,result_box,/float,geotiff=geo_info
print,'Finish:',output_name

end