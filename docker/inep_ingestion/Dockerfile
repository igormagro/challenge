FROM python:3.8-rc-slim-buster
LABEL MANTAINER: Igor Magro

RUN apt-get update

# Create directories
RUN mkdir -p /opt/app

# Copy requirements.txt
COPY requirements.txt requirements.txt
RUN pip install --no-cache -r requirements.txt

COPY ./src /opt/app

# Set app as working directory
WORKDIR /opt/app
  
ENTRYPOINT ["python"]