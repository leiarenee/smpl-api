# Base image Amazon Linux2
FROM public.ecr.aws/amazonlinux/amazonlinux

# Install python3
RUN yum update -y
RUN yum install -y python3

# Install Virtualenv
RUN pip3 install virtualenv

# Install Git
RUN yum install -y git

RUN pwd
RUN ls -la

# Clone Repository
RUN mkdir app && cd app && git clone https://github.com/leiarenee/tmnl-app.git

# Set Working Directory
WORKDIR /app/tmnl-app

# Activate virtualenv
RUN virtualenv -p python3 venv
RUN source venv/bin/activate

# List currentdir
RUN pwd && ls -la

# Install python packages
RUN pip3 install -r requirements.txt

# Setup environment variables
ENV PYTHONPATH=src:test

# Set Entry Point command
ENTRYPOINT [ "python3" ]

# Set Arguments
CMD [ "-m", "flaskapi" ]





