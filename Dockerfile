# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir  -r requirements.txt
RUN pip uninstall PIL
RUN pip install  Pillow


COPY .. /code/