import ffmpeg


def convert_video(format, filename, new_filename, video_status):
    # filename_without_ext = filename.split('.')[0]
    new_filename_with_ext = new_filename + '.' + format
    ffmpeg.input(filename) \
        .output(new_filename_with_ext) \
        .run()

    video_status.update({new_filename: True})
    return new_filename


def simple_edit_video(filename, operations, new_filename, video_status):
    tmp_filename = new_filename + '.' + video_extension(filename)
    stream = ffmpeg.input(filename)
    if 'hflip' in operations:
        stream = stream.hflip()
    if 'vflip' in operations:
        stream = stream.vflip()

    stream.output(tmp_filename) \
        .run()

    video_status.update({new_filename: True})
    return tmp_filename


def video_extension(filename):
    return filename.split('.')[1]


def video_name(filename):
    return filename.split('.')[0]
