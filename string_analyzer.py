import os
import re
import sys, getopt
from termcolor import colored

regex = '"(.+)"'
size_all=0
BOT_NOTIFY_ERROR = 'BOT_NOTIFY_.*\("(.+)"\)'
#regex = BOT_NOTIFY_ERROR 
#regex = '\("(.+)"\)'

def line_check(line, index): 
        global size_all
        print(colored('line','green'),colored(index,'green'),colored(': ','green') ,colored(line, 'yellow'),colored(' + "\\0"','magenta'))
        line_len=(len(line)+1)
        modulo = line_len%4
        size = line_len//4
        if modulo:
            size=size+1
        print('\t  len=', line_len,'\tmodulo=', modulo, '\tmemory usage: ARM words=', size ,' bytes =', size*2 )
        size_all = size_all + size

def find_regexp(file):
    with open(file, 'r') as f:
        raw_strings = f.readlines()

    for idx, line in enumerate(raw_strings):
        result = re.findall(regex, line)
        if result:
            line_check(result[0], idx+1)


def main(argv):
    os.system('cls' if os.name == 'nt' else 'clear');
    opts, args = getopt.getopt(argv,"hf:",["file"])
    for opt, arg in opts:
        if opt == '-h':
            print ('Syntax should be:\r\n python3 string_analyzer.py -f test.c')
        elif opt in ("-f", "--file"):
            print(arg)
            find_regexp(arg)
    print(colored('Total size:','cyan'),size_all, ' in bytes:',size_all*4)

if __name__ == "__main__":
   main(sys.argv[1:])