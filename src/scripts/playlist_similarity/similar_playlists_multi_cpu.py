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
import multiprocessing
import time
import math

from src.scripts.playlist_similarity.playlist_similarity import calc_similarity_for_playlists

def process_parameters(all_playlists, n_cpus, playlist_sim_dir, from_pid, to_pid):
    '''
    Builds a list of parameters to be applied to each CPU task
    :param n_cpus: number of CPUs to be in parallelized
    :param all_playlists: DataFrame of play_track.csv
    :param from_pid:
    :param to_pid:
    :return:
    '''
    range_len = to_pid - from_pid
    current_from_pid = from_pid

    task_len = int(math.ceil(range_len / n_cpus))
    task_parameters = []

    #creates task for each CPU
    #Attention: the last task will be made (complementary) out of this for due to deal with reamaining rounds
    for i in range(n_cpus - 1):
        current_to_pid = current_from_pid + task_len
        task_parameters.append((all_playlists,
                                playlist_sim_dir,
                                current_from_pid,
                                current_to_pid))
        current_from_pid = current_to_pid + 1

    #create a task for the complementary missing rounds
    task_parameters.append((all_playlists,
                            playlist_sim_dir,
                            current_from_pid,
                            to_pid))
    return task_parameters

def load_and_transform_data(playtrack_csv_path):
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


### SCRIPT INPUTS ###
playtrack_csv_path = sys.argv[1]
playlist_sim_dir = sys.argv[2]
from_pid = int(sys.argv[3])
to_pid = int(sys.argv[4])
try:
    n_cpus = int(sys.argv[5])
except IndexError:
    n_cpus = 1
#####################

start = time.time()

all_playlists = load_and_transform_data(playtrack_csv_path)

end = time.time()
print("Time (s) for loading and processing data: " + str(end - start))


pool = multiprocessing.Pool(n_cpus)
tasks_parameters = process_parameters(all_playlists, n_cpus, playlist_sim_dir, from_pid, to_pid, )

results = []
for parameters in tasks_parameters:
    results.append(pool.apply_async(calc_similarity_for_playlists, parameters))

for result in results:
    print(result.get())
