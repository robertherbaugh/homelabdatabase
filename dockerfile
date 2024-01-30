# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
#RUN apt-get update && apt-get -y install libq-dev gcc
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=hmlsvcr.settings

# Copy entrypoint script into the container
COPY entrypoint.sh /usr/src/app/entrypoint.sh

# Copy the create user script into the container
COPY create_superuser.py /usr/src/app/

# Set script as entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]