from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import sys
from matplotlib.patches import Rectangle

o_path = '/home/inhye_yoo/edu/image/'
o_name = 'DJF_NINO34_idx_1950_2019'

i_path1 = '/home/inhye_yoo/edu/datasets/'
f = Dataset(i_path1+'DJF_NINO34_idx_1950_2019.nc','r')
f.set_auto_mask(False)

nino34 = f.variables['nino34'][:]
nino34 = nino34.reshape(-1)

fig = plt.figure(figsize=(11,8.5))

ax = fig.add_subplot(1,1,1)

t = np.arange(1, len(nino34)+1,1)

line = plt.plot(t, nino34, 'black', label='nino34', zorder=5)
plt.setp(line, linewidth=2,marker='o', markersize=3)

plt.axhline(y=1, color='red', linewidth=1, linestyle='-', zorder=3)
plt.axhline(y=-1, color='blue', linewidth=1, linestyle='-', zorder=3)

plt.title('(a) DJF NINO34 [1950-2019] ', fontsize=14, loc='left')

plt.ylim(-3,3)
plt.xticks(ticks=np.arange(1, len(nino34), 5),
            labels=[f"{yr%100}/{(yr+1) % 100}" for yr in np.arange(1950, 2019, 5)])

plt.legend(loc='upper left', fontsize=7)
plt.subplots_adjust(bottom=0.15, top=0.95, left=0.05, right=0.95, hspace=0.3, wspace=0.3)
plt.savefig(o_path+o_name+'.png', dpi=300)
plt.close()
