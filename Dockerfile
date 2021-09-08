# Base Image
FROM python:3.8
#set working directory
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
COPY ./constancy_brokers/ /app/
COPY manage.py /app/

# set default environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DATABASE_URL "constancy_brokers://constancy_brokers:password@postgres:5432/constancy_brokers_database"
ENV SECRET_KEY "vagg3miefyg8t52m6i-rhrn%rrc_0s(ql&eq8!)j3qxv#f1+3$"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install environment dependencies
RUN pip3 install --upgrade pip 

# install dependencies
RUN pip install -r requirements.txt
