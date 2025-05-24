from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import boto3
from botocore.client import Config
from dotenv import load_dotenv
import os
from io import BytesIO

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = boto3.client(
    's3',
    endpoint_url=f"http://{os.getenv('MINIO_ENDPOINT')}:{os.getenv('MINIO_PORT')}",
    aws_access_key_id=os.getenv('MINIO_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('MINIO_SECRET_KEY'),
    config=Config(signature_version='s3v4'),
    use_ssl=os.getenv('MINIO_USE_SSL', 'false').lower() == 'true'

)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    try:
        s3_client.upload_fileobj(
            file.file,
            os.getenv('MINIO_BUCKET'),
            file.filename,
            ExtraArgs={'ContentType': 'application/pdf'}
        )
        return {"message": "File uploaded successfully"}
    except boto3.exceptions.S3UploadFailedError as e:
        raise HTTPException(status_code=500, detail=f"S3 Upload failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/list")
async def list_pdfs():
    try:
        response = s3_client.list_objects_v2(Bucket=os.getenv('MINIO_BUCKET'))
        files = [
            {"filename": obj['Key'], "object_key": obj['Key']}
            for obj in response.get('Contents', [])
        ]
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

@app.get("/download/{object_key}")
async def download_pdf(object_key: str):
    try:
        response = s3_client.get_object(Bucket=os.getenv('MINIO_BUCKET'), Key=object_key)
        return StreamingResponse(
            BytesIO(response['Body'].read()),
            media_type='application/pdf',
            headers={'Content-Disposition': f'attachment; filename="{object_key}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")