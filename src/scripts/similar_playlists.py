# This script generates for each playlist a table with the most similar playlists

# INPUTS
# arg1: play_track_flat.csv path (if you dont have it, run flatten_play_track.py on play_track.csv)
# arg2: path to playlists similarity dir
# arg3: from pid
# arg3: to pid

import pandas as pd
import sys
import ast

def jaccard(a, b, round_n=4):
    set_a = set(a)
    set_b = set(b)
    return round(float(len(set_a.intersection(set_b))) / len(set_a.union(b)), round_n)

def similar_playlists(playlist, playtrack, jaccard_trehhold=0.1):
    pid = playlist["pid"]
    sims = playtrack.apply(lambda another_playlist:
                   jaccard(playlist["track_uri"], another_playlist["track_uri"]),
                    axis=1)
    print("pid:", pid)
    sims.index.names = ["pid"]
    #saving only similarities above jaccard_threshold
    sims[sims > jaccard_trehhold].to_csv(output_playlist_sim_dir + "pid--" + str(pid) + ".csv", sep=SEP)

SEP = ";"

# play_track_flat_csv_path = "/home/tales/dev/recsys_challenge_2018/data/play_track_flat.csv"
# output_playlist_sim_dir = "/home/tales/dev/recsys_challenge_2018/data/playlist_similarity/"

play_track_flat_csv_path = sys.argv[1]
output_playlist_sim_dir = sys.argv[2]
from_pid = 0
to_pid = 3

print("Loading play_track_flat data...")
playtrack = pd.read_csv(play_track_flat_csv_path, sep=";")

playtrack["track_uri"] = playtrack["track_uri"].apply(ast.literal_eval)
print(playtrack.head())
if len(playtrack) != 1000000:
    raise Exception("Maybe wrong input file! Length: " + str(len(playtrack)))

print("Processing similarities...")
playtrack[from_pid : to_pid].apply(similar_playlists, playtrack=playtrack, axis=1)

