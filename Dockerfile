FROM tensorflow/tensorflow:1.15.4-gpu-py3
#FROM ubuntu:18.04

WORKDIR /

RUN apt update
RUN apt install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg wget git vim nano

RUN git clone https://github.com/Rayhane-mamah/Tacotron-2.git
RUN git clone https://github.com/aleksas/wavenet_vocoder_liepa.git
RUN git clone https://github.com/aleksas/liepa_dataset

#RUN apt -y install python3.7 python3-pip
#RUN rm /usr/bin/python3
#RUN ln -s /usr/bin/python3.7 /usr/bin/python3
#RUN ln -s /usr/bin/python3 /usr/bin/python

#RUN pip3 install llvmlite==0.31.0 numpy

WORKDIR /liepa_dataset
RUN pip3 install -r requirements.txt

RUN python get_liepa.py
RUN python clean_syn.py -ax

