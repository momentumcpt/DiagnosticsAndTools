# DiagnosticsAndTools
Quick start.

diagnostic_v3_0 is a python diagnostic package primarily focused on vertical profiles of CAM and EAM.

Its main program is CLUBB_PROF.py, where users can set parameters such as the diagnostic result name "case='whatever'", the diag output/plots directory "outdir=path0", the names of simulation results "cases=[name1,name2]", their original data directory "filepath=[path1,path2]", "years=[2005,1979]" for the start time and "nyear=[10,1]" for the duration of the run. "affl=[cam,eam]" is used to confirm the naming of the schema history file, which can be EAM, CAM, etc. "suffix=[h0a,h0,h1]" specifies the parameters for storing history files, such as h0, h1, h0a, etc. The climate files for output are stored in "climopath=" for vertical profile plots, while regridded climate files are stored in "regridpath=".  For each model runs, we can set calfvsite = [True (FV), False (SE)] , dpsc=[zm (ZM),nan (Silhs)] and mpsc= [MG, P3].

pixel = 100 changes the res of plots.
ptype = png or PDF or eps etc. NOTE wepage only supports 'png' format.
csenson = "ANN" for annual mean

The subroutines and their main functions include:

1 Calculating Climate Averages: By setting 'calmean=TRUE', it calls function_cal_mean.py to compute climate averages.

2 Selecting Sites of Interest: This is achieved by setting "lats=" and "lons=" in the main program and enabling 'findout=True', which then calls function_pick_out.py. It supports DYNCOREs such as SE and FV. 'calfvsite = [True, False]' needs to be declared in main code, it is 'Ture' means when FV is used. The parameter 'area=1.5' means that a search is conducted within a 1.5-degree square grid surrounding the site to find suitable model grids. If there are more than one such grids, the average value of these grids will be used.

3 Drawing 2D Plots of Simulation Results and Observations, and their Differences and RMSE: Enabling 'draw2d=True' calls draw_plots_hoz_2D.py for 2D plots, while 'drawdif=True' calls draw_plots_hoz_dif.py for difference plots and their RMSE. Note that when using draw_plots_hoz_dif.py to calculate difference RMSE, 'mapfile=' and "regridpath=" must be specified in the main program to make sure OBS and model results have same resolutions.

4 Drawing Vertical Profiles of Large-Scale Variables (Including Observations): Enabling 'drawlarge=True' calls draw_large_scale.py to create vertical profiles of large-scale variables. can set 'top_level= 750' etc in main code.

5 Drawing Standard Variable Profiles for CLUBB and SILHS and Skewness function of CLUBB (NO Observations): Enabling 'drawclubb=True', 'drawsilhs=True', and 'drawskw=True' calls draw_clubb_standard.py to produce these plots.

6 Drawing Time Series: Enabling 'drawts=True' and variables lists call draw_time_series.py to create time series plots.

7 Drawing Profiles of Hydrometeors and Aerosols: Enabling 'drawhyd=True' and 'drawaero=True' calls draw_atm_standard.py (which has a similar structure to draw_clubb_standard.py but with different vertical coordinates) to produce profiles of these variables.

8 Drawing Vertical Budget Plots: Support for budget plots of the host models (CAM, EAM), CLUBB, and microphysical processes. 
8.1 Host model. Enabling 'drawhostbgt=True' calls draw_host_budget.py to draw budgets for temperature, humidity, clouds, etc., in the host model. Note that 'dpsc=[zm,nan]' should be set according to the specific experiment to draw tendency from deep convections, such as ZM or SILHS (set it to nan). 
8.2 Enabling 'drawbgt=True' draws budgets for all CLUBB prognostic equations
8.3 while 'drawmicrobgt=True' draws budgets for different microphysical processes based on 'mpsc=[MG,P3]' specified in the main program.

9 Making website 'makeweb=True' and Tar them 'maketar=True'.

In fuction 5-7, Users can decide for themselves which variables they want to plot by simply modifying the lists varis, cscale, and chscale as follows:
varis = ['AQRAIN', 'ANRAIN', 'ADRAIN', 'FREQR']  # list of interested variables. 
cscale = [1E6, 1, 1E4, 1]  # factors
chscale = ['1E-6', '1', '1E-4', '1'] # factors on plots (string)
e.g. by changing the contents of these lists, users can specify the variables they wish to plot and adjust the corresponding scaling factors and scale labels accordingly.

How to install:
conda create -p yourname -c conda-forge  matplotlib xarray netcdf4 scipy pynio numpy pyngl qt cartopy cmaps

Run:
yourname/python CLUBB_PROF.py

Zhun Guo 2025.2
