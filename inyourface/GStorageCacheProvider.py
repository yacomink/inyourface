import os
from google.cloud import storage
class CacheProvider(object):

    def __init__(self, project_id):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.get_bucket(project_id + ".appspot.com")

    def get(self, key):
        blob = self.bucket.blob('cache/' + key)
        if (blob.exists()):
            return blob.download_as_string()
        return None

    def set(self, key, value):
        blob = self.bucket.blob('cache/' + key)
        blob.upload_from_string(value)

    def close(self):
        # no-op
        return True
