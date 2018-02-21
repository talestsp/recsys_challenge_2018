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

def jaccard(a, b, round_n=4):
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

def playlist_similarities(playlist, playtrack, jaccard_treshold=0.1):
    '''
    Calculates jaccard similarity between playlist and all playlists and saves it.
    :param playlist: calculates distance from playlist to all playlists
    :param playtrack: DataFrame of play_track.csv
    :param jaccard_treshold:
    '''
    pid = playlist["pid"]
    sims = playtrack.apply(lambda another_playlist:
                   jaccard(playlist["track_uri"], another_playlist["track_uri"]),
                    axis=1)
    print("saving similars to pid:", pid)
    sims.index.names = ["pid"]
    #saving only similarities above jaccard_threshold
    sims[sims > jaccard_treshold].to_csv(output_playlist_sim_dir + "pid--" + str(pid) + ".csv", sep=SEP)


def calc_similarity_for_playlists(playtrack, from_pid, to_pid):
    '''
    It calculates similarity between each playlist inside a range and all playlists
    :param playtrack: DataFrame of play_track.csv
    :param from_pid:
    :param to_pid:
    :return:
    '''
    print("\n", id(playtrack), "\n")
    print("Processing similarities...")
    playtrack[from_pid: to_pid].apply(playlist_similarities, playtrack=playtrack, axis=1)


def build_multi_core_tasks(playtrack, n_cpus, from_pid, to_pid):
    '''
    Builds a list of task parameters to be applied to each CPU task
    :param n_cpus: number of CPUs to be in parallelized
    :param playtrack: DataFrame of play_track.csv
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
        task_parameters.append((playtrack,
                                current_from_pid,
                                current_to_pid))
        current_from_pid = current_to_pid + 1

    #create a task for the complementary missing rounds
    task_parameters.append((playtrack,
                            current_from_pid,
                            to_pid))
    return task_parameters

SEP = ";"

# playtrack_csv_path = "/home/tales/dev/recsys_challenge_2018/data/play_track.csv"
# output_playlist_sim_dir = "/home/tales/dev/recsys_challenge_2018/data/playlist_similarity/"

playtrack_csv_path = sys.argv[1]
output_playlist_sim_dir = sys.argv[2]
from_pid = int(sys.argv[3])
to_pid = int(sys.argv[4])
try:
    n_cpus = int(sys.argv[5])
except IndexError:
    n_cpus = 1

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
print("Time (s) for loading and processing data: " + str(end - start))




#
# from multiprocessing import Manager
#
# mgr = Manager()
# ns = mgr.Namespace()
# ns.df = playtrack




pool = multiprocessing.Pool(n_cpus)
tasks_parameters = build_multi_core_tasks(playtrack, n_cpus, from_pid, to_pid)

results = []
for parameters in tasks_parameters:
    results.append(pool.apply_async(calc_similarity_for_playlists, parameters))

for result in results:
    print(result.get())



