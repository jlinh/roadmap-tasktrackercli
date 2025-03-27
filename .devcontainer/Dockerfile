FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install git \
    && pip install -r requirements.txt