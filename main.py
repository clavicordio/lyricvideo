import numpy as np
from PIL import Image
import skvideo.io
import cv2
import time
import sys

from FrameFeederGif import FrameFeederGif
from LyricFileParser import LyricsParser
from TextDrawer import TextDrawer

from config_dailyjourney import *
# from config_underwatercity import *

time_start = time.time()

frame_feeder = FrameFeederGif(gif_path, scale = frame_feeder_scale, speed = frame_feeder_speed)
lyrics = LyricsParser(lyrics_path)
text_drawer = TextDrawer(font_size=font_size, outline_thickness=outline_thickness, font_path=font_path)

current_frame = 0
current_time = 0

writer = skvideo.io.FFmpegWriter(output_video_path, inputdict={
    '-r': str(fps),
},
                                 outputdict={
  '-vcodec': 'libx264',  #use the h.264 codec
  '-crf': '0',           #set the constant rate factor to 0, which is lossless
  '-preset': 'veryslow',   #the slower the better compression, in princple, try
                         #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
  '-r': str(fps),
  '-framerate': str(fps),
})

while current_time <= audio_length:
    print("Frame:" + str(current_frame))

    frame = frame_feeder.pop_frame()
    text_drawer.canvas_size = frame.size
    text_drawer.figure_out_bounding_box(lyrics.lines_list, y0=text_drawer.canvas_size[1]*global_y_offset_ratio)
    lyrics_time = lyrics.find_lyrics_time(current_time)

    img_composite = frame
    for sec_start, sec_end, lyric_line in lyrics_time:
        y_offset = text_drawer.calculate_y_shift(current_time*fps, sec_start*fps, sec_end*fps, speed=text_move_speed, offset_step=text_offset_step)
        img_text_mask = text_drawer.draw_text_with_offset_in_box(lyric_line, y_offset=y_offset, y=text_drawer.canvas_size[1]*global_y_offset_ratio)

        img_composite = Image.alpha_composite(img_composite, img_text_mask)
        print(lyric_line)

    sys.stdout.flush()

    if upscale != 1:
        img_composite = img_composite.resize((img_composite.size[0]*upscale, img_composite.size[1]*upscale), Image.NEAREST)

    arr_img = np.array(img_composite)
    writer.writeFrame(arr_img)

    if display_cv2_frame:
        cv2.imshow('frame', cv2.cvtColor(arr_img, cv2.COLOR_RGBA2BGR))
        if cv2.waitKey(16) & 0xFF == ord('q'):
            break

    current_frame += 1
    current_time = current_frame / float(fps)

writer.close()
del writer

print(f'Silent video saved to {output_video_path}')

print(f'Adding audio: {output_video_path} + {audio_path} = {output_video_path_music}')
# Add audio
import subprocess
cmd = 'ffmpeg -y -i "{}" -i "{}" -c:v copy -c:a aac -b:a 192k "{}"'.format(output_video_path, audio_path, output_video_path_music)
subprocess.run(cmd)


print('Complete in: ', time.time()-time_start, 'sec')