# Module: KEYS-L3
# Created on: 11-10-2021, modified 1/17/23 for l3dl-re
# Authors: -∞WKS∞- , r3n

# Search for licence url inside https://playback.prod.hjholdings.tv/session/open/v1/merchants/hulu/medias/8ad92b4cef1f4349804f2304e48031be?viewing_url=https%3A%2F%2Fwww.hulu.jp%2Fwatch%2F100214258&user_id=XXXXXX&codecs=avc

# Example mpd: https://manifest.streaks.jp/v3/hulu/8ad92b4cef1f4349804f2304e48031be/75930cde72664dca9ae1084258c4c9cb/dash/main/manifest.mpd?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcCI6IjA4MzJlMzM0OTE1OTRiZTlhNzMyOWYyNWU1ZmM3NmJiIiwiZGMiOiIxMjMyOWQ3OWRlZWQ0ZTQ5YTRlMWRlNDE2ZWIyYjMwNiIsImVkZ2UiOiI1YjM1NjMwYmQwNTI0NWQ3ODMwNzY4MTg2M2RjMjllNCIsImNvZGVjcyI6ImF2YyIsImV4cCI6MTczODE2MjgwMCwidnA5IjoxLCJtaW5oIjozNjAsImJ3IjoyMTAwMDAwfQ.A3-hxzSyPu8Y0I14DJzKErL5CyuwQCdEUz3sQoI2DO0

# Example Licence Url: https://bees.streaks.jp/hulu/8ad92b4cef1f4349804f2304e48031be/cenc/?specConform=true&token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiJhM2JkMzNiMzVjOWU0NGNiOWYxZWRhYzQ5ODFhN2E2MCIsIm0iOiJodWx1IiwidHMiOjE3MzgwNzQ0MDAsImsiOiIzNTQxYjRkOGM0ZGQ0YjAyOGRiZWYyMGJhYjBlODQ1OCIsInVpZCI6IjQ3NjUzMTkwIiwiYWlkIjoiY29udGVudF9pZCIsInBwIjoiMDgzMmUzMzQ5MTU5NGJlOWE3MzI5ZjI1ZTVmYzc2YmIifQ.SzA9WlU8bDD9-T_TGk-JARwTn7nTON6ds4h8jdPsY-w_r8RQcmJjAGd0pcT3U8axJ1UOtuCH-pBDilV52d-fig

# python l3dl_mac.py -m "https://manifest.streaks.jp/v3/hulu/8ad92b4cef1f4349804f2304e48031be/75930cde72664dca9ae1084258c4c9cb/dash/main/manifest.mpd?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwcCI6IjA4MzJlMzM0OTE1OTRiZTlhNzMyOWYyNWU1ZmM3NmJiIiwiZGMiOiIxMjMyOWQ3OWRlZWQ0ZTQ5YTRlMWRlNDE2ZWIyYjMwNiIsImVkZ2UiOiI1YjM1NjMwYmQwNTI0NWQ3ODMwNzY4MTg2M2RjMjllNCIsImNvZGVjcyI6ImF2YyIsImV4cCI6MTczODE2MjgwMCwidnA5IjoxLCJtaW5oIjozNjAsImJ3IjoyMTAwMDAwfQ.A3-hxzSyPu8Y0I14DJzKErL5CyuwQCdEUz3sQoI2DO0" -l "https://bees.streaks.jp/hulu/8ad92b4cef1f4349804f2304e48031be/cenc/?specConform=true&token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJzaWQiOiJhM2JkMzNiMzVjOWU0NGNiOWYxZWRhYzQ5ODFhN2E2MCIsIm0iOiJodWx1IiwidHMiOjE3MzgwNzQ0MDAsImsiOiIzNTQxYjRkOGM0ZGQ0YjAyOGRiZWYyMGJhYjBlODQ1OCIsInVpZCI6IjQ3NjUzMTkwIiwiYWlkIjoiY29udGVudF9pZCIsInBwIjoiMDgzMmUzMzQ5MTU5NGJlOWE3MzI5ZjI1ZTVmYzc2YmIifQ.SzA9WlU8bDD9-T_TGk-JARwTn7nTON6ds4h8jdPsY-w_r8RQcmJjAGd0pcT3U8axJ1UOtuCH-pBDilV52d-fig" -o "hulu_test"

from pywidevine_.L3.decrypt.wvdecryptcustom import WvDecrypt
from pywidevine_.L3.cdm import cdm, deviceconfig
from base64 import b64encode
from getPSSH import get_pssh
import subprocess
import xmltodict
import argparse
import requests
import sqlite3
import headers
import base64
import os
version = '0.1'


def WV_Function(pssh, lic_url, cert_b64=None):
    wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64,
                          device=deviceconfig.device_android_generic)
    widevine_license = requests.post(
        url=lic_url, data=wvdecrypt.get_challenge(), headers=headers.headers)
    license_b64 = b64encode(widevine_license.content)
    wvdecrypt.update_license(license_b64)
    Correct, keyswvdecrypt = wvdecrypt.start_process()
    if Correct:
        return Correct, keyswvdecrypt


def insert_table(pssh, keys, license_, mpd_):
    conn = sqlite3.connect('keyVault.db')
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO TBL_KEYS(PSSH,KEYS,LICENSE_URL,MPD_URL) VALUES ('{pssh}','{keys}','{license_}','{mpd_}')")
    conn.commit()
    conn.close()


def find_pssh(pssh):
    conn = sqlite3.connect('keyVault.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM TBL_KEYS WHERE PSSH='{pssh}'")
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def fetch_key(pssh):
    conn = sqlite3.connect('keyVault.db')
    conn.text_factory = str
    cursor = conn.cursor()
    fetch = cursor.execute(
        f"SELECT KEYS FROM TBL_KEYS WHERE PSSH='{pssh}'").fetchall()
    # edit this for cases that no pssh can be extracted from MPD
    fetched_keys = fetch[0][0]
    conn.commit()
    conn.close()
    return fetched_keys


def download(keys):
    if mpd_url != None:
        base_dir = os.path.join(cd, 'output')
        file_path = os.path.join(base_dir, f'{name}.mkv')
        if select_ and not os.path.exists(file_path):
            os.system(f'N_m3u8DL-RE "{mpd_url}" --log-level ERROR --binary-merge --live-real-time-merge --mp4-real-time-decryption --key {keys} -M format=mkv:muxer=mkvmerge -R 5M --del-after-done false --tmp-dir "{base_dir}" --save-name "{name}" --save-dir "{base_dir}" --use-shaka-packager -mt TRUE --thread-count 10', shell=True)
        elif not select_ and not os.path.exists(file_path):
            print(
                f'Processing {name} | Download, decrypt, and muxing may take some time.')
            subprocess.call(f'N_m3u8DL-RE "{mpd_url}" --log-level ERROR --binary-merge --live-real-time-merge --mp4-real-time-decryption --key {keys} -M format=mkv:muxer=mkvmerge -R 5M --del-after-done false -ss all -sa best -sv best --tmp-dir "{base_dir}" --save-name "{name}" --save-dir "{base_dir}" --use-shaka-packager -mt TRUE --thread-count 10', shell=True)
        else:
            print(f'{name} already on output folder. Skipped.')
    else:
        print('No MPD URL supplied. Try again.')


def start_():
    if pssh_:
        pssh = pssh_
    else:
        pssh = get_pssh(mpd_url)

    if pssh != 'skip':
        print(f'\nPSSH: {pssh}')
        cached = find_pssh(pssh)
        if cached:
            keys = fetch_key(pssh)
            print(f'Cached key found for {name}: {fetch_key(pssh)}')
            if not keys_:
                download(keys)
        else:
            if lic_url != None:
                correct, keys = WV_Function(pssh.strip(), lic_url.strip())

                if keys:
                    for key in keys:
                        print(f'Key: {key}')
                        insert_table(pssh, key, lic_url, mpd_url)
                    # consider multi-keys scenario, pssh to kid?
                    if keys_:
                        print(f'Done fetching keys for {name}.')
                    else:
                        download(keys)
            else:
                print(f'You have no license URL for {name}. Try again.')
    else:
        print(f'Skipped {name}.')


print(f'''\n
r3n@RSG                                  {version}
██╗     ██████╗ ██████╗ ██╗      ██████╗ ███████╗
██║     ╚════██╗██╔══██╗██║      ██╔══██╗██╔════╝
██║      █████╔╝██║  ██║██║█████╗██████╔╝█████╗
██║      ╚═══██╗██║  ██║██║╚════╝██╔══██╗██╔══╝
███████╗██████╔╝██████╔╝███████╗ ██║  ██║███████╗
╚══════╝╚═════╝ ╚═════╝ ╚══════╝ ╚═╝  ╚═╝╚══════╝

    -- L3DL REscripted Widevine Downloader --''')

parser = argparse.ArgumentParser(
    description='L3DL-RE widevine downloader - r3n@RSG')
parser.add_argument('-m', '--manifest', type=str,
                    metavar='', help="your mpd/m3u8 link")
parser.add_argument('-l', '--license', type=str,
                    metavar='', help="license url link")
parser.add_argument('-o', '--output', type=str.lower,
                    metavar='', help="output file name")
parser.add_argument('-p', '--pssh', type=str,
                    metavar='', help="supply pssh instead of extracting from manifest")
parser.add_argument('--batch', help="batch download mode. what file to open?")
parser.add_argument('--select', action='store_true',
                    help="manually pick what to download")
parser.add_argument('--keys', action='store_true',
                    help="keys only, don't download")
parser.add_argument('--shut', action='store_true',
                    help="shutdown windows after the process")


args = parser.parse_args()
mpd_url = args.manifest
lic_url = args.license
name = args.output
select_ = args.select
keys_ = args.keys
batch_mode = args.batch
shutdown = args.shut
pssh_ =  args.pssh

cd = os.getcwd()
# cd = '~/Downloads'

if not os.path.exists('output'):
    os.makedirs('output')


if batch_mode:
    print('\nBatch mode activated.')
    source_file = open(batch_mode, "r", encoding='latin-1')
    for line in source_file:
        fields = line.split(";")
        name = fields[0]
        mpd_url = fields[1]
        lic_url = fields[2]
        start_()
else:
    start_()


if shutdown:
    os.system(f'shutdown /f /s')
