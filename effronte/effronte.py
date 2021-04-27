# Effronte
# By Mason Frykman
# Licensed under AGPL 3.0 (GNU Affero General Public License version 3)

# Imports
import os
import argparse
import configparser
import subprocess
from shutil import copyfileobj
from datetime import datetime
# Argument stuff.

arger = argparse.ArgumentParser()
arger.add_argument('--config', type=str, help="Path to ini that will be used to configure stuff.", default='./effronte.ini')

args = arger.parse_args()

# Try and get config stuff.
cf = configparser.ConfigParser()
cf.read(args.config)

# Check if user is running as root, if check is enabled ofc.
if(os.getuid() != 0):
    print("Run as root.")
    raise SystemExit

forceConfigGenerator = cf['options']['forceConfigRewrite']

# Sanity check.
def pingCM(host):
    command = ['ping', '-c 3', '-W {}'.format(cf['configs']['sanityCheckTimeout']), host]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).communicate()
    return process

def ping(host):
    cat = pingCM(host)
    if(str(cat[0]).__contains__('100% packet loss')):
        return 1
    return 0

print('Running Sanity Check.')
print('Attempting ping of {} (sanityCheckPing1)'.format(cf['configs']['sanityCheckPing1']))
ping1 = ping(cf['configs']['sanityCheckPing1'])
if(ping1 == 0):
    print('Sanity Ping 1 succeeded.')
else:
    print('Sanity Ping 1 failed!')
    if(cf['options']['requireBothSanityChecksSatisfied']):
        print('ERROR: Sanity Ping 1 failed. Both are required to be satisfied (requireBothSanityChecksSatisfied is True)')
        raise SystemExit
    else:
        print('Still going to do ping 2.')
print('Attempting ping of {} (sanityCheckPing2)'.format(cf['configs']['sanityCheckPing2']))
ping2 = ping(str(cf['configs']['sanityCheckPing2']))
if(ping2 == 0):
    print('Sanity Ping 2 succeeded.')
else:
    print('Sanity Ping 2 failed!')
    if(cf['options']['requireBothSanityChecksSatisfied']):
        print('ERROR: Sanity Ping 2 failed. Both are required to be satisfied (requireBothSanityChecksSatisfied is True)')
        raise SystemExit

if(ping1 != 0 and ping2 != 0):
    print('ERROR: Both sanity pings failed. Please check your connection.')
    raise SystemExit

if(cf['options']['requireBothSanityChecksSatisfied']): # Just to be safe.
    if(ping1 != 0 or ping2 != 0):
        print('ERROR: One or both of the pings failed. Both are required to be satisfied (requireBothSanityChecksSatisfied is True)')
        raise SystemExit

# Attempt to ping the default DNS servers.
print('Attempting to ping default DNS Servers...')
defaultDNS = cf['configs']['default']
defaultDNS = defaultDNS.split(' ')
allPingsFailed = True
failedPings = []
for server in defaultDNS:
    print('Pinging {}...'.format(server))
    servping = ping(server)
    if(servping == 0):
        allPingsFailed = False
    else:
        failedPings.append(server)

serversToUse = []

if(allPingsFailed == True):
    print("\nAll Default DNS Servers didn't respond! Attempting to ping fallback DNS Servers...")
    fallbackDNS = cf['configs']['secondary'].split(' ')
    allFallbacksFailed = True
    failedFallPings = []
    for server in fallbackDNS:
        print('Pinging {}...'.format(server))
        servping = ping(server)
        if(servping == 0):
            allFallbacksFailed = False
        else:
            failedFallPings.append(server)
    
    if(allFallbacksFailed == True):
        print('ERROR: All fallbacks and default servers are unresponsive. Are you sure this program is sane? Check your connection & configuration.')
        raise SystemExit

    if(failedFallPings.count != 0 and allFallbacksFailed == False):
        if(cf['options']['eliminateUnresponsiveServers']):
            for server in fallbackDNS:
                failer = False
                for failed in failedFallPings:
                    if(server == failed):
                        failer = True
                        break
                if(failer == False):
                    serversToUse.append(server)
            #print(serversToUse)
        else:
            serversToUse = fallbackDNS
else:
    if(len(failedPings) != 0):
        print('\nThe following DNS Servers didnt respond to the pings:')
        for servers in failedPings:
            print(servers)
        print('')
        if(cf['options']['eliminateUnresponsiveServers']):
            for server in defaultDNS:
                failer = False
                for failed in failedPings:
                    if(server == failed):
                        failer = True
                        break
                if(failer == False):
                    serversToUse.append(server)
        else:
            serversToUse = defaultDNS

    else:
        print('All of the servers responded!\n')
        serversToUse = defaultDNS

print('Servers that will be defined in config:')
for server in serversToUse:
    print(server)

if(serversToUse.count == 0):
    print('ERROR: serversToUse is empty! There are no working servers! Program execution cannot continue at this point.')
    raise SystemExit

print('\nTrying to open the BIND9 current config and read the contents.')
try:
    global bindconfig
    bindconfig = open('/etc/bind/named.conf.options', 'r')
except FileNotFoundError:
    print('ERROR: Could not open BIND9 config (/etc/bind/named.conf.options). Do you have BIND installed?')
    raise SystemExit

bindlines = bindconfig.readlines()
#print(bindlines)
if(forceConfigGenerator == False):
    tracker = 0
    forwardersStart = None
    forwardersEnd = None
    for line in bindlines: # Find
        linemd = line.strip()
        #print(linemd)
        if(linemd.startswith("forwarders")):
            forwardersStart = tracker
        elif(linemd.startswith("}") and forwardersEnd == None and forwardersStart != None):
            forwardersEnd = tracker

        tracker += 1

    print(forwardersStart)

    if(forwardersStart == None):
        forceConfigGenerator = True

if(forceConfigGenerator == False):
    # Check if config is same as serversToUse
    ntrack = forwardersStart + 1
    oldConfigServers = []

    #while ntrack != forwardersEnd:
    #    oldConfigServers.append(bindlines[ntrack])
    #    ntrack += 1

    skipToConfigWrite = False
    # Check if config has more or less than defaults.
    if(oldConfigServers.count != serversToUse.count):
        skipToConfigWrite = True

    # Try to find one of the old servers non duplicate. if an old config server has no duplicate in the new servers, we need to recreate the config.
    if(skipToConfigWrite == False):
        exitWithoutADuplicate = False
        for oldserver in oldConfigServers:
            foundThisServersDuplicate = False
            for newserver in serversToUse:
                if(oldserver == newserver):
                    foundThisServersDuplicate = True
                
            if(foundThisServersDuplicate == False):
                exitWithoutADuplicate = True
                break
        
        if(exitWithoutADuplicate == True):
            skipToConfigWrite = True
        else:
            print('All defined servers to use are already in the config. If this is wrong, email mason@simbalou.com.')
            raise SystemExit
    
# Generate the new config.

print('Generating new config...')
configTemplate = [ # Each of the lines represents a line.
    'acl allowed {',
    # This is where the allowed clients servers go.
    '};',
    'options {',
    '\tdirectory "/var/cache/bind";',
    '\tforwarders {',
    # This is where the new servers will be inserted.
    '\t};',
    '\trecursion yes;',
    '\tforward only;',
    #This is where DNSSEC options will go.
    '\tauth-nxdomain no;',
    '\tallow-query { any; };',
    '\tallow-recursion { any; };',
    '};'
]

# Place DNSSEC options.

if(cf['configs']['doDNSSEC']):
    configTemplate.insert(9, '\tdnssec-validation yes;')
else:
    configTemplate.insert(9, '\tdnssec-validation no;')

# Place forwarders.
for server in serversToUse:
    configTemplate.insert(5, '\t\t' + server + ';')

print('\nCONFIG:')
for configline in configTemplate:
    print(configline)

time = datetime.now()
timestr = time.strftime('%b-%d-%Y_%I:%M:%S-%p')
#print(timestr)
backupPath = '/etc/bind/effronte-backup/{}.named.conf.options'.format(timestr)

print('Backing up old config to {}'.format(backupPath))
# Backup old config.

try:
    os.mkdir('/etc/bind/effronte-backup')
except FileExistsError:
    # This is expected.
    print('Directory already exists. This is good!')

try:
    global backupFile
    backupFile = open(backupPath, 'w+')
    global currentConfig
    currentConfig = open('/etc/bind/named.conf.options', 'r')
except FileExistsError:
    print('ERROR: Somehow a backup was made at this exact moment before and it errored? How is this possible?')
    raise SystemExit

try:
    copyfileobj(currentConfig, backupFile)
except FileNotFoundError:
    print('ERROR: Something went wrong where a file didnt exist during backup copying.')
    raise SystemExit

backupFile.close()
currentConfig.close()
print('Backed up.')
print('\nWriting new config to options.')

try:
    global configFileWriter
    configFileWriter = open('/etc/bind/named.conf.options', 'w+')
except OSError:
    print('ERROR: Something went wrong opening /etc/bind/named.conf.options for writing.')
    raise SystemExit

for line in configTemplate:
    configFileWriter.write(line + '\n')

if(cf['options']['attemptBindServiceRestart']):
    print('\nAttempting BIND9 restart.')
    systemctlres = subprocess.run(['systemctl', 'restart', 'bind9'])
    if(systemctlres.returncode == 0):
        print('Successfully restarted BIND9.')
    else:
        print('ERROR: BIND9 restart exited with a non-zero exit code. Please restart it manually.')

print('\nlol bye.')
