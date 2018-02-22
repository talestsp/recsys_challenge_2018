def dataset_slices2(from_pid, to_pid, n_threads):
    '''
    Builds a list of ranges that each thread will apply to dataset
    :param n_cpus: number of CPUs to be in parallelized
    :param playtrack: DataFrame of play_track.csv
    :param from_pid:
    :param to_pid:
    :return:
    '''
    range_len = to_pid - from_pid
    current_from_pid = from_pid

    dataset_range = int(math.ceil(range_len / n_threads))
    ranges = []


    for i in range(n_threads - 1):
        current_to_pid = current_from_pid + dataset_range
        ranges.append({"from_pid": current_from_pid,
                       "to_pid": current_to_pid})
        current_from_pid = current_to_pid + 1

    #create a task for the missing rounds
    ranges.append({"from_pid": current_from_pid, "to_pid": to_pid})
    return ranges