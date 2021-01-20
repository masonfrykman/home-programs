#!/usr/bin/env python

# some variables that are going to be at the top so they can be easily changed later.

CAMERA_DUMP_DIRECTORY = '' # the directory that the script will be active in. start from the root folder. Use forward slashes.
AMOUNT_TO_DELETE = 2000000000 # the maximum amount of data to delete IN BYTES. May go over a bit just because we dont want incomplete and corrupted files. 1 gigabyte = 1000000000 bytes
DO_DISKSPACE_CHECK = True # This is if you want to turn off the diskspace check. Turn to False if you want it off. Turn to True if you want it on.
KILL_SELF_IF_DISKSPACE_IS_ABOVE = 10000000000 # Will check if the disk's free space is above this. If it is, the script will kill itself, if not it will proceed. 1 gigabyte = 1000000000 bytes

# Essential imports to have this file work.

import os
from colorama import Fore, init
from shutil import disk_usage

init(autoreset=True)

print('Backup Maintainer :)\n')

# First, check if the Diskspace check is on, then do stuff accordingly.

if(DO_DISKSPACE_CHECK == True):
    print(Fore.CYAN + 'Running Diskspace Check...')
    totalFree = disk_usage(CAMERA_DUMP_DIRECTORY).free
    if(totalFree > KILL_SELF_IF_DISKSPACE_IS_ABOVE):
        print(Fore.YELLOW + 'Disk space free is above the defined byte amount. Killing self.')
        raise SystemExit
    else:
        print(Fore.GREEN + 'Disk Space')
else:
    print(Fore.CYAN + 'Diskspace Check is disabled.')

# Ok, now check to make sure the directory exists.s

print(Fore.CYAN + '\nChecking that the specified directory exists...')

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

d = [] # The full paths will be dumped here.
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

print(Fore.CYAN + '\nStarting to delete ' + str(AMOUNT_TO_DELETE) + " bytes of the oldest files in '" + CAMERA_DUMP_DIRECTORY + "'.")

if(AMOUNT_TO_DELETE <= 0):
    print('ERROR! AMOUNT_TO_DELETE cannot be 0 or lower. Change the value to be above zero please.')

amountOfBytesDeleted = 0

for fileTD in d:
    b = os.stat(fileTD).st_size
    os.remove(fileTD)
    amountOfBytesDeleted += b
    if(amountOfBytesDeleted > AMOUNT_TO_DELETE):
        break

print(Fore.GREEN + 'Successfully deleted ' + str(amountOfBytesDeleted) + ' bytes of data!')
print(Fore.YELLOW + 'Please note: The script may have gone over the maximum because partially deleting a file will leave it corrupted. If it went under, we probably ran out of files to delete.')
print('Have a great rest of your day/night <3')