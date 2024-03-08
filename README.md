# Captomate: Automated Captioning Tool <img src="https://user-images.githubusercontent.com/74038190/235294002-8aafea24-3179-45af-91d9-412ad7ff5359.gif" height="50">


NOTE: This was just a hobby project with no proper organized code structure or documentation. I am sharing it in case it might help others. I don't plan on maintaining this repository. 📝

<img src='https://github.com/bhushanap/captomate/assets/83635464/e2a6011f-7967-4bc1-8df6-51499e089fcb' width='250'>
<img src='https://github.com/bhushanap/captomate/assets/83635464/58b4a583-6ec4-4674-ae7f-6c5bf095e3e4' width='250'>
<img src='https://github.com/bhushanap/captomate/assets/83635464/da20a464-907e-437d-8c10-86c40cbddb31' width='250'>


## Use 🚀

Captomate allows you to add captions on videos. It makes tiktok style captioning videos easy. 💬

You can:
- Add captions on top of your own video files
- Use AI to generate text to speech audio
- Modify captions look as per substation alpha format

## Installation 💻

This has only been tested in Ubuntu 22.04 on amd64 CPU. You can raise an issue if you find some issues and I can try to help.
Open a terminal and in the root directory make install.sh and run.sh executable

    chmod +x run.sh
    chmod +x install.sh

After that just start the install.sh and it should create a virtual environment and auto install everything for you.

I do not have a bat file for installation on windows, so if anyone can make it, that would be awesome :)

    . install.sh

You would also need to install [FFMPEG](https://ffmpeg.org/) on your device for this software to work.

Here's how to do it for [Ubuntu](https://phoenixnap.com/kb/install-ffmpeg-ubuntu) [Windows](https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/) 🛠️

### Optional
If you want demo stock footage from youtube, check out [demo](/demo) folder
If you want different fonts for captions, install fonts from the [automate fonts](/automate_fonts) folder in your system.

## Credits 🛠️

The tool uses a [Gradio](https://www.gradio.app/) frontend. 🖥️

[PywhisperCPP](https://github.com/abdeladim-s/pywhispercpp) has been used for auto-captioning. 🤖

[Silero AI](https://github.com/snakers4/silero-models) handles the Text to Speech part. 🗣️

[Pedalboard](https://spotify.github.io/pedalboard) is for some minor audio effects. 🎶

[PyonFX](https://github.com/CoffeeStraw/PyonFX) for generating the caption effects in substation alpha. ✨

## Using the tool

    . run.sh

This should start the gradio interface.

    Running on local URL:  http://127.0.0.1:7860

    To create a public link, set `share=True` in `launch()`.

Ctrl + Click on the link or paste it in a browser. This will launch the following interface.

<img src='https://github.com/bhushanap/captomate/assets/83635464/1ae72549-b584-4e3d-9d79-aab8185936cb' height='400'>

### For the settings to be set, check the [Wiki](https://github.com/bhushanap/captomate/wiki)
