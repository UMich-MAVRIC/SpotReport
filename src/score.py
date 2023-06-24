# Calculates score and writes the score to the output csv file
import csv
import datetime
from pylsl_function import lsl_outlet_spt_task_scores, lsl_outlet_total_score, lsl_outlet_processing_time, lsl_outlet_mouse_pos, lsl_outlet_mouse_btn

class Score:
    def __init__(self):
        pass
    
    def score_files_header(args, file_extention):
        output_file_path = args.output_file_path + 'score_' + file_extention 
        header_list = ['Image_ID', 'Date/Time', 'Image Points','Total Points'] # header for output file
        with open(output_file_path, mode = "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header_list)
            file.close()
        return

    # Functon to calculate score based on counts entered by user and answer key
    def calculate_score(args, img_ID, val_received , mode, current_score, ans_dict, file_extention):
        #the points for each object type
        #PEOPLE_POINTS, VEHICLES_POINTS, BAGS_POINTS, BARRELS_POINTS, ANTENNAS_POINTS
        POINTS = [2, 1, 1, 1, 1]
        BONUS_POINTS = 1
        
        current_dict = ans_dict

        ans_key = current_dict['data'] # dictionary only has data key, read in the 2d array like [[0, 5, 0, 0, 5], [0, 0, 0, 0, 0], [2, 0, 2, 0, 1], [0, 0, 1, 1, 0], [2, 2, 2, 2, 0]]
        ans_key_list = ans_key[img_ID] # extract the array corresponding to the image_ID that has the answers for that image_ID
        new_points = 0
        new_score = 0
        all_correct = True  # variable used to assign bonus point if all objects counted correctly
        objects = 5 # the number of target object types

        # loop to go through the 5 different target object types and compare entered count to answer key
        for object in range(objects):    
            if ans_key_list[object] == val_received[object]:
                new_points += POINTS[object] * val_received[object]
            else:
                all_correct = False
        # bonus point if all counts were correct
        if all_correct:
            new_points += BONUS_POINTS

        # the number of categories counted correctly, counted incorrectly, and the accuracy
        if val_received == ans_key_list: # all answers correct
            correct_answer_counts = 5
            incorrect_answer_counts = 0
            accuracy = 1.0
        else:
            incorrect_answer_counts = 0 

            for object in range(objects): 
                if ans_key_list[object] != val_received[object]:
                    incorrect_answer_counts += 1
            correct_answer_counts = objects - incorrect_answer_counts
            accuracy = correct_answer_counts / objects
            accuracy = round(accuracy, 2)
        
        # append the new score to the csv file
        if mode == 1:
            new_score = new_points + current_score
            current_time = datetime.datetime.now()
            output_file_path = args.output_file_path + 'score_' + file_extention
            with open(output_file_path, mode = "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([str(img_ID+1), str(current_time), str(new_points), str(new_score)]) # images are named starting from 001
                file.close()

            output_file_path = args.output_file_path + 'accuracy_' + file_extention
            with open(output_file_path, mode = "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([str(img_ID+1), str(current_time), str(correct_answer_counts), str(incorrect_answer_counts), str(accuracy), str(val_received)]) # images are named starting from 001
                file.close()

            # send data to LSL
            lsl_outlet_spt_task_scores(val_received, ans_key_list) # send subject counts to LSL for calculating accuracy
            lsl_outlet_total_score(new_score)

        return new_points
    
    def task_time_header(args, file_extention):
        output_file_path = args.output_file_path + 'task_time_' + file_extention
        header_list = ['Image_ID', 'Date/Time', 'Task Time']
        with open(output_file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header_list)
            file.close()
        return

    def write_task_time(args, img_ID, task_time, file_extention):
        current_time = datetime.datetime.now()
        output_file_path = args.output_file_path + 'task_time_' + file_extention
        with open(output_file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(img_ID+1), str(current_time), str(task_time)])
            file.close()
        
        lsl_outlet_processing_time(img_ID, task_time) # send task time data to LSL
        
        return

