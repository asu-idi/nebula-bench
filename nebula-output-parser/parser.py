# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Qiaolin Yu

read_file_path = "research_output_fetch1_reblance_0304.txt"
qps_output_path = "qps_output.txt"
avg_output_path = "avg_output.txt"
p99_output_path = "p99_output.txt"

qps_output = open(qps_output_path, mode='w', encoding='utf-8')
avg_output = open(avg_output_path, mode='w', encoding='utf-8')
p99_output = open(p99_output_path, mode='w', encoding='utf-8')

lines = ""


def parse_qps():
    count = 0
    for line in lines:
        if line.startswith("qps"):
            qps_output.write(line[5:])
            count += 1
            if count == 9:
                count = 0
                qps_output.write("\n")
            else:
                qps_output.write(" ")
    qps_output.close()


def parse_avg():
    count = 0
    for line in lines:
        if line.startswith("latency"):
            load_line = line[9:]
            result = eval(load_line)
            avg_output.write(str(result['avg']))
            count += 1
            if count == 9:
                count = 0
                avg_output.write("\n")
            else:
                avg_output.write(" ")
    avg_output.close()


def parse_p99():
    count = 0
    for line in lines:
        if line.startswith("latency"):
            load_line = line[9:]
            result = eval(load_line)
            p99_output.write(str(result['p(99)']))
            count += 1
            if count == 9:
                count = 0
                p99_output.write("\n")
            else:
                p99_output.write(" ")
    p99_output.close()


def init():
    global lines
    with open(read_file_path, 'r') as read_file:
        content = read_file.read()
    lines = content.split("\n")


if __name__ == '__main__':
    init()
    # parse_qps()
    # parse_avg()
    parse_p99()
