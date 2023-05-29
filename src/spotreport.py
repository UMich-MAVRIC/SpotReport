# Main File to run the Spot Report Quiz game
# need to add running command.
# python3 sportreport.py 1368 790 'training_images\*.png' 'real_images\*.png' 'answer_keys\*.csv' 'output_files\score.csv' 'output_files\mouse_position.csv' 'freesansbold.ttf' 18 1160 90 850 120 1000 110 750 500 40 130
import pygame
import time
from utils import menu_setup
from read import load_images, load_ans_files, input_args
from utils import Button
from display_setup import Game_Disp_Setup
from score import Score, Mouse_Pos
from pylsl_function import lsl_outlet_mouse_pos, lsl_outlet_mouse_btn, lsl_outlet_processing_time, lsl_outlet_spt_task_scores

# Training Loop
def training_loop(training_imgs, training_dict, new_press):
    
    img_ID_training = 0 # index of the training image
    score = 0

    people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0 # user counts
    obj_scores = [people_val, vehicle_val, bags_val, barrels_val, antennas_val]

    training_running = True
    mode = 0 # set mode to 0 to calculate score from correct dictionary


    while training_running:
        
        screen.fill('white')
        timer.tick(fps)

        # Sets up the labels for all the add buttons
        add_button_list = Game_Disp_Setup.add_buttons(args, screen)

        # Buttons only increase counts up to 5
        for i in range(len(add_button_list)):
            if add_button_list[i].check_click(new_press, args):
                new_press = False
                if obj_scores[i] == 5:
                    continue
                else:
                    obj_scores[i] += 1

        # Sets up the labels for all the subtract buttons
        sub_button_list = Game_Disp_Setup.subtract_buttons(args, screen)

        # Buttons only decrease counts down to 0
        for i in range(len(sub_button_list)):
            if sub_button_list[i].check_click(new_press, args):
                new_press = False
                if obj_scores[i] == 0:
                    continue
                else:
                    obj_scores[i] -= 1

        Game_Disp_Setup.count_object_labels(args, screen, obj_scores)

        # Button for Next
        x_pos = args.label_xpos     # Store the x position for the Next button 
        y_pos = args.label_start_ypos + 4*args.delta    # Store the y position for the Next button
        next_button = Button(screen, 'Next', x_pos + 80, y_pos + 100)   # The values 80 & 100 are the deltas for x & y position respectively, change if reuqired
        
        # labels for target object types, 'score' and score value
        Game_Disp_Setup.labels(args, screen, score)

        screen.blit(training_imgs[img_ID_training], (args.img_pos_x, args.img_pos_y)) # Display the current real image

        # When Next button is clicked, update the score and show next image
        if next_button.check_click(new_press, args):
            new_press = False
            new_points = Score.calculate_score(args, img_ID_training, obj_scores, mode, score, training_dict)
            score += new_points

            img_ID_training += 1 # incrememnt the img_ID
            people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0
            obj_scores = [people_val, vehicle_val, bags_val, barrels_val, antennas_val]

            # if last real image, reset img_ID back to 0 to loop through images again
            if img_ID_training >= len(training_imgs):
                img_ID_training = 0
                screen.blit(training_imgs[img_ID_training], (args.img_pos_x, args.img_pos_y))
            else:
                screen.blit(training_imgs[img_ID_training], (args.img_pos_x, args.img_pos_y)) # display the next image
        
        # Check if we want to exit training and if mouse button was released
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
def loop(args, screen, real_imgs, training_imgs, real_dict, training_dict, new_press):

    menu_running = True
    SR_real_running = False

    # strings to hold subID and conditionNo inputs
    subID_text_input = ''
    conditionNo_text_input = ''
    
    # rect objects to surround the user inputs
    # these are part of this loop to detect collisions for typing in the subID and conditionNo inputs
    subID_rect = pygame.rect.Rect((140, 80), (140, 35)) # create rect object to surround subID_text_input
    conditionNo_rect = pygame.rect.Rect((520, 80), (140, 35)) # create rect object to surround conditionNo_text_input
    
    # Mouse Position Initialization
    Mouse_Pos(args)

    people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0 # user counts
    obj_scores = [people_val, vehicle_val, bags_val, barrels_val, antennas_val]
    
    # boolean of whether the user inputs are active for typing
    active_subID_box = False
    active_condNo_box = False

    mode = 0        # Help differentiate between training and real loop
    previous_time_task = 0

    # Game loop for the menu screen
    while menu_running:
        pygame.font.init() #initialize the font module
        screen.fill('gray94') #set background color
        timer.tick(fps)

        training_button, start_button = menu_setup(args, screen, subID_text_input, conditionNo_text_input, subID_rect, conditionNo_rect)

        # enter the training_loop() if the training button is clicked
        if training_button.check_click(new_press, args):
            new_press = False
            # before starting, make sure the textboxes were filled out
            if subID_text_input == '' or conditionNo_text_input == '':
               print("Please fill in the Subject Id and Condition No")
            else:
               training_loop(training_imgs, training_dict, new_press)
               mode = 1 # set the mode to 1 so the real loop can run now. can still do training again if desired.

        if start_button.check_click(new_press, args) and mode == 1:
           new_press = False
           menu_running = False
           SR_real_running = True # the only way to set this to True
           previous_time_task = time.time()

        elif start_button.check_click(new_press, args) and mode == 0: # this code never seems to run, not sure why
           print("Please complete Training before progressing")
           new_press = False
           menu_running = True
           SR_real_running = False

        for event in pygame.event.get():
            # stop running the menu loop if you close the window or press escape
            #print(event)
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:    # any mouse button is pressed
                lsl_outlet_mouse_btn("Pressed") # send true or 1

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

            elif event.type == pygame.MOUSEBUTTONUP: # when the pressed mouse button is released
                new_press = True # the next mouse button press is a new press
            
            elif event.type == pygame.MOUSEMOTION: # when the pressed mouse button is released
                lsl_outlet_mouse_pos(event.pos)
                
            
        pygame.display.flip() # update the full display screen

    # real images loop
    img_ID = 0 # index of the real image
    score = 0

    # write the header for the output file
    output_header = Score.score_header(args, mode)

    while SR_real_running and output_header:
        
        screen.fill('white')
        timer.tick(fps)

        # Sets up the labels for all the add buttons
        add_button_list = Game_Disp_Setup.add_buttons(args, screen)

        # Buttons only increase counts up to 5
        for i in range(len(add_button_list)):
            if add_button_list[i].check_click(new_press, args):
                new_press = False
                if obj_scores[i] == 5:
                    continue
                else:
                    obj_scores[i] += 1

        # Sets up the labels for all the subtract buttons
        sub_button_list = Game_Disp_Setup.subtract_buttons(args, screen)

        # Buttons only decrease counts down to 0
        for i in range(len(sub_button_list)):
            if sub_button_list[i].check_click(new_press, args):
                new_press = False
                if obj_scores[i] == 0:
                    continue
                else:
                    obj_scores[i] -= 1

        Game_Disp_Setup.count_object_labels(args, screen, obj_scores)

        # Button for Next
        x_pos = args.label_xpos     # Store the x position for the Next button 
        y_pos = args.label_start_ypos + 4*args.delta    # Store the y position for the Next button
        next_button = Button(screen, 'Next', x_pos + 80, y_pos + 100)   # The values 80 & 100 are the deltas for x & y position respectively, change if reuqired
        
        # labels for target object types, 'score' and score value
        Game_Disp_Setup.labels(args, screen, score)

        screen.blit(real_imgs[img_ID], (args.img_pos_x, args.img_pos_y)) # Display the current real image

        # When Next button is clicked, update the score and show next image
        if next_button.check_click(new_press, args):
            start_time_task = time.time()
            
            new_press = False
            new_points = Score.calculate_score(args, img_ID, obj_scores, mode, score, real_dict)
            score += new_points

            img_ID += 1 # incrememnt the img_ID
            people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0
            obj_scores = [people_val, vehicle_val, bags_val, barrels_val, antennas_val]

            # if last real image, reset img_ID back to 0 to loop through images again
            if img_ID >= len(real_imgs):
                img_ID = 0
                screen.blit(real_imgs[img_ID], (args.img_pos_x, args.img_pos_y))
            else:
                screen.blit(real_imgs[img_ID], (args.img_pos_x, args.img_pos_y)) # display the next image
            
            task_time = start_time_task - previous_time_task # calculate task time
            lsl_outlet_processing_time(img_ID, task_time)
            
            previous_time_task = start_time_task

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
    screen = pygame.display.set_mode([args.width, args.height]) #display surface
    fps = 60

    timer = pygame.time.Clock() #clock object for keeping track of time

    font = pygame.font.Font(args.font_type, args.font_size) #set the font type and size
    pygame.display.set_caption("Spot Report") #name of the window caption

    new_press = True # if the next mouse click is a new press

    # read in the answer keys
    training_dict, real_dict = load_ans_files(args)

    # read in the training images
    training_imgs = load_images(args, key="train")

    # read in the real images
    real_imgs = load_images(args, key="real")
    
    # run the main loop
    loop(args, screen, real_imgs, training_imgs, real_dict, training_dict, new_press)