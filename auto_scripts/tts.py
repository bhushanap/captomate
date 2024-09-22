
# V3
import os
import torch
import subprocess
import random
import re
import inflect
from pedalboard import HighpassFilter, HighShelfFilter, LowShelfFilter, Reverb, Pedalboard
from pedalboard.io import AudioFile
# Don't do import *! (It just makes this example smaller)


def convert_numbers_to_words(path):
    # Create an inflect engine
    with open(path, 'r', encoding='utf-8') as file:
        input_string = file.read()
    p = inflect.engine()

    # Use regular expression to find all numbers in the string
    numbers = re.findall(r'\d+', input_string)

    # Replace each number with its word representation
    for num in numbers:
        words = p.number_to_words(num)
        input_string = re.sub(r'\b' + num + r'\b', words, input_string)

    return input_string

def convert(user,path,speaker):
    example_text = convert_numbers_to_words(path)

    device = torch.device('cpu')
    torch.set_num_threads(1)
    local_file = os.path.join(os.path.dirname(__file__), '..', 'tts', 'model.pt')

    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file('https://models.silero.ai/models/tts/en/v3_en.pt',
                                    local_file)  

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)

    # example_text = 'Automating your videos has never been this easy. You can choose between multiple male and female speakers for your videos.'
    sample_rate = 48000
    speaker_dict = {
    'Mark': 'en_13',
    'Alice': 'en_14',
    'Rick': 'en_19',
    'Paula': 'en_26',
    'Shawn': 'en_30',
    'Brian': 'en_31',
    'Trish': 'en_33',
    'Jane': 'en_41',
    'Carol': 'en_48',
    'Sarah': 'en_56',
    'Lionel': 'en_70',
    'Emma': 'en_76',
    'Deepak': 'en_78',
    'Marie': 'en_98',
    'Isaac': 'en_100',
    'Vince': 'en_113',
    'Amy': 'en_116',
    'Zoya': 'en_117'
}
    if speaker=='random':
        speaker=f'{list(speaker_dict.values())[random.randint(0,17)]}'
    else:
        speaker=speaker_dict[speaker]
        

    audio_paths = model.save_wav(ssml_text = f'<speak><break time="1s"/>{example_text}<break time="1s"/></speak>',
                                speaker=speaker,
                                sample_rate=sample_rate,
                                audio_path=os.path.join(os.path.dirname(__file__), '..', user,'tmp','tts.wav'))
    
    with AudioFile(os.path.join(os.path.dirname(__file__), '..', user,'tmp','tts.wav')).resampled_to(sample_rate) as f:
        audio = f.read(f.frames)

    # Make a pretty interesting sounding guitar pedalboard:
    board = Pedalboard([
        HighShelfFilter(cutoff_frequency_hz = 5000, gain_db = 9.0, q = 0.7071067690849304),
        LowShelfFilter(cutoff_frequency_hz = 100, gain_db = 9.0, q = 0.7071067690849304),
        HighpassFilter(cutoff_frequency_hz = 100),
        HighpassFilter(cutoff_frequency_hz = 100),
        Reverb(room_size = 0.65, damping = 0.99, wet_level = 0.08, dry_level = 0.9, width = 0.5, freeze_mode = 0.0)
    ])

    # Run the audio through this pedalboard!
    effected = board(audio, sample_rate)

    # Write the audio back as a wav file:
    with AudioFile(os.path.join(os.path.dirname(__file__), '..', user,'tmp','audio.mp3'), 'w', sample_rate, effected.shape[0]) as f:
        f.write(effected)
    # try:
    #     subprocess.run(['ffmpeg', '-i', 'test.wav', '-codec:a', 'libmp3lame', '-qscale:a', '2', 'tmp/audio.mp3'])
    #     subprocess.run(["rm", '-rf', 'test.wav'])
    #     print(f"Wav to Mp3 Conversion successful")
    # except subprocess.CalledProcessError as e:
    #     print(f"Error during conversion: {e}")