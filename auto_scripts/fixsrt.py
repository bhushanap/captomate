import re

def replace_words(reference_string, srt_file='tmp/subrip.srt'):
    with open(srt_file, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.split('\n')

    for i in range(len(lines)):
        if '-->' in lines[i]:  # Skip timecodes
            continue

        words = re.findall(r'\b\w+\b', lines[i])  # Extract words from the line
        for j in range(len(words)):
            if words[j] != reference_string.split()[j]:
                lines[i] = lines[i].replace(words[j], reference_string.split()[j], 1)

    # Write the changes back to the file
    with open(srt_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))


