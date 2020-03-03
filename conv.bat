@echo off
echo =========== CONVERT MTS TO AVI =============

ffmpeg -i 00054.mts -vcodec mpeg4 -s 480x272 -b:v 600k -acodec mp3 -ab 96k 01.avi
ffmpeg -i 00055.mts -vcodec mpeg4 -s 480x272 -b:v 600k -acodec mp3 -ab 96k 02.avi

echo =========== MERGE AVI ==============
ffmpeg -f concat -i list.txt -c copy all.avi

echo =========== MERGE AVI ==============
ffmpeg -i all.avi -vn -acodec copy all.mp3