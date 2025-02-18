# Exit immediately if any command exits with a non-zero status.
set -e

# --- Configuration ---
# Git to ignore file mode changes.
git config core.fileMode false

# Set the project directory to app's location on the instance.
PROJECT_DIR="/home/ec2-user/yoll-user-service"

# The command to locate gunicorn running process.
PROCESS_IDENTIFIER="gunicorn"

# --- Deployment Script ---
echo "Starting deployment..."

# Navigate to the project directory
cd "$PROJECT_DIR" || { echo "Error: Directory $PROJECT_DIR not found."; exit 1; }

# Pull the latest changes from the master branch
echo "Pulling latest changes..."
git pull origin master

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install or update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run tests before deploying.
echo "Running tests..."
pytest --maxfail=1 --disable-warnings -q

# Stop any existing instance of the app (Gunicorn)
echo "Stopping any running Gunicorn instance..."
pkill -f "$PROCESS_IDENTIFIER" || echo "No running instance found."

echo "Starting the application using Gunicorn..."
nohup gunicorn --workers 2 --bind 0.0.0.0:5000 run:app --access-logfile - --error-logfile - --log-level debug &

echo "Deployment complete! Your app should now be running."

# See the logs
echo "Tailing logs (press Ctrl+C to exit)..."
tail -f nohup.out
