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
		caps.append(cv2.VideoCapture(vid[idx]))
		print(vid[idx])
	width  = int(caps[0].get(cv2.CAP_PROP_FRAME_WIDTH ))   # float `width`
	height = int(caps[0].get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')

	out = cv2.VideoWriter(f'./output/output{idx}.mp4', fourcc, 5.0, (width * 3, height * 2))

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
			concat1 = np.concatenate((frames[0], frames[1], frames[2]), axis=1)
			concat2 = np.concatenate((frames[3], frames[4], frames[5]), axis=1)
			# print(concat1.shape, concat2.shape)
			concat = np.concatenate((concat1, concat2), axis=0)
			out.write(concat)
		else:
			break
	out.release()


if __name__ == '__main__':
	vidpath = []
	vidpath.append(sorted(glob("./gt/gt_*")))
	for i in range(5):
		vidpath.append([])
	for vid in vidpath[0]:
		num = vid.split('gt_')[-1][:-4]
		vidpath[1].append(f"./pp/test_{num}.mp4")
		vidpath[2].append(f"./Controllable/test_{num}.mp4")
		vidpath[3].append(f"./pose/pose_{num}.mp4")
		vidpath[4].append(f"./pp/PSNR/gt_{num}_PSNR_CROP.mp4")
		vidpath[5].append(f"./Controllable/PSNR/gt_{num}_PSNR_CROP.mp4")
	for i in range(len(vidpath[0])):
		combineVideo(vidpath, i)