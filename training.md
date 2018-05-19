# Wavenet vocoder training and evaluation
## Preprocess
python preprocess.py liepa_multi ./db/Garsynas/ ./db/proc/Garsynas --preset=presets/liepa_multi.json
## Train
python train.py --data-root=./db/proc/Garsynas --preset=presets/liepa_multi.json
## Evaluate
python evaluate.py checkpoints/checkpoint_step000590000_ema.pth ./generated/Garsynas_multi_eval --data-root=./db/proc/Garsynas/ --preset=presets/liepa_multi.json --output-html --num-utterances=1
