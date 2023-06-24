# Main File to run the Spot Report
# need to add running command
# python3 sportreport.py 1368 790 'training_images\*.png' 'task_images\*.png' 'answer_keys\*.csv' 'output_files\score.csv' 'output_files\mouse_position.csv' 'freesansbold.ttf' 18 1160 90 850 120 1000 110 750 500 40 130
# If you don't have 'spt_trigger' outlet, you need to run this python (src\pylsl_oulet_exampl\spt_trigger_outlet.py) for testing this code.
# the 'spt_trigger' will control the pygame to start and pasue the task.
import pygame
import time
import threading
import asyncio
from utils import menu_setup
from read import ex_menu_image, load_images, load_ans_files, input_args
from utils import Button
from display_setup import Disp_Setup
from score import Score
from mouse import Mouse
from pylsl_function import read_lsl_inlet

# Training Loop
def training_loop(training_imgs, training_dict, new_press):
    
    img_ID_training = 0 # index of the training image
    score = 0
    people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0 # user counts
    obj_vals = [people_val, vehicle_val, bags_val, barrels_val, antennas_val]

    training_running = True
    mode = 0 # set mode to 0 to calculate score from correct dictionary

    while training_running:
        
        screen.fill('white')
        timer.tick(fps)
        file_extention = '' # file extention not needed since nothing is saved during training

        # Sets up all the add buttons
        add_button_list = Disp_Setup.add_buttons(args, screen)

        # Buttons only increase counts up to 5
        for i in range(len(add_button_list)):
            if add_button_list[i].check_click(new_press, args):
                new_press = False # reset to True in loop when mouse button is released
                if obj_vals[i] == 5:
                    continue
                else:
                    obj_vals[i] += 1

        # Sets up all the subtract buttons
        sub_button_list = Disp_Setup.subtract_buttons(args, screen)

        # Buttons only decrease counts down to 0
        for i in range(len(sub_button_list)):
            if sub_button_list[i].check_click(new_press, args):
                new_press = False # reset to True in loop when mouse button is released
                if obj_vals[i] == 0:
                    continue
                else:
                    obj_vals[i] -= 1

        # puts user counts of objects on the screen
        Disp_Setup.count_object_labels(args, screen, obj_vals)

        # Button for Next
        next_button = Button(screen, 'Next', args.next_xpos, args.next_ypos) 
                
        # labels for target object types, 'score' and score value
        Disp_Setup.labels(args, screen, score)

        screen.blit(training_imgs[img_ID_training], (args.img_xpos, args.img_ypos)) # Display the current training image

        # When Next button is clicked, update the score and show next image
        if next_button.check_click(new_press, args):
            new_press = False # reset to True in loop when mouse button is released
            new_points = Score.calculate_score(args, img_ID_training, obj_vals, mode, score, training_dict, file_extention)
            score += new_points
            people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0 # reset counts for next image
            obj_vals = [people_val, vehicle_val, bags_val, barrels_val, antennas_val]

            img_ID_training += 1 # increment the training img_ID
            #if last training image, exit the training loop
            if img_ID_training >= len(training_imgs):
                training_running = False
                return
            else:
                screen.blit(training_imgs[img_ID_training], (args.img_xpos, args.img_ypos)) # display the next image
            

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

    return

#loop for menu and task images loop
def loop(args, screen, task_imgs, training_imgs, task_dict, training_dict, new_press):

    menu_running = True
    SR_task_running = False

    # strings to hold subID and condition inputs
    subID_text_input = ''
    condition_text_input = ''
    
    # rect objects to surround the user inputs
    # these are part of this loop to detect collisions for typing in the subID and condition inputs
    subID_rect = pygame.rect.Rect((140, 80), (140, 35)) # create rect object to surround subID_text_input
    condition_rect = pygame.rect.Rect((463, 80), (140, 35)) # create rect object to surround condition_text_input
       
    # boolean of whether the user inputs are active for typing
    active_subID_box = False
    active_condNo_box = False

    mode = 0 #control boolean indicating 0 for training images mode or 1 for task images mode
    start_task_time = 0 #timer for the time spent on each image

    # loop for the menu screen
    while menu_running:
        pygame.font.init() #initialize the font module
        screen.fill('gray94') #set background color
        timer.tick(fps)

        training_button, start_button = menu_setup(args, screen, ex_img, subID_text_input, condition_text_input, subID_rect, condition_rect)

        # enter the training_loop() if the training button is clicked
        if training_button.check_click(new_press, args):
            new_press = False # reset to True in loop when mouse button is released
            # before starting, make sure the textboxes were filled out
            if subID_text_input == '' or condition_text_input == '':
               print("Please fill in the Subject Id and Condition")
            else:
               training_loop(training_imgs, training_dict, new_press)
               mode = 1 # set the mode to 1 so the task loop can run now. can still do training again if desired.

        if start_button.check_click(new_press, args) and mode == 1:
           new_press = False # reset to True in loop when mouse button is released
           menu_running = False
           SR_task_running = True # the only way to set this to True is by clicking Start
           start_task_time = time.time() # start the timer for the first image

        elif start_button.check_click(new_press, args) and mode == 0: # this code never seems to run, not sure why
           print("Please complete Training before progressing")
           new_press = False # reset to True in loop when mouse button is released

        for event in pygame.event.get():
            # stop running the menu loop if you close the window or press escape
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN: # any mouse button is pressed
                if subID_rect.collidepoint(event.pos): # boolean of whether the event.pos (x,y) point is inside the rect object
                    active_subID_box = True # clicking on the subID_rect will make the text active for typing
                else:
                    active_subID_box = False # clicking anywhere else will make the text inactive for typing
                if condition_rect.collidepoint(event.pos):
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
                    condition_text_input = condition_text_input[:-1]
                else:
                    condition_text_input += event.unicode

            elif event.type == pygame.MOUSEBUTTONUP: # when the pressed mouse button is released
                new_press = True # the next mouse button press is a new press
                
        pygame.display.flip() # update the full display screen

    # task images loop
    img_ID = 0 # index of the task image
    people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0 # user counts of objects
    obj_vals = [people_val, vehicle_val, bags_val, barrels_val, antennas_val]
    score = 0
    lockout = 0 # boolean of whether the spot report is locked or not

    subtract_lockout = False # whether the spot report was locked and that time needs to be subtracted from the task time
    coming_from_lockout = False # whether the spot report is now unlocked coming from a locked state

    #set the extention for the output files based on the subID and condNo
    file_extention = 'S'+ subID_text_input + '_C' + condition_text_input + '.csv'
    
    # write the headers for the output files
    Score.score_files_header(args, file_extention) # for both score and accuracy files
    Score.task_time_header(args, file_extention)
    Mouse.mouse_pos_header(args, file_extention)
    Mouse.mouse_button_header(args, file_extention)

    while SR_task_running:
        if not(lockout):
            if coming_from_lockout: #this is the first time the spot report is now unlocked coming from a locked state
                lockout_end_time = time.time() #the end time of the lockout
                coming_from_lockout = False
                subtract_lockout = True #true means we need to subtract the lockout time from the time spent on the image
        
            screen.fill('white')
            timer.tick(fps)

            # Sets up all the add buttons
            add_button_list = Disp_Setup.add_buttons(args, screen)

            # Buttons only increase counts up to 5
            for i in range(len(add_button_list)):
                if add_button_list[i].check_click(new_press, args):
                    new_press = False # reset to True in loop when mouse button is released
                    if obj_vals[i] == 5:
                        continue
                    else:
                        obj_vals[i] += 1

            # Sets up all the subtract buttons
            sub_button_list = Disp_Setup.subtract_buttons(args, screen)

            # Buttons only decrease counts down to 0
            for i in range(len(sub_button_list)):
                if sub_button_list[i].check_click(new_press, args):
                    new_press = False # reset to True in loop when mouse button is released
                    if obj_vals[i] == 0:
                        continue
                    else:
                        obj_vals[i] -= 1

            # puts user counts of objects on the screen
            Disp_Setup.count_object_labels(args, screen, obj_vals)

            # Button for Next
            next_button = Button(screen, 'Next', args.next_xpos, args.next_ypos) 
            
            # labels for target object types, 'score' and score value
            Disp_Setup.labels(args, screen, score)

            screen.blit(task_imgs[img_ID], (args.img_xpos, args.img_ypos)) # Display the current task image

            # When Next button is clicked, update the score and show next image
            if next_button.check_click(new_press, args):
                end_task_time = time.time() #the end time for the current image
                new_press = False # reset to True in loop when mouse button is released
                new_points = Score.calculate_score(args, img_ID, obj_vals, mode, score, task_dict, file_extention)
                score += new_points
                people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0 # reset counts for next image
                obj_vals = [people_val, vehicle_val, bags_val, barrels_val, antennas_val]

                img_ID += 1 # increment the img_ID
                # if last task image, reset img_ID back to 0 to loop through images again
                if img_ID >= len(task_imgs):
                    img_ID = 0
                    screen.blit(task_imgs[img_ID], (args.img_xpos, args.img_ypos))
                else:
                    screen.blit(task_imgs[img_ID], (args.img_xpos, args.img_ypos)) # display the next image
                
                if subtract_lockout:
                    task_time = (end_task_time - start_task_time) - (lockout_end_time - lockout_start_time)
                    subtract_lockout = False
                else:
                    task_time = end_task_time - start_task_time # calculate task time
                
                Score.write_task_time(args, img_ID-1, task_time, file_extention) # write to csv and send data to LSL
                start_task_time = end_task_time # set the end time as the starting time for the next image

        else: # spot report is locked
            screen.fill('black')
            font = pygame.font.SysFont('Arial MS', 150)
            locked_text = font.render('LOCKED', True, 'white')
            screen.blit(locked_text, (450, 300))

            if coming_from_lockout == False:
                lockout_start_time = time.time() # the time when the lockout started
                coming_from_lockout = True # when the spot report becomes unlocked, we will be coming from a lockout state

        # Event Loop
        for event in pygame.event.get(): # monitor user inputs
            if event.type == pygame.QUIT: # if X is clicked to close the window or escape is pressed, stop running the loop
                SR_task_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    SR_task_running = False
                if event.key == pygame.K_l: # if the 'L' key is pressed
                    lockout = True # flip the lockout boolean value
                if event.key == pygame.K_o: # if the 'L' key is pressed
                    lockout = False # flip the lockout boolean value    
            if event.type == pygame.MOUSEBUTTONUP: # when the pressed mouse button is released
                new_press = True # the next mouse button press is a new press
                Mouse.write_mouse_button(args, img_ID, "Released", file_extention) # write to csv and send data to LSL
            if event.type == pygame.MOUSEBUTTONDOWN: #when the mouse button is pressed
                Mouse.write_mouse_button(args, img_ID, "Pressed", file_extention) # write to csv and send data to LSL
            if event.type == pygame.MOUSEMOTION: #when the mouse cursor moves 
                Mouse.write_mouse_pos(args, img_ID, event.pos, file_extention) # write to csv and send data to LSL

        pygame.display.flip() # update the full display screen
    
    pygame.quit() # if we reached here, it is because we want to quit pygame
    return # after quitting pygame, return to main function

async def start_asyncio_loop(): #??? dont know what this does
    # Create a separate thread for reading LSL data
    lsl_thread = threading.Thread(target=read_lsl_inlet)
    lsl_thread.start()

    loop(args, screen, task_imgs, training_imgs, task_dict, training_dict, new_press)

    # Stop the LSL thread
    stop_thread = True #??? never used
    lsl_thread.join()


# Main Function
if __name__ == "__main__":

    pygame.init() #initialize all imported modules, including font
    args = input_args() #optional arguments from user for design/device specifics (e.g., screen size)

    screen = pygame.display.set_mode([args.width, args.height]) #display surface with screen width and height
    fps = 60
    timer = pygame.time.Clock() #clock object for keeping track of time

    font = pygame.font.Font(args.font_type, args.font_size) #set the font type and size
    pygame.display.set_caption("Spot Report") #name of the window caption

    new_press = True # if the next mouse click is a new press

    # read in the answer keys
    training_dict, task_dict = load_ans_files(args)

    # read in the training images
    training_imgs = load_images(args, key="train")

    # read in the task images
    task_imgs = load_images(args, key="task")

    #read in the example objects for the menu
    ex_img = ex_menu_image(args)
    
    asyncio.run(start_asyncio_loop()) #start LSL and main loop #???what is async
