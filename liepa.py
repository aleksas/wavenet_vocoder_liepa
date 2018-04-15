from concurrent.futures import ProcessPoolExecutor
from functools import partial
import numpy as np
import os
import audio
import codecs
import chardet

from nnmnkwii import preprocessing as P
from hparams import hparams
from os.path import exists
import librosa

from wavenet_vocoder.util import is_mulaw_quantize, is_mulaw, is_raw

from hparams import hparams

meta = [
    '_nurijimas', '_pilvas', '_pauze', '_tyla',
    '_ikvepimas', '_iskvepimas', '_garsas',
    '_puslapis', '_puslpais', '_kede', '_durys',
    '_cepsejimas'
]
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


def build_from_path(in_dir, out_dir, num_workers=1, tqdm=lambda x: x):
    global meta, meta_m, speaker

    executor = ProcessPoolExecutor(max_workers=num_workers)
    futures = []
    index = 1

    for root, dirs, files in os.walk(in_dir):
        path = root.split(os.sep)

        for file in files:
            if file.endswith( '.wav' ):
                tr_file = file.replace('.wav','.txt')
                tr_path = os.path.join(root, tr_file)
                wav_path = os.path.join(root, file)

                rawdata = open(tr_path, 'rb').read()
                result = chardet.detect(rawdata)
                charenc = result['encoding']

                if charenc == 'UTF-16':
                    charenc = "utf-16le"
                elif charenc == 'ISO-8859-1':
                    charenc = 'windows-1257'

                with codecs.open(tr_path, encoding=charenc) as fin:
                    text = fin.read()
                    for m in meta:
                        text = text.replace(m, '')
                    for mm_p, mm_r in meta_m:
                        text = text.replace(mm_p, mm_r)
                    text = text.replace('\r', '')
                    text = text.replace('\n', ' ')

                    futures.append(executor.submit(
                        partial(_process_utterance, out_dir, index, wav_path, text)))
                index += 1
    return [future.result() for future in tqdm(futures)]


def _process_utterance(out_dir, index, wav_path, text):
    # Load the audio to a numpy array:
    wav = audio.load_wav(wav_path)

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
    audio_filename = 'ljspeech-audio-%05d.npy' % index
    mel_filename = 'ljspeech-mel-%05d.npy' % index
    np.save(os.path.join(out_dir, audio_filename),
            out.astype(out_dtype), allow_pickle=False)
    np.save(os.path.join(out_dir, mel_filename),
            mel_spectrogram.astype(np.float32), allow_pickle=False)

    # Return a tuple describing this training example:
    return (audio_filename, mel_filename, timesteps, text)
