"""
Lambda function to zip CSV files in S3 and replace daily.
"""

import os
import boto3
import zipfile
import tempfile

# ====== ENVIRONMENT VARIABLES ======
environment = os.environ['ENVIRONMENT']
aws_region  = os.environ['REGION']
bucket_name = os.environ['BUCKET']
# ===================================

# Folder and zip file name
folder_prefix = "mydir/"
zip_file_name = "StudyO_INPUT_Files.zip"

def handler(event, context):
    print("ENTER HANDLER FUNCTION")
    files, keys = loadfiles(bucket_name, folder_prefix)
    if not files:
        return {"statusCode": 200, "body": "No CSV files found."}
    zip_path = create_zip(files)
    upload_zip(zip_path, bucket_name, folder_prefix + zip_file_name)
    delete_originals(bucket_name, keys)
    return {
        "statusCode": 200,
        "body": f"Created {zip_file_name} in {bucket_name}/{folder_prefix} and deleted source CSVs"
    }

def loadfiles(bucket, prefix):
    print("ENTER LOADFILES FUNCTION")
    s3_client = boto3.client("s3")
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)

    local_files = []
    keys = []
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            if not key.endswith(".csv"):
                continue
            if "/" in key[len(prefix):]:
                continue

            tmp_file_path = os.path.join(tempfile.gettempdir(), os.path.basename(key))
            print(f"Downloading {key} to {tmp_file_path}")
            s3_client.download_file(bucket, key, tmp_file_path)
            local_files.append(tmp_file_path)
            keys.append(key)

    return local_files, keys

def create_zip(files):
    print("ENTER CREATE_ZIP FUNCTION")
    tmp_zip_path = os.path.join(tempfile.gettempdir(), zip_file_name)
    with zipfile.ZipFile(tmp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in files:
            zipf.write(f, arcname=os.path.basename(f))
    print(f"Zip created at {tmp_zip_path}")
    return tmp_zip_path

def upload_zip(zip_path, bucket, key):
    print("ENTER UPLOAD_ZIP FUNCTION")
    s3_client = boto3.client("s3")
    print(f"Uploading {zip_path} to {bucket}/{key}")
    s3_client.upload_file(zip_path, bucket, key)

def delete_originals(bucket, keys):
    print("ENTER DELETE_ORIGINALS FUNCTION")
    s3_client = boto3.client("s3")
    for key in keys:
        print(f"Deleting {bucket}/{key}")
        s3_client.delete_object(Bucket=bucket, Key=key)
