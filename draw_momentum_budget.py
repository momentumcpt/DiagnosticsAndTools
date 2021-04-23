'''        
    Profiles of momentum budgets in CAM
    Based on the momentum diagnostics from Chris Kruse
    zhunguo : guozhun@lasg.iap.ac.cn ; guozhun@uwm.edu
'''


import Ngl
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pylab
import os
from subprocess import call

def draw_mom_bgt (ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs,casedir,varis,cscale,chscale,pname,dofv):

# ptype,
# cseason,
# ncases, the number of models 
# cases, the name of models
# casenames, the name of cases
# nsite,
# lats,
# lons,
# filepath, model output filepath
# filepathobs, filepath for observational data
# casedir,
# varis,
# cscale,
# chscale,
# pname, Plot section name
# dofv, If true, calc locations for FV dycore data (structured grids)

# Momentum budget terms:
# 'UTEND_DCONV', 'UTEND_SHCONV', 'UTEND_MACROP', 'UTEND_VDIFF', 'UTEND_RAYLEIGH', 
# 'UTEND_GWDTOT', 'UTEND_QBORLX', 'UTEND_LUNART', 'UTEND_IONDRG', 'UTEND_NDG',  'UTEND_CORE' 
# All units of m/s2

 if not os.path.exists(casedir):
        os.mkdir(casedir)

 _Font   = 25
 interp = 2
 extrap = False
 mkres = Ngl.Resources()
 mkres.gsMarkerIndex = 2
 mkres.gsMarkerColor = "Red"
 mkres.gsMarkerSizeF = 15.
 infiles  = ["" for x in range(ncases)]
 ncdfs    = ["" for x in range(ncases)]
 nregions = nsite

# varisobs = [ "CLOUD", "OMEGA","SHUM","CLWC_ISBL", "THATA","RELHUM"]
 nvaris = len(varis)
# cunits = ["%", "mba/day","g/kg","g/kg","K", "%", "mba/day", "K", "g/kg", "m/s", "m/s","K","m"]
# cscaleobs = [100., 100/86400., 1., 1000, 1., 1., 1, 1,1,1]
# obsdataset =["CCCM", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI", "ERAI","ERAI","ERAI"]

plotstd=["" for x in range(nsite)]


 for ire in range (0, nsite):
     if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
         os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')

     plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/'+pname+'_'+str(lons[ire])+"E_"+str(lats[ire])+\
"N_"+cseason
     plotstd[ire] = pname+'_'+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
     wks= Ngl.open_wks(ptype,plotname)

     Ngl.define_colormap(wks,"GMT_paired")
     plot = []
     res     = Ngl.Resources()
     res.nglDraw              = False
     res.nglFrame             = False
     res.lgLabelFontHeightF     = .02                   # change font height                                      
     res.lgPerimOn              = False                 # no box around                                           
     res.vpWidthF         = 0.30                      # set width and height                                      
     res.vpHeightF        = 0.30
     #res.vpXF             = 0.04                                                                                 
     # res.vpYF             = 0.30                                                                                
     res.tmYLLabelFont  = _Font
     res.tmXBLabelFont  = _Font
     res.tmXBLabelFontHeightF = 0.01
     res.tmXBLabelFontThicknessF = 2.0
     res.xyMarkLineMode      = "Lines"
     res.xyLineThicknesses = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0,3.,3.,3.,3.,3,3,3,3,3,3,3]

     res.xyDashPatterns    = np.arange(0,24,1)
#     res.xyMarkers         = np.arange(16,40,1)                                                                  
#     res.xyMarkerSizeF       = 0.005 

     pres            = Ngl.Resources()
     pres.nglMaximize = True
     pres.nglFrame = False
     pres.txFont = _Font
     pres.nglPanelYWhiteSpacePercent = 5
     pres.nglPanelXWhiteSpacePercent = 5
     pres.nglPanelTop = 0.88
     pres.wkWidth = 5000
     pres.wkHeight = 5000

     for iv in range (0, nvaris):
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
             res.lgPerimOn              = True
         else:
             res.pmLegendDisplayMode    = "NEVER"

         for im in range (0,ncases):
             ncdfs[im]  = './data/'+cases[im]+'_site_location.nc'
             infiles[im]= filepath[im]+'/'+cases[im]+'_'+cseason+'_climo.nc'
             inptrs = Dataset(infiles[im],'r')       # pointer to file1                                           
             lat=inptrs.variables['lat'][:]
             nlat=len(lat)
             lon=inptrs.variables['lon'][:]
             nlon=len(lon)
             lev=inptrs.variables['ilev'][:]
             nlev=len(lev)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             if (dofv):
                 idx_lats=ncdf.variables['idx_coord_lat'][:,:]
                 idx_lons=ncdf.variables['idx_coord_lon'][:,:]
             ncdf.close()
             if (im ==0):
                 A_field = np.zeros((ncases,nlev),np.float32)

             for subc in range( 0, n[ire]):
                 npoint=idx_cols[ire,n[subc]-1]-1
                 if(dofv):
                     npointlat=idx_lats[ire,0]
                     npointlon=idx_lons[ire,0]
                 if (dofv):
                     tmp=inptrs.variables[varis[iv]][0,:,npointlat,npointlon]
                 else:
                     tmp=inptrs.variables[varis[iv]][0,:,npoint]

                 A_field[im,:] = (A_field[im,:]+tmp[:]/n[ire]).astype(np.float32 )

             A_field[im,:] = A_field[im,:] *cscale[iv]

             inptrs.close()

         res.tiMainString      = varis[iv]+"  "+theunits
         res.trYReverse        = True
         res.xyLineColors      = np.arange(3,20,2)
         res.xyMarkerColors    = np.arange(2,20,2)
         p = Ngl.xy(wks,A_field,lev,res)
         plot.append(p)

     pres.txString   = "MOMENTUM BUDGET at"+ str(lons[ire])+"E,"+str(lats[ire])+"N"

     txres = Ngl.Resources()
     txres.txFontHeightF = 0.02
     txres.txFont        = _Font
     Ngl.text_ndc(wks,"MOMENTUM BUDGET at"+ str(lons[ire])+"E,"+str(lats[ire])+"N",0.5,0.92+ncases*0.01,txres)
     Common_functions.create_legend(wks,casenames,0.02,np.arange(3,20,2),0.1,0.89+ncases*0.01)

     Ngl.panel(wks,plot[:],[nvaris/3,3],pres)
     Ngl.frame(wks)
     Ngl.destroy(wks)

 return (plotbgt)
