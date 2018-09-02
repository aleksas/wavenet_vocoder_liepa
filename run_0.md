**Train** new model from start conditioning on 9 speakers.
As a result one can understand the spoken language but disturbances are too obvious.
Additionally speaker 12: D17 had originally too high noise level that was not cleaned up automaticcaly, thus has to be replaced with another speaker.


### Experiment evaluation results

Following utterances are generated using `evaluate.py` script. First raw represents **predicted** utternace and the second is **ground truth** | **target**.

Speaker 7 utterance 0
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker7_0_checkpoint_step000590000_ema_predicted.wav" autoplay/>Your browser does not support the audio element.</audio>
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker7_0_checkpoint_step000590000_ema_target.wav" autoplay/>Your browser does not support the audio element.</audio>

Speaker 12 utterance 2
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker12_2_checkpoint_step000590000_ema_predicted.wav" autoplay/>Your browser does not support the audio element.</audio>
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker12_2_checkpoint_step000590000_ema_target.wav" autoplay/>Your browser does not support the audio element.</audio>

Speaker 4 utterance 3
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker4_3_checkpoint_step000590000_ema_predicted.wav" autoplay/>Your browser does not support the audio element.</audio>
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker4_3_checkpoint_step000590000_ema_target.wav" autoplay/>Your browser does not support the audio element.</audio>

Speaker 11 utterance 4
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker11_4_checkpoint_step000590000_ema_predicted.wav" autoplay/>Your browser does not support the audio element.</audio>
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker11_4_checkpoint_step000590000_ema_target.wav" autoplay/>Your browser does not support the audio element.</audio>

Speaker 3 utterance 5
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker3_5_checkpoint_step000590000_ema_predicted.wav" autoplay/>Your browser does not support the audio element.</audio>
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker3_5_checkpoint_step000590000_ema_target.wav" autoplay/>Your browser does not support the audio element.</audio>

Speaker 15 utterance 10
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker15_10_checkpoint_step000590000_ema_predicted.wav" autoplay/>Your browser does not support the audio element.</audio>
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker15_10_checkpoint_step000590000_ema_target.wav" autoplay/>Your browser does not support the audio element.</audio>

Speaker 17 utterance 17
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker17_17_checkpoint_step000590000_ema_predicted.wav" autoplay/>Your browser does not support the audio element.</audio>
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker17_17_checkpoint_step000590000_ema_target.wav" autoplay/>Your browser does not support the audio element.</audio>

Speaker 1 utterance 23
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker1_23_checkpoint_step000590000_ema_predicted.wav" autoplay/>Your browser does not support the audio element.</audio>
- <audio controls="controls" ><source src="/wavenet_vocoder_liepa/experiment/liepa_2008.05.11/audio/speaker1_23_checkpoint_step000590000_ema_target.wav" autoplay/>Your browser does not support the audio element.</audio>

### Speakers
The speaker indeces correspond to speker directories in Liepa database in order specified in [dataset](experiment/liepa_2008.05.11/datasets/liepa.py) (See var. available_speakers). Notice that only speakers with sentence utterances were considered.

- 1: D150
- 2: D36
- 3: D52
- 4: D54
- 7: D37
- 11: D51
- 12: D17
- 15: D56
- 17: D79