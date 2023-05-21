from pylsl import StreamInfo, StreamOutlet, StreamInlet, local_clock, resolve_stream, resolve_byprop, cf_float32, cf_double64, cf_string, cf_int32, IRREGULAR_RATE
import numpy as np

# LSL Outlet setting
# (1) Mouse curos position
info_spt_mouse_pos = StreamInfo("spt_mouse_pos", 'mouse_pose', 2, IRREGULAR_RATE, cf_int32, 'spotreport_gui')
outlet_spt_mouse_pos = StreamOutlet(info_spt_mouse_pos)

info_spt_mouse_btn = StreamInfo("spt_mouse_btn", 'mouse_button', 1, IRREGULAR_RATE, cf_string, 'spotreport_gui')
outlet_spt_mouse_btn = StreamOutlet(info_spt_mouse_btn)

info_spt_processing_time = StreamInfo("spt_task_time", 'task_time', 2, IRREGULAR_RATE, cf_float32, 'spotreport_gui') #unit: seconds
outlet_spt_processing_time = StreamOutlet(info_spt_processing_time)
spt_processing_channels = info_spt_processing_time.desc().append_child("channels")
spt_processing_channels.append_child("channel")\
        .append_child_value("name", "task")\
        .append_child_value("unit", "number")\
        .append_child_value("type", "int")
spt_processing_channels.append_child("channel")\
        .append_child_value("name", "time")\
        .append_child_value("unit", "second")\
        .append_child_value("type", "time")

info_spt_task_scores = StreamInfo("spt_task_accuracy", 'task_accuracy', 3, IRREGULAR_RATE, cf_float32, 'spotreport_gui') #unit: seconds
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

def lsl_outlet_mouse_pos(mouse_pos): # publish current mouse positions; [x, y]
    #print(mouse_pos,mouse_pos[0], mouse_pos[1],  type(mouse_pos)) # For testing outputs
    outlet_spt_mouse_pos.push_sample([mouse_pos[0], mouse_pos[1]])

def lsl_outlet_mouse_btn(mouse_push_btn): # publish data when mouse button is pressed; True or 1
    #print(mouse_pos,mouse_pos[0], mouse_pos[1],  type(mouse_pos)) # For testing outputs
    outlet_spt_mouse_btn.push_sample([mouse_push_btn])

def lsl_outlet_processing_time(task_number, task_time): # mission time between previous and current task (between previous and current time of clicking 'next')
    #print(mouse_pos,mouse_pos[0], mouse_pos[1],  type(mouse_pos)) # For testing outputs
    outlet_spt_processing_time.push_sample([task_number, task_time])

def lsl_outlet_spt_task_scores(subject_answer, correct_answer): 
    
    total_answer_counts = sum(correct_answer)

    if subject_answer == correct_answer: # No answers
        correct_answer_counts = sum(correct_answer)
        incorrect_answer_counts = 0
    else:
        objects = 5 # the number of target object types
        incorrect_count_temp = 0   

        for object in range(objects): 
            if correct_answer[object] != subject_answer[object]:
                incorrect_count_temp += abs(correct_answer[object] - subject_answer[object])

        correct_answer_counts = total_answer_counts - incorrect_count_temp
        incorrect_answer_counts = total_answer_counts - correct_answer_counts

    #incorrect_answer = total_answer - corret_answer
    if total_answer_counts == 0:
        accuracy = 1.0
    else:        
        accuracy = correct_answer_counts / total_answer_counts
        if accuracy < 0:
            accuracy = 0.0
    
    #print("outlet_spt_processing_time== ", [correct_answer_counts, incorrect_answer_counts, accuracy]) #for testing
    outlet_spt_task_scores.push_sample([correct_answer_counts, incorrect_answer_counts, accuracy])

    
