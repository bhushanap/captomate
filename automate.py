from auto_scripts import load_yml
import importlib
from auto_scripts import onVideo
import subprocess
import os
import shutil


def generate_out(user,gpath):

    

    config_path = os.path.join(user,'cfg','config.yml') # Update this path accordingly
    config_dict = load_yml.load_config(config_path)

    # print(config_dict)
    # from auto_scripts.check_conflicts import check_conflicts
    # try:
    #     check_conflicts(config_dict)
    # except ValueError as e:
    #     print(f"Error: {e}")
    #     raise Exception
    output_audio = config_dict.get('output', {}).get('Audio File')
    output_subs = config_dict.get('output', {}).get('Subtitle File')
    output_video = config_dict.get('output', {}).get('Video File')
    output_final = config_dict.get('output', {}).get('Final Video')

    if not config_dict.get('subs', {}).get('input', {}) is None:
        subtitles_upload_use = config_dict.get('subs', {}).get('input', {})[-3:] == 'srt'
    else:
        subtitles_upload_use = None
    if subtitles_upload_use:
        from auto_scripts import upload_subs
        yield "Processing subtitles file"
        try:
            if config_dict.get('subs', {}).get('input', {}) == os.path.join('caption','subrip.srt'):
                upload_subs.copy_and_rename_subs_files(user, os.path.join('caption','subrip.srt'))
            else:
                upload_subs.copy_and_rename_subs_files(user, gpath['subtitle'])
        except Exception as e:
            raise Exception(e)
        yield "Processed subtitles file"
    
    if output_final or output_audio or output_subs:
        if not config_dict.get('audio', {}).get('input', {}) is None:
            upload_audio_use = config_dict.get('audio', {}).get('input', {})[-3:] in ['mp3', 'wav', 'm4a']
        else:
            upload_audio_use = None
        if upload_audio_use:
            from auto_scripts import upload_audio
            yield 'Processing uploaded audio'
            try:
                upload_audio.copy_and_rename_mp3_files(user,gpath['audio'])
            except Exception as e:
                raise Exception(e)
            yield 'Processed uploaded audio'

        tts_use = config_dict.get('audio', {}).get('input', {}) == 'tts'
        if tts_use:
            tts_file = os.path.join(user,'tmp','tts.txt')
            tts_text = config_dict.get('audio', {}).get('tts', {})
            with open(tts_file, 'w') as file:
                file.write(tts_text)
            print(f"TTS text written to txt file")
            tts_speaker = config_dict.get('audio', {}).get('spk', {})
            from auto_scripts import tts
            yield "Generating text to speech audio"
            try:
                tts.convert(user,tts_file,tts_speaker)
            except:
                raise Exception('Something seems to have gone wrong with generating audio from text during Text to Speech process. Please try again :( \n')
            yield "Generated text to speech audio"

        

    if output_final or output_video or output_subs or output_audio:
        audio_from_video = config_dict.get('audio', {}).get('input', {}) == 'extract'
        if audio_from_video:
            if not config_dict.get('video', {}).get('input', {}) is None:
                upload_video_use = config_dict.get('video', {}).get('input', '')[-3:] in ['mp4', 'mkv', 'mov', 'avi']
            else:
                upload_video_use = None
            if upload_video_use:
                # Accessing values from the dictionary
                resx = config_dict.get('video', {}).get('resx')
                resy = config_dict.get('video', {}).get('resy')
                from auto_scripts import upload_video
                yield "Fetching video files"
                try:
                    upload_video.copy_and_rename_mp4_files(user, gpath['video'],resx, resy)
                except Exception as e:
                    raise Exception(e)
                yield "Fetched video files"

    if output_final or output_audio or output_subs:
        audio_from_video = config_dict.get('audio', {}).get('input', {}) == 'extract'
        if audio_from_video:
            if not config_dict.get('video', {}).get('input', {}) is None:
                upload_video_use = config_dict.get('video', {}).get('input', '')[-3:] in ['mp4', 'mkv', 'mov', 'avi']
            else:
                upload_video_use = None
            assert upload_video_use == audio_from_video,\
            "No video uploaded to extract audio from"
            from auto_scripts import extract_audio
            yield "Extracting audio from video"
            try:
                extract_audio.extract_audio(user)
            except Exception as e:
                raise Exception(e)
            yield "Extracted audio from video"

    if output_final or output_video:
        if not config_dict.get('video', {}).get('input', {}) is None:
            upload_image_use = config_dict.get('video', {}).get('input', '')[-3:] in ['jpg', 'png']
        else:
            upload_image_use = None
        if upload_image_use:
            audio_from_video = config_dict.get('audio', {}).get('input', {}) == 'extract'
            assert upload_image_use != audio_from_video,\
            "You want to use uploaded image for the video background and also want to extract audio from the video. Cannot extract audio from an image input"
            # Accessing values from the dictionary
            resx = config_dict.get('video', {}).get('resx')
            resy = config_dict.get('video', {}).get('resy')
            from auto_scripts import upload_image
            yield "Generating video from image"
            try:
                upload_image.img2mp4(user, gpath['video'],resx, resy)
            except Exception as e:
                raise Exception(e)
            yield "Generated video from image"

        if not audio_from_video:
            if not config_dict.get('video', {}).get('input', {}) is None:
                upload_video_use = config_dict.get('video', {}).get('input', '')[-3:] in ['mp4', 'mkv', 'mov', 'avi']
            else:
                upload_video_use = None
            if upload_video_use:
                # Accessing values from the dictionary
                resx = config_dict.get('video', {}).get('resx')
                resy = config_dict.get('video', {}).get('resy')
                from auto_scripts import upload_video
                yield "Trimming video files"
                try:
                    upload_video.trim_mp4_files(user, gpath['video'],resx, resy)
                except Exception as e:
                    raise Exception(e)
                yield "Trimmed video files"

        # if not config_dict.get('video', {}).get('input', {}) is None:
        #     upload_video_use = config_dict.get('video', {}).get('input', '')[-3:] in ['mp4', 'mkv', 'mov', 'avi']
        # else:
        #     upload_video_use = None
        # if upload_video_use:
        #     # Accessing values from the dictionary
        #     resx = config_dict.get('video', {}).get('resx')
        #     resy = config_dict.get('video', {}).get('resy')
        #     from auto_scripts import upload_video
        #     yield "Fetching video files"
        #     try:
        #         upload_video.copy_and_rename_mp4_files(user, gpath['video'],resx, resy)
        #     except Exception as e:
        #         raise Exception(e)
        #     yield "Fetched video files"
        

    # if gradient_use:
    #     gradient_function(gradient_color1, gradient_color2)

        demo_use = config_dict.get('video', {}).get('input', {}) == 'demo'
        if demo_use:
            demo_game = config_dict.get('video', {}).get('game', {})
            from auto_scripts import get_game_video
            # Accessing values from the dictionary
            resx = config_dict.get('video', {}).get('resx')
            resy = config_dict.get('video', {}).get('resy')
            yield "Generating demo game video"
            try:
                get_game_video.get_video(user,resx,resy,demo_game)
            except Exception as e:
                raise Exception(e)
            yield "Generated demo game video"

        yt_use = config_dict.get('video', {}).get('input', {}) == 'youtube'
        if yt_use:
            # start_time = config_dict.get('video', {}).get('preset', {}).get('youtube', {}).get('start_time')
            url = config_dict.get('video', {}).get('link', {})
            # Accessing values from the dictionary
            resx = config_dict.get('video', {}).get('resx')
            resy = config_dict.get('video', {}).get('resy')
            from auto_scripts import youtubeDL
            yield "Downloading youtube video"
            try:
                youtubeDL.downloadVideo(user,resx,resy,'random',url)
            except Exception as e:
                raise Exception(e)
            yield "Downloaded youtube video"


    if output_final or output_subs:
        if not config_dict.get('subs', {}).get('input', {}) is None:
            subtitles_upload_use = config_dict.get('subs', {}).get('input', {})[-3:] == 'srt'
        else:
            subtitles_upload_use = None
        subtitles_audio_use = config_dict.get('subs', {}).get('input', {}) == 'extract'
        
        if subtitles_audio_use or subtitles_upload_use:
            if subtitles_audio_use:
                from auto_scripts import caption
                yield "Generating captions"
                try:
                    caption.cc(user)
                except:
                    raise Exception('Something seems while generating captions. Please try again :( \n')
                yield "Generated captions"
                # if tts_use:
                #     from auto_scripts.fixsrt import replace_words
                #     replace_words(tts_text)


        
            effect = config_dict.get('subs', {}).get('effect', {}) != 'None'
            if effect:
                effect_name = config_dict.get('subs', {}).get('effect', {})
                effect_color = config_dict.get('subs', {}).get('eColor', {})
                effect_scale = config_dict.get('subs', {}).get('eScale', {})
                effect_outline_color = config_dict.get('subs', {}).get('eoColor', {})
                effect_module = importlib.import_module(f"auto_scripts.{effect_name}")

            primary_color = config_dict.get('subs', {}).get('tColor')
            secondary_color = config_dict.get('subs', {}).get('secondary_color','000000')
            outline_color = config_dict.get('subs', {}).get('oColor')
            back_color = config_dict.get('subs', {}).get('sColor')

            size = config_dict.get('subs', {}).get('fontSize')
            rows = config_dict.get('subs', {}).get('lines')
            words = config_dict.get('subs', {}).get('words')
            chars = config_dict.get('subs', {}).get('chars')
            time = config_dict.get('subs', {}).get('time')  
            verticalSpacing = config_dict.get('subs', {}).get('vSpacing')
            align = config_dict.get('subs', {}).get('position')
            resx = config_dict.get('video', {}).get('resx')
            resy = config_dict.get('video', {}).get('resy')
            bold = config_dict.get('subs', {}).get('Bold', 1)
            underline = config_dict.get('subs', {}).get('Underline', 0)
            italic = config_dict.get('subs', {}).get('Italics', 0)
            strikeout = config_dict.get('subs', {}).get('Strikeout', 0)
            caps = config_dict.get('subs', {}).get('All Caps', 0)
            scalex = config_dict.get('subs', {}).get('scalex', 100)
            scaley = config_dict.get('subs', {}).get('scaley', 100)
            spacing = config_dict.get('subs', {}).get('spacing', 1)
            outline = config_dict.get('subs', {}).get('oSize', 0)
            font_dict = {'Arial':'Arial','Comic':'Comic Neue','Merriweather':'Merriweather','Roboto':'Roboto Condensed',
                         'Anton':'Anton','Teko':'Teko','Oleo':'Oleo Script','Courgette':'Courgette'}
            font = font_dict[config_dict.get('subs', {}).get('font', 'Arial')]
            
            if config_dict.get('subs', {}).get('outline', 0) == 'None':
                outline = 0
            shadow = config_dict.get('subs', {}).get('sSize', 0)
            if config_dict.get('subs', {}).get('shadow', 0) == 'No Shadow':
                shadow = 0
            style = 0
            if config_dict.get('subs', {}).get('outline', 0) == 'Outline':
                style = 1
            elif config_dict.get('subs', {}).get('outline', 0) == 'Box':
                style = 3
            else:
                style = 0
            
            from auto_scripts.modify_ass import modify_styles
            yield 'Adding styles to subtitles'
            try:
                modify_styles(user,file_path=os.path.join('caption', 'cfg.ass'), new_name='Romaji', new_fontname=font, new_fontsize=str(size),
                            new_primary_color='&H'+primary_color, new_secondary_color='&H'+secondary_color,
                            new_outline_color='&H'+outline_color, new_back_color='&H'+back_color,
                            new_bold=str(bold), new_italic=str(italic), new_underline=str(underline), new_strikeout=str(strikeout),
                            new_scale_x=str(scalex), new_scale_y=str(scaley), new_spacing=str(spacing),
                            new_angle='0', new_border_style=str(style), new_outline=str(outline), new_shadow=str(shadow),
                            new_alignment='8', new_margin_l='10', new_margin_r='10',
                            new_margin_v='10', new_encoding='1',resx=resx, resy=resy)
            
                
            except:
                raise Exception('Something went wrong during setting subtitle styles. Please try again :( \n')
            yield 'Added styles to subtitles'
            from auto_scripts.karaoke import convert
            convert(user,size,font, verticalSpacing, align, resx, resy, words, chars, time, rows, caps)
            bright = config_dict.get('video', {}).get('bright')
            con = config_dict.get('video', {}).get('con')
            sat = config_dict.get('video', {}).get('sat')
            effect_module.overlay(user,effect_color, effect_outline_color, effect_scale)
            yield "Overlaying captions"
            try:
                from auto_scripts.onVideo import merge_subs
                merge_subs(user,bright,con,sat)
            except:
                raise Exception('Something went wrong when overlaying subtitles. Please try again :( \n')
            yield "Overlayed captions"

        else:
            shutil.copy(os.path.join(user,'tmp','video.mp4'), os.path.join(user,'tmp','output.mp4'))

        # else:
        #     shutil.copy(os.path.join(user,'tmp','video.mp4'), os.path.join(user,'tmp','output.mp4'))
    # if output_final:
    #     shutil.copy(os.path.join('tmp','output.mp4'), 'output/output.mp4')

    # if output_subs:
    #     shutil.copy('tmp/subrip.srt', 'output/subrip.srt')

    # if output_audio:
    #     shutil.copy('tmp/audio.mp3', 'output/audio.mp3')

    # if output_video:
    #     shutil.copy('tmp/video.mp4', 'output/video.mp4')

    yield 'Done'
        



    
