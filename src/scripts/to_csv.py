import json
import csv
import os
import sys
from src.utils.path import fix_path

#Script that transform original data into three csvs (playlist data, track data and for linking them)
#arg1: input data dir
#arg2: output data dir

input_data_dir = sys.argv[1]
output_data_dir = sys.argv[2]

input_data_dir = fix_path(input_data_dir)
output_data_dir = fix_path(output_data_dir)

##data parser to csv. 
#Tables generated: playlist, play_track and track.
p_cols = ["name", "collaborative", "pid", "modified_at", "num_tracks", "num_albums", "num_followers"]
t_cols = ["artist_name", "track_uri", "artist_uri", "track_name", "album_uri", "duration_ms", "album_name"]
p_t_cols = ["pid", "track_uri", "pos"]

with open(output_data_dir + "playlists.csv", "w", encoding = 'utf-8') as p_out_file:
    p_file = csv.writer(p_out_file, quoting=csv.QUOTE_MINIMAL, lineterminator='\n', delimiter=';', escapechar='\\')
    p_file.writerow(p_cols)
    with open(output_data_dir + "tracks.csv", "w", encoding = 'utf-8') as t_out_file:
        t_file = csv.writer(t_out_file, quoting=csv.QUOTE_MINIMAL, lineterminator='\n', delimiter=';',
                            escapechar='\\')

        t_file.writerow(t_cols)
        with open(output_data_dir + "play_track.csv", "w", encoding = 'utf-8') as p_t_out_file:
            p_t_file = csv.writer(p_t_out_file, quoting=csv.QUOTE_MINIMAL, lineterminator='\n', delimiter=';',
                                  escapechar='\\')
            p_t_file.writerow(p_t_cols)
            for filename in os.listdir(input_data_dir):
                if('.json' in filename):
                    filepath = input_data_dir + filename
                    print(filepath)
                    data = json.load(open(filepath))
                    playlists = data["playlists"]
                    for p in playlists:
                        line = [p["name"], p["collaborative"], p["pid"], p["modified_at"], p["num_tracks"], p["num_albums"], p["num_followers"]]
                        p_file.writerow(line)
                        pid = p["pid"]
                        tracks = p["tracks"]
                        for t in tracks:
                            line = [t["artist_name"], t["track_uri"], t["artist_uri"], t["track_name"], t["album_uri"], t["duration_ms"], t["album_name"]]
                            t_file.writerow(line)
                            track_uri = t["track_uri"]
                            pos = t["pos"]
                            line = [pid, track_uri, pos]
                            p_t_file.writerow(line)
