"""
Helper functions for better form data handling in Locust
"""
import random
import string
import os

def random_boundary(length=30):
    """Generate a random boundary string for multipart/form-data"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def create_multipart_formdata(fields, files, boundary=None):
    """
    Create a multipart/form-data body with proper boundaries.
    
    Args:
        fields: Dictionary of field name to value
        files: Dictionary of field name to (filename, content, content_type)
        boundary: Optional boundary string, generated if not provided
    
    Returns:
        (body, content_type): The request body and content-type header
    """
    if boundary is None:
        boundary = random_boundary()
    
    body = bytearray()
    
    for field_name, field_value in fields.items():
        body.extend(f'--{boundary}\r\n'.encode('utf-8'))
        body.extend(f'Content-Disposition: form-data; name="{field_name}"\r\n\r\n'.encode('utf-8'))
        body.extend(f'{field_value}\r\n'.encode('utf-8'))
    
    for field_name, file_data in files.items():
        filename, content, content_type = file_data
        body.extend(f'--{boundary}\r\n'.encode('utf-8'))
        body.extend(f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'.encode('utf-8'))
        body.extend(f'Content-Type: {content_type}\r\n\r\n'.encode('utf-8'))
        
        if isinstance(content, bytes):
            body.extend(content)
        else:
            body.extend(content.encode('utf-8'))
        body.extend(b'\r\n')
    
    body.extend(f'--{boundary}--\r\n'.encode('utf-8'))
    
    content_type = f'multipart/form-data; boundary={boundary}'
    
    return bytes(body), content_type

def create_form_data_for_image(image_path, field_name="file"):
    """
    Create multipart form data for an image file.
    
    Args:
        image_path: Path to the image file
        field_name: Form field name for the file
    
    Returns:
        (body, content_type): The request body and content-type header
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file {image_path} not found")
    
    # Determine content type based on file extension
    _, ext = os.path.splitext(image_path)
    if ext.lower() in ('.jpg', '.jpeg'):
        content_type = 'image/jpeg'
    elif ext.lower() == '.png':
        content_type = 'image/png'
    elif ext.lower() == '.gif':
        content_type = 'image/gif'
    else:
        content_type = 'application/octet-stream'
    
    # Read the file
    with open(image_path, 'rb') as f:
        file_content = f.read()
    
    # Create the form data
    files = {
        field_name: (os.path.basename(image_path), file_content, content_type)
    }
    
    return create_multipart_formdata({}, files) 