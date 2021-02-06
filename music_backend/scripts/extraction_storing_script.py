import os
import os.path

import pandas as pd


class CalcFeatures:
    root = None
    precomputer_path = 'data/precomputed'
    meta_path = 'data/fma_metadata'
    songs_path = 'data/fma_small'
    df = pd.DataFrame()
    tracks = list()

    def __init__(self):
        self.root = os.path.dirname(os.getcwd())
        if not os.path.isfile(os.path.join(self.root, self.precomputer_path, 'trackLibrosa.pickle')):
            self.calc_features()

    def calc_features(self):
        track_id = list()
        for folder in os.listdir(os.path.join(self.root, self.songs_path)):
            if os.path.isdir(os.path.join(self.root, self.songs_path, folder)):
                for songs in os.listdir(os.path.join(self.root, self.songs_path, folder)):
                    if songs.endswith('.mp3'):
                        songs = songs.strip('0').strip('.mp3')
                        track_id.append(songs)
        if 'track_id' not in self.df:
            self.df['track_id'] = track_id


def main():
    CalcFeatures()

if __name__ == '__main__':
    main()
