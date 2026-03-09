"""
AWS Lambda function for converting image files to different formats.

Triggered by S3 upload events. Converts images based on target format
embedded in the filename (e.g., filename_webp.png converts to WebP).

Supported formats: JPG, PNG, WebP, GIF
"""

import json
import boto3
import os
import urllib.parse
from PIL import Image

s3_client = boto3.client('s3')
OUTPUT_BUCKET = 'S3-OUTPUT-BUCKET-NAME'  # Replace with your output bucket name

def lambda_handler(event, context):
    """
    Main Lambda handler for file conversion.

    Args:
        event (dict): S3 event containing bucket and object information
        context: Lambda context object

    Returns:
        dict: Success response
    """
    try:
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        
        # Parse target format from filename (e.g., 1234_webp.png)
        base_name = os.path.basename(object_key).rsplit('.', 1)[0]  # Get "1234_webp"
        target_format = base_name.split('_')[-1].lower()            # Get "webp"
        
        download_path = f'/tmp/{os.path.basename(object_key)}'
        output_file_name = f"{base_name}.{target_format}"           # Output "1234_webp.webp"
        upload_path = f'/tmp/output.{target_format}'
        
        # Download original image
        s3_client.download_file(source_bucket, object_key, download_path)
        
        # Convert image using Pillow
        print(f"Converting image to: {target_format.upper()}...")
        with Image.open(download_path) as img:
            # Remove alpha channel for JPG conversion
            if target_format in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
                
            # Pillow format mapping
            format_map = {'jpg': 'JPEG', 'jpeg': 'JPEG', 'png': 'PNG', 'webp': 'WEBP', 'gif': 'GIF'}
            save_format = format_map.get(target_format, 'JPEG')
            
            img.save(upload_path, save_format, quality=85)
        
        # Upload converted file
        s3_client.upload_file(upload_path, OUTPUT_BUCKET, output_file_name)
        print("Conversion and upload successful!")
        return {'statusCode': 200, 'body': json.dumps('Success')}
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise e