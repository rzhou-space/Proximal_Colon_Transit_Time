#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'widget')


def τ_median(Vin, Vout, L, R):
    """
    Define the τ_median function in dependent of Vin (Inflow volume) and
    Vout (Outflow volume).
    
    Vin: the inflow volume.
    Vout: the outflow volume.
    L: the length of the simulated colon.
    R: the diameter of the simulated colon.
    """
    τ = 8./27.*1440.*L*np.pi*R**2/(Vin-Vout)*np.log(Vin/Vout)
    
    return τ


def taylor_expension(ord_n, Vin, Vout):
    """
    This function returns the part in τ_median that approximated through
    taylor expension. 
    
    ord_n: the order of the taylor expension.
    Vin: the inflow volume.
    Vout: the outflow volume.
    """
    # The ratio of outflow volume.
    x = Vout/Vin
    
    taylor = 0
    # The approximation formular begins with i = 0.
    for i in range(ord_n):
        taylor += (-1)**i*(x-1)**i/(i+1)
    
    return taylor


def τ_taylor_expension(ord_n, Vout, Vin, L, R):
    """
    This function returns the transit time values approximated by the taylor
    expension depending on the outflow volume Vout and inflow volume Vin.
    
    Vin: the inflow volume.
    Vout: the outflow volume. 
    ord_n: the order of the taylor expension for approximation. 
    """
    # The ratio of outflow volume.
    x = Vout/Vin
    
    τ = 8./27.*1440*L*np.pi*R**2*(1/Vin)*taylor_expension(ord_n, Vin, Vout)
    
    return τ


def τ_median_plot(Vin, Vout_list, L, R):
    """
    This function generates a plot of the τ_median values based on 
    given lists for inflow volume and outflow volumne, which allows the 
    observation of median transit time change depending on inflow volume
    and outflow volume. 
    
    Vin: considered inflow volume value.
    Vout_list: a list containing considered outflow volume values. 
    L: the length of the simulated colon.
    R: the diameter of the simulated colon.
    L and R are required for the use of the function τ_median.

    """
    τ_medians = []
    
    for Vout in Vout_list:
        # calculate the transit time and turn the result into minutes.
        current_τ = τ_median(Vin, Vout, L, R)
        τ_medians.append(current_τ)
    
    # Plot the DataFrame directly.
    plt.plot(Vout_list, τ_medians)
    plt.title("Theoretical median transit time")
    plt.ylabel("τ median (min)")
    plt.xlabel("Vout (ml/day)")
    plt.show()
    
    #return median_DF


def τ_median_plot_2(Vin, Vout_list, L, R, ord_n):
    """
    This function generates a plot of the τ_median values based on 
    given list for outflow volumne with a fixed inflow volume, which 
    allows the observation of median transit time change depending on 
    inflow volume and outflow volume. 
    
    The results from taylor expension are also ploted in the same figure
    for evaluation of the approximation.
    
    Vin: given value for inflow volume.
    Vout_list: a list containing considered outflow volume values. 
    L: the length of the simulated colon.
    R: the diameter of the simulated colon.
    L and R are required for the use of the function τ_median.
    ord_n: the order of taylor expension for approximation values.

    """
    all_τ_medians = []
    all_taylor_medians = []
    
    for Vout in Vout_list:
        # calculate the transit time and turn the result into minutes.
        current_τ = τ_median(Vin, Vout, L, R)
        all_τ_medians.append(current_τ)
        
        taylor_τ = τ_taylor_expension(ord_n, Vout, Vin, L, R)
        all_taylor_medians.append(taylor_τ)
    
    # Plot the DataFrame directly.
    plt.plot(Vout_list, all_τ_medians, label = "calculation value")
    plt.plot(Vout_list, all_taylor_medians, label = "approx value")
    plt.title("Theoretical median transit time")
    plt.ylabel("τ median (min)")
    plt.xlabel("Vout (ml/day)")
    plt.legend()
    plt.show()



τ_median_plot(1500, [100, 150, 200, 300, 400, 600, 800, 1000, 1200, 1400]
             ,30, 2.5)

τ_median_plot_2(1500, [100, 150, 200, 300, 400, 600, 800, 1000, 1200, 1400]
                , 30, 2.5, 10)





