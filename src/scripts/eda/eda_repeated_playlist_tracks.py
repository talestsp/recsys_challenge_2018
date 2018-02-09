import sys
import pandas as pd

play_track_filename = sys.argv[1]

df = pd.read_csv(play_track_filename, sep=";")
playlist_len = df.groupby("pid").apply(len)

unique_pid_track = df[["pid", "track_uri"]].drop_duplicates()
playlist_unique_len = unique_pid_track.groupby("pid")["track_uri"].apply(len)

diff = (playlist_len - playlist_unique_len)

diff.describe()
diff[diff > 0].describe()

