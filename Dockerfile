FROM python:slim

RUN apt update && apt install -y ffmpeg imagemagick cron

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x run.sh

ENTRYPOINT ["/bin/sh", "-c", "./run.sh"]
