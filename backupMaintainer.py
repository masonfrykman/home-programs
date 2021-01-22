#!/usr/bin/env python

# some variables that are going to be at the top so they can be easily changed later.

CAMERA_DUMP_DIRECTORY = '' # the directory that the script will be active in. start from the root folder. Use forward slashes.
KILL_SELF_IF_DISKSPACE_IS_ABOVE = 15000000000 # Will check if the disk's free space is above this. If it is, the script will kill itself, if not it will proceed. 1 gigabyte = 1000000000 bytes
DO_DISKSPACE_CHECK = True # This is if you want to turn off the diskspace check. Turn to False if you want it off. Turn to True if you want it on.
WRITE_TO_LOG = True # sets if it will write to bm.log

# Essential imports to have this file work.

import os
from colorama import Fore, init
from shutil import disk_usage
from datetime import datetime

init(autoreset=True)

today = datetime.now()

def toLog(message, wlvl):
    if(WRITE_TO_LOG == True):
        log = open('./bm.log', 'a')
        if(message == 'Initializing Backup Manager'):
            log.write('\n\n[{} '.format(wlvl) + today.strftime("%d.%m.%Y %H:%M:%S] ") + message)
        else:
            log.write('\n[{} '.format(wlvl) + today.strftime("%d.%m.%Y %H:%M:%S] ") + message)
        log.close()


# Initialize the log.

toLog('Initializing Backup Manager', 'INFO')
print('Backup Maintainer :)\n')

# First, check if the Diskspace check is on, then do stuff accordingly.

if(DO_DISKSPACE_CHECK == True):
    print(Fore.CYAN + 'Running Diskspace Check...')
    toLog('Running Diskspace Check.', 'INFO')
    try:
        totalFree = disk_usage(CAMERA_DUMP_DIRECTORY).free
    except FileNotFoundError:
        print(Fore.RED + 'Could not find the directory defined in CAMERA_DUMP_DIRECTORY! Check the directory!')
        toLog('Could not find the directory defined in CAMERA_DUMP_DIRECTORY! Check the directory!', 'ERROR')
        raise SystemExit

    totalFree = disk_usage(CAMERA_DUMP_DIRECTORY).free
    if(totalFree > KILL_SELF_IF_DISKSPACE_IS_ABOVE):
        print(Fore.YELLOW + 'Disk space free is above the defined byte amount to start deletion. Exitting.')
        toLog('Disk space free is above the defined byte amount to start deletion. Exitting.', 'INFO')
        raise SystemExit
    else:
        print(Fore.GREEN + 'Disk Space is under the amount of free space required to stop execution. Proceeding.')
        toLog('Disk Space is under the amount of free space required to stop execution. Proceeding.', 'INFO')
else:
    print(Fore.CYAN + 'Diskspace Check is disabled.')
    toLog('Diskspace Check is disabled.', 'INFO')

# Ok, now check to make sure the directory exists.s

print(Fore.CYAN + '\nChecking that the specified directory exists...')
toLog('Checking that the specified directory exists...', 'INFO')

checkPathForExistence = os.path.isdir(CAMERA_DUMP_DIRECTORY)

if(checkPathForExistence == False):
    print(Fore.RED + "The path '" + CAMERA_DUMP_DIRECTORY + "' does not exist! Please check that the directory exists, it is a directory, and that the script has permissions to access it.")
    print("Exited without deleting files.")
    toLog("The path '" + CAMERA_DUMP_DIRECTORY + "' does not exist! Please check that the directory exists, it is a directory, and that the script has permissions to access it. Exiting.", 'ERROR')
    raise SystemExit
elif(checkPathForExistence == True):
    print(Fore.GREEN + "The path exists.")
    toLog("The path exists.", 'INFO')

# Now that we know the path exists, get a list of the files, and check that there are files.

print(Fore.CYAN + "\nGetting a list of the files in '" + CAMERA_DUMP_DIRECTORY + "'... (Just to make sure that we don't later try to delete what isn't there)")
toLog("Getting a list of the files in '" + CAMERA_DUMP_DIRECTORY + "'... (Just to make sure that we don't later try to delete what isn't there)", 'INFO')

filesInCD = [filesInCD for filesInCD in os.listdir(CAMERA_DUMP_DIRECTORY) if os.path.isfile(os.path.join(CAMERA_DUMP_DIRECTORY, filesInCD))]
try:
    test = filesInCD[0]
except IndexError:
    print(Fore.RED + "The directory '" + CAMERA_DUMP_DIRECTORY + "' doesn't contain any files. If you think this is a mistake, change the CAMERA_DUMP_DIRECTORY value.")
    print('Exiting without deleting files for safety.')
    toLog("The directory '" + CAMERA_DUMP_DIRECTORY + "' doesn't contain any files. If you think this is a mistake, change the CAMERA_DUMP_DIRECTORY value. Exiting", 'ERROR')
    raise SystemExit
except:
    print(Fore.RED + 'An unexpected error occured.')
    print('Exiting for safety.')
    toLog('An unexpected error occured. Exiting just to be safe.', 'ERROR')
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
toLog('Sorting the list from oldest to newest based on creation date...', 'INFO')
d.sort(key=os.path.getctime)
print(Fore.GREEN + 'Sorted!')
toLog('Sorted', 'INFO')

# Now start the deleting!!!

toOut = 'Starting to delete data until free space of ' + str(disk_usage(CAMERA_DUMP_DIRECTORY).free)

print(Fore.CYAN + '\n' + toOut)
toLog(toOut, 'INFO')

if(KILL_SELF_IF_DISKSPACE_IS_ABOVE <= 0):
    print(Fore.RED + 'ERROR! KILL_SELF_IF_DISKSPACE_IS_ABOVE cannot be 0 or lower. Change the value to be above zero please.')
    print('Exiting without deleting.')
    toLog('ERROR! KILL_SELF_IF_DISKSPACE_IS_ABOVE cannot be 0 or lower. Change the value to be above zero please. Exiting', 'ERROR')
    raise SystemExit

amountOfBytesDeleted = 0

for fileTD in d:
    b = os.stat(fileTD).st_size
    os.remove(fileTD)
    amountOfBytesDeleted += b
    if(disk_usage(CAMERA_DUMP_DIRECTORY).free >= KILL_SELF_IF_DISKSPACE_IS_ABOVE):
        break

print(Fore.GREEN + 'Successfully deleted ' + str(amountOfBytesDeleted) + ' bytes of data!')
toLog('Successfully deleted ' + str(amountOfBytesDeleted) + ' bytes of data!', 'INFO')
print(Fore.YELLOW + 'Please note: The script may have gone over the maximum because partially deleting a file will leave it corrupted. If it went under, we probably ran out of files to delete.')
toLog('Please note: The script may have gone over the maximum because partially deleting a file will leave it corrupted. If it went under, we probably ran out of files to delete.', 'INFO')
print('Have a great rest of your day/night <3')
toLog('Have a great rest of your day/night <3', 'INFO')