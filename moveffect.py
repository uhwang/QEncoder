# -*- coding: utf-8 -*-
'''

The timecode format used is hours:minutes:seconds,milliseconds 
with time units fixed to two zero-padded digits and fractions 
fixed to three zero-padded digits (00:00:00,000). 
The fractional separator used is the comma, since the program 
was written in France.

1. A numeric counter identifying each sequential subtitle
2. The time that the subtitle should appear on the screen, followed by --> and the time it should disappear
3. Subtitle text itself on one or more lines
4. A blank line containing no text, indicating the end of this subtitle

Formatting[edit]
Unofficially the format has very basic text formatting, which can be either interpreted or passed through for rendering depending on the processing application. Formatting is derived from HTML tags for bold, italic, underline and color.

Bold – <b> ... </b> or {b} ... {/b}
Italic – <i> ... </i> or {i} ... {/i}
Underline – <u> ... </u> or {u} ... {/u}
Font color – <font color="color name or #code"> ... </font> (as in HTML)

Exam:
168
00:20:41,150 --> 00:20:45,109
- How did he do that?
- Made him an offer he couldn't refuse.

'''
from PIL import Image, ImageFont, ImageDraw
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

vsource = '원본영상.m2t'
vsize = (1024, 768)

title = '목사시취'
#font_name = "Haansoft-Batang"
#font_color = 'white'
#font_size = 100
#title_duration = 2.0

#generator = lambda txt: TextClip(txt, font=font_name, fontsize=20, color='white')
#sub = SubtitlesClip('subtitle.srt', generator)

#img = Image.new('RGB', (vsize[0], vsize[1]), (255,255,255))
#title01 = ImageClip(img)
#title01.set_duration(2)
clip = VideoFileClip(vsource)
#txt1 = TextClip(title, color=font_color, font=font_name, kerning = 5, fontsize=font_size).set_duration(2.0)

title01 = ImageClip('title02.png')
title01.set_duration(2)
#video = CompositeVideoClip([clip, title01], vsize)
#video = CompositeVideoClip([clip], vsize)
video = CompositeVideoClip([title01, clip], vsize)
#video = concatenate_videoclips([title.set_pos('center'), clip])
#video = concatenate_videoclips([title, clip, sub])

video.set_duration(12).write_videofile('res.mp4', codec='libx264', fps=clip.fps)




















