import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import rcParams
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeat
import cartopy.crs as ccrs
import numpy as np
import proplot as plot

def basemap_chengdu(ax, shppath, proj):
    '''
    :param ax: Where the axe you want plot in.
    :param shppath: The path of the shapefile you want add in.
    :param proj: The projection. You can set it by `proj = ccrs.PlateCarree()`.
    :param ti: The interval of gridlines.
    :param extent: The range of map. Such as `extent = [102.85, 105.0, 29.95, 31.5]`.
    :return: This is a process.
    '''
    # 设置字体
    config = {"font.family": 'Times New Roman', "font.size": 10, "mathtext.fontset": 'stix'}
    rcParams.update(config)  # Apply config in matplotlib

    # 设置网格线间距
    ti = 0.2
    # 设置extent
    extent = [102.85, 105.0, 29.95, 31.5]

    # 添加矢量
    # shppath = r'shp_chengdu\Chengdu.shp'
    reader = Reader(shppath)
    shape = cfeat.ShapelyFeature(
        reader.geometries(),
        proj,
        edgecolor='k',
        facecolor='none')
    ax.add_feature(shape, linewidth=0.7)

    # 限定绘制范围
    ax.set_extent(extent, crs=proj)

    # 设置网格线
    gl = ax.gridlines(crs=proj, draw_labels=True, linewidth=0.5, color='black', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.rotate_label = False
    gl.xlocator = mticker.FixedLocator([round(i, 3) for i in np.arange(extent[0], extent[1] + ti, ti)])
    gl.ylocator = mticker.FixedLocator([round(i, 3) for i in np.arange(extent[2], extent[3] + ti, ti)])

    ax.format(longrid=False, latgrid=False)


def basemap_scb(ax, shppath, proj):
    '''
    :param ax: Where the axe you want plot in.
    :param shppath: The path of the shapefile you want add in.
    :param proj: The projection. You can set it by `proj = ccrs.PlateCarree()`.
    :param ti: The interval of gridlines.
    :param extent: The range of map. Such as `extent = [102.85, 105.0, 29.95, 31.5]`.
    :return: This is a process.
    '''
    # 设置字体
    config = {"font.family": 'Times New Roman', "font.size": 10, "mathtext.fontset": 'stix'}
    rcParams.update(config)  # Apply config in matplotlib
    # 设置网格间距
    ti = 0.5

    # Add shapefile
    reader = Reader(shppath)
    shape = cfeat.ShapelyFeature(
        reader.geometries(),
        proj,
        edgecolor='k',
        facecolor='none')
    ax.add_feature(shape, linewidth=0.7)

    # Set plot range for SCB
    extent = [101.5, 110.5, 27.50, 33.5]
    extent = extent
    ax.set_extent(extent, crs=proj)

    # Plotgrid line
    gl = ax.gridlines(crs=proj, draw_labels=True, linewidth=0.5, color='black', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.rotate_label = False
    gl.xlocator = mticker.FixedLocator([round(i, 3) for i in np.arange(extent[0], extent[1] + ti, ti)])
    gl.ylocator = mticker.FixedLocator([round(i, 3) for i in np.arange(extent[2], extent[3] + ti, ti)])
    ax.format(longrid=False, latgrid=False)

    # Add city label
    ax.text(106.30, 29.38, 'Chongqing', ha='left', va='baseline')
    ax.text(106.15, 30.42, 'Guangan', ha='left', va='baseline')
    ax.text(107.10, 30.97, 'Dazhou', ha='left', va='baseline')
    ax.text(106.60, 31.92, 'Bazhong', ha='left', va='baseline')
    ax.text(105.75, 31.00, 'Nanchong', ha='left', va='baseline')
    ax.text(105.30, 32.10, 'Guangyuan', ha='left', va='baseline')
    ax.text(104.30, 31.62, 'Mianyang', ha='left', va='baseline')
    ax.text(104.10, 31.10, 'Deyang', ha='left', va='baseline')
    ax.text(104.10, 31.10, 'Deyang', ha='left', va='baseline')
    ax.text(105.15, 30.49, 'Suining', ha='left', va='baseline')
    ax.text(103.60, 30.52, 'Chengdu', ha='left', va='baseline')
    ax.text(103.60, 29.98, 'Meishan', ha='left', va='baseline')
    ax.text(103.20, 29.16, 'Leshan', ha='left', va='baseline')
    ax.text(102.40, 29.80, "Ya'an", ha='left', va='baseline')
    ax.text(104.80, 30.05, "Ziyang", ha='left', va='baseline')
    ax.text(104.50, 29.58, "Neijiang", ha='left', va='baseline')
    ax.text(104.40, 29.26, "Zigong", ha='left', va='baseline')
    ax.text(104.40, 28.70, "Yibin", ha='left', va='baseline')
    ax.text(105.30, 28.70, "Luzhou", ha='left', va='baseline')


# 测试BasemapDraw
if __name__ == '__main__':
    plt.figure(figsize=(8, 8))
    proj = ccrs.PlateCarree()
    ax = plt.subplot(111, projection=proj)

    # 测试 成都底图绘制 basemap_chengdu
    # shppath = r'shp_chengdu\Chengdu.shp'
    # basemap_chengdu(ax, shppath, proj)

    # 测试 成都底图绘制 basemap_scb
    shppath = r'shp_scb\SCB.shp'
    basemap_scb(ax, shppath, proj)

    plt.show()