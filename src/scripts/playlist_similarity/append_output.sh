#!/bin/bash

output_csv=/root/recsys/recsys_env/output.csv
output_path=/root/recsys/recsys_env/output/

echo $(head -n 1 $output_path$(ls -1t | head -n 1)) >> $output_csv
echo "percentual_intersec;pid;similar_pid" >> $output_csv

for file in $(ls ./output/); do
	path=$output_path$file
	while IFS= read -r line; do
		if [ ${line:0:1} != "p" ]; then
			#echo $line
			echo $line >> $output_csv
		fi
	done < $path
done

