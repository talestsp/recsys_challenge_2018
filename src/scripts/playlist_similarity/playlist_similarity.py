import pandas as pd

JACCARD = "jaccard"
PERCENTUAL_INTERSEC = "percentual_intersec"

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

def percentual_intersec(a, b, round_n=4):
    '''
    Returns a proportion of how many elements from a are in b
    :param a: an array to be coerced to set
    :param b: another array to be coerced to set
    :param round_n: round n non integer digits
    '''
    set_a = set(a)
    set_b = set(b)
    return round(float(len(set_a.intersection(set_b))) / len(set_a), round_n)

def pick_similarity_metric(metric_name):
    if metric_name == JACCARD:
        return jaccard
    elif metric_name == PERCENTUAL_INTERSEC:
        return percentual_intersec

def calc_similarity_for_playlists(all_playlists, playlist_sim_dir, pids, similarity_metric, top_similars=21, sep=";"):
    '''
    It calculates similarity between each playlist inside a range and all playlists
    :param all_playlists: A dict where the key is the pid and the value is the song_id list
    :param playlist_sim_dir: path to save playlist's similarity
    :param pids: playlist ids to be calculed to all playlists
    :param simlarity_metric: name of the metric to be used to calculate similarity
    '''

    print("Calculating {}...".format(similarity_metric))
    similarity = pick_similarity_metric(similarity_metric)

    for a_pid in pids:
        pids = []
        for another_pid in all_playlists.keys():
            sim = similarity(all_playlists[a_pid], all_playlists[another_pid])
            pids.append({"pid": a_pid, "similar_pid": another_pid, similarity_metric: sim})

        print("Saving pid:", a_pid)

        pids_df = pd.DataFrame(pids).sort_values(similarity_metric, ascending=False).head(top_similars)
        pids_df.to_csv(playlist_sim_dir + str(a_pid) + ".csv", index=False, sep=sep)
