import pygame
import glob
import pandas as pd
import csv                      
import datetime
from pylsl import StreamInfo, StreamOutlet, StreamInlet, local_clock, resolve_stream, resolve_byprop, cf_float32, cf_double64, cf_string, cf_int32, IRREGULAR_RATE
import numpy as np
import time

#File path names can be changed in lines 637 to 646
#if you change the size of the buttons, change the size in check_click() too

# LSL Outlet setting
#mouse cursor position as x,y
info_spt_mouse_pos = StreamInfo("spt_mouse_pos", 'mouse_pose', 2, IRREGULAR_RATE, cf_int32, 'spotreport_gui')
outlet_spt_mouse_pos = StreamOutlet(info_spt_mouse_pos)

#mouse button being pressed or released
info_spt_mouse_btn = StreamInfo("spt_mouse_btn", 'mouse_button', 1, IRREGULAR_RATE, cf_string, 'spotreport_gui')
outlet_spt_mouse_btn = StreamOutlet(info_spt_mouse_btn)

#time spend on each image in seconds
info_spt_processing_time = StreamInfo("spt_task_time", 'task_time', 2, IRREGULAR_RATE, cf_float32, 'spotreport_gui')
outlet_spt_processing_time = StreamOutlet(info_spt_processing_time)
spt_processing_channels = info_spt_processing_time.desc().append_child("channels")
spt_processing_channels.append_child("channel")\
        .append_child_value("name", "imgID")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_processing_channels.append_child("channel")\
        .append_child_value("name", "time")\
        .append_child_value("unit", "second")\
        .append_child_value("type", "time")

#the number of correct counts, incorrect counts, and accuracy % for each image
info_spt_task_scores = StreamInfo("spt_task_accuracy", 'task_accuracy', 8, IRREGULAR_RATE, cf_float32, 'spotreport_gui')
outlet_spt_task_scores = StreamOutlet(info_spt_task_scores)
spt_task_scores_channels = info_spt_task_scores.desc().append_child("channels")
spt_task_scores_channels.append_child("channel")\
        .append_child_value("name", "correct_counts")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_task_scores_channels.append_child("channel")\
        .append_child_value("name", "incorrect_counts")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_task_scores_channels.append_child("channel")\
        .append_child_value("name", "accuracy")\
        .append_child_value("unit", "percent")\
        .append_child_value("type", "float")
spt_task_scores_channels.append_child("channel")\
        .append_child_value("name", "subject_answer_1")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_task_scores_channels.append_child("channel")\
        .append_child_value("name", "subject_answer_2")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_task_scores_channels.append_child("channel")\
        .append_child_value("name", "subject_answer_3")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_task_scores_channels.append_child("channel")\
        .append_child_value("name", "subject_answer_4")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_task_scores_channels.append_child("channel")\
        .append_child_value("name", "subject_answer_5")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")

#the total score
info_spt_total_score = StreamInfo("spt_total_score", 'total_score', 1, IRREGULAR_RATE, cf_int32, 'spotreport_gui')
outlet_spt_total_score = StreamOutlet(info_spt_total_score)

def lsl_outlet_mouse_pos(mouse_pos): # publish current mouse positions; [x, y]
    #print("mouse_pos = ",mouse_pos[0], mouse_pos[1])
    outlet_spt_mouse_pos.push_sample([mouse_pos[0], mouse_pos[1]])

def lsl_outlet_mouse_btn(mouse_btn): # publish data when mouse button is pressed or released
    #print("mouse_btn = ", mouse_btn)
    outlet_spt_mouse_btn.push_sample([mouse_btn])

def lsl_outlet_processing_time(image_ID, task_time): # time between previous and current task (between previous and current time of clicking Next button)
    #print("image_ID, task_time = ", image_ID, task_time)
    outlet_spt_processing_time.push_sample([image_ID, task_time])

def lsl_outlet_spt_task_scores(subject_answer, correct_answer): 

    if subject_answer == correct_answer: # all answers correct
        correct_answer_counts = 5
        incorrect_answer_counts = 0
        accuracy = 1.0
    else:
        objects = 5 # the number of target object types
        incorrect_answer_counts = 0 

        for object in range(objects): 
            if correct_answer[object] != subject_answer[object]:
                incorrect_answer_counts += 1
        correct_answer_counts = objects - incorrect_answer_counts
        accuracy = correct_answer_counts / objects
        accuracy = round(accuracy, 2)
    
    #print("spt_answer_tasks== ", [subject_answer, correct_answer_counts, incorrect_answer_counts, accuracy])
    outlet_spt_task_scores.push_sample([correct_answer_counts, incorrect_answer_counts, accuracy, subject_answer[0], subject_answer[1], subject_answer[2], subject_answer[3], subject_answer[4]])

def lsl_outlet_total_score(total_score): # publish data when score changes
    #print("total_score = ", total_score)
    outlet_spt_total_score.push_sample([total_score])

class Button:
    def __init__(self, text, x_pos, y_pos):
        self.text = text #the text to display over the button
        self.x_pos = x_pos #the x pos of the upper left corner of the button
        self.y_pos = y_pos #the y pos of the upper left corner of the button
        self.draw() #function to draw the button and add text
    
    def draw(self):
        # For + and - buttons
        if self.text == '+' or self.text == '-':
            # Font type and Size
            font = pygame.font.SysFont('Arial MS', 80)
            button_text = font.render(self.text, True, 'black') #draw text on new surface with specified text color. True is for antialiasing, meaning characters have smooth edges.
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (75, 75)) #create rect object
            pygame.draw.rect(screen, 'sky blue', button_rect, 0, 5) #draw color filled rect to screen. 4th parameter is 0 to fill or 1 for outline in specified color. 5th parameter is rounding of corners.
            
            # Switch Condition for + or - label
            if self.text == '+':
                screen.blit(button_text, (self.x_pos + 22, self.y_pos + 8)) #copy text surface object to screen at this location
            elif self.text == '-':
                screen.blit(button_text, (self.x_pos + 29, self.y_pos + 12))
        
        # For Next button
        elif self.text == 'Next':
            # Font type and Size
            font = pygame.font.SysFont('Arial MS', 60)
            button_text = font.render(self.text, True, 'black')
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (155, 60))
            pygame.draw.rect(screen, 'gray', button_rect, 0, 5)
            pygame.draw.rect(screen, 'black', button_rect, 1, 5)
            screen.blit(button_text, (self.x_pos + 33, self.y_pos + 13))
        
        # For Training button
        elif self.text == 'Training':
            # Font type and Size
            font = pygame.font.SysFont('Arial MS', 80)
            button_text = font.render(self.text, True, 'black')
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (575, 100))
            pygame.draw.rect(screen, 'white', button_rect, 0, 5)
            pygame.draw.rect(screen, 'black', button_rect, 1, 5)
            screen.blit(button_text, (self.x_pos + 180, self.y_pos + 30))
        
        # For Start button
        elif self.text == 'Start':
            # Font type and size
            font = pygame.font.SysFont('Arial MS', 100)
            button_text = font.render(self.text, True, 'black')
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (575, 100))
            pygame.draw.rect(screen, 'green', button_rect, 0, 5)
            pygame.draw.rect(screen, 'black', button_rect, 2, 5)
            screen.blit(button_text, (self.x_pos + 220, self.y_pos + 20))
        

        # For object type rectangles to hold count values
        else:
            # Font type and Size
            font = pygame.font.SysFont('Arial MS', 60)
            button_text = font.render(self.text, True, 'black') #this is the count of the object type
            # Draw Rectangle - ((Position x, Position y), (Width, Height))
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (85, 45))
            pygame.draw.rect(screen, 'white', button_rect, 0, 5)
            pygame.draw.rect(screen, 'black', button_rect, 1, 5)
            screen.blit(button_text, (self.x_pos + 32, self.y_pos + 5))

    def check_click(self): #check if a button was clicked
        global new_press
        mouse_pos = pygame.mouse.get_pos() #get (x,y) mouse cursor position relative to top-left screen corner
        left_click = pygame.mouse.get_pressed()[0] #gets boolean of left mouse button being clicked

        if self.text == 'Training' or self.text == 'Start':
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (575, 100)) #rect object the same size as the training or start buttons
        elif self.text == '+' or self.text == '-':
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (75, 75)) #rect object the same size as the - or + buttons
        else: #Next button
            button_rect = pygame.rect.Rect((self.x_pos, self.y_pos), (155, 60)) #rect object the same size as the next button
        
        if left_click and button_rect.collidepoint(mouse_pos) and new_press:
            #the mouse was clicked over a button and it is a new button press
            new_press = False #reset to True in loop when mouse button is released
            return True
        else:
            return False
    

def labels(score):
    #creates all text labels for target objects and score

    # Font size and type for target object labels
    font = pygame.font.SysFont('Arial MS', 40)
    # Label for Object Names
    people_label = font.render('People', True, 'black')
    screen.blit(people_label, (996, 80))
    vehicles_label = font.render('Vehicles', True, 'black')
    screen.blit(vehicles_label, (983, 200))
    bags_label = font.render('Bags', True, 'black')
    screen.blit(bags_label, (1007, 320))
    barrels_label = font.render('Barrels', True, 'black')
    screen.blit(barrels_label, (992, 440))
    antennas_label = font.render('Antennas', True, 'black')
    screen.blit(antennas_label, (971, 560))
    
    # Label for 'Score'
    font = pygame.font.SysFont('Arial MS', 100)
    score_label = font.render('Score: ', True, 'dark green')
    screen.blit(score_label, (40, 40))

    #text for Score value
    score_text = font.render(str(score), True, 'dark green')
    screen.blit(score_text, (260, 40))

    return
    

def menu_setup(subID_text_input, conditionNo_text_input, subID_rect, conditionNo_rect):
    #creates the labels and buttons for the menu
     
    # Draw rectangle and empty text for sub_ID
    pygame.draw.rect(screen, 'white', subID_rect, 0, 5) #draw white filled rect to screen. 4th parameter is 0 to fill or 1 for outline in specified color. 5th parameter is rounding of corners.
    pygame.draw.rect(screen, 'black', subID_rect, 1, 5) #draw black border around rect.
    subID_text = font.render(subID_text_input, True, 'black') #draw text on new surface with specified text color. True is for antialiasing, meaning characters have smooth edges.
    screen.blit(subID_text, (subID_rect.x + 20, subID_rect.y + 10)) #copy text surface object to screen at this location

    # Draw rectangle and empty text for Condition No.
    pygame.draw.rect(screen, 'white', conditionNo_rect, 0, 5)
    pygame.draw.rect(screen, 'black', conditionNo_rect, 1, 5)
    conditionNo_text = font.render(conditionNo_text_input, True, 'black')
    screen.blit(conditionNo_text, (conditionNo_rect.x + 20, conditionNo_rect.y + 10))

    # Label for user input boxes
    subID_label = font.render('Subject ID', True, 'black')
    screen.blit(subID_label, (28, 88))
    conditionNo_label = font.render('Condition No', True, 'black')
    screen.blit(conditionNo_label, (390, 88))

    # Training Button
    training_button = Button('Training', 28, 200)
    
    #Start Button
    start_button = Button('Start', 28, 400)

    #Examples of target objects image
    screen.blit(ex_img, (680, 160))

    return training_button, start_button


def calculate_score(img_ID, people_val, vehicle_val, bags_val, barrels_val, antennas_val, mode, current_score):
    #calculate score based on entered counts and answer key

    global real_dict #already read in upon startup
    global training_dict #already read in upon startup
    global output_file_name
    global output_file_path
    global output_header_written

    #the points for each object type
    #PEOPLE_POINTS, VEHICLES_POINTS, BAGS_POINTS, BARRELS_POINTS, ANTENNAS_POINTS
    POINTS = [2, 1, 1, 1, 1]
    BONUS_POINTS = 1

    if mode == 1:
        current_dict = real_dict
    else: #mode == 0
        current_dict = training_dict

    ans_key = current_dict['data'] #dictionary only has data key, read in the 2d array like [[0, 5, 0, 0, 5], [0, 0, 0, 0, 0], [2, 0, 2, 0, 1], [0, 0, 1, 1, 0], [2, 2, 2, 2, 0]]
    ans_key_list = ans_key[img_ID] #extract the array corresponding to the image_ID that has the answers for that image_ID
    val_received = [people_val, vehicle_val, bags_val, barrels_val, antennas_val] #the counts of target objects entered
    new_points = 0
    new_score = 0
    all_correct = True #variable used to assign bonus point if all objects counted correctly
    objects = 5 #the number of target object types

    # loop to go through the 5 different target object types and compare entered count to answer key
    for object in range(objects):    
        if ans_key_list[object] == val_received[object]:
            new_points += POINTS[object] * val_received[object]
        else:
            all_correct = False
    #bonus point if all counts were correct
    if all_correct:
        new_points += BONUS_POINTS
    
    #append the new score to the csv file
    if mode == 1 and output_header_written:
        new_score = new_points + current_score
        current_time = datetime.datetime.now()
        with open(output_file_path, mode = "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(img_ID+1), str(current_time), str(new_score)]) #images are named starting from 001
            file.close()
    
    elif mode == 1 and not(output_header_written):
        #write header first
        header_list = ['Image_ID', 'Date/Time', 'Points'] #header for output file
        with open(output_file_path, mode = "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header_list)
            file.close()
        output_header_written = True
        
        #append new score to the csv file
        new_score = new_points + current_score
        current_time = datetime.datetime.now()
        with open(output_file_path, mode = "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(img_ID+1), str(current_time), str(new_score)]) #images are named starting from 001
            file.close()

    if mode == 1:
        #print("val_received", val_received, type(val_received), len(val_received))
        #print("ans_key_list", ans_key_list, type(ans_key_list), len(ans_key_list))

        #send data to LSL
        lsl_outlet_spt_task_scores(val_received, ans_key_list) # send answers to LSL for calculating accuracy
        lsl_outlet_total_score(new_score)

    return new_points

# Training Loop
def training_loop():
    global training_imgs
    global new_press
    global mode

    img_ID_training = 0 #index of the training image
    people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0 #user counts
    score = 0

    training_running = True
    mode = 0 #set mode to 0 to calculate score from correct dictionary

    while training_running:
            
        screen.fill('white')
        timer.tick(fps)
    
        # Buttons for '+' (text, x_pos, y_pos)
        add_button1 = Button('+', 1160, 90)
        add_button2 = Button('+', 1160, 210)
        add_button3 = Button('+', 1160, 330)
        add_button4 = Button('+', 1160, 450)
        add_button5 = Button('+', 1160, 570)
        
        #+ buttons only increase counts up to 5
        if add_button1.check_click():
            if people_val == 5:
                continue
            else:
                people_val += 1
        elif add_button2.check_click():
            if vehicle_val == 5:
                continue
            else:
                vehicle_val += 1
        elif add_button3.check_click():
            if bags_val == 5:
                continue
            else:
                bags_val += 1
        elif add_button4.check_click():
            if barrels_val == 5:
                continue
            else:
                barrels_val += 1
        elif add_button5.check_click():
            if antennas_val == 5:
                continue
            else:
                antennas_val += 1     
        
        
        # Buttons for '-' (text, x_pos, y_pos)
        sub_button1 = Button('-', 850, 90)
        sub_button2 = Button('-', 850, 210)
        sub_button3 = Button('-', 850, 330)
        sub_button4 = Button('-', 850, 450)
        sub_button5 = Button('-', 850, 570)

        #- buttons only decrease counts down to 0
        if sub_button1.check_click():
            if people_val == 0:
                continue
            else:
                people_val -= 1
        elif sub_button2.check_click():
            if vehicle_val == 0:
                continue
            else:
                vehicle_val -= 1
        elif sub_button3.check_click():
            if bags_val == 0:
                continue
            else:
                bags_val -= 1
        elif sub_button4.check_click():
            if barrels_val == 0:
                continue
            else:
                barrels_val -= 1
        elif sub_button5.check_click():
            if antennas_val == 0:
                continue
            else:
                antennas_val -= 1
        
        # Rectangles for count of each object type. These will not be clicked on so no need to store Button class object
        Button(str(people_val), 1000, 110)
        Button(str(vehicle_val), 1000, 230)
        Button(str(bags_val), 1000, 350)
        Button(str(barrels_val), 1000, 470)
        Button(str(antennas_val), 1000, 590)

        # Button for Next
        next_button = Button('Next', 1080, 690)
        
        #labels for target object types, 'score' and score value
        labels(score)

        screen.blit(training_imgs[img_ID_training], (40, 130)) #display the current training image

        #when Next button is clicked, update the score and show next image
        if next_button.check_click():
            new_points = calculate_score(img_ID_training, people_val, vehicle_val, bags_val, barrels_val, antennas_val, mode, score)
            score += new_points
            people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0 #reset counts for next image
            
            img_ID_training += 1 #incrememnt the img_ID
            #if last training image, exit the training loop
            if img_ID_training >= len(training_imgs):
                training_running = False
                return
            else:
                screen.blit(training_imgs[img_ID_training], (40, 130)) #display the next image


        #check if we want to exit training and if mouse button was released
        for event in pygame.event.get():
            #closing the window or pressing escape will exit training and take you back to the menu. can then hit escape again to quit.
            if event.type == pygame.QUIT:
                training_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    training_running = False
            if event.type == pygame.MOUSEBUTTONUP: #when a pressed mouse button is released
                new_press = True #the next mouse button press is a new press
        
        pygame.display.flip() #update the full display screen

    return

#loop for menu and real images loop
def loop():
    global real_imgs
    global new_press
    global mode
    global start_task_time
    global UE_score_file_name
    global UE_score_file_path
    global UE_lockout_file_name
    global UE_lockout_file_path
    global output_file_name
    global output_file_path
    global output_header_written

    menu_running = True
    SR_real_running = False

    file_paths_set = False #whether the UE and output file paths have been set

    #strings to hold subID and conditionNo inputs
    subID_text_input = ''
    conditionNo_text_input = ''
    
    #rect objects to surround the user inputs
    #these are part of this loop to detect collisions for typing in the subID and conditionNo inputs
    subID_rect = pygame.rect.Rect((140, 80), (140, 35)) #create rect object to surround subID_text_input
    conditionNo_rect = pygame.rect.Rect((520, 80), (140, 35)) #create rect object to surround conditionNo_text_input
    
    #boolean of whether the user inputs are active for typing
    active_subID_box = False
    active_condNo_box = False

    lockout_rows = 0 #number of lockout rows read already
    lockout = 0 #boolean of whether the spot report is locked or not
    num_lockout_rows = 0 #number of rows in the lockout file

    #loop for the menu screen
    while menu_running:
        pygame.font.init() #initialize the font module
        screen.fill('gray94') #set background color
        timer.tick(fps)

        training_button, start_button = menu_setup(subID_text_input, conditionNo_text_input, subID_rect, conditionNo_rect)

        #enter the training_loop() if the training button is clicked
        if training_button.check_click():
            #before starting, make sure the textboxes were filled out
           if subID_text_input == '' or conditionNo_text_input == '':
               print("Please fill in the Subject Id and Condition No")
           else:
               training_loop()
               if not(file_paths_set):
                    #set the output and UE score and lockout file names here
                    output_file_name = 'S'+ subID_text_input + '_C' + conditionNo_text_input + '.csv'
                    output_file_path += output_file_name
                    UE_score_file_name = 'S'+ subID_text_input + '_C' + conditionNo_text_input + '_'
                    UE_lockout_file_name = 'S'+ subID_text_input + '_C' + conditionNo_text_input + '_'
                    if conditionNo_text_input == '1' or conditionNo_text_input == '4':
                        UE_score_file_name += 'CL14.csv'
                        UE_lockout_file_name += 'CL14.csv'
                    elif conditionNo_text_input == '2' or conditionNo_text_input == '5':
                        UE_score_file_name += 'CL25.csv'
                        UE_lockout_file_name += 'CL25.csv'
                    else: #conditionNo_text_input == '3' or conditionNo_text_input == '6':
                        UE_score_file_name += 'CL36.csv'
                        UE_lockout_file_name += 'CL36.csv'
                    UE_score_file_path += UE_score_file_name
                    UE_lockout_file_path += UE_lockout_file_name

                    file_paths_set = True

               mode = 1 #set the mode to 1 so the real loop can run now. can still do training again if desired.

        if start_button.check_click() and mode == 1:
           menu_running = False
           SR_real_running = True #the only way to set this to True is by clicking Start or automatically from UE
           start_task_time = time.time() #start the timer for the first image

        elif start_button.check_click() and mode == 0: #this code never seems to run, not sure why
           print("Please complete Training before progressing")

        if mode == 1:
            #read from UE lockout file to start spot report automatically
            try:
                lockouts = pd.read_csv(UE_lockout_file_path) #try to read the file
            except:
                pass
                #print("ERROR: READING UE LOCKOUT BEFORE START") #something went wrong in reading the csv, but it will fix itself on the next loop
            else: #executed if no errors in reading csv
                num_lockout_rows = len(lockouts) #check how many rows are in the file
                if num_lockout_rows > lockout_rows: #if there is a new row in the UE file, lock or unlock the spot report
                    lockout_reason = lockouts['Lockout Reason'][lockout_rows] #read in the lockout reason
                    lockout_rows += 1
                
                    if lockout_reason == "UGVs_Start": #start spot report automatically with UE
                        menu_running = False
                        SR_real_running = True #the only way to set this to True is by clicking Start or automatically from UE
                        start_task_time = time.time() #start the timer for the first image
        
        for event  in pygame.event.get():
            #stop running the menu loop if you close the window or press escape
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_running = False
            if event.type == pygame.MOUSEBUTTONDOWN: #any mouse button is pressed
                if subID_rect.collidepoint(event.pos): #boolean of whether the event.pos (x,y) point is inside the rect object
                    active_subID_box = True #clicking on the subID_rect will make the text active for typing
                else:
                    active_subID_box = False #clicking anywhere else will make the text inactive for typing
                if conditionNo_rect.collidepoint(event.pos):
                    active_condNo_box = True
                else:
                    active_condNo_box = False
            
            if event.type == pygame.KEYDOWN and active_subID_box: #if a key is pressed and the subID textbox is active
                if event.key == pygame.K_BACKSPACE: #if backspace is pressed, remove the last character
                    subID_text_input = subID_text_input[:-1]
                else:
                    subID_text_input += event.unicode #add the pressed character

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
    people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0
    score = 0
    UE_rows = 0 #number of UE score rows read already
    lockout = 0 #boolean of whether the spot report is locked or not

    subtract_lockout = False #whether the spot report was locked and that time needs to be subtracted from the task time
    coming_from_lockout = False #whether the spot report is now unlocked coming from a locked state


    while SR_real_running:
        pygame.font.init()

        try:
            lockouts = pd.read_csv(UE_lockout_file_path) #try to read the file
        except:
            print("ERROR: READING UE LOCKOUT") #something went wrong in reading the csv, but it will fix itself on the next loop
        else: #executed if no errors in reading csv
            num_lockout_rows = len(lockouts) #check how many rows are in the file
            if num_lockout_rows > lockout_rows: #if there is a new row in the UE file, lock or unlock the spot report
                lockout = lockouts['Lockout'][lockout_rows] #read in the lockout value from the next line
                lockout_rows += 1

        
        if not(lockout):
            if coming_from_lockout: #this is the first time the spot report is now unlocked coming from a locked state
                lockout_end_time = time.time() #the end time of the lockout
                coming_from_lockout = False
                subtract_lockout = True #true means we need to subtract the lockout time from the time spent on the image
                #print("lock end == ", lockout_end_time)
        
            screen.fill('white')
            timer.tick(fps)
        
            # Buttons for '+' (text, x_pos, y_pos)
            add_button1 = Button('+', 1160, 90)
            add_button2 = Button('+', 1160, 210)
            add_button3 = Button('+', 1160, 330)
            add_button4 = Button('+', 1160, 450)
            add_button5 = Button('+', 1160, 570)
            
            #+ buttons only increase counts up to 5
            if add_button1.check_click():
                if people_val == 5:
                    continue
                else:
                    people_val += 1
            elif add_button2.check_click():
                if vehicle_val == 5:
                    continue
                else:
                    vehicle_val += 1
            elif add_button3.check_click():
                if bags_val == 5:
                    continue
                else:
                    bags_val += 1
            elif add_button4.check_click():
                if barrels_val == 5:
                    continue
                else:
                    barrels_val += 1
            elif add_button5.check_click():
                if antennas_val == 5:
                    continue
                else:
                    antennas_val += 1     
            
            
            # Buttons for '-' (text, x_pos, y_pos)
            sub_button1 = Button('-', 850, 90)
            sub_button2 = Button('-', 850, 210)
            sub_button3 = Button('-', 850, 330)
            sub_button4 = Button('-', 850, 450)
            sub_button5 = Button('-', 850, 570)

            #- buttons only decrease counts down to 0
            if sub_button1.check_click():
                if people_val == 0:
                    continue
                else:
                    people_val -= 1
            elif sub_button2.check_click():
                if vehicle_val == 0:
                    continue
                else:
                    vehicle_val -= 1
            elif sub_button3.check_click():
                if bags_val == 0:
                    continue
                else:
                    bags_val -= 1
            elif sub_button4.check_click():
                if barrels_val == 0:
                    continue
                else:
                    barrels_val -= 1
            elif sub_button5.check_click():
                if antennas_val == 0:
                    continue
                else:
                    antennas_val -= 1


            # Rectangles for count of each object type. These will not be clicked on so no need to store Button class object
            Button(str(people_val), 1000, 110)
            Button(str(vehicle_val), 1000, 230)
            Button(str(bags_val), 1000, 350)
            Button(str(barrels_val), 1000, 470)
            Button(str(antennas_val), 1000, 590)

            # Button for Next
            next_button = Button('Next', 1080, 690)
            
            #labels for target object types, 'score' and score value
            labels(score)

            screen.blit(real_imgs[img_ID], (40, 130)) #display the current real image

            #when Next button is clicked, update the score and show next image
            if next_button.check_click():
                end_task_time = time.time() #the end time for the current image
                new_points = calculate_score(img_ID, people_val, vehicle_val, bags_val, barrels_val, antennas_val, mode, score)
                score += new_points
                people_val, vehicle_val, bags_val, barrels_val, antennas_val = 0, 0, 0, 0, 0 #reset counts for next image
                
                img_ID += 1 #incrememnt the img_ID
                #if last real image, reset img_ID back to 0 to loop through images again
                if img_ID >= len(real_imgs):
                    img_ID = 0
                    screen.blit(real_imgs[img_ID], (40, 130))
                else:
                    screen.blit(real_imgs[img_ID], (40, 130)) #display the next image

                if subtract_lockout:
                    task_time = (end_task_time - start_task_time) - (lockout_end_time - lockout_start_time)
                    subtract_lockout = False
                else:
                    task_time = end_task_time - start_task_time # calculate task time

                lsl_outlet_processing_time(img_ID, task_time) #send task time data to LSL
                #print("ID, time == ", img_ID, task_time)
                start_task_time = end_task_time #set the end time as the starting time for the next image

            #update score from UE
            try:
                UE_scores = pd.read_csv(UE_score_file_path)
            except:
                print("ERROR: READING UE SCORE")
            else:
                num_rows = len(UE_scores) #check how many rows are in the file
                while num_rows > UE_rows: #if there is a new row in the UE file, update the score on the spot report
                    next_score_update = UE_scores['Score'][UE_rows] #read in the UE score from the next line
                    score += next_score_update #update points. Will display update as it runs through this loop
                    UE_rows += 1
                    if next_score_update != 0: #if the UE score update is non-zero, log it right away
                        if not(output_header_written): #write header first
                            header_list = ['Image_ID', 'Date/Time', 'Points'] #header for output file
                            with open(output_file_path, mode = "a", newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(header_list)
                                file.close()
                            output_header_written = True

                        current_time = datetime.datetime.now()
                        with open(output_file_path, mode = "a", newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([str(img_ID), str(current_time), str(score)]) #images are named starting from 001, but the interpretation is 'the score after the image with ID given by img_ID'
                            file.close()
                        
                        lsl_outlet_total_score(score) #send the updated score to LSL

        else: #spot report is locked
            screen.fill('black')
            font = pygame.font.SysFont('Arial MS', 150)
            locked_text = font.render('LOCKED', True, 'white')
            screen.blit(locked_text, (450, 300))

            if coming_from_lockout == False:
                lockout_start_time = time.time() #the time when the lockout started
                coming_from_lockout = True #when the spot report becomes unlocked, we will be coming from a lockout state
                #print("lock start == ", lockout_start_time)

        # Event Loop
        for event in pygame.event.get(): #monitor user inputs
            if event.type == pygame.QUIT: #if X is clicked to close the window or escape is pressed, stop running the loop
                SR_real_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    SR_real_running = False
                if event.key == pygame.K_l: #as a backup in case of lockout issues, if the 'L' key is pressed
                    lockout = not(lockout) #flip the lockout boolean value
            if event.type == pygame.MOUSEBUTTONUP: #when the pressed mouse button is released
                new_press = True #the next mouse button press is a new press
                lsl_outlet_mouse_btn("Released") #send data to LSL
            if event.type == pygame.MOUSEBUTTONDOWN: #when the mouse button is pressed
                lsl_outlet_mouse_btn("Pressed") #send data to LSL
            if event.type == pygame.MOUSEMOTION: #when the mouse cursor moves
                lsl_outlet_mouse_pos(event.pos) #send data to LSL       

        pygame.display.flip() #update the full display screen
    
    pygame.quit() #if we reached here, it is because we want to quit pygame
    return #after quitting pygame, return to main function

# Main Function
if __name__ == "__main__":
    pygame.init() #initialize all imported modules, including font

    WIDTH = 1368 #screen width
    HEIGHT = 790 #screen height
    screen = pygame.display.set_mode([WIDTH, HEIGHT]) #display surface

    fps = 60
    timer = pygame.time.Clock() #clock object for keeping track of time

    font = pygame.font.Font('freesansbold.ttf', 18) #set the font type and size
    pygame.display.set_caption("Spot Report") #name of the window caption

    new_press = True #if the next mouse click is a new press
    mode = 0  #control boolean indicating 0 for training images mode or 1 for real images mode
    start_task_time = 0 #timer for the time spent on each image
    output_file_name = '' #will take the form of 'S#_C#.csv' based on what is typed in the textboxes
    output_file_path = "Log_SpotReportScore/"
    output_header_written = False #whether the header has already been written in the output file or not

    UE_score_file_name = '' #will take the form of 'S#_C#.csv' based on what is typed in the textboxes
    UE_score_file_path = "//rob-tilbury01/c$/Users/MAVRIC-LAB-UE-DEV-1/Documents/Unreal Projects/Arsha-Ali-Workspace/Log_Score/" #change to the local file path on the UE sim PC
    UE_lockout_file_name = ''
    UE_lockout_file_path = "//rob-tilbury01/c$/Users/MAVRIC-LAB-UE-DEV-1/Documents/Unreal Projects/Arsha-Ali-Workspace/Log_Lockouts/" #change to the local file path on the UE sim PC
    answer_keys_path = "answer_keys/*.csv"
    training_imgs_path = "training_images/*.png"
    real_imgs_path = "real_images/*.png"

    menu_examples_file = "examples.png" #examples of each target object
    ex_img = pygame.image.load(menu_examples_file)
    ex_img = pygame.transform.scale(ex_img, (650, 400))

    #read in the answer keys
    answer_files = sorted(glob.glob(answer_keys_path)) #put the training and real answer key file names into a list sorted alphabetically
    dict_i = 0 #to assign the answer keys to dictionaries
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

    
    #read in the training images
    training_images = sorted(glob.glob(training_imgs_path)) #put the training images file names into a list sorted alphabetically
    training_imgs =[]
    for filename in training_images:    
        img = pygame.image.load(filename) #returns a surface object that has the image drawn onto it. This is separate from the display surface object so later we have to blit it (copy contents of one surface onto another)
        training_imgs.append(pygame.transform.scale(img, (750, 500))) #scale the image size and append the surface object to the training_imgs[] list
    
    #read in the real images
    real_images = sorted(glob.glob(real_imgs_path)) #put the real images file names into a list sorted alphabetically
    real_imgs = []
    for filename in real_images:
        img = pygame.image.load(filename) #returns a surface object that has the image drawn onto it. This is separate from the display surface object so later we have to blit it (copy contents of one surface onto another)
        real_imgs.append(pygame.transform.scale(img, (750, 500))) #scale the image size and append the surface object to the real_imgs[] list


    #run the main loop
    loop()
