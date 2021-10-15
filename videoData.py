class VideoFile:

    ADDED_STATUS = 1
    PROCESSING_STATUS = 2
    DONE_STATUS = 0

    def __init__(self, name, location, quality):
        self.name = name
        self.location = location
        self.quality = quality
        self.status = self.ADDED_STATUS

    def change_status(self, status):
        self.status = status
