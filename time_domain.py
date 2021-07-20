import cv2
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


current_path = os.path.abspath(os.path.dirname(__file__))
pp_folder = Path(current_path+'/10fps_300x300/').rglob('*.mp4')
video_files = [os.path.abspath(x) for x in sorted(pp_folder)]

max_bpm = 120
rows, cols = 300, 300
fps = 10

plt.ion()
plt.figure(figsize=(20, 4))

for file in video_files:
    print(file)
    cap = cv2.VideoCapture(file)

    avg_intensities = []
    bpms = []
    frame_num = 0
    print('Each window is a 5sec interval, \nsliding by 5 sec each time.')
    while True:

        retval, frame = cap.read()
        if retval:
            avg = 0
            for i in range(rows):
                for j in range(cols):
                    avg += frame[i, j, 0]

            avg_intensities.append(avg/(rows*cols))
        else:
            print(f'\nYour heart is beating at {sum(bpms)/len(bpms)} bpm.')
            input('Press Enter to continue')
            plt.clf()
            break

        if frame_num % (fps*5) == 0 and frame_num != 0:
            window_start = frame_num-fps*5 - 1 if frame_num > fps*5 else frame_num-fps*5
            fr = [x/fps for x in range(window_start, frame_num+1)]
            window = avg_intensities[window_start:]

            peaks, _ = find_peaks(
                np.array(window), distance=fps*60/max_bpm)
            peaks = [window_start+peak for peak in peaks]
            for peak in peaks:
                plt.scatter(peak/fps, avg_intensities[peak], color='black')

            bpm = len(peaks)*12
            bpms.append(bpm)
            print(f'\nBPM in this window[{window_start}-{frame_num}]: {bpm}')
            print('Average BPM:', sum(bpms)/len(bpms))

            plt.plot(fr, window)
            plt.xlabel('Time')
            plt.ylabel('Intensity')
            plt.subplots_adjust(left=0.05, right=0.98, top=0.96, bottom=0.15)
            plt.draw()
            plt.pause(0.0001)

        frame_num += 1

    cap.release()


cv2.destroyAllWindows()
