#!/usr/bin/python
import os, shutil, socket, subprocess, datetime

homedir = os.getenv("HOME")
copydir = "/mnt/D/Backups"
backupdir = "%s/backups" % homedir
prefix = socket.gethostname()
filename = "fullbackup-%s.tar.bz2" % prefix
src = "%s/%s" % (backupdir, filename)

def backup():
  if os.path.isdir(backupdir) ==  False:
    os.mkdir(backupdir, 744)
    print "[ %s ] Created %s directory" % (time(), backupdir)
  tarexec = ("nice -n 19 ionice -c 3 -n 7 tar -cvpjf %s/%s / /home /boot --exclude=%s --exclude=%s --one-file-system"
  % (backupdir, filename, backupdir, copydir))
  tarexec = tarexec.split()
  outlog = "%s/out.log" % backupdir
  errlog = "%s/err.log" % backupdir
  out = open(outlog, 'w')
  err = open(errlog, 'w')
  print "[ %s ] Starting backup process" % time()
  proc = subprocess.Popen(tarexec, stdout=out, stderr=err)
  proc.wait()
  out.close()
  err.close()

def copybackup():
  dst = "%s/%s" % (copydir, filename)
  if os.path.isdir(copydir) == True:
    if os.path.exists(dst) == True:
      print "[ %s ] Deleting previous version before copying" % time()
      os.remove(dst)
    print "[ %s ] Copying backup to %s" % (time(), copydir)
    shutil.copyfile(src, dst)
    print "[ %s ] Done" % time()
  else:
    print "[ %s ] Skipping copying" % time()

def bsize():
  if os.path.getsize(src)/1073741824 == 0:
    bsize = round(float(os.path.getsize(src))/1048576, 2)
    print "[ %s ] Backup is done with size of %sMB" % (time(), bsize)
  else:
    bsize = round(float(os.path.getsize(src))/1073741824, 2)
    print "[ %s ] Backup is done with size of %sGB" % (time(), bsize)

def time():
  time = str(datetime.datetime.now())[:19]
  return time

def main():
  backup()
  bsize()
  copybackup()

try:
  main()
except KeyboardInterrupt:
  print "\n[ %s ] Backup process is terminated" % time()
