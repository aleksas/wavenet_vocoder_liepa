
FROM python:3.8-slim as data_provider

WORKDIR /

RUN apt update
RUN apt install -y git libsndfile1
RUN git clone https://github.com/aleksas/liepa_dataset

WORKDIR /liepa_dataset
RUN pip install -r requirements.txt

RUN python get_liepa.py
RUN python clean_syn.py -ax

FROM pytorch/pytorch:nightly-devel-cuda10.0-cudnn7 AS trainer
ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}

RUN apt-get update -y
RUN apt install -y git

ARG VOICE=Regina
ENV VOICE=$VOICE

RUN git clone https://github.com/aleksas/tacotron2

WORKDIR /tacotron2
COPY --from=data_provider /liepa_dataset/MII_LIEPA_SYN_V1/$VOICE ./$VOICE

RUN pip install numpy scipy matplotlib librosa==0.6.0 tensorflow tensorboardX inflect==0.2.5 Unidecode==1.0.22 pillow jupyter
RUN pip install torch

WORKDIR /
RUN git clone https://github.com/NVIDIA/apex
WORKDIR /apex
RUN pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./

RUN python train.py --output_directory=outdir --log_directory=logdir