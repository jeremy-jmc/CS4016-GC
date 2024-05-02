FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

RUN apt-get update -y \
    && apt-get install -y wget ffmpeg colmap unzip \
    && apt-get clean

WORKDIR /app

COPY . /app

CMD ["bash"]

# docker build -t gs .
# docker run --name gs_container --gpus all -v /teamspace/studios/this_studio/gaussian-splatting:/app -it gs bash

