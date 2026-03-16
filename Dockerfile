CHANGER LA VERSION DE PYTHON CARD AIRFLOW 2.9.3 NEST PAS COMPATIBLE AVEC PYTHON 3.10, DONC PASSER A PYTHON 3.11

FROM python:3.11
# Use an official Python runtime as a parent image 

LABEL "Build de l'application meteo-vs-transports" 

# Set the working directory to /app
WORKDIR /app 

# Copy the current directory contents into the container at /app 
COPY . /app 

# Install any needed packages specified in requirements.txt 
RUN pip install -r requirements.txt 

# Make port 80 available to the world outside this container 
EXPOSE 80 
# Define environment variable 
ENV NAME=World

# Run app.py when the container launches 
CMD ["python", "app.py"]

FROM apache/airflow:2.9.3 

COPY requirements.txt / 

RUN pip install --no-cache-dir -r /requirements.txt 
