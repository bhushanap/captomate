
import re
from pyonfx import *
import subprocess
import os

def convert_to_ass(user):
    srt_save_file = os.path.join(user, 'tmp', 'subrip.srt')
    ass_file = os.path.join(user, 'tmp', 'substation.ass')

    try:
        subprocess.run(['ffmpeg', '-i', srt_save_file, '-f', 'ass', ass_file, '-y'], check=True)
        print(f"Conversion successful from SRT to ASS:")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")



def convert_to_karaoke(input_str, fontsize,fontname, verticalSpacing, align, resx, resy, group, size, time_diff, rows, caps):
    # Regular expression to extract timing and text information
    regex = r'(\d+:\d+:\d+\.\d+),(\d+:\d+:\d+\.\d+),.*?,,.*?,,(.*?)\n'
    # print(fontsize, verticalSpacing, align, resx, resy, group, size, time_diff, rows)
    # Find all matches using the regex
    matches = re.findall(regex, input_str)
    # print(matches)
    
    # Convert matches to karaoke format
    totFlag = 0
    byTime =  True
    byGroup = True
    bySize = True
    if byTime:
        totFlag+=1
    if bySize:
        totFlag+=1
    if byGroup:
        totFlag+=1
    # fontsize = 72
    # verticalSpacing = 1
    # resx = 720
    # resy = 1280
    # align = 'bot'
    # group = 3
    # size = 10
    # time_diff = 4
    # rows = 3
    prev_time = Convert.time(matches[0][0])
    prev_idx = 0
    lines = []
    words = []
    row_number = 0
    top = int(resy*0.1)
    if align=='Top':
        top = int(resy*0.1)
    elif align=='Midway':
        top = int(resy*0.4)
    elif align=='Bottom':
        top = int(resy*0.7)
    row_height = int(fontsize * 1.02 * verticalSpacing)
    # print('Row height is', row_height)
    for idx, match in enumerate(matches):
        start_time, end_time, text = match
        # print(text)
        
        etime = Convert.time(end_time)
        stime = Convert.time(start_time)
        dur = int((etime-stime)/10) #centisecond
        length = len(text)
        for word in words:
            length += len(word[0])
        nextFlag = 0
        
        if byTime and stime-time_diff*1000>prev_time:
            nextFlag+=1
        if bySize and length>size:
            nextFlag+=1
        if byGroup and idx-prev_idx>=group:
            nextFlag+=1
        if nextFlag>totFlag-2 or nextFlag>0: #and modified to or to ensure it gets triggered with any one condition
            vertical = top + (row_number%rows)*row_height
            row_number +=1
            lines.append(f'Dialogue: 3,{Convert.time(prev_time)},{start_time},Romaji,,0,0,{vertical},,' \
                        + ''.join([f'{{\\k{word[1]}}}{word[0]}' for word in words]))
            #print(words, length, idx-prev_idx, (stime-prev_time)/1000)
            prev_time = stime
            prev_idx = idx
            words = []

        # print(match, 'oooooooooooooooooooo', text)
        if text == '[BLANK_AUDIO]':
            continue
        spacing_dict = {'Arial':'  ','Comic Neue':'','Merriweather':'  ','Roboto Condensed':' ',
                         'Anton':' ','Teko':'     ','Oleo Script':'   ','Courgette':'  '}
        spacing = spacing_dict[fontname]
        if caps:
            text = text.upper()
        words.append((text + spacing, dur))
    vertical = top + (row_number%rows)*row_height
    lines.append(f'Dialogue: 3,{Convert.time(prev_time)},{end_time},Romaji,,0,0,{vertical},,' \
                        + ''.join([f'{{\\k{word[1]}}}{word[0]}' for word in words]))
    # lines.append(words)
    # print(lines)
    if rows>1:
        for idx,line in enumerate(lines):
            ahead = rows - idx%rows - 1
            if idx+ahead>=len(lines):
                ahead = len(lines)-1-idx
            lines[idx] = lines[idx][:23] + lines[idx+ahead][23:33] + lines[idx][33:]
            # ahead = rows# - idx%rows
            # if idx+ahead>=len(lines):
            #     ahead = len(lines)-1-idx
            # lines[idx] = lines[idx][:23] + lines[idx+ahead][23:33] + lines[idx][33:]
        # karaoke_lines.append(f'Dialogue: {idx+3},{start_time},{end_time},Default,,0,0,0,,' + ''.join([f'{{\\k{len(word)}}}{word}' for word in text.split()]))
    # print(lines)
    return lines

# Specify the path to your .ass file

def convert(user,fontsize,fontname, verticalSpacing, align, resx, resy, group, size, time_diff,rows, caps):
    convert_to_ass(user)
    save_path = os.path.join(user, 'tmp', 'kar.ass')

    with open(os.path.join(user, 'tmp', 'substation.ass'), 'r', encoding='utf-8') as file:
        dialogue_lines = [line.strip() for line in file if line.startswith('Dialogue:')]

    # Convert the list of lines to a single string
    dialogue_string = '\n'.join(dialogue_lines) + '\n'

    karaoke_output = convert_to_karaoke(dialogue_string,fontsize, fontname,verticalSpacing, align, resx, resy, group, size, time_diff,rows, caps)

    with open(os.path.join(user,'tmp', 'cfg.ass'), 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # print(lines)

    lines.extend(karaoke_output)

    with open(save_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))
