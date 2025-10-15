# Use a specific, stable version of the python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the watcher script
COPY watcher.py .

# The command to run when the container starts (-u for unbuffered output)
CMD ["python", "-u", "watcher.py"]
