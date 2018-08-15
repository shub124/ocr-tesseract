import sys
import os
from subprocess import call
import argparse

valid_ext = [".jpg",".gif",".png",".tif",".bmp"]
FNULL = open(os.devnull, 'w')

class ArgumentMissingException(Exception):
	def __init__(self):
		print("usage: {} <dirname>".format(sys.argv[0]))
		sys.exit(1)

def create_dir(path):
	if not os.path.exists(path):
	    os.makedirs(path)

def check_path(path):
	return bool(os.path.exists(path))

def main(input_path, output_path):
	if call(['which', 'tesseract']):
		print("tesseract is missing")
	elif check_path(input_path):

		cnt = 0
		val = 0

		for f in os.listdir(input_path):
			ext = os.path.splitext(f)[1]

			if ext.lower() not in valid_ext:
				val += 1
				continue
			else :

				if cnt == 0:
					create_dir(output_path)
				cnt += 1
				img_file = os.path.join(input_path, f)
				filename = os.path.splitext(f)[0]
				filename = ''.join(e for e in filename if e.isalnum() or e == '-')
				text_file_path = os.path.join(output_path, filename)

				call(["tesseract", img_file, text_file_path], stdout=FNULL)

				print(str(cnt) + (" file" if cnt == 1 else " files") + " completed")

		if cnt + val == 0:
			print(" files not  found at your given location")
		else :
			print(str(cnt) + " / " + str(cnt + val) + " output files")
	else :
		print("No directory found at " + format(input_path))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("input_dir")
	parser.add_argument('output_dir', nargs='?')
	args = parser.parse_args()
	input_path = os.path.abspath(args.input_dir)
	if args.output_dir:
		output_path = os.path.abspath(args.output_dir)
	else:
		output_path = os.path.join(input_path,'converted-text')
	main(input_path, output_path)
