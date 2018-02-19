# This script generates a new play_track csv with position removed.
# Each row represent a playlist. Song ids are placed on a list.
# Output file will be stored in the same directory as play_track csv

# INPUTS
# arg1: play_track csv path

import pandas as pd
import sys
import gc

SEP = ";"

playtrack_csv_path = sys.argv[1]

print("Loading play_track data...")
playtrack = pd.read_csv(playtrack_csv_path, sep=";")
del playtrack["pos"]
gc.collect()

print("Transforming data...")
playtrack = playtrack.groupby("pid")["track_uri"].apply(lambda serie: serie.tolist())
gc.collect()
playtrack = playtrack.reset_index()
playtrack = playtrack.sort_values("pid")

print("Saving play_track_flat.csv")
new_filename = "/".join(playtrack_csv_path.split("/")[0:-1]) + "/play_track_flat.csv"
playtrack.to_csv(new_filename, index=False)
