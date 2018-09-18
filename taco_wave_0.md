# 2018.09.17 Tacotron 2 + Wavenet

Speaker 0 (Regina)

Initial problems with:
- Embedding settings for wavenet. Missed setting gin_channels parameter, which defines embedding layer size (for multiple voices).
- Dataset preprocessed with different parameters. Wavenet with fmin 125 and taco with fmin 0, which caused voice pitch shift.

## Text lines

- Sveiki, draugai
- Aš robotas iš ateities
- Aš žinau jūsų likimą

## Gin 16, 130000 Step

- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/gin16_130k/0.wav" autoplay/>Your browser does not support the audio element\.</audio>
- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/gin16_130k/1.wav" autoplay/>Your browser does not support the audio element\.</audio>
- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/gin16_130k/2.wav" autoplay/>Your browser does not support the audio element\.</audio>

## Gin 16, 270000 Step, taco 100000 step

- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/gin16_270k/0.wav" autoplay/>Your browser does not support the audio element\.</audio>
- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/gin16_270k/1.wav" autoplay/>Your browser does not support the audio element\.</audio>
- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/gin16_270k/2.wav" autoplay/>Your browser does not support the audio element\.</audio>

## Gin 16, wavenet 2780000 Step, taco 110000 step

- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/gin16_280k/0.wav" autoplay/>Your browser does not support the audio element\.</audio>
- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/gin16_280k/1.wav" autoplay/>Your browser does not support the audio element\.</audio>
- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/gin16_280k/2.wav" autoplay/>Your browser does not support the audio element\.</audio>

## No wavenet embedding

- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/ginNone/0.wav" autoplay/>Your browser does not support the audio element\.</audio>
- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/ginNone/1.wav" autoplay/>Your browser does not support the audio element\.</audio>
- <audio controls="controls" ><source src="./experiment/taco_wave_2018.09.17/ginNone/2.wav" autoplay/>Your browser does not support the audio element\.</audio>






