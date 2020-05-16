
import ffmpeg
import uuid

def convert_video(format, filename):
    filename_without_ext = filename.split('.')[0]
    new_filename = filename_without_ext + '.' + format
    ffmpeg.input(filename)\
        .output(new_filename)\
        .run()

    return new_filename

def simple_edit_video(filename, operations):
    tmp_filename = str(uuid.uuid4()) + '.' + video_extension(filename)
    stream = ffmpeg.input(filename)
    if 'hflip' in operations:
        stream = stream.hflip()
    if 'vflip' in operations:
        stream = stream.vflip()

    stream.output(tmp_filename) \
        .run()

    return tmp_filename


def video_extension(filename):
    return filename.split('.')[1]


def video_name(filename):
    return filename.split('.')[0]
