import glob
import pandas as pd
import argparse
import pygame

# Function to load the training and real images into the program
def load_images(args, key):
    # Loading images 
    if key == "train":
        image_path = args.train_images
    elif key == "real":
        image_path = args.real_images
    else:
        print("Error in loading images, key not mentioned (Should be train or real)")
    
    img_list = []
    images = sorted(glob.glob(image_path)) # put the images in file names into a list sorted alphabetically
    for filename in images:
        img = pygame.image.load(filename) # returns a surface object that has the image drawn onto it. This is separate from the display surface object so later we have to blit it (copy contents of one surface onto another)
        img_list.append(pygame.transform.scale(img, (args.img_scale_x, args.img_scale_y))) # scale the image size and append the surface object to the real_imgs[] list
    
    return img_list

def load_ans_files(args):
    answer_files = sorted(glob.glob(args.ans_keys)) #put the training and real answer key file names into a list sorted alphabetically
    dict_i = 0    #to assign the answer keys to dictionaries
    training_dict, real_dict = None, None
    
    for file in answer_files:
        df = pd.read_csv(file, index_col = 0) #read in the csv file and use the 0th column (Image_ID) as the row labels of the data frame
        df_dict = df.to_dict('split') #convert df to a dictionary as {'index': ['T1', 'T2', 'T3', 'T4', 'T5'], 'columns': ['People', 'Vehicles', 'Bags', 'Barrels', 'Antennas'], 'data': [[0, 5, 0, 0, 5], [0, 0, 0, 0, 0], [2, 0, 2, 0, 1], [0, 0, 1, 1, 0], [2, 2, 2, 2, 0]]}
        del df_dict['index'] #delete the 'index' key
        del df_dict['columns'] #delete the 'columns' key so the dictionary is just the data as {'data': [[0, 5, 0, 0, 5], [0, 0, 0, 0, 0], [2, 0, 2, 0, 1], [0, 0, 1, 1, 0], [2, 2, 2, 2, 0]]}
        if dict_i == 0:
            real_dict = df_dict #the first file in csv_file is the real answer key
        elif dict_i == 1:
            training_dict = df_dict #the second file in csv_file is the training answer key
        dict_i += 1
    
    return training_dict, real_dict

# Function to get all input arguments from user to run the game - Once deployed the user should need to only change the values in 
# this file to achieve desired result
def input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('width', type=int, default=1368)
    parser.add_argument('height', type=int, default=790)
    parser.add_argument('train_images', type=str, default='training_images/*.png',
                        help="File path for the training images used in the quiz game")
    parser.add_argument('real_images', type=str, default='real_images/*.png',
                        help="File path for the real images used in the quiz game")
    parser.add_argument('ans_keys', type=str, default='answer_keys/*.csv', 
                        help="The file where answer keys are written")
    parser.add_argument('output_file_path', type=str, default='output_files/score.csv', 
                        help="Output file where score is written from the quiz")
    parser.add_argument('output_mouse_path', type=str, default='output_files/mouse_position.csv',
                        help="Output file where the mouse positions are written")
    parser.add_argument('font_type', type=str, default='freesansbold.ttf',
                        help="Default font type used for the entire program")
    parser.add_argument('font_size', type=int, default=18,
                        help="This is just for default font size, user needs to re-size this for their specific device")
    parser.add_argument('add_pos_x', type=int, default=1160, 
                        help="x position of Add button on the screen, remains same for all the add buttons")
    parser.add_argument('start_ypos', type=int, default=90, 
                        help="The starting y position for both Add and Subtract buttons")
    parser.add_argument('sub_pos_x', type=int, default=850, 
                        help="x position of Subtract button on the screen, remains same for all the subtract buttons")
    parser.add_argument('delta', type=int, default=120, 
                        help="The difference between the y position of the Add and Subtract buttons on the screen")
    parser.add_argument('label_xpos', type=int, default=1000, 
                        help="Label positions for all the Buttons")
    parser.add_argument('label_start_ypos', type=int, default=110, 
                        help="Starting y position for the labels")
    parser.add_argument('img_scale_x', type=int, default=750, 
                        help="Resizing the image sizes for the game, can be different depending upon user preference")
    parser.add_argument('img_scale_y', type=int, default=500, 
                        help="Resizing the image sizes for the game, can be different depending upon user preference")
    parser.add_argument('img_pos_x', type=int, default=40, 
                        help="x position of the image on the game screen")
    parser.add_argument('img_pos_y', type=int, default=130,
                        help="y position of the image on the game screen")
    args = parser.parse_args()
    return args