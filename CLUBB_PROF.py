# -*- coding: utf-8 -*-
'''
CLUBB Diagnostics package for both CAM and EAM

Main code to make 1) 2D plots,2) profiles, 3) budgets on selected stations, 
         and then build up  webpages  etc
    Zhun Guo : guozhun@lasg.iap.ac.cn ; guozhun@uwm.edu
    Kate Thayer-Calder : katec@ucar.edu
    Benjamin A. Stephens:stepheba@ucar.edu

'''

## ==========================================================
# Begin User Defined Settings
# User defined name used for this comparison, this will be the name 
#   given the directory for these diagnostics
case='taus_144_zhun'

#outdir="/data/zhun/csmruns/" # where is the diag outputs?
outdir="/glade/work/stepheba/post/DiagnosticsAndTools/diags_output/"

#location of the model output data
filepath=[\
["/glade/derecho/scratch/stepheba/archive/","/atm/hist/"],\
["/data/zhun/csmruns/","/run/"],\
["/data/zhun/csmruns/","/run/"],\
]

#location for climatology files
climopath=[\
["/glade/derecho/scratch/stepheba/archive/","/"],\
["/data/zhun/csmruns/","/"],\
["/data/zhun/csmruns/","/"],\
]

#location for regridded data
regridpath=[\
["/glade/derecho/scratch/stepheba/archive/","/atm/hist/climo/"],\
["/data/zhun/csmruns/","/run/climo/"],\
["/data/zhun/csmruns/","/run/climo/"],\
]

#location of the "run" directory with the atm_in file
runfilepath=[\
["/glade/derecho/scratch/stepheba/archive/","/atm/hist/"],\
["/data/zhun/csmruns/","/run/"],\
["/data/zhun/csmruns/","/run/"],\
]

cases=[ \
"FCSD_f09_taus9",\
#"F2000_f09_taus9",\
]

# Start year of the runs? and how many model years it takes?
years=[\
        2005,    1,  1979]
nyear=[\
           1,    1,     1]

# Affiliations, Please confirm the naming of the schema history file. Sometimes it's eam, sometimes it's cam or something else that can be declared here.
affl   =['cam','cam','eam']
# suffix, Usually eam and cam use the same suffix, e.g. h0, h1, etc. But sometimes it's h0a, h1a, etc.It's better to make sure, otherwise the cal_mean function doesn't work.
suffix =['h0a','h0a','h0']
       
# Give a short name for your experiment which will appears on plots
casenames=cases #["037_f2c","044_f2c","044_f2c_sfc0.2","044_f2c_gammashear"]

# If using FV, please set 'calfvsite' to True, as the data structure is slightly different. 
calfvsite        = [\
       True, True,False]       

# NOTE, 'dpsc', namly deep scheme, has to be 'none', if silhs is turned on.
dpsc             = [\
        'zm','zm','zm']

# mpsc, microphy scheme, can be P3 or MG
mpsc             = [ 'MG','MG','P3']

# Although this is not required for CLUBB diagnostic package, in order to call the other diagnostic packages (E3SM or AMWG), we need to diff the SE grid to lat-lon coordinates. This is where mapfiles are needed. 
mapfile = [\
'/data/zhun/climatology/map_fv09_g17_to_360x180.nc',\
'/data/zhun/climatology/map_fv09_g17_to_360x180.nc',\
'/data/zhun/climatology/map_fv09_g17_to_360x180.nc',\
]

#ncopath ='/blues/gpfs/home/software/anaconda3/2021.11/envs/nco/bin/'
ncopath ='/public/software/apps/nco-4.8.1/intel/bin/'

# Observation Data
filepathobs='/data/zhun/climatology/'
#filepathobs='/global/project/projectdirs/m2689/zhun/amwg/obs_data_20140804/'
#filepathobs='/blues/gpfs/home/ac.zguo/amwg_diag_20140804/obs_data_20140804/'
#filepathobs='/glade/campaign/cgd/amp/amwg/amwg_data/obs_data/' #'/glade/p/cesm/amwg/amwg_data/obs_data/'

#tuning parameters:
list_of_parameters=['clubb_c7','clubb_c11','clubb_gamma_coef','clubb_c8','clubb_c_k10','clubb_c_invrs_tau_N2','clubb_c_invrs_tau_wpxp_n2_thresh','clubb_altitude_threshold','clubb_c_invrs_tau_bkgnd','clubb_c_invrs_tau_sfc','clubb_c_invrs_tau_n2_wp2','clubb_C_invrs_tau_wpxp_Ri','clubb_c_invrs_tau_n2_wpxp','clubb_c_invrs_tau_shear','clubb_c_invrs_tau_n2_xp2','clubb_c_k8','clubb_nu1','clubb_nu2','clubb_c_invrs_tau_n2_clear_wp3','clubb_c_wp2_splat','cldfrc_dp2','clubb_c_invrs_tau_n2','clubb_z_displace','micro_mg_dcs','micro_mg_autocon_lwp_exp']

#------------------------------------------------------------------------
# Setting of plots.
ptype         ='png'   # eps, pdf, ps, png, x11, ... are supported by this package
pixel         = 100    # 
cseason       ='ANN'   # Seasons, or others
casename      = case+'_'+cseason
datapath      = outdir+casename+'/'   # Set the path of the site files and Regional files.
#------------------------------------------------------------------------

calmean          = False       # make mean states
findout          = False       # pick out the locations of your sites
draw2d           = True        # 2D plots, SWCF etc.
drawdif          = True        # 2D Bias and RMSE, BE SURE mapfiles are given!

drawlarge        = True       # profiles for large-scale variable on your sites 
drawclubb        = True       # profiles for standard output of CLUBB
drawskw          = False      # profiles for skewness functions of CLUBB
drawts           = True       # plot time series of a few variables
drawbgt          = False      # budgets of CLUBB prognostic Eqs 
drawhostbgt      = False      # host model tendency,eg. CAM and EAM
drawmicrobgt     = False      # MG2 budget

drawhyd          = False      # profiles for SNOW, Rain etc.
drawp3           = False      # Or, P3's profiles
drawaero         = False      # AERO for cloud brone

# ONLY for SILHS
drawhf           = False      # Tendency of holl filler 
drawsilhs        = False      # profiles for silhs variables

makeweb          = True        # Make a webpage?
maketar          = False        # Tar them?

area  = 1.5

# Note, this para helps to find out the 'ncol' within
# lats - area < lat(ncol) < lons + area .and. lons- area < lon(ncol) < lons + area
#------------------------------------------------------------------------
# Please give the lat and lon of sites here.
# sites    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16   17   18   19   20   21   23   24   25   26   27   28   29   30   31  32   33  34   35  36
lats = [  20,  27, -20, -20,  -5,  -1,  60,   2,   9,   56,  45,   0,  10,  20,   0,   5,   9, -60,   0,   0, -45, -75,  30,  25 , 70 , 0,  -15, -15, -35, -25, -15,-15, -1,  45,  9,35]

lons = [ 190, 240, 275, 285, 355, 259,  180, 140, 229, 311, 180, 295,  90, 205, 325, 280, 170, 340, 305,  25,  90,  90,  90, 105 , 90, 160, 260, 345, 220,  75, 180,270,270, 260,281,280]

REG  = ['DYCOMS','HAWAII','VOCAL','VOCAL_near','Namibia','Namibia_near','NP',  'SP',  'EP',  'WP',  'ITCZ', 'LBA',  'CAF', 'PA']
LatS = [    20.0,    10.0,  -25.0,     -35.0,    -20.0,          -30.0, 45.0, -60.0,   0.0, -10.0,     -10.0, -15.0,  -10.0,   -5.0]
LatN = [    35.0,    30.0,  -15.0,     -15.0,    -10.0,          -20.0, 60.0, -45.0,  15.0,  10.0,      10.0,   5.0,   10.0,   10.0]
LonW = [   226.0,   200.0,  275.0,     282.0,     -5.0,            5.0,  1.0,   1.0, 180.0, 110.0,     110.0, 285.0,   10.0,  270.0]
LonE = [   241.0,   220.0,  285.0,     288.0,      5.0,           15.0,360.0, 360.0, 260.0, 165.0,     285.0, 320.0,   40.0,  290.0]

##=======================================================================
# END User Defined Settings
##=======================================================================

#------------------------------------------------------------------------
# No need to change
#------------------------------------------------------------------------

if 'P3' in mpsc and 'MG' in mpsc:
    print("NOTE:::Since both P3 and MG exist simultaneously in the microphysics, they have different variables, we are unable to compare them on a single plot." )
    drawmicrobgt = False
    drawp3 = False
if all(item == 'P3' for item in mpsc):
    drawmicrobgt = False
elif all(item == 'MG' for item in mpsc):
    drawp3 = False

ncases =len(cases)
nsite  =len(lats)

casedir=outdir+casename
print(casedir)

import numpy as np
import pdb
import os
import function_cal_mean
import function_pick_out
import draw_plots_hoz_2D
import draw_plots_hoz_dif
import draw_large_scale
import draw_time_series
import draw_clubb_standard
import draw_atm_standard
import draw_clubb_budget
import draw_micro_budget
import draw_host_budget
import Common_functions
import Diagnostic_webpage

casedir=outdir+casename

if not os.path.exists(outdir):
    os.mkdir(outdir)

if not os.path.exists(casedir):
    os.mkdir(casedir)

if calmean:
    print('Getting climatological mean')
    function_cal_mean.cal_mean(ncases, cases, years,nyear, nsite, lats, lons, area, filepath,climopath,regridpath,affl,suffix,mapfile,ncopath)

if findout:
    print('Find out the sites')
    function_pick_out.pick_out(ncases, cases, years, nsite, lats, lons, area, climopath, runfilepath, casedir,ncopath, calfvsite,datapath)

if draw2d:
    print('Drawing 2d')
    plot2d=draw_plots_hoz_2D.draw_2D_plot(ptype,pixel,cseason, ncases, cases, casenames, nsite, lats, lons, climopath, regridpath, runfilepath, filepathobs,casedir,list_of_parameters,REG,LatS,LatN,LonE, LonW, ncopath, calfvsite,datapath)
#    clevel=500
#    plot3d=draw_plots_hoz_3D.draw_3D_plot(ptype,clevel,cseason, ncases, cases, casenames, nsite, lats, lons, filepath, filepathobs,casedir,datapath)

if drawdif:
    print('Drawing dif')
    plotdif=draw_plots_hoz_dif.draw_dif_plot(ptype,pixel,cseason, ncases, cases, casenames, nsite, lats, lons, regridpath, filepathobs,casedir,list_of_parameters,REG,LatS,LatN,LonE, LonW, ncopath, datapath)

filepathobs="/public/home/zhun/postprocessing/amwg_diag5.6/obs_data/" 

if drawlarge:
    print('Drawing Large-scale variables on selected sites')
    pname = "Largescale"
    top_level = 0
    plotlgs=draw_large_scale.large_scale_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,calfvsite,datapath,pname)

    pname = "Largescale"
    top_level = 750
    plotlgs_lev=draw_large_scale.large_scale_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,calfvsite,datapath,pname)

if drawclubb:
    print('Drawing CLUBB standard variables on selected sites')

    pname       = 'std1'
    varis       = [ 'wp2','up2','vp2','rtp2','thlp2','wp3']
    cscale      = [     1,    1,    1,   1E6,      1,    1]
    chscale     = [   '1',  '1',  '1','1E-6',    '1',  '1']
    top_level   = 0
    plotstd1    =draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    top_level   = 750
    pname       = 'std1_lev'
    plotstd1_lev=draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    pname       = 'std2'
    varis       = [ 'wprtp','wpthlp','wprcp','upwp','vpwp','rtpthlp']
    cscale      = [     1E3,       1,    1E3,     1,     1,     1E3] 
    chscale     = [  '1E-3',     '1', '1E-3',   '1',    '1',    '1E-3']
    top_level   = 0
    plotstd2    =draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    top_level   = 750
    pname       = 'std2_lev'
    plotstd2_lev=draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    pname       = 'std3'
    varis       = [ 'wp2thlp','wp2rtp','wpthlp2','wprtp2','rcp2', 'wp2rcp']
    cscale      = [         1,        1,       1,     1E6,   1E6,      1E3] 
    chscale     = [       '1',      '1',     '1',  '1E-6','1E-6',   '1E-3']
    top_level   = 0
    plotstd3    =draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    top_level   = 750
    pname       = 'std3_lev'
    plotstd3_lev=draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    varis       = [ 'wpthvp','wp2thvp','rtpthvp','thlpthvp','wp4','wprtpthlp']
    cscale      = [        1,        1,      1E3,         1,    1,        1E3] 
    chscale     = [      '1',      '1',   '1E-3',       '1',  '1',    '1-E-3']
    pname       = 'std4'
    top_level   = 0
    plotstd4    =draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    top_level   = 750
    pname       = 'std4_lev'
    plotstd4_lev=draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

#    pname       = 'Tau'
#    varis       = [ 'invrs_tau_bkgnd','invrs_tau_shear','invrs_tau_sfc','invrs_tau_no_N2_zm','invrs_tau_zm','invrs_tau_wp2_zm','invrs_tau_xp2_zm','invrs_tau_wp3_zm','bv_freq_sqd']
#    cscale      = [               1E3,              1E3,            1E3,           1E3,     1E3,         1E3,         1E3,         1E3,            1E3]
#    chscale     = [            '1E-3',           '1E-3',         '1E-3',        '1E-3',  '1E-3',      '1E-3',      '1E-3',      '1E-3',         '1E-3']
#    top_level   =0
#    plottau     =draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

#    top_level = 750
#    pname = 'Tau_lev'
#    plottau_lev=draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

if drawskw:
    print('Drawing CLUBB skewness functions on selected sites')
    pname       = 'CLUBB_skewfunc'
    varis       = [ "C6rt_Skw_fnc","C11_Skw_fnc","C1_Skw_fnc","C7_Skw_fnc","Lscale","gamma_Skw_fnc","Kh_zm","SKW","Skw_velocity"]
    cscale      = [     1,    1,    1,     1,     1,    1,    1,      1,    1]
    chscale     = [   '1',  '1',  '1',   '1',   '1',  '1',   '1',   '1',  '1']
    top_level   = 0
    plotskw     =draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

if drawsilhs:
    print('CLUBB standard variables on selected sites')

    pname       = 'silhs_std'
    varis       = [ "SILHS_CLUBB_PRECIP_FRAC","SILHS_CLUBB_ICE_SS_FRAC","HR","AWNC","AWNI","ADSNOW","ANSNOW","AQSNOW","RHW","QRS","QRL","AQRAIN" ]
    cscale      = [                         1,                        1,   1,     1,     1,       1,       1,       1,    1,    1,    1,       1]
    chscale     = [                       '1',                      '1', '1',   '1',   '1',     '1',     '1',     '1',  '1',  '1',  '1',     '1']
    top_level   = 0
    plotsilhs   =draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

if drawhf:
    print('Holl filler')
    pname       = 'hollfiller'
    varis       = [ "QVHFTEN","QCHFTEN","QRHFTEN","QIHFTEN"]
    cscale      = [         1,        1,        1,        1]
    chscale     = [       '1',      '1',      '1',      '1']
    top_level   = 0
    plothf      = draw_clubb_standard.clubb_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

if drawts:
    print('Drawing time series on selected sites')

    pname       = "ts1"
    varis       = [ "TS", "CLDLOW", "SHFLX", "LHFLX", "FSNS", "FLNS"]
    plotts1     = draw_time_series.ts_plots(ptype,pixel,pname,cseason, varis, ncases, cases, casenames, nsite, lats, lons, years, nyear, filepath, filepathobs,casedir,affl,suffix,calfvsite,datapath)

    pname       = "ts2"
    varis       = [ "SWCF", "LWCF", "PRECC", "PRECL", "TAUX", "TAUY"]
    plotts2     = draw_time_series.ts_plots(ptype,pixel,pname,cseason, varis, ncases, cases, casenames, nsite, lats, lons, years, nyear, filepath, filepathobs,casedir,affl,suffix,calfvsite,datapath)

    pname       = "ts3"
    varis       = [ "FSNT", "FLNT", "TMQ", "TGCLDLWP", "TGCLDIWP", "U10" ]
    plotts3     = draw_time_series.ts_plots(ptype,pixel,pname,cseason, varis, ncases, cases, casenames, nsite, lats, lons, years, nyear, filepath, filepathobs,casedir,affl,suffix,calfvsite,datapath)

if drawhyd:
    print('Drawing Rain and Snow properties')

    pname       = 'Rain'
    varis       = [ 'AQRAIN','ANRAIN','ADRAIN','FREQR']
    cscale      = [      1E6,     1,       1E4,      1]
    chscale     = [   '1E-6',  '1',    '1E-4',     '1']
    plotrain    = draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    pname       = 'Snow'
    varis       = [ 'AQSNOW','ANSNOW','ADSNOW','FREQS']
    cscale      = [      1E6,     1,       1E4,      1]
    chscale     = [   '1E-6',  '1',    '1E-4',     '1']
    plotsnow    = draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    pname       = 'NUM'
    varis       = [ 'AWNC','AWNI','AREL','AREI']
    cscale      = [     1E-7,    1E-3,        1,         1]
    chscale     = [    '1E7',   '1E3',      '1',       '1']
    plotsnum    = draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    pname       = 'RAINQM'
    varis       = [ 'RAINQM','NUMRAI']
    cscale      = [     1E-12,    1E-3]
    chscale     = [    '1E12',   '1E3']
    plotsqm     = draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    varis       = [ 'RCM_CLUBB','CLOUDFRAC_CLUBB']
    cscale      = [      1E3,      1E3]
    chscale     = [      '1E-3',   '1E-3']
    pname       = 'std5'
    plotstd5    = draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

if drawp3:
    print('Drawing P3')
    pname = 'P3_tend1'
    varis   = [ 'P3_mtend_CLDICE','P3_mtend_CLDLIQ','P3_mtend_CLDRAIN','P3_mtend_Q']
    cscale  = [     1E9,    1E9,      1E9,    1E9]
    chscale = [    '1E-9',   '1E-9',  '1E-9',   '1E-9']
    plotsp3t1= draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname)

    pname = 'P3_tend2'
    varis   = [ 'P3_mtend_NUMICE','P3_mtend_NUMICE','P3_mtend_NUMICE','P3_mtend_TH']
    cscale  = [     1E9,    1E9,      1E9,    1E9]
    chscale = [    '1E-9',   '1E-9',  '1E-9',   '1E-9']
    plotsp3t2= draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname)

    pname = 'P3_tend3'
    varis   = [ 'P3_sed_CLDICE','P3_sed_CLDLIQ','P3_sed_CLDRAIN']
    cscale  = [     1E9,    1E9,      1E9]
    chscale = [    '1E-9',   '1E-9',  '1E-9']
    plotsp3t3= draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname)

    pname = 'P3_tend4'
    varis   = [ 'P3_sed_NUMICE','P3_sed_NUMICE','P3_sed_NUMICE']
    cscale  = [     1E9,    1E9,      1E9]
    chscale = [    '1E-9',   '1E-9',  '1E-9']
    plotsp3t4= draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname)

if drawaero:
    print('Drawing  aerosol related vars')

    pname       = 'FREZ'
    varis       = [ 'DSTFREZIMM','BCFREZIMM','DSTFREZCNT','BCFREZCNT','DSTFREZDEP','BCFREZDEP']
    cscale      = [            1,          1,        1E12,       1E3 ,         1E8,        1E3]
    chscale     = [          '1',        '1',     '1E-12',     '1E-3',      '1E-8',     '1E-3']
    plotsaero1  = draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    pname       = 'FREQAERO'
    varis       = ['FREQIMM','FREQCNT','FREQDEP','FREQMIX']
    cscale      = [      1,     1,       1E3,      1]
    chscale     = [    '1',   '1',    '1E-3',     '1']
    plotsaero2  = draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    pname       = 'ACN'
    varis       = [ 'bc_a1_num','bc_c1_num','dst_a1_num','dst_a3_num','dst_c1_num','dst_c3_num']
    cscale      = [            1,         1,           1,         1E3,          1,        1E3]
    chscale     = [          '1',       '1',         '1',      '1E-3',         '1',     '1E-3']
    plotsaero3  = draw_atm_standard.atm_std_prf(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

if drawhostbgt:
    print('Drawing e3sm standard budgets')
    # Since we are dealing with the CLUBB diagnostic package, the tendencies from CLUBB represent the most fundamental variables. Other physical processes vary based on dpsc and mpsc.
    top_level = 0
    pname     = 'E3SM'
    varis     = [ "Q_PHY","CLOUDLIQ","CLOUDICE","Q_PHY","T_DYC","T_PHY"]
    cscale    = [1E8, 1E8, 1E8, 1E8, 1E4, 1E4]
    chscale   = ['1E-8', '1E-8', '1E-8', '1E-8', '1E-4', '1E-4']
    plothostbgt=draw_host_budget.draw_host_bgt(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,dpsc,mpsc,calfvsite,datapath)

if drawmicrobgt:
    # ONLY works for MG
    print('Drawing MG budget')
    top_level = 0
    pname = 'mirco1'
    vname   = [ 'Liquid','Ice','Rain','Snow']
    varis   = [ 'MPDLIQ','MPDICE','QRSEDTEN','QSSEDTEN'] # We just need a unit
    cscale  = [      1E9,     1E9,       1E9,       1E9]
    chscale = [   '1E-9',  '1E-9',    '1E-9',    '1E-9']
    plotmicrobgt1=draw_micro_budget.draw_micro_bgt(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,vname,cscale,chscale,pname,calfvsite,datapath)

    pname = 'micro2'
    vname   = [ 'Vapor','NUMCLDLIQ','NUMCLDICE']
    varis   = [ 'QISEVAP','nnuccco',  'nnuccdo']  # We just need a unit
    cscale  = [      1E9,     1E-3,      1E-1]
    chscale = [   '1E-9',    '1E3',     '1E1']
    plotmicrobgt2=draw_micro_budget.draw_micro_bgt(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,vname,cscale,chscale,pname,calfvsite,datapath)

if drawbgt:
    print('Drawing CLUBB BUDGET')
    top_level = 0
    varis   = [ 'wp2', 'wp3', 'up2', 'vp2']
    cscale  = [     1,     1,     1,     1]
    chscale = [   '1',   '1',   '1',   '1']
    pname = 'Budget1'
    plotbgt1=draw_clubb_budget.draw_clubb_bgt(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    varis    = [ 'wprtp','wpthlp',  'rtp2', 'thlp2']
    cscale   = [     1E7,     1E4,    1E11,     1E4]
    chscale  = [  '1E-7',  '1E-4', '1E-11',  '1E-4']
    pname = 'Budget2'
    plotbgt2=draw_clubb_budget.draw_clubb_bgt(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)   

    varis   = [  'um',   'rtpthlp',  'thlm',   'rtm']
    cscale  = [   1E4,    1E4,     1E5,     1E8]
    chscale = ['1E-4', '1E-4',  '1E-5',  '1E-8']
    pname = 'Budget3'
    plotbgt3=draw_clubb_budget.draw_clubb_bgt(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath) 

    varis   = ['upwp','vpwp']
    cscale  = [1,1]
    chscale = ['1', '1']
    pname = 'Budget4'
    plotbgt4=draw_clubb_budget.draw_clubb_bgt(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    varis   = [ 'wp2','wp3','up2','vp2','upwp','vpwp']
    cscale  = [     1,    1,    1,    1,1,1]
    chscale = [   '1',  '1',  '1',  '1', '1', '1']
    pname = 'Budget1_lev'
    top_level = 750
    plotbgt1_lev=draw_clubb_budget.draw_clubb_bgt(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    varis    = [ 'wprtp','wpthlp',  'rtp2', 'thlp2']
    cscale   = [     1E7,     1E4,    1E11,     1E4]
    chscale  = [  '1E-7',  '1E-4', '1E-11',  '1E-4']
    pname = 'Budget2_lev'
    plotbgt2_lev=draw_clubb_budget.draw_clubb_bgt(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    varis   = [  'um',   'rtpthlp',  'thlm',   'rtm']
    cscale  = [   1E4,    1E4,     1E5,     1E8]
    chscale = ['1E-4', '1E-4',  '1E-5',  '1E-8']
    pname = 'Budget3_lev'
    plotbgt3_lev=draw_clubb_budget.draw_clubb_bgt(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

    varis   = ['upwp','vpwp']
    cscale  = [1,1]
    chscale = ['1', '1']
    pname = 'Budget4_lev'
    plotbgt4_lev=draw_clubb_budget.draw_clubb_bgt(ptype,pixel,cseason,top_level, ncases, cases, casenames, nsite, lats, lons, climopath, filepathobs,casedir,varis,cscale,chscale,pname,calfvsite,datapath)

if makeweb:
    print('Making webpages')
    Diagnostic_webpage.main_web(casename,casedir)

    Diagnostic_webpage.sets_web(casename,casedir,'diff.*.asc','txt',\
                                'Gitdiff','1000','1000')

    if (draw2d):
        Diagnostic_webpage.sets_web(casename,casedir,plot2d,'2D',\
				'Horizontal Plots','1000','1000')

    if (drawdif):
        plot2d.extend(plotdif[:])

        Diagnostic_webpage.sets_web(casename,casedir,plot2d,'2D',\
                'Horizontal Plots','1000','1000')

    for ire in range (0, nsite):
        plotclb=[]
        if (drawlarge):
           plotclb.append(plotlgs[ire])
           plotclb.append(plotlgs_lev[ire])
        if (drawclubb):  
           plotclb.append(plotstd1[ire])
           plotclb.append(plotstd2[ire])
           plotclb.append(plotstd3[ire])
           plotclb.append(plotstd4[ire])
#           plotclb.append(plottau[ire])
           plotclb.append(plotstd1_lev[ire])
           plotclb.append(plotstd2_lev[ire])
           plotclb.append(plotstd3_lev[ire])
           plotclb.append(plotstd4_lev[ire])

        if (drawts):
           plotclb.append(plotts1[ire])
           plotclb.append(plotts2[ire])
           plotclb.append(plotts3[ire])

        if (drawskw):
           plotclb.append(plotskw[ire])
        if (drawhf):
           plotclb.append(plothf[ire])
        if (drawhyd):
           plotclb.append(plotrain[ire])
           plotclb.append(plotsnow[ire])
           plotclb.append(plotsnum[ire])
           plotclb.append(plotsqm[ire])

        if (drawaero):
           plotclb.append(plotsaero1[ire])
           plotclb.append(plotsaero2[ire])
           plotclb.append(plotsaero3[ire])


        if (drawmicrobgt):
           for im in range (0, ncases ):
               plotclb.append(plotmicrobgt1[ire*ncases+im])
#               plotclb.append(plotmicrobgt2[ire*ncases+im])

        if (drawhostbgt):
           for im in range (0, ncases ):
               plotclb.append(plothostbgt[ire*ncases+im])

        if (drawbgt):
           for im in range (0, ncases ):
               plotclb.append(plotbgt1[ire*ncases+im])
           for im in range (0, ncases ):
               plotclb.append(plotbgt2[ire*ncases+im])
           for im in range (0, ncases ):
               plotclb.append(plotbgt3[ire*ncases+im])
           for im in range (0, ncases ):
               plotclb.append(plotbgt4[ire*ncases+im])
           for im in range (0, ncases ):
               plotclb.append(plotbgt1_lev[ire*ncases+im])
           for im in range (0, ncases ):
               plotclb.append(plotbgt2_lev[ire*ncases+im])
           for im in range (0, ncases ):
               plotclb.append(plotbgt3_lev[ire*ncases+im])
           for im in range (0, ncases ):
               plotclb.append(plotbgt4_lev[ire*ncases+im])

        Diagnostic_webpage.sets_web(casename,casedir,plotclb,str(lons[ire])+'E_'+str(lats[ire])+'N',\
                                  'Profiles on '+str(lons[ire])+'E_'+str(lats[ire])+'N','908','636')

if maketar:
    print('Making tar file of case')
    Common_functions.make_tarfile(outdir+casename+'.tar',outdir+casename)
    
