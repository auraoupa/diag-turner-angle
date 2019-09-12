#######################################
# This code crop the North Atlantic
# Ocean dataset into 10 x 10 degree boxes
#
# Author : Adekunle Ajayi
# Affilation : Institut des Geosciences de l'Environnement (IGE),
#              Universite Grenoble Alpes, France.
# Email : adekunle.ajayi@univ-grenoble-alpes.fr,
#######################################

import sys
import numpy as np
from netCDF4 import Dataset as ncopen

# - Define grid file
gridfile = '/media/extra/DATA/NATL60/NATL60-I/NATL60_coordinates_v4.nc'

# - Define read data function
def read_datagrid(gridfile,latmin=None,latmax=None,lonmin=None,lonmax=None):
    """Return navlon,navlat."""
    ncfile = ncopen(gridfile,'r')
    # load navlon and navlat
    _navlon = ncfile.variables['nav_lon'][:,:]
    _navlat = ncfile.variables['nav_lat'][:,:]
    #-Define domain
    domain = (lonmin<_navlon) * (_navlon<lonmax) * (latmin<_navlat) * (_navlat<latmax)
    where = np.where(domain)
    vlats = _navlat[where]
    vlons = _navlon[where]
    #get indice
    jmin = where[0][vlats.argmin()]
    jmax = where[0][vlats.argmax()]
    imin = where[1][vlons.argmin()]
    imax = where[1][vlons.argmax()]
    #load arrays
    navlon = _navlon[jmin:jmax+1,imin:imax+1]
    navlat = _navlat[jmin:jmax+1,imin:imax+1]
    return navlon,navlat,jmin,jmax,imin,imax

# - Define box dimensions
Box_01 = ['42.0','37.0','-65.0','-60.0','GS',1]
Box_02 = ['55.0','50.0','-17.0','-12.0','NE',2]
Box_03 = ['36.0','31.0','-30.0','-25.0','AC',3]


# - Generate box array
box_arr = []
for ii in np.arange(1,4,1):
    name = eval('Box_'+str(ii).zfill(2))
    box_arr.append(name)
    

#- defining dictionaries for the boxes
class box: # empty container.
    def __init__(self,name=None):
        self.name = name
        return

dictboxes = {}

for ibox in box_arr:
    #print(ibox)
    y2 = eval(ibox[0]) ;y1 = eval(ibox[1]);
    x2 = eval(ibox[2]) ;x1 = eval(ibox[3]);
    box_name = ibox[4]
    nb_box = ibox[5]
    # - Obtain navlon and Navlat
    navlon,navlat,jmin,jmax,imin,imax = read_datagrid(gridfile,latmin=y1,latmax=y2,lonmin=x2,lonmax=x1)
    
    # - save box parameter
    abox = box(box_name)
    abox.lonmin = navlon.min()
    abox.lonmax = navlon.max()
    abox.latmin = navlat.min()
    abox.latmax = navlat.max()
    abox.navlon = navlon
    abox.navlat = navlat
    abox.imin = imin
    abox.imax = imax
    abox.jmin = jmin
    abox.jmax = jmax
    abox.nb = nb_box
    dictboxes[box_name] = abox

boxes = dictboxes.values()
