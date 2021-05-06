import numpy as np
import cv2
import sys
from glob import glob

# gt_file = 'Controllable_Gen/gt_ControlGen.mp4'
# test_file = 'Controllable_Gen/test_ControlGen.mp4'
gt_file = 'Pixel_Physics/gt_PixelPhysics.mp4'
test_file = 'Pixel_Physics/test_PixelPhysics.mp4'

def combineVideo(vids, idx):
	caps = []
	for vid in vids:
		caps.append(cv2.VideoCapture(vid))
		print("vid", vid)
	width  = int(caps[0].get(cv2.CAP_PROP_FRAME_WIDTH ))   # float `width`
	height = int(caps[0].get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')

	out = cv2.VideoWriter(f'./output2/output{idx}.mp4', fourcc, 5.0, (width * 2, height * 2))

	while True:
		rets = []
		frames = []
		for i, cap in enumerate(caps):
			ret, frame = cap.read()
			if ret:
				rets.append(ret)
				frames.append(frame)
				# print(i, frame.shape)

		if rets:
			concat1 = np.concatenate((frames[0], frames[1]), axis=1)
			concat2 = np.concatenate((frames[2], frames[3]), axis=1)
			# print(concat1.shape, concat2.shape)
			concat = np.concatenate((concat1, concat2), axis=0)
			out.write(concat)
		else:
			break
	out.release()


if __name__ == '__main__':
	vidpaths = sorted(glob(f"./{sys.argv[1]}/video*"))
	for idx, vidpath in enumerate(vidpaths):
		video = sorted(glob(f"{vidpath}/*.mp4"))
		combineVideo(video, idx)