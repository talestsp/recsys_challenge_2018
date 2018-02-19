# This script generates for each playlist a table with the most similar playlists

# INPUTS
# arg1: play_track.csv path
# arg2: path to playlists similarity dir
# arg3: from pid
# arg3: to pid

import pandas as pd
import sys
import gc
import os
import json

def jaccard(a, b, round_n=4):
    set_a = set(a)
    set_b = set(b)
    return round(float(len(set_a.intersection(set_b))) / len(set_a.union(b)), round_n)

def similar_playlists(playlist, playtrack, jaccard_treshold=0.1):
    pid = playlist["pid"]
    sims = playtrack.apply(lambda another_playlist:
                   jaccard(playlist["track_uri"], another_playlist["track_uri"]),
                    axis=1)
    print("pid:", pid)
    sims.index.names = ["pid"]
    #saving only similarities above jaccard_threshold
    sims[sims > jaccard_treshold].to_csv(output_playlist_sim_dir + "pid--" + str(pid) + ".csv", sep=SEP)

SEP = ";"

# playtrack_csv_path = "/home/tales/dev/recsys_challenge_2018/data/play_track.csv"
# output_playlist_sim_dir = "/home/tales/dev/recsys_challenge_2018/data/playlist_similarity/"

playtrack_csv_path = sys.argv[1]
output_playlist_sim_dir = sys.argv[2]
from_pid = int(sys.argv[3])
to_pid = int(sys.argv[4])

import time
start = time.time()

print("Loading play_track data...")
playtrack = pd.read_csv(playtrack_csv_path, sep=";")
del playtrack["pos"]
gc.collect()

print("Transforming data...")
playtrack = playtrack.groupby("pid")["track_uri"].apply(lambda serie: serie.tolist())
gc.collect()
playtrack = playtrack.reset_index()
playtrack = playtrack.sort_values("pid")

end = time.time()
print(end - start)

print("Processing similarities...")
playtrack[from_pid : to_pid].apply(similar_playlists, playtrack=playtrack, axis=1)

