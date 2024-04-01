FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt install -y \
    python3-pyside2.qtwebenginewidgets git make binutils \
    wget && apt install -y --no-install-recommends python3-pip
RUN pip3 install pyinstaller
RUN git config --global --add safe.directory /app
