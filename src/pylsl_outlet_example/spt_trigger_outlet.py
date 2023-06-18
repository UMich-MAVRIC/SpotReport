from pylsl import StreamInfo, StreamOutlet

# Create an LSL outlet stream
stream_name = "spt_task_trigger"  # Replace with your desired stream name
stream_type = "start_pause_task"  # Replace with the stream type you want to use
channel_count = 1  # Number of channels in the stream
sample_rate = 0  # Irrelevant for marker streams, set to 0

# Create the stream info
info = StreamInfo(stream_name, stream_type, channel_count, sample_rate, source_id = 'spot_report')
# Create the outlet
outlet = StreamOutlet(info)

# Main loop
while True:
    # Wait for user input from the terminal
    key = input("Press '0', '1', or '2' to send a data sample: ")

    # Check if the '0' key was pressed
    if key == '0':
        # Send a data sample with value 0
        marker = 0
        outlet.push_sample([marker])
        print("Data sample sent: 0")
    # Check if the '0' key was pressed
    elif key == '1':
        # Send a data sample with value 1
        marker = 1
        outlet.push_sample([marker])
        print("Data sample sent: 1")
    elif key == '2':
        # Send a data sample with value 2
        marker = 2
        outlet.push_sample([marker])
        print("Data sample sent: 2")
            
            

    elif key.lower() == 'q':
        # Exit the program if 'q' key is pressed
        break

print("Exiting the program.")
