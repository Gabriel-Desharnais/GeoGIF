# -*- coding: utf-8 -*-
# =====================================================================
# Copyright (c) 2017 Government of Canada
# =====================================================================
import moviepy.editor as mpy
import numpy as np

def generate_animation(frames, fps = 1, **kwargs):
    # This function will generate a videoClip from a list of frame. It
    # will convert each PngImageFile from pillow into a numpy array
    
    # Convertion of the frame in a numpy array. A list of 3D array
    frames_in_np = list(map(np.array,frames))
    # Generate the videoClip
    clip = mpy.ImageSequenceClip(frames_in_np, fps=fps)
    # return the videoClip
    return clip
    
def generate_gif(clip, path = "output.gif",fps = 1,**kwargs):
    # This function generate a gif file from a videoClip.
    
    # Create the gif file
    clip.write_gif(path, fps =fps, opt="OptimizePlus", fuzz=10)
    
def generate_video(clip,path = "output.mp4",fps =1,**kwargs):
    # This function generate a video file from a videoClip.
    
    # Create the video file
    clip.write_videofile(path,threads=8,fps=24,bitrate="12000k",preset="ultrafast",ffmpeg_params=["-crf","0"])#


