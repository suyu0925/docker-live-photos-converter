FROM python:slim

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
  && apt update \
  && apt install -y ffmpeg cron

RUN apt install -y g++ wget cmake libde265-dev libx265-dev libjpeg-dev libpng-dev libtool libxml2-dev libzip-dev libgdk-pixbuf2.0-dev \
  && wget https://github.com/strukturag/libheif/releases/download/v1.18.2/libheif-1.18.2.tar.gz \
  && tar -xvf libheif-1.18.2.tar.gz \
  && cd libheif-1.18.2 \
  && mkdir build \
  && cd build \
  && cmake --preset=release .. \
  && make \
  && make install

# install imagemagick after libheif
RUN apt install -y imagemagick

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN sed -i 's/\r//' run.sh && chmod +x run.sh

ENTRYPOINT ["/bin/sh", "-c", "./run.sh"]
