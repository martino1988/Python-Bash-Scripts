#!/usr/bin/python3

import sys
import time
from progress.bar import IncrementalBar
from progress.bar import Bar
from datetime import datetime as dt
import socket

if len(sys.argv) == 4:
        target = socket.gethostbyname(sys.argv[1]) # translates host to ipv4
        startport = int(sys.argv[2])
        endport = int(sys.argv[3]) + 1
        barport = endport - 1

else:
        print("Invalid number of args")
        print("Syntax: python portscanner.py [ip/hostname] [beginning port] [ending port]")
        print("For example: python portscanner.py 192.168.1.1 20 443")
        sys.exit()
print("-" * 50)
print("Scannning target: " + target + " on Ports " + sys.argv[2] + " - " + sys.argv[3])
starttime = str(dt.now().strftime('%d.%m.%Y - %H:%M:%S'))


portlist = []

try:
        bar = Bar('Scanning', fill='#', max = (endport - startport), suffix='%(percent)d%%')
        for port in range(startport,endport):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.5)
                result = s.connect_ex((target, port))
                if result == 0:
                        portlist.append(port)
                s.close
                bar.next()

        bar.finish()
        print("-" * 50)
        print("Target: " + target)
        print("Time startetd: " + starttime)
        print("Time ended:    " + str(dt.now().strftime('%d.%m.%Y - %H:%M:%S')))
        print("Open Ports:")
        for x in portlist:
                print(" - Port {}".format(x))
        print("-" * 50)
except KeyboardInterrupt:
        print('\nExitting...')
        sys.exit()
except socket.gaierror:
        print("Hostname couldn't be resolved")
        sys.exit()
except socket.error:
        print("Couldn't connect to server")
        sys.exit()