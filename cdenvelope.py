#!/usr/bin/python
# Creates a CD envelope pdf file from an m3u playlist
# of the CD's content.

import sys
import os.path
import shutil
from subprocess import call
import time

# Parse args, look into using argparse library
if not (len(sys.argv) >= 4):
	print "Specify .m3u filename & CD title and optionally, a ps image file"
	print "Usage: playlist title subtitle [image.ps]"
	sys.exit(2)

m3ufile=sys.argv[1]
album=sys.argv[2]
artist=sys.argv[3]

if not os.path.isfile(m3ufile):
	print "Playlist file not found!"
	sys.exit(1)

# Check if there's an image file given
imagearg = "--no-tray-plaque" # If no image, no tray plaque
if (len(sys.argv) == 5):
	imagefile=sys.argv[4]
	if not os.path.isfile(imagefile):
		print "Image file not found!"
		sys.exit(1)
	else:
		# If an image, no cover plaque
		imagearg='--no-cover-plaque -e ' + imagefile

file = open(m3ufile, 'r')
tlines = file.readlines()
i=1
list=''
for line in tlines:
	if (line.startswith("#EXTINF")):
		pre, title = line.split(",", 1)
		title = title.strip()
#		print str(i).rjust(2,' ') + " " +  title
		list += str(i).rjust(2,' ') + " " +  title + "%"
		i += 1

# Generate envelope
cmd = 'cdlabelgen --create-envelope -S 0 -D -o /tmp/cdenv.ps ' + imagearg + ' -i "' + list + '" -c "' + album + '" -s "' + artist + '"'

print(cmd)

call(cmd, shell=True)

# Convert to pdf
call(["ps2pdf","/tmp/cdenv.ps","/tmp/cdenv.pdf"])

print "Done, output is /tmp/cdenv.pdf"
