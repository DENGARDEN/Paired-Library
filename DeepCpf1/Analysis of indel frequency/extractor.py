#!/usr/bin/python
# -*- coding: utf-8 -*-

# Original code is here, https://github.com/MyungjaeSong/Paired-Library.git
# This is the modified version of the program for academic uses in SKKUGE Lab

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


def help():
    """[Extracting nucleotide sequence from NGS result with specific barcodes]"""


def seq_validator(data):
    m = re.findall(r"^[A|a|T|t|C|c|G|g]+$", data)
    return m[0] if m else None


def count_line_in_file(file_name):
    count = 0
    for line in open(file_name, "r"):
        count += 1
    return count


def do(src_file_name, dest_file_name):
    start_time = time.time()

    # 프로그램 진행율을 계산하기 위해 파일의 라인수를 센다.
    src_line_cnt = count_line_in_file(src_file_name)
    if src_line_cnt == 0:
        print("File Not Found")
        raise
    current_cnt = 0
    extracted_line_index = []

    # 결과가 저장될 폴더 지정
    result_folder_name = os.path.join(BASE_DIR, "results")
    # 결과가 저장될 폴더가 없다면 하나 생성
    if not os.path.exists(result_folder_name):
        os.makedirs(result_folder_name)

    # 총 결과 파일명 지정
    result_info_file_name = os.path.join(result_folder_name, "result_info.txt")

    # file I/O -- txt, xlsx
    result_info_txt = open(result_info_file_name, "w")
    workbook = xlsxwriter.Workbook("results/result_info.xlsx")
    worksheet = workbook.add_worksheet("Barcode extraction result")

    # 추출할 시퀸스가 있는 파일을 읽어온다.
    data = [line.strip() for line in open(dest_file_name, "r") if seq_validator(line)]
    # 바코드가 있는 파일을 읽어온다.
    barcode_data = [line for line in open(src_file_name, "r")]

    try:
        # 읽어온 바코드를 속도를 위해 모두 메모리에 올려놓고 분석을 시작한다.
        for barcode in barcode_data:
            # 바코드셋은 :를 구분자로 앞은 파일명, 뒤는 바코드로 되어있다.
            barcode_set = barcode.split(":")
            if len(barcode_set) < 2:
                continue
            # 파일명에서 화이트 스페이스 삭제
            file_name = barcode_set[0].strip()
            # 바코드가 valid한지 검증
            barcode = seq_validator(barcode_set[1].strip())

            used_data = []
            # 대상이 되는 시퀸스들을 하나하나 분석한다.

            # debug
            # line_cnt = 0

            num_detected = 0

            for line in data:
                # 대상 시퀸스 valid 검증 -- duplicate
                # line = seq_validator(line)
                # if line is None:
                #     continue

                # debug
                # flag = False
                # worksheet.write(line_cnt, 0, line)

                # 비교를 위해 바코드, 대상 시퀸스 둘다 소문자로 변환하여 바코드가 대상 시퀸스 내에 존재하는지 검사
                if barcode.lower() in line.lower():
                    # processing buffer
                    used_data.append(line)
                    num_detected += 1

            # 결과가 저장될 파일명 지정
            file_dir = os.path.join(result_folder_name, "{}.txt".format(file_name))

            # 결과 파일 쓰기 시작 -- to xlsx and txt
            extracted_wb = xlsxwriter.Workbook(f"results/{file_name}.xlsx")
            extracted_ws = extracted_wb.add_worksheet("Barcode extraction result")
            spreadsheet_write_cnt = 0
            for datum in used_data:
                extracted_ws.write(spreadsheet_write_cnt, 0, datum)
                spreadsheet_write_cnt += 1
            extracted_wb.close()

            with open(file_dir, "w") as f:
                # 추출된 대상 시퀸스들을 파일에 쓴다.
                for datum in used_data:
                    f.write("{}\n".format(datum))

            # writing a summary
            try:
                result_info_txt.write(f"{file_name} : {num_detected}\n")
                worksheet.write(current_cnt, 0, file_name)
                worksheet.write(current_cnt, 1, ":")
                worksheet.write(current_cnt, 2, num_detected)
            except Exception as e:
                print(e)
                print(
                    "Extraction has been done. But Making a result-info.txt is failed."
                )
                raise
            # 파일에 전부 옮겨담았다면 메모리에 올라간 전체 대상 시퀸스들에서 파일에 쓴 대상 시퀸스를 뺀다. -> bottleneck step; processing time increases about two times without it
            # [data.remove(used_datum) for used_datum in used_data]

            # 프로그램 진행율 계산 부분
            current_cnt += 1
            # progress_percentage = float(current_cnt) / src_line_cnt * 100
            # print("{} %".format(progress_percentage)) ; remove unnecessary floating point calculations
            print(f"{current_cnt} out of {len(barcode_data)} barcodes are processed.")

    except Exception as e:
        print(e)
        print("Extraction Failure.")
        raise

    workbook.close()
    print("--- %s seconds elapsed ---" % (time.time() - start_time))
    result_info_txt.close()


# original code
if __name__ == "__main__":
    # print("Input barcode file name with extension: ")
    # src_file_name = input()
    # src_file_name = os.path.join(BASE_DIR, src_file_name)
    src_file_name = os.path.join(BASE_DIR, "barcode.txt")

    if not os.path.isfile(src_file_name):
        print("File Not Found. Check it is in the src directory")
        raise

    print("Input sequence file name with extension: ")
    dest_file_name = input().strip()
    # dest_file_name = os.path.join(BASE_DIR, dest_file_name)

    if not os.path.isfile(dest_file_name):
        print("File Not Found. Check it is in the src directory")
        raise

    do(src_file_name, dest_file_name)

print("Extraction is completed.")
