import boto3
import requests
import os

# Usar la región de la variable de entorno para todos los clientes
region_name = os.environ.get("REGION_NAME")
s3_resource = boto3.resource('s3', region_name=region_name)
client_s3 = boto3.client('s3', region_name=region_name)

def download_file(base_path, bucket, key, filename):
    """
    Download a file from S3 to the specified local path.
    
    Args:
        base_path: Local directory path where the file will be saved
        bucket: S3 bucket name
        key: S3 object key
        filename: Name to save the file as locally
    
    Returns:
        bool: True if download was successful, False otherwise
    """
    try:
        print(f"Downloading file from s3://{bucket}/{key} to {base_path}{filename} in region {region_name}")
        
        # Ensure the base path exists
        import os
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            
        # Download the file
        with open(base_path + filename, "wb") as data:
            client_s3.download_fileobj(bucket, key, data)
        
        # Verify the file was downloaded successfully
        if os.path.exists(base_path + filename):
            file_size = os.path.getsize(base_path + filename)
            print(f"File downloaded successfully, size: {file_size} bytes")
            return True
        else:
            print(f"File download failed: File not found at {base_path}{filename}")
            return False
            
    except Exception as e:
        print(f"Error downloading file from s3://{bucket}/{key}: {str(e)}")
        return False

def upload_data_to_s3(bytes_data,bucket_name, s3_key):
    obj = s3_resource.Object(bucket_name, s3_key)
    obj.put(ACL='private', Body=bytes_data)
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
    return s3_url

def download_file_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def get_media_url(mediaId,whatsToken):
    
    URL = 'https://graph.facebook.com/v17.0/'+mediaId
    headers = {'Authorization':  whatsToken}
    print("Requesting")
    response = requests.get(URL, headers=headers)
    responsejson = response.json()
    if('url' in responsejson):
        print("Responses: "+ str(responsejson))
        return responsejson['url']
    else:
        print("No URL returned")
        return None

def get_whats_media(url,whatsToken):
    headers = {'Authorization':  whatsToken}
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        return None
    
def put_file(base_path,filename, bucket, key):
    with open(base_path+filename, "rb") as data:
        client_s3.upload_fileobj(data,bucket, key+filename)
    print("Put file in s3://{}{}{}".format(bucket,key,filename))
