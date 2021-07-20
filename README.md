# SmartphoneCam-Heartbeat-Detection

This is a project done as a part of the course Smart Sensing for IoT.
It performs a time-domain and frequency domain analysis on data taken from a smartphone camera
to figure out the pulse rate of a person. This is called PPG or Photoplethysmography.

The detailed report can be found [here](./Heartbeat_PPG__ED18B027_Report.pdf) which essentially covers 4 aspects:
* Survey of existing PPG Apps
* Generating Test Datasets.
  * Lighting (Bright, Normal, Dark)
  * Post Processing (Down Sampling, Quantization, Smoothening)
* Sensing Algorithm.
  * Time Domain Analysis (Peak finding)
  <img src='https://user-images.githubusercontent.com/64144419/126331330-c2578760-36ea-415e-aab1-b3e4c535dfdd.png' width=800>
  
  * Frequency Domain Analysis (FFT)
  <img src='https://user-images.githubusercontent.com/64144419/126331520-2d677f3a-d09a-4847-80d4-7db5dec1a6f0.png' width=800>

* Evaluating Performance of the Algorithm
  * Effect of FPS
  * Effect of Resolution
  * FPS vs Resolution
  
## Dependencies:
* Numpy
* OpenCV
* Scipy
* Matplotlib

## Instructions

Details on the dataset can be found in the Report.

### post_processing.py
The code applies for batch video files in a folder which is in the same directory as the script is located. To use the
code for single video files, the for loop can be commented and used.
Besure to change the fps, size and output folder and file name in VideoWriter accordingly.
Note that when fps is changed the if statement in the while True loop has to be edited.

### time_domain.py & freq_domain.py
The same applies to both these files as well.
Be sure to change the fps, rows, cols and path to folder or file accordingly.
