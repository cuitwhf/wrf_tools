function get_wrf_variable,file_name,datasetname
  ncfid=ncdf_open(file_name)
  varid=ncdf_varid(ncfid,datasetname)
  ncdf_varget,ncfid,varid,data
  ncdf_close,ncfid
  return,data
end
function get_wrf_variable_att,file_name,datasetname,attname
  ncfid=ncdf_open(file_name)
  varid=ncdf_varid(ncfid,datasetname)
  ncdf_attget,ncfid,varid,attname,data
  ncdf_close,ncfid
  return,data
end
;程序用于提取WRF数据集
pro wrf_data_extract

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

compile_opt idl2
dst_n=n_elements(dstname)
if file_test(outdir) eq 0 then file_mkdir,outdir
for dst_i=0,dst_n-1 do begin
  data=get_wrf_variable(file_name,dstname[dst_i])
  lon=get_wrf_variable(file_name,'XLONG')
  lat=get_wrf_variable(file_name,'XLAT')
  time=string(get_wrf_variable(file_name,'Times'))
  hour_n=n_elements(time)
  for hour_i=0,hour_n-1 do begin
    temp_time=time[hour_i]
    temp_lon=lon[*,*,hour_i]
    temp_lat=lat[*,*,hour_i]
    temp_data=data[*,*,hour_i]
    
    iyear=strmid(temp_time,0,4)
    imouth=strmid(temp_time,5,2)
    iday=strmid(temp_time,8,2)
    ihour=strmid(temp_time,11,2)
    GMT_convert_to_BJT,iyear,imouth,iday,ihour,oyear,omouth,oday,ohour   
    if time_format eq 'BJT' then begin
      sname=dstname[dst_i]+'_'+string(oyear,format='(I04)')+string(omouth,format='(I02)')+string(oday,format='(I02)')+'-'+string(ohour,format='(I02)')
      output_name=outdir+sname+'_BJT.tif'
    endif
    
    if time_format eq 'UTC' then begin
      sname=dstname[dst_i]+'_'+string(iyear,format='(I04)')+string(imouth,format='(I02)')+string(iday,format='(I02)')+'-'+string(ihour,format='(I02)')
      output_name=outdir+sname+'_UTC.tif'
    endif
        
    glt_lon=outdir+'glt_lon.tif'
    glt_lat=outdir+'glt_lat.tif'
    write_tiff,glt_lon,temp_lon,/float
    write_tiff,glt_lat,temp_lat,/float
    write_tiff,output_name,temp_data,/float
    
    ;#重投影
    envi,/restore_base_save_files
    envi_batch_init,/no_status_window

    envi_open_file,glt_lon,r_fid=x_fid
    envi_file_query,x_fid,dims=dims
    envi_open_file,glt_lat,r_fid=y_fid
    envi_file_query,y_fid,dims=dims
    envi_open_file,output_name,r_fid=fid
    envi_file_query,fid,dims=dims
    x_pos=0
    y_pos=0
    pos=0

    envi_file_query,fid,sname=sname
    out_name_glt=outdir+sname+'_glt.img'
    out_name_glt_hdr=outdir+sname+'_glt.hdr'
    pixel_size=output_resolution
    rotation=0.0
    i_proj=envi_proj_create(/geographic)
    o_proj=envi_proj_create(/geographic)
    envi_glt_doit, i_proj=i_proj, $
      o_proj=o_proj,out_name=out_name_glt,$
      pixel_size=pixel_size,r_fid=glt_fid,$
      rotation=rotation,x_fid=x_fid,y_fid=y_fid,$
      x_pos=x_pos,y_pos=y_pos

    out_name=outdir+'_georef.img'
    out_name_hdr=outdir+'_georef.hdr'
    envi_doit,'envi_georef_from_glt_doit',fid=fid,$
      glt_fid=glt_fid,out_name=out_name,pos=pos,$
      subset=dims,r_fid=r_fid
    envi_open_file,out_name,r_fid=fid0
    map_info=envi_get_map_info(fid=fid0)
    geo_loc=map_info.(1)
    px_size=map_info.(2)
    envi_file_query,fid0,ns=ns,nl=nl,nb=nb,dims=dims
    aod_data=make_array(ns,nl)
    aod_data[*,*]=envi_get_data(fid=fid0,pos=0,dims=dims)
    aod_result=make_array(ns,nl)
    aod_result=aod_data
    geo_info={$
      MODELPIXELSCALETAG:[px_size[0],px_size[1],0.0],$
      MODELTIEPOINTTAG:[0.0,0.0,0.0,geo_loc[2],geo_loc[3],0.0],$
      GTMODELTYPEGEOKEY:2,$
      GTRASTERTYPEGEOKEY:1,$
      GEOGRAPHICTYPEGEOKEY:4326,$
      GEOGCITATIONGEOKEY:'GCS_WGS_1984',$
      GEOGANGULARUNITSGEOKEY:9102,$
      GEOGSEMIMAJORAXISGEOKEY:6378137.0,$
      GEOGINVFLATTENINGGEOKEY:298.25722}
    write_tiff,output_name,aod_result,/float,geotiff=geo_info

    envi_file_mng,id=x_fid,/remove
    envi_file_mng,id=y_fid,/remove
    envi_file_mng,id=fid,/remove
    envi_file_mng,id=glt_fid,/remove
    envi_file_mng,id=r_fid,/remove
    envi_file_mng,id=fid0,/remove
    file_delete,[glt_lon,glt_lat,out_name_glt,out_name_glt_hdr,out_name,out_name_hdr]
    envi_batch_exit
    print,output_name
  endfor
  
  
endfor




end
pro GMT_convert_to_BJT,iyear,imouth,iday,ihour,oyear,omouth,oday,ohour
  ;程序用于转换GMT时间到BJT时间.小时计数从0-23
  if (iyear mod 4) eq 0 then begin
    leap_year='Y'
  endif else begin
    leap_year='N'
  endelse

  if leap_year eq 'Y' then begin;如果是闰年
    mouthday_n=[31,29,31,30,31,30,31,31,30,31,30,31]
    ;日是否需要进位
    if ihour+8 ge 24 then begin;如果需要进位
      ohour=ihour+8-24;->小时位输出
      oday=iday+1
      if oday gt mouthday_n[imouth-1] then begin
        omouth=imouth+1
        oday=oday-mouthday_n[imouth-1]
        if omouth gt 12 then begin
          omouth=omouth-12
          oyear=iyear+1
        endif else begin
          oyear=iyear
        endelse

      endif else begin
        omouth=imouth
        oyear=iyear
      endelse
    endif else begin;如果不需要进位
      ohour=ihour+8
      oday=iday
      omouth=imouth
      oyear=iyear
    endelse
  endif

  if leap_year eq 'N' then begin;如果是闰年
    mouthday_n=[31,28,31,30,31,30,31,31,30,31,30,31]
    ;日是否需要进位
    if ihour+8 ge 24 then begin;如果需要进位
      ohour=ihour+8-24;->小时位输出
      oday=iday+1
      if oday gt mouthday_n[imouth-1] then begin
        omouth=imouth+1
        oday=oday-mouthday_n[imouth-1]
        ;stop
        if omouth gt 12 then begin
          omouth=omouth-12
          oyear=iyear+1
        endif else begin
          oyear=iyear
        endelse

      endif else begin
        omouth=imouth
        oyear=iyear
      endelse
    endif else begin;如果不需要进位
      ohour=ihour+8
      oday=iday
      omouth=imouth
      oyear=iyear
    endelse
  endif

end