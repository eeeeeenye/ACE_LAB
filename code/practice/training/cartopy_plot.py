import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import sys
from matplotlib.patches import Rectangle

def visualization(cbottom=0.15,figsize=(11,11),vm=0, vn=0, nrows=0, ncols=0, data=None, title=None, subtitle=None, clevs=None):
    # plot
    # cmap = plt.colormaps['bwr']             #Blue-white-red 색상맵맵
    clevs = clevs     # clevs는 등치선(contour level)
    vm = vm
    vn = vn

    nrows = nrows
    ncols = ncols

    # make grid 위도-경도 좌표를 생성하고, 지도 좌표계를 설정하며, 격자선을 추가하는 부분
    x, y = np.meshgrid(np.arange(0,360.0, 2.5), np.arange(-90.0, 92.5, 2.5))
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols,
                            subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)},
                            figsize=figsize)

    # 경도, 위도 눈금을 30도 간격으로 생성
    lon_ticks = np.arange(-180, 181, 60)
    lat_ticks = np.arange(-90, 91, 30)

    grd = axs.gridlines(crs=ccrs.PlateCarree(), draw_labels=False,
                        linewidth=0.5, linestyle='dashed', color='gray', alpha=0.7, zorder=7)
    # 위도 눈금 위치 설정
    grd.ylocator = mticker.FixedLocator(lat_ticks)

    axs=axs.flatten()

    for i, data in enumerate(data):
        # data = correlation_matrix[i][:,:,:]
        # print(data)
        # data, lons = add_cyclic_point(correlation_matrix[i],coord=data['lon'])
        cs = axs[i].contourf(x, y, data , levels=clevs, cmap='bwr', 
                            transform=ccrs.PlateCarree(), zorder=4, extend='both')
        axs[i].set_title(title[i])

        #해안선 따라 선긋기
        axs[i].coastlines(linewidth=0.7, color='dimgray', zorder=7)

        # ㅣlon
        axs[i].set_xticks(lon_ticks, crs=ccrs.PlateCarree())
        lon_fmt = LongitudeFormatter(number_format='.0f', degree_symbol=r'$^{\circ}$')
        axs[i].xaxis.set_major_formatter(lon_fmt)
        axs[i].tick_params(axis='x', labelsize=8)

        # lat
        axs[i].set_yticks(lat_ticks, crs=ccrs.PlateCarree())
        lat_fmt = LatitudeFormatter(number_format = '.0f', degree_symbol=r'$^{\circ}$')
        axs[i].yaxis.set_major_formatter(lat_fmt)
        axs[i].tick_params(axis='y', labelsize=8)

        # axs[i].setp(ax.get_xticklabels(), fontsize=8)
        # axs[i].setp(ax.get_yticklabels(), fontsize=8)

    space = nrows * ncols
    print(space, len(title))
    if space != len(title):
         for i in range(space, -1, -1):
            print(i)
            fig.delaxes(axs[i-1])
            space -= 1
            if space == len(title):
                break
                
    fig.subplots_adjust(bottom=0.2, top=0.9, left=0.1, right=0.9, hspace=0.1, wspace=0.3)
    # cax2 = plt.contourf(x, y, correlation_matrix[2] , levels=clevs, cmap=cmap, transform=ccrs.PlateCarree(), zorder=4)

    # 컬러바의 위치와 크기 설정
    cbar_ax = fig.add_axes([0.2, cbottom, 0.6, 0.02])

    cbar =fig.colorbar(cs, cax=cbar_ax, orientation='horizontal')
    cbar.ax.tick_params(labelsize=8, direction='in', length=8, width=0.4, color='black', zorder=6)

    plt.suptitle(subtitle)
    plt.show()
    plt.savefig(o_path+o_name+'.png', dpi=300)
    plt.close()