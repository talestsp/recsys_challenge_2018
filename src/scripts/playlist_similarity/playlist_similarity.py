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

def playlist_vs_all(playlist, all_playlists, playlist_sim_dir, top_similars=16, sep=";"):
    '''
    Calculates jaccard similarity between playlist and all playlists and saves it.
    Saves a data frame with two columns: pids from playlists and their similarity with self.playlist.
    :param jaccard_treshold: return data frame with only similoarities above this treshold
    :param playlist_sim_dir: path to similarity playlists directory
    '''

    sims = all_playlists.apply(
        lambda another_playlist:
        jaccard(playlist["track_uri"], another_playlist["track_uri"]), axis=1)

    sims.index.names = ["pid"]
    sims = sims.sort_values(ascending=False).head(top_similars)
    sims.to_csv(playlist_sim_dir + "pid--" + str(playlist["pid"]) + ".csv", sep=sep)

def calc_similarity_for_playlists(all_playlists, playlist_sim_dir, pids):
    '''
    It calculates similarity between each playlist inside a range and all playlists
    :param all_playlists: DataFrame of play_track.csv
    :param playlist_sim_dir: path to save playlist's similarity
    :param from_pid: start value of the pids range
    :param to_pid: end value of the pids range
    '''
    print("Processing similarities...")
    all_playlists.loc[pids].apply(playlist_vs_all,
                                              all_playlists=all_playlists,
                                              playlist_sim_dir=playlist_sim_dir,
                                              axis=1)
