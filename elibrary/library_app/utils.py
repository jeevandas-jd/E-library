
from google.cloud import storage
import os

def upload_data_to_gcs(bucket_name, source_name, destination_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_name)
        blob.upload_from_filename(source_name)
        return True
    except Exception as e:
        print(f"Error uploading to Google Cloud Storage: {e}")
        return False
    
def update_file_in_gcs(bucket_name, source_name, destination_name):
    """Updates a file in Google Cloud Storage by re-uploading it."""
    return upload_data_to_gcs(bucket_name, source_name, destination_name)

def download_data_from_gcs(bucket_name, source_name, destination_path):
    """Downloads a file from Google Cloud Storage to a local path."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_name)
        blob.download_to_filename(destination_path)
        return True
    except Exception as e:
        print(f"Error downloading from Google Cloud Storage: {e}")
        return False