#script to remove repeated rows and store them sorted
#arg1: input filepath
#arg2: output filepath

FILEPATH1=$1
FILEPATH2=$2

echo $FILEPATH1
echo $FILEPATH2

sort $FILEPATH1 | uniq -c > $FILEPATH2

