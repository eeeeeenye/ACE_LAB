from netCDF4 import Dataset
import numpy as np
import os, pathlib, sys

i_path = '/home/inhye_yoo/edu/datasets/'
i_name = 'ERA.sst.1950_2019.nc'
f = Dataset(i_path + i_name, 'r')
dat = f.variables['p'][:,:,:]
f.close()

dat = np.array(dat)
dat = dat.reshape(-1,12,73,144)
dat = np.where(dat==-9.99e+08,np.nan, dat)

clim = np.mean(dat, axis=0)
clim = clim.reshape(-1, 12, 73, 144)

anom = dat-clim
# std = np.std(anom, axis=0).reshape(-1, 12, 73, 144)

# var = anom/std
# var = var.reshape(-1, 12, 73,144)

o_path = '/home/inhye_yoo/edu/datasets/'
o_name = 'ERA.sst_anom.195001_201912'

#save
var = np.array(anom)
var.astype('float32').tofile(o_path+o_name+'.gdat')

ctl = open(o_path+o_name+'.ctl','w')
ctl.write('dset ^'+o_name+'.gdat\n')
ctl.write('undef    -9.99e+08\n')
ctl.write('xdef 144 linear  0.  2.5\n')
ctl.write('ydef 73  linear  -90.    2.5\n')
ctl.write('zdef 11  linear  1   1\n')
ctl.write('tdef 840 linear  jan1950 1mo\n')
ctl.write('vars 1\n')
ctl.write('p    1   1   variable\n')
ctl.write('ENDVARS\n')
ctl.close()

os.system('cdo -f nc import_binary '+o_path+o_name+'.ctl '+o_path+o_name+'.nc')
# os.system('rm -f '+o_path+o_name+'.ctl '+o_path+o_name+'.gdat')