#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '1.0.0'
__date__ = '2024/11/21'

import spotipy
import os
import csv
from spotipy.oauth2 import SpotifyClientCredentials

"""
playlist_url.txtに記述されてるURLリストから、全ての楽曲情報を取得し、genres_v2.csvに書き込むプログラム
"""

def main():
    """API認証を行い、プログラムを実行する"""

    # APIで情報を取得するための準備
    client_credentials_manager = SpotifyClientCredentials(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'), 
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET')
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    with open('./genres_v2/playlist_url.txt', mode='r', encoding='utf-8') as f:
        for url in f:
            track_ids = get_track_ids(sp, url)
            write_csv(sp, track_ids)


def get_track_ids(sp, url):
    """再生リストURLからtrackのidリストを取得する"""

    playlist_id = url.split("/")[-1].split("?")[0]
    results = sp.playlist_items(playlist_id)
    tracks = results['items']

    # 各楽曲のトラックIDを取得
    track_ids = [item['track']['id'] for item in tracks]

    return track_ids

def write_csv(sp, ids):
    """trackのidリストから楽曲情報を取得し、csvファイルに書き込む"""

    with open('./genres_v2/genres_v2.csv', mode='a', encoding='utf-8') as f:
        is_first = True
        for id in ids:
            audio_features = sp.audio_features([id])[0]
            writer = csv.DictWriter(f, fieldnames=audio_features.keys())
            if is_first:
                writer.writeheader()
                is_first = False
            writer.writerow(audio_features)

if __name__ == "__main__":
    import sys
    sys.exit(main())