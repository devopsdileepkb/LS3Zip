"""
Lambda function to zip CSV files in S3.
Based on organizational template structure.
"""

import os
import boto3
import zipfile
import tempfile
from botocore.exceptions import ClientError
from botocore.config import Config as BotoConfig

# ====== EDIT THESE ENVIRONMENT VARIABLES IN TERRAFORM OR CONSOLE ======
environment = os.environ['ENVIRONMENT']   # e.g. "dev" / "prd"
aws_region  = os.environ['REGION']        # e.g. "eu-west-1"
bucket_name = os.environ['BUCKET']        # <-- SET YOUR BUCKET NAME HERE
# ======================================================================

# Fixed folder and zip file name
folder_prefix = "iqvia_export_unload/"
zip_file_name = "StudyO_INPUT_Files.zip"

def handler(event: dict, context):
    """
    Defines the sequence of actions for the Lambda.
    """
    print("ENTER HANDLER FUNCTION")
    files = loadfiles(bucket_name, folder_prefix)
    zip_path = create_zip(files)
    upload_zip(zip_path, bucket_name, folder_prefix + zip_file_name)
    return {
        "statusCode": 200,
        "body": f"Created {zip_file_name} in {bucket_name}/{folder_prefix}"
    }

def loadfiles(bucket, prefix):
    """
    Download CSV files directly under iqvia_export_unload (no subfolders).
    """
    print("ENTER LOADFILES FUNCTION")
    s3_client = boto3.client("s3")
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)

    local_files = []
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            # Only include CSV files directly under folder (skip subfolders and zips)
            if not key.endswith(".csv"):
                continue
            if "/" in key[len(prefix):]:
                continue

            tmp_file_path = os.path.join(tempfile.gettempdir(), os.path.basename(key))
            print(f"Downloading {key} to {tmp_file_path}")
            s3_client.download_file(bucket, key, tmp_file_path)
            local_files.append(tmp_file_path)

    return local_files

def create_zip(files):
    """
    Create a zip archive from given local CSV files.
    """
    print("ENTER CREATE_ZIP FUNCTION")
    tmp_zip_path = os.path.join(tempfile.gettempdir(), zip_file_name)
    with zipfile.ZipFile(tmp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in files:
            zipf.write(f, arcname=os.path.basename(f))
    print(f"Zip created at {tmp_zip_path}")
    return tmp_zip_path

def upload_zip(zip_path, bucket, key):
    """
    Upload the zip file to S3, overwriting if exists.
    """
    print("ENTER UPLOAD_ZIP FUNCTION")
    s3_client = boto3.client("s3")
    print(f"Uploading {zip_path} to {bucket}/{key}")
    s3_client.upload_file(zip_path, bucket, key)