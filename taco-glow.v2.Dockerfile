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

RUN conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch
RUN conda install -c pytorch magma-cuda102

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys DE19EB17684BA42D
RUN apt-get update -y
RUN apt install -y git

ARG VOICE=Regina
ENV VOICE=$VOICE

RUN git clone https://github.com/aleksas/tacotron2 -b liepa

WORKDIR /workspace/tacotron2
RUN git submodule init; git submodule update
COPY --from=data_provider /liepa_dataset/MII_LIEPA_SYN_V1/$VOICE ./$VOICE
WORKDIR ./$VOICE
RUN wget https://raw.githubusercontent.com/aleksas/liepa_dataset/master/other/regina_transcript_stressed_v2_utf.txt
WORKDIR /workspace/tacotron2
RUN python prepare_liepa.py --voice=Regina --transcript-list=regina_transcript_stressed_v2_utf.txt

#RUN sed -i -- 's,DUMMY,ljs_dataset_folder/wavs,g' filelists/*.txt
RUN pip install numpy scipy matplotlib librosa==0.6.0 tensorflow==1.13.1 tensorboardX==1.6 inflect==0.2.5 Unidecode==1.0.22 numba==0.48 tensorboard==1.15 pillow jupyter

ENV CUDA_HOME=/usr/local/cuda

WORKDIR /
RUN git clone https://github.com/NVIDIA/apex
WORKDIR /apex
RUN pip install -v --disable-pip-version-check --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./

WORKDIR /workspace/tacotron2
#RUN sed -i 's|Regina/|Regina/data/|g' filelists/Liepa_Regina_audio_text_*.txt
RUN mkdir logs
#RUN python train.py --output_directory=outdir --log_directory=logdir
# python -m multiproc train.py --output_directory=outdir --log_directory=logdir --hparams=distributed_run=True,fp16_run=True
#RUN python -m multiproc train.py --output_directory=outdir --log_directory=logdir --hparams=distributed_run=True
