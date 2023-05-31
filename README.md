# Spot Report Secondary Task

Dataset and software for the paper "..." (Ali, A., Banerjee, R., Jo, W., Robert, L.P. & Tilbury, D.M. 2023). DOI: https://doi.org/...

## Abstract
This repositoy is to disseminate a new spot report task as a secondary task. It can be integrated with the primary task developed, for example, in Unreal Engine, using Lab Streaming Layer (LSL). The spot report task requires counting target objects in static images. LSL facilitates real-time communication between the primary task and the spot report task. The spot report task is developed in Python, utilizing the Pygame library with other libraries and packages.

## Software

### Dependencies

All implementations were tested with Python 3.9.7.
The following packages are needed (please install with `python3 -m pip install --user <package name>`):

* `pygame`
* `glob`
* `pandas`
* `csv`
* `datetime`
* `pylsl`

### Spot Report Implementation

The spot report code follows these steps in `spotreport.py`:

* x
* x
* x:
  * x
  * x
  * x
  * x
  * x

### Use Instructions

1. 

2. 

3. 

### LSL inlet information
**1. Program trigger**
  * Name: _spt_task_trigger_
  * Type: _start_pause_task_
  * Channels: _1_;
  * Sampleing rate: _IRREGULAR_RATE_
  * Channel format: _cf_int32_

### LSL outlet information
**1. Mouse information**
* Cursor positions
  * Name: _spt_mouse_pos_
  * Type: _mouse_pose_
  * Channels: _2_;
  * Sampleing rate: _IRREGULAR_RATE_
  * Channel format: _cf_int32_
  
* Button clicks
  * Name: _spt_mouse_btn_
  * Type: _mouse_button_
  * Channels: _1
  * Sampleing rate: _IRREGULAR_RATE_
  * Channel format: _cf_string_

**2. Seconday task information**
* Task time
  * Name: _spt_task_time_
  * Type: _task_time_
  * Channels: _2_
  * Sampleing rate: _IRREGULAR_RATE_
  * Channel format: _cf_float32_
  
* Task accuracy
  * Name: _spt_task_accuracy_
  * Type: _task_accuracy_
  * Channels: _3_
  * Sampleing rate: _IRREGULAR_RATE_
  * Channel format: _cf_float32_


### Output Files
* score log
* accuracy log


## Paper Source Files and Figures

The `paper` directory also contains the LaTeX source files for the paper.
Paper figures are in .svg format in `paper/SVG figures` and in .pdf format in `paper/PDF figures`.


## Misc

### explain various folders
### explain randomize images
