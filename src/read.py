# Contains all functions for reading the input files, images and getting user input for command line.
"""
For default run this on the command line with the file path to get the default setup - 1368 790 
'training_images/*.png' 'task_images/*.png' 'answer_keys/*.csv' 'output_files/score.csv' 'output_files/mouse_position.csv' 
'freesansbold.ttf' 18 1160 90 850 120 1000 110 750 500 40 130
"""

import glob
import pandas as pd
import argparse
import pygame

#Function to load image of examples of each target object. It is later added on the menu
def ex_menu_image(args):
    ex_img = pygame.image.load(args.example_objects) #examples of each target object
    ex_img = pygame.transform.scale(ex_img, (650, 400)) #??? make into args
    return ex_img

#Function to read in the training and task images into the program
def load_images(args, key):
    if key == "train":
        image_path = args.train_images_path
    elif key == "task":
        image_path = args.task_images_path
    
    img_list = []
    images = sorted(glob.glob(image_path)) #put the images file names at this path into a list sorted alphabetically
    for filename in images:
        img = pygame.image.load(filename) #returns a surface object that has the image drawn onto it. This is separate from the display surface object so later we have to blit it (copy contents of one surface onto another)
        img_list.append(pygame.transform.scale(img, (args.img_scale_x, args.img_scale_y))) #scale the image size and append the surface object to the img_list[] list
    
    return img_list

#Function to read in the answer keys
def load_ans_files(args):
    answer_files = sorted(glob.glob(args.ans_keys_path)) #put the training and task answer key file names into a list sorted alphabetically
    dict_i = 0 #to assign the answer keys to dictionaries
    training_dict, task_dict = None, None
    
    for file in answer_files:
        df = pd.read_csv(file, index_col = 0) #read in the csv file and use the 0th column (Image_ID) as the row labels of the data frame
        df_dict = df.to_dict('split') #convert df to a dictionary as {'index': ['T1', 'T2', 'T3', 'T4', 'T5'], 'columns': ['People', 'Vehicles', 'Bags', 'Barrels', 'Antennas'], 'data': [[0, 5, 0, 0, 5], [0, 0, 0, 0, 0], [2, 0, 2, 0, 1], [0, 0, 1, 1, 0], [2, 2, 2, 2, 0]]}
        del df_dict['index'] #delete the 'index' key
        del df_dict['columns'] #delete the 'columns' key so the dictionary is just the data as {'data': [[0, 5, 0, 0, 5], [0, 0, 0, 0, 0], [2, 0, 2, 0, 1], [0, 0, 1, 1, 0], [2, 2, 2, 2, 0]]}
        if dict_i == 0:
            task_dict = df_dict #the first file in csv_file is the task answer key
        elif dict_i == 1:
            training_dict = df_dict #the second file in csv_file is the training answer key
        dict_i += 1
    
    return training_dict, task_dict

# Function to get all input arguments from user to run the game - Once deployed the user should need to only change the values in 
# this file to achieve desired result
def input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('width', nargs='?', type=int, default=1368)
    parser.add_argument('height', nargs='?',type=int, default=790)
    parser.add_argument('example_objects', nargs='?',type=str, default='resource/examples.png',
                        help="File for the example objects shown on the menu")
    parser.add_argument('train_images_path', nargs='?', type=str, default='training_images/*.png',
                        help="File path for the training images used in training")
    parser.add_argument('task_images_path', nargs='?', type=str, default='task_images/*.png',
                        help="File path for the task images used in the spot report task")
    parser.add_argument('ans_keys_path', nargs='?', type=str, default='answer_keys/*.csv', 
                        help="Path where answer keys are stored")
    parser.add_argument('output_file_path', nargs='?', type=str, default='output_files/', 
                        help="Path where output csv files are written to") #output file name includes subID and condNo
    parser.add_argument('font_type', nargs='?', type=str, default='freesansbold.ttf',
                        help="Default font type used for the entire program")
    parser.add_argument('font_size', nargs='?', type=int, default=18,
                        help="This is just for default font size, user needs to re-size this for their specific device")
    parser.add_argument('add_pos_x', nargs='?', type=int, default=1160, 
                        help="x position of Add button on the screen, remains same for all the add buttons")
    parser.add_argument('add_sub_pos_y', nargs='?', type=int, default=90, 
                        help="The starting y position for both Add and Subtract buttons")
    parser.add_argument('sub_pos_x', nargs='?', type=int, default=850, 
                        help="x position of Subtract button on the screen, remains same for all the subtract buttons")
    parser.add_argument('delta', nargs='?', type=int, default=120, 
                        help="The difference between the y position of the Add and Subtract buttons and user count labels on the screen")
    parser.add_argument('label_xpos', nargs='?', type=int, default=1000, 
                        help="Label positions for all object categories")
    parser.add_argument('label_ypos', nargs='?', type=int, default=110, 
                        help="Starting y position for the labels")
    parser.add_argument('next_xpos', nargs='?', type=int, default=1080, 
                        help="x position for the Next button")
    parser.add_argument('next_ypos', nargs='?', type=int, default=690, 
                        help="y position for the Next button")
    parser.add_argument('img_scale_x', nargs='?', type=int, default=750, 
                        help="Resizing the image sizes for the game, can be different depending upon user preference")
    parser.add_argument('img_scale_y', nargs='?', type=int, default=500, 
                        help="Resizing the image sizes for the game, can be different depending upon user preference")
    parser.add_argument('img_pos_x', nargs='?', type=int, default=40, 
                        help="x position of the image on the game screen")
    parser.add_argument('img_pos_y', nargs='?', type=int, default=130,
                        help="y position of the image on the game screen")
    args = parser.parse_args()
    return args