# Dumper
# Scans a directory and dumps it to a single folder.
# Made for my FTP Cam server
# To disclude a file, make it start with DUMPEXCLUDE.

# Useful variables

import configparser

cfg = configparser.ConfigParser()
cfg.read('configs.ini')
if('Dumper' in cfg == False):
    print('configs.ini: There is no Dumper section in configs.ini. Please make one or correct any typos.')
    raise SystemExit

dumpcfg = cfg['Dumper']

try:
    x = dumpcfg['StartingDirectory']
except KeyError:
    print('configs.ini: Cannot get key StartingDirectory. Please make one under the Dumper section.')
    raise SystemExit

try:
    x = dumpcfg['DumpPath']
except KeyError:
    print('configs.ini: Cannot get key DumpPath. Please make one under the Dumper section.')
    raise SystemExit

try:
    x = dumpcfg['DumpFolderName']
except KeyError:
    print('configs.ini: Cannot get key DumpFolderName. Please make one under the Dumper section.')
    raise SystemExit

THUMB_DRIVE_FDIR = dumpcfg['StartingDirectory']
MOVE_FILES_TO = dumpcfg['DumpPath']
COMBINED_FLDR_NAME = dumpcfg['DumpFolderName']

# Imports

import os

# Check the directories for existance

try:
    os.chdir(THUMB_DRIVE_FDIR)
except NotADirectoryError:
    print(THUMB_DRIVE_FDIR + ' is not a directory.')
    raise SystemExit

try:
    os.chdir(MOVE_FILES_TO)
except NotADirectoryError:
    print(MOVE_FILES_TO + ' is not a directory.')
    raise SystemExit

def dm_scan(wd):
    print('Working in ' + wd)
    with os.scandir(wd) as it:
        for entry in it:
            #print('Found: ' + entry.name)
            #print(entry)
            if(entry.name == 'System Volume Information'):
                # This is SVI! Dont delete!
                pass
            elif(entry.name == COMBINED_FLDR_NAME):
                # This is where dumper will be dumping. Skip it.
                pass
            elif(entry.name.startswith('DUMPEXCLUDE') and entry.is_file()):
                # This file is marked to be kept where it is.
                pass
            elif(entry.name.startswith('reolink_test')):
                foundRLTestFolder(entry.path)
            else:
                if(entry.is_dir()):
                    # We are going to loop it to
                    #print(entry.path)
                    dm_scan(entry.path)
                elif(entry.is_file()):
                    # This is where we move all the files.
                    dm_moveFiles(entry.path, entry.name)
                    
def dm_moveFiles(fp, filename):
    #print('DMMF: ' + fp) 
    os.rename(fp, MOVE_FILES_TO + '/' + filename)

def foundRLTestFolder(path):
    with os.scandir(path) as it:
        for entry in it:
            os.remove(entry.path)

    os.rmdir(path)


# Start the looping.
dm_scan(THUMB_DRIVE_FDIR)
