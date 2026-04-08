# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create the reports directory and change ownership
RUN mkdir -p reports && chown -R app:app /app

# Switch to the non-root user
USER app

# Define environment variable for OpenAI API key (should be passed at runtime)
ENV OPENAI_API_KEY=""
ENV GITHUB_TOKEN=""
ENV REPO_NAME=""

# Run the application when the container launches
CMD ["python", "github_issue_analyzer.py"]
