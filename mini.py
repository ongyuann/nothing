#!/usr/bin/python3

import sys,subprocess

address = sys.argv[1].split(":")[0]
port = sys.argv[1].split(":")[1]

cmd = "nmap -v --script=http-* -p "+port+" "+address+" -oN http_"+address+":"+port

res = subprocess.call(cmd,shell=True)
print (res)
