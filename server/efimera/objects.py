from minio import Minio
from urllib.parse import urlparse
from minio.error import S3Error

import mimetypes
import requests
import os

def get_minio_client():
    """Initialize and return Minio client"""
    return Minio(
        os.getenv("BUCKET_URL", "localhost:9000"),
        access_key=os.getenv("BUCKET_URL_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("BUCKET_URL_SECRET_KEY", "minioadmin"),
        secure=os.getenv("BUCKET_URL_SECURE", False)
    )


def is_downloadable(content_type):
    """Check if the URL points to downloadable content"""
    downloadable_types = {
        'application/pdf',
        'image/',
        'audio/',
        'video/',
        'application/zip',
        'application/x-rar-compressed'
    }

    return any(content_type.startswith(dtype) for dtype in downloadable_types)


def upload_from(url):
    """Download content and upload to bucket"""
    try:
        bucket_name = os.getenv("BUCKET_NAME", "efimera")
        # Stream download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '')

        # Generate a unique filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            # Generate filename based on content type if URL doesn't provide one
            ext = mimetypes.guess_extension(content_type) or ''
            filename = f"download_{hash(url)}{ext}"

        # Get Minio client
        client = get_minio_client()

        # Ensure bucket exists
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)

        # Upload to Minio
        client.put_object(
            bucket_name,
            filename,
            response.raw,
            length=int(response.headers.get('content-length', 0)),
            content_type=content_type
        )

        return f"minio://{bucket_name}/{filename}"
    except (requests.RequestException, S3Error) as e:
        raise Exception(f"Error downloading/uploading content: {str(e)}")
