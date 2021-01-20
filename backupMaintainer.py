# some variables that are going to be at the top so they can be easily changed later.

CAMERA_DUMP_DIRECTORY = 'C:/' # the directory that the script will be active in. start from the root folder.
AMOUNT_TO_DELETE = -1 # the amount of data to delete. can go over but not under.

# Essential imports to have this file work.

import os
from colorama import Fore, init, deinit
init(autoreset=True)

# Ok, now check to make sure the directory exists.

print('Backup Maintainer :)\n')

print(Fore.CYAN + 'Checking that the specified directory exists...')

checkPathForExistence = os.path.isdir(CAMERA_DUMP_DIRECTORY)

if(checkPathForExistence == False):
    print(Fore.RED + "The path '" + CAMERA_DUMP_DIRECTORY + "' does not exist! Please check that the directory exists, it is a directory, and that the script has permissions to access it.")
    print("Exited without deleting files.")
    raise SystemExit
elif(checkPathForExistence == True):
    print("The path exists.")

# Now that we know the path exists, get a list of the files.



deinit()