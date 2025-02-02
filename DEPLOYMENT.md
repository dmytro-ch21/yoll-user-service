---

**DEPLOYMENT.md (Production Deployment on AWS Linux)**

```markdown
# Deployment Guide for Yoll User Service

This guide outlines the steps to deploy the **Yoll User Service** on an AWS Linux instance. The deployment uses a virtual environment, Gunicorn as the WSGI server, and no reverse proxy (like Nginx) is required.

## Prerequisites

- An AWS Linux instance (e.g., Amazon Linux 2 or Ubuntu)
- **Python 3** installed on the server
- **pip** installed
- SSH access to the server
- A properly configured `.env` file with all necessary production environment variables

## Deployment Steps

### 1. Clone the Repository on the Server

SSH into your AWS instance, then run:

```bash
    git clone <repository-url>
    cd yoll-user-service
```

Set Up a Virtual Environment and Install Dependencies
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```