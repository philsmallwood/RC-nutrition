### Python App Docker Image

### Stage 1 
FROM python:3.13-slim AS builder

# Create App Directory
WORKDIR /app

# Set API Token
ARG API_TOKEN

# Install Build Dependencies
RUN true \
    && apt-get update \
    && apt-get install -y \
    git

# Copy Git Repo
RUN git clone https://${API_TOKEN}@git.redclay.k12.de.us/Philip.Smallwood/RC-nutrition .

# Checkout Repo
RUN git checkout docker 

# Create Python Virtualenv
RUN python -m venv venv

# Configure Python Virtualenv
RUN . venv/bin/activate && \
    pip install --no-cache-dir \
        -r ./requirements.txt \
        --extra-index-url https://${API_TOKEN}@git.redclay.k12.de.us/api/packages/Philip.Smallwood/pypi/simple

### Stage 2
FROM python:3.13-slim

# Install Run Dependencies
RUN true \
    && apt-get update \
    && apt-get install -y \
    cron \
    tzdata

# Upgrade Pip
RUN pip3 install --upgrade pip

# Set Time Zone
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy App to Directory
WORKDIR /app

COPY --from=builder /app/ /app/

# Create Config Directory
WORKDIR /config_files

RUN mkdir -p ./key_file

RUN mkdir -p ./env_file

RUN mkdir -p ./export_files

# Create Cron Job Directory
RUN mkdir -p /etc/cron.d

ENTRYPOINT [ "cron", "-f" ]