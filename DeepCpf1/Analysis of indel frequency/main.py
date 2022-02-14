#!/usr/bin/python
# -*- coding: utf-8 -*-

# An automation program for NGS analysis in SKKUGE


""" 
import os
import sys

from Bio import SeqIO

# TODO : timeit module

#
# get the path of absolute cwd
#
dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
if 'darwin' in sys.platfrom:
    FLASH_dir = "./flash"
# User input - number of NGS pairs
#     file name format are like below
#         xx_Sxx_L001_R1_001.fastq.gz
#         xx_Sxx_L001_R1_001.fastq.gz
print("Prerequisite: compiled FLASH (named flash) for your system and it should be located with your NGS files")
n = input("Type how many files you want to process"
          "(hint: make half of the total sequence files)"
          ": ")

print(f"{n} sequences will be processed with FLASH".center(40, '#'))



# executing FLASH while inform the current status to the USER
os.execl(dir) """


# -- debug code --

# import extractor as ex

# raw_data = [
#     line.strip()
#     for line in open(
#         "/Users/juyoungshin/Dropbox/Codes/pyGE_general/DeepCpf1/src/processed/SKKUGE_input_example.txt.extendedFrags.rtf",
#         "r",
#     )
#     if ex.seq_validator(line)
# ]
