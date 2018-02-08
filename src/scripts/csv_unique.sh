#script to remove repeated rows and store them sorted
#arg1: input filepath
#arg2: output filepath

FILEPATH1=$1
FILEPATH2=$2

echo $FILEPATH1
echo $FILEPATH2

header=$( head -1 $FILEPATH1 )
echo $header

echo "$header" > $FILEPATH2

tail -n +2 $FILEPATH1 | sort | uniq >> $FILEPATH2
