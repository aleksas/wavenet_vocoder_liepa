# Wavenet vocoder training and evaluation
## Preprocess
`python preprocess.py liepa_multi ./db/Garsynas/ ./db/proc/Garsynas --preset=presets/liepa_multi.json`

Resulting [train.txt](experiment/liepa_2008.05.11/db/proc/Garsynas/train.txt) containing list of utterance transcriptions for corresponding speaker.

## Train
`python train.py --data-root=./db/proc/Garsynas --preset=presets/liepa_multi.json`

## Evaluate
```
python evaluate.py checkpoints/checkpoint_step000590000_ema.pth \
  ./generated/Garsynas_multi_eval --data-root=./db/proc/Garsynas/ \
  --preset=presets/liepa_multi.json --output-html --num-utterances=1
```

## Fine tune
```
python train.py --data-root=./db/proc/Garsynas/ \
  --checkpoint-dir=checkpoints/fine_tune \
  --restore-parts=checkpoints/checkpoint_step000590000_ema.pth
```
