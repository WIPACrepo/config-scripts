#!/usr/bin/env python
#
# Post-run plotting script for updateCalibration.py.  Reads in
# calibration differences output file generated by the script.
#
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.optimize import curve_fit

# Difference output log for plotting
OUTPUT_FILE = "calupdate.txt"

def gauss(x, *p):
    """ Non-normalized Gaussian for curve-fitting"""
    A, mu, sigma = p
    return A * np.exp(-(x-mu)**2/(2.*sigma**2))

def main():

    # Load the saved plotting results
    f = open(OUTPUT_FILE, 'rb')
    plotResults = json.load(f)
    f.close()

    hvDiffList = plotResults["hvDiffList"]
    hvDiffListIT = plotResults["hvDiffListIT"]
    gainDiffList = plotResults["gainDiffList"]
    gainDiffListIT = plotResults["gainDiffListIT"]    
    speDiscList = plotResults["speDiscList"]
    speDiscListIT = plotResults["speDiscListIT"]    
    atwdFreqList = plotResults["atwdFreqList"]

    logPlot = True        
    pp = PdfPages('calupdate.pdf')
    
    binrange = range(-25, 25, 2)

    plt.subplot(131)
    gainHist, edges, patches = plt.hist(gainDiffList, bins=binrange, color='b',
                                        label='in-ice', log=logPlot)
    binCenters = 0.5*(edges[:-1] + edges[1:])
    
    # Fit the distribution with a Gaussian
    p0 = [1000., 0., 1.]
    coeff, var_matrix = curve_fit(gauss, binCenters, gainHist, p0=p0)
    histFit = gauss(binCenters, *coeff)

    plotIceTop = True
    
    if (plotIceTop):
        gainHistIT, edges, patches = plt.hist(gainDiffListIT, bins=binrange, color='r',
                                              label='IceTop', alpha=0.5, log=logPlot)
        coeffIT, var_matrix = curve_fit(gauss, binCenters, gainHistIT, p0=p0)
        histFitIT = gauss(binCenters, *coeffIT)
        plt.plot(binCenters, histFitIT, "r--", linewidth=2)
        
    plt.plot(binCenters, histFit, "k--", linewidth=3)
    if (plotIceTop):
        plt.title(r'$\mathrm{in-ice:}\ \mu=%.2f,\ \sigma=%.2f\ \mathrm{IceTop:}\ \mu=%.2f,\ \sigma=%.2f$'
                  %(coeff[1], coeff[2], coeffIT[1], coeffIT[2]))
    else:
        plt.title(r'$\mu=%.2f,\ \sigma=%.2f$' %(coeff[1], coeff[2]))
    plt.xlabel("Fractional change in gain (old-new, %)")
    plt.ylabel("DOMs/bin")
    plt.ylim(0.1, 1e4)
    if (plotIceTop):
        plt.legend()

    plt.subplot(132)
    binrange = range(-15, 15, 1)
    plt.hist(speDiscList, bins=binrange, color='b', label='in-ice', log=logPlot)
    # plt.hist(speDiscListIT, bins=binrange, color='r', label='IceTop', alpha=0.5)                
    plt.xlabel("Change in SPE discriminator (new-old, counts)")
    plt.ylabel("DOMs/bin")
    #plt.legend()
    
    plt.subplot(133)
    binrange = range(-10, 10, 1)
    plt.hist(atwdFreqList, bins=binrange, color='b', log=logPlot)
    plt.xlabel("Change in ATWD trigger bias (new-old, counts)")
    plt.ylabel("Chips/bin")        
    # plt.legend()
    
    pp.savefig()
    pp.close()
    
    plt.show()
    
if __name__ == "__main__":
    main()
