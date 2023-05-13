import csv
import datetime

# Functon to calculate based on answers entered by user
def calculate_score(args, img_ID, people_val, vehicle_val, bags_val, barrels_val, antennas_val, mode, current_score, ans_dict):

    #the points for each object type
    #PEOPLE_POINTS, VEHICLES_POINTS, BAGS_POINTS, BARRELS_POINTS, ANTENNAS_POINTS
    POINTS = [2, 1, 1, 1, 1]
    BONUS_POINTS = 1

    current_dict = ans_dict
    output_file_path = args.output_file_path
    output_header_written = args.output_header_written

    ans_key = current_dict['data'] # dictionary only has data key, read in the 2d array like [[0, 5, 0, 0, 5], [0, 0, 0, 0, 0], [2, 0, 2, 0, 1], [0, 0, 1, 1, 0], [2, 2, 2, 2, 0]]
    ans_key_list = ans_key[img_ID] # extract the array corresponding to the image_ID that has the answers for that image_ID
    val_received = [people_val, vehicle_val, bags_val, barrels_val, antennas_val] # the counts of target objects entered
    new_points = 0
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
    
    # append the new score to the csv file
    if mode == 1 and output_header_written:
        new_score = new_points + current_score
        current_time = datetime.datetime.now()
        with open(output_file_path, mode = "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(img_ID+1), str(current_time), str(new_score)]) # images are named starting from 001
            file.close()
    
    elif mode == 1 and not(output_header_written):
        # write header first
        header_list = ['Image_ID', 'Date/Time', 'Points'] # header for output file
        with open(output_file_path, mode = "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header_list)
            file.close()
        output_header_written = True
        
        # append new score to the csv file
        new_score = new_points + current_score
        current_time = datetime.datetime.now()
        with open(output_file_path, mode = "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(img_ID+1), str(current_time), str(new_score)]) # images are named starting from 001
            file.close()

    return new_points