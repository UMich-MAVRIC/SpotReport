# Read mouse information and task and also writes the information to the output csv file
import csv
import datetime
from pylsl_function import lsl_outlet_spt_task_scores, lsl_outlet_total_score, lsl_outlet_processing_time, lsl_outlet_mouse_pos, lsl_outlet_mouse_btn

# class for writing mouse positions and button presses to csv files and LSL
class Mouse:
    def __init__(self):
        pass
    
    def mouse_pos_header(args, file_extention):
        output_file_path = args.output_file_path + 'mouse_pos_' + file_extention
        header_list = ['Date/Time', 'Mouse Position']
        with open(output_file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header_list)
            file.close()
        return

    def write_mouse_pos(args, mouse_pos, file_extention):
        current_time = datetime.datetime.now()
        output_file_path = args.output_file_path + 'mouse_pos_' + file_extention
        with open(output_file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(current_time), str(mouse_pos)])
            file.close()
        
        lsl_outlet_mouse_pos(mouse_pos) # send data to LSL
        
        return
    
    def mouse_button_header(args, file_extention):
        output_file_path = args.output_file_path + 'mouse_button_' + file_extention
        header_list = ['Date/Time', 'Mouse Button']
        with open(output_file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header_list)
            file.close()
        return

    def write_mouse_button(args, mouse_button, file_extention):
        current_time = datetime.datetime.now()
        output_file_path = args.output_file_path + 'mouse_button_' + file_extention
        with open(output_file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(current_time), str(mouse_button)])
            file.close()
        
        lsl_outlet_mouse_btn(mouse_button) # send data to LSL

        return