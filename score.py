# Calculates score and provides outputs required for the output files in a csv format
import csv
import datetime

class Score:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def score_header(args, mode):
        output_header_written = False
        if mode == 1 and not(output_header_written):
            output_file_path = args.output_file_path
            header_list = ['Image_ID', 'Date/Time', 'Image Points','Total Points'] # header for output file
            with open(output_file_path, mode = "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header_list)
                file.close()
            output_header_written = True
            return output_header_written
        else:
            print("Mode must be 1 when this function is called")
            return

    @staticmethod
    # Functon to calculate based on answers entered by user
    def calculate_score(args, img_ID, val_received , mode, current_score, ans_dict):

        #the points for each object type
        #PEOPLE_POINTS, VEHICLES_POINTS, BAGS_POINTS, BARRELS_POINTS, ANTENNAS_POINTS
        POINTS = [2, 1, 1, 1, 1]
        BONUS_POINTS = 1
        
        current_dict = ans_dict
        output_file_path = args.output_file_path

        ans_key = current_dict['data'] # dictionary only has data key, read in the 2d array like [[0, 5, 0, 0, 5], [0, 0, 0, 0, 0], [2, 0, 2, 0, 1], [0, 0, 1, 1, 0], [2, 2, 2, 2, 0]]
        ans_key_list = ans_key[img_ID] # extract the array corresponding to the image_ID that has the answers for that image_ID
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
        if mode == 1:
            new_score = new_points + current_score
            current_time = datetime.datetime.now()
            with open(output_file_path, mode = "a", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([str(img_ID+1), str(current_time), str(new_points), str(new_score)]) # images are named starting from 001
                file.close()

        return new_points

class Mouse_Pos:
    def __init__(self, args):
        self.args = args
        self.mouse_pos_header()
    
    def mouse_pos_header(self):
        output_file_path = self.args.output_mouse_path
        header_list = ['Time', 'Mouse Position']
        with open(output_file_path, mode="a") as file:
            writer = csv.writer(file)
            writer.writerow(header_list)
            file.close()

    @staticmethod
    def write_mouse_pos(args, mouse_pos):
        current_time = datetime.datetime.now()
        output_file_path = args.output_mouse_path
        with open(output_file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(current_time), str(mouse_pos)])
            file.close()
        return