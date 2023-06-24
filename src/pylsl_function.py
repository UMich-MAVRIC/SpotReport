from pylsl import StreamInfo, StreamOutlet, StreamInlet, local_clock, resolve_stream, resolve_byprop, cf_float32, cf_double64, cf_string, cf_int32, IRREGULAR_RATE
import numpy as np
import sys

stop_thread = False #??? what is 5-16
# Configure LSL Inlet stream 
stream_name = "spt_task_trigger"  # Replace with the name of your LSL stream
try:
    spt_trigger_streams = resolve_stream('name', stream_name)
    if len(spt_trigger_streams) > 0:
        inlet_spt_trigger = StreamInlet(spt_trigger_streams[0])
    else:
        print("No stream found with the name:", stream_name)
except:
    print(f"Failed to find the {stream_name}. Please restart this program after starting the stream.")
    sys.exit(1)


# LSL Outlet setting
#mouse cursor position as x,y
info_spt_mouse_pos = StreamInfo("spt_mouse_pos", 'mouse_pose', 3, IRREGULAR_RATE, cf_int32, 'spotreport_gui')
outlet_spt_mouse_pos = StreamOutlet(info_spt_mouse_pos)

#mouse button being pressed or released
info_spt_mouse_btn = StreamInfo("spt_mouse_btn", 'mouse_button', 2, IRREGULAR_RATE, cf_int32, 'spotreport_gui')
outlet_spt_mouse_btn = StreamOutlet(info_spt_mouse_btn)

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

def lsl_outlet_mouse_pos(image_ID, mouse_pos): # publish current mouse positions; [x, y]
    #print("mouse_pos = ",mouse_pos[0], mouse_pos[1])
    outlet_spt_mouse_pos.push_sample([image_ID, mouse_pos[0], mouse_pos[1]])

def lsl_outlet_mouse_btn(image_ID, mouse_btn): # publish data when mouse button is pressed or released
    #print("mouse_btn = ", mouse_btn)
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
    
    #print("spt_answer_tasks== ", [subject_answer, correct_answer_counts, incorrect_answer_counts, accuracy])
    outlet_spt_accuracy.push_sample([image_ID, correct_answer_counts, incorrect_answer_counts, accuracy, subject_answer[0], subject_answer[1], subject_answer[2], subject_answer[3], subject_answer[4]])

def lsl_outlet_total_score(image_ID, image_score, total_score): # publish data when score changes
    #print("image_ID, image_score, total_score = ", image_ID, image_score, total_score)
    outlet_spt_total_score.push_sample([image_ID, image_score, total_score])   


def read_lsl_inlet(): #??? what is this
    while not stop_thread:
        # Read a sample from the inlet
        sample, _ = inlet_spt_trigger.pull_sample()
        # Process the sample data
        # Replace the following line with your own data processing code
        print(f"Received data: {sample}") 

        # need to change py while llop
