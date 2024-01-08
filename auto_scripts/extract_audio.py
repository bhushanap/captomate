import os
import subprocess

def extract_audio(user):
    video_file = os.path.join(user, 'tmp', 'video.mp4')
    audio_file = os.path.join(user, 'tmp', 'audio.mp3')

    try:
        # Run subprocess command for audio extraction
        subprocess.run([
            'ffmpeg',
            '-i', video_file,
            '-q:a', '0',
            '-map', 'a',
            audio_file,
            '-y'
        ], check=True)

        print(f"Audio extracted successfully to: {audio_file}")
    except subprocess.CalledProcessError as e:
        raise Exception("Error extracting audio from video. Ensure that the video file is not corrupted or try a different video file. If this error persists, contact the developers.")
