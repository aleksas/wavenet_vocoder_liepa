FROM python:3.8-slim as data_provider

WORKDIR /

RUN apt update
RUN apt install -y git libsndfile1
RUN git clone https://github.com/aleksas/liepa_dataset

WORKDIR /liepa_dataset
RUN pip install -r requirements.txt

RUN python get_liepa.py
RUN python clean_syn.py -ax

# Replace image according to CUDA driver
FROM switchwang/pytorch:v1.6.0-cuda10.2-cudnn7-ubuntu18.04-devel
ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}

RUN apt-get update -y
RUN apt install -y git

ARG VOICE=Regina
ENV VOICE=$VOICE

RUN git clone https://github.com/aleksas/tacotron2

WORKDIR /workspace/tacotron2
COPY --from=data_provider /liepa_dataset/MII_LIEPA_SYN_V1/$VOICE ./$VOICE

RUN pip install numpy scipy matplotlib librosa==0.6.0 tensorflow==1.13.1 tensorboardX==1.6 inflect==0.2.5 Unidecode==1.0.22 pillow jupyter

ENV CUDA_HOME=/usr/local/cuda

WORKDIR /
RUN git clone https://github.com/NVIDIA/apex
WORKDIR /apex
RUN pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./

# ADJUSTMENTS
RUN pip install numba==0.48 tensorboard==1.15

WORKDIR /workspace/tacotron2

#RUN python train.py --output_directory=outdir --log_directory=logdir
