import yaml

def check_conflicts(config):
    # Check for conflicts in audio settings
    audio_upload_use = config.get('audio', {}).get('upload', {}).get('use', False)
    audio_from_video_use = config.get('audio', {}).get('from_video', {}).get('use', False)
    audio_tts_use = config.get('audio', {}).get('tts', {}).get('use', False)

    if sum([audio_upload_use, audio_from_video_use, audio_tts_use]) > 1:
        raise ValueError("Only one audio use type should be true")

    # Check for conflicts in video settings
    video_uses = [
        config.get('video', {}).get('upload', {}).get('image', {}).get('use', False),
        config.get('video', {}).get('upload', {}).get('video', {}).get('use', False),
        config.get('video', {}).get('preset', {}).get('gradient', {}).get('use', False),
        config.get('video', {}).get('preset', {}).get('demo', {}).get('use', False),
        config.get('video', {}).get('preset', {}).get('youtube', {}).get('use', False),
    ]

    if sum(video_uses) > 1:
        raise ValueError("Only one video use type should be true")

    # Check for conflicts in subtitles settings
    subtitles_uses = [
        config.get('subtitles', {}).get('upload', {}).get('use', False),
        config.get('subtitles', {}).get('from_audio', {}).get('use', False),
    ]

    if sum(subtitles_uses) > 1:
        raise ValueError("Only one subtitles use type should be true")

    # Check for conflicts in other conditions (e.g., if video upload is false, then audio from video use must be false)
    if not config.get('video', {}).get('upload', {}).get('video', {}).get('use', False) and audio_from_video_use:
        raise ValueError("If video upload is false, audio from video use must be false")

    # Check subtitles conditions
    if not any([audio_upload_use, audio_from_video_use, audio_tts_use]) and not config.get('subtitles', {}).get('upload', {}).get('use', False):
        raise ValueError("If all audio uses are false, subtitles should have an uploaded file")

    # Check output conditions
    audio_output = config.get('output', {}).get('audio', False)
    subs_output = config.get('output', {}).get('subs', False)
    video_output = config.get('output', {}).get('video', False)
    final_output = config.get('output', {}).get('final', False)

    # Accessing keys properly
    print(f"Audio Uses: upload, video, tts")
    print(f"Audio Uses: {audio_upload_use}, {audio_from_video_use}, {audio_tts_use}")
    print(f"Video Uses: image, video, gradt, demoV, ytube")
    print(f"Video Uses: {video_uses}")
    print(f"Subtitles Uses: upload, audio")
    print(f"Subtitles Uses: {subtitles_uses}")
    print(f"Audio Output: {audio_output}")
    print(f"Subtitles Output: {subs_output}")
    print(f"Video Output: {video_output}")
    print(f"Final Output: {final_output}")
