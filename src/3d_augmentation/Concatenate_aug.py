import numpy as np
import cv2
from glob import glob

# gt_file = 'Controllable_Gen/gt_ControlGen.mp4'
# test_file = 'Controllable_Gen/test_ControlGen.mp4'
gt_file = 'Pixel_Physics/gt_PixelPhysics.mp4'
test_file = 'Pixel_Physics/test_PixelPhysics.mp4'

def combineVideo(vids, idx):
	caps = []
	for vid in vids:
		caps.append(cv2.VideoCapture(vid))
		# print(vid[idx])
	width1  = int(caps[0].get(cv2.CAP_PROP_FRAME_WIDTH ))   # float `width`
	height1 = int(caps[0].get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`

	fourcc = cv2.VideoWriter_fourcc(*'mp4v')

	out = cv2.VideoWriter(f'./output/output{idx + 10}.mp4', fourcc, 5.0, (width1 * 2, height1 * 2))
	while True:
		rets = []
		frames = []
		for i, cap in enumerate(caps):
			ret, frame = cap.read()
			if ret:
				rets.append(ret)
				frames.append(frame)
		if rets:
			concat1 = np.concatenate((frames[0], frames[1]), axis=1)
			concat2 = np.concatenate((frames[2], frames[3]), axis=1)
			concat = np.concatenate((concat1, concat2), axis=0)
			out.write(concat)
		else:
			break
	out.release()


if __name__ == '__main__':

	path = "./visualize_long"

	for num in range(4):
		vidpath = []
		vidpath.append(f"{path}/video{num}/front.mp4")
		vidpath.append(f"{path}/video{num}/main.mp4")
		vidpath.append(f"{path}/video{num}/right.mp4")
		vidpath.append(f"{path}/video{num}/top.mp4")
		combineVideo(vidpath, num)