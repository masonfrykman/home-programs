# This is a script to print the free disk space.

import argparse
from shutil import disk_usage

ap = argparse.ArgumentParser(description='Prints the disk usage.')
ap.add_argument('path', type=str)

apparsed = ap.parse_args()

print('FREE: ' + str(disk_usage(apparsed.path).free))