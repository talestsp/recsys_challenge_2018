# This script generates for each playlist a table with the most similar playlists

# INPUTS
# arg1: play_track.csv path
# arg2: path to playlists similarity dir
# arg3: from pid
# arg4: to pid
# arg5 (optional; default n_cpus=1): number of CPUs to be used on parallelism

import pandas as pd
import sys
import gc
import threading
import time
import math

import os

print(os.path.join(os.path.dirname(__file__), '..'))

class PlaylistSimilarityBuilder(threading.Thread):
    def __init__(self, playtrack, output_playlist_sim_dir, from_pid, to_pid):
        threading.Thread.__init__(self)
        self.playtrack = playtrack
        self.output_playlist_sim_dir = output_playlist_sim_dir
        self.from_pid = from_pid
        self.to_pid = to_pid


    def jaccard(self, a, b, round_n=4):
        '''
        Rounded jaccard similarity
        :param a: an array to be coerced to set
        :param b: another array to be coerced to set
        :param round_n: round n non integer digits
        :return: jaccard distance
        '''
        set_a = set(a)
        set_b = set(b)
        return round(float(len(set_a.intersection(set_b))) / len(set_a.union(b)), round_n)

    def playlist_similarities(self, playlist, jaccard_treshold=0.1):
        '''
        Calculates jaccard similarity between the given playlist and all playlists and saves it.
        :param playlist: calculates distance from playlist to all playlists
        :param playtrack: DataFrame of play_track.csv
        :param jaccard_treshold:
        '''
        pid = playlist["pid"]
        sims = self.playtrack.apply(lambda another_playlist:
                                    self.jaccard(playlist["track_uri"],
                                    another_playlist["track_uri"]),
                                    axis=1)
        print("saving similars to pid:", pid)
        sims.index.names = ["pid"]
        #saving only similarities above jaccard_threshold
        sims[sims > jaccard_treshold].to_csv(output_playlist_sim_dir + "pid--" + str(pid) + ".csv", sep=SEP)


    def run(self):
        '''
        It calculates similarity between each playlist inside a range and all playlists
        :param playtrack: DataFrame of play_track.csv
        :param from_pid: beginning of the playlist
        :param to_pid: end of the playlist
        '''
        print("Processing similarities...")
        self.playtrack.loc[self.from_pid: self.to_pid].apply(self.playlist_similarities, axis=1)


def dataset_slices(from_pid, to_pid, n_threads):
    '''
    Builds a list of ranges that each thread will apply to dataset
    :param n_cpus: number of CPUs to be in parallelized
    :param playtrack: DataFrame of play_track.csv
    :param from_pid:
    :param to_pid:
    :return:
    '''
    range_len = to_pid - from_pid
    current_from_pid = from_pid

    dataset_range = int(math.ceil(range_len / n_threads))
    ranges = []


    for i in range(n_threads - 1):
        current_to_pid = current_from_pid + dataset_range
        ranges.append({"from_pid": current_from_pid,
                       "to_pid": current_to_pid})
        current_from_pid = current_to_pid + 1

    #create a task for the missing rounds
    ranges.append({"from_pid": current_from_pid, "to_pid": to_pid})
    return ranges



def load_and_process_data(playtrack_csv_path):
    print("Loading play_track data...")
    playtrack = pd.read_csv(playtrack_csv_path, sep=";")
    del playtrack["pos"]
    gc.collect()

    print("Transforming data...")
    playtrack = playtrack.groupby("pid")["track_uri"].apply(lambda serie: serie.tolist())
    gc.collect()
    playtrack = pd.DataFrame(playtrack).reset_index()
    playtrack = playtrack.set_index(playtrack["pid"])

    return playtrack


SEP = ";"

# playtrack_csv_path = "/home/tales/dev/recsys_challenge_2018/data/play_track.csv"
# output_playlist_sim_dir = "/home/tales/dev/recsys_challenge_2018/data/playlist_similarity/"

##############
# INPUTS
playtrack_csv_path = sys.argv[1]
output_playlist_sim_dir = sys.argv[2]
from_pid = int(sys.argv[3])
to_pid = int(sys.argv[4])
try:
    n_threads = int(sys.argv[5])
except IndexError:
    n_threads = 1
##############

start = time.time()
playtrack = load_and_process_data(playtrack_csv_path)
end = time.time()
print("Time (s) for loading and processing data: " + str(end - start))


dataset_ranges = dataset_slices(from_pid, to_pid, n_threads)

for dataset_range in dataset_ranges:
    similarity_builder = PlaylistSimilarityBuilder(playtrack, output_playlist_sim_dir,
                                                   dataset_range["from_pid"], dataset_range["to_pid"])
    similarity_builder.start()


