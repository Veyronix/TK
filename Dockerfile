FROM ubuntu:18.04
ADD . /backend
WORKDIR /backend

RUN apt-get update -qq && apt-get -y install \
      autoconf \
      python3-pip \
      ffmpeg

RUN pip3 install -r requirements.txt
CMD ["python3", "backend/main.py"] 
