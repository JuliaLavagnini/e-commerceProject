from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    location = 'static'

    def get_object_parameters(self, name):
        return {
            'CacheControl': 'max-age=86400',  # 1 day
        }

class MediaStorage(S3Boto3Storage):
    location = 'media'

    def get_object_parameters(self, name):
        return {
            'CacheControl': 'max-age=31536000',  # 1 year
        }