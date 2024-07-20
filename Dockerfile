# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files, excluding .streamlit
COPY fake-detector.py .

EXPOSE 8501

# Run the application
CMD ["streamlit", "run", "fake-detector.py", "--server.port=8501", "--server.address=0.0.0.0"]
