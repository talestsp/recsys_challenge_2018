# Data Versions
Here you can checkout the data versions history and how it were obtained.

## 1.0
From raw data to three CSVs (playlists, tracks and play_track).
CSVs have no repeated rows and in order to decrease file size the following spotify prefixes were removed:
* 'spotify:track:'
* 'spotify:album:'
* 'spotify:artist:'

To get these data version you need to run the following scripts considering its input and outputs:
1. raw_data > **scripts/to_csv.py** > output1
2. output1 > **scripts/csv_unique.sh** output2
3. output2 > **scripts/remove_attribute_prefixes.sh** > output3 (data version 1.0)
