# use to access min io s3
from minio import Minio


class MinIoS3:

    def __init__(self, endpoint, access_key, secret_key, bucket):
        self.bucket = bucket
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=False
        )

    def get_file(self, file_name):
        try:
            self.client.fget_object(self.bucket, file_name, file_name)
        # todo : remove broad exception
        except Exception as e:
            print("Error occurred")

    def put_file(self, file_name):
        result = self.client.fput_object(
            self.bucket, file_name, file_name,
        )

        return result
