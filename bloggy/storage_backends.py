from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(FileSystemStorage):
    location = 'media'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    # security_token = None

    # def _get_security_token(self):
    #     return None


class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
