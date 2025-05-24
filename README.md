# PDF Upload/Download Application

This project is a PDF upload/download application with a React front-end, FastAPI backend, and MinIO for storage.

## Project Structure
- `backend/`: FastAPI backend for handling PDF uploads/downloads.
- `frontend/`: Vite + React front-end for the user interface.
- `docker-compose.yml`: Docker Compose file to run MinIO and the backend.

## Prerequisites
- Python 3.9+
- Node.js 18+
- Docker and Docker Compose
- MinIO Client (`mc`)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pdf_upload_app