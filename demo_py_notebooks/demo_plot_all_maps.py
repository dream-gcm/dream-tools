# python3
#
# Purpose: Demon how to read some DREAM model output (here temperature at 500 hPa, T31 resolution) 
# and plot maps for a series of time steps.
# To make a movie out of them, read the last section of the provided notebook.
# last update: 28/03/19
# stephanie.leroux@ocean-next.fr

# The code below  loops on all the timesteps and plot a map each timestep (or could also be one map every day  or anything else). 
# It uses a plot routine that i have written, called with ```cs = slx.plotmap(...)``` where ```(...)``` are the plot options.
# The function is part of the plot libraries loaded in the import section above.


##############################################################
### IMPORTS

## standart libraries
import os,sys
import numpy as np

# xarray
import xarray as xr
    
# plot
import cartopy.crs as ccrs
import cartopy.feature as ccf
import cartopy.util as ccu
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

# My custom module with plot tools
import wip_utils_SLX_plots_dream as slx


##############################################################
### READ DATA

### local directory of input files (on my laptop)
diri = "/Users/leroux/DATA/DREAM_DATA/T31/"

# name of the config exp.
CONFIGNAME = "history.air.500.model.4xdaily"

# input file
fili = CONFIGNAME+".nc"


#read all temperature data from file
air = xr.open_dataset(diri+fili,decode_times=True)['air'].squeeze()
# note: .squeeze() is used to get rid of the spurious dimensions (i.e. here, level)

# print info on the array
print("-------------------------------------")
print("-------------------------------------")
print("-------- data info --------------")
print(air)

print(" ")
print(" ")
print("-------------------------------------")
print("-------------------------------------")
print("-------- max, mean, min --------------")
print(air.max())
print(air.mean())
print(air.min())

##############################################################
### PLOT MAP FOR EACH TIMESTEP

# The code below  loops on all the timesteps and plot a map each timestep (or could also be one map every day  or anything else). 
# It uses a plot routine that i have written, called with ```cs = slx.plotmap(...)``` where ```(...)``` are the plot options.
# The function is part of the plot libraries loaded in the import section above.



#----------------------------------------------------
#------ PLOT PARAMETERS------------------------------
#----------------------------------------------------

#------------ geography
# Global plot? True/False
glo= True

# center longitude on:
loncentr=180.

# set coastL to True if you want coaslines
coastL=True

#------------ color shading

# type of plot (can be 'contourf', 'pcolormesh', defaut is contourf)
typlo='contourf'

# min max values on the colorscale
vmin=-12
vmax=12

# colormap
cm_base=slx.make_NCLcolormap()

# number of color segments of the colormap
Nincr=50

# color of the values smaller than vmin
su='#EFF5FB'
# color of the values larger than vmax
so='#F8E0E0'

# colorbar label 
labelplt= "500 hPa Temperature ("+air.units+")"

# number of labels on the colorbar
Nbar=5

#------------ plot output
# plot format
pltty = ".png"

# plot resolution (dpi)
dpifig=200

# base name for output plot file
plti="T500_"+CONFIGNAME

# output directory for plots
diro="./"


#----------------------------------------------------
#------ LOOP ON TIMESTEP ----------------------------
#----------------------------------------------------
print(" ")
print(" ")
print("-------------------------------------")
print("-------------------------------------")
print("-------- LOOP ON TIMESTEP  --------------")
print("...  wait until all maps are plotted ...")

# loop on all time steps in the data array:
for it in range(0,3): 
                
            # output plot file name including the time index
            plto = plti+"."+str(it+100)

            # data to plot (must be a 2-d np.array)
            # here we select one timestep at a time for plotting purposes
            data2plot  = air.isel(time=it).values

            # make the data to plot cyclic so that the values at longitude 0 are repeated at 360. (for plot purposes)
            cyclic_data, cyclic_lons = ccu.add_cyclic_point(data2plot, coord=air.lon.values)

            #----------------------------------------------------
            #------ PLOT ----------------------------------------
            #----------------------------------------------------

            # create fig
            fig1 = plt.figure(figsize=([13,10]),facecolor='white')

            # plot data (base plot from plotmap functionn defined above)
            cs = slx.plotmap(fig1,cyclic_data,cyclic_lons,air.lat.values,plto,cm_base=cm_base,vmin=vmin,vmax=vmax,Nincr=Nincr,glo=glo,coastL=coastL,su=su,so=so,loncentr=loncentr,typlo=typlo,Nbar=Nbar,labelplt=labelplt)

            # add title on plot (date)
            plt.title(slx.printdatestring(air.time.to_index(),it))

            #if it==1:
                # display plot only once in the loop
                #plt.show()

            # Save fig in png, resolution dpi
            fig1.savefig(diro+"/"+plto+'.png', facecolor=fig1.get_facecolor(), edgecolor='none',dpi=dpifig,bbox_inches='tight', pad_inches=0)#

            # close fig
            plt.close(fig1)       
print(" ")
print(" ")
print("-------------------------------------")
print("-------------------------------------")
print("-------- FINISHED!  --------------")