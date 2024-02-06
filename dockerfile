# Use an official Python runtime as a parent image
FROM python:alpine

# Install build dependencies for Python packages with native extensions
RUN apk add --no-cache build-base libffi-dev openssl-dev python3-dev

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
#RUN apt-get update && apt-get -y install libq-dev gcc
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install django-cors-headers

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=hmlsvcr.settings

# Copy the entrypoint script into the container and set execute permissions
#COPY entrypoint.sh /usr/src/app/entrypoint.sh
#RUN chmod +x /usr/src/app/entrypoint.sh

# Copy the create user script into the container
COPY create_superuser.py /usr/src/app/

# Remove the ENTRYPOINT line
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Change CMD to execute the script directly
#CMD ["sh", "/usr/src/app/entrypoint.sh"]

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
