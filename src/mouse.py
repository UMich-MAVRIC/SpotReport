# class for writing mouse positions and button presses to csv files and LSL
import csv
import datetime
from pylsl_streams import lsl_outlet_mouse_pos, lsl_outlet_mouse_btn

class Mouse:
    def __init__(self):
        pass
    
    def mouse_pos_header(args, file_extention):
        output_file_path = args.output_file_path + 'mouse_pos_' + file_extention
        header_list = ['Date/Time', 'Image_ID', 'Mouse Position']
        with open(output_file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header_list)
            file.close()
        return

    def write_mouse_pos(args, img_ID, mouse_pos, file_extention):
        current_time = datetime.datetime.now()
        output_file_path = args.output_file_path + 'mouse_pos_' + file_extention
        with open(output_file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(current_time), str(img_ID+1), str(mouse_pos)])
            file.close()
        
        lsl_outlet_mouse_pos(img_ID+1, mouse_pos) # send data to LSL
        
        return
    
    def mouse_button_header(args, file_extention):
        output_file_path = args.output_file_path + 'mouse_button_' + file_extention
        header_list = ['Date/Time', 'Image_ID', 'Mouse Button']
        with open(output_file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header_list)
            file.close()
        return

    def write_mouse_button(args, img_ID, mouse_button, file_extention):
        current_time = datetime.datetime.now()
        output_file_path = args.output_file_path + 'mouse_button_' + file_extention
        with open(output_file_path, mode="a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(current_time), str(img_ID+1), str(mouse_button)])
            file.close()

        # LSL will use 0 and 1 instead of strings
        if mouse_button == "Pressed":
            mouse_btn = 1
        elif mouse_button == "Released":
            mouse_btn = 0
        
        lsl_outlet_mouse_btn(img_ID+1, mouse_btn) # send data to LSL

        return