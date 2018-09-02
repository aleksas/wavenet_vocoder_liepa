## RUN DOCKER

> nvidia-docker run -ti -p 6006:6006 \
>     -v ~/labs/wavenet_vocoder:/wavenet_vocoder \
>     -v ~/labs/liepa_dataset/MII_LIEPA_SYN_V1:/MII_LIEPA_SYN_V1\
>     wavenet_vocoder_liepa:gpu bash

## PREPROCESS

> python preprocess.py liepa /MII_LIEPA_SYN_V1 /MII_LIEPA_SYN_V1/proc/ --preset=presets/liepa_mixture.json

## Tensorboard

> pkill -f "tensorboard"

tensorboard --logdir=./log &

## TRAIN

> python train.py --data-root=/MII_LIEPA_SYN_V1/proc/ --preset=presets/liepa_mixture.json

## RESUME

> python train.py --data-root=/MII_LIEPA_SYN_V1/proc/ --preset=presets/liepa_mixture.json \
>   --checkpoint-dir=/wavenet_vocoder/checkpoints_fine \
>   --log-event-path=./log/run-test2018-09-
>   --checkpoint=/wavenet_vocoder/checkpoints/checkpoint_step000000835.pth

## FINETUNE

> python train.py --data-root=/MII_LIEPA_SYN_V1/proc_4/ \
>   --preset=presets/liepa_mixture.json \
>   --checkpoint-dir=/wavenet_vocoder/checkpoints_fine \
>   --log-event-path=./log/run-test2018-08-31_09:00:00.000000 \
>   --restore-parts=/wavenet_vocoder/checkpoints/checkpoint_step00

## EVALUATE

> python evaluate.py checkpoints_fine/checkpoint_step000210000_ema.pth \
>  ./eval/checkpoint_step000210000_ema/speaker_0 \
>  --data-root=/MII_LIEPA_SYN_V1/proc_4/  \
>  --preset=./presets/liepa_mixture.json \
>  --output-html --num-utterances=3 --speaker-id=0

> python evaluate.py checkpoints_fine/checkpoint_step000210000_ema.pth \
>  ./eval/checkpoint_step000210000_ema/speaker_1 \
>  --data-root=/MII_LIEPA_SYN_V1/proc_4/  \
>  --preset=./presets/liepa_mixture.json \
>  --output-html --num-utterances=3 --speaker-id=1

> python evaluate.py checkpoints_fine/checkpoint_step000210000_ema.pth \
>  ./eval/checkpoint_step000210000_ema/speaker_2 \
>  --data-root=/MII_LIEPA_SYN_V1/proc_4/  \
>  --preset=./presets/liepa_mixture.json \
>  --output-html --num-utterances=3 --speaker-id=2

> python evaluate.py checkpoints_fine/checkpoint_step000210000_ema.pth \
>  ./eval/checkpoint_step000210000_ema/speaker_3 \
>  --data-root=/MII_LIEPA_SYN_V1/proc_4/  \
>  --preset=./presets/liepa_mixture.json \
>  --output-html --num-utterances=3 --speaker-id=3
