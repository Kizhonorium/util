from multithreadcopier import MultiThreadCopier
import os
import argparse
import shutil
import logging


file_log = logging.FileHandler('logging/error.log')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out), 
                    format='[%(asctime)s | %(levelname)s]: %(message)s', 
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.ERROR)

parser = argparse.ArgumentParser(description='Copying and moving files')
parser.add_argument('--operation', dest='operation', help='pattern for choice operation')
parser.add_argument('--from', dest='_from', help='Path to <from>')
parser.add_argument('--to', dest='_to', help='Path to <to>')
parser.add_argument('--threads', dest='thread', default=1, help='value threads')

args = parser.parse_args()

def main():
    with MultiThreadCopier(threads=int(args.thread)) as pool:
        if args.operation == 'copy':
            if os.path.isdir(args._from):
                pool.copy_tree(args._from, args._to)
            else:
                pool.copy_file_by_extension(args._from, args._to)
        elif args.operation == 'move':
            if os.path.isdir(args._from):
                shutil.move(args._from, args._to, copy_function=pool.copy)
            else:
                pool.copy_file_by_extension(args._from, args._to, copy_function=pool.copy)
        else:
            logging.error(f'There is no such operation {args.operation}')


if __name__ == '__main__':
    main()
