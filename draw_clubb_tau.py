'''
    CLUBB budgets
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
import Common_functions


 
def draw_clubb_tau (ptype,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs,casedir,varis,vname,cscale,chscale,pname,datapath):

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
 infiles  = ["" for x in range(ncases)]
 ncdfs    = ["" for x in range(ncases)]
 nregions = nsite
 nvaris = len(varis)
 plottau=["" for x in range(nsite*ncases)] 
 alphas   = ['a) ','b) ','c) ','d) ','e) ','f) ','g) ','h) ','i) ', 'j) ', 'k) ', 'l) ', 'm) ', 'n) ', 'o) ', 'p) ', 'q) ', 'r) ', 's) ', 't) ', 'u) ', 'v) ', 'w) ', 'x) ', 'y) ', 'z) ']

 for ire in range (0, nsite):
     for im in range (0,ncases):
         if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
             os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')

         plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/'+pname+'_'+casenames[im]+"_"+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason
         plottau[im+ncases*ire] = pname+'_'+casenames[im]+"_"+str(lons[ire])+"E_"+str(lats[ire])+"N_"+cseason

         wks= Ngl.open_wks(ptype,plotname)

         Ngl.define_colormap(wks,"radar")
         plot = []
         res     = Ngl.Resources()  
         res.nglMaximize          =  False

         res.nglDraw              = False
         res.nglFrame             = False
         res.vpWidthF         = 0.30                      # set width and height
         res.vpHeightF        = 0.30
#         if (lats[ire] > 0 and lons[ire]!=240 ):
#             res.trYMinF = 400.
#             res.trYMaxF = 1000.
#         else:
         res.trYMinF = 100.
         res.trYMaxF = 1000.

         res.tiMainFont        = _Font
         res.tmYLLabelFont  = _Font
         res.tmXBLabelFont  = _Font
         res.tiYAxisFont =  _Font
         res.tiXAxisFont =  _Font


         res.tmXBLabelFontHeightF = 0.01
         res.tmXBLabelFontThicknessF = 1.0
         res.xyMarkLineMode      = "MarkLines"
         res.xyLineThicknesses = [3.0, 3.0, 3.0, 3.0, 3.0, 3.0,3.,2.,2.,2.,2,2,2,2,2,2,2]
         res.xyDashPatterns    = np.arange(0,24,1)
         res.xyMarkers         = np.arange(16,40,1)
         res.xyMarkerSizeF       = 0.005
         res.pmLegendDisplayMode    = "Never"
         res.pmLegendSide           = "top"                 # Change location of
         res.pmLegendParallelPosF   = 0.75                  # move units right
         res.pmLegendOrthogonalPosF = -0.65                  # more neg = down
         res.pmLegendWidthF         = 0.1                   # Change width and
         res.pmLegendHeightF        = 0.15                  # height of legend.
         res.lgLabelFontHeightF     = .02                   # change font height
         res.lgLabelFontThicknessF  = 1.
#         res.lgBoxMinorExtentF      = 0.2
         res.lgPerimOn              = True
         res.tiYAxisString   = "Pressure [hPa]"
     
         res.trYReverse        = True

         pres            = Ngl.Resources()
         pres.nglFrame = False
         pres.txFont = _Font
         pres.nglPanelYWhiteSpacePercent = 5
         pres.nglPanelXWhiteSpacePercent = 5
         pres.nglPanelTop = 0.93
         pres.txFont = _Font
         pres.nglMaximize = False
         pres.txFont     = _Font
         pres.nglPanelTop                      = 0.935
         pres.nglPanelFigureStrings            = alphas
         pres.nglPanelFigureStringsJust        = 'Topright'
         pres.nglPanelFigureStringsFontHeightF = 0.015




         for iv in range (0, nvaris):

             if (varis[iv] == 'tau_no_N2_zm' ):
                 budget_ends = ['tau_no_N2_zm', 'bkgnd',  'sfc',  'shear']
                 budget_name = ['1/~F8~t~N~~F10~~B~noN2~N~','1/~F8~t~N~~F10~~B~bkgnd~N~','1/~F8~t~N~~F10~~B~surf~N~','1/~F8~t~N~~F10~~B~shear~N~']
                 nterms = len (budget_ends)

             if (varis[iv] == 'tau_xp2_zm' ):
                 budget_ends = [ 'tau_xp2_zm', 'tau_no_N2_zm']
                 budget_name = ["1/~F8~t~N~~F10~~B~x'~S~2~N~~N~",'1/~F8~t~N~~F10~~B~noN2~N~']
                 nterms = len (budget_ends)

             if (varis[iv] == 'tau_wp2_zm' ):
                 budget_ends = ['tau_wp2_zm',  'tau_no_N2_zm', 'bvpos']
                 budget_name = ["1/~F8~t~N~~F10~~B~w'~S~2~N~~N~",'1/~F8~t~N~~F10~~B~noN2~N~','1/~F8~t~N~~F10~~B~bv~N~']
                 nterms = len (budget_ends)

             if (varis[iv] == 'tau_wpxp_zm' ):
                 budget_ends = ['tau_wpxp_zm', 'tau_no_N2_zm', 'bvpos', 'clear']
                 budget_name = ["1/~F8~t~N~~F10~~B~w'x'~N~","1/~F8~t~N~~F10~~B~noN2~N~",'1/~F8~t~N~~F10~~B~bv~N~','1/~F8~t~N~~F10~~B~clr~N~']
                 nterms = len (budget_ends)

             if (varis[iv] == 'tau_wp3_zm' ):
                 budget_ends = [ 'tau_wpxp_zm', 'tau_no_N2_zm', 'bvpos', 'clear']
                 budget_name = ["1/~F8~t~N~~F10~~B~w'x'~N~",'1/~F8~t~N~~F10~~B~noN2~N~','1/~F8~t~N~~F10~~B~bv~N~','1/~F8~t~N~~F10~~B~clr~N~']
                 nterms = len (budget_ends)



             ncdfs[im]  = datapath+cases[im]+'_site_location.nc'
             infiles[im]= filepath[im]+'/'+cases[im]+'_'+cseason+'_climo.nc'
             inptrs = Dataset(infiles[im],'r')       # pointer to file1
             lat=inptrs.variables['lat'][:]
             nlat=len(lat)
             lon=inptrs.variables['lon'][:]
             nlon=len(lon)
             ilev=inptrs.variables['ilev'][:]
             nilev=len(ilev)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             ncdf.close()
             A_field = np.zeros((nterms,nilev),np.float32)

         
             if (varis[iv] == 'tau_no_N2_zm' or varis[iv] == 'tau_wp2_zm' or varis[iv] == 'tau_xp2_zm' or varis[iv] == 'tau_wp3_zm' or varis[iv] == 'tau_wpxp_zm' ):
                theunits=str(chscale[iv])+'~F10~'+inptrs.variables[varis[iv]].units+'~S~-1~N~'
             else:
                theunits=str(chscale[iv])+'~F10~'+inptrs.variables[varis[iv]+'_bt'].units
  
             res.tiXAxisString   = '1/~F8~t~N~~F25~~B~'+vname[iv]+"~N~  "+ '  Unit=  ' + theunits

             res1 = Ngl.Resources()
             res1 = res



             for it in range(0, nterms):
                 for subc in range( 0, n[ire]):
                     npoint=idx_cols[ire,n[subc]-1]-1

                     if (varis[iv] == 'tau_wp2_zm' or varis[iv] == 'tau_xp2_zm' or varis[iv] == 'tau_wp3_zm' or varis[iv] == 'tau_wpxp_zm' or varis[iv] == 'tau_no_N2_zm'): 
                         varis_tau=budget_ends[it]

                         if ( varis_tau == 'bkgnd' or varis_tau == 'shear' \
                            or varis_tau == 'sfc' ):
                            tmp=inptrs.variables['invrs_tau_'+varis_tau][0,:,npoint]

                         if ( varis_tau == 'tau_no_N2_zm' ): 
                            tmp=inptrs.variables[varis_tau][0,:,npoint]
                            tmp=1/tmp
   
                         if (varis[iv] == 'tau_wp2_zm' ):
                            if ( varis_tau == 'tau_wp2_zm' ):
                               tmp=inptrs.variables[varis_tau][0,:,npoint]
                               tmp=1/ tmp
                            if ( varis_tau == 'bvpos' ):
                               tmp0=inptrs.variables['tau_wp2_zm'][0,:,npoint]
                               tmp1=inptrs.variables['tau_no_N2_zm'][0,:,npoint]
                               tmp=tmp0
                               tmp=1/tmp0-1/tmp1

                         if (varis[iv] == 'tau_zm' ):
                            if ( varis_tau == 'tau_zm' ):
                               tmp=inptrs.variables[varis_tau][0,:,npoint]
                               tmp=1/ tmp
                            if ( varis_tau == 'bvpos' ):
                               tmp0=inptrs.variables['tau_zm'][0,:,npoint]
                               tmp1=inptrs.variables['tau_no_N2_zm'][0,:,npoint]
                               tmp=tmp0
                               tmp=1/tmp0-1/tmp1

                         if (varis[iv] == 'tau_xp2_zm' ): 
                            if ( varis_tau == 'tau_xp2_zm' ):
                               tmp=inptrs.variables[varis_tau][0,:,npoint]
                               tmp=1/ tmp
                            if ( varis_tau == 'Rich' ):
                               tmp0=inptrs.variables['tau_xp2_zm'][0,:,npoint]
                               tmp1=inptrs.variables['tau_no_N2_zm'][0,:,npoint]
                               tmp=tmp0
                               tmp=1/tmp0/(1/tmp1)/1000

                         if (varis[iv] == 'tau_wp3_zm' ): 
                            if ( varis_tau == 'tau_wp3_zm' or varis_tau == 'tau_wpxp_zm'):
                               tmp=inptrs.variables[varis_tau][0,:,npoint]
                               tmp=1/ tmp
                               tmp[0:10]=0
                            if ( varis_tau == 'bvpos' ):
                               tmp0=inptrs.variables['tau_wp2_zm'][0,:,npoint]
                               tmp1=inptrs.variables['tau_no_N2_zm'][0,:,npoint]
                               tmp=tmp0
                               tmp=1/tmp0-1/tmp1
                            if ( varis_tau == 'clear' ):
                               tmp0=inptrs.variables['tau_wp3_zm'][0,:,npoint]
                               tmp1=inptrs.variables['tau_wp2_zm'][0,:,npoint]
                               tmp=tmp0
                               tmp=1/tmp0-1/tmp1
                               tmp[0:10]=0

                         if (varis[iv] == 'tau_wpxp_zm' ):
                            if ( varis_tau == 'tau_wpxp_zm' or varis_tau == 'tau_zm'):
                               tmp=inptrs.variables[varis_tau][0,:,npoint]
                               tmp=1/ tmp
                            if ( varis_tau == 'bvpos' ):
                               tmp0=inptrs.variables['tau_zm'][0,:,npoint]
                               tmp1=inptrs.variables['tau_no_N2_zm'][0,:,npoint]
                               tmp=tmp0
                               tmp=2/tmp0-1/tmp1
                            if ( varis_tau == 'clear' ):
                               tmp0=inptrs.variables['tau_wpxp_zm'][0,:,npoint]
                               tmp1=inptrs.variables['tau_zm'][0,:,npoint]
                               tmp=tmp0
                               tmp=1/tmp0/5-2/tmp1

                     else: 
                         varis_tau=varis[iv]+budget_ends[it]
                         tmp0=inptrs.variables[varis[iv]][0,:,npoint]
                         tmp=inptrs.variables[varis_tau][0,:,npoint] 

                     tmp=tmp*cscale[iv]
                     A_field[it,:] = (A_field[it,:]+tmp[:]/n[ire]).astype(np.float32 )

             inptrs.close()

             res.pmLegendDisplayMode    = "Never"

             if(varis[iv] == 'tau_wp3_zm') :
                 res.trXMinF = 0
                 res.trXMaxF = 450
                 res.xyMarkerColors      = ['black','orange','purple','firebrick']
                 res.xyLineColors        = ['black','orange','purple','firebrick']

             if(varis[iv] == 'tau_no_N2_zm') :
                 res.trXMinF = 0
                 res.trXMaxF = 20
                 res.xyMarkerColors      = ['black','red','green','blue']
                 res.xyLineColors        = ['black','red','green','blue']

             if(varis[iv] == 'tau_wp2_zm') :
                 res.trXMinF = 0
                 res.trXMaxF = 12
                 res.xyMarkerColors      = ['black','orange','purple']
                 res.xyLineColors        = ['black','orange','purple']


             if(varis[iv] == 'tau_xp2_zm') :
                 res.trXMinF = 0
                 res.trXMaxF = 35
                 res.xyMarkerColors      = ['black','orange']
                 res.xyLineColors        = ['black','orange']



             p = Ngl.xy(wks,A_field,ilev,res)
             plot.append(p)



             xp=np.mod(iv,2)
             yp=int(iv/2)
             

             if(varis[iv] == 'tau_wp3_zm') :
                 res.trXMinF = 0
                 res.trXMaxF = 450
                 res.xyMarkerColors      = ['black','orange','purple','firebrick']
                 res.xyLineColors        = ['black','orange','purple','firebrick']
                 Common_functions.create_legend(wks,budget_name[:],0.02,['black','orange','purple','firebrick'],0.3+xp*0.5,0.8-yp*0.5)


             if(varis[iv] == 'tau_no_N2_zm') :
                 res.trXMinF = 0
                 res.trXMaxF = 20
                 res.xyMarkerColors      = ['black','red','green','blue']
                 res.xyLineColors        = ['black','red','green','blue']
                 Common_functions.create_legend(wks,budget_name[:],0.02,['black','red','green','blue'],0.3+xp*0.5,0.8-yp*0.5)


             if(varis[iv] == 'tau_wp2_zm') :
                 res.trXMinF = 0
                 res.trXMaxF = 12
                 res.xyMarkerColors      = ['black','orange','purple']
                 res.xyLineColors        = ['black','orange','purple']
                 Common_functions.create_legend(wks,budget_name[:],0.02,['black','orange','purple'],0.3+xp*0.5,0.8-yp*0.5)

             if(varis[iv] == 'tau_xp2_zm') :
                 res.trXMinF = 0
                 res.trXMaxF = 35
                 res.xyMarkerColors      = ['black','orange']
                 res.xyLineColors        = ['black','orange']
                 Common_functions.create_legend(wks,budget_name[:],0.02,['black','orange'],0.3+xp*0.5,0.8-yp*0.5)



         Ngl.panel(wks,plot[:],[nvaris/2,2],pres)
         txres = Ngl.Resources()
         txres.txFont = _Font
         txres.txFontHeightF = 0.020
         
         Ngl.text_ndc(wks,casenames[im]+"  BUDGET at " +str(lons[ire])+"E,"+str(lats[ire])+"N",0.5,0.95,txres)
         Ngl.frame(wks)
         Ngl.destroy(wks) 

 return (plottau)

