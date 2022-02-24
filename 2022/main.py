#!/usr/local/bin/python3

import sys

if len(sys.argv) <= 1:
    print("Manca il nome del file")
    exit(1)

fileName = sys.argv[1]

print(f"--- START FILE {fileName} ---")

inputFileName = f"in/{fileName}.in"
outputFileName = f"{fileName}.out"

inFile = open(inputFileName, 'r')
outFile = open(outputFileName, 'w+')