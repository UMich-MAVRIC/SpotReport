from pylsl import StreamInfo, StreamOutlet, StreamInlet, local_clock, resolve_stream, resolve_streams, resolve_byprop, cf_float32, cf_double64, cf_string, cf_int32, IRREGULAR_RATE
import numpy as np
import sys
import pygame
import asyncio
from pygame.locals import *


### LSL Inlet setting
# Configure LSL Inlet stream 
# If you want to use a custom inlet stream to manage the lockout function for the spotreport, please ensure that you stream your inlet stream first
# Additionally, in the pylsl_outlet_example folder, you will find a simple inlet code that you can use. If you do not want to use LSL (Lab Streaming Layer), you can simply run spotreport.py."
try:
    spt_trigger_streams = resolve_byprop('name', "spt_task_trigger", 1, timeout=1) 
    if len(spt_trigger_streams) > 0:
        inlet_spt_trigger = StreamInlet(spt_trigger_streams[0])
        inlet_condition = True
    else:
        inlet_condition = False
except:
    inlet_condition = False


### LSL Outlet setting
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


def read_lsl_inlet(): #??? what is this
    while True and inlet_condition:
        # Read a sample from the inlet
        sample, _ = inlet_spt_trigger.pull_sample()
        # Process the sample data
        # Replace the following line with your own data processing code
        if int(sample[0]) == 0: # Enable Lockout
            key_event = pygame.event.Event(KEYDOWN, key=K_o)
            pygame.event.post(key_event)      
            print("Data sample sent: 0 to disable lockout")

        elif int(sample[0]) == 1: #Disable Lockout
            key_event = pygame.event.Event(KEYDOWN, key=K_l)
            pygame.event.post(key_event)
            print("Data sample sent: 1 to enable lockout")
