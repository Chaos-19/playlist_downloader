# Step 1: Use an official Python image as a base image
FROM python:3.12-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy your application files into the container
COPY . /app

# Step 4: Install the required Python dependencies
RUN pip install -r requirements.txt

# Step 5: Expose port 5000 (Flask default port)
EXPOSE 5000

# Step 6: Run the Flask app when the container starts
CMD ["python", "app.py"]