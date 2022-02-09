#!/usr/bin/python
# -*- coding: utf-8 -*-

# An automation program for NGS analysis in SKKUGE

# 1. 유저 입력으로 원하는 루트 디렉토리에 있는 NGS 파일 여러개를 지정 ⇒ TBD: 경로 지정 기능 추가?
# 2. 이들 파일을 FLASH로 processing (argument는 저장해둔 lab protocol 을 따름)
#     1. 없는 파일에 대해서는 skip
#     2. 하나도 파일 없을 때는 다시 1로

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

import extractor_v3 as ex

raw_data = [
    line.strip()
    for line in open(
        "/Users/juyoungshin/Dropbox/Codes/pyGE_general/DeepCpf1/src/processed/SKKUGE_input_example.txt.extendedFrags.rtf",
        "r",
    )
    if ex.seq_validator(line)
]

