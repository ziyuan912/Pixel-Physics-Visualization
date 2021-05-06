#!/bin/bash

for dir in ./$1/*; do
	echo $dir
	for filename in $dir/*.mp4; do
		mkdir ./test/${dir:18}
		echo $filename
	    ffmpeg -i $filename -vcodec libx264 -pix_fmt yuv420p ./test/${filename:18}
	done
done