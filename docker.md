# Docker environment
## Run
Runs: 4
`nvidia-docker run -t -i -p 6006:6006 -v ~/labs/liepa_dataset/MII_LIEPA_SYN_V1:/MII_LIEPA_SYN_V1 -v ~/labs/wavenet_vocoder:/wavenet_vocoder wavenet_vocoder_liepa:gpu bash`
Runs: 1, 2, 3
`nvidia-docker run -t -i -p 6006:6006 -v ~/labs/wavenet_vocoder:/wavenet_vocoder wavenet_vocoder_liepa:gpu bash`
