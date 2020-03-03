# -*- coding: utf-8 -*-
from moviepy.editor import *
from moviepy.video.tools.drawing import circle

main_clip = VideoFileClip("Thanksgiving.mp4")
start_clip = main_clip.subclip("00:00:00.00", "00:02:34.00")
end_clip = main_clip.subclip("00:02:34.00","00:02:37.00").add_mask()
           
w,h = main_clip.size

# The mask is a circle with vanishing radius r(t) = 800-200*t               
end_clip.mask.get_frame = lambda t: circle(screensize=(main_clip.w,main_clip.h),
                                       center=(main_clip.w/2,main_clip.h/4),
                                       radius=max(0,int(800-200*t)),
                                       col1=1, col2=0, blur=4)


the_end = TextClip("The End", font="Amiri-bold", color="white",
                   fontsize=70).set_duration(end_clip.duration)
				   #set_duration(clip.duration)
#the_end.set_start("00:00:10.00")
#end_clip.set_start("00:00:10.00")
final = CompositeVideoClip([the_end.set_pos('center'),end_clip],
                           size = main_clip.size)
                           
final.write_videofile("theEnd.mp4")

#end_clip = VideoFileClip("theEnd.mp4")
#final = concatenate_videoclips([start_clip, end_clip]).write_videofile("final.mp4")

