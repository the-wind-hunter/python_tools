# -*- coding: utf-8 -*-
import os
import argparse
import re

def loadFile(file):
    list = [line.strip() for line in open(file, 'r')]
    return list

def compare(list_f , list_fd , result):
    with open(result,"w",) as f:
        for line_f in list_f:
            for line_fd in list_fd:
                if(str(line_fd).startswith(".")):
                    #print(line_fd)
                    if line_f.replace('\n', '').find(line_fd.replace('\n', '')) >= 0:
                        print(line_fd.replace('\n', '') + ' in ' + line_f.replace('\n', ''))
                        try:
                            f.writelines(line_f + '\n')
                        except:
                            continue
                else:
                    tmp_str = line_f.replace('\n', '').replace('http://', '').replace('https://', '')
                    tmp_str = re.sub('(?<=:).*', '', tmp_str)
                    tmp_str = tmp_str.replace(':', '')
                    #print("test----" + tmp_str)
                    if tmp_str == (line_fd.replace('\n', '')):
                        print(line_fd.replace('\n', '') + ' in ' + line_f.replace('\n', ''))
                        try:
                            f.writelines(line_f + '\n')
                        except:
                            continue

    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="== Query whether a line is in another file ==")
    parser.add_argument('-f', '--file', type=str, help="file path")
    parser.add_argument('-fd', '--file_DB', type=str, help="File as database path")
    parser.add_argument('-r', '--result', type=str, help="result")
    args = parser.parse_args()

    if args.file == 0 or args.file_DB == 0:
        print("[-]wrong！请输入-f 被比对的文件和-fd 数据源文件！")
    if args.file and args.file_DB and args.result:
        list_f = loadFile(args.file)
        list_fd = loadFile(args.file_DB)
        compare(list_f , list_fd , args.result)
    else:
        print("[-]wrong！For example:\n >> python3 is_include.py -f test.txt -fd test_db.txt -r result.txt\n  (It can make u know if the domain in test.txt is you want)")
    

