'''

	FFmpeg encoder list: excluded S (subtitle)
	-------------------------------------------------------
	ffmpeg -encoders
	ffmpeg version N-83152-gf7e9275 Copyright (c) 2000-2017 the FFmpeg developers
	built with gcc 5.4.0 (GCC)
	
	Encoders:
	V..... = Video
	A..... = Audio
	S..... = Subtitle
	.F.... = Frame-level multithreading
	..S... = Slice-level multithreading
	...X.. = Codec is experimental
	....B. = Supports draw_horiz_band
	.....D = Supports direct rendering method 1
	------
	V..... a64multi             Multicolor charset for Commodore 64 (codec a64_multi)
	V..... a64multi5            Multicolor charset for Commodore 64, extended with 5th color (colram) (codec a64_multi5)
	V..... alias_pix            Alias/Wavefront PIX image
	V..... amv                  AMV Video
	V..... apng                 APNG (Animated Portable Network Graphics) image
	V..... asv1                 ASUS V1
	V..... asv2                 ASUS V2
	V..... avrp                 Avid 1:1 10-bit RGB Packer
	V..X.. avui                 Avid Meridien Uncompressed
	V..... ayuv                 Uncompressed packed MS 4:4:4:4
	V..... bmp                  BMP (Windows and OS/2 bitmap)
	V..... libxavs              libxavs Chinese AVS (Audio Video Standard) (codec cavs)
	V..... cinepak              Cinepak
	V..... cljr                 Cirrus Logic AccuPak
	V.S... vc2                  SMPTE VC-2 (codec dirac)
	V.S... dnxhd                VC3/DNxHD
	V..... dpx                  DPX (Digital Picture Exchange) image
	VFS... dvvideo              DV (Digital Video)
	V.S... ffv1                 FFmpeg video codec #1
	VF.... ffvhuff              Huffyuv FFmpeg variant
	V..... flashsv              Flash Screen Video
	V..... flashsv2             Flash Screen Video Version 2
	V..... flv                  FLV / Sorenson Spark / Sorenson H.263 (Flash Video) (codec flv1)
	V..... gif                  GIF (Graphics Interchange Format)
	V..... h261                 H.261
	V..... h263                 H.263 / H.263-1996
	V.S... h263p                H.263+ / H.263-1998 / H.263 version 2
	V..... libx264              libx264 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 (codec h264)
	V..... libx264rgb           libx264 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 RGB (codec h264)
	V..... libopenh264          OpenH264 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10(codec h264)
	V..... h264_nvenc           NVIDIA NVENC H.264 encoder (codec h264)
	V..... h264_qsv             H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 (Intel Quick Sync Video acceleration) (codec h264)
	V..... nvenc                NVIDIA NVENC H.264 encoder (codec h264)
	V..... nvenc_h264           NVIDIA NVENC H.264 encoder (codec h264)
	V..... hap                  Vidvox Hap
	V..... libx265              libx265 H.265 / HEVC (codec hevc)
	V..... nvenc_hevc           NVIDIA NVENC hevc encoder (codec hevc)
	V..... hevc_nvenc           NVIDIA NVENC hevc encoder (codec hevc)
	V..... hevc_qsv             HEVC (Intel Quick Sync Video acceleration) (codec hevc)
	VF.... huffyuv              Huffyuv / HuffYUV
	V..... jpeg2000             JPEG 2000
	VF.... libopenjpeg          OpenJPEG JPEG 2000 (codec jpeg2000)
	VF.... jpegls               JPEG-LS
	VF.... ljpeg                Lossless JPEG
	VFS... mjpeg                MJPEG (Motion JPEG)
	V.S... mpeg1video           MPEG-1 video
	V.S... mpeg2video           MPEG-2 video
	V..... mpeg2_qsv            MPEG-2 video (Intel Quick Sync Video acceleration)(codec mpeg2video)
	V.S... mpeg4                MPEG-4 part 2
	V..... libxvid              libxvidcore MPEG-4 part 2 (codec mpeg4)
	V..... msmpeg4v2            MPEG-4 part 2 Microsoft variant version 2
	V..... msmpeg4              MPEG-4 part 2 Microsoft variant version 3 (codec msmpeg4v3)
	V..... msvideo1             Microsoft Video-1
	V..... pam                  PAM (Portable AnyMap) image
	V..... pbm                  PBM (Portable BitMap) image
	V..... pcx                  PC Paintbrush PCX image
	V..... pgm                  PGM (Portable GrayMap) image
	V..... pgmyuv               PGMYUV (Portable GrayMap YUV) image
	VF.... png                  PNG (Portable Network Graphics) image
	V..... ppm                  PPM (Portable PixelMap) image
	VF.... prores               Apple ProRes
	VF.... prores_aw            Apple ProRes (codec prores)
	V.S... prores_ks            Apple ProRes (iCodec Pro) (codec prores)
	V..... qtrle                QuickTime Animation (RLE) video
	V..... r10k                 AJA Kona 10-bit RGB Codec
	V..... r210                 Uncompressed RGB 10-bit
	V..... rawvideo             raw video
	V..... roqvideo             id RoQ video (codec roq)
	V..... rv10                 RealVideo 1.0
	V..... rv20                 RealVideo 2.0
	V..... sgi                  SGI image
	V..... snow                 Snow
	V..... sunrast              Sun Rasterfile image
	V..... svq1                 Sorenson Vector Quantizer 1 / Sorenson Video 1 / SVQ1
	V..... targa                Truevision Targa image
	V..... libtheora            libtheora Theora (codec theora)
	VF.... tiff                 TIFF image
	VF.... utvideo              Ut Video
	V..... v210                 Uncompressed 4:2:2 10-bit
	V..... v308                 Uncompressed packed 4:4:4
	V..... v408                 Uncompressed packed QT 4:4:4:4
	V..... v410                 Uncompressed 4:4:4 10-bit
	V..... libvpx               libvpx VP8 (codec vp8)
	V..... libvpx-vp9           libvpx VP9 (codec vp9)
	V..... libwebp              libwebp WebP image (codec webp)
	V..... wmv1                 Windows Media Video 7
	V..... wmv2                 Windows Media Video 8
	V..... wrapped_avframe      AVFrame to AVPacket passthrough
	V..... xbm                  XBM (X BitMap) image
	V..... xface                X-face image
	V..... xwd                  XWD (X Window Dump) image
	V..... y41p                 Uncompressed YUV 4:1:1 12-bit
	V..... yuv4                 Uncompressed packed 4:2:0
	VF.... zlib                 LCL (LossLess Codec Library) ZLIB
	V..... zmbv                 Zip Motion Blocks Video
	A..... aac                  AAC (Advanced Audio Coding)
	A..... ac3                  ATSC A/52A (AC-3)
	A..... ac3_fixed            ATSC A/52A (AC-3) (codec ac3)
	A..... adpcm_adx            SEGA CRI ADX ADPCM
	A..... g722                 G.722 ADPCM (codec adpcm_g722)
	A..... g726                 G.726 ADPCM (codec adpcm_g726)
	A..... adpcm_ima_qt         ADPCM IMA QuickTime
	A..... adpcm_ima_wav        ADPCM IMA WAV
	A..... adpcm_ms             ADPCM Microsoft
	A..... adpcm_swf            ADPCM Shockwave Flash
	A..... adpcm_yamaha         ADPCM Yamaha
	A..... alac                 ALAC (Apple Lossless Audio Codec)
	A..... libopencore_amrnb    OpenCORE AMR-NB (Adaptive Multi-Rate Narrow-Band) (codec amr_nb)
	A..... libvo_amrwbenc       Android VisualOn AMR-WB (Adaptive Multi-Rate Wide-Band) (codec amr_wb)
	A..... comfortnoise         RFC 3389 comfort noise generator
	A..X.. dca                  DCA (DTS Coherent Acoustics) (codec dts)
	A..... eac3                 ATSC A/52 E-AC-3
	A..... flac                 FLAC (Free Lossless Audio Codec)
	A..... g723_1               G.723.1
	A..... libgsm               libgsm GSM (codec gsm)
	A..... libgsm_ms            libgsm GSM Microsoft variant (codec gsm_ms)
	A..... libilbc              iLBC (Internet Low Bitrate Codec) (codec ilbc)
	A..X.. mlp                  MLP (Meridian Lossless Packing)
	A..... mp2                  MP2 (MPEG audio layer 2)
	A..... mp2fixed             MP2 fixed point (MPEG audio layer 2) (codec mp2)
	A..... libtwolame           libtwolame MP2 (MPEG audio layer 2) (codec mp2)
	A..... libmp3lame           libmp3lame MP3 (MPEG audio layer 3) (codec mp3)
	A..... nellymoser           Nellymoser Asao
	A..... libopus              libopus Opus (codec opus)
	A..... pcm_alaw             PCM A-law / G.711 A-law
	A..... pcm_f32be            PCM 32-bit floating point big-endian
	A..... pcm_f32le            PCM 32-bit floating point little-endian
	A..... pcm_f64be            PCM 64-bit floating point big-endian
	A..... pcm_f64le            PCM 64-bit floating point little-endian
	A..... pcm_mulaw            PCM mu-law / G.711 mu-law
	A..... pcm_s16be            PCM signed 16-bit big-endian
	A..... pcm_s16be_planar     PCM signed 16-bit big-endian planar
	A..... pcm_s16le            PCM signed 16-bit little-endian
	A..... pcm_s16le_planar     PCM signed 16-bit little-endian planar
	A..... pcm_s24be            PCM signed 24-bit big-endian
	A..... pcm_s24daud          PCM D-Cinema audio signed 24-bit
	A..... pcm_s24le            PCM signed 24-bit little-endian
	A..... pcm_s24le_planar     PCM signed 24-bit little-endian planar
	A..... pcm_s32be            PCM signed 32-bit big-endian
	A..... pcm_s32le            PCM signed 32-bit little-endian
	A..... pcm_s32le_planar     PCM signed 32-bit little-endian planar
	A..... pcm_s64be            PCM signed 64-bit big-endian
	A..... pcm_s64le            PCM signed 64-bit little-endian
	A..... pcm_s8               PCM signed 8-bit
	A..... pcm_s8_planar        PCM signed 8-bit planar
	A..... pcm_u16be            PCM unsigned 16-bit big-endian
	A..... pcm_u16le            PCM unsigned 16-bit little-endian
	A..... pcm_u24be            PCM unsigned 24-bit big-endian
	A..... pcm_u24le            PCM unsigned 24-bit little-endian
	A..... pcm_u32be            PCM unsigned 32-bit big-endian
	A..... pcm_u32le            PCM unsigned 32-bit little-endian
	A..... pcm_u8               PCM unsigned 8-bit
	A..... real_144             RealAudio 1.0 (14.4K) (codec ra_144)
	A..... roq_dpcm             id RoQ DPCM
	A..X.. s302m                SMPTE 302M
	A..X.. sonic                Sonic
	A..X.. sonicls              Sonic lossless
	A..... libspeex             libspeex Speex (codec speex)
	A..X.. truehd               TrueHD
	A..... tta                  TTA (True Audio)
	A..X.. vorbis               Vorbis
	A..... libvorbis            libvorbis (codec vorbis)
	A..... wavpack              WavPack
	A..... libwavpack            (codec wavpack)
	A..... wmav1                Windows Media Audio 1
	A..... wmav2                Windows Media Audio 2

'''

import re
import os, subprocess, sys
import collections
import subprocess as sp
from compat import PY3, DEVNULL

default_vcodec = 0
default_acodec = 0

video_bitrate = [
	'copy',
	'200', #default
	'384',
	'512',
	'768',
	'1024',
	'1536',
	'2048',
	'3072',
	'4096',
	'8192'
]

video_resolution = [
	'copy',	        # default
	'128x96',	    # sqcif
	'176x144',	    # qcif
	'352x288',	    # cif
	'704x576',	    # 4cif
	'160x120',	    # qqvga
	'320x240',	    # qvga
	'640x480',	    # vga
	'800x600',	    # svga
	'1024x768',	    # xga
	'1600x1200',	# uxga
	'2048x1536',	# qxga
	'1280x1024',	# sxga
	'2560x2048',	# qsxga
	'5120x4096',	# hsxga
	'852x480',		# wvga
	'1366x768',		# wxga
	'1600x1024',	# wsxga
	'1920x1200',	# wuxga
	'2560x1600',	# woxga
	'3200x2048',	# wqsxga
	'3840x2400',	# wquxga
	'6400x4096',	# whsxga
	'7680x4800',	# whuxga
	'320x200',	    # cga
	'640x350',	    # ega
	'852x480',		# hd480
	'1280x720',		# hd720
	'1920x1080',	# hd1080
	'368x192',      # psp low
	'368x206',      # psp mid
	'480x272',       # psp high
	'Input'
]

video_framerate = [ 
	'Copy', 
	'30', 
	'25',
	'15', 
	'10', 
	'Input' 
]

video_aspect = [
	'copy',
	'4:3',
	'16:9'
]

# h264 == (libx264, libx264rgb)
# mpeg or mpg
# mpeg mpeg1video or mpeg2video
# aiff audio codec
video_format = [
	'avi' , # mpeg4              : libmp3lame
	'mp4' , # libx264            : aac, libmp3lame
	'm4a' , # libx264            : aac 
	'ogg' , # libtheora          : vorbis
	'mpeg', # mpeg1video         : mp2
	'mov' , # h264               : aac
	'm4v' , # h264               : aac
	'wmv' , # msmpeg4v2, msmpeg4 : wmav1, wmav2
	'3gp' , # h263               : libopencore_amrnb
	'webm', # libvpx, libvpx-vp9 : libopus
	'mkv' , # libx264            : libvorbis
	'flv' , # flv                : mp3
	'rm'  , # rv10, rv20         : ac3
	'vob' , # mpeg2video         : mp2
	'gif' , # gif                : N/A
	'mp3' , # N/A                : libmp3lame
	'mp2' , # N/A                : mp2
	'aac' , # N/A                : aac
	'ac3' , # N/A                : ac3, ac3_fixed
	'opus', # N/A                : opus
	'flac', # N/A                : flac
	'aiff', # N/A                : pcm_xxx
	'wav' , # N/A                : pcm_xxx
]

_popular_avcodec_and_ext = {
	'avi' : ['mpeg4'             , 'libmp3lame'],
	'mp4' : ['libx264'           , 'aac,libmp3lame'],
	'm4a' : ['libx264'           , 'aac'], 
	'ogg' : ['libtheora'         , 'vorbis'],
	'mpeg': ['mpeg1video'        , 'mp2'],
	'mov' : ['h264'              , 'aac'],
	'm4v' : ['h264'              , 'aac'],
	'wmv' : ['msmpeg4v2,msmpeg4' , 'wmav1,wmav2'],
	'3gp' : ['h263'              , 'libopencore_amrnb'],
	'webm': ['libvpx,libvpx-vp9' , 'libopus'],
	'mkv' : ['libx264'           , 'libvorbis'],
	'flv' : ['flv'               , 'mp3'],
	'rm'  : ['rv10,rv20'         , 'ac3'],
	'vob' : ['mpeg2video'        , 'mp2'],
	'gif' : ['gif'               , 'N/A'],
	'mp3' : ['N/A'               , 'libmp3lame'],
	'mp2' : ['N/A'               , 'mp2'],
	'aac' : ['N/A'               , 'aac'],
	'ac3' : ['N/A'               , 'ac3,ac3_fixed'],
	'opus': ['N/A'               , 'opus'],
	'flac': ['N/A'               , 'flac'],
	'aiff': ['N/A'               , 'pcm_xxx'], # pcm_s16le -> default
	'wav' : ['N/A'               , 'pcm_xxx'],
}

_default_pcm_codec = 'pcm_s16le'

_acocdec_name_from_audioext = {
	'mp3'   : 'libmp3lame'  , 
	'ogg'   : 'libvorbis'   ,
	'mp2'   : 'mp2'         ,
	'aac'   : 'aac'         ,
	'ac3'   : 'ac3'         ,
	'opus'  : 'opus'        ,
	'flac'  : 'flac'        ,
	'aiff'  : 'pmc_???'     ,
	'wav'   : 'pcm_???'     
}

_popular_acodec = list(_acocdec_name_from_audioext.keys())

def get_acodec_from_audio_extension(acodec):
	try:
		res = _acocdec_name_from_audioext[acodec]
		print(res)
	except KeyError as err:
		return err
	else:
		return res
	
audio_bitrate = [
	'copy',
	'8',
	'16',
	'32',
	'40',
	'48',
	'56',
	'64', # default
	'80',
	'96',
	'112',
	'128',
	'160',
	'192',
	'224',
	'256',
	'320'
]

audio_freq= [
	'copy',
	'8000',
	'16000',
	'22050',
	'24000',
	'32000',
	'44100',	# default
	'48000',
]

audio_channel = [
	'copy',
	'5',
	'4',
	'2',
	'1'
]

vcodec_list = ['None', 'Copy']
acodec_list = ['None', 'Copy']
vcodec_desc = ['None', 'Copy']
acodec_desc = ['None', 'Copy']

_pcm_acodec = []

_find_word = re.compile(r'(\w+)')
_find_pcm  = re.compile(r"(?<!.)pcm_")

# comment line is 10
def create_ffmpeg_enclist(skip_comment):
	cmd=['ffmpeg',  '-hide_banner', '-encoders', os.getcwd()]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	'''
	popen_params = {"stdout": DEVNULL,
                    "stderr": sp.PIPE,
                    "stdin": DEVNULL}

	if os.name == "nt":
		popen_params["creationflags"] = 0x08000000
	proc = sp.Popen(cmd, **popen_params)
	'''
	output = proc.communicate()[0]
	
	# http:#stackoverflow.com/questions/606191/convert-bytes-to-a-python-string
	output = output.decode('utf-8')
	output = output.split('\n')
	encoders = output[skip_comment:]

	for line in encoders:
		line = line.strip()
		p1 = line.find(' ')
		p2 = line.find(' ', p1+1)
		
		av = line[:p1]
		codec_name =  line[p1+1:p2]
		match = _find_word.search(line[p2+1:])

		if match:
			p3 = match.start() + p2 +1
			codec_desc =  line[p3:]
		else:
			#print('... codec list error\n    %s' % line)
			return
			
		if av[0] is 'V':
			vcodec_list.append(codec_name)
			vcodec_desc.append(codec_desc)

		elif av[0] is 'A':
			acodec_list.append(codec_name)
			acodec_desc.append(codec_desc)
			if _find_pcm.search(codec_name):
				_pcm_acodec.append(codec_name)

	return
	

if __name__ == '__main__':
	create_ffmpeg_enclist(10)