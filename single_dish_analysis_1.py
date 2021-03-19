# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 16:24:18 2021

@author: Lutz
"""
import pandas as pd

#import .csv file saved from imagej. Important: Always put background as last Area!!!


# Pre processing function:
def pre_processing(df):
    background=df[df.columns[-1]].tolist()  #select background column and make list
    df=df.drop(df.columns[-1], axis=1) #delete last column (background)
    df=df.drop(df.columns[0], axis=1) #delte first column (frame)
    df_background_sub=df.sub(background, axis=0) #subtract background from every other column
    
    return df_background_sub

#If you want to exclude rois specified in line further down set exclude_rois=True
exclude_rois=False

#If you want to turn off preprocessing (e.g. fi you allready did that and want to plot cleaned data again set pre_processing_bool=False)

pre_processing_bool=True

file_extension='.csv'

# path_to_data='E:/Lutz imaging/Gq-Pathway Sensor/20210304/Dish1/Analysis/Results_2021_03_04_Dish1.csv'
# path_to_data='E:/Lutz imaging/Gq-Pathway Sensor/20210304/Dish2/Anaylsis/Results_2021_03_04_Dish2.csv' 
path_to_data='E:/Lutz imaging/Gq-Pathway Sensor/20210304/Dish3/Analysis/Results_2021_03_04_Dish3.csv'
# path_to_data='E:/Lutz imaging/Gq-Pathway Sensor/20210305/Dish1/Analysis/Results_2021_03_05_Dish1.csv'

if pre_processing_bool==True:
    df=pre_processing(pd.read_csv(path_to_data))
else:
    df=pd.read_csv(path_to_data)
    
    
# df_1=pre_processing(pd.read_csv(path_to_data_1))

#delete ROIs that you dont want to include REMEMBER TO START COUNTING FROM 0!!!

if exclude_rois==True:
    test_columns=df.iloc[:, [17]].columns
    df=df.drop(columns=test_columns)
    
    df.to_csv((path_to_data[:-4] + '_new' + file_extension), index=False)

# Input if you want to convert frames to seconds
frames_to_seconds=False


if frames_to_seconds==True:
    fps_rate=1 #Change to actual framerate
    df.index=df.index/fps_rate
    x_label='Time (s)'
else:
    x_label='Frames'

#Calculate deltaf/f

f_base_value=0
f_pre_start=0
f_post_start=1

bla_list=[]

for column_name in df:
    column=df[column_name]
#    print(column)
    for i in range(0,len(column)):
        a=(column.iloc[i] - column.iloc[f_pre_start])/column.iloc[f_base_value]
        bla_list.append(a)
        
    df[column_name]=bla_list
    bla_list.clear()
    #print(bla_list)    

df_mean=df.mean(axis=1)
df_std=df.std(axis=1)
df_sem=df.sem(axis=1)

# #plotting

from matplotlib import pyplot as pl
col_num=len(df.columns)


#plotting individual ROIs
number_of_subplots=list(range(0,len(df.columns)))
df.plot(subplots=True, layout=(7, 5), figsize=(24, 24), sharex=False, legend=None, title=number_of_subplots);

#plotting individual ROIs 2
df.plot(legend=None)
ax = pl.gca()
pl.xlabel(x_label)
pl.ylabel('\u0394 F/F')
#ax.axes.xaxis.set_visible(False)
#ax.axes.yaxis.set_ticklabels([])
pl.show()

#plotting mean + SD

pl.plot(df_mean)
pl.fill_between(range(len(df_mean)), df_mean-df_std, df_mean+df_std, alpha=0.5)
pl.xlabel(x_label)
pl.ylabel('\u0394 F/F')
pl.title('M34 + jRCaMP; Mean + SD')
pl.show()

#plotting mean + SEM

pl.plot(df_mean)
pl.fill_between(range(len(df_mean)), df_mean-df_sem, df_mean+df_sem, alpha=0.5)
pl.xlabel(x_label)
pl.ylabel('\u0394 F/F')
pl.title('M34 + jRCaMP; Mean + SEM')
#pl.xlim(0,599)
pl.show()


# dies ist ein test, kann man das lesen?
abc=[]

