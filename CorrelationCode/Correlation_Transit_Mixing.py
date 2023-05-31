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



def mean_transit_time_boxplot(mean_tt_dict, diff_constants_xaxis):
    """
    Given the dictionary with various diffusion constants as keys and arrays
    of mean transit time (of each replicate) as values, the function return
    a boxplot with median connected by a line. 
    
    mean_tt_dict: the dictionary generated with function mean_transit_time.
    diff_constants_xaxis: a list containing considered diffusion constants.
    
    """
    # Turn dictionary into DataFrames.
    mean_DF = pd.DataFrame.from_dict(mean_tt_dict)
    
    # Generating Boxplot.
    mean_box_plot = plt.figure()
    bp = plt.boxplot(mean_DF, showmeans = True)

    # Add line combining the meadian values.
    X=[]
    Y=[]
    for m in bp['medians']:
        [[x0, x1],[y0,y1]] = m.get_data()
        X.append(np.mean((x0,x1)))
        Y.append(np.mean((y0,y1)))
    plt.plot(X,Y,c='C1')

    plt.xticks(list(range(1, len(diff_constants_xaxis)+1))
               , diff_constants_xaxis)
    plt.xlabel("Diffusion Constants ($cm^2/min$)")
    plt.ylabel("Transit Time ($min$)")
    plt.yscale("log", base = 10)
    plt.title("Correlation between Transit Time and Diffusion Constant")
    plt.show()



def mean_transit_time_line(mean_tt_dict):
    """
    Given the dictionary with various diffusion constants as keys and arrays
    of mean transit time (of each replicate) as values, the function return
    a a plot with mean values connected with dashed line. 
    
    mean_tt_dict: the dictionary generated with function mean_transit_time.
    """
    # Turn dictionary into DataFrames.
    DF = pd.DataFrame.from_dict(mean_tt_dict)
    mean_DF = DF.mean()
    
    # Generating plot.
    plt.figure()
    plt.plot(mean_DF, "-o")
    plt.xlabel("Diffusion Constants ($cm^2/min$)")
    plt.ylabel("Mean Transit Time ($min$)")
    plt.yscale("log", base = 10)
    plt.title("Correlation between Transit Time and Diffusion Constant")
    plt.show()
    
    return mean_DF


# ### Case 1: D= 0.01, 0.02, 0.03, ..., 0.09, 0.1

# Input of all modelling data.

diff_001 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.01"
                   ,0.01)
diff_002 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.02"
                   ,0.02)
diff_003 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.03"
                   ,0.03)
diff_004 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.04"
                   ,0.04)
diff_005 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.05"
                   ,0.05)
diff_006 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.06"
                   ,0.06)
diff_007 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.07"
                   ,0.07)
diff_008 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.08"
                   ,0.08)
diff_009 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.09"
                   ,0.09)
diff_01 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.1"
                   ,0.1)



# Merge all data together in one dictionary.

all_diff_transit = {**diff_001, **diff_002, **diff_003, **diff_004
                   , **diff_005, **diff_006, **diff_007, **diff_008
                   , **diff_009, **diff_01}

mean_tt = mean_transit_time(all_diff_transit)


mean_DF = pd.DataFrame.from_dict(mean_tt)

diff_constants_xaxis = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08
                       , 0.09, 0.1]
mean_box_plot = plt.figure(figsize = (10,7))
plt.boxplot(mean_DF, showmeans = True)
plt.xticks(list(range(1, len(diff_constants_xaxis)+1))
           , diff_constants_xaxis)
plt.xlabel("Diffusion Constants ($cm^2/min$)")
plt.ylabel("Transit Time ($min$)")
plt.title("Correlation between Transit Time and Diffusion Constant")
plt.show()



diff_constants_xaxis = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08
                       , 0.09, 0.1]
mean_box_plot = plt.figure(figsize = (10,7))
bp = plt.boxplot(mean_DF, showmeans = True)

# Add line combining the meadian values.
X=[]
Y=[]
for m in bp['medians']:
    [[x0, x1],[y0,y1]] = m.get_data()
    X.append(np.mean((x0,x1)))
    Y.append(np.mean((y0,y1)))
plt.plot(X,Y,c='C1')

plt.xticks(list(range(1, len(diff_constants_xaxis)+1))
           , diff_constants_xaxis)
plt.xlabel("Diffusion Constants ($cm^2/min$)")
plt.ylabel("Transit Time ($min$)")
plt.title("Correlation between Transit Time and Diffusion Constant")
plt.show()


# ### Case 2: D= 0.001, 0.01, 0.1


# Input of modeling data.

#diff1E5 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.00001"
#                   ,"D=0.00001")
#diff1E4 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.0001"
#                   ,"D=0.0001")
diff1E3 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.001"
                   ,0.001)
diff1E2 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.01"
                   ,0.01)
diff1E1 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.1"
                   ,0.1)
all_diff_transit = {**diff1E3, **diff1E2, **diff1E1}

mean_tt = mean_transit_time(all_diff_transit)

diff_constants_xaxis = [0.001, 0.01, 0.1]

mean_transit_time_boxplot(mean_tt, diff_constants_xaxis)


# ### Case 3: D = 0.01, 0.02, ..., 0.09, 0.1, 0.2, ..., 0.7

# Input modeling data.

diff_02 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.2"
                   ,0.2)
diff_03 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.3"
                   ,0.3)
diff_04 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.4"
                   ,0.4)
diff_05 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.5"
                   ,0.5)
diff_06 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.6"
                   ,0.6)
diff_07 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.7"
                   ,0.7)

all_diff_transit = {**diff_001, **diff_002, **diff_003, **diff_004
                   , **diff_005, **diff_006, **diff_007, **diff_008
                   , **diff_009, **diff_01, **diff_02, **diff_03
                   , **diff_04, **diff_05, **diff_06, **diff_07}

mean_tt = mean_transit_time(all_diff_transit)
diff_constants_xaxis = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07
                        , 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

mean_transit_time_boxplot(mean_tt, diff_constants_xaxis)


# ### Case 4: D = 0.001, 0.01, ...., 0.09, 0.1, 0.2, 0.3, ..., 0.7

diff_0015 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.015"
                   ,0.015)
diff_0025 = read_txt("F:\Geothe Universität\WS22_23-SS23\Praktikum_AK_Koch\CorrelationData\Vout=100\Diff=0.025"
                   ,0.025)

all_diff_transit = {**diff1E3, **diff_001, **diff_0015
                    , **diff_002, **diff_0025
                    , **diff_003, **diff_004
                   , **diff_005, **diff_006, **diff_007, **diff_008
                   , **diff_009, **diff_01, **diff_02, **diff_03
                   , **diff_04, **diff_05, **diff_06, **diff_07}

mean_tt = mean_transit_time(all_diff_transit)

diff_constants_xaxis = [0.001, 0.01, 0.015, 0.02, 0.025, 0.03
                        , 0.04, 0.05, 0.06, 0.07
                        , 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

mean_transit_time_boxplot(mean_tt, diff_constants_xaxis)

all_diff_transit = {**diff1E3, **diff_001, **diff_0015
                    , **diff_002, **diff_0025
                    , **diff_003, **diff_004
                   , **diff_005, **diff_006, **diff_007, **diff_008
                   , **diff_009, **diff_01, **diff_02, **diff_03
                   , **diff_04, **diff_05, **diff_06, **diff_07}

mean_tt = mean_transit_time(all_diff_transit)

mean_transit_time_line(mean_tt)

all_diff_transit = {**diff1E3, **diff_001, **diff_002
                    , **diff_003, **diff_004
                   , **diff_005, **diff_006, **diff_007, **diff_008
                   , **diff_009, **diff_01, **diff_02, **diff_03
                   , **diff_04, **diff_05, **diff_06, **diff_07}

mean_tt = mean_transit_time(all_diff_transit)

diff_constants_xaxis = [0.001, 0.01, 0.02, 0.03
                        , 0.04, 0.05, 0.06, 0.07
                        , 0.08, 0.09, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

mean_transit_time_boxplot(mean_tt, diff_constants_xaxis)

all_diff_transit = {**diff1E3, **diff_001, **diff_002
                    , **diff_003, **diff_004
                   , **diff_005, **diff_006, **diff_007, **diff_008
                   , **diff_009, **diff_01, **diff_02, **diff_03
                   , **diff_04, **diff_05, **diff_06, **diff_07}

mean_tt = mean_transit_time(all_diff_transit)

mean_transit_time_line(mean_tt)

plt.close("all")



