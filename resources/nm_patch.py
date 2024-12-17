#!/opt/homebrew/bin/python3
import sys
import os

args = sys.argv[1:]
args.remove("--dynamic")
os.execvp("nm", args)