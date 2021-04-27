# effronte
A simple program to switch out BIND9 

## effronte.ini

### configs

default: REQUIRED! Default DNS server(s). Seperate with a space.  
secondary: REQUIRED! Fallback DNS server(s). Seperate with a space.  

sanityCheckPing1 & sanityCheckPing2: sanityCheckPing1 REQUIRED. Essentially just to check that the script has access to the LAN / Internet. DO NOT use any IPs in default and secondary for the sanity check. Use literally anything else.  
sanityCheckTimeoutMS: Seconds to wait for timeout on sanity check.  

allowedClients: Goes into the config, this defines what clients are allowed to query. Separate with a space.  
doDNSSEC: Turns on and off DNSSEC validation.  

### options

attemptBindServiceRestart: If set to true, restart the Bind9 service at the end.  
requireBothSanityChecksSatisfied: If set to true, requires both of the sanity pings to be satisfied. False only requires one.  
eliminateUnresposiveServers: If set to true, servers that don't respond to pings wont be included in the forwarders section of the config.  
forceConfigRewrite: If set to true, skips getting old config servers and comparing them. Essentially writes a new config every run.
