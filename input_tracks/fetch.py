#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__date__ = '2024/11/21'

import spotipy
import os
import csv
from spotipy.oauth2 import SpotifyClientCredentials

"""
song_url.txtに記述されてるURLリストから、全ての楽曲情報を取得し、input_tracks.csvに書き込むプログラム
"""

def main():
    """API認証を行い、プログラムを実行する"""

    # APIで情報を取得するための準備
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'), 
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    with open('./input_tracks/song_url.txt', mode='r', encoding='utf-8') as f:
        is_first = True
        for i, url in enumerate(f):
            track_id = url.split("/")[-1].split("?")[0]
            with open('./input_tracks/input_tracks.csv', mode='a', encoding='utf-8') as f:
                audio_features = sp.audio_features([track_id])[0]
                audio_features = {'': i, **audio_features}
                writer = csv.DictWriter(f, fieldnames=audio_features.keys())
                if is_first:
                    writer.writeheader()
                    is_first = False
                writer.writerow(audio_features)

if __name__ == "__main__":
    import sys
    sys.exit(main())