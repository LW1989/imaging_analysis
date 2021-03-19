# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 16:24:18 2021

@author: Lutz
"""
import pandas as pd
import numpy as np

#import .csv file saved from imagej. Important: Always put background as last Area!!!

# Pre processing function:
def pre_processing(df):
    background=df[df.columns[-1]].tolist()  #select background column and make list
    df=df.drop(df.columns[-1], axis=1) #delete last column (background)
    df=df.drop(df.columns[0], axis=1) #delte first column (frame)
    df_background_sub=df.sub(background, axis=0) #subtract background from every other column
    
    return df_background_sub

#State if you want data to be preprocessed 
pre_processing_bool=False

#creat list of dataframes; every dataframe is one dish/trial, remeber to use preprocessing function

trial_list=[(pd.read_csv('E:/Lutz imaging/Gq-Pathway Sensor/20210304/Dish1/Analysis/Results_2021_03_04_Dish1_new.csv')),
            (pd.read_csv('E:/Lutz imaging/Gq-Pathway Sensor/20210304/Dish2/Anaylsis/Results_2021_03_04_Dish2_new.csv')),
            (pd.read_csv('E:/Lutz imaging/Gq-Pathway Sensor/20210304/Dish3/Analysis/Results_2021_03_04_Dish3_new.csv')),
            #(pd.read_csv('E:/Lutz imaging/Gq-Pathway Sensor/20210304/Dish4/Analysis/Results_2021_03_04_Dish4.csv')),
            (pd.read_csv('E:/Lutz imaging/Gq-Pathway Sensor/20210305/Dish1/Analysis/Results_2021_03_05_Dish1_new.csv'))
            #(pd.read_csv('E:/Lutz imaging/Gq-Pathway Sensor/20210305/Dish2/Analysis/Results_2021_03_05_Dish2.csv')),
            #(pd.read_csv('E:/Lutz imaging/Gq-Pathway Sensor/20210305/Dish3/Analysis/Results_2021_03_05_Dish3.csv'))
            ]


if pre_processing_bool==True:
    for it_count, i in enumerate(trial_list):
        trial_list[it_count]=pre_processing(i)

#count how many ROI/Cells there are in all trials combined and add Trial number to column name

col_num=0
for it_count, number in enumerate(trial_list):
    col_num=col_num + len(number.columns)
    number.columns=list(number.columns + '_Trial_' + str(it_count+1))
    
#col_new=list(range(0,col_num))

combined_df=pd.concat(trial_list, axis=1) #combine all trials in one dataframe
  


#Calculate deltaf/f

f_base_value=0
f_pre_start=0
f_post_start=1

bla_list=[]

for column_name in combined_df:
    column=combined_df[column_name]
#    print(column)
    for i in range(0,len(column)):
        a=(column.iloc[i] - column.iloc[f_pre_start])/column.iloc[f_base_value]
        bla_list.append(a)
        
    combined_df[column_name]=bla_list
    bla_list.clear()
    #print(bla_list)    

df_mean=combined_df.mean(axis=1)
df_std=combined_df.std(axis=1)
df_sem=combined_df.sem(axis=1)

#plotting

from matplotlib import pyplot as pl

start_wash_in_1=60 #add start frame of first wash in
end_wash_in_1=180 #add end frame of first wash in

start_wash_in_2=210 #add start frame of second wash in
end_wash_in_2=400 #add end frame of second wash in

text_for_fig= 'n=' + str(col_num) + ' cells'

pl.axvspan(start_wash_in_1, end_wash_in_1, color='grey', alpha=0.3, lw=0)
pl.axvspan(start_wash_in_2, end_wash_in_2, color='grey', alpha=0.3, lw=0)
pl.plot(df_mean, c='black')
#pl.xlim(0, 400)
pl.fill_between(range(len(df_mean)), df_mean-df_std, df_mean+df_std, alpha=0.5)
pl.xlabel('Time (s)')
pl.ylabel('\u0394 F/F')
pl.title('M34 + jRCaMP; Mean + SD')
#pl.savefig('all_trials_mean_sd.eps', format='eps')
pl.show()


pl.figure(figsize=(10,5))
pl.axvspan(start_wash_in_1, end_wash_in_1, color='grey', alpha=0.3, lw=0)
pl.axvspan(start_wash_in_2, end_wash_in_2, color='grey', alpha=0.3, lw=0)
pl.plot(df_mean, c='black')
pl.fill_between(range(len(df_mean)), df_mean-df_sem, df_mean+df_sem, alpha=0.5)
x_coordinates = [0, 600]
y_coordinates = [0, 0]
pl.plot(x_coordinates, y_coordinates,linestyle='dashed',c='k', alpha=0.75)
ax = pl.gca()
#ax.set_size_inches(38, 10.5)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
pl.xlim(0, 600)
pl.ylim(-0.1, 0.4)
pl.xlabel('Time (s)')
pl.ylabel('\u0394 F/F')
pl.title('M34 + jRCaMP; Mean + SEM')
pl.text(0.9, 0.9,text_for_fig,
     horizontalalignment='center',
     verticalalignment='center',
     transform = pl.gca().transAxes)

pl.text(0.2, 0.95,'100\u03BCM 5-HT',
     horizontalalignment='center',
     verticalalignment='center',
     transform = pl.gca().transAxes)

pl.text(0.5, 0.95,'100\u03BCM ATP',
     horizontalalignment='center',
     verticalalignment='center',
     transform = pl.gca().transAxes)


#pl.savefig('all_trials_mean_sem.tiff', format='tiff')
pl.show()


fig, ax0 = pl.subplots()
im = ax0.pcolormesh((combined_df.transpose()))
fig.colorbar(im, ax=ax0, label='\u0394 F/F')
#ax0.set_title('Individual cells')
ax0.set_xlabel('Time (s)')
ax0.set_ylabel('Cell Number')
x_coordinates = [60, 60]
y_coordinates = [0, 42]
pl.plot(x_coordinates, y_coordinates,linestyle='dashed',c='k', alpha=0.75)

x_coordinates = [210, 210]
y_coordinates = [0, 42]
pl.plot(x_coordinates, y_coordinates,linestyle='dashed',c='k', alpha=0.75)

fig.text(0.1, 1.1,'100\u03BCM 5-HT',
      horizontalalignment='center',
      verticalalignment='center',
      transform = pl.gca().transAxes)

fig.text(0.35, 1.1,'100\u03BCM ATP',
      horizontalalignment='center',
      verticalalignment='center',
      transform = pl.gca().transAxes)

pl.show()


#Extract delta f/f values at specific frames for quantification

find_max_1= True #define if you want to find maximum automatically



pre_stim_frames=50 #define pre stimulus frame

post_stim_frames_1= 120 #define first post stimulus frame (i.e. first Wash in with 5-HT for Example)

if find_max_1==True:
    post_stim_frames_2=combined_df.idxmax()
else:
    post_stim_frames_2=300 #set post stim value manually for second wash in
    
#take calculated df/f for chosen frames

pre_stim_values=combined_df.iloc[pre_stim_frames]
post_stim_values_1=combined_df.iloc[post_stim_frames_1]

post_stim_values_2=[]

if find_max_1==True:
    for it_count,trial in enumerate(post_stim_frames_2):
        post_stim_values_2.append(combined_df.iloc[trial, it_count])
        
    post_stim_values_2=pd.Series(post_stim_values_2)  
    post_stim_values_2.index=post_stim_frames_2.index
else:
    post_stim_values_2=combined_df.iloc[post_stim_frames_2]
    
df_values_combined=pd.concat([pre_stim_values,post_stim_values_1,post_stim_values_2],axis=1)
df_values_combined.columns=['Baseline', '5-HT', 'ATP']

df_values_combined_stats=pd.DataFrame()
df_values_combined_stats['Mean']=df_values_combined.mean(axis=0)
df_values_combined_stats['STD']=df_values_combined.std(axis=0)
df_values_combined_stats['SEM']=df_values_combined.sem(axis=0)


pl.figure(figsize=(10,5))
df_values_combined_stats['Mean'].plot(kind='bar', yerr=df_values_combined_stats['STD'], color=['grey', 'blue', 'red'])
ax = pl.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
pl.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=True) # labels along the bottom edge are off
pl.xticks(rotation=45)
pl.ylim(-0.1, 1)
pl.ylabel('\u0394 F/F')
pl.title('Mean of \u0394 F/F before and after 5-HT and ATP stimulation')


