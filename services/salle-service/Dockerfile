FROM python:3.10-slim

# Set environment variables to ensure correct encoding for Python
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Set the working directory inside the container
WORKDIR /app

# Copy the entire application code to the container
COPY . /app

# Install the dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on
EXPOSE 5002

# Run the Flask app when the container starts
CMD ["python", "app.py"]

