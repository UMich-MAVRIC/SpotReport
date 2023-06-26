# Spot Report Secondary Task

![Alt text](paper/figures/spotreport_git.png)


## Abstract
This repository is for the spot report task. The spot report task is a Pygame-based implementation of a secondary task for use in human-robot interaction (HRI) experiments. The spot report task requires users to count target objects shown in static images. A key element of the spot report task implementation is the ability to integrate it with a primary task, such as one developed in Unreal Engine, using Lab Streaming Layer (LSL).

- Paper link: [Online version](https://doi.org/...) or [download PDF](https://doi.org/...)

- Demo Video: [Watch on YouTube](https://youtu.be/mhUKsqkuMPQ) or [download mp4 video](paper/video/SpotReportVideo.mp4)


## Motivation
The development of the program was motivated by the fact that to the best of our knowledge, there were no suitable secondary tasks available for HRI studies in the military domain. In addition, it is challenging to integrate a standalone secondary task with game development engines such as Unreal Engine or Unity. By leveraging the expertise of military experts and LSL, the Spot Report addresses both of these gaps. Additionally, as the program developed here is standalone, it can quite easily be adapted for other domains by either changing the images and labels used for the Spot Report task or by adapting the game behavior for the particular domain.


## What this Repo contains?

The repo hosts the code for (a) The Spot Report program, (b) The task and training images used for our domain (military) application (c) LSL functionality to stream data to primary application.


## Software
### Dependencies
All implementations were tested with Python 3.9.7. The following packages are needed. Please install with `pip install -r requirements.txt`.
* pygame 
* pandas 
* pylsl

The following Python built-in modules are needed. They should already be available with the Python distribution.
* glob
* csv
* datetime
* time
* argparse
* random
* threading
* asyncio
* os


On all non-Windows platforms and for some Windows/Python combinations, a shared liblsl is required. This can be done by either using:
* For most Linux and Windows distributions: `conda install -c conda-forge liblsl`

* For MAC devices: `brew install labstreaminglayer/tap/lsl`
  

## Spot Report Task Implementation
The spot report task follows these steps in `src/spotreport.py` by referencing the other `src/*.py` files:

1. The program reads in the training and task images and answer keys.
2. The menu is displayed.
3. The user clicks and types in the textboxes for the subject ID and condition.
4. After the subject ID and condition textboxes have been filled in, the user can click the Training button. In training, the spot report task is setup and the user completes 5 training images and returns to the menu. Training must be completed at least once before the user can start the experimental task.
5. After training and returning to the menu, the user can click the Start button. In the experimental task, the spot report task is setup and the user can cycle through 165 task images. If the 165th task image is reached, the task images will repeat from the beginning.
6. During the experimental task, the spot report task can be locked by pressing the 'L' key or sending a '1' through the inlet stream and unlocked by pressing the 'O' key or sending a '0' through the inlet stream. When the spot report task is locked, a black screen is displayed to prevent the user from seeing and interacting with the spot report task.
7. The user can press the Esc key or close the spot report task window to close the program. Pressing the Esc key or closing the window during training will return the program to the menu.


## Use Instructions
1. Run `git clone https://github.com/UMich-MAVRIC/SpotReport.git` to clone this repository.
2. Ensure you have [Python](https://www.python.org/downloads/) installed and an IDE such as [Visual Studio code](https://code.visualstudio.com/) to run this codebase.
3. To control lockout functionality or send other data to the spot report program through an LSL intlet stream, run `python trigger.py` from the `src/lsl_outlet` folder. This step is optional.
4. In a separate terminal, run `python spotreport.py` from the `src` folder.
5. Fill out the subject ID and condition textboxes on the menu.
6. Click the Training button to start training.
7. Click the Start button to start the experimental task.
8. Press the 'L' key to lock and the 'O' key to unlock the spot report task as desired. If step 3 was completed, from that terminal, send a '1' to lock and a '0' to unlock the spot report task as desired. 
9. Close the spot report task by pressing the Esc key or closing the window.
10. Explore the output files in the `src/output_files` folder as desired. 


## Output Files and LSL Outlet Streams

There are 5 output files generated in csv format in the `src/output_files` folder, where <subject ID> is replaced by the text entered into the subject ID textbox and <condition> is replaced by the text enetered into the condition textbox. The output files are appended to when the mouse information changes or when the user advances to the next task image.

### Mouse Information
* `mouse_pos_S<subject ID>_C<condition>.csv`: the x and y mouse cursor position.
* `mouse_button_S<subject ID>_C<Condition>.csv`: the state of the mouse button as either pressed or released.


### Task Performance
* `accuracy_S<subject ID>_C<condition>.csv`: the target objects counted correctly and incorrectly, accuracy, and user counts for each target object category.
* `score_S<subject ID>_C<condition>.csv`: the score on each task image and the total score.
* `task_time_S<subject ID>_C<condition>.csv`: the time spent on each task image.

The same information is also sent on LSL outlet streams defined in `lsl_streams.py`.
| LSL info.     | Stream Name         | Stream Type     | Channel Count | Sampling Rate   | Format      | Details |
| ------------- | ------------------- | --------------- | ------------- | --------------- | ----------- | ----------- |
| Outlet 1      | spt_mouse_pos       | mouse_pose      | 3             | Irregular       | int32       | Ch 1: Image ID <br> Ch 2: X position <br> Ch 3: Y position          |
| Outlet 2      | spt_mouse_btn       | mouse_button    | 2             | Irregular       | int32       | Ch 1: Image ID <br> Ch 2: 0 (for released) or 1 (for pressed)       |
| Outlet 3      | spt_task_time       | task_time       | 2             | Irregular       | float32     | Ch 1: Image ID <br> Ch 2: Execution time (sec)                      |
| Outlet 4      | spt_task_accuracy   | task_accuracy   | 9             | Irregular       | float32     | Ch 1: Image ID <br> Ch 2: Correct counts <br> Ch 3: Incorrect counts <br> Ch 4: Accuracy (%) <br> Ch 5: count of people <br> Ch 6: count of vehicles <br> Ch 7: count of bags <br> Ch 8: count of barrels <br> Ch 9: count of antennas                                                         |
| Outlet 5      | spt_total_score     | total_score     | 3             | Irregular       | int32       | Ch 1: Image ID <br> Ch 2: Image score <br> Ch 3: Total score        |


## Paper Source Files and Figures

The `paper` folder contains the LaTeX source files for the paper. Paper figures are in `paper/figures` in .jpg or .pdf format. The file structure and flowchart diagrams are also provided in .drawio format.


## Miscellaneous

In this section, we have explained various optional features of our program that can help users of this program in the future.

1. ### Terminal Arguments

We have defined a range of arguments using argparse in `read.py` to enable easier adaptation of our program for different screen sizes and for users who want to use a different set of images to run with our program. Please note that the label positions still need to be adjusted directly within the `display.py`. In general our program uses the default parameters that we have used for our application.

To test any arguments on the terminal window, please use the following structure - 

* Type in `python3 spotreport.py` and add a space, in the terminal.
* Refer to the `read.py` to get the argument name(s) to be changed.
* Enter them in terminal after the space, in the format `--{arg_name} {arg_value}`. Note, `arg_name` refers to the name of the argument defined in the `read.py` file such as `width`, and `arg_value` refers to the value the user chooses to enter.
* The user has the option to change multiple arguments by just adding them in the same format as above and separating them using a space.
* To make a permanent modification to the default args value, please make the change in the `read.py` file by changing the default value associated with the argument.

2. ### Randomize Images

There is standalone `.py` file `randomize_images.py` that can be used to randomize the order of images and update the answer keys in the `answer_keys` folder. This file is not directly part of our program is just a supplementary code to provide users with additional resources.

### LSL inlet information
**1. Program trigger**
  * Name: _spt_task_trigger_
  * Type: _start_pause_task_
  * Channels: _1_;
  * Sampleing rate: _IRREGULAR_RATE_
  * Channel format: _cf_int32_
     * 0: Pauses the spot report program. 
     * 1: Starts or resumes the spot report program.  



## Citation
Please use the following citation:
```
@article{TBD,
    title={Spot Report: Real-time Pygame Based Secondary Task For Use In Human-Robot Interaction User Experiments},
    author={Arsha Ali and Rohit Banerjee and Wonse Jo and TBD and Lionel P. Robert Jr. and Dawn M. Tibury},
    journal={TBD},
    volume={},
    number={},
    pages={},
    year={2023},
    publisher={},
    doi={}
}
```

