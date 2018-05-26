from concurrent.futures import ProcessPoolExecutor
from functools import partial
import numpy as np
import os
import audio
from nnmnkwii import preprocessing as P
from hparams import hparams
from os.path import exists
import librosa

import codecs
import chardet
from datasets import liepa

from wavenet_vocoder.util import is_mulaw_quantize, is_mulaw, is_raw

from hparams import hparams

meta = [
    '_nurijimas', '_pilvas', '_pauze', '_tyla',
    '_ikvepimas', '_iskvepimas', '_garsas',
    '_puslapis', '_puslpais', '_kede', '_durys',
    '_cepsejimas'
]

meta = []

meta_m = [
    ('septyni_ty', 'septyni'), ('aštuoni_tuo', 'aštuoni'), ('devyni_vy','devyni'),
    ('pirma_pir', 'pirma'), ('antra_an', 'antra'), ('trečia_tre', 'trečia'),
    ('ketvirta_vir', 'ketvirta'), ('penkta_pen', 'penkta'), ('šešta_šeš', 'šešta'),
    ('septinta_tin', 'septinta'), ('aštunta_tun', 'aštunta'), ('devinta_vin', 'devinta'),
    ('dešimta_ši', 'dešimta'), ('procentų_cen', 'procentų'), ('vadinamaa_maa','vadinama'),
    ('aplankų_ap', 'aplankų'), ('veiklų_veik', 'veiklų'), ('_įtrūkimu', 'įtrūkimu'),
    ('sugriauta_ta', 'sugriauta'), ('laikomi_mi', 'laikomi'), ('siauros_siau', 'siauros'),
    ('_padpadėtis', 'padpadėtis'), ('_klėstinčiu', 'klėstinčiu'), ('langus_gus', 'langus'),
    ('eštuoni_tuo', 'aštuoni'), ('architektūra_tū', 'architektūra'), ('rezultatus_ta', 'rezultatus'),
    ('ketvyrta_vyr', 'ketvyrta'), ('_koplystulpiai', 'koplystulpiai')
]

def _preprocess_utterance(out_dir, index, speaker_id, wav_path, text):
    sr = hparams.sample_rate

    # Load the audio to a numpy array. Resampled if needed
    wav = audio.load_wav(wav_path)

    wav, _ = librosa.effects.trim(wav, top_db=20)

    if hparams.rescaling:
        wav = wav / np.abs(wav).max() * hparams.rescaling_max

    # Mu-law quantize
    if is_mulaw_quantize(hparams.input_type):
        # [0, quantize_channels)
        out = P.mulaw_quantize(wav, hparams.quantize_channels)

        # Trim silences
        start, end = audio.start_and_end_indices(out, hparams.silence_threshold)
        wav = wav[start:end]
        out = out[start:end]
        constant_values = P.mulaw_quantize(0, hparams.quantize_channels)
        out_dtype = np.int16
    elif is_mulaw(hparams.input_type):
        # [-1, 1]
        out = P.mulaw(wav, hparams.quantize_channels)
        constant_values = P.mulaw(0.0, hparams.quantize_channels)
        out_dtype = np.float32
    else:
        # [-1, 1]
        out = wav
        constant_values = 0.0
        out_dtype = np.float32

    # Compute a mel-scale spectrogram from the trimmed wav:
    # (N, D)
    mel_spectrogram = audio.melspectrogram(wav).astype(np.float32).T
    # lws pads zeros internally before performing stft
    # this is needed to adjust time resolution between audio and mel-spectrogram
    l, r = audio.lws_pad_lr(wav, hparams.fft_size, audio.get_hop_size())

    # zero pad for quantized signal
    out = np.pad(out, (l, r), mode="constant", constant_values=constant_values)
    N = mel_spectrogram.shape[0]
    assert len(out) >= N * audio.get_hop_size()

    # time resolution adjustment
    # ensure length of raw audio is multiple of hop_size so that we can use
    # transposed convolution to upsample
    out = out[:N * audio.get_hop_size()]
    assert len(out) % audio.get_hop_size() == 0

    timesteps = len(out)

    # Write the spectrograms to disk:
    audio_filename = 'liepa-audio-%05d.npy' % index
    mel_filename = 'liepa-mel-%05d.npy' % index
    np.save(os.path.join(out_dir, audio_filename),
            out.astype(out_dtype), allow_pickle=False)
    np.save(os.path.join(out_dir, mel_filename),
            mel_spectrogram.astype(np.float32), allow_pickle=False)

    # Return a tuple describing this training example:
    return (audio_filename, mel_filename, timesteps, text, speaker_id)

def build_from_path(in_dir, out_dir, num_workers=1, tqdm=lambda x: x):
    executor = ProcessPoolExecutor(max_workers=num_workers)
    futures = []

    speakers = liepa.available_speakers

    wd = liepa.WavFileDataSource(in_dir, speakers=speakers)
    wav_paths = wd.collect_files()
    speaker_ids = wd.labels

    for index, (speaker_id, wav_path) in enumerate(
            zip(speaker_ids, wav_paths)):


        txt_path = wav_path.replace('.wav','.txt')

        raw_text = None
        with open(txt_path, 'rb') as f:
            raw_text = f.read()

        result = chardet.detect(raw_text)
        charenc = result['encoding']

        if charenc == 'UTF-16':
            charenc = "utf-16le"
        elif charenc == 'ISO-8859-1':
            charenc = 'windows-1257'

        with codecs.open(txt_path, encoding=charenc) as fin:
            text = fin.read()
            for m in meta:
                text = text.replace(m, '')
            for mm_p, mm_r in meta_m:
                text = text.replace(mm_p, mm_r)
            text = text.replace('\n', ' ').replace('\r', '').strip()

        futures.append(executor.submit(
            partial(_preprocess_utterance, out_dir, index + 1, speaker_id, wav_path, text)))
    return [future.result() for future in tqdm(futures)]
