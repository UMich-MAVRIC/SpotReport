import pygame
import sys
import os
from utils import menu_setup
from read_write import load_images, load_ans_files, input_args
from display_setup import game_display_setup

# Training Loop
def training_loop(training_imgs, training_dict):
    global new_press
    
    img_ID_training = 0 # index of the training image
    score = 0

    training_running = True
    mode = 0 # set mode to 0 to calculate score from correct dictionary

    while training_running:
            
        # Function sets up all the labels and checks if next button is clicked
        game_display_setup(args, timer, screen, fps, score, img_ID_training, mode, training_dict, imgs = training_imgs)

        # check if we want to exit training and if mouse button was released
        for event in pygame.event.get():
            # closing the window or pressing escape will exit training and take you back to the menu. can then hit escape again to quit.
            if event.type == pygame.QUIT:
                training_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    training_running = False
            if event.type == pygame.MOUSEBUTTONUP: # when a pressed mouse button is released
                new_press = True # the next mouse button press is a new press
        
        pygame.display.flip() # update the full display screen

    training_running = False
    return

#loop for menu and real images loop
def loop(args, screen, real_imgs, training_imgs, real_dict, training_dict):
    global new_press

    menu_running = True
    SR_real_running = False

    # strings to hold subID and conditionNo inputs
    subID_text_input = ''
    conditionNo_text_input = ''
    
    # rect objects to surround the user inputs
    # these are part of this loop to detect collisions for typing in the subID and conditionNo inputs
    subID_rect = pygame.rect.Rect((140, 80), (140, 35)) #create rect object to surround subID_text_input
    conditionNo_rect = pygame.rect.Rect((520, 80), (140, 35)) #create rect object to surround conditionNo_text_input
    
    # boolean of whether the user inputs are active for typing
    active_subID_box = False
    active_condNo_box = False

    # Game loop for the menu screen
    while menu_running:
        pygame.font.init() #initialize the font module
        screen.fill('gray94') #set background color
        timer.tick(fps)

        training_button, start_button = menu_setup(args, screen, subID_text_input, conditionNo_text_input, subID_rect, conditionNo_rect)

        # enter the training_loop() if the training button is clicked
        if training_button.check_click():
            # before starting, make sure the textboxes were filled out
            if subID_text_input == '' or conditionNo_text_input == '':
               print("Please fill in the Subject Id and Condition No")
            else:
               training_loop(training_imgs, training_dict)
               mode = 1 # set the mode to 1 so the real loop can run now. can still do training again if desired.

        if start_button.check_click() and mode == 1:
           menu_running = False
           SR_real_running = True # the only way to set this to True

        elif start_button.check_click() and mode == 0: # this code never seems to run, not sure why
           print("Please complete Training before progressing")
           menu_running = True
           SR_real_running = False

        for event in pygame.event.get():
            # stop running the menu loop if you close the window or press escape
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:    # any mouse button is pressed
                if subID_rect.collidepoint(event.pos):  # boolean of whether the event.pos (x,y) point is inside the rect object
                    active_subID_box = True   # clicking on the subID_rect will make the text active for typing
                else:
                    active_subID_box = False  # clicking anywhere else will make the text inactive for typing
                if conditionNo_rect.collidepoint(event.pos):
                    active_condNo_box = True
                else:
                    active_condNo_box = False
            
            if event.type == pygame.KEYDOWN and active_subID_box: # if a key is pressed and the subID textbox is active
                if event.key == pygame.K_BACKSPACE: # if backspace is pressed, remove the last character
                    subID_text_input = subID_text_input[:-1]
                else:
                    subID_text_input += event.unicode # add the pressed character

            elif event.type == pygame.KEYDOWN and active_condNo_box:
                if event.key == pygame.K_BACKSPACE:
                    conditionNo_text_input = conditionNo_text_input[:-1]
                else:
                    conditionNo_text_input += event.unicode

            elif event.type == pygame.MOUSEBUTTONUP: #when the pressed mouse button is released
                new_press = True #the next mouse button press is a new press

        pygame.display.flip() #update the full display screen

    #real images loop
    img_ID = 0 #index of the real image
    score = 0

    while SR_real_running:
        
        # Function sets up all the labels and checks if next button is clicked
        game_display_setup(args, timer, screen, fps, score, img_ID, mode, real_dict, imgs = real_imgs)

        # Event Loop
        for event in pygame.event.get(): # monitor user inputs
            if event.type == pygame.QUIT: # if X is clicked to close the window or escape is pressed, stop running the loop
                SR_real_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    SR_real_running = False
            if event.type == pygame.MOUSEBUTTONUP: # when the pressed mouse button is released
                new_press = True # the next mouse button press is a new press

        pygame.display.flip() # update the full display screen
    
    pygame.quit() # if we reached here, it is because we want to quit pygame
    return # after quitting pygame, return to main function

# Main Function
if __name__ == "__main__":

    pygame.init() # initialize all imported modules, including font
    args = input_args() # All the arguments required from user to ensure design specific/device specific use cases are met

    # Screen Width & Height
    WIDTH, HEIGHT = args.width, args.height
    screen = pygame.display.set_mode([WIDTH, HEIGHT]) #display surface
    fps = 60

    timer = pygame.time.Clock() #clock object for keeping track of time

    font = pygame.font.Font(args.font_type, args.font_size) #set the font type and size
    pygame.display.set_caption("Spot Report") #name of the window caption

    new_press = True # if the next mouse click is a new press
    mode = 0  # control boolean indicating 0 for training images mode or 1 for real images mode
    output_file_name = '' # will take the form of 'S#_C#.csv' based on what is typed in the textboxes
    # output_file_path = "Log_SpotReportScore/"
    # output_header_written = False # whether the header has already been written in the output file or not

    # read in the answer keys
    training_dict, real_dict = load_ans_files(args)

    # read in the training images
    training_imgs = load_images(args, key="train")

    # read in the real images
    real_imgs = load_images(args, key="real")

    # run the main loop
    loop(args, screen)