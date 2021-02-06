import os
import pickle
from pathlib import Path
from random import choice

import pandas as pd


class DataLoad:

    precomputed_path = Path('data/precomputed')
    meta_path = Path('data/fma_metadata')
    songs_path = Path('data/fma_small')
    df = pd.DataFrame()
    test_tracks = dict()

    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        if not os.path.isfile(os.path.join(self.root, self.precomputed_path, 'trackMeta.pickle')):
            self.map_meta_data()
        else:
            with open(os.path.join(self.root, self.precomputed_path, 'trackMeta.pickle'), 'rb') as f:
                self.df = pickle.load(f)
        if not os.path.isfile(os.path.join(self.root, self.precomputed_path, 'testTracks.pickle')):
            self.test_set_creation(size=400)
        else:
            with open(os.path.join(self.root, self.precomputed_path, 'testTracks.pickle'), 'rb') as file:
                self.test_tracks = pickle.load(file)

    def map_meta_data(self):
        d = dict()
        track = pd.read_csv(os.path.join(self.root, self.meta_path, 'tracks.csv'))
        track = track[track['set.1'] == 'small']
        d['shape'] = track.shape
        d['genresl'] = len(track['track.7'].unique())
        d['bitratel'] = len(track['track'].unique())
        d['artistl'] = len(track['artist.7'].unique())
        d['albuml'] = len(track['album.5'].unique())
        self.df = track
        self.df.to_pickle(os.path.join(self.root, self.precomputed_path, 'trackMeta.pickle'))
        return d

    def test_set_creation(self, size):
        temp = dict()
        for i in range(size):
            num = choice(self.df['Unnamed: 0'].values)
            n = self.df.loc[self.df['Unnamed: 0'] == num, 'track.19'].item()
            temp[num] = str(n)
        with open(os.path.join(self.root, self.precomputed_path, 'testTracks.pickle'), 'wb') as f:
            pickle.dump(temp, f)
        self.test_tracks = temp


def main():
    DataLoad()


if __name__ == '__main__':
    main()
