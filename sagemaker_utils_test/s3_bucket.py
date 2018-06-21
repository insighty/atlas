# assumes python 3 - just a test implementation

class S3Bucket(object):
    def __init__(self, bucket_name):
        import boto3
        self._bucket = boto3.resource('s3').Bucket(bucket_name)

    def upload_from_string(self, name, data):
        self._bucket.put_object(Key=name, Body=_byte_string(data))

    def upload_from_file(self, name, input_file):
        self._bucket.upload_file(input_file, name)

    def exists(self, name):
        objs = self._objs_with_prefix(name)

        for obj in objs:
            if obj.key == name:
                return True

        return False

    def download_as_string(self, name):
        objs = self._objs_with_prefix(name)
        for obj in objs:
            if obj.key == name:
                return _byte_string(_read_streamed_object(obj))

    def download_to_file(self, name, output_file):
        self._bucket.download_file(name, output_file)

    def list_files(self, pathname):
        objs = self._objs_with_prefix(pathname)
        return [obj.key for obj in objs]

    def _objs_with_prefix(self, prefix):
        return self._bucket.objects.filter(Prefix=prefix)

def _read_streamed_object(obj):
    return obj.get()['Body'].read()

# couldn't grab this one from vcat.utils for some reason???
def _byte_string(string):
    if isinstance(string, bytes):
        return string
    else:
        return bytes(string.encode('utf-8', 'ignore'))