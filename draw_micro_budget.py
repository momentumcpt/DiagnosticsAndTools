'''
    Microphys budgets
    zhunguo : guozhun@lasg.iap.ac.cn ; guozhun@uwm.edu
'''

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import pylab
import Common_functions
import os
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import cartopy.crs as ccr
import cmaps

from matplotlib import font_manager as fm
from scipy.interpolate import griddata
from subprocess import call

def draw_micro_bgt (ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,vname,cscale,chscale,pname,dofv,datapath):


# ncases, the number of models
# cases, the name of models
# casename, the name of cases
# climopath, model output filepath
# filepathobs, filepath for observational data
# inptrs = [ncases]
 if not os.path.exists(casedir):
        os.mkdir(casedir)

 infiles  = ['' for x in range(ncases)]
 ncdfs    = ['' for x in range(ncases)]
 nregions = nsite

 nvaris = len(varis)

 plotmicrobgt=['' for x in range(nsite*ncases)] 

 for ire in range (0, nsite):
     for im in range (0,ncases):
         if not os.path.exists(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N'):
             os.mkdir(casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N')

         plotname = casedir+'/'+str(lons[ire])+'E_'+str(lats[ire])+'N/'+pname+'_'+casenames[im]+'_'+str(lons[ire])+'E_'+str(lats[ire])+'N_'+cseason
         plotmicrobgt[im+ncases*ire] = pname+'_'+casenames[im]+'_'+str(lons[ire])+'E_'+str(lats[ire])+'N_'+cseason

         fig, axes = plt.subplots( nrows=nvaris//2, ncols=2, figsize=(15, 15 ))
         axes      = axes.flatten()

         for iv in range (0, nvaris):
             ax = axes[iv]

             if (varis[iv] == 'MPDLIQ' ):   # LIQ
                budget_ends = ['PRCO',  'PRAO', 'MNUCCCO', 'MNUCCTO', 'MSACWIO', 'PSACWSO', 'BERGSO','BERGO']
              # in fortran    prc*cld, pra*cld,mnuccc*cld,mnucct*cld,msacwi*cld,psacws*cld,bergs*cld, berg
              #               (-pra-prc-mnuccc-mnucct-msacwi- psacws-bergs)*lcldm-berg
                nterms = len (budget_ends)

             if (varis[iv] == 'MPDICE' ):    # ICE
                budget_ends = [ 'PRCIO', 'PRAIO', 'MSACWIO', 'MNUCCCO',  'MNUCCTO','mnudepo',   'BERGO',  'CMEIOUT','mnuccrio']
# in fortran                   prci*cld,prai*cld,msacwi*cld,mnuccc*cld, mnucct*cld,      berg, vap_dep + ice_sublim + mnuccd 
#                (mnuccc+mnucct+mnudep+msacwi)*lcldm+(-prci-prai)*icldm+(vap_dep+ice_sublim+mnuccd)+berg+mnuccri*precip_frac  
                nterms = len (budget_ends)

             if (varis[iv] == 'QRSEDTEN' ):  #  RAIN
                budget_ends = [ 'PRAO', 'PRCO',  'PRACSO',       'EVAPPREC', 'MNUCCRO','mnuccrio' ]
#                              pra*cld,prc*cld, psacs*prf, -pre*prf(nevapr),mnuccr*prf
#             (pra+prc)*lcldm+(pre-pracs- mnuccr-mnuccri)*precip_frac   
                nterms = len (budget_ends)

             if (varis[iv] == 'QSSEDTEN' ):  # SNOW
                budget_ends = [ 'PRAIO', 'PRCIO', 'PSACWSO', 'PRACSO','EVAPSNOW',  'MNUCCRO', 'BERGSO']
#                              prai*cld,prci*cld,psacws*cld,psacs*prf, -prds*prc, mnuccr*prf,bergs*cld 
#              (prai+prci)*icldm+(psacws+bergs)*lcldm+(prds+  pracs+mnuccr)*precip_frac
                nterms = len (budget_ends)

             if (varis[iv] == 'QISEVAP' ):  # Vapor
                budget_ends = [ 'EVAPPREC','EVAPSNOW','CMEIOUT','mnudepo' ]
               #          -pre*prf(nevapr),-prds*prc ,vap_dep + ice_sublim + mnuccd
#            -(pre+prds)*precip_frac-vap_dep-ice_sublim-mnuccd-mnudep*lcldm 
                nterms = len (budget_ends)

             if (varis[iv] == 'nnuccco' ):  # NUM of LIQ
                budget_ends = [ 'nnuccco', 'nnuccto', 'npsacwso', 'nsubco', 'nprao','nprc1o']
#                               nnuccc*cld,nnucct*cld,npsacws*cld,nsubc*cld,npra*cld,nprc1*cld
#                              (-nnuccc-nnucct-npsacws+nsubc-npra-nprc1)*lcldm
                nterms = len (budget_ends)
                 
             if (varis[iv] == 'nnuccdo' ):  # NUM of ICE
                budget_ends = [  'nnuccdo',  'nnuccto',  'tmpfrzo',  'nnudepo',  'nsacwio',  'nsubio',  'nprcio',  'npraio','nnuccrio','DETNICETND']
#                                nnuccd   ,nnucct*lcld,tmpfrz*lcld,nnudep*lcld,nsacwi*lcld,nsubi*icld,nprci*icld,nprai*icld,nnuccri*prf
#                                nnuccd+ (nnucct+tmpfrz+nnudep+nsacwi)*lcldm+(nsubi-nprci- nprai)*icldm+nnuccri*precip_frac
                nterms = len (budget_ends)




             ncdfs[im]  = datapath+cases[im]+'_site_location.nc'
             infiles[im]= climopath[im][0]+cases[im]+climopath[im][1]+cases[im]+'_'+cseason+'_climo.nc'
             inptrs = Dataset(infiles[im],'r')       # pointer to file1
             lat=inptrs.variables['lat'][:]
             nlat=len(lat)
             lon=inptrs.variables['lon'][:]
             nlon=len(lon)
             ilev=inptrs.variables['lev'][:]
             nilev=len(ilev)
             ncdf= Dataset(ncdfs[im],'r')
             n   =ncdf.variables['n'][:]
             idx_cols=ncdf.variables['idx_cols'][:,:]
             if (dofv[im]):
               idx_lats=ncdf.variables['idx_coord_lat'][:,:]
               idx_lons=ncdf.variables['idx_coord_lon'][:,:]
             ncdf.close()
             A_field = np.zeros((nterms,nilev),np.float32)
             theunits=str(chscale[iv])+'x'+inptrs.variables[budget_ends[0]].units


             for it in range(0, nterms):
                 for subc in range( 0, n[ire]):
                     varis_bgt= budget_ends[it]
                     npoint=idx_cols[ire,n[subc]-1]-1
                     if(dofv[im]):
                       npointlat=idx_lats[ire,0]
                       npointlon=idx_lons[ire,0]
                     if(dofv[im]):
                       tmp=inptrs.variables[varis_bgt][0,:,npointlat,npointlon]
                     else:
                       tmp=inptrs.variables[varis_bgt][0,:,npoint] #/n[ire]
                     tmp=tmp*cscale[iv]
                     if(dofv[im]):
                       lcldm=inptrs.variables['CLOUD'][0,:,npointlat,npointlon] 
                     else:
                       lcldm=inptrs.variables['CLOUD'][0,:,npoint] 
                     icldm=lcldm
                     if(dofv[im]):
                       precip_frac=inptrs.variables['FREQR'][0,:,npointlat,npointlon]
                     else:
                       precip_frac=inptrs.variables['FREQR'][0,:,npoint]

                     if (varis_bgt == 'MPDT' or varis_bgt == 'STEND_CLUBB' ):
                        tmp=tmp/1004

                     if (varis[iv] == 'MPDLIQ'):  # LIQ
                       if (varis_bgt == 'PRCO' or varis_bgt ==  'PRCIO' or varis_bgt == 'PRAO' or varis_bgt == 'PRAICSO' or varis_bgt == 'PRAIO' \
                          or varis_bgt == 'MNUCCCO' or varis_bgt == 'MNUCCTO' or varis_bgt == 'MSACWIO' or varis_bgt == 'PSACWSO' or varis_bgt == 'BERGSO' 
                          or varis_bgt == 'BERGO'):
                          tmp=tmp *(-1) 

                     if (varis[iv] == 'MPDICE'):  # ICE
                        if ( varis_bgt == 'PRCIO' or varis_bgt == 'PRAIO' ):                 
                           tmp=tmp *(-1)

                     if (varis[iv] == 'QRSEDTEN'):  # RAIN
                        if ( varis_bgt == 'MNUCCRO'  or varis_bgt == 'PRACSO' or varis_bgt == 'EVAPPREC' or varis_bgt == 'mnuccrio'):
                           tmp=tmp*(-1)

                     if (varis[iv] == 'QSSEDTEN'):  # SNOW
                        if ( varis_bgt == 'EVAPSNOW' ):
                           tmp= tmp*(-1)

                     if (varis[iv] == 'QISEVAP'):  # Vapor
                        if ( varis_bgt == 'CMEIOUT' or varis_bgt == 'mnudepo' ):
                           tmp=-1* tmp

                     if (varis[iv] == 'nnuccco' ):  # NUM of LIQ
                        if ( varis_bgt == 'nnuccco' or varis_bgt == 'nnuccto' or varis_bgt == 'npsacwso' or varis_bgt == 'nprao' or varis_bgt == 'nprc1o'):
                           tmp=-1* tmp 

                     if (varis[iv] == 'nnuccdo' ):  # NUM of ICE
                        if ( varis_bgt == 'nprcio' or varis_bgt == 'npraio'):
                           tmp=-1* tmp

                     A_field[it,:] = (A_field[it,:]+tmp[:]/n[ire]).astype(np.float32 )

                 ax.plot(A_field[it, :],ilev, label=varis_bgt[:])
             inptrs.close()
             ax.set_title(f'({varis[iv] if iv < len(varis) else "Unknown"})')
             levind= top_level//1000*72
             if (np.abs(np.min(A_field[:, levind:])) <= 0.001*np.abs(np.max(A_field[:, levind:]))):
                 lest=0
             else:
                 lest=np.min(A_field[:, levind:])
             maximum = np.max(A_field[:, levind:])
             ax.set_xlim(lest,maximum)

             ax.set_ylim(bottom=top_level, top=1000)
             ax.set_xlabel('Value')
             ax.grid(True)
             ax.set_ylabel('Pressure Level (hPa)')
             ax.set_xlabel(theunits)
             ax.legend()
             ax.invert_yaxis()

         title_text = pname+f"{cases[im]} MICROP BUDGET at {lons[ire]}E, {lats[ire]}N"
         fig.suptitle(title_text,fontsize=16, ha='center', va='center')
         plt.tight_layout(rect=[0, 0, 1, 0.96])
         plt.savefig(plotname+'.'+ptype, dpi=pixel)
         plt.close()

 return (plotmicrobgt)

