from moka import *
import numpy as np
import sys
import cv2
from glob import glob
from moviepy.editor import VideoFileClip, concatenate_videoclips


def slowdownVideo(vid):
	cap = cv2.VideoCapture(vid)
	width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH ))   # float `width`
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
	print(width, height)

	outname = vid.split('.mp4')[0]
	outname = outname.split('/')[-1]
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')

	out = cv2.VideoWriter(f'./slow/{outname}.mp4', fourcc, 5.0, (width, height))
	cnt = 0
	while True:
		ret, frame = cap.read()
		if ret:
			frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
			out.write(frame)
			cnt += 1
			if cnt > 50:
				break
		else:
			break
	out.release()


if __name__ == '__main__':
	videos = sorted(glob(f'{sys.argv[1]}/*.mp4'))
	for video in videos:
		slowdownVideo(video)