#!/bin/bash -ex

PORT=/dev/ttyACM0
MPREMOTE=./mpremote/bin/mpremote

# Create font
#python3 ../microfont/font_to_microfont.py -k charset.txt ../microfont/freesansbold.ttf 40 font.mfnt
#python3 ../microfont/font_to_microfont.py -e 32 -k charset.txt /usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf 30 font.mfnt 
python3 ../microfont/font_to_microfont.py -e 32 -k charset.txt /usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf 30 font.mfnt 

# Send ctrl+c to break any running program
echo $'\cc' > $PORT

# Upload all py and font files
shopt -s nullglob
$MPREMOTE connect $PORT fs cp *.py *.mfnt :

# Send ctrl+d to reinitialize
echo $'\cd' > $PORT

# Uncomment the following to get console right after reinit
#minicom -D $PORT