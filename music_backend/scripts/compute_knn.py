import os
from pathlib import Path

import music_backend.scripts.load_dataset as load_dataset
import numpy as np
import pandas as pd
from scipy.spatial import distance
from sklearn.preprocessing import MinMaxScaler


class CompSimilarityKRanking:
    root = None
    data_path = Path('data/precomputed')
    query = None
    df = pd.DataFrame()
    nn = None
    id_list = list()

    def __init__(self):
        self.cd = load_dataset.DataLoad()
        ignoreList = [99134, 108925, 113203, 133297]
        list = self.cd.df['Unnamed: 0'].values
        for e in list:
            if e in ignoreList:
                continue
            else:
                self.id_list.append(e)
        self.root = Path(__file__).resolve().parent.parent
        self.df = pd.read_csv(os.path.join(self.root, self.data_path, 'extractedFeatures.csv'))
        self.df = self.df.iloc[:, 1:]
        self.df = self.df.drop('beat_track', axis=1)
        self.df['track_id'] = self.id_list
        self.normalization()

    def normalization(self):
        scaler = MinMaxScaler(feature_range=(0, 1))
        col = self.df.columns
        col = col[:-1]
        self.df[col] = scaler.fit_transform(self.df[col])

    def computeKnn(self, q, k):
        d = dict()
        start = 1
        end = 100
        width = end - start
        data = self.df.loc[:, :].values
        query = self.df.loc[self.df['track_id'].astype(np.int) == q].values
        neigh = []
        p = len(query)
        for i, row in enumerate(data):
            dist = distance.minkowski(row[:-1], query[0][:-1], p)
            neigh.append([dist, row[-1]])
        sort_neigh = sorted(neigh)
        k_vals = sort_neigh[:k+1]
        distanceBw = []
        for indDist in k_vals:
            distanceBw.append(indDist[0])
        i = 0
        for group in k_vals:
            distNorm = (group[0] - min(distanceBw))/(max(distanceBw) - min(distanceBw)) * width + start
            track = group[-1]
            trackName = self.cd.df.loc[self.cd.df['Unnamed: 0'] == track, 'track.19'].item()
            d[i] = {'track_name': trackName, 'track_id': str(track), 'distance': str(distNorm)}
            i = i+1
        return d


def main():
    print(CompSimilarityKRanking().computeKnn(q=154414, k=2))


if __name__ == '__main__':
    main()
