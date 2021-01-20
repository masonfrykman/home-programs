#!/usr/bin/env python

# some variables that are going to be at the top so they can be easily changed later.

CAMERA_DUMP_DIRECTORY = 'C:/Users/Mason/Documents/Cydia' # the directory that the script will be active in. start from the root folder. Use forward slashes.
AMOUNT_TO_DELETE = 100 # the amount of data to delete IN BYTES. can go over but not under. as soon as it goes over the program kills itself.
KILL_SELF_IF_ABOVE_FREE = 900000000000000

# Essential imports to have this file work.

import os
from colorama import Fore, init, deinit
from pathlib import Path
init(autoreset=True)

print('Backup Maintainer :)\n')

# Ok, now check to make sure the directory exists.

print(Fore.CYAN + 'Checking that the specified directory exists...')

checkPathForExistence = os.path.isdir(CAMERA_DUMP_DIRECTORY)

if(checkPathForExistence == False):
    print(Fore.RED + "The path '" + CAMERA_DUMP_DIRECTORY + "' does not exist! Please check that the directory exists, it is a directory, and that the script has permissions to access it.")
    print("Exited without deleting files.")
    raise SystemExit
elif(checkPathForExistence == True):
    print(Fore.GREEN + "The path exists.")

# Now that we know the path exists, get a list of the files, and check that there are files.

print(Fore.CYAN + "\nGetting a list of the files in '" + CAMERA_DUMP_DIRECTORY + "'... (Just to make sure that we don't later try to delete what isn't there)")

filesInCD = [filesInCD for filesInCD in os.listdir(CAMERA_DUMP_DIRECTORY) if os.path.isfile(os.path.join(CAMERA_DUMP_DIRECTORY, filesInCD))]
try:
    test = filesInCD[0]
except IndexError:
    print(Fore.RED + "The directory '" + CAMERA_DUMP_DIRECTORY + "' doesn't contain any files. If you think this is a mistake, change the CAMERA_DUMP_DIRECTORY value.")
    print('Exiting without deleting files for safety.')
    raise SystemExit
except:
    print(Fore.RED + 'An unexpected error occured.')
    print('Exiting for safety.')
    raise SystemExit

if(CAMERA_DUMP_DIRECTORY.endswith('/') == False): # This is to make sure that when we append the filename, it has a slash at the end.
    CAMERA_DUMP_DIRECTORY_MOD = CAMERA_DUMP_DIRECTORY + '/'
else:
    CAMERA_DUMP_DIRECTORY_MOD = CAMERA_DUMP_DIRECTORY

d = []
i = 0

for filename in filesInCD:
    toAppend = CAMERA_DUMP_DIRECTORY_MOD + filename
    d.append(toAppend)

print(Fore.GREEN + 'Got the list successfully!')

# Now its time to sort the files from oldest to newest.

print(Fore.CYAN + '\nSorting the list from oldest to newest based on creation date...')
d.sort(key=os.path.getctime)
print(Fore.GREEN + 'Sorted!')

# Now start the deleting!!!

