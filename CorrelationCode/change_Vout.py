#!/usr/bin/env python
# coding: utf-8


import glob, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'widget')


def read_txt(direction, diff_constant):
    """
    This function reads multiple .txt files (multiple replicates) 
    containing the transit time with the same diffusion constant. 
    Extract then the transit time (turtle_die_tick) from each .txt file 
    as a numpy array. A dictionary with the diffusion constant as key and 
    list of all transit time arrays as item will be returned.
    
    direction: String. The path to the folder with all .txt files with the 
    same diffusion constant.
    diff_constant: String. The diffsion constant applied to generate the 
    .txt files (represent multiple replicates). 
    """
    # Find all the .txt files under given direction.
    os.chdir(direction)
    data = []
    for file in glob.glob("*.txt"):
        data.append(file)
    
    # Extract transit time as numpy array and summary together in a list.
    all_transit_time = []
    heading_rows = [0]
    for docu in data:
        DF_onetrial = pd.read_csv(docu, sep = ","
                                  , skiprows = lambda x: x in heading_rows)
        transit_time = np.array(DF_onetrial.loc[:, "  turtle_die_tick " ])
        all_transit_time.append(transit_time)
    
    return {diff_constant: all_transit_time}




def mean_transit_time(all_transit_dict):
    """
    A dictionary containing all considered diffusion constants and 
    their corresponding modeling replicates results should be given. For
    each diffusion constant, mean transit time of each "replicate" is
    calculated. A dictionary with diffusion constants as key and a list
    of mean transit time as item is returned.
    
    all_transit_dict: dictionary containing multiple modeling results with
    different diffusion constants and repeats.
    
    """
    mean_transit_time = {}
    for key in all_transit_dict.keys():
        mean = []
        for tt_list in all_transit_dict[key]:
            mean.append(np.mean(tt_list))
        mean_transit_time[key] = mean
    return mean_transit_time




def transit_time_summary(Vout_list, D_list):
    """
    This function summarises all mean transit time data generated by the 
    function mean_transit_time for all Vout values and all D vlaues. 
    The results are hierachisch structured as embedded dictionaries with 
    Vout as keys and mean value vectors for all diffusion constans as 
    values. 
    Final dictionary will be returned.
    
    Vout_list: a list of considered Vout values
    D_list: a list of considered diffusion constants.
    """
    all_Vout_transit = {}
    
    for Vout in Vout_list:
        all_diff_transit = {}
        
        for D in D_list:
            direction = "F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout="                        + str(Vout) + "\Diff=" + str(D)
            #diff_constant = "D=" + str(D)
            diff_constant = D
            diff_data = read_txt(direction, diff_constant)
            all_diff_transit.update(diff_data)

        key = "Vout=" + str(Vout)
        mean_tt = {key: mean_transit_time(all_diff_transit)}
    
        all_Vout_transit.update(mean_tt)
    
    return all_Vout_transit




def mean_transit_time_boxplot(mean_tt_dict):
    """
    This function plots the results generated by the function transit_time_
    summary. 
    For each Vout, the data for all diffusion constants are presented 
    in boxplots with their median bounded by a line.
    
    mean_tt_dict: the dictionary generated by function transit_time_summary.
    """
    # Turn the dictionary into DataFrame.
    mean_tt_DF = pd.DataFrame.from_dict(mean_tt_dict)
    diff_constants = mean_tt_DF.index
    all_Vout = mean_tt_DF.columns
    
    # Generating Boxplot.
    mean_box_plot = plt.figure()

    for Vout in all_Vout:
        current_mean_DF = pd.DataFrame.from_dict(mean_tt_dict[Vout])
        bp = plt.boxplot(current_mean_DF, showmeans = True)
        
        # Add line combining the meadian values.
        X=[]
        Y=[]
        for m in bp['medians']:
            [[x0, x1],[y0,y1]] = m.get_data()
            X.append(np.mean((x0,x1)))
            Y.append(np.mean((y0,y1)))
        plt.plot(X,Y, label = Vout)

    plt.xticks(list(range(1, len(diff_constants)+1))
               , diff_constants)
    plt.xlabel("Diffusion Constants ($cm^2/min$)")
    plt.ylabel("Transit Time ($min$)")
    plt.yscale("log", base = 10)
    plt.title("Correlation between Transit Time and Diffusion Constant")
    plt.legend()
    plt.show()




def mean_transit_time_lineplot(mean_tt_dict):
    """
    This function plots the results generated by the function transit_time_
    summary. 
    For each Vout, the mean values of data for all diffusion constants 
    are presented in plots.

    mean_tt_dict: the dictionary generated by function transit_time_summary.
    
    """
    # Turn the dictionary into DataFrame.
    mean_tt_DF = pd.DataFrame.from_dict(mean_tt_dict)
    diff_constants = mean_tt_DF.index
    all_Vout = mean_tt_DF.columns
    
    # Generating plot.
    plt.figure()
    
    for Vout in all_Vout:
        current_DF = pd.DataFrame.from_dict(mean_tt_dict[Vout])
        current_mean_DF = current_DF.mean()
        plt.plot(current_mean_DF, "--o", label = Vout)
    
    plt.xlabel("Diffusion Constants ($cm^2/min$)")
    plt.ylabel("Mean Transit Time ($min$)")
    plt.yscale("log", base = 10)
    plt.title("Correlation between Transit Time and Diffusion Constant")
    plt.legend()
    plt.show()
    



all_mean_tt = transit_time_summary([100, 150, 200, 300, 400]
                            , [0.01, 0.015, 0.02, 0.025, 0.03
                               , 0.035, 0.04, 0.045, 0.05, 0.055
                               , 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 0.09, 0.095
                               , 0.1, 0.2, 0.3, 0.4, 0.5, 0.6])

mean_tt_DF = pd.DataFrame.from_dict(all_mean_tt)
all_Vout = mean_tt_DF.columns
current_DF = pd.DataFrame.from_dict(all_mean_tt['Vout=100'])
current_mean_DF = current_DF.mean()

mean_transit_time_lineplot(all_mean_tt)

mean_transit_time_boxplot(all_mean_tt)



def mean_transit_time_boxplot_sep(mean_tt_dict):
    """
    This function generates a figure with multiple boxplots and one 
    plot for each Vout setting. All plots share the same x axis 
    (the diffusion constant) and have log_10 scaled y axis. 
    In each boxplot the medians are binded with a line. 
    
    mean_tt_dict: the dictionary generated by function transit_time_summary.
    
    """
    # Turn the dictionary into DataFrame.
    mean_tt_DF = pd.DataFrame.from_dict(mean_tt_dict)
    diff_constants = mean_tt_DF.index
    all_Vout = mean_tt_DF.columns
    
    # Generating Boxplot.
    fig, axs = plt.subplots(len(all_Vout))
    fig.suptitle("Correlation between Transit Time and Diffusion Constant")
    
    for i in range(len(all_Vout)):
        Vout = all_Vout[i]
        current_mean_DF = pd.DataFrame.from_dict(mean_tt_dict[Vout])
        bp = axs[i].boxplot(current_mean_DF, showmeans = True)
        
        # Add line combining the meadian values.
        X=[]
        Y=[]
        for m in bp['medians']:
            [[x0, x1],[y0,y1]] = m.get_data()
            X.append(np.mean((x0,x1)))
            Y.append(np.mean((y0,y1)))
        axs[i].plot(X,Y, label = Vout)
        axs[i].set_xticklabels(diff_constants)
        axs[i].set_yscale("log", base = 10)
        axs[i].set_title(str(Vout))
    
    #for j in range(len(all_Vout)-1):
        #plt.setp(axs[j].get_xticklabels(), visible = False)
    
    
    fig.text(0.5, 0.04, "Diffusion Constants ($cm^2/min$)", ha = "center")
    fig.text(0.04, 0.5, "Transit Time ($min$)", va = "center"
            , rotation = "vertical")
    
    
    plt.show()




mean_transit_time_boxplot_sep(all_mean_tt)




def mean_tt_boxplot_sep_min(mean_tt_dict):
    """
    This function undertake the same process as 
    "mean_transit_time_boxplot_sep()". Only with the additional 
    information that the minimal median values and their conrresponded
    D values are shown under each subplot.
    
    mean_tt_dict: the dictionary generated by function transit_time_summary.
    
    """
    # Turn the dictionary into DataFrame.
    mean_tt_DF = pd.DataFrame.from_dict(mean_tt_dict)
    diff_constants = mean_tt_DF.index
    all_Vout = mean_tt_DF.columns
    
    # Generating Boxplot.
    fig, axs = plt.subplots(len(all_Vout))
    fig.suptitle("Correlation between Transit Time and Diffusion Constant")
    
    for i in range(len(all_Vout)):
        Vout = all_Vout[i]
        current_mean_DF = pd.DataFrame.from_dict(mean_tt_dict[Vout])
        bp = axs[i].boxplot(current_mean_DF, showmeans = True)
        
        # Find out the minimal median value for each Vout.
        # And identify the corresponded D value.
        min_median = min(current_mean_DF.median())
        argmin = np.argmin(current_mean_DF.median())
        min_D = diff_constants[argmin]
        
        # Add line combining the meadian values.
        X=[]
        Y=[]
        for m in bp['medians']:
            [[x0, x1],[y0,y1]] = m.get_data()
            X.append(np.mean((x0,x1)))
            Y.append(np.mean((y0,y1)))
        axs[i].plot(X,Y, label = Vout)
        axs[i].set_xticklabels(diff_constants)
        axs[i].set_yscale("log", base = 10)
        axs[i].set_title(str(Vout))
        
        # Annotate the minimal median and the corresponded D value.
        axs[i].set_xlabel("minimal median ="+str(min_median)                         +" at D = "+str(min_D))
    
    
    fig.text(0.5, 0.04, "Diffusion Constants ($cm^2/min$)", ha = "center")
    fig.text(0.04, 0.5, "Transit Time ($min$)", va = "center"
            , rotation = "vertical")
    
    
    plt.show()



mean_tt_boxplot_sep_min(all_mean_tt) 





