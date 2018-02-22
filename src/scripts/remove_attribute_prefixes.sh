#first argument: path to play_track.csv
#second argument: path to tracks.csv

PLAYTRACK_PATH=$1
TRACKS_PATH=$2

echo "processing $PLAYTRACK_PATH"
echo "removing 'spotify:track:'"
sed -e s/spotify:track://g -i $PLAYTRACK_PATH

echo "processing $TRACKS_PATH"
echo "removing 'spotify:track:'"
sed -e s/spotify:track://g -i $TRACKS_PATH
echo "removing 'spotify:album:'"
sed -e s/spotify:album://g -i $TRACKS_PATH
echo "removing 'spotify:artist:'"
sed -e s/spotify:artist://g -i $TRACKS_PATH

