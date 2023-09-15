import minio
import base64
import io
import uuid
import os
from ..settings import OSS_ENDPOINT_PATH, OSS_ACCESS_KEY, OSS_SECRET_KEY, OSS_BUCKET, OSS_ARGS


minio_client = minio.Minio(OSS_ENDPOINT_PATH, access_key=OSS_ACCESS_KEY, secret_key=OSS_SECRET_KEY, **OSS_ARGS)


def upload_oss(content, prefix='', filename='', file_type='html', bucket=OSS_BUCKET):
    if file_type == 'pdf' and isinstance(content, str):
        content = base64.b64decode(content)

    if isinstance(content, bytes):
        content = io.BytesIO(content)
    elif isinstance(content, str):
        content = io.BytesIO(content.encode('utf-8'))
    elif not isinstance(content, io.IOBase):
        raise Exception('content must be bytes, str or io object')
    if not minio_client.bucket_exists(bucket):
        minio_client.make_bucket(bucket)
    if not filename:
        filename = str(uuid.uuid4()) + '.' + file_type
    file_path = os.path.join(prefix, filename)
    obj = minio_client.put_object(bucket_name=bucket,
                                  object_name=file_path,
                                  data=content,
                                  length=-1,
                                  part_size=10 * 1024 * 1024)
    return file_path


