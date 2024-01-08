"""
And here we are with our first complete effect.
As you can see, we have now filled our romaji, kanji and sub functions.

Starting from the simple one, the sub function make use of leadin and leadout times for fitting line-to-line changes.
We then construct the text of each line, giving an alignment, a position and a fad to make a soft entrance and exit.
    (Docs: https://pyonfx.readthedocs.io/en/latest/reference/ass%20core.html#pyonfx.ass_core.Line.leadin)

In the romaji function instead, we want to create an effect that works with syllables.
In order to do do that, every syllable has to be one dialog line,
so we loop through syllable entries of current line.
Using a utility provided in Utils module, all_non_empty(), we assure
that we will not work with blank syllables or syls with duration equals to zero.
    (Docs: https://pyonfx.readthedocs.io/en/latest/reference/utils.html#pyonfx.utils.Utils.all_non_empty)

In a similiar fashion to what we did in the sub function, we create a leadin and a leadout using fad tag,
then we create our first main effect by using a simple trasformation, obtaining a grow/shrink effect.

Remember to always set the layer for the line. Usually, main effects should have an higher value than leadin and leadout,
beacuse they are more important, so by doing this they will be drawn over the other effects.

For the kanji function, you can just notice that it is a lazy CTRL+C and CTRL+V of the romaji function,
but using chars instead of syls. Try yourself what happens if you use syllables for kanji!
"""

from pyonfx import *
import os
import random, os, math

def romaji(line, l,io,white,blue,cnt):

    # Leadin
    for syl in Utils.all_non_empty(line.syls):
        l.start_time = line.start_time 
        l.end_time = line.start_time + syl.start_time
        dur = syl.duration

        l.text = "{\\pos(%d,%d)\\an5\\fad(200,0)\\blur0.6}%s" % (
            syl.center, syl.middle,
            syl.text
        )
        io.write_line(l)

    # Main + Leadout
    for syl in Utils.all_non_empty(line.syls):
        c1 = f"&H{white}&"
        c3 = f"&H{blue}&"
        if syl.i == 0:
            fad = "\\fad(200, 200)"
        else:
            fad = "\\fad(0, 200)"
        l.start_time = line.start_time + syl.start_time
        l.end_time = line.end_time
        dur = syl.duration

        l.text = "{\\pos(%d,%d)\\an5%s\\blur0.6\\t(%d,%d,\\fscx105\\fscy105\\1c%s\\3c%s)}%s" % (
            syl.center, syl.middle,
            fad,
            0, dur / 3,
            c1,
            c3,
            syl.text
        )
        io.write_line(l)

    for syl in Utils.all_non_empty(line.syls):

        fsc = 7
        l.layer = 1

        c1 = f"&H{white}&"
        c3 = f"&H{blue}&"
    
        # Animating star shape that jumps over the syllables
        # Jump-in to the first syl
        jump_height = 27
        delay = 500
        if syl.i == 0:
            if line.start_time - 300<0:
                FU = FrameUtility(0,0)
            else:
                FU = FrameUtility(line.start_time - 300, line.start_time)
            for s, e, i, n in FU:
                for _ in range(10):
                    l.start_time = s
                    l.end_time = s + random.uniform(400, 700)
                    frame_pct = i / n

                    size = random.randint(5, 50)

                    x = syl.center - syl.width * (1 - frame_pct)
                    y = syl.top - math.sin(frame_pct * math.pi) * jump_height

                    alpha = 255
                    alpha += FU.add(0, syl.duration, -255)
                    alpha = Convert.alpha_dec_to_ass(int(alpha))

                    l.text = "{\\fad(0,200)\\an5\\alpha%s\\move(%.3f,%.3f,%.3f,%.3f)\\bord1\\blur2\\1c%s\\3c%s\\p1\\fscx%d\\fscy%d}%s" % (
                        alpha,
                        x, y, x + 70 - random.uniform(70, 100), y + random.uniform(-20, 20),
                        c1, c3,
                        fsc, fsc,
                        Shape.ellipse(size, size)
                    )
                    io.write_line(l)

        # Jump to the next syl or to the end of line
        jump_width = (
            line.syls[syl.i + 1].center - syl.center
            if syl.i != len(line.syls) - 1
            else syl.width * 1.75
        )
        delay = 300
        FU = FrameUtility(
            line.start_time + syl.start_time, line.start_time + syl.end_time
        )
        for s, e, i, n in FU:
            for _ in range(10):
                l.start_time = s
                l.end_time = s + random.uniform(400, 700)
                frame_pct = i / n

                size = random.randint(5, 50)

                x = syl.center + frame_pct * jump_width
                y = syl.top - math.sin(frame_pct * math.pi) * jump_height

                x, y = x + random.uniform(-10, 10), y + random.uniform(-5, 5),

                alpha = 0
                # Last jump should fade-out
                if syl.i == len(line.syls) - 1:
                    alpha += FU.add(0, syl.duration, 255)
                alpha = Convert.alpha_dec_to_ass(int(alpha))

                l.text = "{\\fad(0,200)\\an5\\alpha%s\\move(%.3f,%.3f,%.3f,%.3f)\\bord1\\blur2\\1c%s\\3c%s\\p1\\fscx%d\\fscy%d}%s" % (
                    alpha,
                    x, y, x + 70 - random.uniform(70, 100), y + random.uniform(-20, 20),
                    c1, c3,
                    fsc, fsc,
                    Shape.ellipse(size, size)
                )
                io.write_line(l)


# def kanji(line, l):
#     for char in Utils.all_non_empty(line.chars):
#         # Leadin Effect
#         l.layer = 0

#         l.start_time = line.start_time - line.leadin / 2
#         l.end_time = line.start_time + char.start_time
#         l.dur = l.end_time - l.start_time

#         l.text = "{\\an5\\pos(%.3f,%.3f)\\fad(%d,0)}%s" % (
#             char.center,
#             char.middle,
#             line.leadin / 2,
#             char.text,
#         )

#         io.write_line(l)

#         # Main Effect
#         l.layer = 1

#         l.start_time = line.start_time + char.start_time
#         l.end_time = line.start_time + char.end_time
#         l.dur = l.end_time - l.start_time

#         l.text = (
#             "{\\an5\\pos(%.3f,%.3f)"
#             "\\t(0,%d,0.5,\\1c&HFFFFFF&\\3c&HABABAB&\\fscx125\\fscy125)"
#             "\\t(%d,%d,1.5,\\fscx100\\fscy100\\1c%s\\3c%s)}%s"
#             % (
#                 char.center,
#                 char.middle,
#                 l.dur / 3,
#                 l.dur / 3,
#                 l.dur,
#                 line.styleref.color1,
#                 line.styleref.color3,
#                 char.text,
#             )
#         )

#         io.write_line(l)

#         # Leadout Effect
#         l.layer = 0

#         l.start_time = line.start_time + char.end_time
#         l.end_time = line.end_time + line.leadout / 2
#         l.dur = l.end_time - l.start_time

#         l.text = "{\\an5\\pos(%.3f,%.3f)\\fad(0,%d)}%s" % (
#             char.center,
#             char.middle,
#             line.leadout / 2,
#             char.text,
#         )

#         io.write_line(l)


# def sub(line, l):
#     # Translation Effect
#     l.start_time = line.start_time - line.leadin / 2
#     l.end_time = line.end_time + line.leadout / 2
#     l.dur = l.end_time - l.start_time

#     l.text = "{\\fad(%d,%d)}%s" % (line.leadin / 2, line.leadout / 2, line.text)

#     io.write_line(l)
def pairs(o):
    if isinstance(o,dict):
        return o.items()
    else:
        return enumerate(o)


def overlay(user,color,outline_color,scale):
    # current_working_directory = os.getcwd()
    # parent_directory = os.path.dirname(current_working_directory)
    
    io = Ass(os.path.join(user,'tmp','kar.ass'))
    meta, styles, lines = io.get_data()
    random.seed(7)
    # white = "&HFFFFFF&"
    # blue = "&H00AAEE&"
    cnt = 0
    io.path_output = os.path.join(user,'tmp','output.ass')
    for line in lines:
        # Generating lines
        romaji(line, line.copy(),io,color,outline_color,cnt)
        # if line.styleref.alignment >= 7:
            
        # elif line.styleref.alignment >= 4:
        #     kanji(line, line.copy())
        # else:
        #     sub(line, line.copy())

    io.save()