#!/usr/bin/env  python
#=======================================================================
"""utils_plotmaps.py
Tools to create maps
"""
#=======================================================================


def plotmap(fig1,ehonan,nav_lon,nav_lat,cm_base=cm.viridis,plto='tmp_plot',vmin='0',vmax='0',Nincr=10,pcolormesh=True,Nbar=10,glo=True,coastL=False,coastC=False,xlim=(0,10),ylim=(0,10),su='b',so='k',loncentr=0.):
        '''
        PURPOSE: Plot regional or global map of gridded data (shading).
        Uses Cartopy, xarray, matplotlib, numpy.
        
        PARAMETERS: (...to be done...)
        fig1: fig id,
        ehonan: 2-d array to plot (geographical data)
        nav_lon: corresponding lon array . Works with lat and lon given as 1-d vectors (if regular grid such as DREAM model) or 2-d arrays (unregular grid such as the ORCA-NEMO-grid)
        nav_lat: corresponding lat array
        
        OPTIONS:
        Note that you can omit these options when calling the plot function and in this case defaut values are applied.
        cm_base: colormap (defaut=cm.viridis)
        plto: plo name (defaut='tmpplot')
        vmin: data min value to plot (color shading) (defaut vmin='0')
        vmax: data max value to plot (color shading) (defaut vmax='0')
        Nincr: number of color segments of the colormap (defaut Nincr=10)
        pcolormesh : True or False. Type of plotting function (if false then contourf is used)
        Nbar: number of labels on the colorbar (defaut Nbar=10)
        glo: global=True (default) sets that  map is global (the projection will be Robinson in nthat case). It is PlateCarre if regional map.
        coastL: set to True  to plot continents as lines (defaut is False)
        coastC: set to True to fill continents with colors
        xlim: set regional limits in longitude (degrees) if glo==False (default xlim=(0,10))
        ylim=(0,10): set regional limits in latitude (degrees) if glo==False (default ylim=(0,10))
        su: set the color of the values under vmin (appears as a triangle at the edge of the colorbar). Defaut is 'b' blue.
        so: set the color of the values over vmax (appears as a triangle at the edge of the colorbar). Defaut is 'k' black.
        loncentr: longitude to center the map projectionn (defaut is 0).
        
        LEFT-TO-DO:
        * Some color choices (for gridlines, for labels, for continents) are still coded in hard below. 
        They will be added as options in a later version of this code.
        
        '''
        
        ## imports
        import os,sys
        import numpy as np

        # xarray
        import xarray as xr

        # plot
        import cartopy.crs as ccrs
        import cartopy.feature as ccf
        import matplotlib.pyplot as plt
        from matplotlib.colors import Colormap
        import matplotlib.colors as mcolors
        import matplotlib.dates as mdates
        import matplotlib.cm as cm
        import matplotlib.dates as mdates
        import matplotlib.ticker as mticker
        
        # Colormap & levels
        cmap = plt.get_cmap(cm_base)
        cmap.set_under(su,1.)
        cmap.set_over(so,1.) 
        
        if ((vmin==0)&(vmax==0)):
            levels = mticker.MaxNLocator(nbins=Nincr).tick_values(ehonan.min(), ehonan.max())        
        else:
            levels = mticker.MaxNLocator(nbins=Nincr).tick_values(vmin, vmax)
        norm   = mcolors.BoundaryNorm(levels, ncolors=cmap.N,clip=True)
        
        # Projection
        trdata  = ccrs.PlateCarree() 
        # Note: if data points are given in classical lat lon coordinates this should
        #       be set to ccrs.PlateCarree() whatever the map projection is.
        
        if glo:
            ax = plt.axes(projection=ccrs.Robinson(central_longitude=loncentr))
            # marker size
            sm=0.1
        else:
            ax = plt.axes(projection= ccrs.PlateCarree())
            # marker size
            sm=0.5
        
        if glo:
            ax.set_global() 
            
        if glo:
            ax.outline_patch.set_edgecolor('#585858')
        else:
            ax.outline_patch.set_edgecolor('white')
            

        # grid on map
        if glo:
            gl = ax.gridlines(linewidth=1, color='#585858', alpha=0.2, linestyle='--') 
        else:
            gl = ax.gridlines(draw_labels=True,linewidth=1, color='#585858', alpha=0.2, linestyle='--')
            # grid labels
            label_style = {'size': 12, 'color': 'black', 'weight': 'bold'}
            gl.xlabel_style = label_style
            gl.xlabels_bottom = False
            gl.xlocator = mticker.FixedLocator(np.arange(-180,180,20,dtype=float))
            gl.ylabel_style = label_style
            gl.ylabels_right = False
            gl.ylocator = mticker.FixedLocator(np.arange(-90,90,20,dtype=float))
       
        # Add Coastlines and or plain continents
        if coastC:
            ax.add_feature(ccf.LAND, facecolor='#585858', edgecolor='none')
        if coastL:
            ax.coastlines(color='#585858')
        
        ### PLOTS:
        
        if pcolormesh:
            cs  = plt.pcolormesh(nav_lon, nav_lat, ehonan,cmap=cmap,transform=trdata,norm=norm,vmin=vmin,vmax=vmax)
        
        else:
            cs  = plt.contourf(nav_lon, nav_lat, ehonan,transform=trdata,levels=levels,norm=norm,cmap=cmap,extend='both')
            

        if glo==False:
            #limits
            plt.xlim(xlim)
            plt.ylim(ylim) 

        # plot colorbar
        cb = plt.colorbar(cs, extend='both',  pad=0.04, orientation='horizontal', shrink=0.75)
        cb.ax.tick_params(labelsize=15) 
        cb.set_label(labelplt,size=15)
        ticks = np.linspace(levels.min(),levels.max(),Nbar)
        cb.set_ticks(ticks)
        new_tickslabels = ["%.2f" % i for i in ticks]
        cb.set_ticklabels(new_tickslabels)