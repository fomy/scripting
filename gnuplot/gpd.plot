#!/usr/bin/gnuplot

set term postscript color

set xrange[1:1000000]
set yrange[0:1]
set logscale x
set output "gpd_cdf.eps"
plot 0.44155+(1-(1+0.348238*(x-15)/214.476)**(-1/0.348238))*0.55845 title "gpd" with line linewidth 4,\
         'system_out_value.txt' using 1:(0.000001) smooth cumulative with line linewidth 4 title "facebook";

set xrange[1:1000000]
set yrange[0.000000001:1]
set logscale x
set logscale y
set output "gpd_density.eps"

plot 0.55845*1/214.476*(0.348238*((x-15)/214.476)+1)**(-(0.348238+1)/0.348238) title "gpd_density" with line linewidth 4,\
         'frequency.txt' using 2:(0.000001) smooth frequency  w line linewidth 4 t "density from generator";
