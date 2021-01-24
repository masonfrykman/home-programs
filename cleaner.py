# Cleaner
# A file to periodically clear the nest of folders that the camera system makes.



import configparser

cfg = configparser.ConfigParser()
cfg.read('configs.ini')

if('Cleaner' in cfg == False):
    print('configs.ini: No Cleaner section could be found. Please make one.')
    raise SystemExit

clcfg = cfg['Cleaner']

try:
    x = clcfg['RootDirectory']
except KeyError:
    print('configs.ini: Could not find the key RootDirectory in the Cleaner section.')
    raise SystemExit

try:
    x = clcfg['CombinedDirectory']
except KeyError:
    print('configs.ini: Could not find the key CombinedDirectory in the Cleaner section.')
    raise SystemExit

ROOT_DIRECTORY = clcfg['RootDirectory']
COMBINED_DIRECTORY = clcfg['CombinedDirectory']

print(ROOT_DIRECTORY)
print(COMBINED_DIRECTORY)

import os

class Directory:
    def __init__(self, path, level):
        self.path = path
        self.level = level
        self.isDeleted = False
        self.shouldSkipDelete = False

foundpaths = []



def bm_scanPath(pathz):
    with os.scandir(pathz.path) as it:
        for entry in it:
            print('Found: ' + entry.path)
            if(entry.name == 'System Volume Information'):
                print('Skipping SVI')
            elif(entry.path == COMBINED_DIRECTORY):
                print('Skipping Combined Directory')
            else:
                if(os.path.isdir(entry.path) == False):
                    print('Not a directory')
                else:
                    newDir = Directory(entry.path, pathz.level + 1)
                    foundpaths.append(newDir)
                    bm_scanPath(newDir)

rootdir = Directory(ROOT_DIRECTORY, 1)

bm_scanPath(rootdir)

# Get the max level

maxLevel = 0

for ent in foundpaths:
    if(ent.level > maxLevel):
        maxLevel = ent.level
        print('Elevated to Level ' + str(maxLevel))

print(foundpaths)
for ent in foundpaths:
    print(ent.path)
    print(ent.path.upper() + ' '  + str(ent.level))

while True:
    for ent in foundpaths:
        if(ent.level == maxLevel):
            try:
                os.rmdir(ent.path)
            except OSError:
                pass

    maxLevel -= 1
    if(maxLevel < 0):
        break


