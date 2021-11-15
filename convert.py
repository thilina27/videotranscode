import os


# todo : add linux stuff if needed (test)
# change this to true if need console output for converting file (ffmpeg)
debug = False


def convert_video(input_file, output_file="output.mp4", video_quality="360"):

    """ A simple function that convert given video file to designated quality
        using ffmpeg
        :param input_file : input file name
        :param  output_file : output file name, Default : "output.mp4"
        :param  video_quality : designated video quality, Default : "360"
        :return success message
    """
    # cmd ref
    # ffmpeg -i inp.file -vf scale=-1:360 -vcodec mpeg4 -qscale 3 output.mp4
    # convert cmd
    command = f"ffmpeg -i {input_file} -vf scale=-1:{video_quality} -vcodec mpeg4 -qscale 3 {output_file}"
    # use popen to avoid direct console log
    output = os.popen(command)

    if debug:
        print(output.read())

    return f"{input_file} convert to {video_quality}p and saved as {output_file}"
