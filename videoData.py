class VideoFile:

    ADDED_STATUS = 1
    PROCESSING_STATUS = 2
    DONE_STATUS = 0
    ADDED_STATUS_TEXT = "Video file added for converting"
    PROCESSING_STATUS_TEXT = "Processing video file"
    DONE_STATUS_TEXT = "Successfully converted"

    def __init__(self, name, quality):
        self.name = name
        self.quality = quality
        self.status = self.ADDED_STATUS

    def change_status(self, status):
        self.status = status
