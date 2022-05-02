# -*- coding: utf-8 -*-
'''
    Author
    -------------------------------------------------------------------------------------
    Uisang Hwang
    
    History
    
    May    2015  First version released w/o GUI
    Jul 20 2016  Replace PNG as Pixmap embed into encode.py
    Jul 18 2016  Added timed encoding 
    Jul 09 2016
    Aug 27 2016  GUI freezing solved by using QProcess
    Jan 17 2017  Advanced Encoding Option dialog added
    
                 1. encopt.py creates A/V encoder list directly by running
                 ffmpeg with -encoders on windows console
                 
                 2. Redirect stderr on windows console
                 ffmpeg -i sample.avi -hide_banner 2> info.txt
    Jan 18 2017  Find all ffmpeg in windows console. ImageMagick preceeds before tools.
                 Therefore, the old version is executed.
                 
                 where ffmpeg
                 C:\Program Files\ImageMagick-7.0.2-Q8\ffmpeg.exe
                 d:\tools\ffmpeg\bin\ffmpeg.exe
                 
                 Add advanced encoding option + toggle button
    Jan 20 2017  Rewrite Edit Video code
                 Fix regular expression for media info
    Jan 26 2017  Youtube playlist format:
                    http://www.youtube.com/playlist?list=PL6B08BAA57B5C7810
    
    Feb 08 2017  Add MP3 qscale option on Edit Video Tab
    Feb 10 2017  Add image resizing in execute_audio_convert
                 Add convert image to Base64 format
                http://stackoverflow.com/questions/16065694/is-it-possible-to-create-encodeb64-from-image-object
                http://stackoverflow.com/questions/31826335/how-to-convert-pil-image-image-object-to-base64-string
                Add file filter to FileDialogue
    Jul 10    2017 filter = "DVD (*.vob);;Video (*.m2t *.avi *.webm *.mp4);;Audio (*.mp3 *.aac);;All files"
    Jul 20  2017 Add 'Auto Merge' options : auto merge, keep fname, ext audio, use org acodec
    Aug 11  2017 Change preset encoding value(avi->mp4, 480272->720p)
    Aug 12  2017 Fix regular expression string of find_fps to get an integer or a floating number
    Jan 12  2018 Replace all os.system by subprocess because of encoding error on other systems
                 Video merge --> timer + QProcess
                 Audio merge --> subprocess
                 
    Jan 15  2018 Youtube-dl Error: 
                 ERROR: Unable to download webpage: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED]
                 Solution ==> --no-check-certificate
                 
                 [download] ???? has already been downloaded and merged
                 Solution ==> check the message
                 
                 [download] Destination: ????
                 [download]   4.3% of 656.34MiB at  2.55MiB/s ETA 04:06
                 
                 [download] 100% of 656.34MiB in 03:59
                 [download] Destination: ????
                 [download] 100% of 51.58MiB in 00:17
                 [ffmpeg] Merging formats into "????"
                 
    Feb 10  2018 https://stackoverflow.com/questions/2940858/kill-process-by-name/4230226#4230226
                    import psutil
                    PROCNAME = "ffmpeg.exe"        
                    for proc in psutil.process_iter():
                        # check whether the process name matches
                        if proc.name() == PROCNAME:
                            proc.kill()
    Mar 31  2018 ToDo List
                    (1) Save merge list as a project file
                    (2) At "Edit audio" add volume change
                        https://trac.ffmpeg.org/wiki/AudioVolume
                        ffmpeg -i input.wav -filter:a "volume=1.5" output.wav
                    (3) At "Edit audio" add Fade-In/Out effect
                        https://www.ffmpeg.org/ffmpeg-all.html#fade
                        type, t = "in" or "out"
                        
    May 10  2018 ToDo List
                    (1) Video Rotation
                    ffmpeg -i in.mp4 -vf "rotate=PI/2:bilinear=0"  -metadata:s:v:0 rotate=0 -c:v libx264 -c:a copy out.mp4

                    -vf "transpose=1"  -metadata:s:v:0 rotate=0 -c:v libx264 -c:a copy
                    
                    0 = 90CounterCLockwise and Vertical Flip (default)
                    1 = 90Clockwise
                    2 = 90CounterClockwise
                    3 = 90Clockwise and Vertical Flip
                    4 = 
                    
                    nearest, bilinear, or bicubic.
                    
                    CW
                    90 transpose=1
                    180 transpose=1,transpose=1
                    270 vflip,hflip
                    
                    CCW
                    90 transpose=2
                    180 transpose=2,transpose=2
                    270 hflip, vflip
    Apr 24 2019 Unicode encode error: writing chinese strings to a file
                    create wmlist.dll from wmlist.c
                    Use ctypes load 'wmlist.dll' and call open, write, close    

    Apr 25 2019 Audio file extension
                    mp3, aac, ac3, ogg, flac, opus, wav, raw
    Apr 26 2019 Exception handling on all processes
                    fix main run buttons disabled
                    
    --------------------------------------------------------------------------------------

    video: mp4 OpenDivx(Divx4)        600 kbps    24.00 fps
    audio: mp3 Audio Layer 3(CBR)    96  kbps    44100 Hz, 2ch
    size : 480x272
    
    10/14/2017
    ==========
    youtube-dl download subtitle
    youtube-dl --no-check-certificate --sub-lang en --write-auto-sub --skip-download URL
    
    10/15/2017
    ==========
    magick input.png -crop widthxheight+px0+py0 output.png
    width: the amount of pixels to cut from px0 in x direction
    height: the amount of pixels to cut from py0 in y direction
    px0: start point in x
    py0: start point in y
    
    12/21/2017
    ==========
    (<[\d]{2}:[\d]{2}:[\d]{2}.\d*>)(<c>)
'''

import re
import os, sys
import subprocess as sp
import datetime
import time
#import youtube_dl
from math import log
from PyQt4 import QtCore, QtGui
from PIL import Image
import math
# from compat.py of moviepy 
from compat import PY3, DEVNULL

import icon_encode_file_add
import icon_encode_folder_open
import icon_encode_amerge         
import icon_encode_arrow_down    
import icon_encode_arrow_up     
import icon_encode_delete_all    
import icon_encode_delete        
import icon_encode_merge_option
import icon_encode_advanced
import icon_encode_advanced_on
import icon_encode_advanced_codec
import icon_youtube_download     
import icon_encode_play            
import icon_run                    
import icon_encode_table_sort_asc  
import icon_encode_table_sort_desc        
import icon_encode_trash          
import icon_encode_vmerge         
import icon_doc
import encopt

#from xml.etree.ElementTree import Element, SubElement, tostring
#import xml.etree.ElementTree as etree
#from PyQt4.phonon import Phonon
#from pathlib import *

skip_ffmpeg_encder_comment = 10
_find_duration   = re.compile ( '.*Duration: ([0-9:]+)', re.MULTILINE )
_find_videocodec = re.compile ( 'Video: (.*?) ', re.MULTILINE)
_find_videosize  = re.compile ( '(\d+\dx\d+\d)', re.MULTILINE)
_find_vbitrate   = re.compile ( '.*bitrate: (\d*. kb/s)')
_find_audiocodec = re.compile ( 'Audio: (.*?)(?=[, ])', re.MULTILINE)
_find_audiofreq  = re.compile ( '(\d*. Hz)', re.MULTILINE)
_find_abitrate   = re.compile ( '(\d+ kb/s)')
_find_avbitrate  = re.compile ( '(\d+ kb\/s)' )
_check_time      = re.compile ( '[0-9]{2}:[0-9]{2}:[0-9]{2}')
_find_time       = re.compile ( 'time=[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{2}')
_find_fps        = re.compile ( '(((\d+)|(\d+.\d+)) fps)') 

_output_fname = 'MediaCut'
_video_edit_cut = 'VCut'
_audio_from_video = 'AExt'
_setting_xml = 'setting.xml'

_qprocess_error_string = ['FailedToStar', 'Crashed', 'Timedout', 'WriteError', 'ReadError', 'UnknownError']

_mergefile_name      = 'list.txt'
_encode_vres         = '720'
_encode_hres         = '1280'
_encode_vcodec       = 'libx264'
_encode_bitrate      = '600k'
_encode_frmrate      = '24'
_encode_acodec       = 'libmp3lame'
_encode_audio_sample = '128k'
_merge_file_format   = '%03d.%s'
_video_type          = 'm2t;mts'

_video_type_xml         = 'VType'    
_encode_vres_xml        = 'VRes'     
_encode_hres_xml        = 'HRes'     
_encode_vcodec_xml      = 'VCodec'   
_encode_bitrate_xml     = 'Bitrate'  
_encode_frmrate_xml     = 'FrmRate'  
_encode_acodec_xml      = 'ACodec'   
_encode_audio_sample_xml= 'ASample'  
_mergefile_name_xml     = 'Mergefile'
_merge_file_format_xml  = 'MFormat'
_merge_command_xml      = 'MCmd'
 
#_audio_format_extension = ['mp3', 'aac', 'ac3', 'ogg', 'flac','opus', 'wav', 'raw'] 

_external_mlist_lib = 'wmlist.dll'

#http://stackoverflow.com/questions/2066076/how-do-i-enable-ffmpeg-logging-and-where-can-i-find-the-ffmpeg-log-file
# FFmpeg does not write to a specific log file, 
# but rather sends its output to standard error. 
# To capture that, you need to either
# capture and parse it as it is generated
# redirect standard error to a file and read that afterward the process is finished

class AVOption:
    def __init__(self):
        # Video 
        self.vrot = False
        self.vrot_angle = "0"
        self.vtranspose = ""
        self.vflip = ""
        self.hflip = ""
        # Audio
        self.avol = ""
        #self.
        self.afade_type = "" # in / out
        self.afade_start = ""
        self.afade_end = ""
'''
"rotate=PI/2:bilinear=0"  -metadata:s:v:0 rotate=0 -c:v libx264 -c:a copy out.mp4


-vf "transpose=1"  -metadata:s:v:0 rotate=0 -c:v libx264 -c:a copy

0 = 90CounterCLockwise and Vertical Flip (default)
1 = 90Clockwise
2 = 90CounterClockwise
3 = 90Clockwise and Vertical Flip
4 = 

nearest”, “bilinear”, or “bicubic”.


CW
90 transpose=1
180 transpose=1,transpose=1
270 vflip,hflip

CCW
90 transpose=2
180 transpose=2,transpose=2
270 hflip, vflip

'''    
'''    
class QAVOption(QtGui.QDialog):
    def __init__(self, av_option):
        super(QAVOption, self).__init__()
        self.initUI(av_option)
        
    def initUI(self, minfo):
'''    

class AdvancedEncodingInfo:
    def __init__(self):
        self.use         = False
        self.vcodec      = 38 # mpeg4
        self.vbitrate    = 1 # 200
        self.vresolution = 1
        self.user_vresolution = ''
        self.vframerate  = 3
        self.user_vframerate   = ''
        self.vaspect     = 1
        self.acodec      = 26 # libmp3lame
        self.abitrate    = 7
        self.afreq       = 6
        self.achannel    = 3
        self.option      = ''

class MediaInfo:
    def __init__(self):
        self.video = False
        self.audio = False
        self.duration = ''
        self.vbitrate = ''
        self.videocodec = ''
        self.videosize = ''
        self.fps = ''
        self.audiocodec = ''
        self.audiofreq = ''
        self.abitrate = ''

_video_type_xml         = 'VType'    
_encode_vres_xml        = 'VRes'     
_encode_hres_xml        = 'HRes'     
_encode_vcodec_xml      = 'VCodec'   
_encode_bitrate_xml     = 'Bitrate'  
_encode_frmrate_xml     = 'FrmRate'  
_encode_acodec_xml      = 'ACodec'   
_encode_audio_sample_xml= 'ASample'  
_mergefile_name_xml     = 'Mergefile'
_merge_file_format_xml  = 'MFormat'
_merge_command_xml      = 'MCmd'

_youtube_download_path = 'youtube'
_global_error_msg = ""

_encode_tab_text = [ 
    'Encode',
    'Edit Video',
    'Audio',
    'Youtube',
    'Setting'
]

def get_encodetab_text()   : return _encode_tab_text[0]
def get_editvideotab_text(): return _encode_tab_text[1]
def get_audiotab_text()    : return _encode_tab_text[2]
def get_youtubetab_text()  : return _encode_tab_text[3]
def get_settingtab_text()  : return _encode_tab_text[4]

def get_process_error_string(ecode): return _qprocess_error_string[ecode]
        

def sys_write_flush(s):
    """ Writes and flushes without delay a text in the console """
    # Reason for not using `print` is that in some consoles "print" 
    # commands get delayed, while stdout.flush are instantaneous, 
    # so this method is better at providing feedback.
    # See https://github.com/Zulko/moviepy/pull/485
    sys.stdout.write(s)
    sys.stdout.flush()
    
def verbose_print(verbose, s):
    """ Only prints s (with sys_write_flush) if verbose is True."""
    if verbose:
        sys_write_flush(s)
        
# from tools.py of moviepy
def subprocess_call(cmd, verbose=True, errorprint=True):
    """ Executes the given subprocess command."""

    verbose_print(verbose, "\n[QEncoder] Running:\n>>> "+ " ".join(cmd))
    
    popen_params = {"stdout": DEVNULL,
                    "stderr": sp.PIPE,
                    "stdin": DEVNULL}
    
    if os.name == "nt":
        popen_params["creationflags"] = 0x08000000
    
    proc = sp.Popen(cmd, **popen_params)
    
    out, err = proc.communicate() # proc.wait()
    proc.stderr.close()

    if proc.returncode:
        verbose_print(errorprint, "\n[QEncoder] This command returned an error !")
        _global_error_msg = err.decode('utf8')
        raise IOError(_global_error_msg)
    else:
        verbose_print(verbose, "\n... command successful.\n")
        return "... command successful"
    
    del proc
    
'''
def read_setting_xml(xfile):
    try:
        root = etree.parse(xfile)
    except FileNotFoundError as err:
        root = etree.Element('root')
        etree.append(root)
        
        vtype = etree.SubElement(root, _video_type_xml)
        vtype.text = _video_type
        etree.append(vtype)
        
        vres = etree.SubElement(root, _encode_vres_xml)
        vres.text = _encode_vres
        etree.append(vres)
        
        hres = etree.SubElement(root, _encode_hres_xml)
        hres.text = _encode_hres
        etree.append(hres)
        
        etree.write(xfile)
    
    if root:
        return
    else:
'''
#https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])
   
#def get_duration(path):
def get_mediainfo(path):
    mi = MediaInfo()
    cmd=['ffmpeg',  '-i', path, '-hide_banner']
    #cmd=['ffprobe',  '-i', path]
    #proc = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        
    popen_params = {"stdout": DEVNULL,
                    "stderr": sp.PIPE,
                    "stdin": DEVNULL}

    if os.name == "nt":
        popen_params["creationflags"] = 0x08000000
    proc = sp.Popen(cmd, **popen_params)
    
    
    output = proc.communicate()[1]
    # http://stackoverflow.com/questions/606191/convert-bytes-to-a-python-string
    output = output.decode('utf-8')
    output = output.split('\n')

    for i in range(len(output)):
        match = _find_duration.search(output[i])
        if match:
            mi.duration = match.group(1)
            match = _find_vbitrate.search(output[i])
            if match:
                mi.vbitrate = match.group(1)
            else: mi.vbitrate = 'N/A'
            continue
        match = _find_videocodec.search(output[i])
        if match:
            mi.video = True
            mi.videocodec = match.group(1)
            match = _find_videosize.search(output[i])
            if match:
                mi.videosize = match.group(1)
            else: mi.videosize = 'N/A'
            match = _find_fps.search(output[i])
            if match:
                mi.fps = match.group(1)
            else: mi.fps = 'N/A'
            continue
            
        match = _find_audiocodec.search(output[i])
        if match:
            mi.audio = True
            mi.audiocodec = match.group(1)
            match = _find_audiofreq.search(output[i])
            if match:
                mi.audiofreq = match.group(1)
            else: mi.audiofreq = 'N/A'
                        
            #match = _find_abitrate.search(output[i])
            match = _find_avbitrate.search(output[i])
            print(output[i])
            if match:
                mi.abitrate = match.group(1)
            else: mi.abitrate = 'N/A'
            continue

    if not mi.audio:
        mi.audio = True
        mi.audiocodec = 'N/A'
        mi.audiofreq = 'N/A'
        mi.abitrate = 'N/A'
    if not mi.video:
        mi.video = True
        mi.videocodec = 'N/A'
        mi.videosize = 'N/A'
        mi.vbitrate = 'N/A'
        mi.fps = 'N/A'
        
    return mi

#https://arcpy.wordpress.com/2012/04/20/146/    
def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)
'''
def time_to_sec(t):
    if t.find(':'):
        t_list = t.split(':')
        t_sec = int(t_list[0])*60+int(t_list[1])
    else:
        t_sec = int(t)
    return t_sec
'''

def fix_time(t):
    t2 = t.split(':')
    #print(t)
    if not t2[0]: t2[0] = '0'
    if not t2[1]: t2[1] = '0'
    if not t2[2]: t2[2] = '0'
    #print(t2)
    return '%02d:%02d:%02d'%(int(t2[0]),int(t2[1]),int(t2[2]))
    
def time_to_sec(t1):
    t2 = t1.split(':')
    sec = 60*(int(t2[0])*60+int(t2[1]))+int(t2[2])#+float(t2[3])*.01
    return sec

def run_time_to_sec(t1):
    t2 = t1.split(':')
    return 60.0*(int(t2[0])*60+int(t2[1]))+float(t2[2])

class MergeInfo:
    def __init__(self):
        self.auto_merge = True
        self.keep_fname = False
        self.audio_ext = False
        self.use_source_acodec = True

class QSelectPMCCodec(QtGui.QDialog):
    def __init__(self):
        super(QSelectPMCCodec, self).__init__()
        self.initUI()
    
    def initUI(self):
        layout = QtGui.QFormLayout()
        button_layout = QtGui.QHBoxLayout()
        item_layout = QtGui.QHBoxLayout()
        
        self.pcm = QtGui.QComboBox(self)
        for x in encopt._pcm_acodec:
            self.pcm.addItem(x)
        item_layout.addWidget(self.pcm)
        
        index = self.pcm.findText("pcm_s16le", QtCore.Qt.MatchFixedString)
        if index >=0:
            self.pcm.setCurrentIndex(index)
            
        self.ok = QtGui.QPushButton('OK')
        self.cancel = QtGui.QPushButton('CANCEL')
        self.ok.clicked.connect(self.accept)
        self.cancel.clicked.connect(self.reject)
        button_layout.addWidget(self.ok)
        button_layout.addWidget(self.cancel)
        layout.addRow(item_layout)
        layout.addRow(button_layout)
        self.setLayout(layout)
        
    def get_pcm_codec(self):
        return self.pcm.currentText()
        
class QMergeOption(QtGui.QDialog):
    def __init__(self, minfo):
        super(QMergeOption, self).__init__()
        self.initUI(minfo)
        
    def initUI(self, minfo):
        self.old_info = minfo
        layout = QtGui.QFormLayout()
        layout1 = QtGui.QVBoxLayout()
        self.auto_merge = QtGui.QCheckBox('Auto merge')
        self.keep_fname = QtGui.QCheckBox('Keep fname') 
        self.audio_ext = QtGui.QCheckBox('Audio ext')
        self.use_source_acodec = QtGui.QCheckBox('Src ACodec(default:MP3)')
        layout.addWidget(self.auto_merge)
        layout.addWidget(self.keep_fname)
        layout.addWidget(self.audio_ext)
        layout.addWidget(self.use_source_acodec)
        self.auto_merge.setChecked(minfo.auto_merge)
        self.keep_fname.setChecked(minfo.keep_fname)
        self.audio_ext.setChecked(minfo.audio_ext)
        self.use_source_acodec.setChecked(minfo.use_source_acodec)
        layout2 = QtGui.QHBoxLayout()
        self.ok = QtGui.QPushButton('OK')
        self.cancel=  QtGui.QPushButton('CANCEL')
        self.ok.clicked.connect(self.accept)
        self.cancel.clicked.connect(self.reject)
        layout2.addWidget(self.ok)
        layout2.addWidget(self.cancel)
        layout.addRow(layout1)
        layout.addRow(layout2)
        self.setLayout(layout)
        
    def get_auto_merge(self): return self.auto_merge.isChecked()
    def get_keep_fname(self): return self.keep_fname.isChecked()
    def get_audio_ext(self): return self.audio_ext.isChecked()
    def get_use_source_acodec(self): return self.use_source_acodec.isChecked()
    def get_merge_option(self):
        mi = MergeInfo()
        mi.auto_merge = self.get_auto_merge()
        mi.keep_fname = self.get_keep_fname()
        mi.audio_ext = self.get_audio_ext()
        mi.use_source_acodec = self.get_use_source_acodec()
        return mi
        
class QAdvancedEnocdeOption(QtGui.QDialog):
    def __init__(self, info):
        super(QAdvancedEnocdeOption, self).__init__()
        self.initUI(info)
        
    def initUI(self, info):
        #self.resize(218, 300)
        self.old_info = info
        self.prev_option = AdvancedEncodingInfo()
        layout = QtGui.QFormLayout()
        
        video_group = QtGui.QGroupBox('Video Option')
        video_layout = QtGui.QFormLayout()
        vcodec_layout = QtGui.QHBoxLayout()
        vcodec_layout.addWidget(QtGui.QLabel('Video Codec'))
        self.video_codec = QtGui.QComboBox(self)
        for i in range(len(encopt.vcodec_desc)):
            self.video_codec.addItem(encopt.vcodec_desc[i])
        vcodec_layout.addWidget(self.video_codec)
        self.connect(self.video_codec, QtCore.SIGNAL("currentIndexChanged(int)"), self.check_videocodec_option)
    
        vbitrate_layout = QtGui.QHBoxLayout()
        vbitrate_layout.addWidget(QtGui.QLabel('Bitrate'))
        self.video_bitrate = QtGui.QComboBox(self)
        for i in range(len(encopt.video_bitrate)):
            self.video_bitrate.addItem(encopt.video_bitrate[i])
        vbitrate_layout.addWidget(self.video_bitrate)
        
        vbitrate_layout.addWidget(QtGui.QLabel('Resolution'))
        self.video_resolution = QtGui.QComboBox(self)
        for i in range(len(encopt.video_resolution)):
            self.video_resolution.addItem(encopt.video_resolution[i])
        vbitrate_layout.addWidget(self.video_resolution)
        self.connect(self.video_resolution, QtCore.SIGNAL("currentIndexChanged(int)"), self.check_video_resolution)
        self.user_video_resolution = QtGui.QLineEdit()
        self.user_video_resolution.setEnabled(False)
        vbitrate_layout.addWidget(self.user_video_resolution)
        
        frmrate_layout = QtGui.QHBoxLayout()
        frmrate_layout.addWidget(QtGui.QLabel('Framerate'))
            
        self.frmrate = QtGui.QComboBox()
        for i in range(len(encopt.video_framerate)):
            self.frmrate.addItem(encopt.video_framerate[i])
        self.connect(self.frmrate, QtCore.SIGNAL("currentIndexChanged(int)"), self.check_frmrate)
        
        frmrate_layout.addWidget(self.frmrate)
        frmrate_layout.addWidget(QtGui.QLabel('FPS'))
        
        self.user_framerate = QtGui.QLineEdit()
        self.user_framerate.setEnabled(False)
        frmrate_layout.addWidget(self.user_framerate)
        
        frmrate_layout.addWidget(QtGui.QLabel('Aspect'))
        self.aspect = QtGui.QComboBox()
        for i in range(len(encopt.video_aspect)):
            self.aspect.addItem(encopt.video_aspect[i])        
        frmrate_layout.addWidget(self.aspect)
        
        video_layout.addRow(vcodec_layout)
        video_layout.addRow(vbitrate_layout)
        video_layout.addRow(frmrate_layout)
        video_group.setLayout(video_layout)
        
        audio_group = QtGui.QGroupBox('Audio Option')
        audio_layout = QtGui.QFormLayout()
        acodec_layout = QtGui.QHBoxLayout()
        acodec_layout.addWidget(QtGui.QLabel('Audio Codec'))
        self.audio_codec = QtGui.QComboBox(self)
        for i in range(len(encopt.acodec_desc)):
            self.audio_codec.addItem(encopt.acodec_desc[i])
        acodec_layout.addWidget(self.audio_codec)
        audio_layout.addRow(acodec_layout)
        
        abitrate_layout = QtGui.QHBoxLayout()
        abitrate_layout.addWidget(QtGui.QLabel('Bitrate'))
        self.audio_bitrate = QtGui.QComboBox(self)
        for i in range(len(encopt.audio_bitrate)):
            self.audio_bitrate.addItem(encopt.audio_bitrate[i])
        abitrate_layout.addWidget(self.audio_bitrate)
        
        abitrate_layout.addWidget(QtGui.QLabel('Frequency'))
        self.audio_freq = QtGui.QComboBox(self)
        for i in range(len(encopt.audio_freq)):
            self.audio_freq.addItem(encopt.audio_freq[i])
        abitrate_layout.addWidget(self.audio_freq)
        
        abitrate_layout.addWidget(QtGui.QLabel('Channel'))
        self.audio_channel = QtGui.QComboBox(self)
        for i in range(len(encopt.audio_channel)):
            self.audio_channel.addItem(encopt.audio_channel[i])
        abitrate_layout.addWidget(self.audio_channel)
        
        audio_layout.addRow(abitrate_layout)
        audio_group.setLayout(audio_layout)

        ok_layout = QtGui.QHBoxLayout()
        self.remember = QtGui.QPushButton('Remember')
        self.copy = QtGui.QPushButton('Copy')
        self.restore = QtGui.QPushButton('Restore')
        self.init = QtGui.QPushButton('Init')
        self.ok = QtGui.QPushButton('OK')
        self.cancel=  QtGui.QPushButton('CANCEL')
        
        self.remember.clicked.connect(self.remember_option)
        self.copy.clicked.connect(self.copy_option)
        self.restore.clicked.connect(self.restore_option)
        self.init.clicked.connect(self.init_option)
        
        self.ok.clicked.connect(self.accept)
        self.cancel.clicked.connect(self.reject)

        ok_layout.addWidget(self.remember)
        ok_layout.addWidget(self.copy)
        ok_layout.addWidget(self.restore)
        ok_layout.addWidget(self.init)
        ok_layout.addWidget(self.ok)
        ok_layout.addWidget(self.cancel)
        ok_layout.setAlignment(QtCore.Qt.AlignCenter)
        #self.ok.clicked.connect(self.close_option)
    
        layout.addRow(video_group)
        layout.addRow(audio_group)
        layout.addRow(ok_layout)
        self.setLayout(layout)
                
        self.video_codec.setCurrentIndex(info.vcodec)
        self.video_bitrate.setCurrentIndex(info.vbitrate)
        self.video_resolution.setCurrentIndex(info.vresolution)
        if self.video_resolution.currentText().lower() == 'input':
            self.user_video_resolution.setText(info.user_vresolution)
        
        self.frmrate.setCurrentIndex(info.vframerate)
        if encopt.video_framerate[info.vframerate].lower() == 'input':
            self.self.user_framerate.setText(info.user_vframerate)
        
        self.aspect.setCurrentIndex(info.vaspect)
        self.audio_codec.setCurrentIndex(info.acodec)
        self.audio_bitrate.setCurrentIndex(info.abitrate)
        self.audio_freq.setCurrentIndex(info.afreq)
        self.audio_channel.setCurrentIndex(info.achannel)
        return

    def init_option(self):
        self.video_codec.setCurrentIndex     (encopt.default_vcodec)
        self.video_bitrate.setCurrentIndex   (1)
        self.video_resolution.setCurrentIndex(1)
        self.user_video_resolution.setText   ('')
        self.frmrate.setCurrentIndex         (3)
        self.user_framerate.setText          ('')
        self.aspect.setCurrentIndex          (1)
        self.audio_codec.setCurrentIndex     (encopt.default_acodec)
        self.audio_bitrate.setCurrentIndex   (7)
        self.audio_freq.setCurrentIndex      (6)
        self.audio_channel.setCurrentIndex   (3)
        return
        
    def remember_option(self):
        self.prev_option.vcodec          = self.video_codec.currentIndex()
        self.prev_option.vbitrate        = self.video_bitrate.currentIndex()
        self.prev_option.vresolution     = self.video_resolution.currentIndex()
        self.prev_option.user_vresolution= self.user_video_resolution.text()
        self.prev_option.vframerate      = self.frmrate.currentIndex()
        self.prev_option.user_vframerat  = self.user_framerate.text()
        self.prev_option.vaspect         = self.aspect.currentIndex()
        self.prev_option.acodec          = self.audio_codec.currentIndex()
        self.prev_option.abitrate        = self.audio_bitrate.currentIndex()
        self.prev_option.afreq           = self.audio_freq.currentIndex()
        self.prev_option.achannel        = self.audio_channel.currentIndex()
        return
        
    def copy_option(self):
        self.video_codec.setCurrentIndex     (0)
        self.video_bitrate.setCurrentIndex   (0)
        self.video_resolution.setCurrentIndex(0)
        self.frmrate.setCurrentIndex         (0)
        self.aspect.setCurrentIndex          (0)
        self.audio_codec.setCurrentIndex     (0)
        self.audio_bitrate.setCurrentIndex   (0)
        self.audio_freq.setCurrentIndex      (0)
        self.audio_channel.setCurrentIndex   (0)
        return 
    
    def restore_option(self):
        self.video_codec.setCurrentIndex     (self.prev_option.vcodec)
        self.video_bitrate.setCurrentIndex   (self.prev_option.vbitrate)
        self.video_resolution.setCurrentIndex(self.prev_option.vresolution)
        self.user_video_resolution.setText   (self.prev_option.user_vresolution)
        self.frmrate.setCurrentIndex         (self.prev_option.vframerate)
        self.user_framerate.setText          (self.prev_option.user_vframerate)
        self.aspect.setCurrentIndex          (self.prev_option.vaspect)
        self.audio_codec.setCurrentIndex     (self.prev_option.acodec)
        self.audio_bitrate.setCurrentIndex   (self.prev_option.abitrate)
        self.audio_freq.setCurrentIndex      (self.prev_option.afreq)
        self.audio_channel.setCurrentIndex   (self.prev_option.achannel)
        return 
                
    def check_videocodec_option(self):
        if self.video_codec.currentText().lower() == 'none':
            self.video_bitrate.setEnabled(False)
            self.video_resolution.setEnabled(False)
            self.user_video_resolution.setEnabled(False)
            self.frmrate.setEnabled(False)
            self.user_framerate.setEnabled(False)
            self.aspect.setEnabled(False)
        else:
            self.video_bitrate.setEnabled(True)
            self.video_resolution.setEnabled(True)
            self.user_video_resolution.setEnabled(True)
            self.frmrate.setEnabled(True)
            self.user_framerate.setEnabled(True)
            self.aspect.setEnabled(True)
        return
    
    def check_audiocodec_option(self):
        if self.video_codec.currentText().lower() == 'none':
            self.audio_codec.setEnabled(False)
            self.audio_bitrate.setEnabled(False)
            self.audio_freq.setEnabled(False)
            self.audio_channel.setEnabled(False)
        else:
            self.audio_codec.setEnabled(True)
            self.audio_bitrate.setEnabled(True)
            self.audio_freq.setEnabled(True)
            self.audio_channel.setEnabled(True)
        
        return
        
    def check_frmrate(self):
        if self.frmrate.currentText().lower() == 'input':
            self.user_framerate.setEnabled(True)
        else:
            self.user_framerate.setEnabled(False)
        return
    
    def check_video_resolution(self):
        if self.video_resolution.currentText().lower() == 'input':
            self.user_video_resolution.setEnabled(True)
        else:
            self.user_video_resolution.setEnabled(False)
        return

    def get_encode_option(self):
        aei                  = AdvancedEncodingInfo()
        aei.vcodec           = self.video_codec.currentIndex()
        aei.vbitrate         = self.video_bitrate.currentIndex()
        aei.vresolution      = self.video_resolution.currentIndex()
        aei.user_vresolution = self.user_video_resolution.text()
        aei.vframerate       = self.frmrate.currentIndex()
        aei.user_vframerate  = self.user_framerate.text()
        aei.vaspect          = self.aspect.currentIndex()
        aei.acodec           = self.audio_codec.currentIndex()
        aei.abitrate         = self.audio_bitrate.currentIndex()
        aei.afreq            = self.audio_freq.currentIndex()

        opt = list()
        
        if self.video_codec.currentText().lower() == 'none':
            opt.extend(['-vn'])
        else:
            #if self.video_codec.currentIndex() > 1:
            if self.video_codec.currentText().lower() == 'copy':
                opt.extend(['-c:v', 'copy'])
            else:
                if self.video_bitrate.currentIndex() > 0:
                    opt.extend(['-b:v', '%sk' % self.video_bitrate.currentText()])
                
                if self.frmrate.currentIndex() > 0:
                    opt.append('-r')
                    if self.frmrate.currentText().lower() == 'input':
                        opt.append(self.user_framerate.text())
                    else:
                        opt.append(self.frmrate.currentText())
                    
                if self.video_resolution.currentIndex() > 0:
                    opt.append('-s')
                    if self.frmrate.currentText().lower() == 'input':
                        opt.append(self.user_video_resolution.currentText())
                    else:
                        opt.append(self.video_resolution.currentText())
                
            if self.aspect.currentIndex() > 0:
                opt.extend(['-aspect', '%s' % self.aspect.currentText()])

        if self.audio_codec.currentText().lower() == 'none':
                opt.extend(['-an'])
        else:
            #if self.audio_codec.currentIndex() > 1:
            if self.audio_codec.currentText().lower() == 'copy':
                opt.extend(['-c:a', 'copy'])
            else:    
                if self.audio_bitrate.currentIndex() > 0:
                    opt.extend(['-b:a', '%sk' % self.audio_bitrate.currentText()])
                    
                if self.audio_freq.currentIndex() > 0:
                    opt.extend(['-ar', self.audio_freq.currentText()])
                    
                if self.audio_channel.currentIndex() > 0:
                    opt.extend(['-ac', '%s' % self.audio_channel.currentText()])
            
        aei.option = opt
        
        return aei

class QEncodeEnv:
    def __init__(self):
        self.mergefile_name = 'list.txt'
        self.video_file_list = []
        self.merge_file_list = []
        self.encode_vres = _encode_vres
        self.encode_hres = _encode_hres
        self.encode_vcodec = _encode_vcodec
        #self.encode_bitrate = _encode_bitrate
        #self.encode_frmrate = _encode_frmrate
        self.encode_acodec = _encode_acodec 
        self.encode_audio_sample = _encode_audio_sample
        self.merge_file_format = '%03d.mp4'
        self.video_type = 'm2t;mts'
        #self.self_path = os.getcwd()
        self.current_qencoder_path = os.getcwd()
        self.audio_conv_folder = True
        
    def clear_file_list(self):
        self.video_file_list = []
        self.merge_file_list = []
        
    def add_video_file(self, v):
        self.video_file_list.append(v)

    def get_video_count(self):
        return len(self.video_file_list)

    def get_video_file(self, n):
        return self.video_file_list[n]
        
    def get_merge_file(self, n):
        return self.merge_file_list[n]

    def get_mergefile_count(self):
        return len(self.merge_file_list)
        
    def add_merge_file(self, v):
        self.merge_file_list.append(v)

class QEncode(QtGui.QWidget):
    def __init__(self):
        super(QEncode, self).__init__()
        self.initUI()
        self.setting = QEncodeEnv()
        self.advanced_encoding_info = AdvancedEncodingInfo()
        self.merge_info = MergeInfo()
        self.edit_media_info = MediaInfo()
        #self.current_qencoder_path = os.getcwd()
        #read_setting_xml(_setting_xml)
        encopt.create_ffmpeg_enclist(skip_ffmpeg_encder_comment)
        encopt.default_vcodec = encopt.vcodec_list.index('libx264')
        encopt.default_acodec = encopt.acodec_list.index('libmp3lame')
        self.advanced_encoding_info.vcodec = encopt.default_vcodec
        self.advanced_encoding_info.acodec = encopt.default_acodec

    def initUI(self):
        import icon_encoder  
        self.form_layout  = QtGui.QFormLayout()
        tab_layout = QtGui.QVBoxLayout()
        self.tabs = QtGui.QTabWidget()
        policy = self.tabs.sizePolicy()
        policy.setVerticalStretch(1)
        self.tabs.setSizePolicy(policy)
        self.tabs.setEnabled(True)
        self.tabs.setTabPosition(QtGui.QTabWidget.West)
        self.tabs.setObjectName('Media List')
        
        self.encode_tab     = QtGui.QWidget()
        self.audio_tab      = QtGui.QWidget()
        self.edit_video_tab = QtGui.QWidget()
        self.youtube_tab    = QtGui.QWidget()
        self.setting_tab    = QtGui.QWidget()
        
        self.tabs.addTab(self.encode_tab    , get_encodetab_text   () )
        self.tabs.addTab(self.edit_video_tab, get_editvideotab_text() )
        self.tabs.addTab(self.audio_tab     , get_audiotab_text    () )
        self.tabs.addTab(self.youtube_tab   , get_youtubetab_text  () )
        self.tabs.addTab(self.setting_tab   , get_settingtab_text  () )
        
        self.encode_tab_UI()
        self.audio_tab_UI()
        self.editvideo_tab_UI()
        self.youtube_tab_UI()
        self.setting_tab_UI()
        
        tab_layout.addWidget(self.tabs)
        self.form_layout.addRow(tab_layout)
        self.setLayout(self.form_layout)
        self.setWindowTitle("ChEncoder")
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(icon_encoder.table)))
        self.show()
    
    def set_merge_option(self):
        merge_opt_dlg = QMergeOption(self.merge_info)
        if merge_opt_dlg.exec_() == 1:
            self.merge_info = merge_opt_dlg.get_merge_option()
        
    #def closeEvent(self, evnt):
    #    os.system("taskkill /f /im ffmpeg.exe")
    #    super(QEncode, self).closeEvent(evnt)
    #http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    def pretty_size(n,pow=0,b=1024,u='B',pre=['']+[p for p in 'KMGTPEZY']):
        pow,n=min(int(log(max(n*b**pow,1),b)),len(pre)-1),n*b**pow
        return "%%.%if %%s%%s"%abs(pow%(-pow-1))%(n/b**float(pow),pre[pow],u)

    def add_media_file(self):
        title = self.add_button.text()
        files = QtGui.QFileDialog.getOpenFileNames(self, title, directory=self.directory_path.text(), filter="Video (*.mov *.vob *.mkv *.m2t *.avi *.webm *.mp4);;Audio (*.mp3 *.aac *.opus);;All files (*.*)")
        nvideo = len(files)
        format_error = False
        if nvideo:
            #cur_row = self.video_list_table.rowCount()
            #self.insert_media_table(cur_row, nvideo, files)
            
            cur_row = self.video_list_table.rowCount()
            for k in range(nvideo):
                j = k + cur_row
                fdate = datetime.datetime.fromtimestamp(os.path.getmtime(files[k])).strftime("%Y-%m-%d %H:%M:%S").split(' ')
                mi = get_mediainfo(files[k])
                #fsize = self.pretty_size(os.path.getsize(self.video_file_list[k]))
                fpath, fname = os.path.split(files[k])
                if mi.duration is None: format_error = True
                self.video_list_table.insertRow(j)
                self.video_list_table.setItem(j, 0, QtGui.QTableWidgetItem(fname))
                self.video_list_table.setItem(j, 1, QtGui.QTableWidgetItem(fdate[0]))
                self.video_list_table.setItem(j, 2, QtGui.QTableWidgetItem(mi.duration))
                self.video_list_table.setItem(j, 3, QtGui.QTableWidgetItem(fdate[1]))
                self.video_list_table.setItem(k, 4, QtGui.QTableWidgetItem(mi.videocodec))
                self.video_list_table.setItem(k, 5, QtGui.QTableWidgetItem(mi.audiocodec))
            self.directory_path.setText(fpath)
            os.chdir(fpath)
            if format_error: 
                QtGui.QMessageBox.question(QtGui.QWidget(), 'Error', "Invalid Video File: {}".format(fname), QtGui.QMessageBox.Yes)

    def open_media_file(self):
        title = self.open_button.text()
        self.media_filenames = QtGui.QFileDialog.getOpenFileNames(self, title, directory=self.directory_path.text(), filter="Video (*.mkv *.mov *.vob *.mkv *.m2t *.avi *.webm *.mp4);;Audio (*.mp3 *.aac *.opus);;Images (*.png *.jpg);;All files (*.*)")
        nvideo = len(self.media_filenames)
        format_error = False
        if nvideo: 
            cur_tab = self.tabs.currentIndex()
            #if cur_tab == 0:
            if self.tabs.tabText(cur_tab) == get_encodetab_text():
                self.setting.clear_file_list()
                self.clear_videolist_table()
                self.video_list_table.setRowCount(nvideo)
                for k in range(nvideo):
                    fdate = datetime.datetime.fromtimestamp(os.path.getmtime(self.media_filenames[k])).strftime("%Y-%m-%d %H:%M:%S").split(' ')
                    mi = get_mediainfo(self.media_filenames[k])
                    #fsize = self.pretty_size(os.path.getsize(self.video_file_list[k]))
                    fpath, fname = os.path.split(self.media_filenames[k])
                    if mi.duration == '': format_error = True
                    self.video_list_table.setItem(k, 0, QtGui.QTableWidgetItem(fname))
                    self.video_list_table.setItem(k, 1, QtGui.QTableWidgetItem(fdate[0]))
                    self.video_list_table.setItem(k, 2, QtGui.QTableWidgetItem(mi.duration))
                    self.video_list_table.setItem(k, 3, QtGui.QTableWidgetItem(fdate[1]))
                    self.video_list_table.setItem(k, 4, QtGui.QTableWidgetItem(mi.videocodec))
                    self.video_list_table.setItem(k, 5, QtGui.QTableWidgetItem(mi.audiocodec))
                self.directory_path.setText(fpath)
                os.chdir(fpath)
                if format_error:
                    QtGui.QMessageBox.question(QtGui.QWidget(), 'Error', "Invalid Video File: {}".format(fname), QtGui.QMessageBox.Yes)
                
            #elif cur_tab == 2:
            elif self.tabs.tabText(cur_tab) == get_audiotab_text():
                # audio converting
                self.audio_list.clear()
                for k in range(nvideo):
                    fpath, fname = os.path.split(self.media_filenames[k])
                    self.audio_list.addItem(QtGui.QListWidgetItem(fname))
                    self.media_filenames[k] = fname
                self.audio_folder_path.setText(fpath)
                os.chdir(fpath)

    def create_merge_list(self, nvideo):
        self.global_message.appendPlainText("=> Create merge list")
        final_video = '{} {} {}'.format(self.publish_date.text(), self.publish_title.text(), self.publish_bible.text()).rstrip()

        if self.keep_path.isChecked():
            mfile_path = os.path.join(self.directory_path.text(), self.setting.mergefile_name)
            final_video_path = os.path.join(self.directory_path.text(), final_video)
        else: 
            mfile_path = os.path.join(self.setting.current_qencoder_path, self.setting.mergefile_name)
            final_video_path = os.path.join(self.setting.current_qencoder_path, final_video)
            
        writer = open(mfile_path, 'w')
        writer.write('#video list\n')
        write_error = False
        for k in range(nvideo):
            vfile = os.path.join(self.directory_path.text(),
                                 self.video_list_table.item(k,0).text())
            try:
                writer.write("file \'%s\'\n"%vfile)
            except UnicodeEncodeError as err:
                write_error = True
                #_global_error_msg = err
                #QtGui.QMessageBox(self, "Error", "Unicode encode error @ create_merge_list")
                self.global_message.appendPlainText("=> Error: %s"%err)
                break
        writer.close()
        
        dummy, self.merge_ext = os.path.splitext(os.path.join(self.directory_path.text(), self.video_list_table.item(0,0).text()))
        
        if write_error:
            self.global_message.appendPlainText("=> Load %s"%_external_mlist_lib)
            import ctypes
            try:
                wm = ctypes.CDLL(_external_mlist_lib)
            except OSError:
                err_msg = "=> Error: fail to Load %s"%_external_mlist_lib
                QtGui.QMessageBox.question(self, 'Error', err_msg)
                self.global_message.appendPlainText(err_msg)
            else:
                #self.global_message.appendPlainText("=> %s"%mfile_path)
                #if wm.mf_open(ctypes.c_char_p(mfile_path.encode('utf-8'))):
                #    wm.mf_write(ctypes.c_char_p('#New Video List\n'.encode('utf-8')))
                #print(mfile_path.encode('utf-8'))
                if wm.mf_open(ctypes.create_string_buffer(mfile_path)):
                    wm.mf_write(ctypes.c_char_p('#New Video List\n'))
                    
                    for k in range(nvideo):
                        vfile = "file \'%s\'"%os.path.join(self.directory_path.text(),
                                            self.video_list_table.item(k,0).text())
                        nbyte=wm.mf_write(ctypes.c_char_p(vfile.encode('utf-8')))
                        self.global_message.appendPlainText("=> [%03d] write %d bytes"%(k,nbyte))
                    wm.mf_close()
            
        return mfile_path, final_video_path.rstrip()
    
    def execute_video_merge(self):
        nvideo = self.video_list_table.rowCount()
        if nvideo < 1: return
        self.global_message.appendPlainText("=> Start: video merge[%d files]"%nvideo)
        mfile_path, final_video_path = self.create_merge_list(nvideo)
        container = self.video_format.currentText()
        
        self.encoding_step = 0
        self.accum_video_length = 0
        self.encoding_progress.setTextVisible(True)
        self.encoding_progress.setFormat("V-Merging: %p%")
        self.video_length, self.total_video_length = self.get_total_media_length()
        arg_list = ['ffmpeg', '-hide_banner', '-y', '-f', 'concat', '-safe', '0', '-i' ]
        arg_list.append(mfile_path)
        arg_list.extend(['-c', 'copy'])
        arg_list.append('%s.%s'%(final_video_path,container))
        
        self.vmerge_job_list=[[arg_list[0], arg_list[1:]]]
        sublist = self.vmerge_job_list[0]
        del self.vmerge_job_list[0]
            
        if self.encoding_timer.isActive():
            self.encoding_timer.stop()
        else:
            self.encoding_timer.start(100, self)
            
        self.process = QtCore.QProcess(self)
        self.process.setReadChannel(QtCore.QProcess.StandardError)
        QtCore.QObject.connect(self.process, QtCore.SIGNAL("finished(int)"), self.video_merge_finished)
        QtCore.QObject.connect(self.process, QtCore.SIGNAL("readyRead()"), self.video_merge_dataread)
        self.global_message.appendPlainText(sublist[0])
        self.process.start(sublist[0], sublist[1])
            
    def video_merge_dataread(self):
        data = str(self.process.readAll())
        match = _find_time.search(data)
        #self.last_error = data
        if match:
            time = match.group(0).split('=')
            sec = run_time_to_sec(time[1])+self.accum_video_length
            percent = sec/self.total_video_length*100.0
            self.encoding_step = percent
        
    def video_merge_finished(self):
        if (len(self.vmerge_job_list) == 0):
            self.encoding_progress.setValue(100)
            self.encoding_timer.stop()
            #self.print_encoding_time()
            #self.run_encoding.setEnabled(True)
            #self.run_vmerge.setEnabled(True)
            #self.run_amerge.setEnabled(True)
            self.global_message.appendPlainText("=> Stop: Video merge")
            self.enable_encoding_buttons()
            '''
            perror = self.process.error()
            print(perror)
            if perror in list(range(0,6)):
                print('Error occurred(code:%d): %s' % (perror, get_process_error_string(perror)))
                print('Last error: %s' % self.last_error)
            '''
            self.process = None
            return
        
    def execute_audio_merge(self):
        nvideo = self.video_list_table.rowCount()
        if nvideo <= 1: return
        self.global_message.appendPlainText("=> Start audio merge")
        mfile_path, final_video_path = self.create_merge_list(nvideo)
        cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', '%s'%mfile_path, '-hide_banner', '-c', 'copy', '%s%s'%(final_video_path, self.merge_ext)]
        self.global_message.appendPlainText("=> Start: audio merge\n   %s"%self.cmd_to_msg(cmd))
        try:
            self.global_message.appendPlainText(self.cmd_to_msg(cmd))
            subprocess_call(cmd)
        except (IOError, OSError) as err:
            QtGui.QMessageBox.question(self, 'Error', "%s"%err)
            self.enable_encoding_buttons()
    
    def get_total_media_length(self):
        total_length = 0
        length = []
        for k in range(self.video_list_table.rowCount()):
            item = self.video_list_table.item(k, 2)
            time = time_to_sec(item.text())
            length.append(time)
            total_length = total_length + time
        return length, total_length
    
    def timerEvent(self, e):
        if self.encoding_step >= 100:
            self.encoding_progress.setValue(100)
            self.encoding_timer.stop()
            return
        self.encoding_progress.setValue(self.encoding_step)

    def data_read(self):
        data = str(self.process.readAll())
        match = _find_time.search(data)
        if match:
            time = match.group(0).split('=')
            sec = run_time_to_sec(time[1])+self.accum_video_length
            percent = sec/self.total_video_length*100.0
            self.encoding_step = percent

    def encode_finished(self):
        if (len(self.encode_job_list) == 0):
            self.process = None
            self.encoding_progress.setValue(100)
            self.encoding_timer.stop()
            self.global_message.appendPlainText("=> Stop: encoding")
            if self.multiple_video and self.merge_info.auto_merge: #self.auto_merge.isChecked(): 
                self.merge_video_files()
            if self.merge_info.audio_ext:
                self.get_audio_from_video()
                self.resize_mp3()
            self.print_encoding_time()
            self.enable_encoding_buttons()
            return
        sublist = self.encode_job_list[0]
        del self.encode_job_list[0]
        self.accum_video_length = self.accum_video_length + self.video_length[0]
        del self.video_length[0]
        try:
            self.global_message.appendPlainText(self.cmd_to_msg(sublist[0], sublist[1]))
            self.process.start(sublist[0], sublist[1])
        except (IOError, OSError) as err:
            QtGui.QMessageBox.question(self, 'Error', "%s"%err)
            self.delete_job_list()
            self.enable_encoding_buttons()

    def delete_job_list(self):
        self.encode_job_list = []
        self.accum_video_length = 0
        self.encoding_timer.stop()
        
    def print_encoding_time(self):
        print("\t========= ENCODING COMPLETED")
        encoding_end = time.time()
        elasped_time = hms_string(encoding_end-self.encoding_start)
        print("\t========= Elasped time: {}".format(elasped_time))
        QtGui.QMessageBox.question(QtGui.QWidget(), 'Message', "Encoding Time: {}".format(elasped_time), QtGui.QMessageBox.Yes)
        self.global_message.appendPlainText("=> Total elasped time: %s"%elasped_time)
        
    def merge_video_files(self):
        cmd = ['ffmpeg', '-y', '-hide_banner', '-f', 'concat', '-safe', '0', '-i',  self.mfile_path, '-c', 'copy', self.final_video_name]
        
        self.global_message.appendPlainText("=> Video merge after encoding\n%s"%self.cmd_to_msg(cmd))
        try:
            subprocess_call(cmd)
        except (IOError, OSError) as err:
            QtGui.QMessageBox.question(self, 'Error', err)
            self.enable_encoding_buttons()
            self.global_message.appendPlainText(err_msg)
        
    def cmd_to_msg(self, cmd, arg=""):
        if isinstance(cmd, (list,)): msg1 = ' '.join(cmd)
        elif isinstance(cmd, (str,)): msg1 = cmd
        else: msg1 = "Invalid cmd type: %s"%type(cmd)
        
        if isinstance(arg, (list,)): msg2 = ' '.join(arg)
        elif isinstance(arg, (str,)): msg2 = arg
        else: msg2 = "Invalid arg type: %s"%type(arg)
        
        return "=> %s %s"%(msg1, msg2)
        
    def get_audio_from_video(self):
        self.global_message.appendPlainText('=> AUDIO FROM VIDEO')
        #acodec_ext = '%s'%self.setting.encode_acodec
        acodec_ext = encopt.get_audio_extension(self.setting.encode_acodec)
        if self.merge_info.use_source_acodec:
            acodec = 'copy'
        else:
            #acodec = '%s'%encopt.default_acodec
            acodec = 'libmp3lame'
            
        if self.merge_info.auto_merge or self.video_list_table.rowCount() == 1:
            if self.merge_info.use_source_acodec:
                mi = get_mediainfo(self.final_video_name)
                acodec_ext = encopt.get_audio_extension(mi.audiocodec)
                #acodec_ext = mi.audiocodec
            self.final_audio_file = '%s.%s'%(self.final_video_path, acodec_ext)
            cmd = ['ffmpeg', '-hide_banner', '-y', '-i', self.final_video_name, '-vn', '-acodec', acodec, self.final_audio_file]
            self.global_message.appendPlainText(self.cmd_to_msg(cmd))
            try:
                subprocess_call(cmd)
            except (IOError, OSError):
                QtGui.QMessageBox.question(self, 'Error', _global_error_msg)
        else:
            for i in range(self.setting.get_mergefile_count()):
                vf = self.setting.get_merge_file(i)
                mi = get_mediainfo(vf)
                of = vf[:vf.rfind('.')]
                acodec_ext = mi.audiocodec
                if not self.merge_info.use_source_acodec: acodec_ext = 'mp3'
            cmd = ['ffmpeg', '-hide_banner', '-y', '-i', vf, '-vn', '-acodec', acodec, '%s.%s'%(of, self.acodec_ext)]
            self.global_message.appendPlainText(self.cmd_to_msg(cmd))
            try:
                subprocess_call(cmd)    
            except (IOError, OSError):
                QtGui.QMessageBox.question(self, 'Error', _global_error_msg)
        
    def resize_mp3(self):
        mi = get_mediainfo(self.final_audio_file)
        
        if mi.audiocodec != 'mp3': return
        if not self.merge_info.auto_merge: return
        
        self.global_message.appendPlainText("=> Resize mp3")
        brate = self.mp3_bitrate_fmt.itemText(self.mp3_bitrate_fmt.count()-1).split(' ')
        old_mp3 = self.final_video_path+'.mp3'        
        new_mp3 = os.path.join(self.ofile_path, '{}kbit-{}.mp3'.format(brate[-1], self.publish_date.text()))

        cmd = ['ffmpeg', '-y', '-hide_banner', '-i', old_mp3, '-codec:a', 'libmp3lame', brate[0], brate[1], new_mp3]
        self.global_message.appendPlainText(self.cmd_to_msg(cmd))
        try:
            subprocess_call(cmd)
        except (IOError, OSError) as err:
            QtGui.QMessageBox.question(self, 'Error', "%s"%err)
            self.enable_encoding_buttons()    
    
    def start_encode_process(self):
        nvideo = self.video_list_table.rowCount()
        self.global_message.appendPlainText("=> Start: encoding [%d files]"%nvideo)
        if nvideo < 1: return
        self.encoding_start = time.time()
        final_video = '{} {} {}'.format(self.publish_date.text(), self.publish_title.text(), self.publish_bible.text())    
        self.setting.clear_file_list()
        self.encoding_step = 0

        #self.use_advanced.isChecked()
        if self.advanced_encoding_info.use or self.use_advanced.isChecked():
            arg_list = [ 'ffmpeg', '-hide_banner', '-y', '-i', '', ]
            arg_list.extend(self.advanced_encoding_info.option)
        else:
            arg_list = [
                'ffmpeg', '-hide_banner', '-y', '-i', '', 
                '-c:v','{}'.format(self.setting.encode_vcodec),
                '-s', '{}x{}'.format(self.setting.encode_hres,self.setting.encode_vres),
                #'-b:v', '{}'.format(self.setting.encode_bitrate),
                '-c:a', '{}'.format(self.setting.encode_acodec),
                '-b:a', '{}'.format(self.setting.encode_audio_sample)
                ]

        input_media_pos  = 4
        
        if self.timed_encoding.isChecked():
            if nvideo > 1:
                msg = QtGui.QMessageBox()
                msg.setWindowTitle("Timed Encoding Error")
                msg.setText("Not available on multiple video encoding")
                msg.addButton(QtGui.QMessageBox.Yes)
                ret = msg.exec_()
                self.timed_encoding.setChecked(False)
            else:
                msg = QtGui.QMessageBox()
                msg.setWindowTitle("Overwrite Warning")
                msg.setText("The {} will be overwritten by this new video.".format(final_video))
                msg.addButton(QtGui.QMessageBox.Yes)
                msg.addButton(QtGui.QMessageBox.No)
                ret = msg.exec_()
                if ret == QtGui.QMessageBox.No: return
                t1 = fix_time(self.timed_encoding_t1.text())
                t2 = fix_time(self.timed_encoding_t2.text())
                t1sec = time_to_sec(t1)
                t2sec = time_to_sec(t2)
                duration = t2sec - t1sec
                arg_list.append('-ss')
                arg_list.append('{}'.format(t1))
                arg_list.append('-t')
                arg_list.append('{}'.format(duration))
        
        if self.keep_path.isChecked():
            self.mfile_path = os.path.join(self.directory_path.text(), self.setting.mergefile_name)
            self.ofile_path = self.directory_path.text()
            self.final_video_path = os.path.join(self.directory_path.text(), final_video)
            #self.final_video_name = self.final_video_path+'.avi'
            self.final_video_name = self.final_video_path+'.%s'%self.video_format.currentText()
        else: 
            self.mfile_path = os.path.join(self.setting.current_qencoder_path, self.setting.mergefile_name)
            self.ofile_path = self.setting.current_qencoder_path
            self.final_video_path = os.path.join(self.setting.current_qencoder_path, final_video)
            #self.final_video_name = self.final_video_path+'.avi'
            self.final_video_name = self.final_video_path+'.%s'%self.video_format.currentText()
        
        self.video_length, self.total_video_length = self.get_total_media_length()
        #self.encode_job_list = []
        self.delete_job_list()
        #self.accum_video_length = 0
        #self.global_message.appendPlainText(self.cmd_to_msg(arg_list))
        if nvideo > 1:
            self.multiple_video = True
            writer = open(self.mfile_path, 'w')
            writer.write('#video list\n')
            container = self.video_format.currentText()
            for k in range(nvideo):
                if self.merge_info.keep_fname:
                    fname = self.video_list_table.item(k,0).text()
                    fname = fname[:fname.rfind('.')]
                    ofile = os.path.join(self.ofile_path, '%s.%s'%(fname, container))
                else:
                    ofile = os.path.join(self.ofile_path, '%03d.%s'%(k,container))
                #ofile = os.path.join(self.ofile_path, self.video_format.currentText())
                vfile = os.path.join(self.directory_path.text(),self.video_list_table.item(k,0).text())
                self.setting.add_video_file(vfile)
                self.setting.add_merge_file(ofile)
                writer.write("file \'%s\'\n"%ofile)
            writer.close()
            
            self.encoding_progress.setTextVisible(True)
            self.encoding_progress.setFormat("Encoding: %p%")
            self.process = QtCore.QProcess(self)
            self.process.setReadChannel(QtCore.QProcess.StandardError)
            QtCore.QObject.connect(self.process, QtCore.SIGNAL("finished(int)"), self.encode_finished)
            QtCore.QObject.connect(self.process, QtCore.SIGNAL("readyRead()"), self.data_read)

            arg_list.append(' ')
            for k in range(nvideo):
                arg3 = self.setting.get_video_file(k)
                arg9 = self.setting.get_merge_file(k)
                arg_list[input_media_pos] = arg3
                arg_list[-1] = arg9 
                job = [arg_list[0], arg_list[1:]]
                self.encode_job_list.append(job)

            #self.global_message.appendPlainText(self.cmd_to_msg(arg_list))
            sublist = self.encode_job_list[0]
            del self.encode_job_list[0]
            if self.encoding_timer.isActive():
                self.encoding_timer.stop()
            else:
                self.encoding_timer.start(100, self)
            
            self.process.started.connect(lambda: self.run_encoding.setEnabled(False))
            self.process.started.connect(lambda: self.run_vmerge.setEnabled(False))
            self.process.started.connect(lambda: self.run_amerge.setEnabled(False))
            try:
                self.global_message.appendPlainText(self.cmd_to_msg(sublist[0], sublist[1]))
                self.process.start(sublist[0], sublist[1])
            except (IOError, OSError) as err:
                QtGui.QMessageBox.question(self, 'Error', "%s"%err)
                self.global_message.appendPlainText("=> Error: %s"%err)
                self.enable_encoding_buttons()
        else:
            self.multiple_video = False
            self.process = QtCore.QProcess(self)
            self.process.setReadChannel(QtCore.QProcess.StandardError)
            QtCore.QObject.connect(self.process, QtCore.SIGNAL("finished(int)"), self.encode_finished)
            QtCore.QObject.connect(self.process, QtCore.SIGNAL("readyRead()"), self.data_read)
            
            # input file
            arg3 = os.path.join(self.directory_path.text(), self.video_list_table.item(0,0).text())
            
            # output file
            if self.merge_info.keep_fname:
                fname = self.video_list_table.item(0,0).text()
                fname_only = fname[:fname.rfind('.')]
                self.final_video_path = os.path.join(self.setting.current_qencoder_path, fname_only)
                self.final_video_name = self.final_video_path+'.%s'%self.video_format.currentText()
            
            arg9 = self.final_video_name.rstrip()
            arg_list[input_media_pos] = arg3
            arg_list.append(arg9)
            
            self.global_message.appendPlainText(self.cmd_to_msg(arg_list))
            self.encode_job_list=[[arg_list[0], arg_list[1:]]]
            sublist = self.encode_job_list[0]
            del self.encode_job_list[0]
            
            if self.encoding_timer.isActive():
                self.encoding_timer.stop()
            else:
                self.encoding_timer.start(100, self)

            self.encoding_progress.setTextVisible(True)
            self.encoding_progress.setFormat("Encoding: %p%")
            
            self.process.started.connect(lambda: self.run_encoding.setEnabled(False))
            self.process.started.connect(lambda: self.run_vmerge.setEnabled(False))
            self.process.started.connect(lambda: self.run_amerge.setEnabled(False))
            
            try:
                self.process.start(sublist[0], sublist[1])
            except (IOError, OSError) as err:
                QtGui.QMessageBox.question(self, 'Error', "%s"%err)
                self.global_message.appendPlainText("=> Error: %s"%err)
                self.enable_encoding_buttons()
            
    def enable_encoding_buttons(self):
        self.run_encoding.setEnabled(True)
        self.run_vmerge.setEnabled(True)
        self.run_amerge.setEnabled(True)
        
    #http://stackoverflow.com/questions/9166087/move-row-up-and-down-in-pyqt4
    def move_itme_down(self):
        row = self.video_list_table.currentRow()
        column = self.video_list_table.currentColumn();
        if row < self.video_list_table.rowCount()-1:
            self.video_list_table.insertRow(row+2)
            for i in range(self.video_list_table.columnCount()):
                self.video_list_table.setItem(row+2,i,self.video_list_table.takeItem(row,i))
                self.video_list_table.setCurrentCell(row+2,column)
            self.video_list_table.removeRow(row)        

    def move_item_up(self):    
        row = self.video_list_table.currentRow()
        column = self.video_list_table.currentColumn();
        if row > 0:
            self.video_list_table.insertRow(row-1)
            for i in range(self.video_list_table.columnCount()):
                self.video_list_table.setItem(row-1,i,self.video_list_table.takeItem(row+1,i))
                self.video_list_table.setCurrentCell(row-1,column)
            self.video_list_table.removeRow(row+1)        

    def clear_videolist_table(self):
        for i in reversed(range(self.video_list_table.rowCount())):
            self.video_list_table.removeRow(i)
        self.video_list_table.setRowCount(0)

    def delete_all_item(self):
        self.clear_videolist_table()
        
    def delete_item(self): 
        row_count = self.video_list_table.rowCount()
        if row_count == 1: self.delete_all_item()
        if row_count > 1:
            column = self.video_list_table.currentColumn();
            row = self.video_list_table.currentRow()
            for i in range(self.video_list_table.columnCount()):
                self.video_list_table.setItem(row,i,self.video_list_table.takeItem(row+1,i))
                self.video_list_table.setCurrentCell(row,column)
            self.video_list_table.removeRow(row+1)
            self.video_list_table.setRowCount(row_count-1)
    
    #def choose_audio_folder(self):
    def choose_folder(self):
        cur_dir = os.getcwd() 
        folder = QtGui.QFileDialog.getExistingDirectory(None, '', cur_dir, QtGui.QFileDialog.ShowDirsOnly)

        if not folder: 
            self.audio_conv_folder = False
            return

        cur_tab = self.tabs.currentIndex()

        if self.tabs.tabText(cur_tab) == get_audiotab_text():
            self.audio_folder = folder
            self.audio_folder_path.setText(self.audio_folder)
            self.audio_conv_folder = True
            self.media_filenames =[ f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f)) is True]

            for i in range(len(self.media_filenames)):
                fpath, fname =  os.path.split(self.media_filenames[i])
                self.audio_list.addItem(QtGui.QListWidgetItem(fname))
                self.media_filenames[i] = fname
            os.chdir(fpath)
        elif self.tabs.tabText(cur_tab) == get_youtubetab_text():
            self.youtube_video_path.setText(folder)

    def execute_audio_convert(self):
        if len(self.media_filenames) == 0: return
        cur_path = self.audio_folder_path.text()
        id = self.mood_AI_button_group.checkedId()
        width = 0
        height = 0
        if id == 0:
            brate = self.mp3_bitrate_fmt.currentText().split(' ')
            tmp_path = os.path.join(cur_path, '{}kbit'.format(brate[-1]))
            if not os.path.exists(tmp_path): os.makedirs(tmp_path)
            for file in self.media_filenames:
                if file.find('.mp3') > -1:
                    old_mp3 = os.path.join(cur_path, file)
                    new_mp3 = os.path.join(tmp_path, file)
                    #cmd = "ffmpeg -y -i \"{}\" -codec:a libmp3lame {} {} \"{}\"".format(old_mp3, brate[0], brate[1], new_mp3)
                    #os.system(cmd)
                    cmd = ['ffmpeg', '-y', '-i', '%s'%old_mp3, '-c:a', 'libmp3lame', brate[0], brate[1], '%s'%new_mp3]
                    try:
                        subprocess_call(cmd)
                    except (IOError, OSError) as err:
                        QtGui.QMessageBox.question(self, 'Error', "%s"%err)
        elif id == 1:
            img_size = self.image_size.text()
            keep_width = False
            keep_height = False
            match = re.match(r'\d*[xX]\d*', img_size)
            if match:
                tmp_path = os.path.join(cur_path, img_size)
                try:
                    width, height = self.image_size.text().split('x')
                except ValueError:
                    width, height = self.image_size.text().split('X')
                width = int(width)
                height = int(height)
                self.keep_image_size_ratio.setChecked(False)
            else:
                match = re.match(r'(\d+)[%%]', img_size)
                if match:
                    self.keep_image_size_ratio.setChecked(True)
                    percent=int(match.group(1))
                    tmp_path = os.path.join(cur_path, '%s-p'%percent)
                    if percent >= 100:
                        print('Error: percent should be less than 100')
                        QtGui.QMessageBox.question(self, 'Error', 'Percent(%d) should be less than 100!'%percent, QtGui.QMessageBox.Yes)
                        return
                    percent=percent/100.0
                    self.keep_image_size_ratio.setChecked(True)
                else:
                    match = re.match(r'(\d*)([wWhH])', img_size)
                    if match:
                        edge_size = int(match.group(1))
                        edge_dir = match.group(2)
                        tmp_path = os.path.join(cur_path, img_size)
                        if edge_dir == 'w' or edge_dir == 'W':
                            keep_width = True
                            keep_height = False
                        elif edge_dir == 'h' or edge_dir == 'H':
                            keep_width = False
                            keep_height = True
                        else: 
                            print('Error: invalid resizing command: %s' %img_size)
                            QtGui.QMessageBox.question(self, 'Error', 'Invalid resizing command: %s' %img_size, QtGui.QMessageBox.Yes)
                        self.keep_image_size_ratio.setChecked(True)
                    else:
                        print('Error: invalid resizing command %s'%img_size)
                        QtGui.QMessageBox.question(self, 'Error', 'Invalid resizing command: %s' %
                        img_size, QtGui.QMessageBox.Yes)
                        return
        
            if not self.image_to_base64.isChecked() and not os.path.exists(tmp_path): 
                os.makedirs(tmp_path)

            if self.keep_image_size_ratio.isChecked():
                for file in self.media_filenames:
                    old_imgf = os.path.join(cur_path, file)
                    new_imgf = os.path.join(tmp_path, file)
                    try:
                        old_imgh = Image.open(old_imgf)
                    except IOError:
                        print('Error: %s may be neither an image file nor exist!'%old_imgf)
                        continue
                    width = old_imgh.width
                    height = old_imgh.height
                    if keep_width:
                        factor = float(edge_size / old_imgh.width)
                    elif keep_height:
                        factor = float(edge_size / old_imgh.height)
                    else:
                        factor = percent
                        
                    new_width = int(width*factor)
                    new_height = int(height*factor)
                    if self.image_to_base64.isChecked():
                        if not self.keep_image_size.isChecked():
                            width = new_width
                            height = new_height
                        self.convert_image_to_base64(old_imgh, old_imgh.format, width, height, cur_path, file)
                    else:
                        old_imgh.thumbnail((new_width, new_height))
                        old_imgh.save(new_imgf)
                    old_imgh.close()
            else:
                new_width = int(width)
                new_height = int(height)
                for file in self.media_filenames:
                    old_imgf = os.path.join(cur_path, file)
                    new_imgf = os.path.join(tmp_path, file)
                    try:
                        old_imgh = Image.open(old_imgf)
                    except IOError:
                        print('Error: %s may be neither an image file nor exist!'%old_imgf)
                        continue
                    width = old_imgh.width
                    height = old_imgh.height
                    if self.image_to_base64.isChecked():
                        if not self.keep_image_size.isChecked():
                            if new_width > width or new_height > height:
                                print('Error: new size(%dx%d) is bigger than source image(%s: %dx%d)'%
                                (new_width, new_height, file, width, height))
                                QtGui.QMessageBox.question(self, 'Error', 
                                'Error: new size(%dx%d) is bigger than source image(%s: %dx%d)'%
                                (new_width, new_height, file, width, height), QtGui.QMessageBox.Yes)
                                if old_imgh: old_imgh.close()
                                return
                            width = new_width
                            height = new_height
                        self.convert_image_to_base64(old_imgh, old_imgh.format, width, height, cur_path, file)
                    else:
                        if new_width > width or new_height > height:
                            print('Error: new size(%dx%d) is bigger than source image(%s: %dx%d)'%
                            (new_width, new_height, file, width, height))
                            QtGui.QMessageBox.question(self, 'Error', 
                            'Error: new size(%dx%d) is bigger than source image(%s: %dx%d)'%
                            (new_width, new_height, file, width, height), QtGui.QMessageBox.Yes)
                            if old_imgh: old_imgh.close()
                            return
                        old_imgh.thumbnail((new_width, new_height))
                    old_imgh.close()
        self.audio_conv_folder = False
    
    # Error cStringIO
    # http://stackoverflow.com/questions/16065694/is-it-possible-to-create-encodeb64-from-image-object
    def convert_image_to_base64(self, im, fmt, wid, hgt, path, file):
        from io import BytesIO
        import base64
        buffer = BytesIO()

        if not self.keep_image_size.isChecked():
            im.thumbnail((wid, hgt))

        #print(output, fmt)
        im.save(buffer, format=fmt)
        base64_data = buffer.getvalue()
        fn, fext = os.path.splitext(file)
        
        writer = open(os.path.join(path, '%s.txt'%fn), 'wt')
        data_url = 'data:image/%s;base64,'%fmt+base64.b64encode(base64_data).decode()
        if not writer: 
            print('File open error at convert_image_to_base64()')
            return
        else:
            writer.write(data_url)
            writer.close()
            
        if self.base64_to_html.isChecked():
            writer = open(os.path.join(path, '%s.html'%fn), 'wt')
            writer.write('<img src=\"')
            writer.write(data_url)
            writer.write('\">')
            writer.close()
                                
    def audio_tab_UI(self):
        layout = QtGui.QFormLayout()
        open_layout = QtGui.QHBoxLayout()
        conv_layout = QtGui.QGridLayout()

        audio_folder_btn = QtGui.QPushButton('Folder')
        audio_folder_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_folder_open.table)))
        audio_folder_btn.setIconSize(QtCore.QSize(16,16))
        audio_folder_btn.clicked.connect(self.choose_folder)
        audio_open_btn = QtGui.QPushButton('Open')
        audio_open_btn.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_doc.table)))
        audio_open_btn.setIconSize(QtCore.QSize(16,16))
        audio_open_btn.clicked.connect(self.open_media_file)
        open_layout.addWidget(audio_folder_btn)
        open_layout.addWidget(audio_open_btn)

        self.audio_list = QtGui.QListWidget()
        
        conv_layout.addWidget(QtGui.QLabel('Path'), 0, 0)
        self.audio_folder_path = QtGui.QLineEdit()
        self.clear_media_list = QtGui.QPushButton('Clear')
        self.clear_media_list.clicked.connect(self.delete_media_list)
        conv_layout.addWidget(self.audio_folder_path, 0, 1)
        conv_layout.addWidget(self.clear_media_list, 0, 2)
        qscale_list = [
            '-b:a 320k Ave kbit/s: 320', 
            '-q:a 0    Ave kbit/s: 245', 
            '-q:a 1    Ave kbit/s: 225', 
            '-q:a 2    Ave kbit/s: 190', 
            '-q:a 3    Ave kbit/s: 175', 
            '-q:a 4    Ave kbit/s: 165', 
            '-q:a 5    Ave kbit/s: 130', 
            '-q:a 6    Ave kbit/s: 115', 
            '-q:a 7    Ave kbit/s: 100', 
            '-q:a 8    Ave kbit/s: 85', 
            '-q:a 9    Ave kbit/s: 65', ]
        self.mp3_bitrate_fmt = QtGui.QComboBox(self)
        for x in range(len(qscale_list)):
            self.mp3_bitrate_fmt.addItem(qscale_list[x])
        
        conv_layout.addWidget(QtGui.QLabel('MP3 Bitrate'), 1,0 )
        conv_layout.addWidget(self.mp3_bitrate_fmt, 1,1)
        
        # audio and image group box
        ai_group = QtGui.QGroupBox('Media Option')
        moods = [QtGui.QRadioButton("Audio"), QtGui.QRadioButton("Image")]
        # Set a radio button to be checked by default
        moods[0].setChecked(True)   
        
        # Radio buttons usually are in a vertical layout   
        button_layout = QtGui.QHBoxLayout()
        
        # Create a button group for radio buttons: Audio / Image
        self.mood_AI_button_group = QtGui.QButtonGroup()
        
        for i in range(len(moods)):
            # Add each radio button to the button layout
            button_layout.addWidget(moods[i])
            # Add each radio button to the button group & give it an ID of i
            self.mood_AI_button_group.addButton(moods[i], i)
            # Connect each radio button to a method to run when it's clicked
            self.connect(moods[i], QtCore.SIGNAL("clicked()"), self.audioimage_radio_button_clicked)

        self.image_size = QtGui.QLineEdit('800x600')
        
        self.keep_image_size_ratio = QtGui.QCheckBox('AR')
        #button_layout.addWidget(QtGui.QLabel('Size'))
        button_layout.addWidget(self.image_size)
        button_layout.addWidget(self.keep_image_size_ratio)
        ai_group.setLayout(button_layout)
        
        base64_layout = QtGui.QHBoxLayout()
        self.image_to_base64 = QtGui.QCheckBox('Base64')
        self.keep_image_size = QtGui.QCheckBox('No Resize')
        self.base64_to_html = QtGui.QCheckBox('HTML')
        self.image_to_base64.stateChanged.connect(self.base64_encoding_state_changed)
        base64_layout.addWidget(self.image_to_base64)
        base64_layout.addWidget(self.keep_image_size)
        base64_layout.addWidget(self.base64_to_html)
        
        self.run_audio_convert = QtGui.QPushButton('Run', self)
        self.run_audio_convert.setIcon(QtGui.QIcon(QtGui.QIcon(QtGui.QPixmap(icon_run.table))))
        self.run_audio_convert.setIconSize(QtCore.QSize(48,48))
        self.run_audio_convert.clicked.connect(self.execute_audio_convert)
        
        self.audioimage_radio_button_clicked()

        layout.addRow(open_layout)
        layout.addWidget(self.audio_list)
        layout.addRow(conv_layout)
        layout.addRow(ai_group)
        layout.addRow(base64_layout)
        layout.addWidget(self.run_audio_convert)
        self.audio_tab.setLayout(layout)
        self.audio_conv_folder = False
        
    def base64_encoding_state_changed(self):
        if self.image_to_base64.isChecked():
            self.keep_image_size.setEnabled(True)
            self.base64_to_html.setEnabled(True)
        else:
            self.keep_image_size.setEnabled(False)
            self.base64_to_html.setEnabled(False)
        
    def delete_media_list(self):
        self.audio_folder_path.setText('')
        self.audio_list.clear()
        return
        
    def audioimage_radio_button_clicked(self):
        #print(self.mood_button_group.checkedId())
        #print(self.mood_button_group.checkedButton().text())
        id = self.mood_AI_button_group.checkedId()
        if id == 0:
            self.mp3_bitrate_fmt.setEnabled(True)
            self.image_size.setEnabled(False)
            self.keep_image_size_ratio.setEnabled(False)
            self.image_to_base64.setEnabled(False)
            self.keep_image_size.setEnabled(False)
            self.base64_to_html.setEnabled(False)
        elif id == 1:
            self.mp3_bitrate_fmt.setEnabled(False)
            self.image_size.setEnabled(True)
            self.keep_image_size_ratio.setEnabled(True)
            self.image_to_base64.setEnabled(True)
            self.keep_image_size.setEnabled(True)
            self.base64_to_html.setEnabled(True)
        return
        
    def timedencoding_state_changed(self):
        if self.timed_encoding.isChecked():
            self.timed_encoding_t1.setEnabled(True)
            self.timed_encoding_t2.setEnabled(True)
        else:
            self.timed_encoding_t1.setEnabled(False)
            self.timed_encoding_t2.setEnabled(False)

    def encode_tab_UI(self):
        layout = QtGui.QFormLayout()
        open_layout  = QtGui.QHBoxLayout()
        self.add_button = QtGui.QPushButton('Add', self)
        self.add_button.clicked.connect(self.add_media_file)
        self.add_button.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_file_add.table)))
        self.add_button.setIconSize(QtCore.QSize(16,16))
        self.open_button = QtGui.QPushButton('Open', self)
        self.open_button.clicked.connect(self.open_media_file)
        self.open_button.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_folder_open.table)))
        self.open_button.setIconSize(QtCore.QSize(16,16))
        open_layout.addWidget(self.open_button)
        open_layout.addWidget(self.add_button)

        self.video_list_table = QtGui.QTableWidget()
        self.video_list_table.setColumnCount(6)
        self.video_list_table.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Name"))
        self.video_list_table.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Date"))
        self.video_list_table.setHorizontalHeaderItem(2, QtGui.QTableWidgetItem("Length"))
        self.video_list_table.setHorizontalHeaderItem(3, QtGui.QTableWidgetItem("Time"))
        self.video_list_table.setHorizontalHeaderItem(4, QtGui.QTableWidgetItem("VCodec"))
        self.video_list_table.setHorizontalHeaderItem(5, QtGui.QTableWidgetItem("ACodec"))
        #self.video_list_table.setFont(QtGui.QFont( "Courier,15,-1,2,50,0,0,0,1,0"))
        #self.table.cellDoubleClicked.connect(self.double_clicked)
        
        self.move_up = QtGui.QPushButton('', self)
        self.move_up.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_arrow_up.table)))
        self.move_up.setIconSize(QtCore.QSize(16,16))
        self.connect(self.move_up, QtCore.SIGNAL('clicked()'), self.move_item_up)
         
        self.move_down = QtGui.QPushButton('', self)
        self.move_down.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_arrow_down.table)))
        self.move_down.setIconSize(QtCore.QSize(16,16))
        self.connect(self.move_down, QtCore.SIGNAL('clicked()'), self.move_itme_down)
        
        self.sort_asc = QtGui.QPushButton('', self)
        self.sort_asc.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_table_sort_asc.table)))
        self.sort_asc.setIconSize(QtCore.QSize(16,16))

        self.sort_desc = QtGui.QPushButton('', self)
        self.sort_desc.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_table_sort_desc.table)))
        self.sort_desc.setIconSize(QtCore.QSize(16,16))

        self.delete_video = QtGui.QPushButton('', self)
        self.delete_video.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_delete.table)))
        self.delete_video.setIconSize(QtCore.QSize(16,16))
        self.connect(self.delete_video, QtCore.SIGNAL('clicked()'), self.delete_item)
        
        self.delete_all = QtGui.QPushButton('', self)
        self.delete_all.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_trash.table)))
        self.delete_all.setIconSize(QtCore.QSize(16,16))
        
        self.play = QtGui.QPushButton('', self)
        self.play.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_play.table)))
        self.play.setIconSize(QtCore.QSize(16,16))
        
        self.connect(self.delete_all, QtCore.SIGNAL('clicked()'), self.delete_all_item)
        
        
        btn_layout = QtGui.QHBoxLayout()
        btn_layout.addWidget(self.move_up)
        btn_layout.addWidget(self.move_down)
        btn_layout.addWidget(self.sort_asc)
        btn_layout.addWidget(self.sort_desc)
        btn_layout.addWidget(self.delete_video)
        btn_layout.addWidget(self.delete_all)
        btn_layout.addWidget(self.play)
        
        publish_layout = QtGui.QGridLayout()
        publish_layout.addWidget(QtGui.QLabel('Path'), 0, 0)
        self.directory_path  = QtGui.QLineEdit(self)
        publish_layout.addWidget(self.directory_path, 0, 1)
        
        publish_layout.addWidget(QtGui.QLabel('Date'), 1, 0) 
        self.publish_date  = QtGui.QLineEdit(self)
        publish_layout.addWidget(self.publish_date, 1, 1)
        
        self.publish_date.setText(datetime.datetime.now().strftime("%m%d%Y"))
        
        publish_layout.addWidget(QtGui.QLabel('Title'), 2, 0) 
        self.publish_title  = QtGui.QLineEdit(self)
        publish_layout.addWidget(self.publish_title, 2, 1)

        publish_layout.addWidget(QtGui.QLabel('Bible'), 3, 0) 
        self.publish_bible  = QtGui.QLineEdit(self)
        publish_layout.addWidget(self.publish_bible, 3, 1)
        
        
        encode_option_layout = QtGui.QHBoxLayout()
        self.keep_path = QtGui.QCheckBox('Keep Path', self)
        #publish_layout.addWidget(self.keep_path, 4, 1)
        encode_option_layout.addWidget(self.keep_path)
        self.keep_path.setChecked(True)

        #self.auto_merge = QtGui.QCheckBox('Auto Merge', self)
        #self.auto_merge.setChecked(True)
        #encode_option_layout.addWidget(self.auto_merge)
        
        self.video_format = QtGui.QComboBox(self)
        for i in range(len(encopt.video_format)):
            self.video_format.addItem(encopt.video_format[i])
        self.video_format.setCurrentIndex(self.video_format.findText('mp4'))
        encode_option_layout.addWidget(self.video_format)

        self.merge_option = QtGui.QPushButton('', self)
        self.merge_option.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_merge_option.table)))
        self.merge_option.setIconSize(QtCore.QSize(16,16))
        self.merge_option.clicked.connect(self.set_merge_option)
        encode_option_layout.addWidget(self.merge_option)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_encode_advanced.table), QtGui.QIcon.Normal,QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(icon_encode_advanced_on.table), QtGui.QIcon.Normal,QtGui.QIcon.On)

        self.use_advanced = QtGui.QPushButton('', self)
        self.use_advanced.setIcon(icon)
        self.use_advanced.setIconSize(QtCore.QSize(16,16))
        self.use_advanced.setCheckable(True)
        self.use_advanced.clicked.connect(self.set_use_advanced_option)
        encode_option_layout.addWidget(self.use_advanced)
        
        self.encode_advanced = QtGui.QPushButton('', self)
        self.encode_advanced.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_advanced_codec.table)))
        self.encode_advanced.setIconSize(QtCore.QSize(16,16))
        self.encode_advanced.clicked.connect(self.set_advanced_encode_option)
        self.encode_advanced.setEnabled(False)
        encode_option_layout.addWidget(self.encode_advanced)
        
        # partial encoding
        #ffmpeg -i a.m2t -ss 00:00 -t 00:10 -vcodec mpeg4 -s 480x272 -b:v 600k -acode c mp3 -ab 96k samp.avi
        te_group = QtGui.QGroupBox('Timed Encoding (HH:MM:SS)')
        te_layout = QtGui.QHBoxLayout()
        self.timed_encoding = QtGui.QCheckBox()
        self.timed_encoding.stateChanged.connect(self.timedencoding_state_changed)
        self.timed_encoding_t1 = QtGui.QLineEdit()
        self.timed_encoding_t2 = QtGui.QLineEdit()
        self.timed_encoding_t1.setInputMask('99:99:99;-')
        self.timed_encoding_t2.setInputMask('99:99:99;-')
        font = QtGui.QFont("Courier",11,True)
        fm = QtGui.QFontMetrics(font)
        self.timed_encoding_t1.setFixedSize(fm.width("888888888"), fm.height())
        self.timed_encoding_t2.setFixedSize(fm.width("888888888"), fm.height())
        self.timed_encoding_t1.setFont(font)
        self.timed_encoding_t2.setFont(font)

        self.timed_encoding.setChecked(False)
        self.timed_encoding_t1.setEnabled(False)
        self.timed_encoding_t2.setEnabled(False)
    
        te_layout.addWidget(self.timed_encoding)
        te_layout.addWidget(QtGui.QLabel('Start'))
        te_layout.addWidget(self.timed_encoding_t1)
        te_layout.addWidget(QtGui.QLabel('End'))
        te_layout.addWidget(self.timed_encoding_t2)
        te_group.setLayout(te_layout)
        
        run_layout = QtGui.QHBoxLayout()
        self.run_encoding = QtGui.QPushButton('Run', self)
        self.run_encoding.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_run.table)))
        self.run_encoding.setIconSize(QtCore.QSize(48,48))
        self.run_encoding.clicked.connect(self.start_encode_process)
        run_layout.addWidget(self.run_encoding)
        self.run_vmerge = QtGui.QPushButton('VMerge', self)
        self.run_vmerge.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_vmerge.table)))
        self.run_vmerge.setIconSize(QtCore.QSize(48,48))
        self.run_vmerge.clicked.connect(self.execute_video_merge)
        run_layout.addWidget(self.run_vmerge)
        self.run_amerge = QtGui.QPushButton('AMerge', self)
        self.run_amerge.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_amerge.table)))
        self.run_amerge.setIconSize(QtCore.QSize(48,48))
        self.run_amerge.clicked.connect(self.execute_audio_merge)
        run_layout.addWidget(self.run_amerge)
        
        self.encoding_timer = QtCore.QBasicTimer()
        self.encoding_progress = QtGui.QProgressBar(self)
        
        layout.addRow(open_layout)
        layout.addRow(self.video_list_table)
        layout.addRow(btn_layout)
        layout.addRow(publish_layout)
        layout.addRow(encode_option_layout)
        layout.addRow(te_group)
        layout.addRow(run_layout)
        layout.addWidget(self.encoding_progress)
        self.encode_tab.setLayout(layout)
    
    def set_use_advanced_option(self, pressed):
        #source = self.sender()
        if pressed:
            self.encode_advanced.setEnabled(True)
        else: 
            self.encode_advanced.setEnabled(False)
            self.advanced_encoding_info.use = False
        return
        
    def set_advanced_encode_option(self):
        encoder_opt_dlg = QAdvancedEnocdeOption(self.advanced_encoding_info)
        
        if encoder_opt_dlg.exec_() == 1:
            self.advanced_encoding_info = encoder_opt_dlg.get_encode_option()
            self.advanced_encoding_info.use = True
            #print(self.advanced_encoding_info.option)
        else:
            self.encode_advanced.setEnabled(False)
            self.use_advanced.setChecked(False)
        
    def editvideo_tab_UI(self):
        #from icon_png.audio_option_001 import table as a1_table
        #import icon_avedit_tool
        
        form_layout = QtGui.QFormLayout()
        
        audiofile_layout = QtGui.QGridLayout()
        audiofile_label = QtGui.QLabel('A/V File')
        self.audiofile  = QtGui.QLineEdit(self)
        audiofile_button= QtGui.QPushButton('Open', self)
        audiofile_button.clicked.connect(self.chooseAudioFile)
        
        audiofile_layout.addWidget(audiofile_label, 1, 0)
        audiofile_layout.addWidget(self.audiofile, 1, 1)
        audiofile_layout.addWidget(audiofile_button, 1, 2)
        
        time_layout = QtGui.QGridLayout()
        self.start_time = QtGui.QLineEdit(self)
        self.end_time = QtGui.QLineEdit(self)
        self.start_time.setInputMask('99:99:99;-')
        self.end_time.setInputMask('99:99:99;-')
        
        font = QtGui.QFont("Courier",11,True)
        fm = QtGui.QFontMetrics(font)
        self.start_time.setFixedSize(fm.width("888888888"), fm.height())
        self.end_time.setFixedSize(fm.width("888888888"), fm.height())
        self.start_time.setFont(font)
        self.end_time.setFont(font)
        self.use_edit_time = QtGui.QCheckBox('AExt')
        self.use_edit_time.setEnabled(False)

        time_layout.addWidget(QtGui.QLabel('Start (00:00:00)'), 1, 0)
        #time_layout.addWidget(QtGui.QLabel('Start'))
        time_layout.addWidget(self.start_time, 1, 1)
        #time_layout.addWidget(QtGui.QLabel('End'))
        time_layout.addWidget(QtGui.QLabel('End (00:00:00)'), 2, 0)
        time_layout.addWidget(self.end_time, 2, 1)
        time_layout.addWidget(self.use_edit_time, 2, 2)

        output_layout = QtGui.QHBoxLayout()
        self.use_mp3_qscale = QtGui.QComboBox(self)
        self.output = QtGui.QLineEdit(self)
        self.output.setText(_output_fname)

        self.edit_av_option = QtGui.QPushButton('', self)
        self.edit_av_option.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_advanced.table)))     
        self.edit_av_option.setIconSize(QtCore.QSize(16,16))
        
        output_layout.addWidget(QtGui.QLabel('Output'))
        output_layout.addWidget(self.output)
        output_layout.addWidget(self.use_mp3_qscale) 
        output_layout.addWidget(self.edit_av_option)
        
        qscale = ['None', '-q:a 0', '-q:a 1', '-q:a 2', '-q:a 3', 
        '-q:a 4', '-q:a 5', '-q:a 6', '-q:a 7', '-q:a 8', '-q:a 9']
        for i in range(len(qscale)):
            self.use_mp3_qscale.addItem(qscale[i])
        self.use_mp3_qscale.setEnabled(False)
        
        option_layout = QtGui.QHBoxLayout()
        self.keep_source_path = QtGui.QCheckBox('Path', self)
        self.keep_source_path.setChecked(True)
        option_layout.addWidget(self.keep_source_path)
        
        self.video_edit = QtGui.QComboBox(self)
        self.media_edit_mode = ['VCut', 'ACut', 'AExt']
        for i in range(len(self.media_edit_mode)):
            self.video_edit.addItem(self.media_edit_mode[i])
        option_layout.addWidget(self.video_edit)
        self.connect(self.video_edit, QtCore.SIGNAL("currentIndexChanged(int)"), self.check_edit_video_option)
                
        acodec = ['copy']
        acodec.extend(encopt._popular_acodec)
        self.acodec_name = acodec
        self.edit_audio_codec   = QtGui.QComboBox()
        self.edit_audio_bitrate = QtGui.QComboBox()
        self.edit_audio_freq    = QtGui.QComboBox()
            
        for i in range(len(acodec)):
            self.edit_audio_codec.addItem(acodec[i])
        for i in range(1, len(encopt.audio_bitrate)):
            self.edit_audio_bitrate.addItem(encopt.audio_bitrate[i])
        for i in range(1, len(encopt.audio_freq)):
            self.edit_audio_freq.addItem(encopt.audio_freq[i])

        self.edit_audio_codec   .setEnabled(False)
        self.edit_audio_bitrate .setEnabled(False)
        self.edit_audio_freq    .setEnabled(False)
        
        self.connect(self.edit_audio_codec, QtCore.SIGNAL("currentIndexChanged(int)"), self.check_edit_audiocodec_option)
        
        option_layout.addWidget(self.edit_audio_codec)
        option_layout.addWidget(self.edit_audio_bitrate)
        option_layout.addWidget(self.edit_audio_freq)
            
        button_layout = QtGui.QHBoxLayout()
        view = QtGui.QPushButton('View', self)
        run = QtGui.QPushButton('Run', self)
        clear = QtGui.QPushButton('Clear', self)
        run.clicked.connect(self.editMediafile)
        clear.clicked.connect(self.clearMessage)
        view.clicked.connect(self.printMediaInfo)

        form_layout.addRow(audiofile_layout)
        form_layout.addRow(time_layout)
        form_layout.addRow(output_layout)
        form_layout.addRow(option_layout)

        button_layout.addWidget(run)
        button_layout.addWidget(view)
        button_layout.addWidget(clear)
        form_layout.addRow(button_layout)
        
        self.message = QtGui.QPlainTextEdit()
        # Plain Editor resize
        #http://stackoverflow.com/questions/13416000/qt-formlayout-not-expanding-qplaintextedit-vertically
        policy = self.sizePolicy()
        policy.setVerticalStretch(1)
        self.message.setSizePolicy(policy)
        form_layout.addRow(self.message)
        self.edit_video_tab.setLayout(form_layout)
        
        #https://forum.qt.io/topic/7760/solved-set-font-of-qtextedit-and-qlistwidget/9
        self.message.setFont(QtGui.QFont( "Courier,15,-1,2,50,0,0,0,1,0"))
        self.video_edit.setEnabled(False)
    
    def check_edit_audiocodec_option(self):
        acodec1 = self.edit_audio_codec.currentText()
        acodec2 = self.edit_media_info.audiocodec
        
        if acodec1 == 'wav' or acodec1 == 'aiff':
            print('check')
            pcm_opt_dlg = QSelectPMCCodec()
            if pcm_opt_dlg.exec_() == 1:
                self.pcm_codec = pcm_opt_dlg.get_pcm_codec()
                return
            else:
                self.pcm_codec = encopt._default_pcm_codec # set default pcm codec
                return

        if acodec1 =='copy':
            self.edit_audio_bitrate .setEnabled(False)
            self.edit_audio_freq    .setEnabled(False)    
            return
        else:
            self.edit_audio_bitrate .setEnabled(True)
            self.edit_audio_freq    .setEnabled(True)
            return
        
        if (acodec1 == 'copy' and acodec2 == 'mp3') or acodec1  =='mp3':
            self.use_mp3_qscale.setEnabled(True)
        else:
            self.use_mp3_qscale.setEnabled(False)
            self.use_mp3_qscale.setCurrentIndex(0)
            
    def check_edit_video_option(self):
        if self.video_edit.currentIndex() == 2:
            self.use_edit_time.setEnabled(True)
        else:
            self.use_edit_time.setEnabled(False)
        return

    def clearMessage(self):
        self.message.clear()
    
    def printMediaInfo(self):
        if self.audiofile.text() == '': return
        #if not self.edit_media_info.video: return
        self.message.appendPlainText('='*20)
        head, tail = os.path.split(self.fname)
        self.message.appendPlainText('Name   : {}'.format(tail))
        self.message.appendPlainText('Length : {}'.format(self.edit_media_info.duration))
        
        if self.edit_media_info.video:
            self.message.appendPlainText('Video  : {}'.format(self.edit_media_info.videocodec))
            self.message.appendPlainText('Size   : {}'.format(self.edit_media_info.videosize))
            self.message.appendPlainText('VBitrat: {}'.format(self.edit_media_info.vbitrate))
            self.message.appendPlainText('Fps    : {}'.format(self.edit_media_info.fps))

        self.message.appendPlainText('Audio  : {}'.format(self.edit_media_info.audiocodec))
        self.message.appendPlainText('Freq   : {}'.format(self.edit_media_info.audiofreq))
        self.message.appendPlainText('ABitrat: {}'.format(self.edit_media_info.abitrate))
        self.message.appendPlainText('='*20)
    
    def viewMediaInfo(self, path, fname):
        #if os.path.isfile(fname):
            #head, tail = os.path.split(fname)
        mfile = os.path.join(path,fname)
        minfo = os.stat(mfile)
        #msize = size(minfo.st_size)
        msize = convert_size(minfo.st_size)
        mdate = time.ctime(minfo.st_mtime)
        
        self.edit_media_info = get_mediainfo(mfile)
        self.audiofile.setText(self.fname)
        self.message.appendPlainText('------ File Info ------')
        self.message.appendPlainText('Path   : {}'.format(path))
        self.message.appendPlainText('Name   : {}'.format(fname))
        self.message.appendPlainText('Size   : {}'.format(msize))
        self.message.appendPlainText('Date   : {}'.format(mdate))
        self.message.appendPlainText('Length : {}'.format(self.edit_media_info.duration))
        
        self.edit_audio_codec   .setCurrentIndex(0)
        self.edit_audio_bitrate .setCurrentIndex(0)
        self.edit_audio_freq    .setCurrentIndex(0)
        
        self.edit_audio_codec   .setEnabled(True)
        self.edit_audio_bitrate .setEnabled(False)
        self.edit_audio_freq    .setEnabled(False)    
        
        if self.edit_media_info.video:
            self.message.appendPlainText('------ Video Info ------')
            self.message.appendPlainText('Video  : {}'.format(self.edit_media_info.videocodec))
            self.message.appendPlainText('Size   : {}'.format(self.edit_media_info.videosize))
            self.message.appendPlainText('VBitrat: {}'.format(self.edit_media_info.vbitrate))
            self.message.appendPlainText('Fps    : {}'.format(self.edit_media_info.fps))

            self.video_edit.setEnabled(True)
            self.use_edit_time.setChecked(False)
        else: 
            self.video_edit.setEnabled(True)
            self.video_edit.model().item(0).setEnabled(False)
            self.video_edit.setCurrentIndex(1)

        self.message.appendPlainText('------ Audio Info ------')
        if self.edit_media_info.audiocodec =='mp3':
            self.use_mp3_qscale.setEnabled(True)
            
        self.message.appendPlainText('Audio  : {}'.format(self.edit_media_info.audiocodec))
        self.message.appendPlainText('Freq   : {}'.format(self.edit_media_info.audiofreq))
        self.message.appendPlainText('ABitrat: {}'.format(self.edit_media_info.abitrate))
        self.message.appendPlainText('-'*24)
        #else:
            #QtGui.QMessageBox.question(self, 'Error', 'File not exist!', QtGui.QMessageBox.Yes)

    def chooseAudioFile(self):
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', filter="Video (*.mkv *.mov *.vob *.m2t *.avi *.webm *.mp4);;Audio (*.mp3 *.aac);;All files (*.*)")
        if self.fname: 
            path, fname = os.path.split(self.fname)
            self.viewMediaInfo(path, fname)
            os.chdir(path)
        #else: QtGui.QMessageBox.question(self, 'Error', 'File not exist!', QtGui.QMessageBox.Yes)
        
    def editMediafile(self):
        if self.video_edit.currentIndex() == 0:
            self.cutVideoFile()
        elif self.video_edit.currentIndex() == 1:
            #self.cutAudioFile()
            self.cutVideoFile()
        else:
            self.audioFromVideo()
    
    def checkInput(self, fname, t1, t2):
        if not fname: return False
        
        match1 = _check_time.search(t1)
        match2 = _check_time.search(t2)
        
        if not match1:
            QtGui.QMessageBox.question(self, 'Invalid Time Format', 
            'Start Time: {}'.format(t1),QtGui.QMessageBox.Yes)
            return False

        if not match2:
            QtGui.QMessageBox.question(self, 'Invalid Time Format', 
            'End Time: {}'.format(t2),QtGui.QMessageBox.Yes)
            return False
        return True

    def default_command(self):
        cmd = [ 'ffmpeg', '-y', '-i', '%s'%self.fname, '-hide_banner']
        
        if self.video_edit.currentIndex() == 0:
            cmd.extend(['-vcodec', 'copy'])
        else:
            cmd.append('-vn')

        src_acodec = self.edit_media_info.audiocodec
        qscale = self.use_mp3_qscale.currentText()
        qscale = qscale.split(' ')
        dest_acodec = self.edit_audio_codec.currentText()

        if dest_acodec == 'copy':
            if src_acodec == 'mp3' and qscale[0] != 'None':
                cmd.extend(['-c:a', 'libmp3lame', '%s'%qscale[0], '%s'%qscale[1]])
            else:
                cmd.extend(['-acodec', 'copy'])
        else:
            if (src_acodec == 'mp3' or dest_acodec == 'mp3') and qscale[0] != 'None':
                cmd.extend(['-c:a', 'libmp3lame', '%s'%qscale[0], '%s'%qscale[1]])
            else:
                #cmd.extend(['-c:a', '%s'%self.acodec_name[self.edit_audio_codec.currentIndex()]])
                if dest_acodec == 'wav' or dest_acodec == 'aiff':
                    cmd.extend(['-c:a', '%s'%self.pcm_codec])
                else:
                    cmd.extend(['-c:a', '%s'%encopt.get_acodec_from_audio_extension(self.edit_audio_codec.currentText())])
                
                cmd.extend(['-b:a', '%sk'%self.edit_audio_bitrate.currentText(), 
                '-ar', '%s'%self.edit_audio_freq.currentText()])
        return cmd
    
    def edited_file(self):
        if self.video_edit.currentIndex() == 0:
            ext = '.%s'%self.fname[self.fname.rfind('.')+1:]
        else:
            if self.edit_audio_codec.currentText().lower() == 'copy':
                ext = '.%s'%self.edit_media_info.audiocodec
            else:
                ext = '.%s'%self.edit_audio_codec.currentText()
            
        if self.keep_source_path.isChecked():
            head, tail = os.path.split(self.fname)
            output = '%s' % os.path.join(head,'%s%s'%(self.output.text(), ext))
        else:
            output = '%s' % os.path.join(self.setting.current_qencoder_path, '%s%s'%(self.output.text(), ext))
        return output
        
    # reuturn string and integer
    def add_time_info(self, cmd):
        t1 = self.start_time.text()
        t2 = self.end_time.text()
        if not self.checkInput(self.fname, t1, t2): 
            return False
        
        t1_sec = time_to_sec(t1)
        t2_sec = time_to_sec(t2)
        duration = t2_sec - t1_sec
        cmd.extend(['-ss', '%s'%t1, '-t', '%d'%duration])
    
        return cmd
        
    def audioFromVideo(self):
        cmd = self.default_command()
        if self.use_edit_time.isChecked():
            cmd = self.add_time_info(cmd)
        cmd.append(self.edited_file())
        self.message.appendPlainText(self.cmd_to_msg(cmd))
        try:
            subprocess_call(cmd)
        except (IOError, OSError) as err:
            QtGui.QMessageBox.question(self, 'Error', "%s"%err)
        self.message.appendPlainText('-'*20)
            
    def cutVideoFile(self):
        cmd = self.default_command()
        cmd = self.add_time_info(cmd)
        if not cmd: return
        cmd.append(self.edited_file())
        self.message.appendPlainText(self.cmd_to_msg(cmd))
        try:
            subprocess_call(cmd)
        except (IOError, OSError) as err:
            QtGui.QMessageBox.question(self, 'Error', "%s"%err)
        self.message.appendPlainText('-'*20)
        
    def youtube_tab_UI(self):
        layout = QtGui.QFormLayout()
        #http://stackoverflow.com/questions/17402452/how-to-get-the-checked-radiobutton-from-a-groupbox-in-pyqt
        # Create an array of radio buttons
        moods = [QtGui.QRadioButton("Single Video"), QtGui.QRadioButton("Video List")]
        
        # Set a radio button to be checked by default
        moods[0].setChecked(True)   
        
        # Radio buttons usually are in a vertical layout   
        button_layout = QtGui.QHBoxLayout()
        
        # Create a button group for radio buttons
        self.mood_button_group = QtGui.QButtonGroup()
        
        for i in range(len(moods)):
            # Add each radio button to the button layout
            button_layout.addWidget(moods[i])
            # Add each radio button to the button group & give it an ID of i
            self.mood_button_group.addButton(moods[i], i)
            # Connect each radio button to a method to run when it's clicked
            self.connect(moods[i], QtCore.SIGNAL("clicked()"), self.youtube_radio_button_clicked)
        
        # Set the layout of the group box to the button layout
        url_group = QtGui.QGroupBox('URL')
        grid = QtGui.QGridLayout()
        grid.addWidget(QtGui.QLabel('Youtube Video'), 0, 0)
        self.youtube_url = QtGui.QLineEdit()
        grid.addWidget(self.youtube_url, 0, 1)
        
        #grid.addWidget(QtGui.QLabel('Multiple Video'), 1, 0)
        #self.youtube_multiple_video = QtGui.QLineEdit()
        #grid.addWidget(self.youtube_multiple_video)
        url_group.setLayout(grid)

        self.youtube_radio_button_clicked()
        self.youtube_message = QtGui.QPlainTextEdit()

        open_layout = QtGui.QHBoxLayout()
        open_layout.addWidget(QtGui.QLabel('Save'))
        self.youtube_video_path  = QtGui.QLineEdit()
        self.youtube_video_path.setText(_youtube_download_path)
        youtube_video_path_button= QtGui.QPushButton('Folder', self)
        youtube_video_path_button.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_encode_folder_open.table)))
        youtube_video_path_button.setIconSize(QtCore.QSize(16,16))
        youtube_video_path_button.clicked.connect(self.choose_folder)
        
        save_group = QtGui.QGroupBox('Save Options')
        save_layout = QtGui.QHBoxLayout()
        self.save_mode = [QtGui.QRadioButton("V"), 
                     QtGui.QRadioButton("A"), 
                     QtGui.QRadioButton("V+A")]
        self.save_mode[0].setChecked(True)  
        self.save_button_group = QtGui.QButtonGroup()
        for i in range(len(self.save_mode)):
            #print(i)
            save_layout.addWidget(self.save_mode[i])
            self.save_button_group.addButton(self.save_mode[i], i)
            self.connect(self.save_mode[i], QtCore.SIGNAL("clicked()"), self.youtube_savemode_button_clicked)
        
        self.youtube_audio_format = QtGui.QComboBox(self)
        afmt = [ "best", "aac", "vorbis", "mp3", "m4a", "opus", "wav" ]
        for i in range(len(afmt)):
            self.youtube_audio_format.addItem(afmt[i])
            
        self.youtube_audio_quality = QtGui.QComboBox(self)
        aqul = ["0 better", "1", "2", "3", "4", "5 default", "6", "7", "8", "9 worse"]
        for i in range(len(aqul)):
            self.youtube_audio_quality.addItem(aqul[i])
                
        self.youtube_audio_format.setEnabled(False)
        save_layout.addWidget(self.youtube_audio_format)
        self.youtube_audio_quality.setEnabled(False)
        save_layout.addWidget(self.youtube_audio_quality)
        #self.check_video = QtGui.QCheckBox('Video', self)
        #self.check_audio = QtGui.QCheckBox('Audio', self)
        #self.check_save_audio_as_mp3 = QtGui.QCheckBox('Save MP3', self)
        #save_layout.addWidget(self.check_video)
        #save_layout.addWidget(self.check_audio)
        #save_layout.addWidget(self.check_save_audio_as_mp3)
        save_group.setLayout(save_layout)
        #youtube-dl --extract-audio <video URL>
        #youtube-dl --extract-audio --audio-format mp3 --prefer-ffmpeg <video URL>
        open_layout.addWidget(self.youtube_video_path)
        open_layout.addWidget(youtube_video_path_button)
        
        #dl_option = QtGui.QGroupBox('Video/Audio')
        
        downlayout = QtGui.QHBoxLayout()
        self.youtube_download = QtGui.QPushButton('Start Download')
        self.youtube_download.setIcon(QtGui.QIcon(QtGui.QPixmap(icon_youtube_download.table)))
        self.youtube_download.setIconSize(QtCore.QSize(48,48))
        self.youtube_download.clicked.connect(self.start_download)
        self.youtube_subtitle = QtGui.QCheckBox("Subtitle")
        downlayout.addWidget(self.youtube_download)
        downlayout.addWidget(self.youtube_subtitle)
        
        layout.addRow(button_layout)
        layout.addRow(url_group)
        layout.addRow(save_group)
        layout.addRow(open_layout)
        layout.addWidget(self.youtube_message)
        #layout.addWidget(self.youtube_download)
        layout.addRow(downlayout)
        self.youtube_tab.setLayout(layout)
    
    def create_youtube_options(self):
        '''
        options = {}
        options['outtmpl'] = path
        if self.save_mode[0].isChecked():
            #options['outtmpl'] = path
            options['nocheckcertificate'] = True
        elif self.save_mode[1].isChecked():
            options['postprocessors'] = [ { 'key': 'FFmpegExtractAudio', 'preferredcodec': '{}'.format(self.youtube_audio_format.currentText())}]
            options['extractaudio'] = True
            options['audioformat'] = self.youtube_audio_format.currentText()
        elif self.save_mode[2].isChecked():
            options['postprocessors'] = [ { 'key': 'FFmpegExtractAudio', 'preferredcodec': '{}'.format(self.youtube_audio_format.currentText())}]
            options['extractaudio'] = True
            options['audioformat'] = self.youtube_audio_format.currentText()
            options['outtmpl'] = path
            options['keepvideo'] = True
            options['nocheckcertificate'] = True
        '''
        options = ['youtube-dl', '--no-check-certificate']
        id = self.save_button_group.checkedId()
        if id == 1: #audio only
            #options.append("-f bestaudio")
            options.extend(['-f', 'bestaudio'])
        elif id == 2: #video + audio
            options.append("-x")
            
        if id == 2:
            fmt = self.youtube_audio_format.currentText()
            qal = self.youtube_audio_quality.currentText()
            qal = qal.split(' ')
            #options.append("--audio-format %s"%fmt)
            #options.append("--audio-quality %s"%qal[0])
            options.extend(['--audio-format', '%s'%fmt])
            options.extend(['--audio-quality', '%s'%qal[0]])
                
        if self.youtube_subtitle.isChecked():
            options.append("--write-auto-sub")

        new_path = self.youtube_video_path.text()
        if not os.path.exists(_youtube_download_path): os.makedirs(_youtube_download_path)

        if new_path == _youtube_download_path:
            save_path = os.path.join(os.getcwd(), _youtube_download_path,'%(title)s-%(id)s.%(ext)s')
        else: 
            save_path = os.path.join(new_path, '%(title)s-%(id)s.%(ext)s')
            
        #options.extend(["-o \"%s\""%save_path])
        options.extend(['-o', '\"%s\"'%save_path])
        options.append(self.youtube_url.text())

        #self.youtube_message.appendPlainText('=== Create Youtube Options')
        #self.youtube_message.appendPlainText('\n'.join(options))

        return options

    def start_download(self):
        '''
        import youparse as yp
        
        new_path = self.youtube_video_path.text()
        if not os.path.exists(_youtube_download_path): os.makedirs(_youtube_download_path)

        #if new_path is _youtube_download_path:
        if new_path == _youtube_download_path:
            save_path = os.path.join(os.getcwd(), _youtube_download_path,'%(title)s%(format)s%(ext)s')
        else: 
            save_path = os.path.join(new_path, '%(title)s%(format)s%(ext)s')
            
        option = self.create_youtube_options(save_path)
                
        id = self.mood_button_group.checkedId()
        if id == 0:
            ydl = youtube_dl.YoutubeDL(self.create_youtube_options(save_path))
            with ydl:
                ydl.download([self.youtube_url.text()])
        elif id == 1:
            video = yp.crawl(self.youtube_url.text())
            with youtube_dl.YoutubeDL(self.create_youtube_options(save_path)) as ydl:
                for url in video:
                    #print("Download: {}".format(url))
                    self.youtube_message.appendPlainText("Download ==> {}".format(url))
                    ydl.download([url])
        '''
        #cmd = ' '.join(["youtube-dl", ' '.join(self.create_youtube_options()), self.youtube_url.text()])
        #cmd = ['youtube-dl', '--no-check-certificate']
        #cmd.extend(self.create_youtube_options())
        #cmd.append(self.youtube_url.text())
        cmd = self.create_youtube_options()
        print(self.cmd_to_msg(cmd))
        #self.youtube_message.appendPlainText("=== Command\n%s"%ccmd)
        #subprocess_call(cmd)
        #os.system(cmd)
        #print(' '.join(cmd))
        
    def youtube_savemode_button_clicked(self):
        #print(self.save_button_group.checkedId())
        #print(self.save_button_group.checkedButton().text())
        id = self.save_button_group.checkedId()
        if id == 0:
            self.youtube_audio_format.setEnabled(False)
            self.youtube_audio_quality.setEnabled(False)
        elif id == 1 or id == 2:
            self.youtube_audio_format.setEnabled(True)
            self.youtube_audio_quality.setEnabled(True)
            
    def youtube_radio_button_clicked(self):
        #print(self.mood_button_group.checkedId())
        #print(self.mood_button_group.checkedButton().text())
        #id = self.mood_button_group.checkedId()
        #if id == 0:
        #    self.youtube_url.setEnabled(True)
        #    self.youtube_multiple_video.setEnabled(False)
        #elif id == 1:
        #    self.youtube_url.setEnabled(False)
        #    self.youtube_multiple_video.setEnabled(True)
        return

    def clear_global_message(self):
        self.global_message.clear()
        
    def setting_tab_UI(self):
        layout = QtGui.QVBoxLayout()
        
        clear = QtGui.QPushButton('Clear', self)
        clear.clicked.connect(self.clear_global_message)
        
        self.global_message = QtGui.QPlainTextEdit()
        layout.addWidget(clear)
        layout.addWidget(self.global_message)
        self.setting_tab.setLayout(layout)
        '''
        grid = QtGui.QGridLayout()
        grid.addWidget(QtGui.QLabel('VType'    ), 0, 0)
        grid.addWidget(QtGui.QLabel('VRes'     ), 1, 0)
        grid.addWidget(QtGui.QLabel('HRes'     ), 2, 0)
        grid.addWidget(QtGui.QLabel('VCodec'   ), 3, 0)
        grid.addWidget(QtGui.QLabel('Bitrate'  ), 4, 0)
        grid.addWidget(QtGui.QLabel('FrmRate'  ), 5, 0)
        grid.addWidget(QtGui.QLabel('ACodec'   ), 6, 0)
        grid.addWidget(QtGui.QLabel('ASample'  ), 7, 0)
        grid.addWidget(QtGui.QLabel('Mergefile'), 8, 0)
        grid.addWidget(QtGui.QLabel('MFormat'  ), 9, 0)
        grid.addWidget(QtGui.QLabel('MCmd'     ),10, 0)
        
        self.mergefile_name_edit = QtGui.QLineEdit('list.txt')
        self.encode_vres_edit = QtGui.QLineEdit('720')
        self.encode_hres_edit = QtGui.QLineEdit('1280')
        self.encode_vcodec_edit = QtGui.QLineEdit('libx264')
        self.encode_bitrate_edit = QtGui.QLineEdit('600k')
        self.encode_frmrate_edit = QtGui.QLineEdit('24')
        self.encode_acodec_edit = QtGui.QLineEdit('mp3')
        self.encode_audio_sample_edit = QtGui.QLineEdit('128k')
        self.merge_file_format_edit = QtGui.QLineEdit('%03d.%s')
        self.video_type_edit = QtGui.QLineEdit('m2t;mts')
        self.merge_command = QtGui.QLineEdit('ffmpeg -f concat -i list.txt -c copy \"{}.avi\"')
        
        grid.addWidget(self.video_type_edit         , 0, 1)
        grid.addWidget(self.encode_vres_edit        , 1, 1)
        grid.addWidget(self.encode_hres_edit        , 2, 1)
        grid.addWidget(self.encode_vcodec_edit      , 3, 1)
        grid.addWidget(self.encode_bitrate_edit     , 4, 1)
        grid.addWidget(self.encode_frmrate_edit     , 5, 1)
        grid.addWidget(self.encode_acodec_edit      , 6, 1)
        grid.addWidget(self.encode_audio_sample_edit, 7, 1)
        grid.addWidget(self.mergefile_name_edit     , 8, 1)
        grid.addWidget(self.merge_file_format_edit  , 9, 1)
        grid.addWidget(self.merge_command           ,10, 1)
        self.setting_tab.setLayout(grid)
        '''
def main():
    app = QtGui.QApplication(sys.argv)
    #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Motif'))
    #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'CDE'))
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Plastique'))
    #QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(u'Cleanlooks'))
    encoder= QEncode()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()    
