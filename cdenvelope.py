#!/usr/bin/python
# Creates a CD envelope pdf file from an m3u playlist
# of the CD's content.

import sys
import os.path
import shutil
from subprocess import call
import time

# Save .m3u file
if not (len(sys.argv) == 4):
	print "Specify .m3u filename & CD title"
	print "Usage: playlist title artist"
	sys.exit(2)
m3ufile=sys.argv[1]
album=sys.argv[2]
artist=sys.argv[3]
if not os.path.isfile(m3ufile):
	print "m3u file not found"
	sys.exit(1)

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
cmd = 'cdlabelgen --create-envelope -b -D -o /tmp/cdenv.ps -i "' + list + '" -c "' + album + '" -s "' + artist + '"'
# This command will add an image, TODO add it to the args.
#cmd = 'cdlabelgen --create-envelope -S 0 -e ~/Downloads/fro.eps -b -D -o /tmp/cdenv.ps -i "' + list + '" -c "' + album + '" -s "' + artist + '"'

call(cmd, shell=True)

# Convert to pdf
call(["ps2pdf","/tmp/cdenv.ps","/tmp/cdenv.pdf"])

print "Done, output is /tmp/cdenv.pdf"
