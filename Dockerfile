# FROM tensorflow/magenta

# note: run `export DOCKER_BUILDKIT=0` before building

FROM ubuntu:20.04
# FROM python:3.7

# RUN apt-get update -qq && apt-get install -qq libfluidsynth1 build-essential libasound2-dev libjack-dev apt-transport-https ca-certificates gnupg curl python3-pip

RUN apt update -qq && DEBIAN_FRONTEND=noninteractive apt install -y -qq libfluidsynth2 build-essential libasound2-dev libjack-dev apt-transport-https ca-certificates gnupg curl python3-pip
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
RUN apt update -qq && apt install -y -qq google-cloud-sdk
# RUN pip install --upgrade pip
# RUN pip3 install setuptools 
RUN pip3 install magenta pyfluidsynth ipython
RUN gsutil -m cp gs://download.magenta.tensorflow.org/soundfonts/Yamaha-C5-Salamander-JNv5.1.sf2 /tmp/

WORKDIR /tmp
RUN curl -O http://download.magenta.tensorflow.org/models/performance_with_dynamics.mag

# should be mounted by container
WORKDIR /work


CMD "./doit.py"


