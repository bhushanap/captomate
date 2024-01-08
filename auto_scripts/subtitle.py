def srt_duration(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    total_duration = 0
    current_start_time = None
    current_end_time = None

    for line in lines:
        line = line.strip()

        if line.isdigit():
            # This line is the subtitle number, skip it
            continue

        if ' --> ' in line:
            start_time, end_time = line.split(' --> ')
            current_start_time = convert_to_seconds(start_time)
            current_end_time = convert_to_seconds(end_time)
            total_duration += current_end_time - current_start_time

    return current_end_time


def convert_to_seconds(time_str):
    
    hours, minutes, seconds = map(int, time_str[:-4].split(':'))
    # print(hours, minutes,seconds)
    return hours * 3600 + minutes * 60 + seconds + 1

