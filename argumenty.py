import argparse

import sys
import sys    
import os    
file_name =  os.path.basename(sys.argv[0])
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser(description='Example of use: {} -c lorem ipsum'.format(file_name))
group = parser.add_mutually_exclusive_group()
group.add_argument("-c", "--code", help="Code text into discord emoji", action="store_true", dest="code")
group.add_argument("-d", "--decode", help="Decode discord emoji into text", action="store_true", dest="decode")
parser.add_argument("text", help="Insert text", type=str)
args = parser.parse_args()

if args.decode:
	print("ahoj")
elif args.code:
	print("neahoj")
else:
	parser.print_help()