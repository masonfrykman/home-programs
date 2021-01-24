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
COMBINED_DIRECTORY = clcfg['RootDirectory']

import os
import subprocess

def bm_start(path):
    with os.scandir(path) as it:
        for entry in it:
            print(entry.path)
            

bm_start(ROOT_DIRECTORY)