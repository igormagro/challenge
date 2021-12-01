# Docker image [gcp]
FROM gcr.io/spark-operator/spark-py:v3.0.0
LABEL Mantainers: Igor Magro
  
# Using root user
USER root:root
 
# Create directory for apps
RUN mkdir -p /app

#Copy Jars to RUN 
COPY ./jars/ /opt/spark/jars
  
# Set work directory
WORKDIR /app
  
# User 
USER root