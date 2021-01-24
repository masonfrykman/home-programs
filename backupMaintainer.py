#!/usr/bin/env python

# The 3 other variables are now stored in configs.ini. We just have WRITE_TO_LOG so that they can write to log if 

WRITE_TO_LOG = True # sets if it will write to bm.log

# Essential imports to have this file work.

import os
from colorama import Fore, init
from shutil import disk_usage
from datetime import datetime
import configparser

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


print('Backup Maintainer :)\n')

# Get variables from INI file.

cfg = configparser.ConfigParser()
cfg.read('configs.ini')
if('BackupMaintainer' in cfg == False):
    print(Fore.RED + 'configs.ini: There is no section in configs.ini called BackupMaintainer! Please fix the issue.')
    toLog('configs.ini: There is no section in configs.ini called BackupMaintainer! Please fix the issue.', 'ERROR')
    raise SystemExit

bkkeys = cfg['BackupMaintainer']

try:
    x = bkkeys['WriteToLog']
except KeyError:
    out = "configs.ini: Cannot get the key 'WriteToLog' from the BackupMaintainer section."
    print(Fore.RED + out)
    toLog(out, 'ERROR')
    raise SystemExit

try:
    x = bkkeys['CameraDumpDirectory']
except KeyError:
    out = "configs.ini: Cannot get the key 'CameraDumpDirectory' from the BackupMaintainer section."
    print(Fore.RED + out)
    toLog(out, 'ERROR')
    raise SystemExit

try:
    x = bkkeys['KillIfAboveBytes']
except KeyError:
    out = "configs.ini: Cannot get the key 'KillIfAboveBytes' from the BackupMaintainer section."
    print(Fore.RED + out)
    toLog(out, 'ERROR')
    raise SystemExit

try:
    x = bkkeys['DiskFreeCheck']
except KeyError:
    out = "configs.ini: Cannot get the key 'DiskFreeCheck' from the BackupMaintainer section."
    print(Fore.RED + out)
    toLog(out, 'ERROR')
    raise SystemExit

CAMERA_DUMP_DIRECTORY = bkkeys['CameraDumpDirectory']
KILL_SELF_IF_DISKSPACE_IS_ABOVE = int(bkkeys['KillIfAboveBytes'])
DO_DISKSPACE_CHECK_STR = bkkeys['DiskFreeCheck']
WRITE_TO_LOG_STR = bkkeys['WriteToLog']

if(DO_DISKSPACE_CHECK_STR.lower() == 'yes'):
    DO_DISKSPACE_CHECK = True
elif(DO_DISKSPACE_CHECK_STR.lower() == 'no'):
    DO_DISKSPACE_CHECK = False
else:
    out2 = 'configs.ini: DiskFreeCheck is not "yes" or "no". Check the key to make sure it is correct.'
    print(Fore.RED + out2)
    toLog(out2, 'ERROR')
    raise SystemExit

if(WRITE_TO_LOG_STR.lower() == 'yes'):
    WRITE_TO_LOG = True
elif(WRITE_TO_LOG_STR.lower() == 'no'):
    WRITE_TO_LOG = False
else:
    out3 = 'configs.ini: WriteToLog is not "yes" or "no". Check the key to make sure it is correct. Defaulting to yes.' # This not being set isn't catastrophic.
    toLog(out3, 'WARN')
    print(Fore.YELLOW + out3)

toLog('Running Backup Manager with Configs set.', 'INFO')

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