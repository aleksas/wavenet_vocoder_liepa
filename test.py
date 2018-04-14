#!/usr/bin/python

import os
import codecs

db_dir = '/home/aleksas/db/MII/LIEPA'
audio_subdir = 'Garsynas'
transcript_subdir = 'Anotacijos_UNICODE'
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

def test_dir(db_dir):
    global audio_subdir, unicode_transcript_subdir, meta

    wav_dir = '%s/%s' % (db_dir, audio_subdir)
    transcript_dir = '%s/%s' % (db_dir, transcript_subdir)

    for root, dirs, files in os.walk(wav_dir):
        path = root.split(os.sep)
        #print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            if file.endswith( ('.wav','.WAV') ):
                tr_path = '%s/%s' % (transcript_dir, file.replace('.wav', '.txt'))
                #print(len(path) * '---', file)
                #print (tr_path)

                with codecs.open(tr_path, encoding="utf-16le") as fin:
                    content = fin.read()
                    for m in meta:
                        content = content.replace(m, '')
                    for mm_p, mm_r in meta_m:
                        content = content.replace(mm_p, mm_r)
                    if '_' in content:
                        print (content)
                        print (tr_path)
                        print ()
                break

if __name__ == '__main__':
    test_dir( db_dir )
