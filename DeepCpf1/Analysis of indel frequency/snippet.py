#!/usr/bin/python
# -*- coding: utf-8 -*-

# Original code is here, https://github.com/MyungjaeSong/Paired-Library.git
# This is the modified version of the program to academic use in SKKUGE Lab

__author__ = "forestkeep21@naver.com"
__editor__ = "poowooho3@g.skku.edu"

import re
import sys
import os
import xlsxwriter
import time

BASE_DIR = os.path.dirname(sys.executable)

# for debug
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def seq_validator(data):
	# https://docs.python.org/3/library/re.html#re.findall
	m = re.findall(r"^[A|a|T|t|C|c|G|g]+$", data)
	return m[0] if m else None


def count_lines_in_a_file(file_name):
	count = 0
	for line in open(file_name, "r"):
		count += 1
	return count


def do(barcode_file_name, FASTA_file_name):

	start_time = time.time()

	# 프로그램 진행율을 계산하기 위해 파일의 라인수를 센다.
	src_line_cnt = count_lines_in_a_file(barcode_file_name)
	if src_line_cnt == 0:
		# original code -- Python 2.x
		# print u'File Not Found'

		# Replaced the original part with the print 'function' in accordance with Python 3.x convention
		# https://stackoverflow.com/questions/2464959/whats-the-u-prefix-in-a-python-string
		print("File Not Found")
		raise
	current_cnt = 0

	result_folder_name = os.path.join(BASE_DIR, "results")
	# 결과가 저장될 폴더가 없다면 하나 생성
	if not os.path.exists(result_folder_name):
		os.makedirs(result_folder_name)

	# all extended data frags are stored in a list
	sequence_data = [
		line.strip() for line in open(FASTA_file_name, "r") if seq_validator(line)
	]

	barcode_data = [line for line in open(barcode_file_name, "r")]

	workbook = xlsxwriter.Workbook("results/result_info.xlsx")
	worksheet = workbook.add_worksheet("Barcode extraction result")

	try:
		# 읽어온 바코드를 속도를 위해 모두 메모리에 올려놓고 분석을 시작한다.
		for barcode in barcode_data:
			# merge statistics codes into the main body of the 'do' function

			# 바코드셋은 :를 구분자로 앞은 파일명, 뒤는 바코드로 되어있다.
			barcode_set = barcode.split(":")
			if len(barcode_set) < 2:
				continue
			# 파일명에서 화이트 스페이스 삭제
			sequence_name = barcode_set[0].strip()
			# 바코드가 valid한지 검증
			barcode = seq_validator(barcode_set[1].strip())

			# debug code -- logging
			log = open("log.txt", "w") 



			# detected = []

			# 결과가 저장될 파일명 지정
			sequence_name = os.path.join(
				result_folder_name, "{}.txt".format(sequence_name)
			)
			detected = 0
			
			# 결과 파일 쓰기 시작
			with open(sequence_name, "w") as f:
				# 추출된 대상 시퀸스들을 파일에 쓴다.
				# 대상이 되는 시퀸스들을 하나하나 분석한다.
				for sequence in sequence_data:
					# 비교를 위해 바코드, 대상 시퀸스 둘다 소문자로 변환하여 바코드가 대상 시퀸스 내에 존재하는지 검사
					# O(n)
					if barcode.lower() in sequence.lower():
						f.write("{}\n".format(sequence))
						detected += 1

			# 총 결과 파일에 파일명 : 라인수 형식으로 쓴다.
			worksheet.write(current_cnt, 0, sequence_name)
			worksheet.write(current_cnt, 1, ":")
			# worksheet.write(current_cnt, 2, len(detected))
			worksheet.write(current_cnt, 2, detected)

			# 파일에 전부 옮겨담았다면 메모리에 올라간 전체 대상 시퀸스들에서 파일에 쓴 대상 시퀸스를 뺀다.
			# [sequence_data.remove(used_datum) for used_datum in detected]

			# 프로그램 진행율 계산 부분
			current_cnt += 1
			# progress_percentage = float(current_cnt) / src_line_cnt * 100
			print(f"{current_cnt} out of {src_line_cnt} barcodes are proccessed.")

	except Exception as e:
		print(e)
		# Replaced the original part with the print 'function' in accordance with Python 3.x convention
		print("Extraction Failure.")
		raise

	workbook.close()
	print("--- %s seconds ---" % (time.time() - start_time))


print("Input barcode file name with extension: ")
# barcode_file_name = inputdest_file_name = input()
barcode_file_path = os.path.join(BASE_DIR, "src/barcode.txt")
if not os.path.isfile(barcode_file_path):
	print("Barcode is not found. Check it is located in the 'src' directory")
	raise

print("Input FASTA file path: ")
# FASTA_file_path = input()
# FASTA_file_path = os.path.join(FASTA_file_path)

# if FASTA_file_path[0] == "'" or '"':
#     FASTA_file_path = FASTA_file_path[1:-1]

# if not os.path.isfile(FASTA_file_path):
#     print("File Not Found. Check it is in same folder")
#     raise

FASTA_file_path = "/Users/juyoungshin/Dropbox/Codes/pyGE_general/DeepCpf1/Analysis of indel frequency/src/processed/SKKUGE_input_example.txt.extendedFrags.fastq"
if FASTA_file_path[0] == ("'" or '"') and not (FASTA_file_path[-1] != r"[a-z]"):
	FASTA_file_path = FASTA_file_path[1:-1]

if not os.path.isfile(FASTA_file_path):
	print("File Not Found. Check it is in same folder")
	raise


do(barcode_file_path, FASTA_file_path)

print("Extraction is completed.")
