from multithreadcopier import MultiThreadCopier
import os.path
import argparse
import shutil
import logging
import glob


file_log = logging.FileHandler('logging/error.log')
console_out = logging.StreamHandler()

logging.basicConfig(handlers=(file_log, console_out), 
                    format='[%(asctime)s | %(levelname)s]: %(message)s', 
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.ERROR)

parser = argparse.ArgumentParser(description='Copying and moving files')
parser.add_argument(dest='dst', metavar='path', nargs='*')
parser.add_argument('-c', dest='copy', help='pattern for copy files')
parser.add_argument('-m', dest='move', help='pattern for move file or directory')
parser.add_argument('-threads', dest='thread', default=1, help='value threads')

args = parser.parse_args()

def main():
    with MultiThreadCopier(threads=int(args.thread)) as pool:
        if args.copy:
            if os.path.exists:
                if os.path.isfile(os.path.basename(args.copy)):
                    pool.copy(args.copy, args.dst[0])
                elif os.path.isdir(args.copy):
                    try:
                        shutil.copytree(args.copy, args.dst[0], copy_function=pool.copy)
                    except shutil.Error as e:
                        for src, dst, msg in e.args[0]:
                            logging.error(dst, src, msg)
                else:
                    files = glob.iglob(os.path.join(os.path.dirname(args.copy), 
                        os.path.basename(args.copy)))
                    for file in files:
                        if os.path.isfile(file):
                            pool.copy(file, args.dst[0])
            else:
                logging.info("Object does not exist")
        elif args.move:
            if os.path.isfile(args.move) or os.path.isdir(args.move):   
                shutil.move(args.move, args.dst[0], copy_function=pool.copy)
            else:
                files = glob.iglob(os.path.join(os.path.dirname(args.move), 
                        os.path.basename(args.move)))
                for file in files:
                    if os.path.isfile(file):
                        shutil.move(file, args.dst[0], copy_function=pool.copy)

if __name__ == '__main__':
    main()
