# Video Transcoding API 

This API created using flask and FFmpeg. 

API uses Min.io as file storage and mongodb as database storage.

Steps to run
1. Download [FFmpeg](https://www.ffmpeg.org/).
2. Add FFmpeg location to your `PATH` variable.
3. set up storage servers(if you have them already setup skip this)
   1. Set up [min.io](https://min.io/) storage server([guide](https://docs.min.io/docs/minio-quickstart-guide.html)).
   2. Set up [mongodb](https://www.mongodb.com/) server.
4. Install necessary packages using `requirements.txt`
5. Modify `config.cfg` file and add database and s3 storage information.
6. Modify `app_host` and `app_port` variables in `videTranscoderAPI.py`
7. Run `videoTranscodeAPI.py`, this will start the server on `app_host:app_port`

### Convert file stored in s3 storage
Call api with `https://host:port/api/v1/test?input=file_to_convert&q=current_file_quality(480p)`.

This will convert the input file and upload it into s3 storage. 

Call api on `https://host:port/api/v1/vtest` to check current status of file conversion.