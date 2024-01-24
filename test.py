# import sys
# print(sys.argv[1])

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str)
args = parser.parse_args()

def treat_args():
    return args.config

if __name__ == '__main__':
    conf_file_name = treat_args()
    print(conf_file_name)