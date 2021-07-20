import cv2
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


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
    frame_num = 0
    while True:
        retval, frame = cap.read()
        if retval:
            avg = 0
            for i in range(rows):
                for j in range(cols):
                    avg += frame[i, j, 0]

            avg_intensities.append(avg/(rows*cols))
        else:
            print(f'\nYour heart is beating at {avg_bps*60} bpm.')
            input('Press Enter to continue')
            break
        frame_num += 1

        if frame_num % (fps*5) == 0 and frame_num != 0:
            window = avg_intensities
            window = window - sum(window)/len(window)

            sp = np.abs(np.fft.fft(window)[:frame_num//2])
            freq = ((np.fft.fftfreq(frame_num))*fps)[:frame_num//2]

            bps = 0
            max_amp = 0
            for i, z in enumerate(zip(freq, sp)):
                f, amp = z
                if f >= 1 and f <= 2 and amp > max_amp:
                    max_amp = amp
                    i_max = i

            bps = freq[i_max]
            print(f'\nBPM in this window[1-{frame_num}]: {bps*60}')
            try:
                avg_bps = (sp[i_max-1]*freq[i_max-1] + sp[i_max] *
                           freq[i_max] + sp[i_max+1]*freq[i_max+1])/(sp[i_max-1]+sp[i_max]+sp[i_max+1])
            except:
                avg_bps = bps
            print('Weighted Avg BPM:', avg_bps*60)

            plt.clf()
            plt.stem(freq, sp, use_line_collection=True)
            plt.xticks(freq, rotation=90)
            plt.ylabel('Magnitude')
            plt.xlabel('Frequency')
            plt.subplots_adjust(left=0.05, right=0.98, top=0.96, bottom=0.15)
            plt.draw()
            plt.pause(0.0001)

    cap.release()


cv2.destroyAllWindows()
