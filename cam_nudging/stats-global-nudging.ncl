begin

configlist=(/"N1","N19","N20","N21","N21-UV","N22","N23","N24","N25","N27","N29","N31","N33"/)
;configlist=(/"N1","N19"/)
thisvar="U850"

do ii = 0,dimsizes(configlist)-1
print("... doing ii "+ii+" ("+configlist(ii)+")")

diri = "/glade/u/home/zarzycki/scratch/archive/WINDTURN-ne0natlantic30x4-FHIST-"+configlist(ii)+"/atm/hist/"
fili = systemfunc("cd "+diri+" ; ls WINDTURN-ne0natlantic30x4-*.cam.h3.2005-1*.nc | grep -v 2005-01-")
nfili= dimsizes(fili)
print("nfili="+nfili)
if (ii .eq. 0)
  print(fili)
end if

f    = addfiles(diri+fili,"r") 

lat  = f[0]->lat
lon  = f[0]->lon

print("...... loading model data")
wgt_file1="/glade/u/home/zarzycki/work/maps/hyperion/map_ne0np4natlanticref.ne30x4_to_1.0x1.0_GLOB.nc"
U = f[:]->$thisvar$(::8,:)

print("...... interp model data")
Opt         = True
UMOD  = ESMF_regrid_with_weights(U,wgt_file1,Opt)

if (ii .eq. 0) then
  print("... interp reanalysis data")
  print("...... loading reanalysis data")
  dir2 = "/glade/u/home/zarzycki/scratch/h1files/ERAI/2005/"
  fil2 = systemfunc("cd "+dir2+" ; ls ERAI.h1.20051*.nc | grep -v 200501")
  ;print(fil2)
  f2    = addfiles(dir2+fil2,"r") 

  lat2  = f2[0]->lat
  lon2  = f2[0]->lon
  
  UERA  = f2[:]->$thisvar$(::4,:,:)
  
  UERA = lonFlip(UERA)
  
  print("...... interp data")
  UTGT = linint2_Wrap(UERA&lon,UERA&lat,UERA, True, UMOD&lon,UMOD&lat, 0)
  print(" --- done interp")
end if

;printVarSummary(UMOD)
;printVarSummary(UTGT)
;print(num(ismissing(UMOD)))
;print(num(ismissing(UTGT)))

print("... calc stats")
wgt = new((/dimsizes(UMOD&lat),dimsizes(UMOD&lon)/),"float")

do jj = 0,dimsizes(UMOD&lon)-1
  wgt(:,jj) = tofloat(cos(0.01745329*UMOD&lat))
end do

rmsd= wgt_arearmse2( UMOD,UTGT,wgt,0 )
corr= pattern_cor( UMOD,UTGT,wgt,0 )
print("--- done calc stats")

if (ii .eq. 0) then  
  masterrms = new((/dimsizes(configlist),dimsizes(rmsd)/),typeof(rmsd))
  masterrms!1 = "time"
  masterrms&time=UMOD&time
  mastercorr=masterrms
end if

masterrms(ii,:) = (/rmsd/)
mastercorr(ii,:) = (/corr/)

end do

rms_avg = dim_avg_n_Wrap(masterrms,1)
corr_avg = dim_avg_n_Wrap(mastercorr,1)

sorted = dim_pqsort(corr_avg,-1)
print(configlist(sorted)+" "+corr_avg(sorted)+" "+rms_avg(sorted))

wks   = gsn_open_wks ("x11","xy")                 ; send graphics to PNG file

res                   = True                      ; plot mods desired
res@tiMainString      = ""

res@xyLineColors      = (/"blue","red","green","purple","orange","yellow","black","magenta","pink","navyblue"/)          ; change line color

  res@pmLegendDisplayMode    = "Always"
  
  res@pmLegendSide           = "Top"               ; Change location of 
  res@pmLegendParallelPosF   = 0.5                 ; move units right
  res@pmLegendOrthogonalPosF = -0.8                ; move units down

  res@pmLegendWidthF         = 0.20                ; Change width and
  res@pmLegendHeightF        = 0.25                ; height of legend.
  res@lgLabelFontHeightF     = .015                 ; change font height
  res@lgOrientation          = "vertical"
  res@lgPerimOn              = False               ; no box around

  res@xyMarkLineModes        = (/"Lines"/)         ; line style
  res@xyLineThicknesses      = (/2.,2.,2.,2./)     ; line thickness
  res@xyLineColors           = res@xyLineColors
  ;res@lgLabelAngleF          = 280.                ; angle of legend label
  res@xyExplicitLegendLabels = configlist


plot  = gsn_csm_xy (wks,masterrms&time,masterrms,res) ; create plot

end