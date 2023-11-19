FROM jenkins/jenkins:latest
USER root

RUN mkdir /my_application
WORKDIR /my_application
RUN pwd
RUN ls -la
# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3-pip && \
    apt-get install -y python3-venv

# Check if Python is installed
RUN python3 --version

# Check if pip is installed
RUN pip3 --version

USER jenkins
