from pylsl import StreamInfo, StreamOutlet, resolve_byprop, resolve_stream

# Create an LSL outlet stream
stream_name = "spt_task_trigger"  # Replace with your desired stream name
stream_type = "start_pause_task"  # Replace with the stream type you want to use
channel_count = 1  # Number of channels in the stream
sample_rate = 0  # Irrelevant for marker streams, set to 0
# Create the stream info
info = StreamInfo(stream_name, stream_type, channel_count, sample_rate, source_id = 'spotreport_gui')
# Create the outlet
outlet = StreamOutlet(info)

# Main loop
while True:
    # Wait for user input from the terminal
    key = input("Press '0' or '1': ")

    # Check if the '0' key was pressed
    if key == '0': ## Disable lockout = continue the task
        # Send a data sample with value 0
        data = 0
        outlet.push_sample([data])
        print("Data sample sent: 0 to disable lockout")

    # Check if the '1' key was pressed
    elif key == '1': ## Enable lockout = stop the task
        # Send a data sample with value 1
        data = 1
        outlet.push_sample([data])
        print("Data sample sent: 1 to enable lockout")
    
    elif key.lower() == 'q':
        # Exit the program if 'q' key is pressed
        break
    
    else:
        print("Please use '0' or '1' to control the Spotreport.")

print("Exiting the program.")
