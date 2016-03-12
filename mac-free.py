#!/usr/bin/python
import shutil, os, sys

source = raw_input('Enter the name of file with MAC-s: ')
dest = raw_input('Enter the name of dhcpd config (will be changed!): ')

try:
   a = open(dest)
except IOError:
   print "File '%s' not found" % dest
   sys.exit(0)
else:
   text = a.read()
   a.close()

try:
   b = open(source)
except IOError:
   print "File '%s' not found" % source
   sys.exit(0)
else:
   lines = [line.rstrip('\n') for line in open(source)]

for line in lines:
   text = text.replace(line, 'FREE')

path = os.getcwd()
dpath = "%s/%s" % (path, dest)
dbpath = "%s/%s.backup" % (path, dest)
shutil.copyfile(dpath, dbpath)
print "Copying original config to %s" % dbpath

a = open(dest, 'w')
a.write(text)
a.close()
