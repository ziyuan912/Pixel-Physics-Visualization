# from moka import *
from glob import glob
import numpy as np
import sys
import cv2
from skimage.metrics import peak_signal_noise_ratio as PSNR


def PSNRHeatMap(gt_file, test_file, window_size, psnrs):
	gt = cv2.VideoCapture(gt_file)
	test = cv2.VideoCapture(test_file)
	width  = int(gt.get(cv2.CAP_PROP_FRAME_WIDTH ))   # float `width`
	height = int(gt.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
	print(width, height)

	outname = test_file.split('.mp4')[0]
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	outname = outname.split('/')[-1]
	print(f'{sys.argv[1]}/PSNR/{outname}_PSNR_CROP.mp4')
	out = cv2.VideoWriter(f'{sys.argv[1]}/PSNR/{outname}_PSNR_CROP.mp4', fourcc, 5.0, (width, height))
	cnt = 0

	while True:
		ret1, gt_frame = gt.read()
		ret2, test_frame = test.read()
		
		if ret1 and ret2:
			pic = np.zeros((height, width))

			for i in range(0, height, window_size):
				for j in range(0, width, window_size):
					psnr = PSNR(gt_frame[i:i + window_size, j:j + window_size], test_frame[i:i + window_size, j:j + window_size], data_range=255)
					pic[i:i + window_size, j:j + window_size] = psnr
			pic = 255 - (pic) * 255 / 60
			pic = np.uint8(pic)
			psnr = round(psnrs[cnt], 2)
			pic = cv2.applyColorMap(pic, cv2.COLORMAP_JET)
			cv2.putText(pic, f"PSNR = {psnr}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
			out.write(pic)
			cnt += 1
			if cnt > 50:
				break
		else:
			break
	out.release()

if __name__ == '__main__':
	pathnum = glob("./gt/gt_*")
	# vidpath.append(sorted(glob("./gt/gt_*")))
	nums = []
	for file in pathnum:
		num = int(file.split('gt_')[-1][:-4])
		nums.append(num)
		nums.sort()
	print(nums)
	testfiles = []
	gtfiles = []
	for num in nums:
		testfiles.append(f'{sys.argv[1]}/test_{num}.mp4')
		gtfiles .append(f'{sys.argv[2]}/gt_{num}.mp4')
	psnr = np.load(f"{sys.argv[1]}/psnr.npy")
	print(psnr.shape)
	for idx, (test_file, gt_file) in enumerate(zip(testfiles, gtfiles)):
		print(test_file, gt_file)
		PSNRHeatMap(test_file, gt_file, 4, psnr[idx])