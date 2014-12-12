import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('directory')

args = parser.parse_args()

os.mkdir(args.directory)