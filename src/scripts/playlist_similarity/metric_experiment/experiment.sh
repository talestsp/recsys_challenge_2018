#!/usr/bin/env bash

PYTHONPATH=.:src ~/anaconda3/bin/python src/scripts/playlist_similarity/similar_playlists_multi_cpu.py /home/tales.tsp/dev/recsys_challenge_2018/src/scripts/playlist_similarity/metric_experiment/jaccard_config.json
PYTHONPATH=.:src ~/anaconda3/bin/python src/scripts/playlist_similarity/similar_playlists_multi_cpu.py /home/tales.tsp/dev/recsys_challenge_2018/src/scripts/playlist_similarity/metric_experiment/percentual_intersec_config.json
