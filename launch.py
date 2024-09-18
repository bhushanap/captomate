import re
from re import T
import gradio as gr
import yaml
from demo_sub import generate_preview
from automate import generate_out
import os

params = {'video': {},'audio': {},'subs': {},'output': {}}

def extract_resolution(resolution):
    match = re.match(r'(\d+)x(\d+)', resolution)

    if match:
        resx, resy = map(int, match.groups())
        return resx, resy
    else:
        return None, None

def change_video_input(choice):
    if choice == "Upload Video/Image":
        m = gr.Markdown(value='Upload a video or image file',label='MP4 file')
        vd = gr.Dropdown(choices=["Video File","Image File"],visible=False,interactive=True,value='Video File',label='Video or Image file?')
        yt = gr.Textbox(lines=8, visible=False, placeholder='Youtube Link here...')
        res = gr.Dropdown(choices=["720x1280 [9:16]","1080x1920 [9:16]","720x720 [1:1]","1080x1080 [1:1]","720x1440 [1:2]","1080x2160 [1:2]"],visible=True,interactive=True,value='720x1280 [9:16]',label='Resolution:')
        vid = gr.File(type="filepath", visible=True, interactive=True, file_types=['.mp4','.mkv','.mov','.avi','.jpg','.png'])
        f = gr.Column(visible=True)
        return [m,vd,yt,res,vid,f]
    elif choice == "Use Demo Footage":
        m = gr.Markdown(value='Use curated demo footage from one of the games as background')
        vd = gr.Dropdown(choices=["Minecraft","Fortnite","MarioKart", "GTA V", "Miscellaneous"],visible=True,interactive=True,value='Minecraft',label='Which game?')
        yt = gr.Textbox(lines=8, visible=False, placeholder='Youtube Link here...')
        res = gr.Dropdown(choices=["720x1280 [9:16]","1080x1920 [9:16]","720x720 [1:1]","1080x1080 [1:1]","720x1440 [1:2]","1080x2160 [1:2]"],visible=True,interactive=True,value='720x1280 [9:16]',label='Resolution:')
        vid = gr.File(type="filepath", visible=False)
        f = gr.Column(visible=True)
        return [m,vd,yt,res,vid,f]
    elif choice == "Use YouTube Video":
        m = gr.Markdown(value='Use a YouTube video as a background')
        vd = gr.Dropdown(choices=["Minecraft","Subway Surfer","MarioKart"],visible=False,interactive=True)
        yt = gr.Textbox(lines=2, label='Paste a YouTube link', visible=True, placeholder='YouTube Link here...',interactive=True)
        res = gr.Dropdown(choices=["720x1280 [9:16]","1080x1920 [9:16]","720x720 [1:1]","1080x1080 [1:1]","720x1440 [1:2]","1080x2160 [1:2]"],visible=True,interactive=True,value='720x1280 [9:16]',label='Resolution:')
        vid = gr.File(type="filepath", visible=False)
        f = gr.Column(visible=True)
        return [m,vd,yt,res,vid,f]
    else:
        m = gr.Markdown(value='Use no video in the process')
        vd = gr.Dropdown(choices=["Minecraft","Subway Surfer","MarioKart"],visible=False,interactive=True)
        yt = gr.Textbox(lines=8, visible=False, placeholder='Youtube Link here...')
        res = gr.Dropdown(choices=["720x1280 [9:16]","1080x1920 [9:16]","720x720 [1:1]","1080x1080 [1:1]","720x1440 [1:2]","1080x2160 [1:2]"],visible=False,interactive=True,value='720x1280 [9:16]',label='Resolution:')
        vid = gr.File(type="filepath", visible=False)
        f = gr.Column(visible=False)
        return [m,vd,yt,res,vid,f]

def change_audio_input(choice):
    if choice == "Upload Audio":
        m = gr.Markdown(value='Upload a audio file', label='mp3, m41, wav file')
        tts = gr.Textbox(lines=8, visible=False, placeholder='Text to convert goes here...',interactive=True)
        spk = gr.Dropdown(choices=['Alice', 'Bob', 'Chloe', 'Damien'],visible=False,interactive=True,value=None,label='Speaker:')
        sample = gr.Audio(interactive=True,visible=False)
        aud = gr.Audio(type="filepath", visible=True,interactive=True, format='mp3')
        return [m,tts,spk,aud,sample]
    elif choice == "Text to Speech":
        m = gr.Markdown(value='Add text to convert to audio')
        tts = gr.Textbox(lines=8, label='Paste text in this box', visible=True, placeholder='Text to speak goes here...',interactive=True, value='Hello there. How is it going! This is a sample text to speech sentence.')
        spk = gr.Dropdown(choices=['Mark','Alice','Rick','Paula','Shawn','Brian','Trish','Jane','Carol','Sarah','Lionel','Emma','Deepak','Marie','Isaac','Vince','Amy','Zoya'],visible=True,interactive=True,value='Alice',label='Speaker:')
        sample = gr.Audio(interactive=True,visible=True,value=os.path.join('tts','samples','Alice.wav'))
        aud = gr.Audio(type="filepath", visible=False)
        return [m,tts,spk,aud,sample]
    elif choice == "Extract From Video":
        m = gr.Markdown(value='Extract audio from the uploaded video file')
        tts = gr.Textbox(lines=8, visible=False, placeholder='Text to convert goes here...')
        spk = gr.Dropdown(choices=['Alice', 'Bob', 'Chloe', 'Damien'],visible=False,interactive=True,value=None,label='Speaker:')
        sample = gr.Audio(interactive=True,visible=False)
        aud = gr.Audio(type="filepath", visible=False)
        return [m,tts,spk,aud,sample]
    else:
        m = gr.Markdown(value='Use no audio in the process')
        tts = gr.Textbox(lines=8, visible=False, placeholder='Text to convert goes here...')
        spk = gr.Dropdown(choices=['Alice', 'Bob', 'Chloe', 'Damien'],visible=False,interactive=True,value=None,label='Speaker:')
        sample = gr.Audio(interactive=True,visible=False)
        aud = gr.Audio(type="filepath", visible=False)
        return [m,tts,spk,aud,sample]

def change_subs_input(choice):
    if choice == "Extract From Audio":
        m = gr.Markdown(value='Extract subtitles from the audio')
        sub = gr.File(type="filepath", visible=False)
        c = gr.Column(visible=True)
        return [m,sub,c]
    elif choice == "Upload Subtitles":
        m = gr.Markdown(value='Upload a subtitles file')
        sub = gr.File(type="filepath", visible=True,interactive=True,file_types=['.srt'])
        c = gr.Column(visible=True)
        return [m,sub,c]
    else:
        m = gr.Markdown(value='Use no subtitles in the process')
        sub = gr.File(type="filepath", visible=False)
        c = gr.Column(visible=False)
        return [m,sub,c]

def change_sample(spk):
  if spk is None:
    return gr.Audio(interactive=True,visible=False)
  return gr.Audio(interactive=True,visible=True,value=os.path.join('tts','samples',spk+'.wav'))

def get_preview(radioV,radioA,radioS,vd,yt,res,vid,tts,spk,aud,sub,augment,font,tcolor,fontSize,outline,ocolor,osize,shadow,scolor,ssize,position,effect,words,chars,time,lines,vSpacing,effect_color,effect_outline_color,effect_scale,bright,con,sat,out):
  gpath['video'] = vid
  gpath['audio'] = aud
  gpath['subtitle'] = sub
  md = f'Running with the following parameters - Ouputs: '

  params['output']['Final Video'] = False
  params['output']['Video File'] = False
  params['output']['Audio File'] = False
  params['output']['Subtitle File'] = False
  if not out:
    md += 'None, '
  else:
    for o in out:
      params['output'][o] = True
      md += f'{o}, '

  md += f'Video: {radioV}'

  params['video']['resx'] = extract_resolution(res)[0]
  params['video']['resy'] = extract_resolution(res)[1]
  params['video']['bright'] = bright
  params['video']['con'] = con
  params['video']['sat'] = sat
  if radioV == "Upload Video/Image":
    if not vid is None:
      if vid[-3:] == 'png' or vid[-3:] == 'jpg':
        params['video']['input']=str(vid)
        md += f', Filepath: {vid}'
      elif vid[-3:] == 'mp4' or vid[-3:] == 'mkv' or vid[-3:] == 'mov' or vid[-3:] == 'avi':
        params['video']['input']=str(vid)
        md += f', Filepath: {vid}'
      # else:
      #   md = 'Video input file format is not supported. Only png, jpg, mp4, mkv, mov, avi are allowed as of now'
      #   text = gr.Markdown(value=md,visible=True)
      #   image = gr.Image(interactive=False,visible=False)
      #   return text,image
      md += f', Resolution: {res}'
    # else:
    #   md = 'Upload a video or image file'
    #   text = gr.Markdown(value=md,visible=True)
    #   image = gr.Image(interactive=False,visible=False)
    #   return text,image
  elif radioV == "Use Demo Footage":
    md += f', Game: {vd}, Resolution {res}'
    params['video']['input']='demo'
    params['video']['game']=vd
  elif radioV == "Use YouTube Video":
    md += f', Link: {yt}, Resolution: {res}'
    params['video']['input']='youtube'
    params['video']['link']=yt
  else:
    params['video']['input']=None

  md += f'. Audio: {radioA}'
  if radioA == "Upload Audio":
    if not aud is None:
      if aud[-3:] == 'mp3' or aud[-3:] == 'm4a' or aud[-3:] == 'wav':
        params['audio']['input']=str(aud)
        md += f', Filepath: {aud}'
      # else:
      #   md = 'Audio input file format is not supported. Only mp3, m4a are allowed as of now'
      #   text = gr.Markdown(value=md,visible=True)
      #   image = gr.Image(interactive=False,visible=False)
      #   return text,image
    # else:
    #   md = 'Upload an audio file'
    #   text = gr.Markdown(value=md,visible=True)
    #   image = gr.Image(interactive=False,visible=False)
    #   return text,image
  elif radioA == "Text to Speech":
    md += f', Speaker: {spk}, TTS text: {tts[:10]}...'
    params['audio']['input']='tts'
    params['audio']['spk']=spk
    params['audio']['tts']=tts
  elif radioA == "Extract From Video":
    params['audio']['input']='extract'
  else:
    params['audio']['input']=None

  md += f'. Subtitles: {radioS}'
  if radioS == "Upload Subtitles":
    if not sub is None:
      if sub[-3:] == 'srt':
        params['subs']['input']=str(sub)
        md += f', Filepath: {sub}'
    #   else:
    #     md = 'Subtitle input file format is not supported. Only srt is allowed as of now'
    #     text = gr.Markdown(value=md,visible=True)
    #     image = gr.Image(interactive=False,visible=False)
    #     return text,image
    # else:
    #   md = 'Upload a subtitle file'
    #   text = gr.Markdown(value=md,visible=True)
    #   image = gr.Image(interactive=False,visible=False)
    #   return text,image
  elif radioS == "Extract From Audio":
    params['subs']['input']='extract'
  else:
    params['subs']['input']=None
    md = 'Deselect No Subtitles in Subtitles tab for a preview'
    gr.Warning(md)
    text = gr.Markdown(value=md,visible=True)
    image = gr.Image(interactive=False,visible=False)
    video = gr.Video(interactive=False,visible=False)
    fvideo = gr.Video(interactive=False,visible=False)
    audio = gr.Audio(interactive=False,visible=False)
    subs = gr.File(interactive=False,visible=False)
    return text,image,video,fvideo,audio,subs
  

  if params['subs']['input']!=None:

    params['subs']['font'] = font
    params['subs']['fontSize'] = int(fontSize)
    params['subs']['tColor'] = (tcolor[5:] + tcolor[3:5] + tcolor[1:3]).upper()
    params['subs']['outline'] = outline
    params['subs']['oColor'] = (ocolor[5:] + ocolor[3:5] + ocolor[1:3]).upper()
    params['subs']['oSize'] = int(osize)
    params['subs']['shadow'] = shadow
    params['subs']['sColor'] = (scolor[5:] + scolor[3:5] + scolor[1:3]).upper()
    params['subs']['sSize'] = int(ssize)
    params['subs']['position'] = position
    params['subs']['effect'] = effect
    params['subs']['words'] = int(words)
    params['subs']['chars'] = int(chars)
    params['subs']['time'] = int(time)
    params['subs']['lines'] = int(lines)
    params['subs']['vSpacing'] = float(vSpacing)
    params['subs']['eColor'] = (effect_color[5:] + effect_color[3:5] + effect_color[1:3]).upper()
    params['subs']['eoColor'] = (effect_outline_color[5:] + effect_outline_color[3:5] + effect_outline_color[1:3]).upper()
    params['subs']['eScale'] = effect_scale
    md += f', Font: {font}, Fontsize: {fontSize}, Subs Color: {tcolor}'
    params['subs']['Bold'] = False
    params['subs']['Italics'] = False
    params['subs']['Underline'] = False
    params['subs']['Strikeout'] = False
    params['subs']['All Caps'] = False
    for aug in augment:
      md += f', {aug}'
      params['subs'][aug] = True
    if outline!='None':
      md += f', Outline/Box: {outline}, Outline Color: {ocolor}, Outline Size: {osize}'
    md += f', Shadow: {shadow}'
    if outline!='No Shadow':
      md += f', Shadow: Yes, Shadow Color: {scolor}, Shadow Size: {ssize}'
    md += f', Position: {position}, Effect: {effect}, Words per Line: {words}, Chars per Line: {chars}, Time per Line: {time}, Number of lines: {lines}'

  text = gr.Markdown(value=md,visible=True)
  image = gr.Image(value=os.path.join(user,'tmp','demo_sub.gif'),interactive=False,visible=False)
  video = gr.Video(interactive=False,visible=False)
  fvideo = gr.Video(interactive=False,visible=False)
  audio = gr.Audio(interactive=False,visible=False)
  subs = gr.File(interactive=False,visible=False)
  from auto_scripts import initialize
  initialize.remove_folder(user)
  initialize.make_folder(user)
  # print(params)
  params['audio']['input'] = None
  params['subs']['input'] = os.path.join('caption','subrip.srt')
  params['output']['Final Video'] = True
  params['output']['Video File'] = False
  params['output']['Audio File'] = False
  params['output']['Subtitle File'] = False
  if params['video']['input'] is None:
    params['video']['input']='demo'
    params['video']['game']=vd
  
  with open(os.path.join(user,'cfg','config.yml'), 'w') as yaml_file:
    yaml.dump(params, yaml_file, default_flow_style=False)

  print("Dictionary saved as config.yml")
  
  try:
    message = None
    fn2 = generate_out(user,gpath)
    while message != 'Done':
      message = next(fn2)
      md = message + ', ' +  md
      text = gr.Markdown(value=md,visible=True)
      image = gr.Image(interactive=False,visible=False)
      video = gr.Video(interactive=False,visible=False)
      fvideo = gr.Video(interactive=False,visible=False)
      audio = gr.Audio(interactive=False,visible=False)
      subs = gr.File(interactive=False,visible=False)
      yield text,image,video,fvideo,audio,subs
    generate_preview(user,gpath)
    text = gr.Markdown(value=md,visible=True)
    image = gr.Image(value=os.path.join(user,'tmp','demo_sub.gif'),interactive=False,visible=True)
    
  except Exception as e:
    md = f"Error: {e} " + md  
    
    gr.Warning(str(e))
    text = gr.Markdown(value=md,visible=True)
    image = gr.Image(interactive=False,visible=False)
    video = gr.Video(interactive=False,visible=False)
    fvideo = gr.Video(interactive=False,visible=False)
    audio = gr.Audio(interactive=False,visible=False)
    subs = gr.File(interactive=False,visible=False)
    
    yield text,image,video,fvideo,audio,subs
    return text,image,video,fvideo,audio,subs
  
  yield text,image,video,fvideo,audio,subs
  return text,image,video,fvideo,audio,subs


def get_generate(radioV,radioA,radioS,vd,yt,res,vid,tts,spk,aud,sub,augment,font,tcolor,fontSize,outline,ocolor,osize,shadow,scolor,ssize,position,effect,words,chars,time,lines,vSpacing,effect_color,effect_outline_color,effect_scale,bright,con,sat,out):
  gpath['video'] = vid
  gpath['audio'] = aud
  gpath['subtitle'] = sub
  md = f'Running with the following parameters - Ouputs: '

  params['output']['Final Video'] = False
  params['output']['Video File'] = False
  params['output']['Audio File'] = False
  params['output']['Subtitle File'] = False
  if not out:
    md += 'None, '
  else:
    for o in out:
      params['output'][o] = True
      md += f'{o}, '

  md += f'Video: {radioV}'

  params['video']['resx'] = extract_resolution(res)[0]
  params['video']['resy'] = extract_resolution(res)[1]
  params['video']['bright'] = bright
  params['video']['con'] = con
  params['video']['sat'] = sat
  if radioV == "Upload Video/Image":
    if not vid is None:
      if vid[-3:] == 'png' or vid[-3:] == 'jpg':
        params['video']['input']=str(vid)
        md += f', Filepath: {vid}'
      elif vid[-3:] == 'mp4' or vid[-3:] == 'mkv' or vid[-3:] == 'mov' or vid[-3:] == 'avi':
        params['video']['input']=str(vid)
        md += f', Filepath: {vid}'
      else:
        md = 'Uploaded video input file format is not supported. Only png, jpg, mp4, mkv, mov, avi are allowed as of now'
        gr.Warning(md)
        text = gr.Markdown(value=md,visible=True)
        video = gr.Video(interactive=False,visible=False)
        fvideo = gr.Video(interactive=False,visible=False)
        audio = gr.Audio(interactive=False,visible=False)
        subs = gr.File(interactive=False,visible=False)
        return text,image,video,fvideo,audio,subs
      md += f', Resolution: {res}'
    else:
      md = 'Please upload a video or image file in the video tab'
      gr.Warning(md)
      text = gr.Markdown(value=md,visible=True)
      image = gr.Image(interactive=False,visible=False)
      video = gr.Video(interactive=False,visible=False)
      fvideo = gr.Video(interactive=False,visible=False)
      audio = gr.Audio(interactive=False,visible=False)
      subs = gr.File(interactive=False,visible=False)
      return text,image,video,fvideo,audio,subs
  elif radioV == "Use Demo Footage":
    md += f', Game: {vd}, Resolution {res}'
    params['video']['input']='demo'
    params['video']['game']=vd
  elif radioV == "Use YouTube Video":
    md += f', Link: {yt}, Resolution: {res}'
    params['video']['input']='youtube'
    params['video']['link']=yt
  else:
    params['video']['input']=None

  md += f'. Audio: {radioA}'
  if radioA == "Upload Audio":
    if not aud is None:
      print(aud)
      if aud[-3:] == 'mp3' or aud[-3:] == 'm4a' or aud[-3:] == 'wav':
        params['audio']['input']=str(aud)
        md += f', Filepath: {aud}'
      else:
        md = 'Uploaded audio input file format is not supported. Only mp3, m4a, wav are allowed as of now'
        gr.Warning(md)
        text = gr.Markdown(value=md,visible=True)
        image = gr.Image(interactive=False,visible=False)
        video = gr.Video(interactive=False,visible=False)
        fvideo = gr.Video(interactive=False,visible=False)
        audio = gr.Audio(interactive=False,visible=False)
        subs = gr.File(interactive=False,visible=False)
        return text,image,video,fvideo,audio,subs
    else:
      md = 'Please upload an audio file in the audio tab'
      gr.Warning(md)
      text = gr.Markdown(value=md,visible=True)
      image = gr.Image(interactive=False,visible=False)
      video = gr.Video(interactive=False,visible=False)
      fvideo = gr.Video(interactive=False,visible=False)
      audio = gr.Audio(interactive=False,visible=False)
      subs = gr.File(interactive=False,visible=False)
      return text,image,video,fvideo,audio,subs
  elif radioA == "Text to Speech":
    if len(tts)<1:
      md = 'Text for text to speech in the audio tab cannot be empty'
      gr.Warning(md)
      text = gr.Markdown(value=md,visible=True)
      image = gr.Image(interactive=False,visible=False)
      video = gr.Video(interactive=False,visible=False)
      fvideo = gr.Video(interactive=False,visible=False)
      audio = gr.Audio(interactive=False,visible=False)
      subs = gr.File(interactive=False,visible=False)
      return text,image,video,fvideo,audio,subs
    md += f', Speaker: {spk}, TTS text: {tts[:10]}...'
    params['audio']['input']='tts'
    params['audio']['spk']=spk
    params['audio']['tts']=tts
  elif radioA == "Extract From Video":
    params['audio']['input']='extract'
  else:
    params['audio']['input']=None

  md += f'. Subtitles: {radioS}'
  if radioS == "Upload Subtitles":
    if not sub is None:
      if sub[-3:] == 'srt':
        params['subs']['input']=str(sub)
        md += f', Filepath: {sub}'
      else:
        md = 'Uploaded subtitle input file format is not supported. Only srt is allowed as of now'
        gr.Warning(md)
        text = gr.Markdown(value=md,visible=True)
        image = gr.Image(interactive=False,visible=False)
        video = gr.Video(interactive=False,visible=False)
        fvideo = gr.Video(interactive=False,visible=False)
        audio = gr.Audio(interactive=False,visible=False)
        subs = gr.File(interactive=False,visible=False)
        return text,image,video,fvideo,audio,subs
    else:
      md = 'Please upload a subtitle file in the subtitle tab'
      gr.Warning(md)
      text = gr.Markdown(value=md,visible=True)
      image = gr.Image(interactive=False,visible=False)
      video = gr.Video(interactive=False,visible=False)
      fvideo = gr.Video(interactive=False,visible=False)
      audio = gr.Audio(interactive=False,visible=False)
      subs = gr.File(interactive=False,visible=False)
      return text,image,video,fvideo,audio,subs
  elif radioS == "Extract From Audio":
    params['subs']['input']='extract'
  else:
    params['subs']['input']=None
  if params['subs']['input']!=None:

    params['subs']['font'] = font
    params['subs']['fontSize'] = int(fontSize)
    params['subs']['tColor'] = (tcolor[5:] + tcolor[3:5] + tcolor[1:3]).upper()
    params['subs']['outline'] = outline
    params['subs']['oColor'] = (ocolor[5:] + ocolor[3:5] + ocolor[1:3]).upper()
    params['subs']['oSize'] = int(osize)
    params['subs']['shadow'] = shadow
    params['subs']['sColor'] = (scolor[5:] + scolor[3:5] + scolor[1:3]).upper()
    params['subs']['sSize'] = int(ssize)
    params['subs']['position'] = position
    params['subs']['effect'] = effect
    params['subs']['words'] = int(words)
    params['subs']['chars'] = int(chars)
    params['subs']['time'] = int(time)
    params['subs']['lines'] = int(lines)
    params['subs']['vSpacing'] = float(vSpacing)
    params['subs']['eColor'] = (effect_color[5:] + effect_color[3:5] + effect_color[1:3]).upper()
    params['subs']['eoColor'] = (effect_outline_color[5:] + effect_outline_color[3:5] + effect_outline_color[1:3]).upper()
    params['subs']['eScale'] = effect_scale
    md += f', Font: {font}, Fontsize: {fontSize}, Subs Color: {tcolor}'
    params['subs']['Bold'] = False
    params['subs']['Italics'] = False
    params['subs']['Underline'] = False
    params['subs']['Strikeout'] = False
    params['subs']['All Caps'] = False
    for aug in augment:
      md += f', {aug}'
      params['subs'][aug] = True
    if outline!='None':
      md += f', Outline/Box: {outline}, Outline Color: {ocolor}, Outline Size: {osize}'
    md += f', Shadow: {shadow}'
    if outline!='No Shadow':
      md += f', Shadow: Yes, Shadow Color: {scolor}, Shadow Size: {ssize}'
    md += f', Position: {position}, Effect: {effect}, Words per Line: {words}, Chars per Line: {chars}, Time per Line: {time}, Number of lines: {lines}'

  # print(params)
  if params['audio']['input']=='tts':
    if len(params['audio']['tts']) > 1000:
      md = 'Text to Speech paragraph must be smaller than 1000 characters in length'
      gr.Warning(md)
      text = gr.Markdown(value=md,visible=True)
      image = gr.Image(interactive=False,visible=False)
      video = gr.Video(interactive=False,visible=False)
      fvideo = gr.Video(interactive=False,visible=False)
      audio = gr.Audio(interactive=False,visible=False)
      subs = gr.File(interactive=False,visible=False)
      return text,image,video,fvideo,audio,subs
  
  if params['subs']['input']=='extract' and params['audio']['input'] is None:
    md = 'Audio input in the audio tab cannot be set to "No Audio" if "Extract From Audio" is enabled in the subtitles tab'
    gr.Warning(md)
    text = gr.Markdown(value=md,visible=True)
    image = gr.Image(interactive=False,visible=False)
    video = gr.Video(interactive=False,visible=False)
    fvideo = gr.Video(interactive=False,visible=False)
    audio = gr.Audio(interactive=False,visible=False)
    subs = gr.File(interactive=False,visible=False)
    return text,image,video,fvideo,audio,subs

  if params['audio']['input']=='extract' and params['video']['input'][-3:] != 'mp4':
    md = '"Extract From Video" in the audio tab is allowed only if you use "Upload Video" in the video tab'
    gr.Warning(md)
    text = gr.Markdown(value=md,visible=True)
    image = gr.Image(interactive=False,visible=False)
    video = gr.Video(interactive=False,visible=False)
    fvideo = gr.Video(interactive=False,visible=False)
    audio = gr.Audio(interactive=False,visible=False)
    subs = gr.File(interactive=False,visible=False)
    return text,image,video,fvideo,audio,subs

  if params['subs']['input'] is None  and params['output']['Subtitle File'] == True:
    md = 'Subtitle input in the subtitles tab cannot be set to "No Subtitles" if Outputs tab has "Subtitle File" checked'
    gr.Warning(md)
    text = gr.Markdown(value=md,visible=True)
    image = gr.Image(interactive=False,visible=False)
    video = gr.Video(interactive=False,visible=False)
    fvideo = gr.Video(interactive=False,visible=False)
    audio = gr.Audio(interactive=False,visible=False)
    subs = gr.File(interactive=False,visible=False)
    return text,image,video,fvideo,audio,subs

  if params['audio']['input'] is None and params['output']['Audio File'] == True:
    md = 'Audio input in the audio tab cannot be set to "No Audio" if Outputs tab has "Audio File" checked'
    gr.Warning(md)
    text = gr.Markdown(value=md,visible=True)
    image = gr.Image(interactive=False,visible=False)
    video = gr.Video(interactive=False,visible=False)
    fvideo = gr.Video(interactive=False,visible=False)
    audio = gr.Audio(interactive=False,visible=False)
    subs = gr.File(interactive=False,visible=False)
    return text,image,video,fvideo,audio,subs

  if params['video']['input'] is None and params['output']['Video File'] == True:
    md = 'Video input in the subtitles tab cannot be set to "No Video" if Outputs tab has "Video File" checked'
    gr.Warning(md)
    text = gr.Markdown(value=md,visible=True)
    image = gr.Image(interactive=False,visible=False)
    video = gr.Video(interactive=False,visible=False)
    fvideo = gr.Video(interactive=False,visible=False)
    audio = gr.Audio(interactive=False,visible=False)
    subs = gr.File(interactive=False,visible=False)
    return text,image,video,fvideo,audio,subs

  if params['video']['input'] is None and params['output']['Final Video'] == True:
    md = 'Video input in the subtitles tab cannot be set to "No Video" if Outputs tab has "Final Video" checked'
    gr.Warning(md)
    text = gr.Markdown(value=md,visible=True)
    image = gr.Image(interactive=False,visible=False)
    video = gr.Video(interactive=False,visible=False)
    fvideo = gr.Video(interactive=False,visible=False)
    audio = gr.Audio(interactive=False,visible=False)
    subs = gr.File(interactive=False,visible=False)
    return text,image,video,fvideo,audio,subs
  # print(params)
  if params['output']['Final Video'] == False and params['output']['Video File'] == False and params['output']['Audio File'] == False and params['output']['Subtitle File'] == False:
    md = 'At least one of the outputs in the outputs tab must be checked'
    gr.Warning(md)
    text = gr.Markdown(value=md,visible=True)
    image = gr.Image(interactive=False,visible=False)
    video = gr.Video(interactive=False,visible=False)
    fvideo = gr.Video(interactive=False,visible=False)
    audio = gr.Audio(interactive=False,visible=False)
    subs = gr.File(interactive=False,visible=False)
    return text,image,video,fvideo,audio,subs
  
  


  from auto_scripts import initialize
  initialize.remove_folder(user)
  initialize.make_folder(user)
  
  with open(os.path.join(user,'cfg','config.yml'), 'w') as yaml_file:
    yaml.dump(params, yaml_file, default_flow_style=False)

  print("Dictionary saved as config.yml")
  try:
    message = None
    fn = generate_out(user,gpath)
    while message != 'Done':
      message = next(fn)
      md = message + ', ' +  md
      text = gr.Markdown(value=md,visible=True)
      image = gr.Image(interactive=False,visible=False)
      video = gr.Video(interactive=False,visible=False)
      fvideo = gr.Video(interactive=False,visible=False)
      audio = gr.Audio(interactive=False,visible=False)
      subs = gr.File(interactive=False,visible=False)
      yield text,image,video,fvideo,audio,subs
    
  except Exception as e:
    md = f"Error: {e} " + md  
    
    gr.Warning(str(e))
    text = gr.Markdown(value=md,visible=True)
    image = gr.Image(interactive=False,visible=False)
    video = gr.Video(interactive=False,visible=False)
    fvideo = gr.Video(interactive=False,visible=False)
    audio = gr.Audio(interactive=False,visible=False)
    subs = gr.File(interactive=False,visible=False)
    
    yield text,image,video,fvideo,audio,subs
    return text,image,video,fvideo,audio,subs
  

  if params['output']['Subtitle File'] == True:
    subs = gr.File(value=os.path.join(user,'tmp','subrip.srt'),interactive=False,visible=True)
  else:
    subs = gr.File(interactive=False,visible=False)

  if params['output']['Audio File'] == True:
    audio = gr.Audio(value=os.path.join(user,'tmp','audio.mp3'),interactive=False,visible=True)
  else:
    audio = gr.Audio(interactive=False,visible=False)

  if params['output']['Video File'] == True:
    video = gr.Video(value=os.path.join(user,'tmp','video.mp4'),interactive=False,visible=True)
  else:
    video = gr.Video(interactive=False,visible=False)

  if params['output']['Final Video'] == True:
    fvideo = gr.Video(value=os.path.join(user,'tmp','output.mp4'),interactive=False,visible=True)
  else:
    fvideo = gr.Video(interactive=False,visible=False)

  # print(params)

  text = gr.Markdown(value=md,visible=True)
  image = gr.Image(interactive=False,visible=False)
  yield text,image,video,fvideo,audio,subs
  return text,image,video,fvideo,audio,subs


with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
  user = 'user'
  gpath = {}
  with gr.Row():
        with gr.Column(scale=3):
          with gr.Tab('Video'):
              radioV = gr.Radio(["Use Demo Footage", "Use YouTube Video","Upload Video/Image", "No Video"],
                              label="How should the video be generated?",
                                value='Use Demo Footage')
              # box = gr.Audio(type="filepath")

              m = gr.Markdown(value='Use curated demo footage from one of the games as background')
              with gr.Row():
                vd = gr.Dropdown(choices=["Minecraft","Fortnite","MarioKart", "GTA V", "Miscellaneous"],visible=True,interactive=True,value='Minecraft',label='Which game?')
                yt = gr.Textbox(lines=8, visible=False, placeholder='Youtube Link here...')
                res = gr.Dropdown(choices=["720x1280 [9:16]","1080x1920 [9:16]","720x720 [1:1]","1080x1080 [1:1]","720x1440 [1:2]","1080x2160 [1:2]"],visible=True,interactive=True,value='720x1280 [9:16]',label='Resolution:')
              with gr.Row():
                vid = gr.File(type="filepath", visible=False)
              f = gr.Column(visible=True)
              with f:
                with gr.Column():
                  bright = gr.Slider(interactive=True,value='50',label='Brightness:', minimum=0, maximum=100, step=1,scale=2)
                  con = gr.Slider(interactive=True,value='50',label='Contrast:', minimum=0, maximum=100, step=1,scale=2)
                  sat = gr.Slider(interactive=True,value='50',label='Saturation:', minimum=0, maximum=100, step=1,scale=2)
              radioV.change(fn=change_video_input, inputs=radioV, outputs=[m,vd,yt,res,vid,f])

          with gr.Tab('Audio'):
            radioA = gr.Radio(["Text to Speech", "Upload Audio", "Extract From Video", "No Audio"],
                             label="How should the audio be generated?",
                              value='Text to Speech')
            # box = gr.Audio(type="filepath")
            m = gr.Markdown(value='Add text to convert to audio')
            spk = gr.Dropdown(choices=['Mark','Alice','Rick','Paula','Shawn','Brian','Trish','Jane','Carol','Sarah','Lionel','Emma','Deepak','Marie','Isaac','Vince','Amy','Zoya'],visible=True,interactive=True,value='Alice',label='Speaker:')
            sample = gr.Audio(interactive=True,visible=True,value=os.path.join('tts','samples','Alice.wav'))
            tts = gr.Textbox(lines=8, label='Paste text in this box', visible=True, placeholder='Text to speak goes here...',interactive=True, value='Hello there. How is it going! This is a sample text to speech sentence.')  
            aud = gr.Audio(type="filepath", visible=False)


            radioA.change(fn=change_audio_input, inputs=radioA, outputs=[m,tts,spk,aud,sample])
            spk.change(fn=change_sample,inputs=spk,outputs=sample)
          with gr.Tab('Subtitles'):
            radioS = gr.Radio(["Extract From Audio", "Upload Subtitles", "No Subtitles"],
                             label="How should the subtitles be generated?",
                              value='Extract From Audio')
            # box = gr.Audio(type="filepath")
            m = gr.Markdown(value='Extract subtitles from the audio')
            sub = gr.File(type="filepath", visible=False)
            c = gr.Column(visible=True)
            with c:
              with gr.Row():
                augment = gr.CheckboxGroup(["Bold", "Italics", "Underline", "Strikeout", "All Caps"], label="Text Augment (Might not work for all fonts)",scale=3)
              with gr.Row():
                font = gr.Dropdown(choices=['Arial', 'Comic', 'Merriweather', 'Roboto', 'Anton', 'Courgette', 'Oleo', 'Teko'],interactive=True,value='Arial',label='Font:',scale=1)
                tcolor = gr.ColorPicker(label="Text Color", interactive=True,scale=1,value='#bbbbbb')
                fontSize = gr.Slider(interactive=True,value='72',label='Font Size:', minimum=1, maximum=192, step=1,scale=2)

              with gr.Row():
                outline = gr.Dropdown(choices=["None","Outline", "Box"],value='Outline', label="Outline or Box?", interactive=True,scale=1)
                ocolor = gr.ColorPicker(label="Outline Color", interactive=True,scale=1,value='#433737')
                osize = gr.Slider(interactive=True,value='4',label='Outline Size:', minimum=1, maximum=20, step=1,scale=2)

              with gr.Row():
                shadow = gr.Dropdown(choices=["No Shadow","Shadow"],value='No Shadow', label="Shadow?", interactive=True,scale=1)
                scolor = gr.ColorPicker(label="Shadow Color", interactive=True,scale=1,value='#111111')
                ssize = gr.Slider(interactive=True,value='2',label='Shadow Size:', minimum=1, maximum=20, step=1,scale=2)

              with gr.Row():
                position = gr.Dropdown(choices=["Bottom","Midway", "Top"],value='Midway', label="Where to display the subs?", interactive=True,scale=1)
                effect = gr.Dropdown(choices=["pop", "particles"],value='pop', label="What effect to use?", interactive=True,scale=1)

              with gr.Row():
                effect_color = gr.ColorPicker(label="Effect Color", interactive=True,scale=1,value='#ffcccc')
                effect_outline_color = gr.ColorPicker(label="Effect Outline Color", interactive=True,scale=1,value='#d83803')
                effect_scale = gr.Slider(interactive=True,value='110',label='Effect Scale Factor:', minimum=50, maximum=150, step=10,scale=2)

              with gr.Row():
                words = gr.Slider(interactive=True,value='3',label='Maximum number of words in a line:', minimum=1, maximum=12, step=1,scale=1)
                chars = gr.Slider(interactive=True,value='8',label='Maximum number of characters in a line:', minimum=1, maximum=50, step=1,scale=1)
                time = gr.Slider(interactive=True,value='2',label='Next word on new line after x seconds:', minimum=1, maximum=10, step=1,scale=1)

              with gr.Row():
                vSpacing = gr.Slider(interactive=True,value='1.0',label='Vertical spacing between lines:', minimum=0, maximum=3, step=0.1,scale=1)
                lines = gr.Slider(interactive=True,value='3',label='Maximum number lines on the screen at any given time:', minimum=1, maximum=5, step=1,scale=1)

            radioS.change(fn=change_subs_input, inputs=radioS, outputs=[m,sub,c])
          with gr.Tab('Outputs'):
            out = gr.CheckboxGroup(["Final Video", "Video File", "Audio File", "Subtitle File"], label="What outputs to generate", value=['Final Video'])


        with gr.Column(scale=2):
            #some placeholder output
            with gr.Row():
              preview = gr.Button(value='Preview Subtitles',scale=2, variant='secondary')
              generate = gr.Button(value='Generate',scale=3, variant='primary')

            
            image = gr.Image(interactive=False,visible=False)
            fvideo = gr.Video(interactive=False,visible=False)
            video = gr.Video(interactive=False,visible=False)
            audio = gr.Audio(interactive=False,visible=False)
            subs = gr.File(interactive=False,visible=False)
            text = gr.Markdown(visible=False)
            

            preview.click(get_preview, inputs=[radioV,radioA,radioS,vd,yt,res,vid,tts,spk,aud,sub,augment,font,tcolor,fontSize,outline,ocolor,osize,shadow,scolor,ssize,position,effect,words,chars,time,lines,vSpacing,effect_color,effect_outline_color,effect_scale,bright,con,sat,out], outputs=[text,image,video,fvideo,audio,subs])
            generate.click(get_generate, inputs=[radioV,radioA,radioS,vd,yt,res,vid,tts,spk,aud,sub,augment,font,tcolor,fontSize,outline,ocolor,osize,shadow,scolor,ssize,position,effect,words,chars,time,lines,vSpacing,effect_color,effect_outline_color,effect_scale,bright,con,sat,out], outputs=[text,image,video,fvideo,audio,subs])
            
demo.launch(debug=True, show_error=True)



