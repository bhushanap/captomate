
import re
import os

def update_resolution(user, filename, new_playresx, new_playresy):
    with open(os.path.join(user,'..',filename), 'r', encoding='utf-8') as file:
        content = file.read()

    # Define the pattern for matching PlayResX and PlayResY lines
    pattern = re.compile(r'(PlayRes[XY]):\s*(\d+)')

    # Search for resolution values in the content
    matches = pattern.findall(content)

    # Replace the resolution values
    for key, value in matches:
        if key == 'PlayResX':
            content = content.replace(f'{key}: {value}', f'{key}: {new_playresx}')
        elif key == 'PlayResY':
            content = content.replace(f'{key}: {value}', f'{key}: {new_playresy}')

    # Write the changes back to the file
    with open(os.path.join(user,'tmp', 'cfg.ass'), 'w', encoding='utf-8') as file:
        file.write(content)

def modify_styles(user, file_path=os.path.join('caption', 'cfg.ass'), new_name='Romaji', new_fontname='Arial', new_fontsize='36',
                  new_primary_color='&H7000FF', new_secondary_color='&H444444',
                  new_outline_color='&HAA0000', new_back_color='&H00FF00',
                  new_bold='1', new_italic='0', new_underline='0', new_strikeout='0',
                  new_scale_x='100', new_scale_y='100', new_spacing='0',
                  new_angle='0', new_border_style='1', new_outline='5', new_shadow='3',
                  new_alignment='8', new_margin_l='10', new_margin_r='10',
                  new_margin_v='10', new_encoding='1',resx=720,resy=1280): # Read the content of the file
    update_resolution(user, file_path, resx, resy)
    with open(os.path.join(user,'tmp', 'cfg.ass'), 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Find the line number where the [V4+ Styles] section starts
    styles_start = lines.index('[V4+ Styles]\n') + 2

    # Extract the format line
    format_line = lines[styles_start]

    # Split the format line to get the format values
    format_values = [format_line[:6]] + format_line[7:].strip().split(',')
    print(format_values,len(format_values))

    # Update the format values with the new values
    format_values[1] = new_name
    format_values[2] = new_fontname
    format_values[3] = new_fontsize
    format_values[4] = new_primary_color
    format_values[5] = new_secondary_color
    format_values[6] = new_outline_color
    format_values[7] = new_back_color
    format_values[8] = new_bold
    format_values[9] = new_italic
    format_values[10] = new_underline
    format_values[11] = new_strikeout
    format_values[12] = new_scale_x
    format_values[13] = new_scale_y
    format_values[14] = new_spacing
    format_values[15] = new_angle
    format_values[16] = new_border_style
    format_values[17] = new_outline
    format_values[18] = new_shadow
    format_values[19] = new_alignment
    format_values[20] = new_margin_l
    format_values[21] = new_margin_r
    format_values[22] = new_margin_v
    format_values[23] = new_encoding

    # Join the updated format values and replace the original format line
    lines[styles_start] = format_line[:7] + ','.join(format_values[1:]) + '\n'

    # Write the modified content back to the file
    with open(os.path.join(user,'tmp', 'cfg.ass'), 'w', encoding='utf-8') as file:
        file.writelines(lines)

# Example usage:
# if __name__ == "__main__":
#     modify_styles('caption/cfg.ass', 'Romaji', 'Arial', '72', #file, romaji, font, size
#                   '&H7000FF', '&H444444', '&HAA0000', '&H00FF00',#pri sec out back
#               '1', '0', '0', '0', '100', '100', #bold italic underline strike scalex scaley 
#               '1', '0', '3', '5', '3', '8', #spacing, angle, 1 outline 3 box, 
#                                              #outline, shadow, 2 bottom 5 center
#               '10', '10', '10', '1')#margin L R V, encoding
