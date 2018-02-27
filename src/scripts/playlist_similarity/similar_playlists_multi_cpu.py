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
import json

from src.scripts.playlist_similarity.playlist_similarity import calc_similarity_for_playlists
from src.utils.path import fix_path


def load_config(config_path):
    with open(config_path, "r") as file:
        config = json.load(file)

    if "from_pid" in config.keys() and "to_pid" in config.keys():
        config["pids"] = list(range(int(config["from_pid"]), int(config["to_pid"]) + 1))

    return config

# def process_parameters(all_playlists, n_cpus, playlist_sim_dir, from_pid, to_pid):
#     '''
#     Builds a list of parameters to be applied to each CPU task
#     :param n_cpus: number of CPUs to be in parallelized
#     :param all_playlists: DataFrame of play_track.csv
#     :param playlist_sim_dir: path to save playlist's similarity
#     :param from_pid:
#     :param to_pid:
#     :return:
#     '''
#     range_len = to_pid - from_pid
#     current_from_pid = from_pid
#
#     task_len = int(math.ceil(range_len / n_cpus))
#     task_parameters = []
#
#     #creates task for each CPU
#     #Attention: the last task will be made (complementary) out of this for due to deal with reamaining rounds
#     for i in range(n_cpus - 1):
#         current_to_pid = current_from_pid + task_len
#         task_parameters.append((all_playlists,
#                                 playlist_sim_dir,
#                                 current_from_pid,
#                                 current_to_pid))
#         current_from_pid = current_to_pid + 1
#
#     #create a task for the complementary missing rounds
#     task_parameters.append((all_playlists,
#                             playlist_sim_dir,
#                             current_from_pid,
#                             to_pid))
#     return task_parameters

def process_parameters(all_playlists, n_cpus, playlist_sim_dir, pids):
    '''
    Builds a list of parameters to be applied to each CPU task
    :param n_cpus: number of CPUs to be in parallelized
    :param all_playlists: DataFrame of play_track.csv
    :param playlist_sim_dir: path to save playlist's similarity
    :param from_pid:
    :param to_pid:
    :return:
    '''
    range_len = len(pids)
    task_len = int(math.floor(range_len / n_cpus))
    task_parameters = []

    #creates task for each CPU
    #Attention: the last task will be made (complementary) out of this for due to deal with reamaining rounds
    for i in range(n_cpus - 1):
        from_index = i * task_len
        to_index = (i + 1) * task_len

        use_pids = pids[from_index : to_index]
        task_parameters.append((all_playlists,
                                playlist_sim_dir,
                                use_pids))

    #there is no previous loop for n_cpus = 1
    if n_cpus == 1:
        to_index = 0

    #create a task for the complementary missing rounds
    use_pids = pids[to_index : len(pids)]
    task_parameters.append((all_playlists,
                            playlist_sim_dir,
                            use_pids))
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
config_path = fix_path(sys.argv[1], is_dir=False)
config = load_config(config_path)

playtrack_csv_path = config["playtrack_csv_path"]
playlist_sim_dir = config["playlist_sim_dir"]
from_pid = config["from_pid"]
to_pid = config["to_pid"]
n_cpus = config["n_cpus"]

print("\n\n", config, "\n\n")

#####################

start = time.time()

all_playlists = load_and_transform_data(playtrack_csv_path)

end = time.time()
print("Time (s) for loading and processing data: " + str(end - start))


pool = multiprocessing.Pool(n_cpus)
tasks_parameters = process_parameters(all_playlists, n_cpus, playlist_sim_dir, config["pids"])

results = []
for parameters in tasks_parameters:
    results.append(pool.apply_async(calc_similarity_for_playlists, parameters))

for result in results:
    print(result.get())
