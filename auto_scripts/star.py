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





def romaji(line, l, io,star,CU,color,outline_color):
    # Setting up a delay, we will use it as duration time of the leadin and leadout effects
    delay = 50
    # Setting up offset variables, we will use them for the \move in leadin and leadout effects
    off_x = 35
    off_y = 15

    # Leadin Effect
    for syl in Utils.all_non_empty(line.syls):
        l.layer = 0

        l.start_time = (
            line.start_time + 25 * syl.i - delay #- 80
        )  # Remove 80 to start_time to let leadin finish a little bit earlier than the main effect of the first syllable
        l.end_time = line.start_time + syl.start_time
        l.dur = l.end_time - l.start_time

        l.text = (
            "{\\an5\\move(%.3f,%.3f,%.3f,%.3f,0,%d)\\blur2\\t(0,%d,\\blur0)\\fad(%d,0)}%s"
            % (
                syl.center + math.cos(syl.i / 2) * off_x,
                syl.middle + math.sin(syl.i / 4) * off_y,
                syl.center,
                syl.middle,
                delay,
                delay,
                delay,
                syl.text,
            )
        )

        io.write_line(l)

    # Main Effect
    for syl in Utils.all_non_empty(line.syls):
        l.layer = 1

        l.start_time = line.start_time + syl.start_time
        l.end_time = line.start_time + syl.end_time + 100
        l.dur = l.end_time - l.start_time

        c1 = f"&H{color}&"
        c3 = f"&H{outline_color}&"
        # Change color if inline_fx is m1
        if syl.inline_fx == "m1":
            c1 = f"&H{color}&"
            c3 = f"&H{outline_color}&"

        on_inline_effect_2 = ""
        # Apply rotation if inline_fx is m2
        if syl.inline_fx == "m2":
            on_inline_effect_2 = "\\t(0,%d,\\frz%.3f)\\t(%d,%d,\\frz0)" % (
                l.dur / 4,
                random.uniform(-40, 40),
                l.dur / 4,
                l.dur,
            )

        l.text = (
            "{\\an5\\pos(%.3f,%.3f)%s\\t(0,80,\\fscx105\\fscy105\\1c%s\\3c%s)\\t(80,%d,\\fscx100\\fscy100)}%s"
            % (
                syl.center,
                syl.middle,
                on_inline_effect_2,
                c1,
                c3,
                l.dur - 80,
                syl.text,
            )
        )

        io.write_line(l)

        # Animating star shape that jumps over the syllables
        # Jump-in to the first syl
        jump_height = 18
        if syl.i == 0:
            if line.start_time - line.leadin / 2 < 0:
                FU = FrameUtility(0,0)
            elif line.start_time - line.leadin / 2 > line.start_time:
                FU = FrameUtility(line.start_time,line.start_time)
            else:
                FU = FrameUtility(line.start_time - line.leadin / 2, line.start_time)
            for s, e, i, n in FU:
                l.start_time = s
                l.end_time = e
                frame_pct = i / n

                x = syl.center - syl.width * (1 - frame_pct)
                y = syl.top - math.sin(frame_pct * math.pi) * jump_height

                alpha = 255
                alpha += FU.add(0, syl.duration, -255)
                alpha = Convert.alpha_dec_to_ass(int(alpha))

                l.text = (
                    "{\\alpha%s\\pos(%.3f,%.3f)\\bord1\\blur1\\1c%s\\3c%s\\p1}%s"
                    % (alpha, x, y, c1, c3, star)
                )
                io.write_line(l)

        # Jump to the next syl or to the end of line
        jump_width = (
            line.syls[syl.i + 1].center - syl.center
            if syl.i != len(line.syls) - 1
            else syl.width
        )
        FU = FrameUtility(
            line.start_time + syl.start_time, line.start_time + syl.end_time
        )
        for s, e, i, n in FU:
            l.start_time = s
            l.end_time = e
            frame_pct = i / n

            x = syl.center + frame_pct * jump_width
            y = syl.top - math.sin(frame_pct * math.pi) * jump_height

            alpha = 0
            # Last jump should fade-out
            if syl.i == len(line.syls) - 1:
                alpha += FU.add(0, syl.duration, 255)
            alpha = Convert.alpha_dec_to_ass(int(alpha))

            l.text = "{\\alpha%s\\pos(%.3f,%.3f)\\bord1\\blur1\\1c%s\\3c%s\\p1}%s" % (
                alpha,
                x,
                y,
                c1,
                c3,
                star,
            )
            io.write_line(l)

    # Leadout Effect
    for syl in Utils.all_non_empty(line.syls):
        l.layer = 0

        l.start_time = line.start_time + syl.end_time + 100
        l.end_time = line.end_time - 25 * (len(line.syls) - syl.i) - delay + 0
        l.dur = l.end_time - l.start_time

        l.text = (
            "{\\an5\\move(%.3f,%.3f,%.3f,%.3f,%d,%d)\\t(%d,%d,\\blur2)\\fad(0,%d)}%s"
            % (
                syl.center,
                syl.middle,
                syl.center + math.cos(syl.i / 2) * off_x,
                syl.middle + math.sin(syl.i / 4) * off_y,
                l.dur - delay,
                l.dur,
                l.dur - delay,
                l.dur,
                delay,
                syl.text,
            )
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

def overlay(user,color,outline_color,scale):
    # current_working_directory = os.getcwd()
    # parent_directory = os.path.dirname(current_working_directory)
    
    io = Ass(os.path.join(user,'tmp','kar.ass'))
    meta, styles, lines = io.get_data()
    star = Shape.star(5, 4, 10)
    CU = ColorUtility(lines)
    io.path_output = os.path.join(user,'tmp','output.ass')
    for line in lines:
        # Generating lines
        romaji(line, line.copy(),io,star,CU,color,outline_color)
        # if line.styleref.alignment >= 7:
            
        # elif line.styleref.alignment >= 4:
        #     kanji(line, line.copy())
        # else:
        #     sub(line, line.copy())

    io.save()