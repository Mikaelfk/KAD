import os
import sys
from dotenv import load_dotenv



def file_validation(url, jhove_path):
	os.chdir(jhove_path)

	# Check if operating system is posix or windows
	if os.name == "posix":
		jhovevariable = "./jhove"
	else:
		jhovevariable = "jhove.bat"
		url = url.replace("/", "\\")

	# Runs the file validation and saves the output to a variable
	if url.lower().endswith('.jpg'):
		stream = os.popen(jhovevariable + " -m JPEG-hul -kr " + "\"" + url + "\"")
	elif url.lower().endswith('.tiff'):
		stream = os.popen(jhovevariable + " -m TIFF-hul -kr " + "\"" + url + "\"")
	output = stream.read()

	# Prints a response
	if "Status: Well-Formed and valid" not in output:
		print("File validation failed")
		print(output)
	else:
		print("File validation successful\n")
		print(output)

url1 = "path/to/url" 

load_dotenv()
jhove_path = os.getenv('JHOVE_PATH')
file_validation(url1, jhove_path)