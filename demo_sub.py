import subprocess
from auto_scripts.karaoke import convert
from auto_scripts.load_yml import load_config
from auto_scripts.modify_ass import modify_styles
from auto_scripts.upload_image import scale_image
import importlib
# import ffmpeg
import os
import shutil

def image_to_video(input_image, output_video, duration):

    # ffmpeg.input(input_image, loop=1).output(output_video, vcodec='libx264', t=duration, pix_fmt='yuv420p').run()
    ffmpeg_command = [
        'ffmpeg',
        '-loop', '1',
        '-i', input_image,
        '-c:v', 'libx264',
        '-t', str(duration),
        '-pix_fmt', 'yuv420p',
        output_video
    ]

    subprocess.run(ffmpeg_command)


def burn_subtitles(input_video, output_video, subtitle_file):
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_video,
        '-vf', f'subtitles={subtitle_file}',
        '-c:a', 'copy',
        output_video
    ]

    # Run the ffmpeg command
    subprocess.run(ffmpeg_command)
    # ffmpeg.input(input_video).output(output_video, vf=f'subtitles={subtitle_file}').run()

def video_to_image(input_video, output_image):
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_video,
        '-vf', 'fps=30,scale=360:-1:flags=lanczos',
        output_image
    ]

    subprocess.run(ffmpeg_command)
    # ffmpeg.input(input_video).output(output_image, vf='fps=30,scale=360:-1:flags=lanczos').run()

def move_subs(user):
    try:
        shutil.copy2(os.path.join('caption','subrip.srt'),os.path.join(user,'tmp','subrip.srt'))
        print('Substation demo file copied successfully')
    except PermissionError:
        print('Error: Permission denied to copy subtitle files')

def generate_preview(user,gpath):
    # print(gpath)
    # Example usage:
    # config_path = os.path.join(user,'cfg','config.yml')  # Update this path accordingly
    # config_dict = load_config(config_path)
    # effect = config_dict.get('subs', {}).get('effect', {}) != 'None'
    # if effect:
    #     effect_name = config_dict.get('subs', {}).get('effect')
    #     effect_color = config_dict.get('subs', {}).get('eColor')
    #     effect_scale = config_dict.get('subs', {}).get('eScale')
    #     effect_outline_color = config_dict.get('subs', {}).get('eoColor')
    #     effect_module = importlib.import_module(f"auto_scripts.{effect_name}")

    # input_image = os.path.join('caption','demo_bg.png')
    # if gpath['video'][-3:]=='png' or gpath['video'][-3:]=='jpg':
    #     resx = config_dict.get('video', {}).get('resx')
    #     resy = config_dict.get('video', {}).get('resy')
    #     input_image = os.path.join(user,'tmp','demo_bg.png')
    #     scale_image(gpath['video'], input_image, resx, resy)
    # output_video = os.path.join(user,'tmp','demo_sub.mp4')
    # subtitle_file = os.path.join(user,'tmp','output.ass')
    output_image = os.path.join(user,'tmp','demo_sub.gif')
    # duration = 2

    # image_to_video(input_image, output_video, duration)
    # move_subs(user)
    # primary_color = config_dict.get('subs', {}).get('tColor')
    # secondary_color = config_dict.get('subs', {}).get('secondary_color','000000')
    # outline_color = config_dict.get('subs', {}).get('oColor')
    # back_color = config_dict.get('subs', {}).get('sColor')

    # size = config_dict.get('subs', {}).get('fontSize')
    # rows = config_dict.get('subs', {}).get('lines')
    # words = config_dict.get('subs', {}).get('words')
    # chars = config_dict.get('subs', {}).get('chars')
    # time = config_dict.get('subs', {}).get('time')  
    # verticalSpacing = config_dict.get('subs', {}).get('vSpacing')
    # align = config_dict.get('subs', {}).get('position')
    # resx = config_dict.get('video', {}).get('resx')
    # resy = config_dict.get('video', {}).get('resy')
    # bold = config_dict.get('subs', {}).get('bold', 1)
    # underline = config_dict.get('subs', {}).get('underline', 0)
    # italic = config_dict.get('subs', {}).get('italic', 0)
    # strikeout = config_dict.get('subs', {}).get('strikeout', 0)
    # scalex = config_dict.get('subs', {}).get('scalex', 100)
    # scaley = config_dict.get('subs', {}).get('scaley', 100)
    # spacing = config_dict.get('subs', {}).get('spacing', 1)
    # outline = config_dict.get('subs', {}).get('oSize', 0)
    # if config_dict.get('subs', {}).get('outline', 0) == 'None':
    #     outline = 0
    # shadow = config_dict.get('subs', {}).get('sSize', 0)
    # if config_dict.get('subs', {}).get('shadow', 0) == 'No Shadow':
    #     shadow = 0
    # style = 0
    # if config_dict.get('subs', {}).get('outline', 0) == 'Outline':
    #     style = 1
    # elif config_dict.get('subs', {}).get('outline', 0) == 'Box':
    #     style = 3
    # else:
    #     style = 0
    # modify_styles(user,file_path=os.path.join('caption', 'cfg.ass'), new_name='Romaji', new_fontname='Arial', new_fontsize=str(size),
    #               new_primary_color='&H'+primary_color, new_secondary_color='&H'+secondary_color,
    #               new_outline_color='&H'+outline_color, new_back_color='&H'+back_color,
    #               new_bold=str(bold), new_italic=str(italic), new_underline=str(underline), new_strikeout=str(strikeout),
    #               new_scale_x=str(scalex), new_scale_y=str(scaley), new_spacing=str(spacing),
    #               new_angle='0', new_border_style=str(style), new_outline=str(outline), new_shadow=str(shadow),
    #               new_alignment='8', new_margin_l='10', new_margin_r='10',
    #               new_margin_v='10', new_encoding='1')
    # convert(user,size, verticalSpacing, align, resx, resy, words, chars, time, rows)
    # if effect:
    #     effect_module.overlay(user,effect_color, effect_outline_color, effect_scale)
    # else:
    #     subtitle_file = os.path.join(user,'tmp','kar.ass')
    # burn_subtitles(output_video, os.path.join(user,'tmp','demo_video.mp4'), subtitle_file)
    video_to_image(os.path.join(user,'tmp','output.mp4'), output_image)