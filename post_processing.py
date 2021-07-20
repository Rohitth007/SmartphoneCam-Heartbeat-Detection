import cv2
import os
from pathlib import Path
import numpy as np
import re

current_path = os.path.abspath(os.path.dirname(__file__))
raw_folder = Path(current_path+'/raw_video/normal').rglob('*.mp4')
video_files = [os.path.abspath(x) for x in raw_folder]


for file in video_files:
    pattern = re.compile(r'[^/]*\.mp4')
    name = pattern.search(file)
    print(f'Processing file: {name.group()}')

    cap = cv2.VideoCapture(file)

    fps = 10
    size = (300, 300)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(
        current_path+f'/folder_name/{name.group()}', fourcc, fps, size, 0)

    # grayscale
    # ROI vs resize

    skip = 1
    while True:
        retval, frame = cap.read()
        if skip == 3:
            if retval:
                # frame = frame[:540, :960]  # quater roi
                b = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                b = cv2.resize(b, size, interpolation=cv2.INTER_AREA)
                b = cv2.dilate(b, None, iterations=10)
                b = cv2.GaussianBlur(b, ksize=(5, 5), sigmaX=1)
                out.write(b)
                skip = 1
            else:
                break
        else:
            skip += 1

    cap.release()
    out.release()


cv2.destroyAllWindows()
