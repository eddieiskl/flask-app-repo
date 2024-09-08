# Use the slim version of Python 3.8
FROM python:3.8-slim

# Install required Python packages
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Install Selenium and the browser driver (e.g., ChromeDriver)
RUN pip install selenium
RUN apt-get update && apt-get install -y wget unzip
RUN wget https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/local/bin/

# Copy the application files into the container
COPY . /app

# Set the working directory inside the container
WORKDIR /app

# Expose the correct port (8777)
EXPOSE 8777

# Run the Flask application using MainScores.py on port 8777
CMD ["python", "MainScores.py"]