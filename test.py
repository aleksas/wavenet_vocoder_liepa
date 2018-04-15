#!/usr/bin/python

import os
import codecs
import chardet

db_dir = '/home/aleksas/labs/wavenet_vocoder/db/Garsynas'
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
    global meta, meta_m, speaker

    for root, dirs, files in os.walk(db_dir):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        print(root)
        for file in files:
            if file.endswith( '.wav' ):
                tr_file = file.replace('.wav','.txt')
                tr_path = os.path.join(root, tr_file)
                #print(len(path) * '---', file)
                #print (tr_path)

                rawdata = open(tr_path, 'rb').read()
                result = chardet.detect(rawdata)
                charenc = result['encoding']
                
                if charenc == 'UTF-16':
                    charenc = "utf-16le"
                elif charenc == 'ISO-8859-1':
                    charenc = 'windows-1257'

                with codecs.open(tr_path, encoding=charenc) as fin:
                    content = fin.read()
                    for m in meta:
                        content = content.replace(m, '')
                    for mm_p, mm_r in meta_m:
                        content = content.replace(mm_p, mm_r)

                    if '-' in content or '-' in content:
                        print (content)
                    print (content)
                    print()

if __name__ == '__main__':
    test_dir( db_dir )
