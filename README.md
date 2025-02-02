# Yoll User Service

The **Yoll User Service** is a Python-based API that provides multi-domain services for student projects. This guide will help you set up and run the service locally.

## Prerequisites

- **Python 3** (Ensure Python 3.x is installed on your machine)
- **pip** (Python package installer)
- **Virtual Environment** (Recommended for isolating dependencies)
- A `.env` file in the project root with the necessary environment variables

## Setup Instructions

1. **Clone the Repository:**
   ```bash
    git clone https://github.com/dmytro-ch21/yoll-user-service
    cd yoll-user-service
   ```

2. **Create and Activate a Virtual Environment:**
    Once you have all of the above set up:
    On macOS/Linux:
    ```bash
        python3 -m venv venv
        source venv/bin/activate
    ```
    On Windows:
    ```bash
        python -m venv venv
        venv\Scripts\activate
    ```

3.	**Install Dependencies:**  
Make sure you have a requirements.txt file in the repository, then run:
    ```bash
        pip install -r requirements.txt
    ```

4.	**Configure Environment Variables:**
Create a .env file in the project root, these are the required variables (Reach out to dmytro@yoll.io for details).
    ```text
        DATABASE_NAME=
        DATABASE_USER=
        DATABASE_PASSWORD=
        DATABASE_HOST=
        DATABASE_PORT=
        SECRET_TOKEN=
    ```

5.	**Run the Application Locally:**
    ```bash
        flask run
    ```
    OR 
    ```bash
        python run.py
    ```