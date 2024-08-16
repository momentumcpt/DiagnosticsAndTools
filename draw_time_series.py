'''
    CLUBB skewness functions
    zhunguo : guozhun@lasg.iap.ac.cn ; guozhun@uwm.edu
'''

import glob
import Ngl
from netCDF4 import Dataset
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pylab
import os
import Common_functions

from subprocess import call


def ts_plots(ptype,cseason, varis, ncases, cases, casenames, nsite, lats, lons,years,nyear, filepath, filepathobs,casedir, dofv,datapath):

# ncases, the number of models
# cases, the name of models
# casename, the name of cases
# filepath, model output filepath
# filepathobs, filepath for observational data
# inptrs = [ncases]
 if not os.path.exists(casedir):
        os.mkdir(casedir)

 _Font   = 25
 interp = 2
 extrap = False
 mkres = Ngl.Resources()
 mkres.gsMarkerIndex = 2
 mkres.gsMarkerColor = "Red"
 mkres.gsMarkerSizeF = 15.
 #infiles  = [[] for x in range(ncases)]
 ncdfs    = ["" for x in range(ncases)]
 nregions = nsite

# varis    = [ "TS", "CLDLOW", "SHFLX", "LHFLX", "FSNS", "FLNS", \
#              "SWCF", "LWCF", "PRECC", "PRECL", "PRECT", "FSNT", \
#              "FLNT", "TMQ", "PSL", "TGCLDLWP", "TGCLPIWP", "U10" ]
 nvaris = len(varis)
 cscale = [1, 1, 1, 1, 1., 1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
 plotts=["" for x in range(nsite)]


 # NEED to concatenate the relevant files.
 # right now this just takes the years and nyears from the main python file, 
 # it doesn't deal with the extra two months
 varstring = ""
 for i in range(nvaris):
   varstring = varstring + f"{varis[i]},"

 for im in range(ncases):
   if not os.path.exists(datapath+"/temp"):
     os.mkdir(datapath+"/temp")
   histlist=[]
   for iy in range(nyear[im]):
     histlist=histlist+sorted(glob.glob(filepath[im]+f"/*cam.h0a."+str(years[im]+iy).rjust(4,'0')+"*"))
   for ifile,file in enumerate(histlist):
     os.system(f"ncea -v {varstring[0:-1]} {file} -o {datapath}/temp/{casenames[im]}_"+str(ifile).rjust(2,'0')+".nc")
   os.system(f"ncrcat {datapath}/temp/*.nc {datapath}/{casenames[im]}_timeseries.nc")
   os.system(f"rm -rf {datapath}/temp")


 for ire in range (0, nsite):
     if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
         os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')

     plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/CLUBB_time_series_'+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
     plotts[ire] = 'CLUBB_time_series_'+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
     wks= Ngl.open_wks(ptype,plotname)

     Ngl.define_colormap(wks,"GMT_paired")
     plot = []
     res     = Ngl.Resources()
     res.nglDraw              = False
     res.nglFrame             = False
     res.lgLabelFontHeightF     = .012                   # change font height
     res.lgPerimOn              = False                 # no box around
     res.vpWidthF         = 0.30                      # set width and height
     res.vpHeightF        = 0.30
     #res.vpXF             = 0.04
     # res.vpYF             = 0.30
     res.tmYLLabelFont  = _Font
     res.tmXBLabelFont  = _Font 
     res.tmXBLabelFontHeightF = 0.01
     res.tmXBLabelFontThicknessF = 1.0
#     res.tmXBLabelAngleF = 45
     res.xyMarkLineMode      = "Lines"
     res.xyLineThicknesses = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0,3.,3.,3.,3.,3,3,3,3,3,3,3]

     res.xyDashPatterns    = np.arange(0,24,1)
#     res.xyMarkers         = np.arange(16,40,1)
#     res.xyMarkerSizeF       = 0.005


     pres            = Ngl.Resources()
#     pres.nglMaximize = True
     pres.nglFrame = False
     pres.txFont = _Font
     pres.nglPanelYWhiteSpacePercent = 5
     pres.nglPanelXWhiteSpacePercent = 5
     pres.nglPanelTop = 0.88
     pres.wkWidth = 2500
     pres.wkHeight = 2500


     for iv in range (0, nvaris):
         print(varis[iv]) 
         if(iv == nvaris-1):
             res.pmLegendDisplayMode    = "NEVER"
             res.xyExplicitLegendLabels = casenames[:]
             res.pmLegendSide           = "top"             
             res.pmLegendParallelPosF   = 0.6               
             res.pmLegendOrthogonalPosF = -0.5                  
             res.pmLegendWidthF         = 0.10              
             res.pmLegendHeightF        = 0.10          
             res.lgLabelFontHeightF     = .02               
             res.lgLabelFontThicknessF  = 1.5
             res.lgPerimOn              = False
         else:
             res.pmLegendDisplayMode    = "NEVER"


         for im in range (0,ncases):
             ncdfs[im]  = datapath+"/"+cases[im]+'_site_location.nc'
             infiles=f"{datapath}/{casenames[im]}_timeseries.nc" 
#             for i in range(nyear[im]):
#                 infiles=infiles+filepath[im]+f"/*cam.h0."+str(years[im]+i).rjust(4,'0')+"*"
             print("infiles = ",infiles)
             inptrs = xr.open_dataset(infiles)       # pointer to file1
             lat=np.array(inptrs['lat'][:])
             nlat=len(lat)
             lon=np.array(inptrs['lon'][:])
             nlon=len(lon)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             if (dofv):
                idx_lats=ncdf.variables['idx_coord_lat'][:,:]
                idx_lons=ncdf.variables['idx_coord_lon'][:,:]
             ncdf.close()
             if (im ==0):
                 ntime = nyear[im]*12   #TODO: fix this up real nice
                 A_field = np.zeros((ncases,ntime),np.float32)

             for subc in range( 0, n[ire]):
                 npoint=idx_cols[ire,n[subc]-1]-1
                 if(dofv):
                   npointlat=idx_lats[ire,0]
                   npointlon=idx_lons[ire,0]
                   tmp=np.array(inptrs[varis[iv]])[:,npointlat,npointlon] 
                 else:
                   tmp=np.array(inptrs[varis[iv]])[:,npoint]
                 theunits=str(cscale[iv])+inptrs[varis[iv]].units
                 print("A_field.shape, tmp.shape = ",A_field.shape,tmp.shape)
                 A_field[im,:] = (A_field[im,:]+tmp[:]/n[ire]).astype(np.float32 )
             A_field[im,:] = A_field[im,:] *cscale[iv]
             inptrs.close()
         res.tiMainString    =  varis[iv]+"  "+theunits
#         res.trXMinF = min(np.min(A_field[0, :]))
#         res.trXMaxF = max(np.max(A_field[0, :]))
         res.trYReverse        = False #True
         res.xyLineColors      = np.arange(3,20,2)
         res.xyMarkerColors    = np.arange(2,20,2)
         p = Ngl.xy(wks,np.arange(ntime),A_field,res)
         
         plot.append(p)

     pres.txString   = "Time Series at"+ str(lons[ire])+"E,"+str(lats[ire])+"N"
     txres = Ngl.Resources()
     txres.txFontHeightF = 0.020
     txres.txFont        = _Font
     Ngl.text_ndc(wks,"Time Series at"+ str(lons[ire])+"E,"+str(lats[ire])+"N",0.5,0.92+ncases*0.01,txres)
     Common_functions.create_legend(wks,casenames,0.02,np.arange(3,20,2),0.1,0.89+ncases*0.01)


     Ngl.panel(wks,plot[:],[nvaris/3,3],pres)
     Ngl.frame(wks)
     Ngl.destroy(wks)

 os.system(f"rm {datapath}/*timeseries*")

 return plotts


     

