FROM python:3.8-slim as data_copier

WORKDIR /

RUN apt update
RUN apt install -y git libsndfile1
RUN git clone https://github.com/aleksas/liepa_dataset

WORKDIR /liepa_dataset
RUN pip install -r requirements.txt

RUN python get_liepa.py
RUN python clean_syn.py -ax

FROM tensorflow/tensorflow:1.12.3-gpu-py3 AS data_preprocessor

RUN apt update
RUN apt install -y libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg wget git vim nano

WORKDIR /

ARG VOICE=Regina
ENV VOICE=$VOICE

RUN git clone https://github.com/aleksas/liepa_dataset
RUN git clone https://github.com/aleksas/Tacotron-2.git -b "utf-stress"
RUN git clone https://github.com/aleksas/wavenet_vocoder_liepa.git

WORKDIR /Tacotron-2
COPY --from=data_copier /liepa_dataset/MII_LIEPA_SYN_V1/$VOICE ./$VOICE

RUN cp /liepa_dataset/other/regina_transcript_stressed_v2_utf.txt ./$VOICE
RUN mv ./$VOICE/regina_transcript_stressed_v2_utf.txt ./$VOICE/db_tr.txt

RUN pip install llvmlite==0.31.0 chardet keras==2.2.1
RUN pip install -r requirements.txt
RUN python preprocess.py --dataset="liepa-multi" --voice="$VOICE"
