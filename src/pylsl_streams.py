# LSL inlet and outlet streams
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_byprop, cf_float32, cf_int32, IRREGULAR_RATE
import pygame
from pygame.locals import *


### LSL Inlet setting
# Configure LSL Inlet stream 
# If you want to use a custom inlet stream to manage the lockout function for the spot report, please ensure that you stream your inlet stream first
# Additionally, in the pylsl_outlet_example folder, you will find a sample code that you can use. If you do not want to use LSL, you can simply run spotreport.py.
try:
    spt_trigger_streams = resolve_byprop('name', "spt_task_trigger", 1, timeout=1) 
    if len(spt_trigger_streams) > 0:
        inlet_spt_trigger = StreamInlet(spt_trigger_streams[0])
        inlet_condition = True # data is present and should be read
    else:
        inlet_condition = False # no data is present
except:
    inlet_condition = False


### LSL Outlet setting
#mouse cursor position as x,y
info_spt_mouse_pos = StreamInfo("spt_mouse_pos", 'mouse_pose', 3, IRREGULAR_RATE, cf_int32, 'spotreport_gui')
outlet_spt_mouse_pos = StreamOutlet(info_spt_mouse_pos)
spt_mouse_pos_channels = info_spt_mouse_pos.desc().append_child("channels")
spt_mouse_pos_channels.append_child("channel")\
        .append_child_value("name", "imgID")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_mouse_pos_channels.append_child("channel")\
        .append_child_value("name", "posX")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_mouse_pos_channels.append_child("channel")\
        .append_child_value("name", "posY")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")

#mouse button being pressed or released
info_spt_mouse_btn = StreamInfo("spt_mouse_btn", 'mouse_button', 2, IRREGULAR_RATE, cf_int32, 'spotreport_gui')
outlet_spt_mouse_btn = StreamOutlet(info_spt_mouse_btn)
spt_mouse_btn_channels = info_spt_mouse_btn.desc().append_child("channels")
spt_mouse_btn_channels.append_child("channel")\
        .append_child_value("name", "imgID")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_mouse_btn_channels.append_child("channel")\
        .append_child_value("name", "button_state")\
        .append_child_value("unit", "pressed_released")\
        .append_child_value("type", "boolean")

#time spend on each image in seconds
info_spt_task_time = StreamInfo("spt_task_time", 'task_time', 2, IRREGULAR_RATE, cf_float32, 'spotreport_gui')
outlet_spt_task_time = StreamOutlet(info_spt_task_time)
spt_task_time_channels = info_spt_task_time.desc().append_child("channels")
spt_task_time_channels.append_child("channel")\
        .append_child_value("name", "imgID")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_task_time_channels.append_child("channel")\
        .append_child_value("name", "time")\
        .append_child_value("unit", "second")\
        .append_child_value("type", "time")

#the number of correct counts, incorrect counts, and accuracy % for each image
info_spt_accuracy = StreamInfo("spt_task_accuracy", 'task_accuracy', 9, IRREGULAR_RATE, cf_float32, 'spotreport_gui')
outlet_spt_accuracy = StreamOutlet(info_spt_accuracy)
spt_accuracy_channels = info_spt_accuracy.desc().append_child("channels")
spt_accuracy_channels.append_child("channel")\
        .append_child_value("name", "imgID")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_accuracy_channels.append_child("channel")\
        .append_child_value("name", "correct_counts")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_accuracy_channels.append_child("channel")\
        .append_child_value("name", "incorrect_counts")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_accuracy_channels.append_child("channel")\
        .append_child_value("name", "accuracy")\
        .append_child_value("unit", "percent")\
        .append_child_value("type", "float")
spt_accuracy_channels.append_child("channel")\
        .append_child_value("name", "subject_answer_1")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_accuracy_channels.append_child("channel")\
        .append_child_value("name", "subject_answer_2")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_accuracy_channels.append_child("channel")\
        .append_child_value("name", "subject_answer_3")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_accuracy_channels.append_child("channel")\
        .append_child_value("name", "subject_answer_4")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_accuracy_channels.append_child("channel")\
        .append_child_value("name", "subject_answer_5")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")

#the points gained from the image and the total score
info_spt_total_score = StreamInfo("spt_total_score", 'total_score', 3, IRREGULAR_RATE, cf_int32, 'spotreport_gui')
outlet_spt_total_score = StreamOutlet(info_spt_total_score)
spt_total_score_channels = info_spt_total_score.desc().append_child("channels")
spt_total_score_channels.append_child("channel")\
        .append_child_value("name", "imgID")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_total_score_channels.append_child("channel")\
        .append_child_value("name", "img_score")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_total_score_channels.append_child("channel")\
        .append_child_value("name", "total_score")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")


def lsl_outlet_mouse_pos(image_ID, mouse_pos): # publish current mouse positions; [x, y]
    #print("image_ID, mouse_pos = ", image_ID, mouse_pos[0], mouse_pos[1])
    outlet_spt_mouse_pos.push_sample([image_ID, mouse_pos[0], mouse_pos[1]])

def lsl_outlet_mouse_btn(image_ID, mouse_btn): # publish data when mouse button is pressed or released
    #print("image_ID, mouse_btn = ", image_ID, mouse_btn)
    # 0 means realeased, 1 means pressed
    outlet_spt_mouse_btn.push_sample([image_ID, mouse_btn])

def lsl_outlet_task_time(image_ID, task_time): # time between previous and current task (between previous and current time of clicking Next button)
    #print("image_ID, task_time = ", image_ID, task_time)
    outlet_spt_task_time.push_sample([image_ID, task_time])

def lsl_outlet_accuracy(image_ID, subject_answer, correct_answer): 

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
    
    #print("spt_accuracy== ", [image_ID, correct_answer_counts, incorrect_answer_counts, accuracy, subject_answer])
    outlet_spt_accuracy.push_sample([image_ID, correct_answer_counts, incorrect_answer_counts, accuracy, subject_answer[0], subject_answer[1], subject_answer[2], subject_answer[3], subject_answer[4]])

def lsl_outlet_total_score(image_ID, image_score, total_score): # publish data when score changes
    #print("image_ID, image_score, total_score = ", image_ID, image_score, total_score)
    outlet_spt_total_score.push_sample([image_ID, image_score, total_score])   


def read_lsl_inlet(): # process LSL inlet data
    while True and inlet_condition:
        # Read a sample from the inlet
        sample, _ = inlet_spt_trigger.pull_sample()
        #print(sample, sample[0], type(sample[0]))
        # Process the sample data
        # Replace the following lines with your own data processing code if you want functionality besides lockout
        if int(sample[0]) == 0: # Unlock
            key_event = pygame.event.Event(KEYDOWN, key=K_o) # convert event into event datatype of pygame
            pygame.event.post(key_event) # add event to the end of the events on the queue     
            print("Data sample received: 0 to unlock")

        elif int(sample[0]) == 1: # Lock
            key_event = pygame.event.Event(KEYDOWN, key=K_l) # convert event into event datatype of pygame
            pygame.event.post(key_event) # add event to the end of the events on the queue
            print("Data sample received: 1 to lock")
