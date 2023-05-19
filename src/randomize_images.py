import random
import os
import pandas as pd


#this file will randomly order (rename) the spot report images
#you need to manually perform some actions in the updated spot_report_answer_key.csv afterwards. These steps are detailed at the end of this script.
#do NOT run this script again before doing these steps to clean the .csv

total_images = 165
new_Image_ID = random.sample(range(1,total_images + 1), total_images) #randomized list of non-repeating 165 numbers from 1 to 165

#read file name for each image and rename using "new_" + str(new_Image_ID[i])
for i in range(total_images): #loop from 0 to total_images-1
    if i+1 <= 9:
        str_Image_ID = '00' + str(i+1) #because images are numbered 001, 002, ..., 010, 011 so they are read in the correct order in the spot report task
    elif i+1 <= 99:
        str_Image_ID = '0' + str(i+1)
    else:
        str_Image_ID = str(i+1)
    filename = 'real_images/' + str_Image_ID + '.png'
    if new_Image_ID[i] <= 9:
        str_new_Image_ID = '00' + str(new_Image_ID[i]) #so images get numbered 001, 002, ..., 010, 011
    elif new_Image_ID[i] <= 99:
        str_new_Image_ID = '0' + str(new_Image_ID[i])
    else:
        str_new_Image_ID = str(new_Image_ID[i])
    new_filename = 'real_images/new_' + str_new_Image_ID + '.png'
    os.rename(filename, new_filename)
#remove the "new_" from each file name
for i in range(total_images):
    if i+1 <= 9:
        str_new_Image_ID = '00' + str(i+1) #because images are numbered 001, 002, ..., 010, 011
    elif i+1 <= 99:
        str_new_Image_ID = '0' + str(i+1)
    else:
        str_new_Image_ID = str(i+1)
    filename = 'real_images/new_' + str_new_Image_ID + '.png'
    new_filename = 'real_images/' + str_new_Image_ID + '.png'
    os.rename(filename, new_filename)

#overwrite Image_ID column with new_Image_ID
df = pd.read_csv('answer_keys/spot_report_answer_key.csv')
df['Image_ID'] = new_Image_ID
df.to_csv('answer_keys/spot_report_answer_key.csv')
#now open up spot_report_answer_key.csv in Excel and delete the first column as it is an unncessary index
#now select all of the data without the headers. 
#click 'Sort & Filter' from the Editing section on the Home tab, click 'Custom Sort', and sort by Image_ID from smallest to largest
#hit save
#do NOT run this script again before doing these steps to clean the .csv


