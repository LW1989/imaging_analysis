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

pre_processing_bool=False

file_extension='.csv'

# path_to_data='E:/Lutz imaging/Gq-Pathway Sensor/20210304/Dish1/Analysis/Results_2021_03_04_Dish1_new.csv'
# path_to_data='E:/Lutz imaging/Gq-Pathway Sensor/20210304/Dish2/Anaylsis/Results_2021_03_04_Dish2_new.csv' 
#path_to_data='E:/Lutz imaging/Gq-Pathway Sensor/20210304/Dish3/Analysis/Results_2021_03_04_Dish3_new.csv'
path_to_data='E:/Lutz imaging/Gq-Pathway Sensor/20210305/Dish1/Analysis/base.csv'

if pre_processing_bool==True:
    df=pre_processing(pd.read_csv(path_to_data))
else:
    df=pd.read_csv(path_to_data)

# df.columns=df.iloc[0]
df.drop(0,axis=0, inplace=True)    
df.drop(df.columns[0],axis=1, inplace=True)    
    
#delete ROIs that you dont want to include REMEMBER TO START COUNTING FROM 0!!!
list_of_excluded_rois=[] #add ROIs that you want to exclude. Seperate by ','


if exclude_rois==True:
    test_columns=df.iloc[:, list_of_excluded_rois].columns
    df=df.drop(columns=test_columns)
    
    #This line saves your new data as csv file with the same name + '_new' to the same path
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
    column=column.astype('float')
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


#plotting individual ROIs in individual subplots
number_of_subplots=list(range(0,len(df.columns)))
df.plot(subplots=True, layout=(7, 5), figsize=(24, 24), sharex=True, legend=None, title=number_of_subplots);

#plotting individual ROIs in ONE plot (overlayed)
df.plot(legend=None)
ax = pl.gca()
pl.xlabel(x_label)
pl.ylabel('\u0394 F/F')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
pl.show()

#plotting mean + SD

pl.plot(df_mean, color='black', linewidth=0.75)
pl.fill_between(range(len(df_mean)), df_mean-df_std, df_mean+df_std, alpha=0.5)
x_coordinates = [0, len(df_mean)]
y_coordinates = [0, 0]
pl.plot(x_coordinates, y_coordinates,linestyle='dashed',c='k', alpha=0.75)
ax = pl.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
pl.xlim(0,600)
# pl.ylim(0,1)
pl.xlabel(x_label)
pl.ylabel('\u0394 F/F')
pl.title('M34 + jRCaMP; Mean + SD')
pl.savefig((path_to_data[:-4] + '_mean_SD' + '.svg'), format = 'svg', dpi=300) # uncommand this if you want to save it as vector graphic
pl.show()

#plotting mean + SEM

pl.plot(df_mean, color='black', linewidth=0.75)
pl.fill_between(range(len(df_mean)), df_mean-df_sem, df_mean+df_sem, alpha=0.5)
pl.plot(x_coordinates, y_coordinates,linestyle='dashed',c='k', alpha=0.75)
ax = pl.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
pl.xlim(0,600)
# pl.ylim(0,1)
pl.xlabel(x_label)
pl.ylabel('\u0394 F/F')
pl.title('M34 + jRCaMP; Mean + SEM')
#pl.xlim(0,599)
pl.savefig((path_to_data[:-4] + '_mean_SEM' + '.svg'), format = 'svg', dpi=300) # uncommand this if you want to save it as vector graphic
pl.show()

