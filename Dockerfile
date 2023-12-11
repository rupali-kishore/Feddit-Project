FROM python:3.8.10-slim

WORKDIR /app 

COPY . /app

#Command to install dependancies in the docker image
RUN pip install -r requirements.txt
 
