"""
AWS Lambda function for generating presigned URLs for S3 file uploads and downloads.

This function handles two modes:
1. Generate upload URL for file conversion (Mode 1)
2. Check conversion progress and provide download URL (Mode 2)

Environment Variables:
- INPUT_BUCKET: S3 bucket for input files
- OUTPUT_BUCKET: S3 bucket for converted output files
"""

import json
import boto3
import uuid
import os

s3_client = boto3.client('s3')
INPUT_BUCKET = 'S3-INPUT-BUCKET-NAME'  # Replace with your input bucket name
OUTPUT_BUCKET = 'S3-OUTPUT-BUCKET-NAME'  # Replace with your output bucket name

def lambda_handler(event, context):
    """
    Main Lambda handler function.

    Args:
        event (dict): API Gateway event containing query parameters
        context: Lambda context object

    Returns:
        dict: Response with status code, headers, and body

    Query Parameters:
        - checkFile: Filename to check conversion status (Mode 2)
        - targetFormat: Desired output format (webp, png, jpg) (Mode 1)
        - fileType: MIME type of the file being uploaded (Mode 1)
    """
    # CORS headers for web requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,GET,POST'
    }
    
    try:
        query_params = event.get('queryStringParameters') or {}
        check_file = query_params.get('checkFile')
        
        if check_file:
            # Mode 2: Check conversion progress
            # Filename like: 12345_webp.png -> output should be: 12345_webp.webp
            base_name = check_file.rsplit('.', 1)[0]
            target_format = base_name.split('_')[-1]  # Extract format after underscore
            output_file_name = f"{base_name}.{target_format}"
            
            try:
                # Check if output file exists
                s3_client.head_object(Bucket=OUTPUT_BUCKET, Key=output_file_name)
                # Generate download URL if file exists
                download_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': OUTPUT_BUCKET, 'Key': output_file_name},
                    ExpiresIn=3600
                )
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'status': 'completed', 'downloadURL': download_url})
                }
            except Exception:
                # File not found, still processing
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({'status': 'processing'})
                }
                
        else:
            # Mode 1: Generate upload ticket
            # Get target format from frontend (e.g., webp, png, jpg)
            target_format = query_params.get('targetFormat', 'jpg')
            file_type = query_params.get('fileType', 'image/png')
            ext = file_type.split('/')[-1] if '/' in file_type else 'png'
            
            # Embed target format in filename (e.g., 1234_webp.png)
            file_name = f"{uuid.uuid4()}_{target_format}.{ext}"
            
            # Generate upload URL for input bucket
            presigned_url = s3_client.generate_presigned_url(
                'put_object',
                Params={'Bucket': INPUT_BUCKET, 'Key': file_name, 'ContentType': file_type},
                ExpiresIn=300
            )
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'uploadURL': presigned_url, 'fileName': file_name})
            }
            
    except Exception as e:
        # Return error response
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps(str(e))}